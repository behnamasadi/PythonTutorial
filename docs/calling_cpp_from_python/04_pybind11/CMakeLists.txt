cmake_minimum_required(VERSION 3.18)
project(mathlib_pb LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Modern CPython discovery. Development.Module (not Development) is what you
# want for extension modules — it does not require the Python *library*, which
# matters on macOS and for manylinux wheels.
find_package(Python 3.8 REQUIRED COMPONENTS Interpreter Development.Module)

# Let CMake find the pip-installed pybind11 by asking Python where it is.
execute_process(
  COMMAND "${Python_EXECUTABLE}" -m pybind11 --cmakedir
  OUTPUT_VARIABLE pybind11_DIR
  OUTPUT_STRIP_TRAILING_WHITESPACE)
find_package(pybind11 CONFIG REQUIRED)

# pybind11_add_module handles: -fPIC, -fvisibility=hidden, the right suffix
# (.cpython-312-x86_64-linux-gnu.so), LTO, and stripping in Release.
pybind11_add_module(mathlib_pb
  bindings.cpp
  ../cpp/mathlib.cpp)

target_include_directories(mathlib_pb PRIVATE ../cpp)
