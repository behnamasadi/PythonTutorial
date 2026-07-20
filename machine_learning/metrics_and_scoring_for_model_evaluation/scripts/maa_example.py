#!/usr/bin/env python3
"""mAA (mean Average Accuracy) worked example for camera-pose estimation.

Companion code for metrics_and_scoring_methods.ipynb (section 1.7.1 "mAA").
The notebook works the numbers by hand; this script reproduces them and
renders the cumulative-accuracy staircase.

Outputs:
  - prints the rotation-error identity check (matrix / quaternion / angle-axis)
  - prints per-scene AA and the final mAA for the notebook's `scenes` data
  - writes images/maa_cumulative_accuracy.png  (the Acc(theta) staircase = error CDF)
"""
import os
import numpy as np
from scipy.spatial.transform import Rotation as Rot
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# 1) How the rotation error (deg) is measured: three equivalent geodesic angles.
#    err = angle of the relative rotation R_est @ R_gt^T ; same in every rep.
# ---------------------------------------------------------------------------
R_gt = Rot.from_euler("xyz", [10, 20, 30], degrees=True)
R_est = Rot.from_euler("xyz", [11, 18, 31], degrees=True)              # slightly off

R_rel = R_est.as_matrix() @ R_gt.as_matrix().T
ang_trace = np.degrees(np.arccos(np.clip((np.trace(R_rel) - 1) / 2, -1.0, 1.0)))
ang_quat = np.degrees(2 * np.arccos(np.clip(abs(np.dot(R_gt.as_quat(), R_est.as_quat())), -1, 1)))
ang_axis = np.degrees(np.linalg.norm((R_est * R_gt.inv()).as_rotvec()))
print(f"rotation error : trace={ang_trace:.4f}  quat={ang_quat:.4f}  angle-axis={ang_axis:.4f} (deg)")

# translation error for RELATIVE pose = angle between direction vectors (scale unknown)
t_gt, t_est = np.array([1.0, 0.0, 0.5]), np.array([0.9, 0.1, 0.55])
ang_t = np.degrees(np.arccos(np.clip(t_gt @ t_est / (np.linalg.norm(t_gt) * np.linalg.norm(t_est)), -1, 1)))
print(f"translation err: direction angle = {ang_t:.4f} deg  (absolute pose would use ||t_est - t_gt|| in m)\n")


# ---------------------------------------------------------------------------
# 2) mAA over the notebook's scenes. Each row is one IMAGE PAIR:
#    (rotation_err_deg, translation_err_deg).
# ---------------------------------------------------------------------------
scenes = {
    "scene_A": np.array([(0.5, 1.2), (2.1, 3.0), (0.9, 0.7), (8.0, 12.0), (1.5, 2.2)]),
    "scene_B": np.array([(3.2, 4.1), (0.8, 1.0), (15.0, 20.0), (2.0, 1.8), (4.5, 5.0)]),
}
thr = np.arange(1, 11)                        # thresholds 1..10 degrees


def average_accuracy(errors, thresholds):
    """AA = mean over thresholds of the fraction within tolerance
    = normalized area under the accuracy-vs-threshold (cumulative) curve."""
    errors = np.asarray(errors, float)
    acc = np.array([(errors <= t).mean() for t in thresholds])
    return acc.mean(), acc


per_scene_aa = {}
for name, errs in scenes.items():
    combined = errs.max(axis=1)               # a pair passes theta only if BOTH R and t do
    aa, acc = average_accuracy(combined, thr)
    per_scene_aa[name] = aa
    print(f"{name}: sorted combined err = {sorted(combined)}")
    print(f"{name}: Acc@theta = {np.round(acc, 2)}  ->  AA = {aa:.4f}")

mAA = float(np.mean(list(per_scene_aa.values())))
acc5 = float(np.mean([(scenes[s].max(axis=1) <= 5).mean() for s in scenes]))
print(f"\nmAA = mean over scenes = {mAA:.4f}")
print(f"plain accuracy @ 5deg  = {acc5:.4f}  (single threshold -- less informative than mAA)")


# ---------------------------------------------------------------------------
# 3) Figure: Acc(theta) is the empirical CDF of the errors -> a rising staircase.
#    Uses the 5-camera micro-example from the notebook (one 30-deg outlier).
# ---------------------------------------------------------------------------
micro = np.array([0.4, 1.2, 2.6, 4.9, 30.0])
acc_micro = np.array([(micro <= t).mean() for t in thr])

fig, ax = plt.subplots(figsize=(7.5, 4.2))
ax.step(thr, acc_micro, where="post", color="#1f77b4", lw=2.5, label="Acc(θ) = error CDF")
ax.fill_between(thr, acc_micro, step="post", alpha=0.15, color="#1f77b4",
                label=f"area = AA = {acc_micro.mean():.2f}")
for e in micro[micro <= thr.max()]:
    ax.axvline(e, color="gray", ls=":", lw=0.9)
    ax.text(e, 0.02, f"{e:g}°", color="gray", fontsize=8, ha="center")
ax.set_xlabel("threshold θ (degrees)  —  looser tolerance →")
ax.set_ylabel("Acc(θ) = fraction of poses within θ")
ax.set_title("Acc(θ) only ever climbs (cumulative): each error crossed adds 1/N")
ax.set_ylim(0, 1.05)
ax.set_xticks(thr)
ax.legend(loc="lower right")
ax.grid(alpha=0.3)
fig.tight_layout()

img_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "images"))
out = os.path.join(img_dir, "maa_cumulative_accuracy.png")
fig.savefig(out, dpi=140, bbox_inches="tight")
print(f"\nwrote {out}")
