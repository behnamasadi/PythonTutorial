// How do you get a std::vector<T> into Python? There are FOUR answers and they
// behave very differently. This module demonstrates all of them side by side.
//
//   (A) automatic conversion   vector<double>  -> list[float]     COPY
//   (B) opaque binding         vector<double>  -> VectorDouble    NO COPY, mutable
//   (C) NumPy view             vector<double>  -> np.ndarray      NO COPY, zero-copy
//   (D) vector of structs      vector<Point>   -> list[Point]     copy of handles
//
// The single most common bug: (A) copies, so `obj.data().append(1)` in Python
// silently does nothing to the C++ side. (B) and (C) fix that.

#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>        // enables (A): vector<->list, map<->dict, ...
#include <pybind11/stl_bind.h>   // enables (B): py::bind_vector

#include <numeric>
#include <string>
#include <vector>

namespace py = pybind11;
using namespace pybind11::literals;

// --------------------------------------------------------------- C++ side
struct Point {
  double x{0}, y{0};
  std::string label;
};

// A class that OWNS a vector, so we can show mutation semantics.
struct Cloud {
  std::vector<double> values;
  std::vector<Point> points;

  explicit Cloud(std::size_t n) {
    values.resize(n);
    std::iota(values.begin(), values.end(), 0.0);
    for (std::size_t i = 0; i < n; ++i) {
      points.push_back(Point{static_cast<double>(i), static_cast<double>(i * i),
                             "p" + std::to_string(i)});
    }
  }
  double sum() const {
    return std::accumulate(values.begin(), values.end(), 0.0);
  }
};

// IMPORTANT: this must appear BEFORE any binding that touches
// std::vector<double>. It disables the automatic copy-conversion from
// <pybind11/stl.h> for this exact type, so it can be bound as a real class.
PYBIND11_MAKE_OPAQUE(std::vector<int>);

std::vector<double> make_doubles(std::size_t n) {
  std::vector<double> v(n);
  std::iota(v.begin(), v.end(), 1.0);
  return v;
}

double sum_doubles(const std::vector<double>& v) {
  return std::accumulate(v.begin(), v.end(), 0.0);
}

PYBIND11_MODULE(vectors_pb, m) {
  m.doc() = "Four ways to expose std::vector<T> to Python";

  // ================================================================== (A)
  // Automatic conversion. Include <pybind11/stl.h> and you are done.
  // vector<double> <-> list[float], and it works in BOTH directions.
  //
  // Cost: a full element-by-element COPY on every crossing. Fine for small
  // vectors and function returns; terrible for a 10M-element buffer in a loop.
  m.def("make_doubles", &make_doubles, "n"_a,
        "Returns a Python list (copy of the C++ vector)");
  m.def("sum_doubles", &sum_doubles, "v"_a,
        "Accepts any Python sequence of floats (copied into a C++ vector)");

  // ================================================================== (B)
  // Opaque binding: expose std::vector<int> as a real Python class with
  // append/__getitem__/__len__/iteration/slicing. No copy on crossing, and
  // mutations from Python are visible to C++.
  //
  // Requires PYBIND11_MAKE_OPAQUE(std::vector<int>) above.
  py::bind_vector<std::vector<int>>(m, "VectorInt");
  m.def("sum_ints", [](const std::vector<int>& v) {
    return std::accumulate(v.begin(), v.end(), 0);
  });

  // ================================================================== (D)
  // A vector of user-defined structs. Bind the element type as a class, then
  // vector<Point> converts to a list[Point] via <pybind11/stl.h>.
  py::class_<Point>(m, "Point")
      .def(py::init<>())
      .def(py::init([](double x, double y, std::string label) {
             return Point{x, y, std::move(label)};
           }),
           "x"_a, "y"_a, "label"_a = "")
      .def_readwrite("x", &Point::x)
      .def_readwrite("y", &Point::y)
      .def_readwrite("label", &Point::label)
      .def("__repr__", [](const Point& p) {
        return "Point(x=" + std::to_string(p.x) + ", y=" + std::to_string(p.y) +
               ", label='" + p.label + "')";
      });

  py::class_<Cloud>(m, "Cloud")
      .def(py::init<std::size_t>(), "n"_a)
      .def("sum", &Cloud::sum)

      // ---- (A) again, as a property: this COPIES. Mutating the returned
      //      list does NOT change the C++ vector. This surprises everyone.
      .def_property_readonly(
          "values_copy", [](const Cloud& c) { return c.values; },
          "list[float] — a snapshot copy; edits do not reach C++")

      // ================================================================ (C)
      // Zero-copy NumPy view onto the vector's memory.
      //
      // The second argument to py::array_t is the *base* object: it keeps the
      // Cloud alive as long as the array exists. WITHOUT it you get a dangling
      // pointer the moment the Cloud is collected — a use-after-free that
      // looks like random numbers.
      //
      // Danger: if C++ later push_back()s and the vector reallocates, this
      // view still points at the freed buffer. Only expose a view when the
      // buffer's lifetime and size are stable.
      .def(
          "values_view",
          [](py::object self) {
            Cloud& c = self.cast<Cloud&>();
            return py::array_t<double>(
                {static_cast<py::ssize_t>(c.values.size())},  // shape
                {sizeof(double)},                             // strides (bytes)
                c.values.data(),                              // the raw pointer
                self);                                        // base / keep-alive
          },
          "np.ndarray view — zero copy, writes go straight into the C++ vector")

      // ---- (D): list of Point objects
      .def_property_readonly(
          "points", [](const Cloud& c) { return c.points; },
          "list[Point] — the Point objects themselves are copies too");

  // ================================================================== (C')
  // Returning a vector as an array WITHOUT copying, when C++ hands over
  // ownership: move the vector to the heap and attach a capsule that deletes
  // it when NumPy is done with the array. This is the standard idiom for
  // "compute a big buffer in C++ and give it to Python".
  m.def(
      "make_array_no_copy",
      [](std::size_t n) {
        auto* v = new std::vector<double>(make_doubles(n));
        // The capsule is NumPy's deleter hook.
        py::capsule owner(v, [](void* p) {
          delete reinterpret_cast<std::vector<double>*>(p);
        });
        return py::array_t<double>({static_cast<py::ssize_t>(v->size())},
                                   {sizeof(double)}, v->data(), owner);
      },
      "n"_a, "np.ndarray that owns the C++ vector via a capsule deleter");
}
