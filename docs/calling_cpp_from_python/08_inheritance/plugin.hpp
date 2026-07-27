// A plugin-style C++ API: an abstract base class that C++ code calls through,
// plus functions that take Python callables. This is the shape you hit the
// moment you bind a *real* library rather than a bag of free functions.
//
// The hard part is that the arrows point BOTH ways:
//   Python -> C++   is easy (that is what every other example does)
//   C++    -> Python is the interesting half: C++ calling a virtual method that
//                    a Python subclass overrode, or invoking a Python lambda.
#pragma once

#include <cstddef>
#include <functional>
#include <memory>
#include <string>
#include <vector>

namespace plugin {

// --------------------------------------------------------------- enums
enum class Mode { Fast, Accurate };

std::string describe(Mode m);

// ------------------------------------------------- abstract base class
class Filter {
 public:
  virtual ~Filter() = default;

  // Pure virtual: a Python subclass MUST provide this.
  virtual double apply(double x) const = 0;

  // Virtual with a default: a Python subclass MAY override it.
  virtual std::string name() const { return "filter"; }

  // Non-virtual, and the whole point of the exercise: this is C++ code that
  // calls apply() in a loop. If a Python subclass overrode apply(), C++ must
  // end up calling back into Python here.
  double apply_all(const std::vector<double>& xs) const;
};

// A concrete C++ implementation, so we can show C++ and Python subclasses
// living side by side behind the same base pointer.
class Scale : public Filter {
 public:
  explicit Scale(double factor = 2.0) : factor_(factor) {}
  double apply(double x) const override { return x * factor_; }
  std::string name() const override { return "scale"; }
  double factor() const { return factor_; }

 private:
  double factor_;
};

// A factory returning a base-class pointer — the classic C++ idiom that
// bindings must map onto Python's object model.
std::unique_ptr<Filter> make_scale(double factor);

// Free function taking the base by reference: dispatches virtually, and works
// identically whether `f` came from C++ or from Python.
double pipeline_sum(const Filter& f, const std::vector<double>& xs);

// ------------------------------------------------------- callbacks in
// A C++ function that takes a callable. Bound to accept ANY Python callable.
double transform_sum(const std::vector<double>& xs,
                     const std::function<double(double)>& fn);

// A class that STORES a callback and invokes it later. Storing is what makes
// lifetime interesting: the Python object must outlive the C++ object.
class Button {
 public:
  void on_click(std::function<void(int)> cb) { cb_ = std::move(cb); }
  void click();
  int clicks() const { return clicks_; }

 private:
  std::function<void(int)> cb_;
  int clicks_ = 0;
};

// Invoke a callback from worker threads. The GIL rules here are the ones that
// cause real deadlocks and crashes — see the bindings for the details.
std::vector<double> parallel_apply(const std::vector<double>& xs,
                                   const std::function<double(double)>& fn,
                                   std::size_t n_threads);

}  // namespace plugin
