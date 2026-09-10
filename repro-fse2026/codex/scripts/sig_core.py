"""Shared significance core: MEDIAN-decision bootstrap.

The paper's RQ2 decisions are medians over runs/seeds. To test whether a
reported flip is a stable finding (not a single-run fluke), each bootstrap
replicate resamples (a) the held-out evaluation configurations and (b) the runs
of each strategy-level cell, recomputes the MEDIAN MRE and MEDIAN cost per cell,
then recomputes the count-cost and measured-cost winners over ALL candidates and
checks whether the same (count-winner, measured-winner) flip recurs.

p_reproduce = fraction of replicates reproducing the flip. Robust if >= 0.95.

cells[(strategy, level)] = {
    "errs":     list of per-run error vectors aligned to the eval pool,
    "pct_cost": list of per-run measured-cost fractions,
    "pct_n":    scalar or list (sample-size fraction; count-cost axis),
}
"""
import numpy as np

LAMBDAS = [0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 10.0]


def _norm(a):
    a = np.asarray(a, float)
    r = max(a.max() - a.min(), 1e-12)
    return (a - a.min()) / r


def median_decision_flips(cells, context, B, rng, lambdas=LAMBDAS, combo=None, agg="median"):
    """agg = 'median' (default, matches the pipeline) or 'mean' (sensitivity check)."""
    aggf = np.median if agg == "median" else np.mean
    keys = sorted(cells)
    if len(keys) < 2:
        return []
    errM = {k: np.asarray(cells[k]["errs"], float) for k in keys}   # runs x pool
    costM = {k: np.asarray(cells[k]["pct_cost"], float) for k in keys}
    pn = np.array([aggf(cells[k]["pct_n"]) if np.ndim(cells[k]["pct_n"]) else cells[k]["pct_n"]
                   for k in keys], float)
    L = errM[keys[0]].shape[1]
    pool = np.arange(L)

    def decision(samp, resample_runs):
        mm, cc = [], []
        for k in keys:
            M = errM[k][:, samp].mean(axis=1)   # per-run MRE on this eval sample
            c = costM[k]
            if resample_runs and len(M) > 1:
                idx = rng.integers(0, len(M), len(M)); M = M[idx]; c = c[idx]
            mm.append(aggf(M)); cc.append(aggf(c))
        return np.array(mm), np.array(cc)

    mm0, cc0 = decision(pool, False)
    out = []
    for lam in lambdas:
        iC = int((_norm(mm0) + lam * _norm(pn)).argmin())
        iM = int((_norm(mm0) + lam * _norm(cc0)).argmin())
        if iC == iM:
            continue
        rep = 0
        for _ in range(B):
            samp = rng.choice(pool, size=pool.size, replace=True)
            mmb, ccb = decision(samp, True)
            if int((_norm(mmb) + lam * _norm(pn)).argmin()) == iC and \
               int((_norm(mmb) + lam * _norm(ccb)).argmin()) == iM:
                rep += 1
        rec = dict(system=context, lam=lam,
                   kind="budget" if keys[iC][0] == keys[iM][0] else "strategy",
                   cw=f"{keys[iC][0]}@{keys[iC][1]}", mw=f"{keys[iM][0]}@{keys[iM][1]}",
                   p_reproduce=rep / B,
                   dMRE_pct=(mm0[iC] - mm0[iM]) / mm0[iM] * 100,
                   dCost_pct=(cc0[iC] - cc0[iM]) / cc0[iM] * 100)
        if combo is not None:
            rec["combo"] = combo
        out.append(rec)
    return out


def _pareto_mask(cost, err):
    """Efficient = no other point has <= cost AND <= err (with one strictly <)."""
    cost = np.asarray(cost, float); err = np.asarray(err, float)
    n = len(cost); keep = np.ones(n, bool)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if cost[j] <= cost[i] and err[j] <= err[i] and (cost[j] < cost[i] or err[j] < err[i]):
                keep[i] = False; break
    return keep


def pareto_choiceset(cells, context, B, rng, agg="mean", combo=None):
    """Does the measured-cost Pareto-efficient choice-set differ from the count-cost one,
    and does that difference reproduce under bootstrap?  lambda-free (whole frontier).

    Returns one row: jaccard(count-frontier, measured-frontier), n_missed (measured-efficient
    combos that the count view treats as dominated), and p_differ (bootstrap fraction where the
    two frontiers differ -> robust choice-set change)."""
    aggf = np.median if agg == "median" else np.mean
    keys = sorted(cells)
    if len(keys) < 2:
        return None
    errM = {k: np.asarray(cells[k]["errs"], float) for k in keys}
    costM = {k: np.asarray(cells[k]["pct_cost"], float) for k in keys}
    pn = np.array([aggf(cells[k]["pct_n"]) if np.ndim(cells[k]["pct_n"]) else cells[k]["pct_n"] for k in keys])
    L = errM[keys[0]].shape[1]; pool = np.arange(L)

    def frontiers(samp, resample_runs):
        err, cost = [], []
        for k in keys:
            M = errM[k][:, samp].mean(axis=1); c = costM[k]
            if resample_runs and len(M) > 1:
                idx = rng.integers(0, len(M), len(M)); M = M[idx]; c = c[idx]
            err.append(aggf(M)); cost.append(aggf(c))
        err = np.array(err); cost = np.array(cost)
        return _pareto_mask(pn, err), _pareto_mask(cost, err)   # count-frontier, measured-frontier

    cnt0, meas0 = frontiers(pool, False)
    inter = int((cnt0 & meas0).sum()); union = int((cnt0 | meas0).sum())
    jacc0 = inter / union if union else 1.0
    missed0 = int((meas0 & ~cnt0).sum())     # measured-efficient but count-dominated
    differ = 0
    for _ in range(B):
        samp = rng.choice(pool, size=pool.size, replace=True)
        cnt, meas = frontiers(samp, True)
        if not np.array_equal(cnt, meas):
            differ += 1
    row = dict(context=context, n_combos=len(keys), n_count_eff=int(cnt0.sum()), n_meas_eff=int(meas0.sum()),
               jaccard=round(jacc0, 4), n_missed=missed0, p_differ=differ / B)
    if combo is not None:
        row["combo"] = combo
    return row


def flips_both(cells, context, B, rng, lambdas=LAMBDAS, combo=None):
    """Run the flip-significance for BOTH aggregations; tag each row with 'agg'.
    Note: the set of point-estimate flips can differ between mean and median
    (different aggregate winners), so the two aggs are reported as separate rows."""
    rows = []
    for agg in ("mean", "median"):
        for f in median_decision_flips(cells, context, B, rng, lambdas, combo, agg=agg):
            f["agg"] = agg
            rows.append(f)
    return rows
