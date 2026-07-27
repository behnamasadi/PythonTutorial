// A flat C ABI in front of the C++ API.
//
// ctypes and cffi can ONLY call C. They cannot see C++ names (they are mangled),
// cannot construct C++ objects, and cannot catch C++ exceptions. So if you want
// to use them, *you* have to write this shim by hand:
//
//   - classes           -> opaque pointer + create/destroy/method functions
//   - std::string       -> const char*
//   - std::vector<T>    -> T* + size_t, or a copy-out function
//   - exceptions        -> integer status code + out-parameter
//
// Notice how much code this is for four small entities. That cost is the main
// reason most projects reach for pybind11/nanobind instead.
#pragma once

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

// `extern "C"` disables C++ name mangling, so the symbol in the .so is literally
// "ml_add" and dlsym() can find it.

double ml_add(double a, double b);

void ml_scale_inplace(double* data, size_t n, double factor);

// Exceptions cannot cross a C ABI boundary. Return 0 on success, non-zero on
// error, and write the result through a pointer.
int ml_divide(double a, double b, double* out_result);

// --- Accumulator, as an opaque handle -------------------------------------
typedef struct MlAccumulator MlAccumulator;  // incomplete type: Python only
                                             // ever holds a pointer to it.

MlAccumulator* ml_acc_create(double start, const char* name);
void ml_acc_destroy(MlAccumulator* self);       // caller MUST call this
void ml_acc_add(MlAccumulator* self, double v);
double ml_acc_total(const MlAccumulator* self);
size_t ml_acc_size(const MlAccumulator* self);
const char* ml_acc_name(const MlAccumulator* self);  // borrowed, valid while
                                                     // the object lives
// Copy the history into a caller-provided buffer; returns the number written.
size_t ml_acc_history(const MlAccumulator* self, double* out, size_t capacity);

#ifdef __cplusplus
}  // extern "C"
#endif
