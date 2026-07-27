"""Use the SWIG-generated module (see run_all.sh or the header of mathlib.i)."""

import mathlib_swig


def main() -> None:
    print("add(2, 3)          =", mathlib_swig.add(2.0, 3.0))

    print("divide(1, 4)       =", mathlib_swig.divide(1.0, 4.0))
    try:
        mathlib_swig.divide(1.0, 0.0)
    except ValueError as exc:  # via the %exception block in mathlib.i
        print("divide(1, 0)       -> ValueError:", exc)

    # SWIG bound the class straight from the header — note it kept the C++
    # method names (total(), size()) rather than making them properties.
    acc = mathlib_swig.Accumulator(1.0, "swig-acc")
    for v in (2.0, 3.0, 4.0):
        acc.add(v)
    print(
        f"name={acc.name()} total={acc.total()} "
        f"size={acc.size()} history={list(acc.history())}"
    )
    # `scale_inplace` is deliberately not exercised here: a bare `double*` has
    # no length, so SWIG cannot bind it safely without a hand-written typemap.
    # That is the SWIG tax — pybind11/nanobind handle it with one lambda.


if __name__ == "__main__":
    main()
