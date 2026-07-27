// pybind11: the de-facto standard for binding C++ to Python.
//
// Header-only, C++11 (works fine with C++17/20), no code generator, no separate
// interface language. You describe the API in ordinary C++ and the compiler
// does the rest. Compare the size of this file with 01_ctypes/ + cpp/c_api.cpp:
// same functionality, ~1/4 the code, and it is type-checked.

#include <pybind11/numpy.h>    // py::array_t  (NumPy interop)
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>      // std::vector <-> list, std::string <-> str, ...

#include "mathlib.hpp"

namespace py = pybind11;
using namespace pybind11::literals;  // enables the "name"_a argument syntax

// PYBIND11_MODULE(<module name>, <handle>) expands to the PyInit_ function
// CPython looks for. The module name MUST match the .so filename.
PYBIND11_MODULE(mathlib_pb, m) {
  m.doc() = "pybind11 bindings for the mathlib C++ API";

  // --- free functions -----------------------------------------------------
  m.def("add", &mathlib::add, "Add two numbers", "a"_a, "b"_a);

  // Default arguments and keyword names are declared, not inferred.
  m.def("divide", &mathlib::divide, "a"_a, "b"_a = 1.0,
        "Divide a by b; raises ValueError on b == 0");
  // std::invalid_argument is translated to ValueError automatically.
  // Full default table: std::out_of_range -> IndexError, std::domain_error ->
  // ValueError, std::runtime_error -> RuntimeError. Register your own with
  // py::register_exception<MyError>(m, "MyError").

  // --- NumPy without copying ---------------------------------------------
  m.def(
      "scale_inplace",
      [](py::array_t<double, py::array::c_style | py::array::forcecast> arr,
         double factor) {
        py::buffer_info buf = arr.request();   // shape/stride/pointer metadata
        // gil_scoped_release: let other Python threads run while C++ works.
        // Only safe because we touch no Python objects inside.
        py::gil_scoped_release release;
        mathlib::scale_inplace(static_cast<double*>(buf.ptr),
                               static_cast<std::size_t>(buf.size), factor);
      },
      "arr"_a, "factor"_a, "Multiply a float64 array in place");

  // --- a class ------------------------------------------------------------
  py::class_<mathlib::Accumulator>(m, "Accumulator")
      .def(py::init<double, std::string>(), "start"_a = 0.0, "name"_a = "acc")
      .def("add", &mathlib::Accumulator::add, "value"_a)
      // read-only property from a getter
      .def_property_readonly("total", &mathlib::Accumulator::total)
      // read/write property from a getter + setter pair
      .def_property("name", &mathlib::Accumulator::name,
                    &mathlib::Accumulator::set_name)
      // std::vector<double> -> Python list, thanks to <pybind11/stl.h>
      .def("history", &mathlib::Accumulator::history)
      .def("__len__", &mathlib::Accumulator::size)
      .def("__repr__", [](const mathlib::Accumulator& a) {
        return "<Accumulator name='" + a.name() +
               "' total=" + std::to_string(a.total()) + ">";
      });
  // Lifetime: pybind11 owns the C++ object via a holder (std::unique_ptr by
  // default) and destroys it when the Python object is collected. No manual
  // free, no __del__.
}
