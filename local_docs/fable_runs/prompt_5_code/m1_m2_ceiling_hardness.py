"""Rows M1 and M2: energy-product ceiling mu0*Ms^2/4 = (mu0 Ms)^2/(4 mu0), and hardness
parameter kappa_h = sqrt(K1/(mu0 Ms^2)).
LOOKUP source actually read: data/m1_intrinsic_magnetic.csv (arXiv 2310.02106 Table 1, a secondary
open review) -- NOT the Coey 2011 / Skomski-Coey 2016 tables named in the spec (not readable).
Co is absent from the readable table: Co K1 and mu0Ms use the planner's UNSURE endpoints (not a lookup).
Realised (BH)max values are MEMORY UNSURE ranges from the spec; upper endpoint is used for the check.
Published reference kappa_h values and ceilings (512, 45 kJ/m3) are the spec's/planner's, not read from the
Skomski-Coey table. Level: derived.
"""
import csv, os, math
MU0=1.25663706e-6
here=os.path.dirname(os.path.abspath(__file__))
rows={}
for l in open(os.path.join(here,'data','m1_intrinsic_magnetic.csv')):
    if l.startswith('#') or l.startswith('material'): continue
    p=l.strip().split(',')
    rows[p[0]]=(float(p[1]),float(p[3]))
fails=[]
def chk(n,ok,d=''):
    print(f"  CHECK {n}: {'PASS' if ok else 'FAIL'} {d}")
    if not ok: fails.append(n)
print("LOOKUP source: Granados-Miralles et al., arXiv:2310.02106, Table 1, https://arxiv.org/pdf/2310.02106, accessed 2026-11-14 (secondary; see data header)")
exp_range={'Fe':(2.15,2.15),'Fe65Co35':(2.43,2.45),'Nd2Fe14B':(1.61,1.61),'SmCo5':(1.05,1.14),'Sm2Co17':(1.25,1.25),'BaFe12O19':(0.48,0.48),'SrFe12O19':(0.48,0.48)}
print("== M1 ==")
ceil={}
for m in ['Fe','Fe65Co35','Nd2Fe14B','SmCo5','Sm2Co17','BaFe12O19','SrFe12O19']:
    B,K=rows[m]; lo,hi=exp_range[m]
    ceil[m]=B*B/(4*MU0)
    print(f"  {m}: mu0Ms={B} T (UNSURE expected {lo}-{hi}: {'inside' if lo-1e-9<=B<=hi+1e-9 else 'OUTSIDE'}) ceiling={ceil[m]/1e3:.1f} kJ/m3")
chk("Nd2Fe14B ceiling vs published 512 kJ/m3 within 2%",abs(ceil['Nd2Fe14B']/512e3-1)<0.02,f"{ceil['Nd2Fe14B']/1e3:.1f}")
chk("BaM ceiling vs published 45 kJ/m3 within 2%",abs(ceil['BaFe12O19']/45e3-1)<0.02,f"{ceil['BaFe12O19']/1e3:.1f}")
real={'NdFeB (400-474)':(474e3,ceil['Nd2Fe14B']),'ferrite (30-40) vs BaM':(40e3,ceil['BaFe12O19']),
      'Alnico5 (40-44) vs AlNiCo5 Bs':(44e3,rows['AlNiCo5'][0]**2/(4*MU0)),'Alnico9 (72-84) vs AlNiCo5 Bs [no Alnico9 Ms read]':(84e3,rows['AlNiCo5'][0]**2/(4*MU0))}
for k,(r,c) in real.items():
    print(f"  realised {k}: upper {r/1e3:.0f} kJ/m3, ceiling {c/1e3:.1f}, ratio {r/c:.3f}")
    chk(f"realised {k} below ceiling",r<c)
print("== M2 ==")
pub={'Nd2Fe14B':1.54,'SmCo5':4.35,'BaFe12O19':1.35,'Fe':0.12}
for m in ['Nd2Fe14B','SmCo5','BaFe12O19','Fe','Sm2Co17','Fe65Co35']:
    B,K=rows[m]; kh=math.sqrt(K*1e6*MU0/(B*B))
    s=f"  {m}: K1={K} MJ/m3 kappa_h={kh:.3f}"
    if m in pub:
        d=kh/pub[m]-1; s+=f" published(UNSURE, planner) {pub[m]} dev {100*d:+.1f}%"
    print(s)
    if m in pub: chk(f"kappa_h {m} within 3% of planner's published value",abs(kh/pub[m]-1)<0.03,f"{kh:.3f}")
# Co: not a lookup
for K in (0.41,0.53):
    B=1.82  # MEMORY UNSURE mu0 Ms of Co
    print(f"  Co (NOT A LOOKUP: planner endpoint K1={K} MJ/m3, mu0Ms=1.82 T MEMORY UNSURE): kappa_h={math.sqrt(K*1e6*MU0/B**2):.3f}; planner published range 0.41-0.45")
print("  Check on Co is circular (planner endpoints vs planner range): not scored.")
print("FAILS:",fails)
