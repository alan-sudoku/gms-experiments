"""Row H3: Ragone crossover time double-layer cell vs Li-ion cell.
Model A (spec): deliverable specific energy in time t = min(E, P_max*t) per device;
 t* = crossing found with brentq on [0.1, 1e4] s.
Model B (cross-check, planner's reading of Christen and Carlen 2000, UNSURE): E_d(t)=P t/(1+P t/E),
 which has E_d = E/2 at t = E/P. Not read from the paper.
Inputs MEMORY UNSURE: DL cell 4-8 Wh/kg, 5-15 kW/kg; Li-ion 150-260 Wh/kg, 0.3-3 kW/kg. Level: derived.
"""
import itertools, numpy as np
from scipy.optimize import brentq
fails=[]
def chk(n,ok,d=''):
    print(f"  CHECK {n}: {'PASS' if ok else 'FAIL'} {d}")
    if not ok: fails.append(n)
def curveA(E,P,t): return np.minimum(E,P*t)
def curveB(E,P,t): return P*t/(1+P*t/E)
def tstar(model,Ec,Pc,Eb,Pb,lo=0.1,hi=1e4):
    f=lambda t: model(Ec,Pc,t)-model(Eb,Pb,t)
    if f(lo)*f(hi)>0: return None
    return brentq(f,lo,hi,xtol=1e-10)
# note: model A has a flat region f==0 only if both saturate equal; here Ec<Eb so unique sign change
cen=dict(Ec=6*3600,Pc=10e3,Eb=200*3600,Pb=1.5e3)
print("central: E_c=6 Wh/kg P_c=10 kW/kg ; E_b=200 Wh/kg P_b=1.5 kW/kg")
tA=tstar(curveA,**cen); tB=tstar(curveB,**cen)
print(f"  t*(A)={tA:.3f} s, analytic E_c/P_b={cen['Ec']/cen['Pb']:.3f} s ; t*(B)={tB:.3f} s")
chk("A: t* = E_c/P_b",abs(tA-cen['Ec']/cen['Pb'])<1e-6)
chk("A vs B within factor 2",0.5<tA/tB<2,f"ratio {tA/tB:.3f}")
chk("t* inside 1-1000 s (central)",1<tA<1000)
print("limits: t=0.1 s capacitor ahead?",curveA(cen['Ec'],cen['Pc'],0.1)>curveA(cen['Eb'],cen['Pb'],0.1),
      "; t=1e4 battery/capacitor energy ratio",curveA(cen['Eb'],cen['Pb'],1e4)/curveA(cen['Ec'],cen['Pc'],1e4),"vs E_b/E_c",cen['Eb']/cen['Ec'])
chk("limit t=1e4: ratio = E_b/E_c",abs(curveA(cen['Eb'],cen['Pb'],1e4)/curveA(cen['Ec'],cen['Pc'],1e4)-cen['Eb']/cen['Ec'])<1e-9)
print("range corners (E_c,P_c,E_b,P_b), all 16 corners:")
ts=[];allbr=True;maxr=0;minr=9
for Ec,Pc,Eb,Pb in itertools.product([4,8],[5e3,15e3],[150,260],[300,3000]):
    c=dict(Ec=Ec*3600,Pc=Pc,Eb=Eb*3600,Pb=Pb)
    a=tstar(curveA,**c); b=tstar(curveB,**c)
    if a is None or b is None: allbr=False; print("  no bracket",c); continue
    ts.append(a); r=a/b; maxr=max(maxr,r); minr=min(minr,r)
print(f"  t*(A) range {min(ts):.2f} .. {max(ts):.2f} s ; A/B ratio range {minr:.2f}..{maxr:.2f}")
chk("sweep [0.1,1e4] s brackets t* at all corners",allbr)
chk("all corners A/B within factor 2",maxr<2 and minr>0.5)
chk("all corner t* within 1-1000 s",min(ts)>1 and max(ts)<1000)
print("note: CHECK 'A: t*=E_c/P_b' compares a root with the closed form of the same model (consistency of root finder, not independent evidence).")
print("FAILS:",fails)
