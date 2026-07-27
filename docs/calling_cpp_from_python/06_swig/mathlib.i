/* SWIG interface file.
 *
 * SWIG parses your real C++ headers and *generates* the glue code. You write a
 * small .i file instead of binding code. Its selling point is that the same .i
 * can also emit Java, C#, Ruby, Lua, ... bindings.
 *
 * Build:
 *   swig -c++ -python -I../cpp -o mathlib_swig_wrap.cxx mathlib.i
 *   g++ -O2 -std=c++17 -shared -fPIC -I../cpp $(python-config --includes) \
 *       mathlib_swig_wrap.cxx ../cpp/mathlib.cpp -o _mathlib_swig.so
 *
 * SWIG produces TWO artifacts: mathlib_swig.py (the Python-side shim) and
 * _mathlib_swig.so (the compiled part). You must ship both.
 */

%module mathlib_swig

%{
/* Verbatim block: copied into the generated .cxx so it can compile. */
#include "mathlib.hpp"
%}

/* Typemap libraries: teach SWIG about std::string / std::vector so they
   convert to str / list instead of becoming opaque proxy objects. */
%include "std_string.i"
%include "std_vector.i"
%include "exception.i"

/* Instantiate the template you actually use. SWIG cannot bind a template,
   only a concrete instantiation — a recurring annoyance with C++ libraries. */
%template(DoubleVector) std::vector<double>;

/* Turn C++ exceptions into Python exceptions. Without this, a throw crossing
   the boundary terminates the interpreter. */
%exception {
  try {
    $action
  } catch (const std::invalid_argument& e) {
    SWIG_exception(SWIG_ValueError, e.what());
  } catch (const std::exception& e) {
    SWIG_exception(SWIG_RuntimeError, e.what());
  }
}

/* Now just point SWIG at the real header: it generates bindings for
   everything declared in it. */
%include "mathlib.hpp"
