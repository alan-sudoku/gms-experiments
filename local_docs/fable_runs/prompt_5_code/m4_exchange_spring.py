"""Row M4: exchange-spring hard fraction and energy product (formulas of D9, equation numbers UNSURE).
f_h = mu0 Ms^2/(4 K_h); (BH)max = (mu0 Ms^2/4)(1 - mu0 (Ms-Mh) Ms/(2 K_h)); wall width pi*sqrt(A/K_h).
Inputs MEMORY UNSURE (spec): Sm2Fe17N3 mu0Mh=1.55 T, K_h=12 MJ/m3; Fe65Co35 mu0Ms=2.43 T;
Nd2Fe14B 1.61 T, 4.9 MJ/m3, A=8 pJ/m. A for Sm2Fe17N3 is not given; the Nd2Fe14B value 8 pJ/m is reused (UNSURE).
No LOOKUP was performed (Skomski and Coey 1993 not read); the 1 090 kJ/m3 'published' value is the spec's
memory, so the 3% check is against an unverified number. Sensitivity to Fe65Co35 mu0Ms=2.45 T (read in M1 lookup) is shown.
Level: derived.
"""
import math
MU0=1.25663706e-6
fails=[]
def chk(n,ok,d=''):
    print(f"  CHECK {n}: {'PASS' if ok else 'FAIL'} {d}")
    if not ok: fails.append(n)
def calc(Bs,Bh,K,A):
    Ms=Bs/MU0; Mh=Bh/MU0
    ceil=MU0*Ms*Ms/4
    fh=MU0*Ms*Ms/(4*K)
    corr=1-MU0*(Ms-Mh)*Ms/(2*K)
    bh=ceil*corr
    return fh,bh,math.pi*math.sqrt(A/K),Mh
for lab,Bs,Bh,K,A in [("Sm2Fe17N3 + FeCo(2.43)",2.43,1.55,12e6,8e-12),("Nd2Fe14B + FeCo(2.43)",2.43,1.61,4.9e6,8e-12),
                      ("Sm2Fe17N3 + FeCo(2.45)",2.45,1.55,12e6,8e-12),("Nd2Fe14B + FeCo(2.45)",2.45,1.61,4.9e6,8e-12)]:
    fh,bh,w,Mh=calc(Bs,Bh,K,A)
    single=Bh**2/(4*MU0)
    # hard-phase volume per unit energy product vs single phase (1 m3 of hard phase gives 'single')
    vr=(fh/bh)/(1/single)
    print(f"  {lab}: f_h={fh:.4f}  (BH)max={bh/1e3:.1f} kJ/m3  wall width={w*1e9:.2f} nm  single-phase ceiling={single/1e3:.1f} kJ/m3  hard-phase volume per unit (BH): {vr:.3f} of single-phase")
    if lab.startswith("Sm2Fe17N3 + FeCo(2.43)"):
        chk("Sm pair (BH)max vs published 1090 (unverified) within 3%",abs(bh/1090e3-1)<0.03,f"{bh/1e3:.1f}")
        chk("Sm pair f_h ~ 9% (spec 9-10%)",0.085<=fh<=0.105,f"{fh:.4f}")
    if lab.startswith("Nd2Fe14B + FeCo(2.43)"):
        chk("Nd pair f_h ~0.24 within 3%",abs(fh/0.24-1)<0.03,f"{fh:.4f}")
        chk("Nd pair (BH)max ~985 within 3%",abs(bh/985e3-1)<0.03,f"{bh/1e3:.1f}")
        chk("Nd pair wall ~4 nm within 10%",abs(w*1e9/4-1)<0.10,f"{w*1e9:.2f}")
print("note: 'hard-phase volume' stands in for rare-earth volume: the rare-earth atom share inside the hard phase is not modelled.")
print("note: (BH)max with Ms=Mh gives the pure ceiling mu0 Ms^2/4, exceeding the single-phase hard ceiling when soft Ms > Mh (this is the Skomski-Coey result as remembered).")
print("FAILS:",fails)
