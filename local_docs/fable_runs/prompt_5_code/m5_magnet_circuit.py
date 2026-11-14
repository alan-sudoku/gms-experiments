"""Row M5: magnet volume vs energy product at device level.
Formula: V_m = Bg^2 Vg/(mu0 |BH|). Independent numerical route: linear demagnetisation line Bm=Br+mu0 mu_r Hm,
ideal iron, no leakage; minimise V_m=A_m*l_m over (ln A_m, ln l_m) with scipy.optimize.minimize (SLSQP, one
equality constraint: Hm*l_m = -Hg*lg with Bm=Bg*Ag/Am), then compare with the formula at (BH)max=Br^2/(4 mu0 mu_r).
Inputs (spec): Bg=0.8 T, Vg=1e-5 m3 (Ag=1e-2 m2, lg=1e-3 m), mu_r=1.05; MEMORY UNSURE: NdFeB Br 1.35 T, 7500 kg/m3,
HcJ>=900 kA/m; ferrite Br 0.41 T, 4900 kg/m3, HcJ 250-400 kA/m. No LOOKUP. Level: derived.
Caveat: the optimiser uses the same physical model as the formula (ideal iron, linear line), so agreement tests the
algebra and the location of the optimum (Bm=Br/2), not the physics of leakage or fringing.
"""
import numpy as np
from scipy.optimize import minimize
MU0=1.25663706e-6
Bg=0.8; Ag=1e-2; lg=1e-3; Vg=Ag*lg; mur=1.05
fails=[]
def chk(n,ok,d=''):
    print(f"  CHECK {n}: {'PASS' if ok else 'FAIL'} {d}")
    if not ok: fails.append(n)
def formula(BH): return Bg**2*Vg/(MU0*BH)
print("formula (BH sweep, kJ/m3 -> cm3):",{b:round(formula(b*1e3)*1e6,2) for b in (10,32,100,350,450)})
chk("14.6 cm3 at 350 kJ/m3 within 5%",abs(formula(350e3)*1e6/14.6-1)<0.05,f"{formula(350e3)*1e6:.2f}")
chk("159 cm3 at 32 kJ/m3 within 5%",abs(formula(32e3)*1e6/159-1)<0.05,f"{formula(32e3)*1e6:.1f}")
out={}
for name,Br,rho,HcJ in [('NdFeB',1.35,7500,(900e3,900e3)),('ferrite',0.41,4900,(250e3,400e3))]:
    BHmax=Br**2/(4*MU0*mur)
    Hg=Bg/MU0
    def V(x):
        Am,lm=np.exp(x); return Am*lm
    cons={'type':'eq','fun':lambda x:(((Bg*Ag/np.exp(x[0]))-Br)/(MU0*mur))*np.exp(x[1])+Hg*lg*1.0}
    # scale: normalise constraint by Hg*lg
    cons={'type':'eq','fun':lambda x,Br=Br:((((Bg*Ag/np.exp(x[0]))-Br)/(MU0*mur))*np.exp(x[1])+Hg*lg)/(Hg*lg)}
    best=None
    for Bm0 in (0.2*Br,0.5*Br,0.8*Br):   # several starts
        Am0=Bg*Ag/Bm0; Hm0=(Bm0-Br)/(MU0*mur); lm0=-Hg*lg/Hm0
        r=minimize(lambda x:np.log(V(x)),np.log([Am0,lm0]),constraints=[cons],method='SLSQP',options={'ftol':1e-14,'maxiter':500})
        if r.success and (best is None or r.fun<best.fun): best=r
    Am,lm=np.exp(best.x); Bm=Bg*Ag/Am; Hm=(Bm-Br)/(MU0*mur)
    Vf=formula(BHmax)
    out[name]=(Am*lm,rho)
    print(f"  {name}: Br={Br} T BHmax={BHmax/1e3:.1f} kJ/m3  formula V_m={Vf*1e6:.3f} cm3  optimiser V_m={Am*lm*1e6:.3f} cm3  Bm/Br={Bm/Br:.4f}  Hm={Hm/1e3:.1f} kA/m  HcJ(UNSURE)={HcJ[0]/1e3:.0f}-{HcJ[1]/1e3:.0f} kA/m  mass={Am*lm*rho*1e3:.1f} g")
    chk(f"{name} optimiser vs formula within 5%",abs(Am*lm/Vf-1)<0.05,f"{Am*lm/Vf-1:+.2e}")
    chk(f"{name} operates at Bm=Br/2 (1%)",abs(Bm/Br-0.5)<0.01)
    chk(f"{name} |Hm| below lowest HcJ (UNSURE)",abs(Hm)<HcJ[0],"")
vr=out['ferrite'][0]/out['NdFeB'][0]; mr=vr*out['ferrite'][1]/out['NdFeB'][1]
print(f"  volume ratio ferrite/NdFeB={vr:.2f} (expected ~11); mass ratio={mr:.2f} (expected ~7)")
chk("volume ratio ~11 within 10%",abs(vr/11-1)<0.10); chk("mass ratio ~7 within 10%",abs(mr/7-1)<0.10)
print("note: formula at BHmax vs optimiser is non-identity only through the optimum location; V_m formula and constraint solve share the same equations.")
print("FAILS:",fails)
