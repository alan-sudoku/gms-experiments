"""Prompt 6 review (S5), script 1: independent recomputation of the headline numbers.

Level `derived` (unverified). Independent of prompt_6_code: no import from it. Coupled lives are
obtained by ODE integration with an event (scipy solve_ivp), not by the closed forms; maxima by
bounded scalar optimisation; roots by brentq. Inputs restated from prompt_6_answer.md section 2.

Run: <gms-local>/.venv/bin/python rv01_core_independent.py > outputs/rv01_core_independent.txt
"""
import math
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq, minimize_scalar

SIGF, N0, NU, YR = 900.0, 5e8, 1.0, 3.15576e7
TAU0 = N0 / NU / YR


def life_linear(rho, q):
    """u_fail = tau/t_c for dD/du = (1/rho)(1-u)^-q, D(u_fail) = 1, by ODE + event. inf if none before u=1."""
    ev = lambda u, D: D[0] - 1.0
    ev.terminal, ev.direction = True, 1
    f = lambda u, D: [(1.0 / rho) * (1.0 - u) ** (-q)]
    sol = solve_ivp(f, (0.0, 1.0 - 1e-12), [0.0], events=ev, rtol=1e-11, atol=1e-14, method="LSODA")
    return sol.t_events[0][0] if len(sol.t_events[0]) else math.inf


def life_parabolic(rho, q):
    """Parabolic recession x = sqrt(u): dD/du = (1/rho)(1-sqrt(u))^-q."""
    ev = lambda u, D: D[0] - 1.0
    ev.terminal, ev.direction = True, 1
    f = lambda u, D: [(1.0 / rho) * (1.0 - math.sqrt(u)) ** (-q)]
    sol = solve_ivp(f, (0.0, 1.0 - 1e-12), [0.0], events=ev, rtol=1e-11, atol=1e-14, method="LSODA")
    return sol.t_events[0][0] if len(sol.t_events[0]) else math.inf


def fmin(rho, q, law):
    u = law(rho, q)
    return min(rho, 1.0) / u


def fmax_over_rho(q, law):
    r = minimize_scalar(lambda lr: -fmin(10 ** lr, q, law), bounds=(-3, 3), method="bounded", options={"xatol": 1e-7})
    return -r.fun, 10 ** r.x


def m_lin_quad(xe, p):
    return quad(lambda x: (1 - x) ** (-p), 0, xe, epsabs=1e-14)[0] / xe


print("rv01: independent recomputation (ODE+event, brentq, bounded optimisation). Level derived.")
res = {}
for b in (-0.102, -0.124):
    m = -1.0 / b
    sig = SIGF * (2 * N0) ** b
    R = {"m": m, "sig": sig}
    print("\n" + "=" * 90 + "\nb = %.3f  m = %.4f  sigma_a0 = %.4f MPa  tau0 = %.4f yr" % (b, m, sig, TAU0))

    # --- section-loss worst case, linear and parabolic recession, p = 1, 2, 3
    for p, lab in ((1, "wall, membrane (p=1)"), (2, "round strut axial / wall bending (p=2)"), (3, "round strut bending or torsion (p=3)")):
        fl, rl = fmax_over_rho(p * m, life_linear)
        fp, rp = fmax_over_rho(p * m, life_parabolic)
        R["lin%d" % p], R["par%d" % p] = fl, fp
        print("[sec] %-40s q=%7.3f  linear: max F_min = %.4f at rho = %.4f | parabolic: max F_min = %.4f at rho = %.4f" % (lab, p * m, fl, rl, fp, rp))
    print("[sec] parabolic, q = m, F_min at rho = 0.01, 0.1, 1, 10: " + ", ".join("%.3f" % fmin(r, m, life_parabolic) for r in (0.01, 0.1, 1, 10)))

    # --- worked pair
    tcg, tcs = 15.0, 300.0
    ug, us = life_linear(TAU0 / tcg, 2 * m), life_linear(TAU0 / tcs, m)
    Fg, Fs = TAU0 / (ug * tcg), TAU0 / (us * tcs)
    R.update(Fg=Fg, Fs=Fs)
    ve = {w: (w * Fg + 1 - w) / (w * Fs + 1 - w) for w in (1.0, 0.5, 0.1)}
    print("[pair] g: x_e = %.5f F_cur = %.4f ; s: x_e = %.5f F_cur = %.4f ; verdict error w=1/0.5/0.1: %.4f / %.4f / %.4f"
          % (ug, Fg, us, Fs, ve[1.0], ve[0.5], ve[0.1]))
    R.update(ve1=ve[1.0], ve05=ve[0.5])

    # --- lower bound and margin
    rho_g = TAU0 / tcg
    xs = brentq(lambda x: x - rho_g * (1 - x) ** (2 * m), 0, 1, xtol=1e-15)
    cU = 0.5 * TAU0 / (xs * tcg) + 0.5 * (1 - ug) ** -2
    ctrue = 0.5 * Fg + 0.5 * m_lin_quad(ug, 2)
    print("[E4] x* = %.6f tau_LB = %.4f yr ; c_U/c_model = %.4f -> margin %.4f ; exact c_true/c_model = %.4f -> margin with exact life %.4f"
          % (xs, xs * tcg, cU, 1 / cU, ctrue, 1 / ctrue))
    R.update(margin=1 / cU)

    # --- environment curve (own construction)
    def fenv(k5, k8, s=sig):
        s5 = k5 * SIGF * (2e5) ** b
        s8 = k8 * SIGF * (2e8) ** b
        be = math.log10(s8 / s5) / 3
        n_env = 1e5 * (s / s5) ** (1 / be)
        n_air = 0.5 * (s / SIGF) ** (1 / b)
        return n_air / n_env, n_env, be
    fe = fenv(0.9, 0.4)[0]
    grid = np.array([[fenv(k5, k8)[0] for k8 in np.linspace(0.25, 0.6, 71)] for k5 in np.linspace(0.8, 1.0, 41)])
    print("[env] F_env(0.9, 0.4) = %.3f ; continuous planner box k5 in [0.8,1], k8 in [0.25,0.6]: %.2f to %.2f" % (fe, grid.min(), grid.max()))
    R.update(fe=fe, felo=grid.min(), fehi=grid.max())
    for lab, tgt in (("linear strut p=2", R["lin2"]), ("linear strut p=3", R["lin3"]), ("parabolic strut p=2", R["par2"]), ("parabolic wall p=1", R["par1"])):
        k8 = brentq(lambda k: fenv(0.9, k)[0] - tgt, 0.25, 1.0)
        print("[env] k8 (k5 = 0.9) at which F_env equals %-22s %.3f: k8 = %.4f ; planner-box low end %.2f %s it"
              % (lab, tgt, k8, grid.min(), "above" if grid.min() > tgt else "BELOW"))

    # --- concurrent cases: block damage vs separate treatments
    print("[conc] factor by which separate treatment overstates life, relative to the block (envelope) life:")
    for s in (0.1, 1.0):
        for phi in (9, 33, 129, 1025):
            blk = (1 + s) ** m + (phi - 1) * s ** m
            tslow, tfast, tminer = blk, blk / (phi * s ** m), blk / (1 + phi * s ** m)
            print("    s=%.1f phi=%5d: (1+s)^m = %8.2f  slow-case/block = %8.2f  min-rule/block = %8.2f  Miner/block = %8.2f"
                  % (s, phi, (1 + s) ** m, tslow, min(tslow, tfast), tminer))
    for phi in (9, 33, 129, 1025):
        g = lambda s: -min((1 + s) ** m + (phi - 1) * s ** m, ((1 + s) ** m + (phi - 1) * s ** m) / (phi * s ** m))
        r = minimize_scalar(g, bounds=(1e-3, 3), method="bounded", options={"xatol": 1e-9})
        h = lambda s: -((1 + s) ** m + (phi - 1) * s ** m) / (1 + phi * s ** m)
        r2 = minimize_scalar(h, bounds=(1e-3, 3), method="bounded", options={"xatol": 1e-9})
        print("    phi=%5d: max over s of min-rule/block = %8.2f at s = %.4f ; of Miner/block = %8.2f at s = %.4f"
              % (phi, -r.fun, r.x, -r2.fun, r2.x))

    # --- pits: two Delta-K conventions at R = -1
    Y = 2 * 1.12 / math.pi
    for conv, ds in (("full range 2 sigma_a (S2)", 2 * sig), ("positive part sigma_a (E647 R<0 practice)", sig)):
        a0 = (1 / math.pi) * (3.0 / (Y * ds)) ** 2 * 1e6
        lf = (a0 / (a0 + 100)) ** (-m / 2)
        ta = a0 / 100.0
        e = m / 2 + 1
        tau = ta * ((1 + e * TAU0 / ta) ** (1 / e) - 1)
        print("[pit] %-42s a0 = %8.2f um ; life factor at 100 um = %7.3f ; thin wall PF10 r10: pit-fatigue %.3f yr vs t_perf 1.500 yr"
              % (conv, a0, lf, tau))
        if conv.startswith("full"):
            # Rule W check: 3 mm wall, one side, PF = 3, r = 10 um/yr, same stress
            ta3 = a0 / 30.0
            tau3 = ta3 * ((1 + e * TAU0 / ta3) ** (1 / e) - 1)
            tc3 = 300.0
            tauc3 = life_linear(TAU0 / tc3, m) * tc3
            tperf3 = 3000.0 / (1 * 3 * 10)
            ruleW = min(tauc3, tperf3)
            print("[pit] Rule W check, 3 mm wall, one side, PF = 3, r = 10: Rule W = min(tau_c %.3f, t_perf %.1f) = %.3f yr ; pit-initiated fatigue %.3f yr ; Rule W / pit = %.2f"
                  % (tauc3, tperf3, ruleW, tau3, ruleW / tau3))
            R.update(ruleW_ratio=ruleW / tau3, a0=a0, lf=lf)

    # --- displacement control threshold, by integration
    rs = brentq(lambda r: quad(lambda u: (1 - u) ** m, 0, 1)[0] / r - 1.0, 0.01, 0.5)
    print("[disp] rho* (D(t_c) = 1 under sigma ~ (1-u)^+1) = %.5f" % rs)
    res[b] = R

print("\n" + "=" * 90)
print("Sensitivity to b: ratio (b=-0.124)/(b=-0.102) of headline quantities (answer verdict item 5 says 'up to about 40 %')")
a, c = res[-0.102], res[-0.124]
for k in ("sig", "lin1", "lin2", "par2", "Fg", "ve1", "margin", "fe", "felo", "lf"):
    print("    %-8s %10.4g %10.4g  ratio %.3f  change %+.0f %%" % (k, a[k], c[k], c[k] / a[k], 100 * (c[k] / a[k] - 1)))
for s in (0.5, 1.0):
    r = (1 + s) ** c["m"] / (1 + s) ** a["m"]
    print("    (1+s)^m at s=%.1f ratio %.3f change %+.0f %%" % (s, r, 100 * (r - 1)))

# --- Tedmon bounds via ODE (dimensionless dy/dth = 1/y - 1)
print("\n[tedmon] dy/dtheta = 1/y - 1, y(0)=0 (start from series y = sqrt(2 th) at th = 1e-8)")
th = np.logspace(-4, 3, 2001)
sol = solve_ivp(lambda t, y: [1 / y[0] - 1], (1e-8, th[-1]), [math.sqrt(2e-8)], t_eval=th, rtol=1e-11, atol=1e-14, method="LSODA")
mm = sol.y[0] + th
U = np.sqrt(2 * th) + th
L = np.maximum(np.sqrt(2 * th), th)
print("    violations L <= m <= U: %d ; max U/m = %.4f at theta = %.3f ; max m/L = %.4f at theta = %.3f"
      % (np.sum((mm < L - 1e-9) | (mm > U + 1e-9)), (U / mm).max(), th[np.argmax(U / mm)], (mm / L).max(), th[np.argmax(mm / L)]))

# --- D5 / D6
E_OX, NU_OX = 380e9, 0.25
dc = lambda gc, eps: gc * (1 - NU_OX) / (E_OX * eps ** 2) * 1e6
print("\n[D5] delta_c (G_c = 5, dT = 200 K): 7e-6: %.3f um ; 14.7e-6: %.3f um ; ratio %.4f ; time ratio %.4f"
      % (dc(5, 7e-6 * 200), dc(5, 14.7e-6 * 200), dc(5, 14.7e-6 * 200) / dc(5, 7e-6 * 200), (dc(5, 14.7e-6 * 200) / dc(5, 7e-6 * 200)) ** 2))
print("[D5] mismatch stress dT = 200 K: %.3f / %.3f GPa" % (E_OX * 7e-6 * 200 / (1 - NU_OX) / 1e9, E_OX * 14.7e-6 * 200 / (1 - NU_OX) / 1e9))
for b in (-0.102, -0.124):
    ea = SIGF * (2 * N0) ** b * 1e6 / 73e9
    cx = lambda k, e: (1 / math.pi) * (k * 1e6 / (1.12 * E_OX * e)) ** 2 * 1e6
    print("[D6] b=%.3f eps_a = %.4e ; c_x(K_Ic=1) = %.3f um ; dT(eps_th = eps_a) Al = %.1f K ; c_x at dT=100 K = %.3f um"
          % (b, ea, cx(1, ea), ea / 14.7e-6, cx(1, ea + 14.7e-6 * 100)))

# --- C14 null case
print("\n[C14 null] q = 0: life = min(tau0, t_c) in the model with recession; tau/tau0 = %s for rho = 0.01, 0.1, 1, 10"
      % ", ".join("%.3f" % (min(1.0, 1.0 / r)) for r in (0.01, 0.1, 1, 10)))
print("    so for rho >= 1 the expected null value is 1/rho (recession governs), not 1.")
print("\nAll values level `derived`.")
