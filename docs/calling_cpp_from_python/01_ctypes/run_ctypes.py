"""ctypes: call a plain shared library from pure Python. No compiler needed.

Build the .so first (from this directory):

    g++ -O2 -std=c++17 -shared -fPIC -I../cpp \
        ../cpp/mathlib.cpp ../cpp/c_api.cpp -o libmathlib_c.so

Then:  python run_ctypes.py

Key idea: ctypes speaks the *C* ABI only. It loads the .so with dlopen(),
looks symbols up by name, and you declare each signature by hand. Nothing is
checked at compile time — a wrong argtype is a segfault, not a TypeError.
"""

import ctypes
import pathlib

import numpy as np

# ---------------------------------------------------------------- load the lib
HERE = pathlib.Path(__file__).resolve().parent
lib = ctypes.CDLL(str(HERE / "libmathlib_c.so"))
# On Windows this would be ctypes.WinDLL / a .dll; on macOS a .dylib.

# ------------------------------------------- declare every signature BY HAND
# If you skip this, ctypes assumes every argument is an int and the return type
# is int. For doubles that silently produces garbage.
lib.ml_add.argtypes = [ctypes.c_double, ctypes.c_double]
lib.ml_add.restype = ctypes.c_double

lib.ml_scale_inplace.argtypes = [
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_size_t,
    ctypes.c_double,
]
lib.ml_scale_inplace.restype = None

lib.ml_divide.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double)]
lib.ml_divide.restype = ctypes.c_int

lib.ml_acc_create.argtypes = [ctypes.c_double, ctypes.c_char_p]
lib.ml_acc_create.restype = ctypes.c_void_p  # opaque handle
lib.ml_acc_destroy.argtypes = [ctypes.c_void_p]
lib.ml_acc_add.argtypes = [ctypes.c_void_p, ctypes.c_double]
lib.ml_acc_total.argtypes = [ctypes.c_void_p]
lib.ml_acc_total.restype = ctypes.c_double
lib.ml_acc_size.argtypes = [ctypes.c_void_p]
lib.ml_acc_size.restype = ctypes.c_size_t
lib.ml_acc_name.argtypes = [ctypes.c_void_p]
lib.ml_acc_name.restype = ctypes.c_char_p
lib.ml_acc_history.argtypes = [
    ctypes.c_void_p,
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_size_t,
]
lib.ml_acc_history.restype = ctypes.c_size_t


# ------------------------------------- wrap the handle in a Python class
class Accumulator:
    """Hand-written RAII wrapper so the C++ object is freed deterministically."""

    def __init__(self, start: float = 0.0, name: str = "acc") -> None:
        self._handle = lib.ml_acc_create(start, name.encode())
        if not self._handle:
            raise MemoryError("ml_acc_create failed")

    def add(self, value: float) -> None:
        lib.ml_acc_add(self._handle, value)

    @property
    def total(self) -> float:
        return lib.ml_acc_total(self._handle)

    @property
    def name(self) -> str:
        return lib.ml_acc_name(self._handle).decode()

    def history(self) -> np.ndarray:
        n = lib.ml_acc_size(self._handle)
        out = np.empty(n, dtype=np.float64)
        written = lib.ml_acc_history(
            self._handle, out.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), n
        )
        return out[:written]

    def close(self) -> None:
        if getattr(self, "_handle", None):
            lib.ml_acc_destroy(self._handle)
            self._handle = None

    # __del__ is best-effort; prefer an explicit close() or a context manager.
    def __del__(self) -> None:
        self.close()

    def __enter__(self) -> "Accumulator":
        return self

    def __exit__(self, *exc) -> None:
        self.close()


def divide(a: float, b: float) -> float:
    """Turn the C status code back into a Python exception."""
    out = ctypes.c_double()
    if lib.ml_divide(a, b, ctypes.byref(out)) != 0:
        raise ZeroDivisionError(f"{a} / {b}")
    return out.value


def main() -> None:
    print("add(2, 3)          =", lib.ml_add(2.0, 3.0))

    # Zero-copy into NumPy: we hand C++ the raw pointer NumPy already owns.
    arr = np.arange(5, dtype=np.float64)  # dtype MUST match double
    lib.ml_scale_inplace(
        arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), arr.size, 10.0
    )
    print("scale_inplace(x10) =", arr)

    print("divide(1, 4)       =", divide(1.0, 4.0))
    try:
        divide(1.0, 0.0)
    except ZeroDivisionError as exc:
        print("divide(1, 0)       -> ZeroDivisionError:", exc)

    with Accumulator(1.0, "ctypes-acc") as acc:
        for v in (2.0, 3.0, 4.0):
            acc.add(v)
        print(f"{acc.name}: total={acc.total} history={acc.history()}")


if __name__ == "__main__":
    main()
