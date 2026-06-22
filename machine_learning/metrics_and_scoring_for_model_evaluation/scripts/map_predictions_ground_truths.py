#!/usr/bin/env python3
"""Render the multi-class, multi-image mAP worked example figure.

Generates images/predictions_ground_truths_mAP.png used by
metrics_and_scoring_methods.ipynb (section "mAP").

Setup: 3 images, 2 classes (Cat, Dog), IoU threshold tau = 0.5.
  Green dashed box = ground truth (GT)
  Solid box        = prediction (blue = Cat, orange = Dog)
  Label            = class, confidence, IoU to matched GT, and TP/FP/FN.

The numbers here match exactly the tables computed in the notebook:
  AP_cat = 0.667, AP_dog = 0.833  ->  mAP@0.5 = 0.75
"""
import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

CAT = "#1f77b4"   # blue  -> Cat predictions
DOG = "#ff7f0e"   # orange -> Dog predictions
GT = "#2ca02c"    # green  -> ground truth

# Each panel is a 0..10 x 0..10 canvas.
# A box is (x, y, w, h). GT boxes are dashed green; predictions are solid colored.
# "fn" marks a ground-truth object that no prediction matched (missed detection).
images = {
    "Image 1": {
        "gt": [
            ("Cat", (1.0, 5.0, 3.0, 3.5)),
            ("Dog", (5.8, 0.8, 3.3, 3.2)),
        ],
        "pred": [
            ("Cat", CAT, (1.2, 5.1, 2.9, 3.3), 0.95, 0.90, "TP"),
            ("Cat", CAT, (1.3, 2.6, 2.6, 2.2), 0.60, 0.40, "FP"),
            ("Dog", DOG, (5.9, 0.9, 3.1, 3.0), 0.90, 0.85, "TP"),
        ],
        "fn": [],
    },
    "Image 2": {
        "gt": [
            ("Cat", (2.0, 3.5, 3.4, 3.6)),
        ],
        "pred": [
            ("Cat", CAT, (2.2, 3.7, 3.2, 3.3), 0.85, 0.70, "TP"),
            ("Dog", DOG, (6.2, 1.0, 2.8, 2.6), 0.75, 0.00, "FP"),
        ],
        "fn": [],
    },
    "Image 3": {
        "gt": [
            ("Cat", (0.6, 6.0, 2.6, 2.7)),   # this Cat GT is never matched -> FN
            ("Dog", (5.4, 5.6, 3.3, 2.9)),
            ("Dog", (5.2, 1.7, 3.0, 2.6)),
        ],
        "pred": [
            ("Cat", CAT, (0.9, 1.7, 2.1, 1.9), 0.50, 0.10, "FP"),
            ("Dog", DOG, (5.5, 5.7, 3.0, 2.6), 0.70, 0.60, "TP"),
            ("Dog", DOG, (5.3, 1.8, 2.8, 2.4), 0.55, 0.55, "TP"),
        ],
        "fn": ["Cat GT (missed -> FN)"],
    },
}

fig, axes = plt.subplots(1, 3, figsize=(16, 6))
fig.suptitle(
    "mAP worked example - 3 images, 2 classes (Cat, Dog), IoU threshold tau = 0.5",
    fontsize=15, fontweight="bold",
)

for ax, (title, data) in zip(axes, images.items()):
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])

    # ground-truth boxes (green dashed)
    for cls, (x, y, w, h) in data["gt"]:
        ax.add_patch(Rectangle((x, y), w, h, fill=False, edgecolor=GT,
                               linestyle="--", linewidth=2.2))
        ax.text(x, y + h + 0.12, f"GT {cls}", color=GT, fontsize=9,
                fontweight="bold")

    # prediction boxes (solid, colored by class)
    for cls, color, (x, y, w, h), conf, iou, tag in data["pred"]:
        ax.add_patch(Rectangle((x, y), w, h, fill=False, edgecolor=color,
                               linewidth=2.4))
        verdict = "TP" if tag == "TP" else "FP"
        ax.text(x, y - 0.45,
                f"{cls}  conf={conf:.2f}\nIoU={iou:.2f}  {verdict}",
                color=color, fontsize=8.5, va="top", fontweight="bold")

    # missed ground truth note
    for i, note in enumerate(data["fn"]):
        ax.text(0.4, 5.2 + i * 0.6, note, color="red", fontsize=8.5,
                fontstyle="italic")

# shared legend
legend_handles = [
    Line2D([0], [0], color=GT, lw=2.2, ls="--", label="Ground truth (GT)"),
    Line2D([0], [0], color=CAT, lw=2.4, label="Prediction: Cat"),
    Line2D([0], [0], color=DOG, lw=2.4, label="Prediction: Dog"),
]
fig.legend(handles=legend_handles, loc="lower center", ncol=3, fontsize=11,
           frameon=False, bbox_to_anchor=(0.5, -0.02))

fig.tight_layout(rect=(0, 0.04, 1, 0.95))

img_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "images"))
out = os.path.join(img_dir, "predictions_ground_truths_mAP.png")
fig.savefig(out, dpi=130, bbox_inches="tight")
print(f"wrote {out}")


# ---------------------------------------------------------------------------
# Second figure: per-class Precision-Recall curves for the SAME example.
# AP is computed with the Pascal VOC (2010+) "all-point" area method so the
# numbers match the tables in the notebook exactly.
# ---------------------------------------------------------------------------
import numpy as np


def average_precision(confidences, is_tp, n_gt):
    """All-point (area-under-PR) AP. Inputs need not be pre-sorted."""
    order = np.argsort(-np.asarray(confidences))
    tp = np.asarray(is_tp, dtype=float)[order]
    fp = 1.0 - tp
    cum_tp = np.cumsum(tp)
    cum_fp = np.cumsum(fp)
    recall = cum_tp / n_gt
    precision = cum_tp / np.maximum(cum_tp + cum_fp, 1e-12)

    mrec = np.concatenate(([0.0], recall, [1.0]))
    mpre = np.concatenate(([0.0], precision, [0.0]))
    for i in range(len(mpre) - 2, -1, -1):       # monotone-decreasing envelope
        mpre[i] = max(mpre[i], mpre[i + 1])
    idx = np.where(mrec[1:] != mrec[:-1])[0]
    ap = float(np.sum((mrec[idx + 1] - mrec[idx]) * mpre[idx + 1]))
    return ap, recall, precision, mrec, mpre


# (confidence, is_TP) per class, exactly as drawn above.
per_class = {
    "Cat": {"color": CAT, "n_gt": 3,
            "dets": [(0.95, 1), (0.85, 1), (0.60, 0), (0.50, 0)]},
    "Dog": {"color": DOG, "n_gt": 3,
            "dets": [(0.90, 1), (0.75, 0), (0.70, 1), (0.55, 1)]},
}

fig2, axes2 = plt.subplots(1, 2, figsize=(12, 5))
aps = {}
for ax, (cls, d) in zip(axes2, per_class.items()):
    conf = [c for c, _ in d["dets"]]
    tp = [t for _, t in d["dets"]]
    ap, rec, prec, mrec, mpre = average_precision(conf, tp, d["n_gt"])
    aps[cls] = ap

    ax.step(np.concatenate(([0], rec)), np.concatenate(([prec[0]], prec)),
            where="post", color=d["color"], lw=2, label="raw PR")
    ax.plot(mrec, mpre, color="gray", ls="--", lw=1.5, label="interpolated envelope")
    ax.fill_between(mrec, mpre, step="pre", alpha=0.12, color=d["color"])
    ax.scatter(rec, prec, color=d["color"], zorder=5)
    ax.set_title(f"{cls}: AP = {ap:.3f}", fontsize=13, fontweight="bold")
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_xlim(-0.02, 1.05)
    ax.set_ylim(0, 1.05)
    ax.grid(alpha=0.3)
    ax.legend(loc="lower left", fontsize=9)

mAP = sum(aps.values()) / len(aps)
fig2.suptitle(
    f"Per-class Precision-Recall (all-point AP).  "
    f"mAP@0.5 = ({aps['Cat']:.3f} + {aps['Dog']:.3f}) / 2 = {mAP:.3f}",
    fontsize=14, fontweight="bold",
)
fig2.tight_layout(rect=(0, 0, 1, 0.94))
out2 = os.path.join(img_dir, "precision_recall.png")
fig2.savefig(out2, dpi=130, bbox_inches="tight")
print(f"wrote {out2}")
print(f"AP_cat={aps['Cat']:.4f}  AP_dog={aps['Dog']:.4f}  mAP@0.5={mAP:.4f}")
