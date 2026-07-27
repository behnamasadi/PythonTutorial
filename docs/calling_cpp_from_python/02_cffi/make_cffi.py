"""cffi, "API mode": generate + compile a real extension module.

    pip install cffi
    python make_cffi.py           # produces _mathlib_cffi*.so
    python run_cffi.py

Unlike ctypes, you paste the actual C declarations and cffi runs a C compiler.
That means the signatures are checked by the compiler, not by you, and the call
overhead is much lower (it is a compiled extension, not runtime dlsym).

cffi also has an "ABI mode" (ffi.dlopen) that behaves like ctypes: no compiler,
no checking. Prefer API mode for anything you ship.
"""

import pathlib

from cffi import FFI

HERE = pathlib.Path(__file__).resolve().parent
CPP = HERE.parent / "cpp"

ffibuilder = FFI()

# 1. cdef(): the declarations Python should know about.
#    This is *parsed C* — no #include, no #ifdef, no C++ here.
ffibuilder.cdef(
    """
    double ml_add(double a, double b);
    void   ml_scale_inplace(double *data, size_t n, double factor);
    int    ml_divide(double a, double b, double *out_result);

    typedef struct MlAccumulator MlAccumulator;
    MlAccumulator* ml_acc_create(double start, const char* name);
    void   ml_acc_destroy(MlAccumulator* self);
    void   ml_acc_add(MlAccumulator* self, double v);
    double ml_acc_total(const MlAccumulator* self);
    size_t ml_acc_size(const MlAccumulator* self);
    const char* ml_acc_name(const MlAccumulator* self);
    size_t ml_acc_history(const MlAccumulator* self, double* out, size_t capacity);
    """
)

# 2. set_source(): the real C/C++ that gets compiled into the extension.
ffibuilder.set_source(
    "_mathlib_cffi",
    '#include "c_api.h"',
    sources=[str(CPP / "mathlib.cpp"), str(CPP / "c_api.cpp")],
    include_dirs=[str(CPP)],
    source_extension=".cpp",          # tell cffi to drive the C++ compiler
    extra_compile_args=["-std=c++17"],
)

if __name__ == "__main__":
    # tmpdir also receives the intermediate .o tree, so keep it out of the way.
    out = HERE / "build"
    out.mkdir(exist_ok=True)
    so = ffibuilder.compile(tmpdir=str(out), verbose=True)
    # Put the finished module where run_cffi.py can import it.
    pathlib.Path(so).replace(HERE / pathlib.Path(so).name)
