# Calling C++ from Python — runnable examples

Companion code for [../calling_cpp_from_python.md](../calling_cpp_from_python.md).
Read the doc first; this directory is the proof that everything in it works.

The **same** C++ API ([`cpp/mathlib.hpp`](cpp/mathlib.hpp) — a free function, a
buffer function, a throwing function, and a stateful class) is bound six
different ways so you can diff them against each other.

```bash
pip install pybind11 nanobind cython cffi swig numpy setuptools
./run_all.sh       # builds and runs all seven examples
python bench.py      # per-call overhead of each technique
```

| Directory | Technique | What to look at |
|---|---|---|
| [`cpp/`](cpp/) | — | The C++ API, plus the `extern "C"` shim ctypes/cffi require |
| [`01_ctypes/`](01_ctypes/) | ctypes | How much hand-written code a C++ class costs you |
| [`02_cffi/`](02_cffi/) | cffi | API mode: real compiler, `ffi.gc` destructors |
| [`03_cython/`](03_cython/) | Cython | `cdef class`, `except +`, memoryviews, a compiled hot loop |
| [`04_pybind11/`](04_pybind11/) | pybind11 | The reference implementation — start here |
| [`05_nanobind/`](05_nanobind/) | nanobind | Same module, `s/py::/nb::/`, plus a generated `.pyi` |
| [`06_swig/`](06_swig/) | SWIG | `.i` interface file, typemaps, `%exception` |
| [`07_vectors/`](07_vectors/) | pybind11 | **`std::vector<T>`: copy vs opaque vs zero-copy vs structs** |
| [`08_inheritance/`](08_inheritance/) | pybind11 | **Python subclassing a C++ abstract class (trampolines), callbacks, threads/GIL, enums, pickling** |

Build artifacts (`build/`, `*.so`, generated `.cpp`/`.cxx`/`.py`) are gitignored.

To use a specific interpreter: `PYTHON=/path/to/python ./run_all.sh`.
