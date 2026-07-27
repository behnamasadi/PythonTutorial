// Binding an abstract base class so PYTHON can subclass it, plus callbacks.
//
// The problem: `plugin::Filter::apply` is pure virtual. C++ code
// (`Filter::apply_all`) calls it through a `Filter&`. If a Python class
// subclasses Filter and overrides apply(), C++ must somehow end up executing
// Python. C++ has no idea Python exists — so we insert a TRAMPOLINE.

#include <pybind11/functional.h>  // std::function <-> any Python callable
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "plugin.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

// ============================== THE TRAMPOLINE ==============================
// A C++ class deriving from Filter whose every virtual method asks Python
// "did a subclass override this?" — and if so, calls the Python method.
//
// It is a normal C++ class, so C++ can hold it as a Filter& and dispatch
// virtually without knowing anything unusual is going on. The macro body is
// what bridges back into the interpreter (acquiring the GIL as needed).
class PyFilter : public plugin::Filter {
 public:
  using plugin::Filter::Filter;  // inherit constructors

  double apply(double x) const override {
    PYBIND11_OVERRIDE_PURE(
        double,          // return type
        plugin::Filter,  // parent class
        apply,           // method name in C++
        x                // arguments
    );
    // _PURE = no C++ fallback. If Python did not override it, this raises
    // RuntimeError("Tried to call pure virtual function") instead of crashing.
  }

  std::string name() const override {
    PYBIND11_OVERRIDE(
        std::string,     // return type
        plugin::Filter,  // parent class
        name,            // method name
                         // (no arguments — note the trailing comma above)
    );
    // Non-PURE: if Python did not override name(), Filter::name() runs.
  }
};
// ============================================================================

PYBIND11_MODULE(plugin_pb, m) {
  m.doc() = "Virtual overrides from Python (trampolines) + callbacks";

  // ------------------------------------------------------------- enums
  // py::enum_ makes a proper Python enum-like type. `.export_values()` would
  // also dump Fast/Accurate into the module namespace; scoped is usually nicer.
  py::enum_<plugin::Mode>(m, "Mode")
      .value("Fast", plugin::Mode::Fast)
      .value("Accurate", plugin::Mode::Accurate);
  m.def("describe", &plugin::describe, "mode"_a);

  // ------------------------------------------- the base class + trampoline
  // The SECOND template argument is the trampoline. Without it, a Python
  // subclass's apply() would be invisible to C++: pipeline_sum would call the
  // C++ base implementation (or abort on a pure virtual).
  py::class_<plugin::Filter, PyFilter>(m, "Filter")
      .def(py::init<>())
      .def("apply", &plugin::Filter::apply, "x"_a)
      .def("name", &plugin::Filter::name)
      .def("apply_all", &plugin::Filter::apply_all, "xs"_a);

  // A C++ subclass. The third argument declares the BASE, which is what makes
  // Python's isinstance() and implicit upcasting work.
  py::class_<plugin::Scale, plugin::Filter>(m, "Scale")
      .def(py::init<double>(), "factor"_a = 2.0)
      .def_property_readonly("factor", &plugin::Scale::factor)
      // ---- pickling: required if these objects must cross a multiprocessing
      //      boundary. __getstate__ / __setstate__ in pybind11 form.
      .def(py::pickle(
          [](const plugin::Scale& s) {          // __getstate__
            return py::make_tuple(s.factor());
          },
          [](py::tuple t) {                     // __setstate__
            if (t.size() != 1) throw std::runtime_error("bad state");
            return plugin::Scale(t[0].cast<double>());
          }));

  // Returning std::unique_ptr<Filter>: pybind11 takes ownership and gives
  // Python an object of the most-derived *bound* type it can identify.
  m.def("make_scale", &plugin::make_scale, "factor"_a);

  // Takes `const Filter&` — accepts a C++ Scale OR a Python subclass.
  m.def("pipeline_sum", &plugin::pipeline_sum, "f"_a, "xs"_a);

  // --------------------------------------------------------- callbacks
  // <pybind11/functional.h> converts ANY Python callable into a
  // std::function: a lambda, a def, a functools.partial, a class with
  // __call__, or a bound method.
  m.def("transform_sum", &plugin::transform_sum, "xs"_a, "fn"_a);

  py::class_<plugin::Button>(m, "Button")
      .def(py::init<>())
      // STORING a callback: the std::function keeps a reference to the Python
      // object, so it stays alive. Beware the reference CYCLE if the callback
      // closes over the Button itself — Python's GC cannot see through C++,
      // so that leaks. Use a weakref in the closure if you need that.
      .def("on_click", &plugin::Button::on_click, "cb"_a)
      .def("click", &plugin::Button::click)
      .def_property_readonly("clicks", &plugin::Button::clicks);

  // ------------------------------------------------- callbacks + threads
  // parallel_apply invokes `fn` from several std::threads. Two rules:
  //
  //  1. We MUST release the GIL here. The worker threads need to acquire it to
  //     call Python, and join() would otherwise block forever holding it.
  //     That is the classic binding deadlock.
  //  2. Each worker must ACQUIRE the GIL before touching Python. pybind11's
  //     std::function wrapper does that for us automatically, so the lambda
  //     body needs no extra code.
  //
  // Note this buys no parallelism for a Python callback — the GIL serialises
  // them. It is the correct pattern for a C++-heavy kernel that occasionally
  // calls back; genuine speedup requires the work to be in C++.
  m.def(
      "parallel_apply",
      [](const std::vector<double>& xs, const std::function<double(double)>& fn,
         std::size_t n_threads) {
        py::gil_scoped_release release;  // rule 1
        return plugin::parallel_apply(xs, fn, n_threads);
      },
      "xs"_a, "fn"_a, "n_threads"_a = 4);
}
