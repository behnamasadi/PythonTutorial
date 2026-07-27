#include "c_api.h"

#include <algorithm>
#include <cstring>
#include <new>

#include "mathlib.hpp"

// The opaque struct is just a C++ object in disguise.
struct MlAccumulator {
  mathlib::Accumulator impl;
  MlAccumulator(double start, const char* name) : impl(start, name ? name : "acc") {}
};

extern "C" {

double ml_add(double a, double b) { return mathlib::add(a, b); }

void ml_scale_inplace(double* data, size_t n, double factor) {
  mathlib::scale_inplace(data, n, factor);
}

int ml_divide(double a, double b, double* out_result) {
  // Every C entry point must be noexcept in practice: letting a C++ exception
  // unwind through C frames is undefined behaviour.
  try {
    *out_result = mathlib::divide(a, b);
    return 0;
  } catch (const std::exception&) {
    return 1;
  }
}

MlAccumulator* ml_acc_create(double start, const char* name) {
  try {
    return new MlAccumulator(start, name);
  } catch (...) {
    return nullptr;
  }
}

void ml_acc_destroy(MlAccumulator* self) { delete self; }

void ml_acc_add(MlAccumulator* self, double v) { self->impl.add(v); }

double ml_acc_total(const MlAccumulator* self) { return self->impl.total(); }

size_t ml_acc_size(const MlAccumulator* self) { return self->impl.size(); }

const char* ml_acc_name(const MlAccumulator* self) {
  return self->impl.name().c_str();
}

size_t ml_acc_history(const MlAccumulator* self, double* out, size_t capacity) {
  const std::vector<double> h = self->impl.history();
  const size_t n = std::min(capacity, h.size());
  std::memcpy(out, h.data(), n * sizeof(double));
  return n;
}

}  // extern "C"
