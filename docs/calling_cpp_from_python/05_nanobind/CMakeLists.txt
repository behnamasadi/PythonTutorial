cmake_minimum_required(VERSION 3.18)
project(mathlib_nb LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Python 3.8 REQUIRED COMPONENTS Interpreter Development.Module)

execute_process(
  COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
  OUTPUT_VARIABLE nanobind_DIR
  OUTPUT_STRIP_TRAILING_WHITESPACE)
find_package(nanobind CONFIG REQUIRED)

# NB_STATIC links nanobind's runtime into this module (fine for a single
# module; drop it if you ship several modules that should share it).
nanobind_add_module(mathlib_nb NB_STATIC
  bindings.cpp
  ../cpp/mathlib.cpp)

target_include_directories(mathlib_nb PRIVATE ../cpp)

# Bonus: generate a .pyi stub so editors and mypy understand the module.
# nanobind ships this out of the box; pybind11 needs pybind11-stubgen.
nanobind_add_stub(
  mathlib_nb_stub
  MODULE mathlib_nb
  OUTPUT mathlib_nb.pyi
  PYTHON_PATH $<TARGET_FILE_DIR:mathlib_nb>
  DEPENDS mathlib_nb)
