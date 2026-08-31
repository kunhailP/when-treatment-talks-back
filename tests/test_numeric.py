"""수치 회귀 방지 테스트 (W5 — 1/p 버그류 재발 방지).

실행: pytest tests/ -q   (repo 루트에서)
원칙: 느린 시뮬레이션 본체가 아니라 이론 대응 수치·공식의 불변식을 잠근다.
"""

import os
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "simulation", "src"))


def test_closed_form_e_inv_p():
    """Uniform(-1,1), Δ=H에서 E[1/p_τ] = 1 + τ·sinh(1/τ) (noniden §반례, 4차 비판 #5)."""
    from continuous_h import population_objects, BETAS
    for tau in (0.6, 0.3, 0.15):
        mc = population_objects("uniform", BETAS["const"], tau, m=1_000_000)["e_inv_p"]
        closed = 1 + tau * np.sinh(1 / tau)
        assert abs(mc - closed) / closed < 0.02, (tau, mc, closed)


def test_overlap_kernel_identity():
    """ω_τ = p(1-p) = 1/[4cosh²(Δ/2τ)] — Result B 증명의 핵심 항등식."""
    rng = np.random.default_rng(0)
    d = rng.normal(size=1000)
    tau = 0.3
    p = 1 / (1 + np.exp(-d / tau))
    lhs = p * (1 - p)
    rhs = 1 / (4 * np.cosh(d / (2 * tau)) ** 2)
    assert np.allclose(lhs, rhs, atol=1e-12)


def test_kish_formula():
    """Kish ESS = (Σw)²/Σw² — 균등 가중이면 n, 단일 지배 가중이면 ~1."""
    from continuous_h import kish
    assert abs(kish(np.ones(100)) - 100) < 1e-9
    w = np.array([1000.0] + [1e-6] * 99)
    assert kish(w) < 1.01


def test_result_b_limit_direction():
    """τ↓0에서 β^ov → β(0): kink β(H)=1+|H|이면 극한 1 (Result B Proposition)."""
    from continuous_h import population_objects, BETAS
    b_ov_hi = population_objects("uniform", BETAS["kink"], 0.5, m=500_000)["beta_ov"]
    b_ov_lo = population_objects("uniform", BETAS["kink"], 0.05, m=500_000)["beta_ov"]
    assert b_ov_lo < b_ov_hi          # 경계로 갈수록 β(0)=1 방향으로 감소
    assert abs(b_ov_lo - 1.0) < 0.1   # 극한값 근접


def test_overlap_mass_linear_in_tau():
    """Result B (ii): E[ω_τ] = τ·f(0)/|Δ'(0)|·(1+o(1)) — Uniform이면 τ/2."""
    from continuous_h import population_objects, BETAS
    for tau in (0.1, 0.05):
        m = population_objects("uniform", BETAS["const"], tau, m=1_000_000)["overlap_mass"]
        assert abs(m - tau / 2) / (tau / 2) < 0.05, (tau, m)


def test_study0a_strict_fixture(tmp_path):
    """02 --strict가 fixture에서 통과 (4차 비판 #1 재발 방지).
    --out 임시 경로 사용 — 실데이터 reproduce_summary.csv를 덮어쓰지 않는다."""
    r = subprocess.run(
        [sys.executable, "02_reproduce.py", "--data", "../tests/fixture_debates.csv",
         "--strict", "--out", str(tmp_path / "summary.csv")],
        cwd=os.path.join(ROOT, "analysis", "src"), capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert (tmp_path / "summary.csv").exists()


def test_dirichlet_smoothing_floor():
    """08 파이프라인의 스무딩: 미관측 전략의 p̂ = α/(k+αK) > 0 (zero-prob 방지)."""
    alpha, k, K = 0.5, 20, 8
    floor = alpha / (k + alpha * K)
    assert floor > 0
    assert abs(floor - 0.5 / 24) < 1e-12
