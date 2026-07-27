"""Measure per-call overhead of each binding technique.

Run ./run_all.sh first, then:  python bench.py

What this measures: the cost of *crossing the boundary*, not the cost of the
C++ work. `add(a, b)` is one FLOP, so essentially 100% of the time below is
argument conversion + dispatch. That is exactly the number you care about when
deciding whether to call C++ in a tight Python loop.
"""

import ctypes
import pathlib
import sys
import timeit

HERE = pathlib.Path(__file__).resolve().parent
N = 200_000
REPEAT = 7  # take the MIN across repeats: a single timing run is very noisy
            # (CPU frequency scaling, other load). Min is the standard estimator
            # for "how fast can this go".

for sub in ("01_ctypes", "02_cffi", "03_cython", "06_swig"):
    sys.path.insert(0, str(HERE / sub))
for sub in ("04_pybind11", "05_nanobind", "07_vectors"):
    sys.path.insert(0, str(HERE / sub / "build"))

results: list[tuple[str, float]] = []


def bench(label: str, stmt) -> None:
    secs = min(timeit.repeat(stmt, number=N, repeat=REPEAT))
    results.append((label, secs / N * 1e9))


# --- pure Python baseline
bench("python (baseline)", lambda: 2.0 + 3.0)

# --- ctypes
try:
    lib = ctypes.CDLL(str(HERE / "01_ctypes" / "libmathlib_c.so"))
    lib.ml_add.argtypes = [ctypes.c_double, ctypes.c_double]
    lib.ml_add.restype = ctypes.c_double
    ml_add = lib.ml_add
    bench("ctypes", lambda: ml_add(2.0, 3.0))
except OSError as exc:
    print("  skip ctypes:", exc)

# --- cffi
try:
    from _mathlib_cffi import lib as cffi_lib

    bench("cffi (API mode)", lambda: cffi_lib.ml_add(2.0, 3.0))
except ImportError as exc:
    print("  skip cffi:", exc)

# --- Cython
try:
    import mathlib_cy

    bench("Cython", lambda: mathlib_cy.add(2.0, 3.0))
except ImportError as exc:
    print("  skip Cython:", exc)

# --- pybind11
try:
    import mathlib_pb

    bench("pybind11", lambda: mathlib_pb.add(2.0, 3.0))
except ImportError as exc:
    print("  skip pybind11:", exc)

# --- nanobind
try:
    import mathlib_nb

    bench("nanobind", lambda: mathlib_nb.add(2.0, 3.0))
except ImportError as exc:
    print("  skip nanobind:", exc)

# --- SWIG
try:
    import mathlib_swig

    bench("SWIG", lambda: mathlib_swig.add(2.0, 3.0))
except ImportError as exc:
    print("  skip SWIG:", exc)

print(f"\nPer-call overhead: best of {REPEAT} runs of {N:,} calls of add(2.0, 3.0)\n")
print(f"  {'technique':<20} {'ns/call':>9}   {'vs fastest':>10}")
print("  " + "-" * 44)
best = min(t for _, t in results)
for label, ns in sorted(results, key=lambda r: r[1]):
    print(f"  {label:<20} {ns:>9.0f}   {ns / best:>9.1f}x")
