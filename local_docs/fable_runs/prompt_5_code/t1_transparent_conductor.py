"""Row T1: metal mesh vs In-based oxide film as transparent conductor.
Mesh (square grid, line fraction f=w/p, thickness t): R_s = 1/(sigma t f); T=(1-f)^2 (geometric, no diffraction/haze).
Film: R_s = rho_f/t_f, T given. Haacke FoM = T^10/R_s (1/Ohm). Sweep f in [0.005,0.2], t in [0.1,2] um for Cu and Al.
sigma from row A1 (Cu 5.80e7, Al 3.54e7 S/m); densities Cu 8960, Al 2700 kg/m3 (MEMORY, A1).
Film data: NOT A LOOKUP (Ellmer 2012 paywalled; see data/t1_ito_film.csv): planner's UNSURE endpoints
(rho 1-2e-6 Ohm m, t 100-200 nm, T 0.85-0.90), In mass fraction 0.74, film density 7140 kg/m3 (MEMORY UNSURE).
Level: derived.
"""
import os, numpy as np
from scipy.optimize import minimize_scalar
here=os.path.dirname(os.path.abspath(__file__))
film=[]
for l in open(os.path.join(here,'data','t1_ito_film.csv')):
    if l.startswith('#') or l.startswith('case'): continue
    c,rho,t,T=l.strip().split(','); film.append((c,float(rho),float(t)*1e-9,float(T)))
fails=[]
def chk(n,ok,d=''):
    print(f"  CHECK {n}: {'PASS' if ok else 'FAIL'} {d}")
    if not ok: fails.append(n)
M={'Cu':(5.80e7,8960.),'Al':(3.54e7,2700.)}
def mesh(sig,t,f): return 1/(sig*t*f),(1-f)**2
def fom(R,T): return T**10/R
print("film cases (NOT A LOOKUP):")
fF=[]
for c,rho,t,T in film:
    R=rho/t; fF.append(fom(R,T)); m_in=7140*0.74*t
    print(f"  {c}: rho={rho:.2e} t={t*1e9:.0f} nm T={T} R_s={R:.2f} Ohm/sq FoM={fom(R,T):.4f} 1/Ohm  In mass={m_in*1e3:.3f} g/m2")
print(f"  film FoM range {min(fF):.4f} .. {max(fF):.4f} (best film combination of best-corner values)")
# also extreme corner combos (best rho, thickest, highest T) - already 'best'.
Rm,Tm=mesh(5.80e7,0.5e-6,0.025)
print(f"Cu w/p=0.025 t=0.5 um: R_s={Rm:.3f} Ohm/sq T={Tm:.4f} (expected ~1.4 and ~0.95)")
chk("Cu example R_s ~1.4 within 2%",abs(Rm/1.4-1)<0.02,f"{Rm:.3f}"); chk("Cu example T ~0.95 within 2%",abs(Tm/0.95-1)<0.02,f"{Tm:.4f}")
chk("limit w/p->1: R_s=1/(sigma t)",abs(mesh(5.8e7,0.5e-6,1.0)[0]*5.8e7*0.5e-6-1)<1e-12," (identity: same formula)")
f=np.logspace(np.log10(0.005),np.log10(0.2),200); t=np.linspace(0.1e-6,2e-6,40)
for mat,(sig,rho) in M.items():
    Fg=np.array([[fom(*mesh(sig,tt,ff)) for ff in f] for tt in t])
    beats=(Fg>max(fF)).mean()
    print(f"{mat}: FoM over sweep min {Fg.min():.3f} max {Fg.max():.3f}; fraction of sweep above best film FoM: {beats:.3f}; above worst film: {(Fg>min(fF)).mean():.3f}")
    # optimum f at each t via minimize_scalar bracket
    for tt in (0.1e-6,0.5e-6,2e-6):
        r=minimize_scalar(lambda ff:-fom(*mesh(sig,tt,ff)),bounds=(0.005,0.2),method='bounded',options={'xatol':1e-10})
        print(f"   t={tt*1e6} um: f*={r.x:.5f} (analytic 1/21={1/21:.5f}) FoM*={-r.fun:.3f}")
    chk(f"{mat} some swept mesh exceeds best film FoM",beats>0)
    chk(f"{mat} f* = 1/21 (bracket [0.005,0.2] contains it)",abs(r.x-1/21)<1e-6)
print("note: FoM grows linearly with t at fixed f (no interior optimum in t; the sweep's upper edge t=2 um is the maximum, limited by process aspect ratio, not by the formula).")
print("note: T=(1-f)^2 neglects diffraction, haze and edge shadowing; T^10/R_s is Haacke's definition for continuous films; applying it to a mesh is a spec choice.")
print("Mesh/film comparison, masses per m2 (mesh solid area fraction 2f-f^2):")
for mat,(sig,rho) in M.items():
    for ff,tt in ((0.025,0.5e-6),(1/21,0.5e-6)):
        R,T=mesh(sig,tt,ff); ma=rho*tt*(2*ff-ff*ff)
        print(f"  {mat} f={ff:.4f} t={tt*1e6} um: R_s={R:.3f} T={T:.4f} FoM={fom(R,T):.3f} mass={ma*1e3:.3f} g/m2")
print("Equal-R_s and equal-T mesh thickness to mid film (R_s=10, T=0.875):")
for mat,(sig,rho) in M.items():
    ff=1-np.sqrt(0.875); tt=1/(sig*ff*10); print(f"  {mat}: f={ff:.4f} needs t={tt*1e9:.1f} nm, mass={rho*tt*(2*ff-ff*ff)*1e3:.4f} g/m2 vs In in film {7140*0.74*150e-9*1e3:.3f} g/m2 (In)")
print("Minimum line width (process input, not provided): for f=0.025, a 5 um line (UNSURE, example only) implies pitch 200 um; a 1 um line pitch 40 um. Not computed by spec.")
print("FAILS:",fails)
