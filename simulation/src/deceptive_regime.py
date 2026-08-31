import numpy as np
rng=np.random.default_rng(4)
sig=lambda x:1/(1+np.exp(-x))
# continuous_h main DGP: H~U(-1,1), p=sig(H/tau), Y = H + beta(H)A + N(0,1)
# Two laws differing ONLY in beta on the rarely-treated region H < -w  (where p is tiny).
def run(tau, n, nsims, shift, w=0.6):
    est=[]; ate=[]
    for _ in range(nsims):
        H=rng.uniform(-1,1,n); p=sig(H/tau); A=(rng.random(n)<p).astype(int)
        beta = 1+np.abs(H) + shift*(H < -w)
        Y = H + beta*A + rng.normal(0,1,n)
        w1=A/p; w0=(1-A)/(1-p)
        est.append(np.sum(w1*Y)/np.sum(w1) - np.sum(w0*Y)/np.sum(w0))   # Hajek
        ate.append(beta.mean())
    return np.array(est), np.mean(ate)

print("Deceptive regime: two DGPs, different true ATE, indistinguishable estimates")
print(f"{'tau':>6}{'n':>8}{'shift':>7}{'true ATE':>10}{'Hajek mean':>12}{'Hajek SD':>10}{'|bias|':>9}")
for tau,n in [(0.08, 2000), (0.08, 32000), (0.22, 2000)]:
    for shift in [0.0, 1.0]:
        e,a = run(tau,n,300,shift)
        print(f"{tau:>6.2f}{n:>8}{shift:>7.1f}{a:>10.3f}{e.mean():>12.3f}{e.std():>10.3f}{abs(e.mean()-a):>9.3f}")
    e0,a0=run(tau,n,300,0.0); e1,a1=run(tau,n,300,1.0)
    sep=abs(e1.mean()-e0.mean())/np.sqrt((e0.var()+e1.var())/2)
    print(f"       -> true ATE gap = {a1-a0:.3f} | estimated gap = {e1.mean()-e0.mean():+.3f}"
          f" | separation = {sep:.2f} SD\n")
