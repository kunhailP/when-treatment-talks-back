"""Study 0-a with inferential structure.

02_reproduce.py checks the *direction* of the Salvi et al. result on the
public DebateGPT release: it binarizes the pre/post shift at delta > 0,
compares crude odds against the Human-Human arm, and asserts an ordering.
That is a reproduction check, not an estimate, and it has two defects that
matter if any number from it appears in the paper.

1. Clustering. The 750 released rows come from 600 debates. The
   Human-Human arms contribute two rows per debate (both participants), so
   300 of the rows are paired. Treating them as independent understates the
   standard error on every contrast involving those arms.

2. Discarding the outcome. delta ranges over -4..+4 and 371 of 750 rows
   (49.5%) are exactly zero. Binarizing at delta > 0 throws away both the
   ties and the magnitudes.

This script reports the same contrasts with cluster-robust inference and,
separately, on the ordinal scale, so the paper can cite an estimate with an
interval rather than a point.

Usage: python 13_inference.py [--data ../data/raw/debategpt.csv] [--out ...]
"""
import argparse
import os

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.miscmodels.ordinal_model import OrderedModel

ARMS = ["Human-Human", "Human-Human, personalized", "Human-AI", "Human-AI, personalized"]
BASE = "Human-Human"


def load(path):
    df = pd.read_csv(path).copy()
    df["delta"] = df.sideAgreementPostTreatment - df.sideAgreementPreTreatment
    df["increased"] = (df.delta > 0).astype(int)
    return df[df.treatmentType.isin(ARMS)]


def binary_contrasts(df):
    """Logistic regression on 1{delta > 0}, SEs clustered on debateID."""
    X = pd.get_dummies(df.treatmentType, drop_first=False)[
        [a for a in ARMS if a != BASE]
    ].astype(float)
    X = sm.add_constant(X, has_constant="add")
    # GEE with an independence working correlation gives the sandwich
    # (cluster-robust) covariance, which is what the paired arms require.
    fit = sm.GEE(df.increased.values, X.values, groups=df.debateID.values,
                 family=sm.families.Binomial(),
                 cov_struct=sm.cov_struct.Independence()).fit()
    names = ["const"] + [a for a in ARMS if a != BASE]
    out = []
    for i, nm in enumerate(names):
        if nm == "const":
            continue
        b, se = fit.params[i], fit.bse[i]
        out.append({
            "arm": nm,
            "n": int((df.treatmentType == nm).sum()),
            "clusters": int(df.loc[df.treatmentType == nm, "debateID"].nunique()),
            "OR": np.exp(b),
            "ci_lo": np.exp(b - 1.96 * se),
            "ci_hi": np.exp(b + 1.96 * se),
            "p": fit.pvalues[i],
        })
    return pd.DataFrame(out)


def ordinal_contrasts(df):
    """Proportional-odds model on the full -4..+4 shift.

    Uses all 750 rows including the 49.5% ties. Reported without cluster
    adjustment -- statsmodels' ordinal model has no cluster-robust
    covariance -- so the interval is optimistic for the paired arms and we
    say so rather than quietly using it.
    """
    X = pd.get_dummies(df.treatmentType, drop_first=False)[
        [a for a in ARMS if a != BASE]
    ].astype(float)
    fit = OrderedModel(df.delta.values, X.values, distr="logit").fit(
        method="bfgs", disp=0
    )
    out = []
    for i, nm in enumerate([a for a in ARMS if a != BASE]):
        b, se = fit.params[i], fit.bse[i]
        out.append({
            "arm": nm, "OR": np.exp(b),
            "ci_lo": np.exp(b - 1.96 * se), "ci_hi": np.exp(b + 1.96 * se),
            "p": fit.pvalues[i],
        })
    return pd.DataFrame(out)


def main(path, out):
    df = load(path)
    print(f"n = {len(df)} rows, {df.debateID.nunique()} debates, "
          f"{(df.delta == 0).mean():.1%} ties\n")

    b = binary_contrasts(df)
    print("Binary outcome 1{delta > 0}, cluster-robust on debateID")
    print("  (reference arm: Human-Human)")
    for r in b.itertuples():
        print(f"  {r.arm:<28} n={r.n:>3} k={r.clusters:>3}  "
              f"OR={r.OR:5.3f}  95% CI [{r.ci_lo:5.3f}, {r.ci_hi:5.3f}]  p={r.p:.4f}")

    o = ordinal_contrasts(df)
    print("\nOrdinal outcome (proportional odds, all -4..+4; no cluster adjustment)")
    for r in o.itertuples():
        print(f"  {r.arm:<28}          "
              f"OR={r.OR:5.3f}  95% CI [{r.ci_lo:5.3f}, {r.ci_hi:5.3f}]  p={r.p:.4f}")

    if out:
        b.assign(model="binary_cluster_robust").to_csv(out, index=False)
        o.assign(model="ordinal_unadjusted").to_csv(
            out.replace(".csv", "_ordinal.csv"), index=False)
        print(f"\nwrote {out}")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=os.path.join(here, "..", "data", "raw", "debategpt.csv"))
    ap.add_argument("--out", default=os.path.join(here, "..", "results", "study0a_inference.csv"))
    a = ap.parse_args()
    main(a.data, a.out)
