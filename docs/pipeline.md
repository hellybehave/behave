# Pipeline — high level

This describes *what* each stage does and *why*, at a level sufficient to understand and reproduce the method. It does **not** publish the calibrated numerical core (weights, kernel widths, baseline distributions), which are deployment-specific and withheld.

---

## 0. Input

Overhead or elevated video of a shared space, or pre-extracted trajectories (position over time). BEHAVE works directly on public trajectory datasets (DIAMOR, MADRAS, Jülich) without the video stages, and on raw video via the perception stages below.

## 1. Perception (video → tracks)

- **Pose extraction** — per-frame 2D pose per person (off-the-shelf pose estimator).
- **Multi-object tracking** — stable identities over time via appearance + motion association.
- Output per agent: position, speed, and — where the viewpoint permits — body orientation.

This stage is standard computer vision. It is the *input device*, not the contribution.

## 2. Observability filtering

Before any state is computed, agents are filtered by whether the scene actually supports measurement (see [observability.md](observability.md)):

- **Separability** — agents must be distinguishable in projection (no identity swaps).
- **Resolution** — enough of each figure visible for the required micro-signals.

Agents failing these are excluded; the effective observation region is declared. This step is what makes results comparable across recordings.

## 3. Interaction graph

From the kinematics of the retained agents, BEHAVE builds a directed interaction structure: for each ordered pair, an influence weight combining spatial proximity and directional alignment (who is oriented toward whom). The construction is asymmetric — orientation matters, not just distance.

The interaction weights are row-normalized (a fixed attention budget per agent). This is the object on which everything downstream is defined.

**Validated independently:** on DIAMOR, this construction predicts real human-annotated group membership beyond a strong proximity/motion/facing baseline (see [`../results/`](../results/)).

## 4. Group segmentation

Persistent interaction groups vs. ungrouped people are identified from the interaction structure over time (not from instantaneous proximity). Each group is a subsystem with its own state.

## 5. State fields

Computed at three scales:

- **Whole system** — organization (focused / polycentric / fluid / fragmented / reorganizing), dynamical regime, coordination, momentum, fragility.
- **Per group** — membership, extent, persistence, coordination/alignment, local reactivity and fragility, emerging merge/split/dissolve transitions.
- **Spatial** — interaction centers, group boundaries, fragile vs. robust zones, candidate propagation corridors.

The *definitions* of these fields are in the preprint. The *calibrated numerical implementation* (baseline normalization per vertical) is withheld.

## 6. Response estimation

Given an external disturbance or a candidate machine action, BEHAVE estimates the system's response: whether the effect is absorbed or amplified, which groups may split / merge / recruit, where the response propagates, and which zone is affected next — each with a confidence value.

**Validated independently:** on MADRAS (multi-camera) present state carries information about future physical reconfiguration; on Jülich, states identical on conventional measures but different in structure diverge later (see [`../results/`](../results/)).

---

## Notes on honesty

- Where body orientation is not recoverable (tilted viewpoint), orientation-dependent fields degrade gracefully and are marked low-confidence rather than fabricated.
- Response/propagation are surfaced **where identifiable, with confidence** — not as universal predictions.
- Fields that were found to be redundant or mis-specified on real data were corrected, not hidden; see [limitations.md](limitations.md).
