# Calling C++ from Python

Every technique in this document — ctypes, cffi, Cython, SWIG, Boost.Python,
pybind11, nanobind — solves the same problem in the same place. Once you see
what that place is, the whole landscape collapses into one picture and choosing
becomes easy.

All the code referenced here lives in
[`calling_cpp_from_python/`](calling_cpp_from_python/) and is runnable:

```bash
cd docs/calling_cpp_from_python
pip install pybind11 nanobind cython cffi swig numpy setuptools
./run_all.sh          # builds and runs all 7 examples
python bench.py         # measures per-call overhead of each
```

---

## Table of contents

1. [The one mental model](#1-the-one-mental-model)
2. [What actually crosses the boundary](#2-what-actually-crosses-the-boundary)
3. [The menu, and what people actually use](#3-the-menu-and-what-people-actually-use)
4. [How a call works, step by step](#4-how-a-call-works-step-by-step)
5. [How data is passed: the three modes](#5-how-data-is-passed-the-three-modes)
6. [`std::vector<T>` — the four answers](#6-stdvectort--the-four-answers)
7. [Classes, ownership and lifetime](#7-classes-ownership-and-lifetime)
8. [Exceptions](#8-exceptions)
9. [The GIL and threading](#9-the-gil-and-threading)
10. [How the big projects actually do it](#10-how-the-big-projects-actually-do-it)
11. [Measured overhead](#11-measured-overhead)
12. [Packaging and shipping](#12-packaging-and-shipping)
13. [Which one should you use?](#13-which-one-should-you-use)
14. [The bugs everyone hits](#14-the-bugs-everyone-hits)

---

## 1. The one mental model

CPython can load a **shared library** (`.so` / `.pyd` / `.dylib`) at runtime and
call functions in it. That is the entire foundation. There are exactly **two**
ways to use it:

**Path A — the extension module.** You build a `.so` that exports one specially
named function, `PyInit_<modulename>`. When you write `import foo`, CPython
finds `foo.cpython-312-x86_64-linux-gnu.so`, `dlopen()`s it, calls
`PyInit_foo()`, and gets back a module object full of functions and types. The
`.so` is linked against the CPython runtime and speaks `PyObject*` fluently.

**Path B — the plain shared library.** You build an ordinary `.so` that knows
nothing about Python. Something on the Python side (`ctypes`) `dlopen()`s it,
looks up symbols by name, and pushes raw C values across by hand.

```
                    ┌──────────────────── Path A ────────────────────┐
                    │  a real CPython extension module               │
Python code  ──────►│  PyInit_foo() → module with functions & types  │
                    │  Cython · SWIG · Boost.Python · pybind11 ·     │
                    │  nanobind · cffi(API mode) · raw Python.h      │
                    └───────────────────────────────────────────────┘

                    ┌──────────────────── Path B ────────────────────┐
Python code  ──────►│  dlopen() a plain C .so, call symbols by name  │
                    │  ctypes · cffi(ABI mode)                      │
                    └───────────────────────────────────────────────┘
```

Two consequences fall out immediately, and they explain almost every tradeoff
in this document:

- **Path B can only speak C.** C++ names are mangled (`_ZN7mathlib3addEdd`), C++
  objects have no stable layout, templates do not exist as symbols, and C++
  exceptions cannot unwind through C frames. So to use ctypes on a C++ library
  you must hand-write a flat `extern "C"` shim — see
  [`cpp/c_api.h`](calling_cpp_from_python/cpp/c_api.h). That shim is the tax.
- **Path A tools differ only in how you describe your API.** Raw `Python.h` = you
  write the glue by hand. SWIG = you write a `.i` file and a generator writes
  the glue. Cython = you write a `.pyx` hybrid language. pybind11/nanobind = you
  describe the API in ordinary C++ and templates generate the glue at compile
  time. **Same output, different authoring experience.**

Everything below is detail on those two paths.

---

## 2. What actually crosses the boundary

Nothing "shared" crosses. There are two universes with incompatible
representations, and *something* must translate at every call:

| | Python | C++ |
|---|---|---|
| integer | `PyLongObject`, arbitrary precision, heap, refcounted | `int` / `int64_t`, fixed width, register |
| float | `PyFloatObject` (boxed) | `double` (unboxed) |
| text | `str`, UTF-8/16/32 internally | `std::string` (bytes), `const char*` |
| list of numbers | array of `PyObject*` pointers to boxed floats | `std::vector<double>`, contiguous doubles |
| object | refcounted `PyObject*` | value / `unique_ptr` / `shared_ptr` / raw pointer |
| error | exception object set on the thread state | `throw` + stack unwinding |
| lifetime | garbage collected (refcount + cycle GC) | RAII, scopes, ownership |

Note the fourth row, because it is the one that costs real money: a Python
`list` of 1,000,000 floats is a **million pointers to a million heap-allocated
boxed float objects**. A `std::vector<double>` is **one contiguous 8 MB block**.
They are not the same shape, so converting between them cannot be free — it is
a million allocations and a million pointer chases.

This is precisely why NumPy exists, and why "pass a NumPy array, not a list" is
the single highest-leverage rule in this entire document. A `np.ndarray` is
already a contiguous C buffer with a dtype and shape — it has the *same memory
layout* as `std::vector<double>`, so it can cross the boundary with **zero
copying**, just by handing over a pointer.

The three things a binding layer must do on every call:

1. **Convert** (or expose) arguments Python → C++.
2. **Call** the C++ function.
3. **Convert** (or wrap) the result C++ → Python, and translate any exception.

A "binding tool" is just a way of generating steps 1 and 3.

---

## 3. The menu, and what people actually use

| Tool | Path | You write | C++ classes/templates | Best at | Status in 2026 |
|---|---|---|---|---|---|
| **pybind11** | A | C++ | ✅ native | binding real C++ | **The default.** Most widely used by a wide margin |
| **nanobind** | A | C++ | ✅ native | same, but leaner | Rising fast; same author as pybind11 |
| **Cython** | A | `.pyx` hybrid | ✅ good | numeric code + bindings together | Very widely used (SciPy, pandas, scikit-learn) |
| **ctypes** | B | pure Python | ❌ needs C shim | quick calls into an existing **C** lib | Stdlib, zero setup, universally available |
| **cffi** | A or B | Python + C decls | ❌ needs C shim | same as ctypes but safer/faster | Common; the PyPy-friendly choice |
| **SWIG** | A | `.i` interface | ⚠️ partial | one binding → many languages | Legacy; still alive where Java/C# also needed |
| **Boost.Python** | A | C++ | ✅ native | — | Legacy. pybind11 is its spiritual successor |
| **raw `Python.h`** | A | C | ✅ (by hand) | absolute control | Only NumPy-tier projects do this |
| **cppyy** | A | nothing | ✅ automatic | exploratory / no build step | Niche, powerful (uses Cling JIT) |

### Which is "the one"?

**pybind11.** If you have a C++ codebase and want it callable from Python, this
is the answer roughly 80% of the time, and it is what you should learn first.
It is header-only (just `pip install pybind11`), needs no separate code
generator or interface language, understands C++ natively — classes,
inheritance, templates, `std::` containers, smart pointers, lambdas, operator
overloading — and it integrates with NumPy and Eigen out of the box.

The short version of the rest:

- **nanobind** if you are starting fresh, can require C++17, and care about
  binary size or compile times. In our identical test module: **pybind11 230 KB,
  nanobind 128 KB**, and nanobind was measurably faster per call. The API is
  close enough that porting is mostly `s/py::/nb::/`.
- **Cython** if the goal is *speeding up Python*, not merely *reaching C++*. Its
  superpower is that the same file can contain hot loops compiled to C++ **and**
  the glue. This is why the scientific stack is built on it.
- **ctypes** if the library is plain C, you only need a handful of functions,
  and you do not want a build step at all. Pure Python, stdlib, no compiler.
- **cffi** for the same job as ctypes but with the signatures checked by a real
  C compiler — and ~3× lower call overhead.
- **SWIG** essentially only if you must also emit Java/C#/Ruby bindings from the
  same source.
- **Boost.Python** only in codebases that already use it.

---

## 4. How a call works, step by step

Take the pybind11 binding from
[`04_pybind11/bindings.cpp`](calling_cpp_from_python/04_pybind11/bindings.cpp):

```cpp
m.def("add", &mathlib::add, "a"_a, "b"_a);
```

When Python executes `mathlib_pb.add(2.0, 3.0)`:

1. **CPython** evaluates the call, packs the arguments, and invokes the C
   function pointer stored in the module's function object.
2. **pybind11's dispatcher** receives the raw `PyObject*` arguments. If the name
   has several overloads it tries each in turn.
3. **Type casters** run. `type_caster<double>::load(PyObject*)` checks the object
   is float-like and calls `PyFloat_AsDouble()` → a real machine `double`.
   *A failure here is what produces `TypeError: incompatible function
   arguments`, and it is the reason a wrong type raises instead of segfaulting
   the way ctypes would.*
4. **The actual C++ function runs** — `mathlib::add(2.0, 3.0)`. At this point
   there is no Python involved, it is a plain function call on unboxed doubles.
5. **The return caster** runs: `type_caster<double>::cast(5.0)` →
   `PyFloat_FromDouble(5.0)` → a new `PyObject*` with refcount 1.
6. **If C++ threw**, the exception is caught at the boundary and translated to a
   Python exception (`std::invalid_argument` → `ValueError`), which is *set* on
   the thread state while the C function returns `nullptr`.

Steps 1, 2, 3, 5 and 6 are pure overhead — measured at ~44 ns for pybind11 in
[§11](#11-measured-overhead). Step 4 is the work you actually wanted. **The
whole art of binding design is making step 4 large relative to the rest.** One
call that processes a 10-million-element array is excellent; ten million calls
that each add two numbers is a catastrophe.

The magic that makes `&mathlib::add` "just work" is that pybind11 reads the
function's **type signature at compile time** via templates, and instantiates
the right casters. Nothing is parsed, nothing is generated on disk, and if you
get a type wrong it is a compile error rather than a runtime crash.

---

## 5. How data is passed: the three modes

Every single question of the form "how do I pass X?" reduces to picking one of
these three.

### Mode 1 — Copy / convert (by value)

The binding layer builds a new object on the other side. Simple, safe, always
correct, and O(n).

```cpp
#include <pybind11/stl.h>                       // enables the conversions
m.def("sum_doubles", &sum_doubles);             // takes const std::vector<double>&
```
```python
sum_doubles([1, 2, 3])          # list  -> new std::vector<double>
sum_doubles((1, 2, 3))          # tuple -> works too
sum_doubles(np.arange(4.0))     # any iterable of floats works
```

With `<pybind11/stl.h>` included, these convert automatically **in both
directions**:

| C++ | Python |
|---|---|
| `std::vector<T>`, `std::array<T,N>`, `std::list<T>` | `list` |
| `std::map<K,V>`, `std::unordered_map<K,V>` | `dict` |
| `std::set<T>`, `std::unordered_set<T>` | `set` |
| `std::pair<A,B>`, `std::tuple<...>` | `tuple` |
| `std::string`, `const char*` | `str` (UTF-8) |
| `std::optional<T>` | `T` or `None` |
| `std::variant<...>` | the corresponding type |
| `std::function<R(Args...)>` | any callable |

That last row is worth noticing: **callbacks work in both directions.** A C++
function taking `std::function<double(double)>` can be handed a Python lambda,
and pybind11 will call back into Python for each invocation.

> ⚠️ The `#include` is what enables this. If you forget `<pybind11/stl.h>`, a
> `std::vector<double>` argument becomes an opaque, unusable Python object and
> the error message will not tell you why.

### Mode 2 — Reference / handle (by pointer)

Python holds an **opaque handle** to a C++ object living in C++ memory. Nothing
is converted; method calls are forwarded. This is how classes are bound.

```cpp
py::class_<mathlib::Accumulator>(m, "Accumulator")
    .def(py::init<double, std::string>())
    .def("add", &mathlib::Accumulator::add);
```
```python
acc = mathlib_pb.Accumulator(1.0, "acc")   # C++ object allocated, Python holds a handle
acc.add(2.0)                               # forwarded to C++, no conversion
```

O(1) per call, and state persists in C++. The catch is **lifetime**, which is
[§7](#7-classes-ownership-and-lifetime).

### Mode 3 — Shared buffer (zero copy)

Both sides point at *the same memory*. Nothing is copied or converted; only a
pointer, a dtype, a shape and strides are exchanged. This is how you move
gigabytes for free, and it is the entire basis of the scientific Python stack.

```cpp
m.def("scale_inplace",
      [](py::array_t<double, py::array::c_style | py::array::forcecast> arr,
         double factor) {
        py::buffer_info buf = arr.request();     // pointer + shape + strides
        py::gil_scoped_release release;          // let other threads run
        mathlib::scale_inplace(static_cast<double*>(buf.ptr),
                               static_cast<std::size_t>(buf.size), factor);
      });
```
```python
arr = np.arange(5, dtype=np.float64)
mathlib_pb.scale_inplace(arr, 10.0)
print(arr)          # [ 0. 10. 20. 30. 40.]  — C++ wrote into NumPy's own memory
```

The interchange contracts that make this possible:

- **The buffer protocol** (`PEP 3118`) — CPython's native "here is my raw memory
  plus its layout" interface. `memoryview`, `bytes`, `array.array` and
  `np.ndarray` all speak it. pybind11 exposes it as `py::buffer` /
  `py::array_t`; Cython exposes it as typed memoryviews (`double[::1]`).
- **`__array_interface__` / `__cuda_array_interface__`** — NumPy's older
  dict-based protocol, still widely supported.
- **DLPack** — the cross-framework standard (NumPy, PyTorch, TensorFlow, JAX,
  CuPy). This is what nanobind's `nb::ndarray` targets, which is why one
  nanobind signature accepts a NumPy array *and* a Torch tensor.

Two rules keep Mode 3 safe:

1. **The dtype must match exactly.** `double*` needs `float64`. Hand it an
   `int64` array and you either get a silent reinterpretation of the bits or an
   error, depending on how you declared the caster. `forcecast` (pybind11) will
   convert-and-copy rather than fail — convenient, but it silently removes the
   zero-copy property, so use it deliberately.
2. **Someone must keep the memory alive.** See the `base`/keep-alive discussion
   in [§6](#6-stdvectort--the-four-answers) and [§7](#7-classes-ownership-and-lifetime).

---

## 6. `std::vector<T>` — the four answers

This is the most common concrete question, so it gets its own section. The
runnable version is
[`07_vectors/vectors.cpp`](calling_cpp_from_python/07_vectors/vectors.cpp) +
[`run_vectors.py`](calling_cpp_from_python/07_vectors/run_vectors.py); the output
quoted below is real.

There is no single right answer — there are four, and they differ in **cost**
and, more importantly, in **whether Python mutations reach C++**.

### (A) Automatic conversion → `list` (copies)

```cpp
#include <pybind11/stl.h>
m.def("make_doubles", &make_doubles);   // returns std::vector<double>
```
```
make_doubles(5) -> [1.0, 2.0, 3.0, 4.0, 5.0]   <class 'list'>
```

The default, and usually right. A real Python `list`, works with every Python
idiom. Costs one full element-by-element copy per crossing — and each element
gets boxed into a `PyFloat`.

**The trap.** Because it copies, a vector exposed as a property is a *snapshot*:

```python
copy = cloud.values_copy      # def_property_readonly returning std::vector<double>
copy[0] = -1000.0             # edits the Python list
cloud.sum()                   # 10.0 — UNCHANGED. The C++ vector never saw it.
```

This silently-does-nothing behaviour is the #1 surprise in pybind11. If Python
must mutate the real vector, use (B) or (C).

### (B) Opaque binding → a real `VectorInt` class (no copy, mutable)

```cpp
PYBIND11_MAKE_OPAQUE(std::vector<int>);          // must come BEFORE any binding
// ...
py::bind_vector<std::vector<int>>(m, "VectorInt");
```
```python
vi = v.VectorInt()
vi.append(10); vi.extend([20, 30])
vi[0] = 99
v.sum_ints(vi)        # 149 — C++ sees the mutation
```

`PYBIND11_MAKE_OPAQUE` switches off the automatic copy-conversion for that exact
type, and `bind_vector` gives you a Python class with `append`, `extend`,
`__len__`, `__getitem__`, `__setitem__`, slicing and iteration. Nothing is
copied at the boundary and mutations are two-way.

Cost: it is not a `list`. Anything expecting a real list needs `list(vi)`, and
element access still pays a boundary crossing each time — so it is a poor choice
for numeric bulk work. Use it for modest, genuinely mutable containers.

### (C) NumPy view → zero copy (the right answer for numeric data)

```cpp
.def("values_view", [](py::object self) {
    Cloud& c = self.cast<Cloud&>();
    return py::array_t<double>(
        {static_cast<py::ssize_t>(c.values.size())},   // shape
        {sizeof(double)},                              // strides in BYTES
        c.values.data(),                               // the raw pointer
        self);                                         // base object = keep-alive
})
```
```python
view = cloud.values_view()
view.flags.owndata      # False  — it is a view, not a copy
view.base is cloud      # True   — the Cloud cannot be collected while view lives
view[0] = -1000.0
cloud.sum()             # -990.0 — the C++ vector really changed
```

Zero copy, full NumPy vectorisation on top of C++-owned memory. Two hazards:

- **Omit the `base` argument and you get a use-after-free.** Without it, the
  `Cloud` can be garbage-collected while the array still points into its
  buffer. The symptom is garbage numbers or a crash, far from the cause.
- **Reallocation invalidates the view.** If C++ later `push_back()`s and the
  vector grows, its buffer moves and your view dangles. Only expose views onto
  buffers whose size is stable for the view's lifetime.

### (C′) C++ allocates, NumPy takes ownership (capsule)

For "compute a big result in C++ and hand it to Python" — no copy, no lifetime
puzzle, because NumPy owns the vector and deletes it:

```cpp
auto* v = new std::vector<double>(make_doubles(n));
py::capsule owner(v, [](void* p) { delete reinterpret_cast<std::vector<double>*>(p); });
return py::array_t<double>({(py::ssize_t)v->size()}, {sizeof(double)}, v->data(), owner);
```
```python
a = v.make_array_no_copy(6)
type(a.base)     # PyCapsule — holds the deleter; fires when the array dies
```

### (D) `std::vector<SomeStruct>` → `list[Struct]`

Bind the element type as a class; the vector then converts elementwise:

```cpp
py::class_<Point>(m, "Point")
    .def(py::init<>())
    .def_readwrite("x", &Point::x)
    .def_readwrite("y", &Point::y)
    .def_readwrite("label", &Point::label);
```
```python
cloud.points[:2]   # [Point(x=0.0, y=0.0, label='p0'), Point(x=1.0, y=1.0, label='p1')]
```

Correct and readable, but for a million records it is a million Python objects.
When the struct is plain-old-data and performance matters, prefer either a NumPy
**structured dtype** over the same memory, or **struct-of-arrays** (one
contiguous array per field). Both keep you in Mode 3.

### Choosing

| Situation | Use |
|---|---|
| Small vector, returned once | **(A)** — let it copy, keep it simple |
| Large numeric buffer, C++ owns it | **(C)** view with a keep-alive `base` |
| Large numeric buffer, C++ hands it over | **(C′)** capsule |
| Python must mutate in place | **(B)** `bind_vector` |
| Vector of records | **(D)**, or structured dtype / struct-of-arrays |

**Cython equivalents:** (A) is automatic (`vector[double]` ↔ `list` when you
`from libcpp.vector cimport vector`); (C) is a typed memoryview, `double[::1]`.
**nanobind equivalents:** `nb::bind_vector` and `nb::ndarray`.

---

## 7. Classes, ownership and lifetime

Binding a class is the point where the toolchains genuinely diverge, so compare
the same `Accumulator` across all of them. The C++ is
[`cpp/mathlib.hpp`](calling_cpp_from_python/cpp/mathlib.hpp).

**pybind11** — declarative, and the object's lifetime is handled for you:

```cpp
py::class_<mathlib::Accumulator>(m, "Accumulator")
    .def(py::init<double, std::string>(), "start"_a = 0.0, "name"_a = "acc")
    .def("add", &mathlib::Accumulator::add, "value"_a)
    .def_property_readonly("total", &mathlib::Accumulator::total)
    .def_property("name", &mathlib::Accumulator::name, &mathlib::Accumulator::set_name)
    .def("__len__", &mathlib::Accumulator::size)
    .def("__repr__", [](const mathlib::Accumulator& a) { /* ... */ });
```

**ctypes** — the class does not exist. You write an opaque-pointer C shim
(`ml_acc_create` / `ml_acc_add` / `ml_acc_destroy` / …), declare every signature
by hand, then hand-write a Python wrapper class **including its destructor**:

```python
class Accumulator:
    def __init__(self, start=0.0, name="acc"):
        self._handle = lib.ml_acc_create(start, name.encode())
        if not self._handle:
            raise MemoryError
    def close(self):
        if self._handle:
            lib.ml_acc_destroy(self._handle)   # forget this and you leak
            self._handle = None
    def __del__(self):
        self.close()
```

Compare the file sizes in the repo: the ctypes version needs
[`c_api.h`](calling_cpp_from_python/cpp/c_api.h) +
[`c_api.cpp`](calling_cpp_from_python/cpp/c_api.cpp) +
[`run_ctypes.py`](calling_cpp_from_python/01_ctypes/run_ctypes.py) to achieve
what pybind11 does in the 15 lines above. **That ratio is the single strongest
practical argument for pybind11.**

**Cython** — `cdef class` holds the pointer; `__dealloc__` is guaranteed to run:

```cython
cdef class PyAccumulator:
    cdef Accumulator* _thisptr
    def __cinit__(self, double start=0.0, str name="acc"):
        self._thisptr = new Accumulator(start, name.encode())
    def __dealloc__(self):
        del self._thisptr
```

### Ownership rules that matter

By default pybind11 stores the C++ object in a `std::unique_ptr` holder and
destroys it when the Python object's refcount hits zero. Two situations need
your attention:

**Returning a pointer/reference to something you do not own.** Use a
`return_value_policy`:

| Policy | Meaning |
|---|---|
| `automatic` (default) | copy for values, take ownership for pointers |
| `copy` | always copy — safest |
| `reference` | Python gets a non-owning view; **C++ must outlive it** |
| `reference_internal` | non-owning, tied to the parent's lifetime (for getters) |
| `take_ownership` | Python will `delete` it |

**Keeping a parent alive.** If a returned object points into a parent, say so:

```cpp
.def("get_child", &Parent::get_child, py::keep_alive<0, 1>())
//  keep_alive<Nurse, Patient>: 0 = return value, 1 = `this`
//  "keep argument 1 alive as long as the return value lives"
```

Getting this wrong produces use-after-free bugs that appear as corrupted data
long after the call. If you use `shared_ptr` in C++, declare it as the holder —
`py::class_<T, std::shared_ptr<T>>` — so refcounts on both sides stay coherent.

---

## 8. Exceptions

A C++ exception must never unwind through CPython's C frames — that is
undefined behaviour, usually a hard crash. Every binding layer catches at the
boundary.

**pybind11 / nanobind** do it automatically, with a default table:

| C++ | Python |
|---|---|
| `std::invalid_argument`, `std::domain_error` | `ValueError` |
| `std::out_of_range`, `std::length_error` | `IndexError` / `ValueError` |
| `std::runtime_error` | `RuntimeError` |
| `std::bad_alloc` | `MemoryError` |
| `std::exception` (anything else) | `RuntimeError` |

```python
mathlib_pb.divide(1.0, 0.0)      # ValueError: division by zero
```

Custom types: `py::register_exception<MyError>(m, "MyError");`

**Cython** needs the `except +` annotation — omit it and a throw terminates the
process:

```cython
double c_divide "mathlib::divide"(double a, double b) except +
```

**SWIG** needs an explicit `%exception` block (see
[`06_swig/mathlib.i`](calling_cpp_from_python/06_swig/mathlib.i)).

**ctypes/cffi** cannot do it at all — exceptions do not cross a C ABI. Your shim
must catch everything and return a status code, and the Python wrapper turns
that code back into an exception:

```cpp
int ml_divide(double a, double b, double* out) {
  try { *out = mathlib::divide(a, b); return 0; }
  catch (const std::exception&) { return 1; }
}
```

---

## 9. The GIL and threading

The Global Interpreter Lock is held whenever Python code runs. Your C++ function
inherits it, which means **a long C++ call blocks every other Python thread** —
unless you release it:

```cpp
py::gil_scoped_release release;      // release for this scope
// ... long C++ work, touching NO Python objects ...
```                                   // GIL reacquired on scope exit

This is how you get real multithreaded parallelism out of Python: release the
GIL, run OpenMP/TBB/`std::thread` inside C++, reacquire on the way out. NumPy,
PyTorch and OpenCV all do exactly this in their heavy kernels.

The absolute rule: **while the GIL is released you may not touch any
`PyObject*`** — no Python containers, no `py::object`, no exceptions carrying
Python state. If a C++ thread needs to call back into Python, it must first
acquire the GIL with `py::gil_scoped_acquire`.

(Free-threaded CPython 3.13+ removes the GIL, but the discipline is unchanged
and arguably more important: your C++ must then be genuinely thread-safe.)

---

## 10. How the big projects actually do it

This is the most instructive part, because the answers are not uniform — each
project's choice follows from its constraints.

### OpenCV → a bespoke generator that parses its own headers

`cv2` is **not** pybind11 or SWIG. OpenCV has thousands of functions, so it
built its own generator (`modules/python/src2/`): `hdr_parser.py` parses the C++
headers, `gen2.py` emits `pyopencv_generated_*.h`, and everything is compiled
into one large `cv2` extension module.

The mechanism is worth stealing: OpenCV **annotates its own headers** with
macros marking what should be exported.

```cpp
CV_EXPORTS_W void GaussianBlur(InputArray src, OutputArray dst, Size ksize,
                               double sigmaX, double sigmaY = 0, ...);
//        ^^^ "W" = wrap this for the bindings
class CV_EXPORTS_W CascadeClassifier {
    CV_WRAP void detectMultiScale(InputArray image, CV_OUT std::vector<Rect>& objects, ...);
};
```

`CV_WRAP`, `CV_OUT`, `CV_IN_OUT` are no-ops for the C++ compiler and directives
for the generator. Conversion is done by overloads of `pyopencv_to(PyObject*,
T&)` / `pyopencv_from(const T&)` written once per type. `CV_OUT` on a reference
parameter is why `detectMultiScale` **returns** its results in Python instead of
taking an out-parameter — a very Pythonic API generated from a very C++ one.

The `cv::Mat` ↔ `np.ndarray` bridge is pure Mode 3: OpenCV installs a custom
`MatAllocator` (`NumpyAllocator`) so a `cv::Mat` created during a Python call
allocates its pixels **through NumPy**, and refcounts are shared. So
`cv2.imread()` returns an array that owns its buffer, and passing an array into
a `cv2` function copies nothing.

**Lesson:** at OpenCV's scale, and with Java/JS bindings generated from the same
parse, a custom generator pays for itself. Below that scale it does not — do not
imitate this.

### Eigen → there is nothing to bind; NumPy *is* the Python side

Eigen is a header-only template library, and templates have no symbols to bind.
There is no "Eigen for Python" — the Python equivalent of an `Eigen::MatrixXd`
is an `np.ndarray`. What you bind is *your* function that happens to take Eigen
types, and pybind11 supplies the casters:

```cpp
#include <pybind11/eigen.h>

// (1) by value / const ref -> COPIES, but accepts any compatible array
m.def("solve", [](const Eigen::MatrixXd& A, const Eigen::VectorXd& b) {
    return A.colPivHouseholderQr().solve(b);      // returns -> new NumPy array
});

// (2) Eigen::Ref -> ZERO COPY view; C++ writes straight into NumPy's buffer
m.def("scale", [](Eigen::Ref<Eigen::VectorXd> v, double f) { v *= f; });
```

```python
A = np.random.rand(3, 3); b = np.random.rand(3)
x = mymod.solve(A, b)      # A, b copied into Eigen; result copied back to NumPy
```

The classic gotcha: **Eigen defaults to column-major, NumPy defaults to
row-major.** A mismatch makes `Eigen::Ref<MatrixXd>` silently fall back to
copying (or refuse the argument). Fixes: use
`Eigen::Ref<Eigen::Matrix<double, Dynamic, Dynamic, Eigen::RowMajor>>`, or pass
`np.asfortranarray(A)`, or accept the copy for small matrices. Vectors are 1-D
and unaffected.

`Eigen::Ref<const MatrixXd>` accepts anything and copies when it must —
convenient, but it means "zero copy" is no longer guaranteed. nanobind offers
the same via `nanobind/eigen/dense.h`.

**Lesson:** the header-only/template case is the general case for modern C++ —
you bind concrete instantiations of *your* functions, never the template
library itself.

### The rest of the ecosystem

| Project | Technique | Why |
|---|---|---|
| **PyTorch** | **pybind11** | Huge C++ core, deep class hierarchies, `torch.utils.cpp_extension` hands the same tool to users |
| **TensorFlow** | **pybind11** (migrated from SWIG) | The migration is a good summary of the industry's verdict |
| **NumPy** | raw CPython C API | It *is* the foundation; it cannot depend on a binding library |
| **SciPy** | **Cython** + f2py + C | Wrapping Fortran/C numerics and writing hot loops in the same place |
| **pandas** | **Cython** | Same: performance-critical loops living next to the glue |
| **scikit-learn** | **Cython** | Same |
| **OpenCV** | custom generator | Scale + multi-language output |
| **PyQt / PySide** | SIP / Shiboken | Qt-specific generators handling signals/slots and moc |
| **llvmlite** | C shim + **ctypes** | Deliberately keeps a stable C ABI in the middle |

The pattern: **new C++ projects choose pybind11 (or nanobind). Projects whose
problem is "make Python numerics fast" choose Cython. Projects at extreme scale
or with multi-language needs write a generator. ctypes shows up where a stable C
ABI already exists.**

---

## 11. Measured overhead

From [`bench.py`](calling_cpp_from_python/bench.py) — best of 7 runs of 200,000
calls of `add(2.0, 3.0)`, so this is *almost entirely* boundary-crossing cost,
not arithmetic. (Linux, GCC, CPython 3.12, `-O2`.)

```
  technique              ns/call   vs fastest
  --------------------------------------------
  python (baseline)           12         1.0x
  Cython                      26         2.2x
  nanobind                    29         2.4x
  pybind11                    44         3.6x
  SWIG                        51         4.3x
  cffi (API mode)             71         5.9x
  ctypes                     197        16.3x
```

> Measure this yourself before quoting it. A *single* timing run of a
> sub-100 ns operation is badly noisy — on this machine individual runs
> disagreed by 2–3× and even reordered the table. `bench.py` takes the min of 7
> repeats, which reproduces to ±1 ns across invocations. Absolute numbers still
> depend on compiler, flags and CPU; the *ratios* are the durable part.

Module size, same functionality, same compiler flags:

```
  nanobind   128 KB
  SWIG       171 KB
  pybind11   230 KB
```

How to read this:

- **Calling C++ to do a tiny amount of work is a net loss.** Adding two floats in
  pure Python costs 12 ns; going to C++ to do it costs 26–197 ns. Batch your
  work — one call over an array, not one call per element.
- **ctypes is 3–7× slower than everything else**, because it re-derives the call
  at runtime from your `argtypes` instead of compiling it. Fine for setup and
  configuration calls, bad in a loop. This is the one genuinely large gap in the
  table.
- **The compiled tools cluster in a 26–71 ns band.** Do not choose between
  pybind11, nanobind, Cython and SWIG on these numbers — choose on ergonomics
  and C++ feature support. The difference vanishes the moment step 4 does real
  work: at 1 µs of C++ per call, a 20 ns difference is 2%.
- **nanobind is leaner than pybind11 on both axes** (29 vs 44 ns, 128 vs 230 KB),
  which is exactly its stated goal.
- **Cython is fastest here** because `add` compiles to a direct C call with
  minimal dispatch — it has the least generic machinery to traverse.
- **cffi lands behind the C++-native binders**, but it is still ~2.8× faster than
  ctypes, which is the comparison that matters when choosing between those two.

---

## 12. Packaging and shipping

The modern standard for a pybind11/nanobind project is **scikit-build-core**,
which lets `pip install .` drive your existing CMake build:

```toml
# pyproject.toml
[build-system]
requires = ["scikit-build-core>=0.10", "pybind11>=2.12"]
build-backend = "scikit_build_core.build"

[project]
name = "mathlib"
version = "0.1.0"
requires-python = ">=3.9"

[tool.scikit-build]
minimum-version = "0.10"
cmake.version = ">=3.18"
wheel.expand-macos-universal-tags = true
```

with a `CMakeLists.txt` like
[`04_pybind11/CMakeLists.txt`](calling_cpp_from_python/04_pybind11/CMakeLists.txt)
plus `install(TARGETS mathlib_pb DESTINATION .)`. Then `pip install .` or
`python -m build` just works.

Points that bite people:

- **Binary wheels are per (Python version × OS × architecture).** Use
  [`cibuildwheel`](https://cibuildwheel.pypa.io/) in CI to produce the matrix;
  hand-building is not viable. (This repo's
  [act tutorial](run_github_actions_locally_with_act.md) is handy for testing
  that workflow locally.)
- **`Development.Module`, not `Development`,** in `find_package(Python ...)` —
  extension modules must not link `libpython`, or manylinux/macOS wheels break.
- **The ABI is version-specific.** A module built for 3.11 will not import in
  3.12. The **stable ABI** (`Py_LIMITED_API`) avoids this — nanobind supports it
  well, pybind11 partially — at the cost of some features.
- **Ship type stubs.** A compiled module is opaque to editors and mypy until you
  provide a `.pyi`. nanobind generates them via `nanobind_add_stub` (see
  [`05_nanobind/CMakeLists.txt`](calling_cpp_from_python/05_nanobind/CMakeLists.txt));
  pybind11 users run `pybind11-stubgen`. Our nanobind build produces:

  ```python
  def add(a: float, b: float) -> float:
      """Add two numbers"""

  class Accumulator:
      def __init__(self, start: float = 0.0, name: str = 'acc') -> None: ...
      @property
      def total(self) -> float: ...
  ```

- **Match the C++ runtime.** Mixing libstdc++ versions, or a debug CPython with a
  release module, produces import errors and crashes that look like nothing.

---

## 13. Which one should you use?

```
Is the library plain C (no C++ classes)?
├─ yes ─► Just a few functions, no build step wanted?   ──► ctypes
│         Want compiler-checked signatures / speed?     ──► cffi (API mode)
└─ no  ─► It's C++
          │
          ├─ Goal is "speed up my Python", loops and all?          ──► Cython
          │
          ├─ Must also generate Java / C# / Ruby bindings?         ──► SWIG
          │
          ├─ Starting fresh, C++17 OK, want small & fast?          ──► nanobind
          │
          └─ Anything else ──────────────────────────────────────► pybind11
```

**If you are learning one thing: learn pybind11.** It is the default answer, the
largest community, the best documentation, and nanobind is a small step away
once you know it.

---

## 14. The bugs everyone hits

1. **Forgetting `#include <pybind11/stl.h>`** — `std::vector`/`std::map`
   arguments become unusable opaque objects with a baffling error message.
2. **Expecting a returned container to be mutable** — it is a copy;
   `obj.items().append(x)` silently does nothing. See
   [§6(A)](#a-automatic-conversion--list-copies).
3. **`PYBIND11_MAKE_OPAQUE` placed after the bindings** — it must precede every
   use of that type, in every translation unit that touches it.
4. **A NumPy view without a keep-alive `base`** — use-after-free that shows up as
   corrupted numbers much later.
5. **A view onto a vector that later grows** — `push_back` reallocates and your
   view dangles.
6. **dtype mismatch** — `float64` vs `float32` vs `int64`. Either the caster
   silently copies (killing your zero-copy) or you reinterpret garbage.
7. **Row-major vs column-major with Eigen** — silently degrades `Eigen::Ref` into
   a copy. See [§10](#eigen--there-is-nothing-to-bind-numpy-is-the-python-side).
8. **Touching Python objects with the GIL released** — instant, undebuggable
   crash.
9. **Cython without `except +`** — a C++ throw kills the interpreter instead of
   raising.
10. **ctypes without `argtypes`/`restype`** — arguments are assumed `int`. Pass a
    `double` and you get silent garbage, or a segfault.
11. **The module name not matching the filename** — `PYBIND11_MODULE(foo, m)`
    must be built as `foo*.so`, or the import fails cryptically.
12. **Calling across the boundary in a tight loop** — see
    [§11](#11-measured-overhead). Batch it.

---

## The runnable examples

| Directory | Technique | Shows |
|---|---|---|
| [`cpp/`](calling_cpp_from_python/cpp/) | — | The shared C++ API + the `extern "C"` shim that ctypes/cffi need |
| [`01_ctypes/`](calling_cpp_from_python/01_ctypes/) | ctypes | Manual signatures, opaque handles, hand-written destructor |
| [`02_cffi/`](calling_cpp_from_python/02_cffi/) | cffi | API mode, compiler-checked decls, `ffi.gc` |
| [`03_cython/`](calling_cpp_from_python/03_cython/) | Cython | `cdef class`, `except +`, typed memoryviews, a compiled hot loop |
| [`04_pybind11/`](calling_cpp_from_python/04_pybind11/) | pybind11 | Classes, properties, defaults, NumPy, GIL release |
| [`05_nanobind/`](calling_cpp_from_python/05_nanobind/) | nanobind | The same module, side by side + generated `.pyi` |
| [`06_swig/`](calling_cpp_from_python/06_swig/) | SWIG | `.i` interface file, typemaps, `%exception` |
| [`07_vectors/`](calling_cpp_from_python/07_vectors/) | pybind11 | **`std::vector<T>`: copy vs opaque vs zero-copy vs structs** |
| [`bench.py`](calling_cpp_from_python/bench.py) | all | Per-call overhead measurement |

```bash
cd docs/calling_cpp_from_python
./run_all.sh      # builds and runs everything
python bench.py
```

## Further reading

- pybind11 — https://pybind11.readthedocs.io/
- nanobind — https://nanobind.readthedocs.io/
- Cython — https://cython.readthedocs.io/
- ctypes — https://docs.python.org/3/library/ctypes.html
- cffi — https://cffi.readthedocs.io/
- SWIG — https://www.swig.org/Doc4.0/Python.html
- Buffer protocol (PEP 3118) — https://peps.python.org/pep-3118/
- scikit-build-core — https://scikit-build-core.readthedocs.io/
- cibuildwheel — https://cibuildwheel.pypa.io/
