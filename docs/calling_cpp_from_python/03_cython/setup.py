"""Build the Cython extension:  python setup.py build_ext --inplace"""

import pathlib

import numpy as np
from Cython.Build import cythonize
from setuptools import Extension, setup

HERE = pathlib.Path(__file__).resolve().parent
CPP = HERE.parent / "cpp"

ext = Extension(
    name="mathlib_cy",
    sources=["mathlib_cy.pyx", str(CPP / "mathlib.cpp")],
    include_dirs=[str(CPP), np.get_include()],
    language="c++",
    extra_compile_args=["-std=c++17", "-O2"],
)

setup(
    name="mathlib_cy",
    ext_modules=cythonize([ext], language_level="3"),
)
