# 수식 LaTeX 원본 (PNG 재렌더·PPT 수식 편집기용)

각 항목의 코드를 PowerPoint 수식 편집기(LaTeX 모드) 또는 build_eqs.py에 붙여 쓰면 됩니다.

**eq_S7_prop1A** — Prop 1A 반례쌍
```latex
P(H,A,Y) = P(H)\,\pi^{\mathrm{dep}}(A\mid H)\,\mathcal{N}\!\bigl(Y;\,\mu_A(H),1\bigr),
\qquad \pi^{\mathrm{dep}}(1\mid h_1)=0
\;\Longrightarrow\; \beta^{(2)}-\beta^{(1)} = q\,(c_2-c_1)\neq 0
```

**eq_S8_resultA** — Result A 하한 (본편 낭독 수식)
```latex
V_\tau \ge \underline{\sigma}^2 \cdot P(\mathcal{H}_\delta)\cdot e^{\,\delta/\tau}
```

**eq_S9_AT** — Proposition A-T 다턴 복리
```latex
V_{\mathrm{eff}} \ge \underline{\sigma}^2\cdot P_1(\mathcal{H}_\delta)\cdot
p_\delta^{\,T-1}\left[\frac{e^{\,\delta/\tau}}{K^2}\right]^{T}
\quad\text{(compounds iff } \tau < \delta/\log(K^2/p_\delta)\text{)}
```

**eq_S11_overlap** — overlap 가중치와 경계 estimand
```latex
\omega_\tau(H) = p_\tau(H)\{1-p_\tau(H)\},\qquad
\beta^{\mathrm{ov}}_\tau=\frac{\mathbb{E}[\omega_\tau(H)\{Y(1)-Y(0)\}]}{\mathbb{E}[\omega_\tau(H)]}
```

**eq_S12_boundary** — 닫힌형 경계 곡선 (정성적 척도로 표기)
```latex
\log \mathbb{E}[1/p_\tau] = \log\!\bigl(1+\tau\,\sinh(1/\tau)\bigr)
```

**eq_B1_hahn** — Hahn(1998) bound + 삽입 부등식
```latex
V_\tau=\mathbb{E}\!\left[\frac{\sigma_1^2(H)}{p_\tau(H)}+\frac{\sigma_0^2(H)}{1-p_\tau(H)}
+(\beta(H)-\beta)^2\right],\qquad
\min(p_\tau,1-p_\tau)=\sigma(-|\Delta|/\tau)\le e^{-\delta/\tau}
```

**eq_B3_threshold** — 복리 임계와 K=2 환원
```latex
\tau < \frac{\delta}{\log(K^2/p_\delta)}:\quad
K=2:\ \log 4 = 1.386 < 3.71\ \checkmark \qquad
K=8:\ \log 64 = 4.159 > 3.71\ \times
```

**eq_B4_kernel** — Result B 커널 항등식
```latex
\omega_\tau(h)=\frac{1}{4\cosh^{2}(\Delta(h)/2\tau)},\quad
\int_{\mathbb{R}} K(u)\,du=1,\quad
\mathbb{E}[\omega_\tau]=\tau\,\frac{f(0)}{|\Delta'(0)|}(1+o(1))
```

**eq_aux_softmax** — softmax 정책
```latex
\pi_\tau(a\mid h)\propto\exp(u(a,h)/\tau),\qquad p_\tau(h)=\sigma(\Delta(h)/\tau)
```

**eq_aux_kish** — arm-specific Kish 유효표본
```latex
n_{\mathrm{eff}}(a)=\frac{n}{\mathbb{E}[1/\pi_\tau(a\mid H)]}
```

**eq_aux_counterexample** — 고정 τ 반례 수치
```latex
\tau=0.3,\ n=4\times10^{6}:\quad
\widehat{\mathrm{IPW}} = 1.792 \approx \mathrm{ATE}=1.798 \neq \beta^{\mathrm{ov}} = 1.356
```

표기 참고: `\underline{\sigma}`(σ̲)는 논문 표기. 학부생용으로 바꾸려면 `\sigma_{\min}`.
