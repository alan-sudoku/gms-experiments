"""Shared models for Prompt 1b (stage S2).  Level: derived (unverified).

Purpose: common inputs (plan section 3.0) and the models of section 3.1:
M-PF (plate fins), M-PIN (staggered pin fins), M-GYR (homogenised gyroid),
M-SP (base spreading), M-ENT (entropy by mechanism), plus the V-dot solver,
design sweeps and small check/print helpers.  Every formula is implemented as
written in the plan, including constants the plan marks UNSURE.

Not a row script: imported by the row scripts in this folder.
Assumptions: constant air properties; numpy and standard library only.
Lines starting with 'ISSUE:' in script output are collected into issues.md.
"""
import math
import os
import sys

import numpy as np

# ---------------------------------------------------------------- inputs 3.0
Q = 100.0
W = 0.060
L = 0.060
H = 0.030
TB = 0.005
T0 = 298.15
P0 = 101325.0
RHO = 1.1614
CP = 1007.0
MU = 1.846e-5
KA = 0.0263
PR = 0.707
RAIR = 287.05
ALPHA_A = KA / (RHO * CP)
K_CU = 390.0
K_AL_SET = [100, 120, 150, 180, 200]
RHO_CU = 8960.0
RHO_AL = 2670.0
P_SET = [0.01, 0.03, 0.1, 0.3, 1.0]
ETA_FAN = 0.25
TAU_LIFE = 1.578e8
FAN_A, FAN_V = 60.0, 0.012
A_S = 4.0e-4
F_CONST = 96485.33
R_GAS = 8.314462
J_EC = 1.0e4
CU_T = [0.3e-3, 0.4e-3, 0.5e-3, 0.6e-3, 0.8e-3, 1.0e-3]
AL_T = [0.4e-3, 0.5e-3, 0.6e-3, 0.8e-3, 1.0e-3, 1.2e-3, 1.5e-3, 2.0e-3]
S_MIN = 0.8e-3
PIN_D = [1.0e-3, 1.5e-3, 2.0e-3, 3.0e-3]
PIN_P = [1.5, 1.75, 2.0, 2.5, 3.0]
GY_A = [3e-3, 4e-3, 5e-3, 6e-3, 8e-3, 10e-3, 12e-3, 15e-3]
GY_RHO = [0.15, 0.20, 0.30]
S_G = 3.0915


def rho_s(k):
    return RHO_CU if k >= 390 else RHO_AL


# ------------------------------------------------------------------ helpers
def issue(msg):
    print("ISSUE: " + msg)


def check(label, cond, detail=""):
    print(("PASS  " if cond else "FAIL  ") + label + ("  | " + detail if detail else ""))
    if not cond:
        issue("FAIL " + label + " | " + detail)
    return cond


def rng(label, val, lo, hi):
    ok = lo <= val <= hi
    print(("RANGE-OK    " if ok else "RANGE-MISS  ") + "%s = %.6g (hand range %.6g to %.6g)" % (label, val, lo, hi))
    if not ok:
        issue("hand-range miss %s = %.6g, range %.6g to %.6g" % (label, val, lo, hi))
    return ok


def info(label, detail=""):
    print("INFO  " + label + ("  | " + detail if detail else ""))


def head(txt):
    print("\n=== " + txt + " ===")


def print_inputs(**kw):
    print("Inputs used: " + ", ".join("%s=%s" % (k, v) for k, v in kw.items()))


# -------------------------------------------------------------- V-dot solver
def solve_V(dpf, P, lo=1e-6, hi=0.2, tol=1e-8):
    """Bisection on V in [lo, hi] for V*dP(V) = P, relative tolerance tol."""
    if lo * dpf(lo) > P or hi * dpf(hi) < P:
        return None
    while (hi - lo) > tol * 0.5 * (hi + lo):
        mid = 0.5 * (lo + hi)
        if mid * dpf(mid) < P:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def close_thermal(G, V, k, Rb1d_k=None):
    """(X1), (X2). Returns dict of closure quantities."""
    C = RHO * V * CP
    NTU = G / C
    Rfa = 1.0 / (C * (1.0 - math.exp(-NTU)))
    dT = Q / C
    return dict(C=C, NTU=NTU, R_fa=Rfa, invC=1.0 / C, dT=dT, T_out=T0 + dT,
                T_root=T0 + Q * Rfa, G=G, Rb1d=TB / (k * W * L))


# ----------------------------------------------------- M-PF low-level pieces
def pf_dp_u(s, Hh, Ll, u, Kc=None, Ke=None, sigma=None):
    """(PF3)-(PF7).  Kc, Ke given explicitly override sigma-based values."""
    Dh = 2 * s * Hh / (s + Hh)
    Re = RHO * u * Dh / MU
    b = s / Hh
    fRe = 24 * (1 - 1.3553 * b + 1.9467 * b ** 2 - 1.7012 * b ** 3 + 0.9564 * b ** 4 - 0.2537 * b ** 5)
    Lp = Ll / (Dh * Re)
    fapp = math.sqrt((3.44 / math.sqrt(Lp)) ** 2 + fRe ** 2) / Re
    if Kc is None:
        Kc = 0.42 * (1 - sigma ** 2)
    if Ke is None:
        Ke = (1 - sigma ** 2) ** 2
    return (4 * fapp * Ll / Dh + Kc + Ke) * RHO * u * u / 2, Re, fapp


def pf_nu(Ll, s, u):
    """(PF8)."""
    Repp = RHO * u * 2 * s / MU
    xs = Ll / (2 * s * Repp * PR)
    return 7.55 + 0.024 * xs ** -1.14 / (1 + 0.0358 * PR ** 0.17 * xs ** -0.64)


def pf_teertstra_nu(Ll, s, u):
    """(PF12)."""
    Reb = RHO * u * s / MU
    Rbs = Reb * s / Ll
    return ((Rbs * PR / 2) ** -3 + (0.664 * math.sqrt(Rbs) * PR ** (1 / 3) * math.sqrt(1 + 3.65 / math.sqrt(Rbs))) ** -3) ** (-1 / 3)


# ----------------------------------------------------------------- designs
class PF:
    kind = "PF"

    def __init__(self, t, Nf, k):
        self.t, self.Nf, self.k = t, Nf, k
        self.Nch = Nf - 1
        self.s = (W - Nf * t) / self.Nch
        self.Aflow = self.Nch * self.s * H
        self.sigma = self.Nch * self.s / W
        self.hydkey = ("PF", t, Nf)
        self.sweepkey = (t, Nf)
        self.valid = self.s > 0

    def label(self):
        return "PF t=%.2fmm Nf=%d s=%.3fmm k=%g" % (self.t * 1e3, self.Nf, self.s * 1e3, self.k)

    def dp(self, V):
        return pf_dp_u(self.s, H, L, V / self.Aflow, sigma=self.sigma)[0]

    def eval(self, V):
        u = V / self.Aflow
        dP, Re, fapp = pf_dp_u(self.s, H, L, u, sigma=self.sigma)
        Nu = pf_nu(L, self.s, u)
        h = Nu * KA / (2 * self.s)
        m = math.sqrt(2 * h / (self.k * self.t))
        eta = math.tanh(m * H) / (m * H)
        Afin = 2 * self.Nch * H * L
        Abase = self.Nch * self.s * L
        G = h * (eta * Afin + Abase)
        r = close_thermal(G, V, self.k)
        # PF12
        Nut = pf_teertstra_nu(L, self.s, u)
        hT = Nut * KA / self.s
        mT = math.sqrt(2 * hT / (self.k * self.t))
        etaT = math.tanh(mT * H) / (mT * H)
        RfaT = 1.0 / (hT * (etaT * Afin + Abase))
        r.update(V=V, u=u, Re=Re, dP=dP, P_air=V * dP, Nu=Nu, h=h, m=m, eta=eta, A_f=Afin, A_b=Abase,
                 mass=rho_s(self.k) * (self.Nf * self.t * H * L + W * L * TB), R_faT=RfaT, hT=hT, etaT=etaT,
                 excluded=Re >= 2300, flags="Re>=2300" if Re >= 2300 else "", s=self.s)
        return r


class PIN:
    kind = "PIN"

    def __init__(self, d, p, k, fric="min", nu="K"):
        self.d, self.p, self.k, self.fric, self.nu = d, p, k, fric, nu
        self.ST = self.SL = p * d
        self.NT = int(math.floor(W / self.ST + 1e-9))
        self.NL = int(math.floor(L / self.SL + 1e-9))
        self.N = self.NT * self.NL
        self.hydkey = ("PIN", d, p, fric)
        self.sweepkey = (d, p)
        self.valid = self.N > 0

    def label(self):
        return "PIN d=%.1fmm p=%.2f N=%d(NT=%d,NL=%d) k=%g fric=%s nu=%s" % (
            self.d * 1e3, self.p, self.N, self.NT, self.NL, self.k, self.fric, self.nu)

    def _Re(self, V):
        Uapp = V / (W * H)
        Umax = Uapp * self.ST / (self.ST - self.d)
        return Umax, RHO * Umax * self.d / MU

    def f_K(self, Re):
        p = self.p
        K1 = 1.175 * (self.SL / (self.ST * Re ** 0.3124)) + 0.5 * Re ** 0.0807
        return K1 * (378.6 / p ** (13.1 / p)) / Re ** (0.68 / p ** 1.29)

    def f_J(self, Re):
        return 4 * (0.25 + 0.118 / ((self.ST - self.d) / self.d) ** 1.08) * Re ** -0.16

    def dp(self, V):
        Umax, Re = self._Re(V)
        if self.fric == "K":
            f = self.f_K(Re)
        elif self.fric == "J":
            f = self.f_J(Re)
        else:
            f = min(self.f_K(Re), self.f_J(Re))
        return self.NL * f * RHO * Umax ** 2 / 2

    def Nu_K(self, Re):
        p = self.p
        C1 = 0.61 * p ** 0.091 * p ** 0.053 / (1 - 2 * math.exp(-1.09 * p))
        return C1 * Re ** 0.5 * PR ** (1 / 3)

    def Nu_Z(self, Re):
        if Re < 500:
            return 1.04 * Re ** 0.4 * PR ** 0.36
        if Re < 1000:
            return 0.71 * Re ** 0.5 * PR ** 0.36
        return 0.35 * (self.ST / self.SL) ** 0.2 * Re ** 0.6 * PR ** 0.36

    def eval(self, V):
        Umax, Re = self._Re(V)
        dP = self.dp(V)
        Nu = self.Nu_K(Re) if self.nu == "K" else self.Nu_Z(Re)
        h = Nu * KA / self.d
        m = math.sqrt(4 * h / (self.k * self.d))
        eta = math.tanh(m * H) / (m * H)
        Apin = math.pi * self.d * H * self.N
        Abase = W * L - self.N * math.pi * self.d ** 2 / 4
        G = h * (eta * Apin + Abase)
        r = close_thermal(G, V, self.k)
        fl = []
        if Re < 40 or Re > 1000:
            fl.append("Re_d outside 40-1000")
        if self.NL < 10:
            fl.append("N_L<10")
        r.update(V=V, u=Umax, Re=Re, dP=dP, P_air=V * dP, Nu=Nu, h=h, m=m, eta=eta, A_f=Apin, A_b=Abase,
                 mass=rho_s(self.k) * (self.N * math.pi * self.d ** 2 / 4 * H + W * L * TB),
                 excluded=False, flags="; ".join(fl), fK=self.f_K(Re), fJ=self.f_J(Re))
        return r


class GY:
    kind = "GY"

    def __init__(self, a, rho_bar, k, cf, chi):
        self.a, self.rb, self.k, self.cf, self.chi = a, rho_bar, k, cf, chi
        self.ts = rho_bar * a / S_G
        self.valid = self.ts >= 0.3e-3
        self.asf = 2 * S_G / a
        self.phi = 1 - rho_bar
        self.Dh = 4 * self.phi / self.asf
        self.Aflow = self.phi * W * H
        self.hydkey = ("GY", a, rho_bar, cf)
        self.sweepkey = (a, rho_bar)

    def label(self):
        return "GY a=%.0fmm rho=%.2f ts=%.3fmm k=%g cf=%g chi=%g" % (self.a * 1e3, self.rb, self.ts * 1e3, self.k, self.cf, self.chi)

    def fD(self, Re):
        return self.cf * (133.33 / Re + 2.333)

    def dp(self, V):
        u = V / self.Aflow
        Re = RHO * u * self.Dh / MU
        return self.fD(Re) * (L / self.Dh) * RHO * u * u / 2

    def eval(self, V):
        u = V / self.Aflow
        Re = RHO * u * self.Dh / MU
        fD = self.fD(Re)
        dP = fD * (L / self.Dh) * RHO * u * u / 2
        h = self.chi * (fD / 4) * RHO * u * CP * PR ** (-2 / 3)
        keff = self.k * 2 * self.rb / (3 - self.rb)
        m = math.sqrt(h * self.asf / keff)
        eta = math.tanh(m * H) / (m * H)
        Awet = self.asf * W * L * H
        Ab = self.phi * W * L
        G = h * (eta * Awet + Ab)
        r = close_thermal(G, V, self.k)
        fl = "homogenisation doubtful (H/a=%.2f<3)" % (H / self.a) if H / self.a < 3 else ""
        r.update(V=V, u=u, Re=Re, dP=dP, P_air=V * dP, h=h, m=m, eta=eta, A_f=Awet, A_b=Ab, keff=keff,
                 mass=rho_s(self.k) * (self.rb * W * L * H + W * L * TB), excluded=False, flags=fl, ts=self.ts)
        return r


# ------------------------------------------------------------ design sweeps
def plate_designs(k):
    ts = CU_T if k >= 390 else AL_T
    out = []
    for t in ts:
        Nf = 6
        while (W - Nf * t) / (Nf - 1) >= S_MIN:
            out.append(PF(t, Nf, k))
            Nf += 1
    return out


def pin_designs(k, fric="min", nu="K"):
    return [PIN(d, p, k, fric, nu) for d in PIN_D for p in PIN_P]


def gy_designs(k, cf, chi):
    return [GY(a, r, k, cf, chi) for a in GY_A for r in GY_RHO if r * a / S_G >= 0.3e-3]


_VC = {}


def V_at_P(design, P):
    key = (design.hydkey, P)
    if key not in _VC:
        _VC[key] = solve_V(design.dp, P)
    return _VC[key]


def ranked(designs, P):
    """All valid, non-excluded designs at fan power P, sorted by R_fa."""
    out = []
    for d in designs:
        if not d.valid:
            continue
        V = V_at_P(d, P)
        if V is None:
            continue
        r = d.eval(V)
        if r["excluded"]:
            continue
        out.append((r["R_fa"], r, d))
    out.sort(key=lambda x: x[0])
    return out


def best(designs, P):
    rk = ranked(designs, P)
    return rk[0] if rk else None


def boundary_notes(design, kind, k=None):
    """Report whether a winner sits on a sweep boundary."""
    notes = []
    if kind == "PF":
        ts = CU_T if design.k >= 390 else AL_T
        if design.t == ts[0]:
            notes.append("t at sweep minimum")
        if design.t == ts[-1]:
            notes.append("t at sweep maximum")
        if (W - (design.Nf + 1) * design.t) / design.Nf < S_MIN:
            notes.append("s at 0.8 mm limit (next N_f violates)")
        if design.Nf == 6:
            notes.append("N_f at lower sweep start (6)")
    elif kind == "PIN":
        if design.d in (PIN_D[0], PIN_D[-1]):
            notes.append("d on sweep edge")
        if design.p in (PIN_P[0], PIN_P[-1]):
            notes.append("p on sweep edge")
    elif kind == "GY":
        if design.a in (GY_A[0], GY_A[-1]):
            notes.append("a on sweep edge")
        if design.rb in (GY_RHO[0], GY_RHO[-1]):
            notes.append("rho on sweep edge")
    return notes


def print_top3(title, designs, P, kind):
    rk = ranked(designs, P)
    if not rk:
        print("%s: no valid design" % title)
        return None
    print("%s  P_air=%g W" % (title, P))
    for i, (R, r, d) in enumerate(rk[:3]):
        tag = ("WINNER   ", "runner-up", "runner-up")[i]
        print("   %s R_fa=%.4f K/W V=%.4e dP=%.3f Re=%.1f eta=%.3f NTU=%.3f dT=%.2f mass=%.4f kg  %s %s" % (
            tag, R, r["V"], r["dP"], r["Re"], r["eta"], r["NTU"], r["dT"], r["mass"], d.label(), r["flags"]))
    bn = boundary_notes(rk[0][2], kind)
    print("   winner boundary: " + ("; ".join(bn) if bn else "interior of sweep"))
    return rk[0]


# --------------------------------------------------------------- M-SP model
def sp_ab(a_s, b_p, tb, k, R0):
    eps = a_s / b_p
    tau = tb / b_p
    Bi = 1.0 / (math.pi * k * b_p * R0)
    lam = math.pi + 1 / (math.sqrt(math.pi) * eps)
    th = math.tanh(lam * tau)
    Phi = (th + lam / Bi) / (1 + (lam / Bi) * th)
    sp = math.sqrt(math.pi)
    psi_max = eps * tau / sp + (1 - eps) * Phi / sp
    psi_avg = eps * tau / sp + 0.5 * (1 - eps) ** 1.5 * Phi
    return psi_max / (sp * k * a_s), psi_avg / (sp * k * a_s)


def sp_area(A_s, A_p, tb, k, R0):
    return sp_ab(math.sqrt(A_s / math.pi), math.sqrt(A_p / math.pi), tb, k, R0)


# -------------------------------------------------------------- M-ENT model
def entropy(res, P_air=0.1, eta_fan=ETA_FAN, n=400):
    """(EN1)-(EN11) for a solved design result dict (case U)."""
    h, m, NTU, C = res["h"], res["m"], res["NTU"], res["C"]
    Af, Ab, Troot, Tout = res["A_f"], res["A_b"], res["T_root"], res["T_out"]
    Tin = T0
    x = (np.arange(n) + 0.5) * L / n
    z = (np.arange(n) + 0.5) * H / n
    dx, dz = L / n, H / n
    Tair = Tin + (Troot - Tin) * (1 - np.exp(-NTU * x / L))
    Tw = Tair[:, None] + (Troot - Tair[:, None]) * np.cosh(m * (H - z[None, :])) / np.cosh(m * H)
    qf = h * (Tw - Tair[:, None])
    dAf = Af / (L * H) * dx * dz
    qb = h * (Troot - Tair)
    dAb = Ab / L * dx
    Qnum = qf.sum() * dAf + qb.sum() * dAb
    Sfilm = (qf * (1 / Tair[:, None] - 1 / Tw)).sum() * dAf + (qb * (1 / Tair - 1 / Troot)).sum() * dAb
    Sfin = (qf * (1 / Tw - 1 / Troot)).sum() * dAf
    Thot = Troot + Q * res["Rb1d"]
    Sbase = Q * (1 / Troot - 1 / Thot)
    Smix = C * ((Tout - T0) / T0 - math.log(Tout / T0))
    Spump = P_air / T0
    Sfl = P_air * (1 / eta_fan - 1) / T0
    Sth = Q * (1 / T0 - 1 / Thot)
    Sdev = Q / Thot
    Tlm = (Tout - Tin) / math.log(Tout / Tin)
    Tmean = 0.5 * (Tin + Tout)
    E = {nm: Q * (1 / Tc - 1 / Thot) + P_air / T0 for nm, Tc in (("T0", T0), ("Tmean", Tmean), ("Tlm", Tlm))}
    return dict(Qnum=Qnum, Sfilm=Sfilm, Sfin=Sfin, Thot=Thot, Sbase=Sbase, Smix=Smix, Spump=Spump,
                Sfanloss=Sfl, Sth=Sth, Sdev=Sdev, Tlm=Tlm, E=E,
                stream=C * math.log(Tout / Tin) - Q / Troot)


def lnfit_slope(xs, ys):
    lx = np.log(xs)
    ly = np.log(ys)
    return float(np.polyfit(lx, ly, 1)[0])


# --------------------------------------------- shared study helpers (B10-B13, B20)
def arch_designs(name):
    """Design lists for the architectures used by B10-B13, B15, B16, B19, B20."""
    table = {
        "Cu plate": lambda: plate_designs(390.0),
        "Al plate k=100": lambda: plate_designs(100.0),
        "Al plate k=150": lambda: plate_designs(150.0),
        "Al plate k=180": lambda: plate_designs(180.0),
        "Al plate k=200": lambda: plate_designs(200.0),
        "Al pin k=150 fav": lambda: pin_designs(150.0, "min", "K"),
        "Gyroid ks=150 cf=0.3 chi=0.2": lambda: gy_designs(150.0, 0.3, 0.2),
        "Gyroid ks=150 cf=1.0 chi=0.1": lambda: gy_designs(150.0, 1.0, 0.1),
    }
    return table[name]()


def min_R(designs, P):
    b = best(designs, P)
    return b[0] if b else float("inf")


def required_power(designs, target, lo=0.01, hi=30.0, rtol=1e-3):
    """Bisection on ln P for min_R(P) = target, re-optimising the design at each P.
    Designs with Re >= 2300 are excluded, so min_R can become infinite at high P; the upper end is then
    lowered to the largest P on a 200-point log grid where a design survives (noted in the return text).
    Returns (P_req or None, note)."""
    note_extra = ""
    if min_R(designs, hi) == float("inf"):
        grid = [math.exp(math.log(lo) + (math.log(hi) - math.log(lo)) * i / 199) for i in range(200)]
        fin = [P for P in grid if min_R(designs, P) < float("inf")]
        hi = fin[-1]
        note_extra = " [upper bound lowered to %.3f W: no design with Re<2300 and a V root inside [1e-6, 0.2] m3/s above it]" % hi
    if min_R(designs, hi) > target:
        return None, "not reachable: min R_fa at %.3f W = %.4f > target %.4f%s" % (hi, min_R(designs, hi), target, note_extra)
    if min_R(designs, lo) <= target:
        return lo, "target already met at lower bound %.3g W" % lo
    a, b = math.log(lo), math.log(hi)
    while (b - a) > rtol:
        mid = 0.5 * (a + b)
        if min_R(designs, math.exp(mid)) > target:
            a = mid
        else:
            b = mid
    return math.exp(0.5 * (a + b)), "ok" + note_extra


def solve_fan_point(design, a=FAN_A, vmax=FAN_V, tol=1e-8):
    """dP_sink(V) = a*(1 - V/vmax) by bisection on V in (0, vmax)."""
    lo, hi = 1e-9, vmax
    f = lambda V: design.dp(V) - a * (1 - V / vmax)
    if f(lo) > 0 or f(hi) < 0:
        return None
    while (hi - lo) > tol * 0.5 * (hi + lo):
        mid = 0.5 * (lo + hi)
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)
