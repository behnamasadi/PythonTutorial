"""Use the nanobind module.

    cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
    cmake --build build -j
    PYTHONPATH=build python run_nanobind.py
"""

import numpy as np

import mathlib_nb


def main() -> None:
    print("add(2, 3)          =", mathlib_nb.add(2.0, 3.0))

    arr = np.arange(5, dtype=np.float64)
    mathlib_nb.scale_inplace(arr, 10.0)
    print("scale_inplace(x10) =", arr)

    print("divide(1, 4)       =", mathlib_nb.divide(1.0, 4.0))
    try:
        mathlib_nb.divide(1.0, 0.0)
    except ValueError as exc:
        print("divide(1, 0)       -> ValueError:", exc)

    acc = mathlib_nb.Accumulator(1.0, name="nanobind-acc")
    for v in (2.0, 3.0, 4.0):
        acc.add(v)
    acc.name = "renamed"
    print(f"{acc!r} len={len(acc)} history={acc.history()}")

    try:
        mathlib_nb.add("two", 3.0)
    except TypeError as exc:
        print("add('two', 3)      -> TypeError:", str(exc).splitlines()[0])


if __name__ == "__main__":
    main()
