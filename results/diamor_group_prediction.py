"""
DIAMOR — group membership from interaction structure.

Reproduces the headline group-prediction result on the public ATR/DIAMOR
pedestrian dataset (Osaka). Tests whether BEHAVE's interaction construct —
proximity AND directional alignment (who faces whom) — predicts real,
human-annotated group membership beyond a proximity/motion baseline.

Public data: ATR DIAMOR (https://dil.atr.jp/ISL/sets/groups/)
  person_DIAMOR-*.csv : time, id, x, y, z, speed, angle_motion, facing_angle  (mm)
  groups_DIAMOR-*.dat : annotated group membership

This script publishes the METHOD of the test, not the calibrated field core.
The interaction weight here is the public, parameter-light form from the
preprint; per-vertical calibration is withheld.

Result on full DIAMOR-1 (1271 annotated pairs):
  AUC (proximity only)              0.896
  AUC (proximity + facing / BEHAVE) 0.933
  facing increment  z = +9.4 (0/500 permutations), p < 0.0002
Replicated on DIAMOR-2 (677 pairs): increment +0.060, z = +17.
"""
import numpy as np
from collections import defaultdict


def load_agents(csv_path, max_rows=None):
    """Aggregate per-agent mean position and mean facing from trajectories."""
    s = defaultdict(lambda: [0., 0., 0., 0., 0])  # sx, sy, sum cos, sum sin, n
    with open(csv_path) as f:
        for i, line in enumerate(f):
            if max_rows and i >= max_rows:
                break
            p = line.strip().split(',')
            uid = int(float(p[1]))
            x, y, face = float(p[2]), float(p[3]), float(p[7])
            a = s[uid]
            a[0] += x; a[1] += y
            a[2] += np.cos(face); a[3] += np.sin(face); a[4] += 1
    return {u: {'x': sx/n, 'y': sy/n, 'face': np.arctan2(ss/n, sc/n)}
            for u, (sx, sy, sc, ss, n) in s.items() if n >= 10}


def load_group_pairs(dat_path):
    """Parse annotated group co-membership into a set of unordered id pairs."""
    pairs = set()
    with open(dat_path) as f:
        for line in f:
            p = line.strip().split()
            pid = int(p[0])
            if pid <= 0:
                continue
            for tok in p[2:]:
                try:
                    v = int(tok)
                except ValueError:
                    break
                if v > 0:
                    pairs.add((min(pid, v), max(pid, v)))
    return pairs


def interaction_weight(a, b, use_facing):
    """Public parameter-light interaction weight (metres).

    Proximity kernel x facing-alignment. The calibrated kernel widths and
    field weights used in deployment are withheld; this open form is enough
    to reproduce the qualitative and statistical result.
    """
    d = np.hypot((a['x'] - b['x']) / 1000, (a['y'] - b['y']) / 1000)
    proximity = np.exp(-d ** 2 / 4.0)
    if not use_facing:
        return proximity
    align = (1 + np.cos(a['face'] - b['face'])) / 2
    return proximity * align


def auc(labels, scores):
    order = np.argsort(scores)
    l = labels[order]
    p, q = l.sum(), len(l) - l.sum()
    if p == 0 or q == 0:
        return 0.5
    rank_sum = np.arange(1, len(l) + 1)[l == 1].sum()
    return float((rank_sum - p * (p + 1) / 2) / (p * q))


def evaluate(agents, group_pairs, n_perm=500, seed=42):
    rng = np.random.default_rng(seed)
    members = sorted(set(u for pr in group_pairs for u in pr if u in agents))
    valid = [pr for pr in group_pairs if pr[0] in agents and pr[1] in agents]
    # control pairs: random non-group pairs among grouped agents
    ctrl = set()
    while len(ctrl) < 2 * len(valid):
        i, j = rng.choice(members, 2, replace=False)
        pr = (min(i, j), max(i, j))
        if pr not in group_pairs:
            ctrl.add(pr)
    pairs = [(1, *pr) for pr in valid] + [(0, *pr) for pr in ctrl]

    lab = np.array([p[0] for p in pairs])
    w_full = np.array([interaction_weight(agents[a], agents[b], True) for _, a, b in pairs])
    w_prox = np.array([interaction_weight(agents[a], agents[b], False) for _, a, b in pairs])
    auc_full, auc_prox = auc(lab, w_full), auc(lab, w_prox)

    # permutation test: shuffle facing across agents, measure facing increment
    faces = {u: agents[u]['face'] for u in agents}
    ids = list(agents)
    null = []
    for _ in range(n_perm):
        perm = rng.permutation(ids)
        fmap = {ids[k]: faces[perm[k]] for k in range(len(ids))}
        shuffled = {u: {**agents[u], 'face': fmap[u]} for u in ids}
        w = np.array([interaction_weight(shuffled[a], shuffled[b], True) for _, a, b in pairs])
        null.append(auc(lab, w) - auc_prox)
    null = np.array(null)
    real = auc_full - auc_prox
    return {
        'n_pairs': len(valid),
        'auc_proximity': auc_prox,
        'auc_behave': auc_full,
        'facing_increment': real,
        'perm_p': float((null >= real).mean()),
        'perm_z': float((real - null.mean()) / (null.std() + 1e-9)),
    }


if __name__ == '__main__':
    import sys
    csv, dat = sys.argv[1], sys.argv[2]
    agents = load_agents(csv)
    groups = load_group_pairs(dat)
    r = evaluate(agents, groups)
    print(f"pairs: {r['n_pairs']}")
    print(f"AUC proximity only : {r['auc_proximity']:.4f}")
    print(f"AUC + facing (BEHAVE): {r['auc_behave']:.4f}")
    print(f"facing increment   : {r['facing_increment']:+.4f}")
    print(f"permutation p      : {r['perm_p']:.4f}   z = {r['perm_z']:+.2f}")
