#include "mathlib.hpp"

#include <utility>

namespace mathlib {

double add(double a, double b) { return a + b; }

void scale_inplace(double* data, std::size_t n, double factor) {
  for (std::size_t i = 0; i < n; ++i) {
    data[i] *= factor;
  }
}

double divide(double a, double b) {
  if (b == 0.0) {
    throw std::invalid_argument("division by zero");
  }
  return a / b;
}

Accumulator::Accumulator(double start, std::string name)
    : total_(start), name_(std::move(name)) {
  history_.push_back(start);
}

void Accumulator::add(double value) {
  total_ += value;
  history_.push_back(total_);
}

}  // namespace mathlib
