#!/usr/bin/env bash
# Pre-commit validation.  Run before tagging or archiving:  bash scripts/validate_repo.sh
#
# What this checks, and what it deliberately does not.  Steps 1-5 establish
# that the code runs and that the committed Study 0-a summary matches the real
# data.  Step 6 checks that numbers printed in the manuscript still match the
# result files they came from, which is the failure mode this project has hit
# most often: an analysis is rerun, the CSV changes, and the prose does not.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== [1/6] compile check =="
python -m py_compile simulation/src/*.py analysis/src/*.py analysis/tests/make_fixture.py

echo "== [2/6] unit tests =="
python -m pytest tests/ -q

echo "== [3/6] fixture regeneration =="
( cd analysis/tests && python make_fixture.py )

echo "== [4/6] Study 0-a strict direction check (fixture) =="
( cd analysis/src && python 02_reproduce.py --data ../tests/fixture_debates.csv --strict )
# The fixture run overwrites results/reproduce_summary.csv; restore from real
# data when it is present.
if [ -f analysis/data/raw/debategpt.csv ]; then
  echo "== [4b] restore real-data summary =="
  ( cd analysis/src && python 02_reproduce.py --data ../data/raw/debategpt.csv --strict )
fi

echo "== [5/6] temperature collapse smoke run (temp dir; results/ preserved) =="
TMP=$(mktemp -d)
mkdir -p "$TMP/src"
cp simulation/src/temperature_collapse.py "$TMP/src/"
( cd "$TMP/src" && python temperature_collapse.py --nsims 5 --n 500 )
rm -rf "$TMP"

echo "== [6/6] manuscript numbers vs result files =="
python - <<'PY'
import re, sys
import pandas as pd

tex = open("paper/tex/main.tex").read()
fails = []

def check(label, cond, detail):
    print(f"   {'ok  ' if cond else 'FAIL'}  {label}")
    if not cond:
        fails.append(f"{label}: {detail}")

# Study 0-a: cluster-robust and ordinal odds ratios
inf = pd.read_csv("analysis/results/study0a_inference.csv")
ai = inf[inf.arm == "Human-AI, personalized"].iloc[0]
check("0-a cluster-robust OR in text",
      f"{ai.OR:.2f}" in tex, f"file says {ai.OR:.2f}")
check("0-a CI in text",
      f"{ai.ci_lo:.2f}" in tex and f"{ai.ci_hi:.2f}" in tex,
      f"file says [{ai.ci_lo:.2f}, {ai.ci_hi:.2f}]")

# Study 0-b: modal strategy shares
mc = pd.read_csv("analysis/results/model_comparison.csv")
lo, hi = mc.modal_share.min() * 100, mc.modal_share.max() * 100
check("0-b modal share range in text",
      f"{lo:.1f}--{hi:.1f}" in tex, f"file says {lo:.1f}--{hi:.1f}")

# Study 0-c: eta^2 range and total n
fa = open("analysis/results/fidelity_audit_summary.txt").read()
ns = [int(x) for x in re.findall(r"'n': (\d+)", fa)]
check("0-c total n in text",
      f"{sum(ns):,}".replace(",", "{,}") in tex, f"file says {sum(ns)}")

# No retracted phrasing survives
for phrase in ["exact boundary", "escapes the rate", "tracks the exact"]:
    check(f"retracted phrase absent: '{phrase}'", phrase not in tex, "present")

# Figures shipped with the manuscript must match the generated ones.
# paper/tex/figs/ is a copy (LaTeX and arXiv need figures beside the source),
# and it has silently gone stale before.
import hashlib, os
def md5(f): return hashlib.md5(open(f, "rb").read()).hexdigest()
for fig in sorted(os.listdir("paper/tex/figs")):
    src = os.path.join("simulation/results", fig)
    check(f"figure in sync: {fig}",
          os.path.exists(src) and md5(src) == md5(os.path.join("paper/tex/figs", fig)),
          "differs from simulation/results/ or has no generated source")

# No placeholders or TODO strings
bib = open("paper/references.bib").read()
check("bib has no TODO", "TODO" not in bib, "present")
check("author filled in", "[Author]" not in tex,
      "\\author{[Author]} is still a placeholder")

if fails:
    print("\n   " + str(len(fails)) + " check(s) failed:")
    for f in fails:
        print("     - " + f)
    sys.exit(1)
PY

echo "== validate_repo: ALL PASS =="
