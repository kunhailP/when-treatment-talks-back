"""Human double-coding agreement for the strategy taxonomy.

Referenced by analysis/human_coding/CODING_INSTRUCTIONS.md. Reads the coded
sample and reports agreement between the two human coders, and between each
human and the LLM judge whose labels the paper uses.

The point of the exercise is not to confirm the judge. Appendix E of the
paper reports that two judges agree at kappa = 0.13 and essentially not at
all outside the modal category, and that the modal category is close to
tautological with the generation prompt. Human coding can distinguish two
explanations for that: the taxonomy is unreliable for anyone, or it is
reliable for humans and the judge is the weak instrument. Those imply
different fixes, which is why this is worth running.

Read the caveat in CODING_INSTRUCTIONS.md before interpreting the output:
coders are asked to apply the taxonomy as written rather than to improve it,
so a high human-human kappa establishes that the taxonomy is applicable, not
that it is valid. If the modal category is tautological with the prompt,
humans will reproduce that too.

Usage: python 14_human_agreement.py [--data ../human_coding/coding_sample_200.csv]
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd

C1, C2, JUDGE = "label_coder1", "label_coder2", "label_judge"


def kappa(a, b):
    """Cohen's kappa over the union of observed categories."""
    cats = sorted(set(a) | set(b))
    idx = {c: i for i, c in enumerate(cats)}
    m = np.zeros((len(cats), len(cats)))
    for x, y in zip(a, b):
        m[idx[x], idx[y]] += 1
    n = m.sum()
    po = np.trace(m) / n
    pe = (m.sum(0) / n * (m.sum(1) / n)).sum()
    return po, pe, (po - pe) / (1 - pe) if pe < 1 else float("nan")


def report(name, a, b):
    po, pe, k = kappa(a, b)
    # bootstrap interval over items
    rng = np.random.default_rng(7)
    a, b = np.asarray(a), np.asarray(b)
    ks = []
    for _ in range(2000):
        i = rng.integers(0, len(a), len(a))
        try:
            ks.append(kappa(a[i], b[i])[2])
        except Exception:
            pass
    lo, hi = np.nanpercentile(ks, [2.5, 97.5])
    print(f"  {name:<26} n={len(a):>4}  agree={po:.3f}  kappa={k:+.3f}  "
          f"95% CI [{lo:+.3f}, {hi:+.3f}]")
    return k


def main(path):
    df = pd.read_csv(path)
    for col in (C1, C2):
        if col not in df.columns:
            sys.exit(f"missing column {col} in {path}")

    coded = df.dropna(subset=[C1, C2])
    if len(coded) == 0:
        print(f"No coded rows in {path}.")
        print(f"  {len(df)} rows are prepared and both coder columns are empty.")
        print("  Human double-coding has not been carried out. The paper reports")
        print("  the judge-only figures and says so; nothing here is blocked on")
        print("  this script.")
        return

    print(f"{len(coded)} of {len(df)} rows coded by both coders\n")
    print("Agreement")
    k_hh = report("coder1 vs coder2", coded[C1], coded[C2])

    if JUDGE in coded.columns:
        report("coder1 vs judge", coded[C1], coded[JUDGE])
        report("coder2 vs judge", coded[C2], coded[JUDGE])

    modal = coded[C1].value_counts(normalize=True)
    print(f"\nModal category (coder1): {modal.index[0]} at {modal.iloc[0]:.1%}")
    both_modal = (coded[C1] == modal.index[0]) & (coded[C2] == modal.index[0])
    if (~both_modal).sum() > 10:
        print("\nExcluding items both coders assigned to the modal category")
        report("coder1 vs coder2", coded.loc[~both_modal, C1],
               coded.loc[~both_modal, C2])
        print("  (this is the comparison on which the two LLM judges collapse)")

    print()
    if k_hh >= 0.6:
        print(f"kappa = {k_hh:.3f} clears the 0.6 threshold the paper commits to.")
        print("That establishes the taxonomy is applicable, not that it is valid:")
        print("the modal-category tautology is a separate objection and is not")
        print("addressed by agreement.")
    else:
        print(f"kappa = {k_hh:.3f} is below the 0.6 threshold the paper commits to.")
        print("The taxonomy needs revision before the entropy figures can carry")
        print("weight; report this outcome rather than the threshold.")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=os.path.join(
        here, "..", "human_coding", "coding_sample_200.csv"))
    main(ap.parse_args().data)
