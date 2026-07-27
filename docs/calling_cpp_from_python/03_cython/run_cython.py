"""Use the extension built by setup.py."""

import numpy as np

import mathlib_cy


def main() -> None:
    print("add(2, 3)          =", mathlib_cy.add(2.0, 3.0))

    arr = np.arange(5, dtype=np.float64)
    mathlib_cy.scale_inplace(arr, 10.0)          # typed memoryview, zero copy
    print("scale_inplace(x10) =", arr)

    print("divide(1, 4)       =", mathlib_cy.divide(1.0, 4.0))
    try:
        mathlib_cy.divide(1.0, 0.0)
    except ValueError as exc:                    # `except +` did the translation
        print("divide(1, 0)       -> ValueError:", exc)

    acc = mathlib_cy.PyAccumulator(1.0, "cython-acc")
    for v in (2.0, 3.0, 4.0):
        acc.add(v)
    print(f"{acc!r} len={len(acc)} history={acc.history()}")

    print("sum_of_squares     =", mathlib_cy.sum_of_squares(np.arange(5, dtype=np.float64)))


if __name__ == "__main__":
    main()
