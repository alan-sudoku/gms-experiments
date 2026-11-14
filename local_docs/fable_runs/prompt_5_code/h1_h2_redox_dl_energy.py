"""Rows H1 and H2 (prompt 5 plan, section 3): energy of redox cells per kg and per atom,
and double-layer energy per carbon atom with its geometric ceiling.
Assumptions: voltages and C_dl are MEMORY inputs from the spec; atomic masses are standard
atomic weights typed from memory (UNSURE; not looked up). No LOOKUP value could be read:
Linden and Reddy 2002 Table 1.2 is a book, so the 1 470 Wh/kg reference is NOT a lookup.
Level: derived (unverified).
"""
import math
F=96485.332; NA=6.02214076e23; QE=1.602176634e-19
AM={'Li':6.94,'S':32.06,'O':15.999,'Cl':35.45,'Zn':65.38,'Mn':54.938,'Co':58.933,'C':12.011,
    'Fe':55.845,'P':30.974,'Pb':207.2,'H':1.008}
def M(f): return sum(AM[k]*n for k,n in f.items())/1000.0   # kg/mol
fails=[]
def chk(name,ok,detail=''):
    print(f"  CHECK {name}: {'PASS' if ok else 'FAIL'} {detail}")
    if not ok: fails.append(name)
print("== H1 ==  inputs: n, V (MEMORY), reactant formula, N_at atoms per reactant formula")
SOCl2={'S':1,'O':1,'Cl':2}
cells=[
 ('4Li+2SOCl2',4,3.65,{'Li':4,'S':2,'O':2,'Cl':4},12),
 ('Zn+2MnO2',2,1.5,{'Zn':1,'Mn':2,'O':4},7),
 ('LiCoO2+3C (0.5 Li)',0.5,3.7,{'Li':1,'Co':1,'O':2,'C':3},6),
 ('LiFePO4+6C',1,3.3,{'Li':1,'Fe':1,'P':1,'O':4,'C':6},13),
 ('Pb+PbO2+2H2SO4',2,2.05,{'Pb':2,'O':2+8,'H':4,'S':2},18),
]
res={}
for name,n,V,form,nat in cells:
    m=M(form)
    e_kg=n*F*V/m
    e_atom=n*F*V/(nat*NA)/QE      # eV (n*F*V/(N_at*N_A) J divided by e)
    res[name]=e_atom
    print(f"  {name}: n={n} V={V} M={m*1000:.2f} g/mol N_at={nat}  E={e_kg/3600:.0f} Wh/kg ({e_kg/1e6:.3f} MJ/kg)  {e_atom:.3f} eV/atom")
# Li/SOCl2 reference
wh=4*F*3.65/M(cells[0][3])/3600
print(f"  Li/SOCl2 theoretical {wh:.1f} Wh/kg; reference 1470 (spec: Linden and Reddy Table 1.2, UNSURE) -- NOT A LOOKUP, book not readable;")
print("   web snippets from secondary pages gave 1470 and 1500 (not Table 1.2; not recorded as a lookup).")
chk("H1 Li/SOCl2 within 2% of 1470 (reference unverified)",abs(wh/1470-1)<0.02,f"dev {100*(wh/1470-1):+.2f}%")
chk("H1 per-atom 1.22 (SOCl2) within 2%",abs(res['4Li+2SOCl2']/1.22-1)<0.02,f"{res['4Li+2SOCl2']:.3f}")
chk("H1 per-atom 0.43 (Zn/MnO2) within 2%",abs(res['Zn+2MnO2']/0.43-1)<0.02,f"{res['Zn+2MnO2']:.3f}")
print("  UNSURE 0.26 eV expected: LiFePO4 gives %.3f, LiCoO2+3C gives %.3f (atom basis ambiguous, see issues)"%(res['LiFePO4+6C'],res['LiCoO2+3C (0.5 Li)']))
chk("H1 per-atom 0.26 within 2% for LiCoO2 cell",abs(res['LiCoO2+3C (0.5 Li)']/0.26-1)<0.02,f"{res['LiCoO2+3C (0.5 Li)']:.3f}")
chk("H1 per-atom 0.26 within 2% for LiFePO4 cell",abs(res['LiFePO4+6C']/0.26-1)<0.02,f"{res['LiFePO4+6C']:.3f}")
print("\n== H2 ==")
a=0.142e-9; CDL=21e-6/1e-4   # F/m2 (21 uF/cm2, MEMORY, Xia 2009)
A_at=3*math.sqrt(3)/4*a*a
ssa=2*A_at*NA/(AM['C']/1000)   # m2/kg
print(f"  area/atom {A_at:.4e} m2 ; SSA two faces {ssa/1000:.1f} m2/g (published 2630)")
chk("H2 SSA 2630 +-10 m2/g",abs(ssa/1000-2630)<=10,f"{ssa/1000:.1f}")
Csp=CDL*ssa
print(f"  C_sp ceiling = 21 uF/cm2 * SSA = {Csp/1000:.1f} F/g (expected ~550)")
chk("H2 C_sp ~550 F/g within 1%",abs(Csp/1000/550-1)<0.01,f"{Csp/1000:.1f}")
eps0=8.8541878128e-12; ch=eps0*10/0.5e-9*1e6/1e4
print(f"  Helmholtz eps0*eps_r/d (eps_r=10, d=0.5 nm) = {ch:.1f} uF/cm2 (expected ~18, same order as 21)")
chk("H2 Helmholtz same order (within 25% of 21)",abs(ch/21-1)<0.25,f"{ch:.1f}")
def e_atom(Cs,V): return 0.5*(Cs/4)*V*V*(AM['C']/1000)/NA/QE
cases=[('100 F/g, 1.0 V',100e3,1.0,0.0016),('100 F/g, 2.7 V',100e3,2.7,0.011),
       ('ceiling, 2.7 V',Csp,2.7,0.062),('ceiling, 4.0 V',Csp,4.0,0.14)]
for nm,Cs,V,exp in cases:
    e=e_atom(Cs,V)
    print(f"  {nm}: {e:.5f} eV/atom (expected {exp}); ratio to H1 Li/SOCl2 per atom {res['4Li+2SOCl2']/e:.0f}x, to LiFePO4 {res['LiFePO4+6C']/e:.1f}x")
    chk(f"H2 {nm} within 1%... (expected values are 2-sig-fig, tolerance 1% applied to rounded values)",abs(e/exp-1)<0.01,f"{e:.5f}")
print("FAILS:",fails)
