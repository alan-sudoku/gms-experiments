"""Row P1: heat pipe capillary limit, effective conductivity, wall share of radial resistance.
Q_max = (rho_l sigma_l hfg/mu_l) * (K A_w/L_eff) * (2/r_eff)   (vapour and gravity terms neglected, as in spec)
Radial resistance per end: R = t_w/(k_wall A_e) + t_wick/(k_wick A_e), A_e = pi*OD*L_e (outer surface of heated or cooled
length; my choice, spec does not define A_e). k_eff = Q L_eff/(A_x dT), dT = Q*(R_evap+R_cond), A_x = pi/4 OD^2 (my choice).
A_w = wick annulus: ID = OD-2*t_wall, vapour core dia = ID-2*t_wick.
LOOKUP: water at 60 C from data/p1_water_60C.csv (Cengel and Cimbala 2014 Table A-3, SUBSTITUTE for Incropera Table A.6,
accessed 2026-11-14). Reay, Kew and McGlen 2014 NOT readable: the worked-example reproduction was NOT performed.
k_wick=40 W/mK is the spec's UNSURE input. Fluid-wall compatibility is a threshold, not computed. Level: derived.
"""
import os, math, numpy as np
here=os.path.dirname(os.path.abspath(__file__))
for l in open(os.path.join(here,'data','p1_water_60C.csv')):
    if l.startswith('#') or l.startswith('rho'): continue
    rho,sig,hfg,mu=map(float,l.strip().split(','))
print("LOOKUP (Cengel and Cimbala 2014, Table A-3, 60 C; substitute for Incropera Table A.6): rho_l=%g sigma_l=%g hfg=%g mu_l=%g"%(rho,sig,hfg,mu))
print("planner UNSURE expected: rho 983, sigma 0.066, hfg 2.36e6, mu 4.7e-4 -> all four inside (983.3; 0.0662; 2.359e6; 4.67e-4)")
fails=[]
def chk(n,ok,d=''):
    print(f"  CHECK {n}: {'PASS' if ok else 'FAIL'} {d}")
    if not ok: fails.append(n)
Mn=rho*sig*hfg/mu
print(f"merit number = {Mn:.4e} W/m2 (expected ~3.3e11)"); chk("merit ~3.3e11 within 5%",abs(Mn/3.3e11-1)<0.05)
OD=6e-3; tw=0.3e-3; twk=0.5e-3; kwick=40.0; Le=0.03; Leff=0.15
ID=OD-2*tw; Dv=ID-2*twk
Aw=math.pi/4*(ID**2-Dv**2); Ax=math.pi/4*OD**2; Ae=math.pi*OD*Le
print(f"geometry: ID={ID*1e3} mm vapour dia={Dv*1e3:.2f} mm A_w={Aw*1e6:.3f} mm2 A_x={Ax*1e6:.2f} mm2 A_e={Ae*1e6:.1f} mm2")
def Qmax(K,r,L): return Mn*K*Aw/L*2/r
Q0=Qmax(5e-11,30e-6,Leff)
print(f"Q_max (K=5e-11, r=30 um, L_eff=0.15) = {Q0:.1f} W (expected 10-100)"); chk("Q_max in 10-100 W",10<=Q0<=100)
K=np.logspace(-12,-9,31); r=np.linspace(5e-6,200e-6,40); L=np.linspace(0.05,0.5,10)
Qg=np.array([[[Qmax(k,rr,l) for l in L] for rr in r] for k in K])
print(f"sweep Q_max: min {Qg.min():.3g} W (K=1e-12,r=200um,L=0.5) max {Qg.max():.3g} W (K=1e-9,r=5um,L=0.05); fraction of grid within 10-100 W: {np.mean((Qg>=10)&(Qg<=100)):.2f}")
print("sweep status: Q_max is a monotone power-law in K, 1/r, 1/L (no crossover); the sweep brackets 10-100 W (grid spans below and above) but nothing else.")
print("wall share (k_wick=40) and k_eff:")
for kw in (400,200,16):
    Rw=tw/(kw*Ae); Rk=twk/(kwick*Ae); Rend=Rw+Rk; share=Rw/Rend
    keff=Leff/(Ax*2*Rend)
    print(f"  k_wall={kw}: R_wall/end={Rw:.4e} K/W R_wick/end={Rk:.4e} K/W wall share={100*share:.1f}%  k_eff={keff:.3g} W/mK ({keff/400:.0f}x Cu 400); dT at Q0={Q0*2*Rend:.2f} K")
    if kw==200:
        chk("wall share < 20% for k_wall=200",share<0.20,f"{100*share:.1f}%")
        chk("k_eff >= 10x 400 W/mK",keff>=4000,f"{keff:.3g}")
print("note: k_eff = L_eff/(A_x*R_total) does not depend on Q or on K, r_eff; the K/r/L sweep therefore does not change wall share or k_eff (L_eff enters k_eff only linearly).")
print("note: wall share vs k_wall is mostly set by the wick resistance (k_wick 40, UNSURE); a hotter-wick (k_wick->200) would raise the wall share.")
for kwk in (10,40,100,200):
    Rw=tw/(200*Ae); Rk=twk/(kwk*Ae); print(f"  sensitivity k_wick={kwk}: wall share (k_wall=200) = {100*Rw/(Rw+Rk):.1f}%")
print("Reay worked example: NOT performed (book not readable).")
print("FAILS:",fails)
