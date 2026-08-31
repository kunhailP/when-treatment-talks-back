#!/usr/bin/env python3
"""Slide figures: S3 timeline, S5 (pi,G,E) loop, S11 overlap localization."""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

mpl.rcParams.update({
    "font.family": "Noto Sans CJK JP",
    "text.color": "#0b0b0b", "axes.edgecolor": "#52514e",
    "axes.labelcolor": "#0b0b0b", "xtick.color": "#52514e", "ytick.color": "#52514e",
    "figure.facecolor": "white", "axes.facecolor": "white", "svg.fonttype": "none",
})
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, MUT = "#0b0b0b", "#52514e"

# ---------------------------------------------------------------- S3 timeline
fig, ax = plt.subplots(figsize=(12, 4.2))
ax.set_xlim(2023.85, 2027.0); ax.set_ylim(-2.6, 2.9); ax.axis("off")
ax.axhline(0, color=MUT, lw=1.2, zorder=1)
for yr in [2024, 2025, 2026]:
    ax.plot([yr, yr], [-0.07, 0.07], color=MUT, lw=1.2)
    ax.text(yr, -0.38, str(yr), ha="center", va="top", fontsize=11, color=MUT)

events = [  # (x, y, color, bold-title, sub)
    (2024.30, 1.10, AQUA,  "세계 '선거의 해'",        "세계 인구 절반이 투표"),
    (2024.70, -1.30, BLUE, "Science (Costello 팀)",  "AI 대화 → 음모론 믿음 ≈20%↓,\n2개월 지속"),
    (2025.10, 1.85, AQUA,  "EU AI Act 금지 조항 적용", "조작적·기만적 AI 기법 금지\n(Article 5, 2025.2 발효)"),
    (2025.38, -1.85, BLUE, "Nature Human Behaviour (Salvi 팀)", "토론에서 GPT-4 > 인간 설득자"),
    (2025.62, 1.00, BLUE,  "Science (Hackenburg 팀)", "설득의 지렛대 대규모 분해 실험"),
    (2025.90, -0.95, BLUE, "PNAS",                    "설득 이론을 AI로 검증"),
    (2026.62, 1.55, ORANGE,"본 연구 (2026.8)",        "무엇이 어떻게 설득하는지\n분해·감사하는 방법론"),
]
for x, y, c, t, s in events:
    ax.plot([x, x], [0, y], color=c, lw=1.4, zorder=2)
    ax.plot([x], [0], "o", ms=7, color=c, zorder=3)
    va = "bottom" if y > 0 else "top"
    dy = 0.12 if y > 0 else -0.12
    w = "bold"
    ax.text(x, y + dy, t, ha="center", va=va, fontsize=10.5, color=c, weight=w)
    ax.text(x, y + dy + (0.34 if y > 0 else -0.34), s, ha="center", va=va,
            fontsize=8.8, color=MUT, linespacing=1.25)
# category key (colored text, not a legend box)
ax.text(2023.9, 2.72, "학계", color=BLUE, fontsize=10, weight="bold")
ax.text(2024.06, 2.72, "· 규제/배경", color=AQUA, fontsize=10, weight="bold")
ax.text(2024.42, 2.72, "· 본 연구", color=ORANGE, fontsize=10, weight="bold")
fig.tight_layout()
fig.savefig("fig_S3_timeline.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# ------------------------------------------------------------ S5 (pi,G,E) loop
fig, ax = plt.subplots(figsize=(10.5, 5.4))
ax.set_xlim(0, 10.5); ax.set_ylim(0, 5.65); ax.axis("off")

def box(x, y, w, h, title, sub, fc, ec):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12",
                                fc=fc, ec=ec, lw=1.6, zorder=2))
    ax.text(x + w/2, y + h*0.63, title, ha="center", va="center",
            fontsize=12.5, weight="bold", color=INK, zorder=3)
    ax.text(x + w/2, y + h*0.28, sub, ha="center", va="center",
            fontsize=9.2, color=MUT, zorder=3)

box(0.45, 2.55, 2.5, 1.35, "정책 π", "전략 선택\n(약사의 판단)", "#eaf1fb", BLUE)
box(4.00, 2.55, 2.5, 1.35, "생성기 G", "전략 → 실제 문장\n(처방전 → 약)", "#eaf1fb", BLUE)
box(7.55, 2.55, 2.5, 1.35, "사용자", "발화 $M_t$ 수신 후\n반응 $R_t$", "#fdeee7", ORANGE)
box(4.00, 0.42, 2.5, 1.10, "정보 환경 E", "잠긴 evidence bank\n(약장의 내용물)", "#e8f7f1", AQUA)

def arrow(p, q, label, dy=0.22, color=INK, rad=0.0, ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16,
                 lw=1.6, color=color, connectionstyle=f"arc3,rad={rad}",
                 linestyle=ls, zorder=1))
    mx, my = (p[0]+q[0])/2, (p[1]+q[1])/2
    if label:
        ax.text(mx, my + dy, label, ha="center", va="bottom",
                fontsize=10, color=color, weight="bold")

arrow((2.98, 3.23), (3.97, 3.23), "행동 배정 $A_t$")
arrow((6.53, 3.23), (7.52, 3.23), "발화 $M_t$")
arrow((5.25, 1.62), (5.25, 2.42), "", color=AQUA)
# feedback: user -> policy (arc over the top)
ax.add_patch(FancyArrowPatch((8.8, 4.10), (1.7, 4.10), arrowstyle="-|>",
             mutation_scale=16, lw=1.8, color=ORANGE,
             connectionstyle="arc3,rad=0.22", zorder=1))
ax.text(5.25, 4.42, "반응 $R_t$가 이력 $H_{t+1}$에 쌓여 다음 턴의 선택을 바꾼다", ha="center",
        fontsize=9.6, color=ORANGE, weight="bold")
ax.text(5.25, 5.35, "처치 = (π, G, E)의 합성 — 그리고 이 전체가 사용자 반응에 적응한다",
        ha="center", fontsize=11.5, weight="bold", color=INK)
fig.tight_layout()
fig.savefig("fig_S5_pge_loop.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------- S11 overlap localization curves
h = np.linspace(-1, 1, 4001)
taus = [1.0, 0.3, 0.1, 0.03]
ramp = ["#b7d3f0", "#6fa7e3", "#2a78d6", "#173f75"]  # single hue, light->dark
fig, ax = plt.subplots(figsize=(9, 4.8))
for t, c in zip(taus, ramp):
    w = 1.0 / (4 * np.cosh(h / (2 * t)) ** 2)
    dens = w / np.trapezoid(w, h)          # area-normalised (f uniform)
    ax.plot(h, dens, color=c, lw=2.2, zorder=3)
    peak = dens.max()
    xlab = 0.04 if t <= 0.1 else (0.42 if t == 0.3 else 0.72)
    ylab = peak * (1.02 if t <= 0.1 else 1.1)
    ax.text(xlab, min(ylab, 8.2), f"τ = {t:g}", color=c, fontsize=10.5, weight="bold")
ax.axvline(0, color=MUT, lw=1.2, ls="--", zorder=2)
ax.annotate("결정경계 {Δ(h) = 0}\n= AI가 망설이는 상황", xy=(-0.012, 8.35),
            xytext=(-0.52, 8.05), ha="center", fontsize=10, color=INK, weight="bold",
            linespacing=1.3, arrowprops=dict(arrowstyle="->", color=MUT, lw=1.3))
ax.annotate("τ ↓ (고집↑):\noverlap 질량이\n경계로 집중된다", xy=(0.055, 5.2),
            xytext=(0.5, 5.4), fontsize=10, color=INK, linespacing=1.35,
            arrowprops=dict(arrowstyle="->", color=MUT, lw=1.3))
ax.set_xlabel("이력 h  (사용자 상태; Δ(h) = 점수 격차)", fontsize=10.5)
ax.set_ylabel("정규화된 overlap 밀도", fontsize=10.5)
ax.set_xlim(-1, 1); ax.set_ylim(0, 9.0)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", color="#e8e7e3", lw=0.8, zorder=0)
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig("fig_S11_overlap_localization.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("figures done")
