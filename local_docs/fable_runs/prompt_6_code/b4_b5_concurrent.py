"""B4, B5: life under two concurrent load cases (idealised block) and rainflow verification.

Spec rows B4, B5 (plan 3.3, rainflow routine of 3.2 in rainflow_util.py).
B4: d = 1/N(s1+s2) + (phi-1)/N(s2); tau_blk = 1/(nu1 d); ratios tau1/tau_blk,
    min(tau1,tau2)/tau_blk, tau_Miner(cases)/tau_blk.  sigma1 = 108.7 MPa (C1 value,
    taken as sigma_f' (2 N0)^b = 108.703 MPa), nu1 = 1 Hz.
    Check: tau1/tau_blk >= (1+s)^m.  This is true by construction (d contains the extra
    positive term (phi-1) s^m): flagged as an identity-type check.
B5: sigma(t) = s1 sin(2 pi nu1 t) + s2 sin(2 pi phi nu1 t) over one slow period, n_pts per fast
    period 256, 512, 1024; rainflow (periodic history, turning points cyclic); Miner damage
    variants a and b vs B4.  Aligned phi {9,33,129}, non-aligned {10,32,128}.
    'Envelope cycle dominates' (spec leaves undefined): I use envelope share
    (1/N(s1+s2))/d >= 0.5 -> recorded as ambiguity.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from p6_common import tag
from rainflow_util import SIGMA_A0, basquin_N, rainflow, damage, B

m = -1 / B
S1 = SIGMA_A0
S_LIST = [0.05, 0.1, 0.2, 0.5, 1.0]
print(f"sigma1={S1:.4f} MPa, m={m:.5f}")

print("=== B4 ===")
hand = {0.05: 1.61, 0.1: 2.55, 0.2: 5.97, 0.5: 53.3, 1.0: 894}
B4 = {}
for s in S_LIST:
    s2 = s * S1
    for phi in [9, 33, 129, 1025]:
        N1 = float(basquin_N(S1))
        d = 1 / float(basquin_N(S1 + s2)) + (phi - 1) / float(basquin_N(s2))
        tau_blk = 1 / (1.0 * d)
        tau1 = N1 / 1.0
        tau2 = float(basquin_N(s2)) / (phi * 1.0)
        tmin = min(tau1, tau2)
        tM = 1 / (1 / tau1 + 1 / tau2)
        B4[(s, phi)] = d
        lb = (1 + s) ** m
        print(f"s={s:4.2f} phi={phi:4d}: tau1/tau_blk={tau1/tau_blk:10.3f} (>= (1+s)^m={lb:9.3f}: {tau1/tau_blk>=lb*(1-1e-12)}) "
              f"tmin/tau_blk={tmin/tau_blk:9.3f} tauMiner/tau_blk={tM/tau_blk:9.3f} tau_blk/tau1={tau_blk/tau1:.4g}")
for s, h in hand.items():
    v = (1 + s) ** m
    print(f"B4 hand (1+s)^m s={s}: hand {h} calc {v:.3f} rel={abs(v-h)/h:.4f} {tag(abs(v-h)/h<0.01)}")
print("B4 identity flag: tau1/tau_blk >= (1+s)^m is an algebraic identity (tau1/tau_blk = (1+s)^m + (phi-1) s^m); "
      "the ratios are closed-form arithmetic, no independent check inside B4 (B5 is the independent check).")

print("\n=== B5 ===")
T_NPTS = [256, 512, 1024]
def history(s, phi, npts):
    n = phi * npts
    t = np.arange(n) / n
    return S1 * np.sin(2 * np.pi * t) + s * S1 * np.sin(2 * np.pi * phi * t)
all_ok = True
for aligned, phis in [("aligned", [9, 33, 129]), ("non-aligned", [10, 32, 128])]:
    for phi in phis:
        for s in S_LIST:
            d4 = B4[(s, phi)] if (s, phi) in B4 else None
            if d4 is None:
                s2 = s * S1
                d4 = 1 / float(basquin_N(S1 + s2)) + (phi - 1) / float(basquin_N(s2))
            env_share = (1 / float(basquin_N(S1 + s * S1))) / d4
            out = {}
            for npts in T_NPTS:
                cyc, res, st = rainflow(history(s, phi, npts))
                Da = damage(cyc, 'a'); Db = damage(cyc, 'b')
                amax = max(c[0] for c in cyc) / 2
                out[npts] = (len(cyc), amax, Da, Db, len(res))
            n_, amax, Da, Db, nres = out[1024]
            ch = [abs(out[T_NPTS[i+1]][2] - out[T_NPTS[i]][2]) / out[T_NPTS[i+1]][2] for i in range(2)]
            chb = [abs(out[T_NPTS[i+1]][3] - out[T_NPTS[i]][3]) / out[T_NPTS[i+1]][3] for i in range(2)]
            amp_ok = abs(amax - S1 * (1 + s)) / (S1 * (1 + s)) < 1e-3
            ratio_a = Da / d4
            dom = env_share >= 0.5
            rin = 0.7 <= ratio_a <= 1.05
            print(f"{aligned:11s} phi={phi:3d} s={s:4.2f}: n_cyc={n_} (<=phi:{n_<=phi}) residue={nres} max amp/(s1+s2)={amax/(S1*(1+s)):.5f}"
                  f"{' [aligned: within 0.1% '+tag(amp_ok)+']' if aligned=='aligned' else ''} | Da/B4={ratio_a:.4f} Db/Da={Db/Da:.4f} "
                  f"env_share={env_share:.3f}{' (dominant; in [0.7,1.05]: '+tag(rin)+')' if dom else ''} | "
                  f"dD(a) 256->512,512->1024={ch[0]:.1e},{ch[1]:.1e} {tag(ch[1]<5e-3)} dD(b)={chb[0]:.1e},{chb[1]:.1e} "
                  f"| Db>=Da {tag(Db>=Da*(1-1e-12))}")
