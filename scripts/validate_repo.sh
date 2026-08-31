#!/usr/bin/env bash
# 배포 전 검증 (4차 비판 수용, 2026-07-30 신설).
# 압축·커밋 전에 반드시 통과해야 한다:  bash scripts/validate_repo.sh
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== [1/4] compile check =="
python -m py_compile simulation/src/*.py analysis/src/*.py analysis/tests/make_fixture.py

echo "== [2/4] fixture 재생성 =="
( cd analysis/tests && python make_fixture.py )

echo "== [3/4] Study 0-a strict 방향 검정 =="
( cd analysis/src && python 02_reproduce.py --data ../tests/fixture_debates.csv --strict )
# fixture 실행이 results/reproduce_summary.csv를 덮어쓰므로, 실데이터가 있으면 복원 (2026-07-30 수정)
if [ -f analysis/data/raw/debategpt.csv ]; then
  echo "== [3b] 실데이터 summary 복원 =="
  ( cd analysis/src && python 02_reproduce.py --data ../data/raw/debategpt.csv --strict )
fi

echo "== [4/4] 소형 temperature collapse (smoke — 임시 폴더에서 실행, 실제 results/ 보존) =="
TMP=$(mktemp -d)
mkdir -p "$TMP/src"
cp simulation/src/temperature_collapse.py "$TMP/src/"
( cd "$TMP/src" && python temperature_collapse.py --nsims 5 --n 500 )
rm -rf "$TMP"

echo "== validate_repo: ALL PASS =="
