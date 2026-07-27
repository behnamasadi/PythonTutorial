"""Subclassing a C++ class from Python, and passing Python callables to C++.

    cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j
    PYTHONPATH=build python run_inheritance.py
"""

import pickle

import plugin_pb as p


# ============================================================== subclassing
# `Filter` is an ABSTRACT C++ class. This is a Python class inheriting from it.
class Square(p.Filter):
    def apply(self, x):  # overrides a PURE virtual
        return x * x

    def name(self):  # overrides a virtual that has a C++ default
        return "square (from Python)"


class Offset(p.Filter):
    def __init__(self, k):
        # MUST call the base __init__, or the C++ half is never constructed.
        # Forgetting this is the #1 trampoline bug. pybind11 catches it at
        # construction with a clear TypeError rather than crashing later —
        # see NoInit below for the actual message.
        super().__init__()
        self.k = k

    def apply(self, x):
        return x + self.k

    # name() deliberately NOT overridden -> the C++ default runs.


class Broken(p.Filter):
    pass  # does not implement the pure virtual apply()


class NoInit(p.Filter):
    """The classic trampoline mistake: overriding __init__ without chaining."""

    def __init__(self, k):
        self.k = k  # super().__init__() missing -> no C++ half exists

    def apply(self, x):
        return x + self.k


def main() -> None:
    xs = [1.0, 2.0, 3.0, 4.0]

    print("=" * 68)
    print("1. Python subclasses of an abstract C++ class")
    print("=" * 68)
    cpp = p.Scale(10.0)
    py_sq = Square()
    py_off = Offset(100.0)

    print(f"  {'class':<10} {'defined in':<10} {'name()':<24} apply(5)")
    print("  " + "-" * 58)
    for f, where in ((cpp, "C++"), (py_sq, "Python"), (py_off, "Python")):
        print(f"  {type(f).__name__:<10} {where:<10} {f.name():<24} {f.apply(5.0)}")

    print()
    print("  isinstance(Square(), p.Filter) =", isinstance(py_sq, p.Filter))
    print("  Offset did not override name() -> C++ default:", py_off.name())

    print()
    print("=" * 68)
    print("2. C++ calling BACK into Python (the whole point of trampolines)")
    print("=" * 68)
    # pipeline_sum is C++ taking `const Filter&`. It loops in C++ and calls
    # apply() virtually. For the Python subclasses, each iteration re-enters
    # the interpreter.
    for f in (cpp, py_sq, py_off):
        print(f"  pipeline_sum({type(f).__name__:<7}, {xs}) = {p.pipeline_sum(f, xs)}")
    print("  ^ C++ ran the loop and dispatched virtually; for Square and Offset")
    print("    every iteration re-entered the interpreter via the trampoline.")

    print()
    print("  The two ways a Python subclass goes wrong — both caught cleanly:")
    try:
        p.pipeline_sum(Broken(), xs)
    except RuntimeError as exc:
        print("   forgot the pure virtual ->", type(exc).__name__ + ":", exc)
    try:
        NoInit(1.0)
    except TypeError as exc:
        print("   forgot super().__init__ ->", type(exc).__name__ + ":", exc)

    print()
    print("=" * 68)
    print("3. Factory returning std::unique_ptr<Filter>")
    print("=" * 68)
    made = p.make_scale(5.0)
    print("  make_scale(5.0)     ->", type(made).__name__, "| name:", made.name())
    print("  recovered as Scale  -> factor =", made.factor)

    print()
    print("=" * 68)
    print("4. Callbacks: any Python callable becomes a std::function")
    print("=" * 68)
    print("  lambda            ->", p.transform_sum(xs, lambda v: v * 100))
    print("  builtin (abs)     ->", p.transform_sum([-1.0, -2.0], abs))

    def cube(v):
        return v**3

    print("  def               ->", p.transform_sum(xs, cube))
    print("  bound method      ->", p.transform_sum(xs, p.Scale(2.0).apply))

    class Callable:
        def __call__(self, v):
            return v + 0.5

    print("  __call__ object   ->", p.transform_sum(xs, Callable()))

    print()
    print("  A C++ object that STORES a callback and fires it later:")
    btn = p.Button()
    btn.on_click(lambda n: print(f"    clicked from Python, count={n}"))
    btn.click()
    btn.click()
    print("  btn.clicks =", btn.clicks)

    print()
    print("=" * 68)
    print("5. C++ worker threads calling a Python callback (GIL)")
    print("=" * 68)
    out = p.parallel_apply(xs, lambda v: v * 2, n_threads=4)
    print("  parallel_apply(x2, 4 threads) =", out)
    print("  Correct result, no deadlock: the binding released the GIL and")
    print("  each worker re-acquired it around the callback.")

    print()
    print("=" * 68)
    print("6. Enums and pickling")
    print("=" * 68)
    print("  Mode.Fast          ->", p.Mode.Fast, "|", p.describe(p.Mode.Fast))
    print("  Mode.Accurate      ->", p.describe(p.Mode.Accurate))

    s = p.Scale(7.5)
    blob = pickle.dumps(s)  # needs py::pickle in the bindings
    back = pickle.loads(blob)
    print(f"  pickle round-trip  -> factor {s.factor} -> {back.factor}")
    print("  (without py::pickle this raises TypeError — and that is what")
    print("   breaks multiprocessing with bound C++ objects)")


if __name__ == "__main__":
    main()
