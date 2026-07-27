#!/usr/bin/env bash
# Build and run all five binding techniques.
#
#   pip install pybind11 nanobind cython numpy setuptools cffi swig
#   ./run_all.sh
#
# Each section is independent — comment out the ones you do not care about.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${PYTHON:-python}"
cd "$HERE"

hr() { printf '\n\033[1m=== %s ===\033[0m\n' "$1"; }

# ---------------------------------------------------------------- 1. ctypes
hr "ctypes"
g++ -O2 -std=c++17 -shared -fPIC -I cpp \
    cpp/mathlib.cpp cpp/c_api.cpp -o 01_ctypes/libmathlib_c.so
(cd 01_ctypes && "$PY" run_ctypes.py)

# ------------------------------------------------------------------ 2. cffi
hr "cffi"
(cd 02_cffi && "$PY" make_cffi.py >/dev/null && "$PY" run_cffi.py)

# ---------------------------------------------------------------- 3. Cython
hr "Cython"
(cd 03_cython && "$PY" setup.py build_ext --inplace >/dev/null 2>&1 && "$PY" run_cython.py)

# ------------------------------------------------------------- 4. pybind11
hr "pybind11"
cmake -S 04_pybind11 -B 04_pybind11/build -DCMAKE_BUILD_TYPE=Release \
      -DPython_EXECUTABLE="$(command -v "$PY")" >/dev/null
cmake --build 04_pybind11/build -j >/dev/null
(cd 04_pybind11 && PYTHONPATH=build "$PY" run_pybind11.py)

# -------------------------------------------------------------- 5. nanobind
hr "nanobind"
cmake -S 05_nanobind -B 05_nanobind/build -DCMAKE_BUILD_TYPE=Release \
      -DPython_EXECUTABLE="$(command -v "$PY")" >/dev/null
cmake --build 05_nanobind/build -j >/dev/null
(cd 05_nanobind && PYTHONPATH=build "$PY" run_nanobind.py)

# ------------------------------------------------------------------ 6. SWIG
hr "SWIG"
(
  cd 06_swig
  swig -c++ -python -I../cpp -o mathlib_swig_wrap.cxx mathlib.i
  PY_INC="$("$PY" -c 'import sysconfig; print(sysconfig.get_paths()["include"])')"
  g++ -O2 -std=c++17 -shared -fPIC -I../cpp -I"$PY_INC" \
      mathlib_swig_wrap.cxx ../cpp/mathlib.cpp -o _mathlib_swig.so
  "$PY" run_swig.py
)

# ------------------------------------------------- 7. std::vector deep dive
hr "std::vector<T> (pybind11)"
cmake -S 07_vectors -B 07_vectors/build -DCMAKE_BUILD_TYPE=Release \
      -DPython_EXECUTABLE="$(command -v "$PY")" >/dev/null
cmake --build 07_vectors/build -j >/dev/null
(cd 07_vectors && PYTHONPATH=build "$PY" run_vectors.py)

# --------------------------- 8. inheritance, callbacks, GIL (pybind11)
hr "inheritance & callbacks (pybind11)"
cmake -S 08_inheritance -B 08_inheritance/build -DCMAKE_BUILD_TYPE=Release \
      -DPython_EXECUTABLE="$(command -v "$PY")" >/dev/null
cmake --build 08_inheritance/build -j >/dev/null
(cd 08_inheritance && PYTHONPATH=build "$PY" run_inheritance.py)

hr "all built and ran"
