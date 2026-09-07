# Results — reproducible on public data

All numbers below are produced by the scripts in this directory on public
third-party datasets. No proprietary data or calibration is involved.

---

## 1. Group membership — interaction structure beyond geometry

**Dataset:** ATR/DIAMOR (Osaka pedestrian data with human-annotated groups)
**Script:** `diamor_group_prediction.py`
**Claim:** the interaction construct (proximity **and** directional alignment)
predicts real group membership beyond a proximity/motion baseline.

| Dataset | Pairs | AUC (proximity) | AUC (BEHAVE) | Facing increment | z | p |
|---|---|---|---|---|---|---|
| DIAMOR-1 | 1271 | 0.896 | **0.933** | +0.037 | +9.4 | <0.0002 |
| DIAMOR-2 | 677 | 0.777 | **0.837** | +0.060 | +17.0 | <0.0002 |

The facing increment is robust and *grows* with sample size — evidence it is
real structure, not a small-sample artefact. Two separate recording days.

Time-series synchrony (DIAMOR-1, dynamics not means): direction-of-motion
synchronized within pairs (+0.270 vs +0.023, p = 0.0002); body-facing
(+0.201 vs −0.129, p = 0.0001); 72% side-by-side / 28% front-to-back
formation.

## 2. Future reconfiguration — present state predicts near future

**Dataset:** MADRAS (Lyon Fête des Lumières, synchronized multi-camera crowd)
**Claim:** the human-system state read from the present carries information
about how the crowd physically reconfigures 1–2s later, measured on an
independent camera.

Positive uplift over strong kinematic/geometric baselines in **all four**
synchronized camera directions at +1s and +2s. Where a stronger baseline
(dispersion + directional coherence) already captures the effect, the
topology-specific gain becomes small — retained as an honest boundary.

## 3. Same present, different future — matched-state test

**Dataset:** Jülich Pedestrian Dynamics bottleneck experiments
**Script:** `julich_matched_state.py`
**Claim:** states identical on density/speed/flow diverge later, and a
structural read separates them ~3s ahead.

| Horizon | Divergence multiple (structurally-different vs matched) |
|---|---|
| 5 s | up to **1.44×** |
| 10 s | 1.28× |
| 20 s | 1.11× |

Matched on occupancy, density, speed, dispersion, directional coherence,
throughput, queue geometry. Structural read separates robust from fragile:
p < 0.001, permutation control z = +7.0. Reproduced on a real crowd (Lyon)
in the transitional regime — see `../docs/observability.md`.

---

## Reproduction

```bash
# DIAMOR (download person_DIAMOR-1_all.csv and groups_DIAMOR-1.dat from ATR)
python diamor_group_prediction.py person_DIAMOR-1_all.csv groups_DIAMOR-1.dat

# Jülich (download bottleneck trajectory .txt files from ped.fz-juelich.de)
python julich_matched_state.py "bottleneck/*.txt"
```

Datasets are not redistributed here; download from the original providers
(links in `../README.md`). Scripts use only the public trajectory columns.
