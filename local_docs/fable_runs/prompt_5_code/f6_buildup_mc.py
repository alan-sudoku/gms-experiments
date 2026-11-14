#!/usr/bin/env python3
"""Row F6 / Note F6 (claim G3.4): broad-beam energy buildup, C and W, 0.5 and 1 MeV, slab Monte Carlo.

Physics (Note F6): monoenergetic normal pencil beam on an infinite slab of areal density x. Compton on free electrons
(Klein-Nishina total x N_A Z/A), photoelectric absorption (NIST XCOM, log-log interpolation, each side of the W K-edge
separately), pair production zero (E <= 1.022 MeV). COHERENT SCATTERING AND FLUORESCENCE ARE NEGLECTED. Cut-off 20 keV: deposit locally.
mu in mu*x = XCOM photoelectric + KN Compton at E0 (total WITHOUT coherent, consistent with the simulation).
Compton energy sampled by rejection from f(eps) ~ (1/eps + eps - sin^2 theta), eps in [1/(1+2k), 1], cos theta = 1-(1-eps)/(k eps);
uniform azimuth; direction cosine update. Transmitted/reflected tallies are photon energies leaving through the far/near face;
absorbed = energy deposited (photoelectric absorption, Compton recoil energy, cut-off deposit).
LOOKUP: XCOM photoelectric (data/xcom_z006.csv, z074; XCOM web, access 2026-11-14), Z/A (data/nist_tab1_za.csv).
Run parameters: mu*x = 0.5 ... 12 step 0.5, N histories per case (default 1e6), fixed seed. Level `derived`.
Usage: python3 f6_buildup_mc.py [N_histories]
"""
import os, sys, math, csv, time
import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "data")
N = int(float(sys.argv[1])) if len(sys.argv) > 1 else 1_000_000
SEED = 20261114
NA = 6.02214076e23; re_cm = 2.8179403e-13; mec2 = 0.51099895; ECUT = 0.020
FAILS = []; NOTES = []

def load_pe(z):
    E=[]; V=[]
    for ln in open(os.path.join(D, "xcom_z%03d.csv" % z)):
        if ln.startswith("#") or ln.startswith("edge"): continue
        p = ln.strip().split(","); E.append(float(p[1])); V.append(float(p[4]))
    return np.array(E), np.array(V)
def za(z):
    for r in csv.DictReader(l for l in open(os.path.join(D,"nist_tab1_za.csv")) if not l.startswith("#")):
        if int(r["Z"])==z: return float(r["Z_over_A"])
MAT = {"C": 6, "W": 74}
PE = {m: load_pe(z) for m, z in MAT.items()}
def tau(m, E):
    x, y = PE[m]; E = np.asarray(E, float)
    i = np.clip(np.searchsorted(x, E, side="right") - 1, 0, len(x) - 2)
    x0, x1, y0, y1 = x[i], x[i+1], y[i], y[i+1]
    same = x1 == x0
    t = np.where(same, 1.0, (np.log(E) - np.log(x0)) / np.where(same, 1.0, np.log(x1) - np.log(x0)))
    return np.where(same, y1, np.exp(np.log(y0) + t*(np.log(y1) - np.log(y0))))
def kn_barn(E):
    k = np.asarray(E, float)/mec2
    f = (1+k)/k**2*(2*(1+k)/(1+2*k) - np.log1p(2*k)/k) + np.log1p(2*k)/(2*k) - (1+3*k)/(1+2*k)**2
    return 2*math.pi*re_cm**2*f/1e-24
def sig_c(m, E): return NA*za(MAT[m])*kn_barn(E)*1e-24      # cm2/g
def mu_tot(m, E): return tau(m, E) + sig_c(m, E)

def sample_compton(E, rng):
    k = E/mec2; emin = 1/(1+2*k); fmax = 1/emin + emin
    eps = np.empty_like(E); todo = np.arange(len(E))
    while len(todo):
        e = emin[todo] + (1-emin[todo])*rng.random(len(todo))
        c = 1 - (1-e)/(k[todo]*e); s2 = np.maximum(0, 1-c*c)
        f = 1/e + e - s2
        ok = rng.random(len(todo))*fmax[todo] < f
        eps[todo[ok]] = e[ok]; todo = todo[~ok]
    return eps

def run(m, E0, X, scatter, rng):
    E = np.full(N, E0); u = np.ones(N); z = np.zeros(N); idx = np.arange(N)
    Tt = np.zeros(N); Rsum = 0.0; Asum = 0.0
    n_int = 0
    while len(idx):
        mu = mu_tot(m, E)
        z = z + (-np.log(rng.random(len(idx)))/mu)*u
        far = z >= X; near = z <= 0.0
        Tt[idx[far]] = E[far]; Rsum += E[near].sum()
        keep = ~(far | near)
        idx, E, u, z, mu = idx[keep], E[keep], u[keep], z[keep], mu[keep]
        if not len(idx): break
        n_int += len(idx)
        pe = rng.random(len(idx)) < tau(m, E)/mu
        if not scatter: pe[:] = True
        Asum += E[pe].sum()
        cm = ~pe
        idx, E, u, z = idx[cm], E[cm], u[cm], z[cm]
        if not len(idx): break
        eps = sample_compton(E, rng); k = E/mec2
        c = np.clip(1-(1-eps)/(k*eps), -1, 1); s = np.sqrt(1-c*c)
        En = eps*E; Asum += (E-En).sum()
        phi = 2*math.pi*rng.random(len(idx))
        un = np.clip(u*c + np.sqrt(np.maximum(0, 1-u*u))*s*np.cos(phi), -1, 1)
        cut = En < ECUT
        Asum += En[cut].sum()
        keep = ~cut
        idx, E, u, z = idx[keep], En[keep], un[keep], z[keep]
    Tsum = Tt.sum()
    # per-history transmitted energy fraction: mean and standard error
    t = Tt/E0
    return dict(T=t.mean(), Terr=t.std(ddof=1)/math.sqrt(N), R=Rsum/E0/N, A=Asum/E0/N, nint=n_int)

def check(name, ok, detail):
    print("  [%s] %s: %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok: FAILS.append(name)

print("F6 run: N=%d histories per case, seed=%d, mu*x = 0.5..12 step 0.5, cut-off %.0f keV" % (N, SEED, ECUT*1000))
print("NEGLECTED: coherent scattering, fluorescence, bremsstrahlung, electron transport (recoil/photo-electron energy deposited locally).")
print("LOOKUP: photoelectric from data/xcom_z006.csv (C) and data/xcom_z074.csv (W), NIST XCOM web, access 2026-11-14; Z/A from data/nist_tab1_za.csv")
# sampler self-test against closed-form KN mean scattered energy fraction
rng0 = np.random.default_rng(np.random.SeedSequence([SEED, 0]))
for E0 in (0.5, 1.0):
    k = E0/mec2
    def dsig(c):   # KN dsigma/dOmega per sin(theta) measure, eps(c)
        eps = 1/(1+k*(1-c)); return eps**2*(eps+1/eps-(1-c*c))
    num = quad(lambda c: dsig(c)/(1+k*(1-c)), -1, 1)[0]; den = quad(dsig, -1, 1)[0]
    Es = sample_compton(np.full(2_000_000, E0), rng0)
    se = Es.std(ddof=1)/math.sqrt(len(Es))
    check("Compton sampler: mean scattered-photon fraction at %g MeV vs numerical KN integral (4 sigma)" % E0, abs(Es.mean()-num/den) < 4*se, "MC %.5f +- %.5f, quad %.5f" % (Es.mean(), se, num/den))
print("\nmu (cm2/g, no coherent) at E0 and XCOM total without coherent:")
Xnc = {}
for m, z in MAT.items():
    Xnc[m] = {}
    for ln in open(os.path.join(D, "xcom_z%03d.csv" % z)):
        if ln.startswith("#") or ln.startswith("edge"): continue
        p = ln.strip().split(","); Xnc[m][round(float(p[1]), 6)] = float(p[8])
for m in MAT:
    for E0 in (0.5, 1.0):
        mt = float(mu_tot(m, E0)); ref = Xnc[m][round(E0, 6)]
        print("  %s %.1f MeV: mu = tau %.5g + KN %.5g = %.5g; XCOM total w/o coherent %.5g (diff %+.2f%%; XCOM total includes pair/triplet = 0 here)" % (m, E0, float(tau(m, E0)), float(sig_c(m, E0)), mt, ref, 100*(mt/ref-1)))
        print("    [info, not a spec check] free-electron KN differs from XCOM (which includes binding via the scattering function) by %+.2f%%; the spec prescribes free-electron KN and this mu is used throughout" % (100*(mt/ref-1)))
MUX = np.arange(0.5, 12.0001, 0.5)
RES = {}; t0 = time.time()
for m in MAT:
    for E0 in (0.5, 1.0):
        mu0 = float(mu_tot(m, E0))
        rows = []
        for j, mx in enumerate(MUX):
            rng = np.random.default_rng(np.random.SeedSequence([SEED, 1, ord(m[0]), int(E0*1000), j]))
            r = run(m, E0, mx/mu0, True, rng)
            r["mx"] = mx; r["B"] = r["T"]/math.exp(-mx); r["Berr"] = r["Terr"]/math.exp(-mx)
            r["bal"] = r["T"] + r["R"] + r["A"]
            rows.append(r)
        RES[(m, E0)] = rows
        print("  done %s %.1f MeV (elapsed %.0f s)" % (m, E0, time.time()-t0), flush=True)
print("\n=== Results: T_E (transmitted energy fraction), B_E = T_E/exp(-mu x), R (reflected), A (absorbed), balance T+R+A ===")
worst_bal = 0
for (m, E0), rows in RES.items():
    print("\n%s %.1f MeV  (mu = %.5g cm2/g)" % (m, E0, float(mu_tot(m, E0))))
    print("   mu*x    T_E          +-         B_E      +-        R         A        T+R+A-1")
    for r in rows:
        worst_bal = max(worst_bal, abs(r["bal"]-1))
        print("  %5.1f  %.5e  %.1e  %8.4f  %.1e  %.5f  %.5f  %+.1e" % (r["mx"], r["T"], r["Terr"], r["B"], r["Berr"], r["R"], r["A"], r["bal"]-1))
print("\n--- Checks ---")
check("(ii) energy balance T+R+A = 1 to 1e-9 in all %d cases [bookkeeping check (identity-like): A is summed from deposits, T and R from exits; it fails only if photons are lost or duplicated]" % len(RES), worst_bal < 1e-9, "max |T+R+A-1| = %.2e" % worst_bal)
# (i) absorption-only
nfail = 0; ncase = 0; zmax = 0
for m in MAT:
    for E0 in (0.5, 1.0):
        mu0 = float(mu_tot(m, E0))
        for j, mx in enumerate(MUX):
            rng = np.random.default_rng(np.random.SeedSequence([SEED, 2, ord(m[0]), int(E0*1000), j]))
            r = run(m, E0, mx/mu0, False, rng)
            ncase += 1; z = abs(r["T"]-math.exp(-mx))/r["Terr"]; zmax = max(zmax, z)
            if z > 3: nfail += 1
print("  (i) scattering replaced by absorption: T_E vs exp(-mu x): %d cases, %d outside 3 sigma (chance expectation %.2f), max |z| = %.2f" % (ncase, nfail, 0.0027*ncase, zmax))
check("(i) T_E = exp(-mu x) within 3 sigma (<= 1 chance excursion allowed)", nfail <= 1, "%d/%d" % (nfail, ncase))
# (iii)
bad = []; amb = []
for j, mx in enumerate(MUX):
    for E0 in (0.5, 1.0):
        c = RES[("C", E0)][j]; w = RES[("W", E0)][j]
        d = c["B"]-w["B"]; se = math.hypot(c["Berr"], w["Berr"])
        if d <= 0: bad.append((E0, mx, d))
        elif d < 3*se: amb.append((E0, mx, d/se))
check("(iii) B_C > B_W at every mu x (both energies)", not bad, "violations %s; differences within 3 sigma of zero at %s" % (bad, amb))
# targets
print("\n--- Areal densities for T_E = 1e-2 and 1e-3 (PCHIP of ln T_E vs mu*x, brentq; +-1 sigma by shifting T_E data) ---")
XT = {}
for (m, E0), rows in RES.items():
    mu0 = float(mu_tot(m, E0)); lx = np.array([r["mx"] for r in rows]); lt = np.log([r["T"] for r in rows])
    for tgt in (1e-2, 1e-3):
        # bracket check
        br = (lt[0] > math.log(tgt)) and (lt[-1] < math.log(tgt))
        f = PchipInterpolator(lx, lt)
        root = brentq(lambda x: f(x)-math.log(tgt), lx[0], lx[-1], xtol=1e-12) if br else float("nan")
        # statistical error: shift ln T by +-sigma_lnT around the root (local, pointwise)
        i = int(np.searchsorted(lx, root)); sig = rows[min(i, len(rows)-1)]["Terr"]/rows[min(i, len(rows)-1)]["T"]
        slope = float(f(root, 1)) if br else float("nan")
        err = sig/abs(slope) if br else float("nan")
        XT[(m, E0, tgt)] = (root, err, root/mu0)
        print("  %s %.1f MeV  T_E=%g: mu*x = %.4f +- %.4f (bracketed by sweep: %s); areal density x = %.4f g/cm2" % (m, E0, tgt, root, err, br, root/mu0))
        if not br: NOTES.append("%s %.1f MeV target %g not bracketed by mu*x in 0.5..12" % (m, E0, tgt))
print("\n--- Areal-density ratio x_C/x_W for equal transmitted energy ---")
for E0 in (0.5, 1.0):
    for tgt in (1e-2, 1e-3):
        c = XT[("C", E0, tgt)]; w = XT[("W", E0, tgt)]
        r = c[2]/w[2]; er = r*math.hypot(c[1]/c[0], w[1]/w[0])
        # narrow-beam ratio for comparison: x = ln(1/tgt)/mu
        mc, mw = float(mu_tot("C", E0)), float(mu_tot("W", E0))
        nb = (math.log(1/tgt)/mc)/(math.log(1/tgt)/mw)
        print("  E=%.1f MeV T_E=%g: x_C/x_W = %.4f +- %.4f   (narrow-beam ratio mu_W/mu_C = %.4f)" % (E0, tgt, r, er, nb))
        if E0 == 1.0:
            check("x_C/x_W at 1 MeV, T_E=%g in UNSURE range 1.1-1.4" % tgt, 1.1 <= r <= 1.4, "%.4f" % r)
print("\n(iv) LOOKUP of exposure buildup factors (ANSI/ANS-6.4.3-1991 via Shultis and Faw 2000): NOT RUN here, see outputs/issues_b.md (source not reachable / not recorded).")
print("Total runtime %.0f s. Sweep brackets: %s" % (time.time()-t0, NOTES if NOTES else "all four (material, E) sweeps bracket both targets"))
print("FAILED CHECKS:", FAILS if FAILS else "none")
