import numpy as np
rng=np.random.default_rng(0)
sig=lambda x:1/(1+np.exp(-x))

print("=== 1. KL algebra check (Gaussian outcomes, shift only on rare arm) ===")
# one observation: H ~ Bern(c) for in/out of H_d; if in, A=a* w.p. e^{-d}; Y|A=a* ~ N(mu,1)
c, d, eps, s2 = 0.4, 3.0, 0.25, 1.0
kl_analytic = c*np.exp(-d)*eps**2/(2*s2)
# MC: KL = E_{P0}[log dP0/dP1]; only the (in-stratum, A=a*) cell contributes
n=8_000_000
inH = rng.random(n) < c
rare = inH & (rng.random(n) < np.exp(-d))
Y = rng.normal(0.0,1.0,n)                      # under P0, mu=0 on that cell
llr = np.zeros(n)
llr[rare] = (-(Y[rare]-0)**2 + (Y[rare]-eps)**2)/2   # log p0/p1
print(f"  analytic KL/obs = {kl_analytic:.3e}   MC = {llr.mean():.3e}   ratio={llr.mean()/kl_analytic:.3f}")

print()
print("=== 2. Le Cam bound: minimax risk >= rho_min*sigma*sqrt(c e^d / n) ===")
print("   choose eps so that n*KL = 1/2, then Delta = rho_min*c*eps")
for dd in [2.0,4.0,6.0]:
    for nn in [1000, 100000]:
        e_star = np.sqrt(2*s2*0.5/(nn*c*np.exp(-dd)))
        Delta = 1.0*c*e_star
        print(f"   d={dd}, n={nn:>6}: eps*={e_star:.4f}  Delta={Delta:.4f}  "
              f"pred={1.0*np.sqrt(c*np.exp(dd)/nn):.4f}")

print()
print("=== 3. two-point indistinguishability, simulated ===")
print("   oracle-IPW estimator on data from P0 vs P1; if TV small it cannot separate")
def draw(N, d, eps, c=0.4, rho=0.5):
    inH = rng.random(N) < c
    p_rare = np.where(inH, np.exp(-d), 0.5)
    A = (rng.random(N) < p_rare).astype(int)      # A=1 is the rare arm inside H_d
    mu1 = np.where(inH, eps, 0.0)
    Y = np.where(A==1, mu1, 0.0) + rng.normal(0,1,N)
    return inH, p_rare, A, Y
def ipw(inH,p,A,Y):                                # target: E[rho*mu1] with rho=1
    return np.mean(A*Y/p)
for d in [4.0, 7.0]:
    n = 20000
    eps = np.sqrt(2*0.5/(n*0.4*np.exp(-d)))
    b0=[]; b1=[]
    for _ in range(400):
        b0.append(ipw(*draw(n,d,0.0))); b1.append(ipw(*draw(n,d,eps)))
    b0,b1=np.array(b0),np.array(b1)
    truth_gap = 0.4*eps
    sep = abs(b1.mean()-b0.mean())/np.sqrt((b0.var()+b1.var())/2)
    print(f"   d={d}: eps*={eps:.4f} true gap={truth_gap:.4f} | est gap={b1.mean()-b0.mean():+.4f} "
          f"est SD={b0.std():.4f} | separation={sep:.2f} SD")
