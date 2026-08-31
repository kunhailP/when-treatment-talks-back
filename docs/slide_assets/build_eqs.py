#!/usr/bin/env python3
"""Render slide equations to transparent PNGs via pdflatex + pdftocairo."""
import subprocess, os, textwrap

OUT = "/home/claude/work/slide_assets"
os.makedirs(OUT, exist_ok=True)

EQS = {
    # main deck
    "eq_S7_prop1A": r"""
        P(H,A,Y) \;=\; P(H)\,\pi^{\mathrm{dep}}(A\mid H)\,\mathcal{N}\!\bigl(Y;\,\mu_A(H),1\bigr),
        \qquad \pi^{\mathrm{dep}}(1\mid h_1)=0
        \;\;\Longrightarrow\;\;
        \beta^{(2)}-\beta^{(1)} = q\,(c_2-c_1)\neq 0
    """,
    "eq_S8_resultA": r"""
        V_\tau \;\ge\; \underline{\sigma}^2 \cdot P(\mathcal{H}_\delta)\cdot e^{\,\delta/\tau}
    """,
    "eq_S9_AT": r"""
        V_{\mathrm{eff}} \;\ge\; \underline{\sigma}^2\cdot P_1(\mathcal{H}_\delta)\cdot
        p_\delta^{\,T-1}\left[\frac{e^{\,\delta/\tau}}{K^2}\right]^{T}
        \qquad\text{(compounds iff } \tau < \delta/\log(K^2/p_\delta)\text{)}
    """,
    "eq_S11_overlap": r"""
        \omega_\tau(H) = p_\tau(H)\bigl\{1-p_\tau(H)\bigr\},
        \qquad
        \beta^{\mathrm{ov}}_\tau=\frac{\mathbb{E}\bigl[\omega_\tau(H)\{Y(1)-Y(0)\}\bigr]}{\mathbb{E}[\omega_\tau(H)]}
    """,
    "eq_S12_boundary": r"""
        \log \mathbb{E}[1/p_\tau] \;=\; \log\!\bigl(1+\tau\,\sinh(1/\tau)\bigr)
    """,
    # backups
    "eq_B1_hahn": r"""
        V_\tau=\mathbb{E}\!\left[\frac{\sigma_1^2(H)}{p_\tau(H)}+\frac{\sigma_0^2(H)}{1-p_\tau(H)}
        +\bigl(\beta(H)-\beta\bigr)^2\right],
        \qquad
        \min(p_\tau,1-p_\tau)=\sigma\!\bigl(-|\Delta|/\tau\bigr)\le e^{-\delta/\tau}
    """,
    "eq_B3_threshold": r"""
        \tau < \frac{\delta}{\log(K^2/p_\delta)}:\quad
        K=2:\ \log 4 = 1.386 < 3.71\ \checkmark
        \qquad
        K=8:\ \log 64 = 4.159 > 3.71\ \times
    """,
    "eq_B4_kernel": r"""
        \omega_\tau(h)=\frac{1}{4\cosh^{2}\!\bigl(\Delta(h)/2\tau\bigr)},\quad
        \int_{\mathbb{R}} K(u)\,du=1,\quad
        \mathbb{E}[\omega_\tau]=\tau\,\frac{f(0)}{|\Delta'(0)|}\bigl(1+o(1)\bigr)
    """,
    "eq_aux_softmax": r"""
        \pi_\tau(a\mid h)\;\propto\;\exp\!\bigl(u(a,h)/\tau\bigr),
        \qquad
        p_\tau(h)=\sigma\!\bigl(\Delta(h)/\tau\bigr)
    """,
    "eq_aux_kish": r"""
        n_{\mathrm{eff}}(a)\;=\;\frac{n}{\mathbb{E}\bigl[1/\pi_\tau(a\mid H)\bigr]}
    """,
    "eq_aux_counterexample": r"""
        \tau=0.3,\ n=4\times10^{6}:\qquad
        \widehat{\mathrm{IPW}} = 1.792 \;\approx\; \mathrm{ATE}=1.798
        \;\neq\; \beta^{\mathrm{ov}} = 1.356
    """,
}

TEMPLATE = textwrap.dedent(r"""
    \documentclass[border=8pt]{standalone}
    \usepackage{amsmath,amssymb}
    \usepackage[T1]{fontenc}
    \begin{document}
    $\displaystyle %s$
    \end{document}
""")

for name, body in EQS.items():
    tex = TEMPLATE % body.strip()
    with open(f"{OUT}/{name}.tex", "w") as f:
        f.write(tex)
    r = subprocess.run(["pdflatex", "-interaction=nonstopmode", f"{name}.tex"],
                       cwd=OUT, capture_output=True, text=True)
    if not os.path.exists(f"{OUT}/{name}.pdf"):
        print(f"FAIL {name}:", r.stdout[-600:])
        continue
    subprocess.run(["pdftocairo", "-png", "-transp", "-r", "600",
                    "-singlefile", f"{name}.pdf", name], cwd=OUT, check=True)
    print("ok", name)

# cleanup aux files
for f in os.listdir(OUT):
    if f.endswith((".aux", ".log", ".pdf")):
        os.remove(os.path.join(OUT, f))
