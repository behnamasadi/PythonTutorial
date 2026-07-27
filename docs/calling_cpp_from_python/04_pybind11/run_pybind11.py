"""Use the pybind11 module.

    cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
    cmake --build build -j
    PYTHONPATH=build python run_pybind11.py
"""

import numpy as np

import mathlib_pb


def main() -> None:
    print("add(2, 3)          =", mathlib_pb.add(2.0, 3.0))
    print("add(b=3, a=2)      =", mathlib_pb.add(b=3.0, a=2.0))  # keyword args work
    print("help(add)          :", mathlib_pb.add.__doc__.strip().splitlines()[0])

    arr = np.arange(5, dtype=np.float64)
    mathlib_pb.scale_inplace(arr, 10.0)
    print("scale_inplace(x10) =", arr)

    print("divide(1, 4)       =", mathlib_pb.divide(1.0, 4.0))
    print("divide(7)          =", mathlib_pb.divide(7.0))  # b defaults to 1.0
    try:
        mathlib_pb.divide(1.0, 0.0)
    except ValueError as exc:  # std::invalid_argument -> ValueError
        print("divide(1, 0)       -> ValueError:", exc)

    acc = mathlib_pb.Accumulator(1.0, name="pybind11-acc")
    for v in (2.0, 3.0, 4.0):
        acc.add(v)
    acc.name = "renamed"
    print(f"{acc!r} len={len(acc)} history={acc.history()}")

    # Type errors are caught at the boundary instead of segfaulting.
    try:
        mathlib_pb.add("two", 3.0)
    except TypeError as exc:
        print("add('two', 3)      -> TypeError:", str(exc).splitlines()[0])


if __name__ == "__main__":
    main()
