// The "existing C++ API" that every binding technique in this tutorial wraps.
// Nothing here knows about Python — that is the whole point.
#pragma once

#include <cstddef>
#include <stdexcept>
#include <string>
#include <vector>

namespace mathlib {

// 1. A plain free function (the "hello world" of bindings).
double add(double a, double b);

// 2. A function that mutates a raw buffer in place. This is what you use to
//    talk to NumPy without copying.
void scale_inplace(double* data, std::size_t n, double factor);

// 3. A function that throws, to show exception translation.
double divide(double a, double b);

// 4. A class with state, a std::vector member, and a std::string.
//    Binding *this* is where the techniques really differ.
class Accumulator {
 public:
  explicit Accumulator(double start = 0.0, std::string name = "acc");

  void add(double value);
  double total() const { return total_; }
  const std::string& name() const { return name_; }
  void set_name(const std::string& name) { name_ = name; }
  std::vector<double> history() const { return history_; }
  std::size_t size() const { return history_.size(); }

 private:
  double total_;
  std::string name_;
  std::vector<double> history_;
};

}  // namespace mathlib
