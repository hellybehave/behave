# Limitations and retained negative results

We keep the results that survived and the ones that didn't. This section exists because a method you can only see the wins of is not one you can trust.

---

## Negative results (retained)

- **Forward spike prediction** did not survive permutation testing on calm data (AUC ≈ chance at ≥10s horizon). Predicting *that a specific event will happen* is not claimed on data without genuine transitions.
- **Spatial propagation by zones** was not significant on calm data (zone cross-correlation, p ≈ 0.17) — lag structure consistent with lag-selection on uncorrelated series.
- **Propagation depth on rich-geometry data** collapsed into ordinary crowd geometry: once the baseline includes dispersion + directional coherence, the topology-specific gain became small/mixed. Reported as a falsification, not folded into a positive claim.

## Implementation defects found on real data (corrected)

These were invisible on small synthetic examples and only appeared at scale on real footage:

- **Field redundancy** — one dispersion field duplicated the tension field (r ≈ 0.996). Redefined pre-normalization / as directional dispersion.
- **Attention vs. density** — an influence field with a proximity kernel too wide measured local crowding, not directed attention. Recomputed via directional convergence.
- **Orientation on tilted views** — body orientation from pose is unreliable when the camera looks down-and-across; sign is set by camera geometry, not by the person. Orientation-dependent fields degrade gracefully and are marked low-confidence.
- **Inclusion criterion** — an absolute figure-height threshold wrongly excluded seated people; replaced by keypoint-confidence (see [observability.md](observability.md)).

## Theoretical scope

- Stability/response linearization holds near equilibrium; predictions weaken at large excursions, including at the transition itself.
- The dangerous/target set is defined per vertical, not derived from the formalism.
- Human-in-the-loop by design: the system estimates state and response; the decision and its responsibility remain with the operator.

## What is deliberately not published

Per-vertical calibration parameters, baseline recordings, raw proprietary video, and the full numerical core. The *method* is public (preprint + this repo); the *calibration and data* accumulated for a specific environment are not part of the method.
