"""std::vector<T> in Python: copy vs opaque vs zero-copy view.

    cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j
    PYTHONPATH=build python run_vectors.py
"""

import numpy as np

import vectors_pb as v


def main() -> None:
    print("=" * 66)
    print("(A) automatic conversion  vector<double> <-> list   [COPIES]")
    print("=" * 66)
    lst = v.make_doubles(5)
    print("  make_doubles(5) ->", lst, type(lst).__name__)
    # The reverse direction accepts ANY Python sequence, not just a list.
    print("  sum_doubles([1,2,3])   =", v.sum_doubles([1, 2, 3]))
    print("  sum_doubles((1,2,3))   =", v.sum_doubles((1, 2, 3)))
    print("  sum_doubles(np.arange) =", v.sum_doubles(np.arange(4.0)))
    print("  sum_doubles(range(4))  =", v.sum_doubles(range(4)))

    print()
    print("=" * 66)
    print("(B) opaque binding        vector<int> -> VectorInt   [NO COPY]")
    print("=" * 66)
    vi = v.VectorInt()
    vi.append(10)
    vi.extend([20, 30])
    print("  VectorInt          ->", vi, "len =", len(vi))
    print("  vi[1]              ->", vi[1])
    print("  list(vi)           ->", list(vi))
    print("  sum_ints(vi)       ->", v.sum_ints(vi))
    vi[0] = 99  # mutation is visible to C++ — this is the point of opaque
    print("  after vi[0]=99     ->", v.sum_ints(vi))

    print()
    print("=" * 66)
    print("(C) NumPy view            vector<double> -> ndarray  [ZERO COPY]")
    print("=" * 66)
    cloud = v.Cloud(5)
    print("  cloud.sum()            =", cloud.sum())

    copy = cloud.values_copy  # (A) a snapshot
    view = cloud.values_view()  # (C) a window onto the same memory
    print("  values_copy            =", copy, type(copy).__name__)
    print("  values_view()          =", view, type(view).__name__)
    print("  view.flags.owndata     =", view.flags.owndata, "(False = it is a view)")
    print("  view.base is cloud     =", view.base is cloud, "(keep-alive works)")

    copy[0] = -1000.0  # edits the Python list only
    print("  after copy[0]=-1000    -> cloud.sum() =", cloud.sum(), "(unchanged!)")

    view[0] = -1000.0  # edits the C++ vector directly
    print("  after view[0]=-1000    -> cloud.sum() =", cloud.sum(), "(changed)")

    print()
    print("=" * 66)
    print("(D) vector of structs     vector<Point> -> list[Point]")
    print("=" * 66)
    pts = cloud.points
    print("  cloud.points[:2]       =", pts[:2])
    print("  pts[0].x, pts[0].label =", pts[0].x, ",", pts[0].label)
    p = v.Point(1.5, 2.5, "made-in-python")
    print("  constructed in Python  =", p)
    print("  sum_doubles([p.x,p.y]) =", v.sum_doubles([p.x, p.y]))

    print()
    print("=" * 66)
    print("(C') C++ allocates, NumPy owns it via a capsule deleter")
    print("=" * 66)
    a = v.make_array_no_copy(6)
    print("  make_array_no_copy(6)  =", a)
    print("  a.flags.owndata        =", a.flags.owndata)
    print("  type(a.base)           =", type(a.base).__name__, "(the capsule)")

    print()
    print("Rule of thumb:")
    print("  small / returned once      -> (A) let it copy, keep it simple")
    print("  large numeric buffer       -> (C) NumPy view or (C') capsule")
    print("  Python must mutate in place-> (B) opaque bind_vector")
    print("  vector of records          -> (D) bind the struct, or use a")
    print("                                structured dtype / one array per field")


if __name__ == "__main__":
    main()
