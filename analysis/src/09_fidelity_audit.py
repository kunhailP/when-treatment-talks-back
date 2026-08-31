"""
Study 0-c: Hackenburg fidelity audit — "무작위화된 것은 지시였지 행동이 아니다".

**인식론적 지위: descriptive / motivating** (Study 0 공통 규율). 공개 데이터에는
대화 transcript가 없으므로, 원 저자들이 제공한 실현-행동 측정치로 감사한다:
  - convo_n_facts_total: GPT-4 fact 추출 수 (원 논문 검증 r=.87 — 실현 dose proxy)
  - study 1/3: grammar/ontopic/valence_complied, compliance (지시 준수 flag)
발화 수준 form audit(예: 단언/질문 구현 여부)은 transcript 필요 — PA 트랙.

감사 논리 (framework §4 fidelity 규약의 관측 대응물):
  1. between: 배정 수사전략(prompt_rhetoric_id)이 실현 fact dose를 크게 바꾼다
     → 전략 지시는 dose와 bundling — 관측 로그에서 "전략 효과"는 dose 효과와 얽힘
  2. within: 같은 배정 안에서 실현 dose 분산이 거대 (assignment가 설명하는
     분산 비율 = R² 산출) → 지시는 실현 행동의 작은 부분만 고정한다
  3. zero-dose rate: 설득 배정인데 fact 0개 실현 — 극단 비순응의 하한
  4. compliance flags (study 1/3): 지시 준수율의 배정별 이질성

Usage: python 09_fidelity_audit.py
Output: results/fidelity_audit.csv, fidelity_audit_summary.txt
"""

import os

import numpy as np
import pandas as pd
import pyreadr

BASE = os.path.join(os.path.dirname(__file__), "..", "data",
                    "scaling-conversational-AI", "data_and_analysis_code")
PLACEBO = {"cats", "dogs", "homework", "officework", "iphone", "android",
           "digitalbook", "physicalbook"}


def load(study):
    path = os.path.join(BASE, f"study_{study}", "output", "data_prepared.rds")
    df = pyreadr.read_r(path)[None]
    # study 1은 d1./d2. 접두 (d1 = 첫 대화) — d1만 사용
    if f"d1.prompt_rhetoric_id" in df.columns:
        cols = {c: c[3:] for c in df.columns if c.startswith("d1.")}
        df = df.rename(columns=cols)
    return df


def audit(df, study):
    need = {"prompt_rhetoric_id", "convo_n_facts_total"}
    if not need <= set(df.columns):
        return None, None
    d = df.dropna(subset=["prompt_rhetoric_id", "convo_n_facts_total"]).copy()
    d = d[~d.prompt_rhetoric_id.isin(PLACEBO)]  # 설득 조건만
    g = d.groupby("prompt_rhetoric_id")["convo_n_facts_total"]
    tab = g.agg(n="count", mean_facts="mean", sd_facts="std",
                zero_rate=lambda s: (s == 0).mean()).round(3)
    tab["study"] = study
    # 분산분해: 배정이 설명하는 실현 dose 분산 비율 (eta^2)
    grand = d.convo_n_facts_total.mean()
    ss_between = (g.mean().sub(grand).pow(2) * g.count()).sum()
    ss_total = d.convo_n_facts_total.sub(grand).pow(2).sum()
    eta2 = float(ss_between / ss_total)
    extra = {"study": study, "n": len(d), "eta2_assignment": round(eta2, 4),
             "overall_zero_rate": round(float((d.convo_n_facts_total == 0).mean()), 3)}
    for c in ("compliance", "grammar_complied", "ontopic_complied", "valence_complied"):
        if c in d.columns:
            extra[c + "_rate"] = round(float(pd.to_numeric(d[c], errors="coerce").mean()), 3)
    return tab.reset_index(), extra


def main():
    tabs, extras = [], []
    for s in (1, 2, 3):
        try:
            tab, extra = audit(load(s), s)
        except Exception as e:
            print(f"study {s}: skip ({e})")
            continue
        if tab is not None:
            tabs.append(tab)
            extras.append(extra)

    tab = pd.concat(tabs, ignore_index=True)
    outdir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(outdir, exist_ok=True)
    tab.to_csv(os.path.join(outdir, "fidelity_audit.csv"), index=False)

    lines = ["Study 0-c fidelity audit (descriptive/motivating; transcript 없는 공개본 기준)",
             ""]
    for e in extras:
        lines.append(str(e))
    lines += ["", "배정별 실현 fact dose (설득 조건만, placebo 제외):",
              tab.to_string(index=False)]
    txt = "\n".join(lines)
    print(txt)
    with open(os.path.join(outdir, "fidelity_audit_summary.txt"), "w") as f:
        f.write(txt + "\n")
    print("\nsaved results/fidelity_audit.csv, fidelity_audit_summary.txt")


if __name__ == "__main__":
    main()
