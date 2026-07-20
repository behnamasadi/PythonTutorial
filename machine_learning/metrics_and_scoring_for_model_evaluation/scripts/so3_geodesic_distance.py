#!/usr/bin/env python3
"""Render the SO(3) geodesic-distance figure.

Generates images/so3_geodesic_distance.png used by
metrics_and_scoring_methods.ipynb (section "mAA" -> "How is the error measured").

Two panels:
  Left  - concrete meaning: R_est is R_gt rotated by angle theta about a single
          axis n; that theta IS the rotation error (geodesic distance on SO(3)).
  Right - abstract meaning: SO(3) is a curved manifold. The error is the length
          of the shortest path (geodesic, drawn on a sphere for intuition),
          NOT the straight-line chord. geodesic = theta ; chord ~ sin(theta/2).

Key identities annotated:
  theta = arccos((tr(R_est R_gt^T) - 1) / 2)                 (geodesic distance)
  ||R_est - R_gt||_F = 2*sqrt(2)*sin(theta/2)                (Frobenius / chordal)
"""
import os
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

X, Y, Z = "#d62728", "#2ca02c", "#1f77b4"   # axis colors: x=red, y=green, z=blue
GEO = "#7b3fbf"                              # geodesic (purple)
CHORD = "#888888"                           # chord (gray)


def rot(axis, angle):
    """Rodrigues rotation matrix for `axis` (need not be unit) and `angle` rad."""
    a = np.asarray(axis, float)
    a = a / np.linalg.norm(a)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * (K @ K)


def triad(ax, R, origin=(0, 0, 0), length=1.0, ls="-", alpha=1.0, lw=2.5, tag=""):
    """Draw the coordinate frame whose axes are the columns of R."""
    o = np.asarray(origin, float)
    for j, c in enumerate((X, Y, Z)):
        v = R[:, j] * length
        ax.quiver(*o, *v, color=c, linewidth=lw, arrow_length_ratio=0.12,
                  linestyle=ls, alpha=alpha)
    if tag:
        tip = o + R[:, 2] * length * 1.15
        ax.text(*tip, tag, fontsize=11, fontweight="bold")


fig = plt.figure(figsize=(13.5, 6.2))
fig.suptitle(r"SO(3) geodesic distance = the rotation error $\theta$",
             fontsize=15, fontweight="bold")

# --------------------------------------------------------------------------
# Panel A - the shortest rotation carrying R_gt onto R_est
# --------------------------------------------------------------------------
axA = fig.add_subplot(1, 2, 1, projection="3d")
theta = np.radians(75)                       # the rotation error
n = np.array([0.25, 0.15, 1.0])              # relative-rotation axis
n = n / np.linalg.norm(n)
R_gt = np.eye(3)
R_est = rot(n, theta) @ R_gt

triad(axA, R_gt, length=1.0, ls="-", alpha=1.0, tag=r"$R_{gt}$")
triad(axA, R_est, length=1.0, ls="--", alpha=0.55, lw=2.2, tag=r"$R_{est}$")

# rotation axis n
axA.quiver(0, 0, 0, *(n * 1.35), color="k", lw=1.6, arrow_length_ratio=0.1)
axA.text(*(n * 1.5), r"$n$", fontsize=12, fontweight="bold")

# geodesic sweep: an arc of angle theta in the plane perpendicular to n
u = np.cross(n, [0, 0, 1]); u = u / np.linalg.norm(u)
v = np.cross(n, u)
r = 0.62
a = np.linspace(0, theta, 60)
arc = (r * (np.cos(a)[:, None] * u + np.sin(a)[:, None] * v)).T
axA.plot(arc[0], arc[1], arc[2], color=GEO, lw=3)
tan = arc[:, -1] - arc[:, -6]
tan = tan / np.linalg.norm(tan) * 0.2                          # short, clean arrowhead
axA.quiver(*arc[:, -1], *tan, color=GEO, arrow_length_ratio=0.55, lw=3)
mid = arc[:, arc.shape[1] // 2] * 1.25
axA.text(*mid, r"$\theta$", color=GEO, fontsize=16, fontweight="bold")

axA.set_title(r"$R_\Delta = R_{est}R_{gt}^{\top}$: rotate $R_{gt}$ by $\theta$ about $n$",
              fontsize=11)
axA.set_xlim(-1, 1); axA.set_ylim(-1, 1); axA.set_zlim(-0.6, 1.3)
axA.set_box_aspect((1, 1, 1)); axA.view_init(elev=20, azim=35)
axA.set_xticks([]); axA.set_yticks([]); axA.set_zticks([])

# --------------------------------------------------------------------------
# Panel B - geodesic (arc) vs chord on a curved manifold (sphere for intuition)
# --------------------------------------------------------------------------
axB = fig.add_subplot(1, 2, 2, projection="3d")

# translucent sphere
uu, vv = np.mgrid[0:2 * np.pi:40j, 0:np.pi:20j]
axB.plot_surface(np.cos(uu) * np.sin(vv), np.sin(uu) * np.sin(vv), np.cos(vv),
                 color="#cfe3f7", alpha=0.18, linewidth=0, shade=False)
axB.plot_wireframe(np.cos(uu) * np.sin(vv), np.sin(uu) * np.sin(vv), np.cos(vv),
                   color="#b8d4ea", alpha=0.35, linewidth=0.4)

# two points on the sphere = two rotations
def sph(lat, lon):
    lat, lon = np.radians(lat), np.radians(lon)
    return np.array([np.cos(lat) * np.cos(lon), np.cos(lat) * np.sin(lon), np.sin(lat)])

p1, p2 = sph(18, -35), sph(52, 45)
th = np.arccos(np.clip(p1 @ p2, -1, 1))

# geodesic = great-circle arc (slerp)
t = np.linspace(0, 1, 80)
so = np.sin(th)
arcB = np.array([(np.sin((1 - ti) * th) / so) * p1 + (np.sin(ti * th) / so) * p2 for ti in t]).T
axB.plot(arcB[0], arcB[1], arcB[2], color=GEO, lw=3.5, label=r"geodesic (arc) = $\theta$")

# chord = straight line through the interior
axB.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color=CHORD, lw=2,
         ls="--", label=r"chord $\propto \sin(\theta/2)$")

# radii from centre + points
for p in (p1, p2):
    axB.plot([0, p[0]], [0, p[1]], [0, p[2]], color="k", lw=0.9, alpha=0.6)
axB.scatter(*p1, color=GEO, s=45); axB.scatter(*p2, color=GEO, s=45)
axB.text(*(p1 * 1.12), r"$R_{gt}$", fontsize=11, fontweight="bold")
axB.text(*(p2 * 1.12), r"$R_{est}$", fontsize=11, fontweight="bold")
axB.text(*(arcB[:, len(t) // 2] * 1.18), r"$\theta$", color=GEO, fontsize=15,
         fontweight="bold")

axB.set_title("curved manifold: error is the arc length, not the chord", fontsize=11)
axB.set_xlim(-1, 1); axB.set_ylim(-1, 1); axB.set_zlim(-1, 1)
axB.set_box_aspect((1, 1, 1)); axB.view_init(elev=22, azim=-60)
axB.set_xticks([]); axB.set_yticks([]); axB.set_zticks([])
axB.legend(loc="upper left", fontsize=9, frameon=False)

fig.text(0.5, 0.02,
         r"$\theta=\arccos\dfrac{\mathrm{tr}(R_{est}R_{gt}^{\top})-1}{2}$"
         r"$\qquad\|R_{est}-R_{gt}\|_F = 2\sqrt{2}\,\sin(\theta/2)$"
         r"$\qquad$ geodesic $\theta \geq$ chordal separation",
         ha="center", fontsize=12)

fig.tight_layout(rect=(0, 0.05, 1, 0.94))

img_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "images"))
out = os.path.join(img_dir, "so3_geodesic_distance.png")
fig.savefig(out, dpi=140, bbox_inches="tight")
print(f"wrote {out}")
print(f"panel A theta = {np.degrees(theta):.1f} deg ; panel B theta = {np.degrees(th):.1f} deg")
