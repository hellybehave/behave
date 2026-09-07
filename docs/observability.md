# Observability conditions

BEHAVE only produces valid state when the scene actually supports measurement. These conditions are checked **before** any field is computed, and they do not require event labels. They are the reason the method is comparable across recordings.

---

## C1 — Metric calibration

Distance-dependent fields are defined in scene metres, not image pixels. A planar homography maps image coordinates to scene coordinates (minimum four non-collinear known points; wide-angle lenses require undistortion first). Without this, interaction radius is physically different in different parts of the frame.

## C2 — Agent separability

Identities must be stable in projection over the analysis window. Operational criterion: median displacement of a track's reference point per sampling step must be a small fraction of the inter-agent spacing.

Measured contrast across real setups (identical pipeline, different viewpoints):

| Setup | Viewpoint | Median track step | Usable tracks |
|---|---|---|---|
| Dense audience | shoulder level | 200–330 px | 2 / 15 |
| Seated audience | elevated ~3–4 m | 0.9–5.7 px | 11 / 14 |
| Open elevated camera | elevated ~3–4 m | 1.1–14.7 px | 14 / 14 |

Two orders of magnitude difference — driven by separability, not detector quality. The elevated viewpoint is a sufficient, not necessary, condition; any viewpoint that separates agents satisfies C2.

## C3 — Effective observation region

The region where extraction meets quality thresholds. Agents are included when the keypoints required for the fields in use are reliably detected. For mixed standing/seated scenes the criterion is keypoint confidence (shoulders, arms), not absolute figure height — a height threshold calibrated on standing people wrongly excludes seated people the detector sees perfectly well.

---

## Regime of validity (empirically bounded)

The latent flow-response state (robust vs. fragile) is defined for **dense flow in a transitional regime** — a system balanced between free movement and congestion. Confirmed by testing across three regimes:

- **Free flow** (mall, ~1.2 m/s, sparse) — no congestion to break; observable not defined.
- **Saturated jam** (dense static crowd, ~0.4 m/s) — already at the floor; nothing left to break.
- **Transitional** (bottleneck; dense crowd tr.) — the observable works, ~3s ahead.

This is an honest boundary, not a limitation of the idea: early-warning signals live near the transition, not deep inside either stable regime.
