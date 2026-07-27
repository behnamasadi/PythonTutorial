# distutils: language = c++
"""Cython: write Python-ish code that compiles to C++.

Cython is not primarily a *binding* generator — it is a compiler for a
Python/C++ hybrid language. You get bindings as a side effect, plus the ability
to write hot loops in the same file. That is why NumPy/SciPy/pandas use it.

Build:  python setup.py build_ext --inplace
"""

from libcpp.string cimport string
from libcpp.vector cimport vector

import numpy as np
cimport numpy as cnp


# 1. Declare the C++ API you want to reach. This mirrors mathlib.hpp.
cdef extern from "mathlib.hpp" namespace "mathlib":
    double c_add "mathlib::add"(double a, double b)
    void c_scale_inplace "mathlib::scale_inplace"(double* data, size_t n, double factor)
    double c_divide "mathlib::divide"(double a, double b) except +
    #                                                     ^^^^^^
    # `except +` = translate a C++ exception into a Python exception.
    # std::invalid_argument becomes ValueError automatically.

    cdef cppclass Accumulator:
        Accumulator(double start, string name) except +
        void add(double value)
        double total()
        const string& name()
        void set_name(const string& name)
        vector[double] history()
        size_t size()


# 2. Expose it to Python.
def add(double a, double b) -> float:
    return c_add(a, b)


def divide(double a, double b) -> float:
    return c_divide(a, b)          # raises ValueError("division by zero")


def scale_inplace(double[::1] data not None, double factor):
    """`double[::1]` is a typed memoryview: any C-contiguous float64 buffer
    (NumPy array, array.array, ...) with zero copy and a shape check."""
    if data.shape[0] == 0:
        return
    c_scale_inplace(&data[0], data.shape[0], factor)


# 3. `cdef class` = a real Python extension type holding a C++ object.
cdef class PyAccumulator:
    cdef Accumulator* _thisptr        # owned raw pointer

    def __cinit__(self, double start=0.0, str name="acc"):
        # __cinit__ runs before any Python code can touch the object.
        self._thisptr = new Accumulator(start, name.encode())

    def __dealloc__(self):
        # Called exactly once, when the object is collected. No leaks, no
        # hand-written destroy() like in the ctypes version.
        del self._thisptr

    def add(self, double value):
        self._thisptr.add(value)

    @property
    def total(self) -> float:
        return self._thisptr.total()

    @property
    def name(self) -> str:
        return self._thisptr.name().decode()      # std::string -> bytes -> str

    @name.setter
    def name(self, str value):
        self._thisptr.set_name(value.encode())

    def history(self):
        # std::vector<double> is auto-converted to a Python list by Cython.
        return np.asarray(self._thisptr.history(), dtype=np.float64)

    def __len__(self):
        return self._thisptr.size()

    def __repr__(self):
        return f"PyAccumulator(name={self.name!r}, total={self.total})"


# 4. The thing bindings alone cannot do: a hot loop compiled to C++.
cimport cython


@cython.boundscheck(False)
@cython.wraparound(False)
def sum_of_squares(double[::1] data not None) -> float:
    cdef double acc = 0.0
    cdef Py_ssize_t i
    for i in range(data.shape[0]):        # compiles to a plain C for-loop
        acc += data[i] * data[i]
    return acc
