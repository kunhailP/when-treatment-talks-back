#!/usr/bin/env bash
# Fetch the full upstream replication packages.
#
# This repository vendors only the files its own pipeline reads:
#   scaling-conversational-AI/data_and_analysis_code/study_{1,2,3}/output/data_prepared.rds
#   raw/debategpt.csv
# The rest of each upstream release (R analysis code, figures, fact-checker
# assessments, supplementary materials) is not redistributed here. Run this to
# obtain it if you want to reproduce the original papers rather than our use
# of them.
set -euo pipefail
cd "$(dirname "$0")"

echo "== Hackenburg et al. (2025), Science 390(6777):eaea3884 =="
echo "   https://github.com/kobihackenburg/scaling-conversational-AI"
if [ -d scaling-conversational-AI/.git ]; then
  echo "   already a clone; pulling"; ( cd scaling-conversational-AI && git pull --ff-only )
else
  echo "   cloning into scaling-conversational-AI_upstream/"
  git clone --depth 1 https://github.com/kobihackenburg/scaling-conversational-AI \
    scaling-conversational-AI_upstream
fi

echo
echo "== Salvi et al. (2025), Nature Human Behaviour 9(8):1645-1653 =="
echo "   raw/debategpt.csv is vendored; see analysis/src/01_download.py for the"
echo "   original download path (Hugging Face; blocked on some networks)."
