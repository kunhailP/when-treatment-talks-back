"""스키마 호환 합성 fixture 생성 — 데이터 없이 02/06 스크립트 무결성 테스트용."""
import numpy as np, pandas as pd, os
rng = np.random.default_rng(3)
n = 400
t = rng.choice(["Human-Human", "Human-Human, personalized", "Human-AI", "Human-AI, personalized"], n)
pre = rng.integers(1, 6, n)
boost = np.where(t == "Human-AI, personalized", 0.9, np.where(t == "Human-AI", 0.3, 0.0))  # 방향 검정이 확실히 성립하도록 상향 (2026-07-29)
post = np.clip(pre + rng.normal(boost, 1.0, n).round().astype(int), 1, 5)
df = pd.DataFrame({
    "debateID": np.arange(n) // 2, "side": np.tile(["PRO", "CON"], n // 2),
    "treatmentType": t, "sideAgreementPreTreatment": pre, "sideAgreementPostTreatment": post,
    "agreementPreTreatment": pre, "agreementPostTreatment": post,
    "topic": rng.choice(["Universal basic income", "Nuclear energy", "School uniforms"], n),
    "argument": ["Lorem ipsum argument text " + str(i) for i in range(n)],
    "argumentOpponent": ["Opponent argument text " + str(i) for i in range(n)],
})
out = os.path.join(os.path.dirname(__file__), "fixture_debates.csv")
df.to_csv(out, index=False); print("wrote", out, len(df))
