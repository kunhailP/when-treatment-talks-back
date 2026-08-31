"""
Study 0-a: Salvi et al. (NHB 2025) 핵심 결과의 방향 재현 (descriptive).

원 논문의 primary: 사후 상대편 동의(sideAgreementPostTreatment) 증가가
Human-AI personalized 조건에서 Human-Human 대비 높다 (OR ~1.8).
여기서는 정확한 계수 재현이 아니라 방향·순위 확인이 목표
(정확 재현은 원 저장소 regressionAnalysisR.ipynb 사용).

Input : --data debates(.csv) — 스키마: debateID, side, treatmentType,
        sideAgreementPreTreatment, sideAgreementPostTreatment, ...
Output: results/reproduce_summary.csv + 콘솔 표

Usage: python 02_reproduce.py --data ../data/raw/debates.csv
"""

import argparse
import os

import numpy as np
import pandas as pd

TREATMENTS = ["Human-Human", "Human-Human, personalized", "Human-AI", "Human-AI, personalized"]


def main(path, strict=False, out=None):
    df = pd.read_csv(path)
    need = {"treatmentType", "sideAgreementPreTreatment", "sideAgreementPostTreatment"}
    missing = need - set(df.columns)
    if missing:
        raise SystemExit(f"missing columns: {missing}\navailable: {list(df.columns)}")

    df = df.copy()
    df["delta"] = df.sideAgreementPostTreatment - df.sideAgreementPreTreatment
    df["increased"] = (df.delta > 0).astype(int)

    rows = []
    base = df[df.treatmentType == "Human-Human"]
    for t in TREATMENTS:
        sub = df[df.treatmentType == t]
        if len(sub) == 0:
            continue
        p1, p0 = sub.increased.mean(), base.increased.mean()
        # crude OR vs Human-Human (원 논문은 다층 ordered/logistic — 방향 확인용)
        odds = lambda p: p / (1 - p)
        rows.append({
            "treatment": t, "n": len(sub),
            "mean_delta": round(sub.delta.mean(), 3),
            "pct_increased": round(p1, 3),
            "crude_OR_vs_HH": round(odds(p1) / odds(p0), 3) if t != "Human-Human" else 1.0,
        })
    df_out = pd.DataFrame(rows)
    print(df_out.to_string(index=False))
    print("\n방향 체크: Human-AI, personalized 의 OR가 최대이고 >1 이면 원 논문과 일치.")

    if strict:
        ors = {r["treatment"]: r["crude_OR_vs_HH"] for r in rows}
        pers = ors.get("Human-AI, personalized", 0)
        assert pers > 1, f"strict: personalized AI OR {pers} <= 1"
        assert pers >= max(v for k, v in ors.items() if k != "Human-AI, personalized"), \
            f"strict: personalized AI OR가 최대가 아님: {ors}"
        print("[strict] 방향 검정 통과")

    if out is None:
        outdir = os.path.join(os.path.dirname(__file__), "..", "results")
        os.makedirs(outdir, exist_ok=True)
        out = os.path.join(outdir, "reproduce_summary.csv")
    df_out.to_csv(out, index=False)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--strict", action="store_true", help="fixture/재현 방향 assertion")
    ap.add_argument("--out", default=None,
                    help="summary 출력 경로 (기본 results/reproduce_summary.csv — 테스트는 임시 경로 사용)")
    a = ap.parse_args()
    main(a.data, strict=a.strict, out=a.out)
