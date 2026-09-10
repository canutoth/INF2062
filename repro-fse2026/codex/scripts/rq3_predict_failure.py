#!/usr/bin/env python3
"""RQ3 as a TESTED explanation: can the cheap pilot diagnostics predict when the
count proxy fails? Fit a logistic regression and a depth-2 decision tree
(5-fold stratified CV, ROC-AUC) on per-context diagnostics
  - p90/p10 (cost spread)
  - per-strategy Ratio spread (strategy_bias)
  - target-cost asymmetry (target_cost_decorr)
predicting several failure outcomes (Pareto-set divergence, KW top-group change,
material recommendation change). Honest about base-rate saturation.

Reuses artifacts/audit_validation.csv (diagnostics + KW/material outcomes) and the
per-scenario Pareto CSVs. Run with .venv-linux/bin/python.
"""
import csv, os
from collections import defaultdict
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import roc_auc_score

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def A(p): return os.path.join(REPO, p)

# ---- 1. diagnostics + KW/material outcomes (per context) ----
diag = list(csv.DictReader(open(A("artifacts/audit_validation.csv"))))
for d in diag:
    d["key"] = d["context"].split("/")[0] if d["family"] == "energy" else d["context"]

# ---- 2. per-context Pareto divergence (aggregate p_differ / jaccard over combos) ----
PARETO = {
    "energy":   "artifacts/significance_pareto_energy.csv",
    "icse19":   "artifacts/corrected/kw_icse19_ridge_largestn_pareto.csv",
    "x264":     "artifacts/corrected/kw_x264_ridge_largestn_pareto.csv",
    "workload": "artifacts/corrected/kw_workload_ridge_largestn_pareto.csv",
    "lcbench":  "artifacts/corrected/kw_lcbench_ridge_largestn_pareto.csv",
    "linux":    "artifacts/significance_linux_hgbtfull_pareto.csv",
}
par = defaultdict(lambda: {"pd": [], "jac": []})   # (family,key) -> lists
for fam, path in PARETO.items():
    if not os.path.exists(A(path)):
        print(f"  [warn] missing {path}"); continue
    for x in csv.DictReader(open(A(path))):
        k = (fam, x["context"])
        try: par[k]["pd"].append(float(x["p_differ"]))
        except: pass
        try: par[k]["jac"].append(float(x["jaccard"]))
        except: pass

# ---- 3. assemble the modelling table ----
rows = []
for d in diag:
    k = (d["family"], d["key"])
    p = par.get(k)
    r = dict(family=d["family"], context=d["context"],
             p90p10=float(d["cost_p90p10"]), bias=float(d["strategy_bias"]),
             decorr=float(d["target_cost_decorr"]), cv=float(d["cost_cv"]),
             kw_flip=int(round(float(d["flipped"]))),
             material=int(round(float(d["stakes_any"]))))
    if p and p["pd"]:
        r["par_any"]  = int(any(v >= 0.95 for v in p["pd"]))            # ≥1 scenario diverges
        r["par_maj"]  = int(np.mean([v >= 0.95 for v in p["pd"]]) >= 0.5)  # majority diverge
        r["par_subst"] = int(np.median(p["jac"]) < 0.6) if p["jac"] else None  # substantial menu change
    rows.append(r)

print(f"contexts: {len(rows)}  (with Pareto join: {sum('par_any' in r for r in rows)})")
by = defaultdict(int)
for r in rows: by[r["family"]] += 1
print("per family:", dict(by))

FEATS = ["p90p10", "bias", "decorr"]
FEATS_CV = ["p90p10", "bias", "decorr", "cv"]

def evaluate(outcome, feats, subset=None):
    data = [r for r in rows if r.get(outcome) is not None and (subset is None or subset(r))]
    y = np.array([r[outcome] for r in data])
    X = np.array([[r[f] for f in feats] for r in data], float)
    base = y.mean()
    n = len(y)
    if len(set(y)) < 2:
        return f"{outcome:12s} n={n:3d} base={base:.2f}  [constant outcome, AUC undefined]"
    if min(base, 1 - base) * n < 5:
        note = "  (near-saturated; AUC unstable)"
    else:
        note = ""
    cv = StratifiedKFold(5, shuffle=True, random_state=0)
    lr = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    dt = DecisionTreeClassifier(max_depth=2, random_state=0, class_weight="balanced")
    auc_lr = cross_val_score(lr, X, y, cv=cv, scoring="roc_auc")
    auc_dt = cross_val_score(dt, X, y, cv=cv, scoring="roc_auc")
    # standardized LR coefficients (fit on all data, for direction/magnitude)
    lr.fit(X, y)
    coef = lr.named_steps["logisticregression"].coef_[0]
    coefs = ", ".join(f"{f}{'+' if c>=0 else ''}{c:.2f}" for f, c in zip(feats, coef))
    return (f"{outcome:12s} n={n:3d} base={base:.2f} | "
            f"LR-AUC {auc_lr.mean():.2f}±{auc_lr.std():.2f} | tree-AUC {auc_dt.mean():.2f} | "
            f"coef[{coefs}]{note}")

print("\n=== Outcome predictability (features = p90/p10, Ratio-spread bias, target-cost decorr) ===")
for oc in ["par_any", "par_maj", "par_subst", "kw_flip", "material"]:
    print("  " + evaluate(oc, FEATS))

print("\n=== + cost_cv as a 4th feature ===")
for oc in ["par_subst", "material"]:
    print("  " + evaluate(oc, FEATS_CV))

# ---- interpretable depth-2 tree for the best outcome (material change) ----
print("\n=== Depth-2 decision tree for 'material recommendation change' (the one-line model) ===")
data = [r for r in rows if r.get("material") is not None]
y = np.array([r["material"] for r in data]); X = np.array([[r[f] for f in FEATS] for r in data], float)
dt = DecisionTreeClassifier(max_depth=2, random_state=0, class_weight="balanced").fit(X, y)
print(export_text(dt, feature_names=FEATS))
print(f"full-fit AUC (optimistic): {roc_auc_score(y, dt.predict_proba(X)[:,1]):.2f}")
