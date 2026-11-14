"""Row M3: shape-anisotropy energy-product ceiling (planner derivation D9, UNSURE as published result).
BH = mu0 (p Ms - H') H', H' in [0,(1-p) Ms/2], p in (0,1). In units of mu0 Ms^2: f=(p-h)h, h in [0,(1-p)/2].
Method (spec): brute-force 2000x2000 grid (p x s with H'=s*(1-p)/2 Ms, s in [0,1]); also analytic optimum via
minimize_scalar on bracket p in [0.5,1], and the p<=0.5 branch. Absolute values use mu0Ms from
data/m1_intrinsic_magnetic.csv (LOOKUP source: arXiv 2310.02106 Table 1, accessed 2026-11-14).
Skomski et al. 2010 (J. Appl. Phys. 107, 09A739) was NOT read; whether it states mu0Ms^2/12 is UNKNOWN.
Level: derived.
"""
import os, numpy as np
from scipy.optimize import minimize_scalar
MU0=1.25663706e-6
here=os.path.dirname(os.path.abspath(__file__))
B={}
for l in open(os.path.join(here,'data','m1_intrinsic_magnetic.csv')):
    if l.startswith('#') or l.startswith('material'): continue
    p=l.split(','); B[p[0]]=float(p[1])
fails=[]
def chk(n,ok,d=''):
    print(f"  CHECK {n}: {'PASS' if ok else 'FAIL'} {d}")
    if not ok: fails.append(n)
N=2000
def grid(pmax):
    p=np.linspace(0,pmax,N)[:,None]; s=np.linspace(0,1,N)[None,:]
    h=s*(1-p)/2
    f=(p-h)*h
    i=np.unravel_index(np.argmax(f),f.shape)
    return f[i],p[i[0],0],h[i]
f1,p1,h1=grid(1.0)
print(f"full grid {N}x{N}: max={f1:.6f} mu0Ms^2 at p={p1:.5f}, H'/Ms={h1:.5f}  (1/12={1/12:.6f})")
chk("grid max = 1/12 within 0.1%",abs(f1*12-1)<1e-3,f"{f1*12:.6f}")
f2,p2,h2=grid(0.5)
print(f"grid p<=0.5: max={f2:.6f} at p={p2:.5f} (1/16={1/16:.6f})")
chk("grid p<=0.5 = 1/16 within 0.1%",abs(f2*16-1)<1e-3,f"{f2*16:.6f}")
# analytic optimum on bracket [0.5,1]
r=minimize_scalar(lambda p:-(3*p-1)*(1-p)/4,bounds=(0.5,1.0),method='bounded',options={'xatol':1e-12})
print(f"analytic (minimize_scalar on p in [0.5,1], branch H'=Hc): p*={r.x:.8f}, f={-r.fun:.10f}; 1/12={1/12:.10f}")
chk("analytic optimum p=2/3",abs(r.x-2/3)<1e-6); chk("analytic value 1/12",abs(-r.fun-1/12)<1e-12)
print("bracket status: the p grid spans (0,1) and contains the optimum p=2/3 in its interior; minimize_scalar bracket [0.5,1] contains it; the unconstrained branch (p<=0.5) has its max at the bracket edge p=0.5 (monotonic p^2/4), grid-limited.")
print("note: the grid maximum is compared with the analytic optimum of the SAME function: consistency of the numerics, not evidence for the model (the model is the planner's derivation).")
print("Absolute values (mu0 Ms^2/12 = (mu0Ms)^2/(12 mu0)); mu0Ms from LOOKUP file:")
for m in ['Fe','Fe65Co35']:
    print(f"  {m}: mu0Ms={B[m]} T  BH_max(shape)= {B[m]**2/(12*MU0)/1e3:.1f} kJ/m3 ; single-needle mu0 Hc = mu0Ms/2 = {B[m]/2:.3f} T")
chk("Fe65Co35 within 390-400 kJ/m3 (spec UNSURE range)",390e3<=B['Fe65Co35']**2/(12*MU0)<=400e3,f"{B['Fe65Co35']**2/(12*MU0)/1e3:.1f}")
chk("Fe approx 307 kJ/m3 within 1%",abs(B['Fe']**2/(12*MU0)/307e3-1)<0.01,f"{B['Fe']**2/(12*MU0)/1e3:.1f}")
chk("Fe single needle mu0Hc ~1.08 T within 1%",abs(B['Fe']/2/1.08-1)<0.01,f"{B['Fe']/2:.3f}")
print("Skomski et al. 2010 statement: NOT READ (unverified whether it agrees).")
print("FAILS:",fails)
