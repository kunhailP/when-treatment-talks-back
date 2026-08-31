import numpy as np
rng = np.random.default_rng(20260831)

# ---------- 1. Direct TV, not via Pinsker ----------
# Under the construction, P0 and P1 differ ONLY on the (a*, H_d) cell, so the
# log-likelihood ratio for n obs is a sum over the m ~ Bin(n, c e^{-d}) rare
# observations.  TV = E|1 - exp(LLR)|/2 computed on the sufficient statistic.
def tv_direct(n, c, d, eps, s2=1.0, reps=400_000):
    p_rare = c*np.exp(-d)
    m = rng.binomial(n, p_rare, reps)                 # rare-cell count
    # under P0, Y ~ N(0,s2) on those cells; LLR = sum[(Y-0)^2-(Y-eps)^2]/(2 s2)
    #                                          = sum[2 eps Y - eps^2]/(2 s2)
    S = rng.normal(0.0, np.sqrt(s2*m.clip(1)), reps)*np.sqrt(m>0)   # sum of m N(0,s2)
    llr = (2*eps*S - m*eps**2)/(2*s2)
    return np.mean(np.abs(1-np.exp(llr)))/2

print("=== 1. TV computed directly vs Pinsker bound (Gaussian outcomes) ===")
print(f"{'n':>8}{'d':>5}{'eps*':>9}{'KL_n':>8}{'Pinsker':>10}{'TV direct':>11}{'LeCam floor':>13}")
c, s2 = 0.4, 1.0
for n in [2000, 20000]:
    for d in [4.0, 7.0]:
        eps = np.sqrt(2*s2*0.5/(n*c*np.exp(-d)))      # chosen so n*KL = 1/2
        kl_n = n*c*np.exp(-d)*eps**2/(2*s2)
        tv = tv_direct(n, c, d, eps, s2)
        Delta = c*eps                                  # rho_min = 1
        print(f"{n:>8}{d:>5.1f}{eps:>9.4f}{kl_n:>8.3f}{np.sqrt(kl_n/2):>10.3f}"
              f"{tv:>11.3f}{Delta/2*(1-tv):>13.5f}")
print("   Pinsker is an upper bound on TV, so the true Le Cam floor is at least")
print("   as large as the one the proposition states.  Confirmed above.")

# ---------- 2. Different likelihood family: Bernoulli outcomes ----------
# If the argument were Gaussian-specific the rate would change.  With
# Y|A=a*,H in H_d ~ Bern(1/2) vs Bern(1/2+eps), KL per rare obs is
# the binary KL, which is ~2 eps^2 for small eps -- same eps^2 scaling.
print()
print("=== 2. Bernoulli outcomes: does eps* scale the same way? ===")
def kl_bern(p, q): return p*np.log(p/q) + (1-p)*np.log((1-p)/(1-q))
for d in [4.0, 7.0]:
    n = 20000
    # solve n * c e^{-d} * KL_bern(.5, .5+eps) = 1/2
    lo, hi = 1e-6, 0.49
    for _ in range(200):
        mid = (lo+hi)/2
        if n*c*np.exp(-d)*kl_bern(0.5, 0.5+mid) < 0.5: lo = mid
        else: hi = mid
    eps_b = (lo+hi)/2
    eps_g = np.sqrt(2*0.25*0.5/(n*c*np.exp(-d)))   # Gaussian with sigma^2 = 1/4 (Bern var)
    print(f"   d={d}: eps*(Bernoulli)={eps_b:.5f}   eps*(Gaussian, s2=1/4)={eps_g:.5f}"
          f"   ratio={eps_b/eps_g:.3f}")
print("   ratio ~ 1 => the eps* ~ sigma sqrt(e^d/(nc)) scaling is not Gaussian-specific.")

# ---------- 3. Bayes risk floor: simulate the actual best estimator ----------
# For a two-point prior the Bayes-optimal estimator is the posterior mean; its
# risk is a hard floor for ANY estimator.  Compare to the stated bound.
print()
print("=== 3. Bayes risk of the two-point prior vs the stated floor ===")
def bayes_risk(n, c, d, eps, s2=1.0, reps=200_000):
    p_rare = c*np.exp(-d)
    theta = rng.integers(0, 2, reps)                  # which of P0/P1
    m = rng.binomial(n, p_rare, reps)
    mu = np.where(theta == 1, eps, 0.0)
    S = rng.normal(mu*m, np.sqrt(s2*m.clip(1)))*np.sqrt(m > 0)
    llr = (2*eps*S - m*eps**2)/(2*s2)                 # log p1/p0
    post1 = 1/(1+np.exp(-llr))
    beta = np.where(theta == 1, c*eps, 0.0)           # true parameter
    est = post1*(c*eps)                               # posterior mean
    return np.mean(np.abs(est-beta))
for d in [4.0, 7.0]:
    n = 20000
    eps = np.sqrt(2*0.5/(n*c*np.exp(-d)))
    br = bayes_risk(n, c, d, eps)
    stated = 0.25*np.sqrt(c*np.exp(d)/n)
    print(f"   d={d}: Bayes risk={br:.5f}   stated floor (1/4)sqrt(cM/n)={stated:.5f}"
          f"   ratio={br/stated:.2f}")
print("   Bayes risk >= stated floor => the proposition's constant is not too large.")
