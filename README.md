<img width="1280" height="853" alt="photo_2026-05-18 03 08 25" src="https://github.com/user-attachments/assets/e9db0f0e-b6c6-4520-8ceb-dbb677a8f755" />
# BEHAVE

# Human-system intelligence for autonomous machines operating around people.

# CORE THESIS
Robots can see where people are and predict individual trajectories. They still cannot represent how those people are organized as a system, what state that system is in, or how it will reorganize when something happens — and that missing state can change the correct operational action.

**BEHAVE reconstructs that missing layer.** From video or trajectory data — existing cameras, sensors, or tracking — it models the surrounding humans as a coupled dynamical system, not independent tracks, because the operationally relevant state lives in the interaction structure, not in any single trajectory.

# SCIENTIFIC FOUNDATION
Core Behavioral field framework: https://arxiv.org/abs/2605.12730
arXiv:2605.12730
> This repository documents the **method and pipeline at a high level**, and provides **reproducible evaluation on public research datasets**. It deliberately does **not** include calibration parameters, baseline recordings, raw proprietary video, or the full numerical core — these are withheld (see [Scope](#scope)). Everything here runs on third-party public data.
Technical co-founder holds a PhD and peer-reviewed publications (European Journal of Operational Research) in the optimization of manufacturing operations — the domain BEHAVE deploys into.

# WHAT THE SYSTEM COMPUTES

From tracked positions and orientations, BEHAVE produces a live **Human System State**:

- **Whole system** — organization, dynamical regime, coordination, momentum, fragility
- **Interaction groups** — persistent groups vs. ungrouped people, each with its own state
- **Spatial structure** — interaction centers, group boundaries, fragile zones, propagation corridors
- **Response** — given a disturbance or a candidate machine action: which groups respond, whether the effect is absorbed or amplified, where it may split, merge or propagate, and which zone is affected next

Individuals are observed; the collective is modeled.

# LIVE DEMO
<img width="1894" height="1057" alt="Screenshot 2026-05-18 at 03 42 41" src="https://github.com/user-attachments/assets/f5555331-7635-4919-aac6-ab6e7f01e671" />
Interactive Human System State over real trajectory data. 

# YOUTUBE LINK 
https://youtu.be/4YXE6GpJqHU

# Video Link
https://www.loom.com/share/a9b439289a274e3dbe378fd00dc81d72 

---

# EVIDENCE

Tested on independent public research datasets, with negative results retained alongside positive ones.

| Test | Dataset | Result |
|---|---|---|
| Group membership | ATR/DIAMOR (Osaka) | interaction structure predicts real human-annotated groups beyond geometry/motion/facing — ROC AUC 0.956 → 0.967, log-loss −8.5%, strict chronological split |
| Future reconfiguration | MADRAS (Lyon) | present human-system state predicts physical reconfiguration 1–2s later, confirmed on all four synchronized cameras |
| Same present, different future | Jülich bottleneck | states identical on density/speed/flow but different in structure diverge later — up to 1.44× at 5s |

We also retain results where a stronger conventional baseline explains the effect. The propagation-depth signal, for instance, collapsed into ordinary crowd geometry once the baseline included dispersion and directional coherence — reported as a falsification, not folded into a claim.

---
# DATA AVAILABILITY

All evaluations use public research datasets, downloadable from their original providers. We do not redistribute the data; download from source and cite the original authors as required.

**ATR / DIAMOR** — pedestrian trajectories with human-annotated groups, Osaka
https://dil.atr.jp/ISL/sets/groups/
Laser-range-finder tracking; groups labelled manually. Free for research use only; cite Zanlungo et al.

**Jülich Pedestrian Dynamics Data Archive** — bottleneck experiments
https://ped.fz-juelich.de/database (DOI: 10.34735/ped.da)
Bottleneck 2021: http://ped.fz-juelich.de/da/2021bottleneck
Head trajectories + mood-rating questionnaires; PeTrack extraction. Free to use, name the source.

**MADRAS** — Lyon Fête des Lumières crowd dataset
https://zenodo.org/records/13830435 (DOI: 10.5281/zenodo.13830435)
Dense real-crowd trajectories, synchronized cameras. Open, cite the MADRAS project.

Reproduction scripts for the DIAMOR and Jülich tests are in [`results/`](results/); they use only the public trajectory columns.

---

# SCOPE

**Open:** method, high-level pipeline, observability conditions, and reproducible evaluation on public datasets.

**Withheld:** per-vertical calibration parameters, baseline recordings, raw proprietary video (recordings of people not consented for publication), and the full numerical core. The *method* is public; the *calibration and data* accumulated for a specific environment are not part of it.

---

# STATUS

Turning the research prototype into an operational product for Physical AI: video, sensor or trajectory feeds → BEHAVE Human System State → operational objects → decision loop.

---

*BEHAVE Dynamics — the human-system state layer for Physical AI.*
