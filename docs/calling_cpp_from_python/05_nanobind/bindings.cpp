// nanobind: same author as pybind11, same API shape, rewritten for C++17 and
// modern CPython. Smaller binaries, faster compiles, lower call overhead.
//
// Read this side by side with 04_pybind11/bindings.cpp — the differences are
// almost entirely cosmetic:
//
//   pybind11.h        -> nanobind/nanobind.h
//   py::             -> nb::
//   PYBIND11_MODULE  -> NB_MODULE
//   pybind11/stl.h   -> nanobind/stl/vector.h, .../string.h  (opt in per type)
//   py::array_t      -> nb::ndarray  (works with NumPy, PyTorch, JAX, CuPy)
//
// The cost: nanobind requires C++17 and Python >= 3.8, and does not support
// some pybind11 corner cases (e.g. multiple inheritance from Python types).

#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>

#include "mathlib.hpp"

namespace nb = nanobind;
using namespace nb::literals;

NB_MODULE(mathlib_nb, m) {
  m.doc() = "nanobind bindings for the mathlib C++ API";

  m.def("add", &mathlib::add, "a"_a, "b"_a, "Add two numbers");
  m.def("divide", &mathlib::divide, "a"_a, "b"_a = 1.0);

  // nb::ndarray is framework-agnostic: this same signature accepts a NumPy
  // array, a torch.Tensor on CPU, or anything else exposing DLPack.
  m.def(
      "scale_inplace",
      [](nb::ndarray<double, nb::ndim<1>, nb::c_contig, nb::device::cpu> arr,
         double factor) {
        nb::gil_scoped_release release;
        mathlib::scale_inplace(arr.data(), arr.shape(0), factor);
      },
      "arr"_a, "factor"_a);

  nb::class_<mathlib::Accumulator>(m, "Accumulator")
      .def(nb::init<double, std::string>(), "start"_a = 0.0, "name"_a = "acc")
      .def("add", &mathlib::Accumulator::add, "value"_a)
      .def_prop_ro("total", &mathlib::Accumulator::total)
      .def_prop_rw("name", &mathlib::Accumulator::name,
                   &mathlib::Accumulator::set_name)
      .def("history", &mathlib::Accumulator::history)
      .def("__len__", &mathlib::Accumulator::size)
      .def("__repr__", [](const mathlib::Accumulator& a) {
        return "<Accumulator name='" + a.name() +
               "' total=" + std::to_string(a.total()) + ">";
      });
}
