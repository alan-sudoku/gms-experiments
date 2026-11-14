"""Review of prompt 4, claims C4 and C5: monotonicity in tw at exact ties, and interval screening on fully
non-degenerate boxes, coupled coefficients, and corner-construction hazards.

Purpose
  (1) C4, tie scan: for fixed exact tau, evaluate G(s) = Kg [m sqrt(s) + sqrt(tau - m s)] + m R on a
      sorted list of s that contains every exact tie s = tau/k (k = 1..60 and 8 large k), s (1 -+ 1e-30)
      around each, random s in (0, tau) and s > tau. Check G non-increasing in s, under the brief's tie
      convention m = floor(tau/s) AND under the alternative m = ceil(tau/s) - 1 (tie in the earlier segment).
  (2) C5 on FULLY non-degenerate product boxes (every coordinate lo < hi; the implementer's run had 6 such
      boxes in 3000): all 128 vertices + 24 interior points, tau at random values, exact ties j*tw for the
      pessimistic, optimistic and every sampled tw, their float ulp neighbours, tau = 0 and tau < tw_lo.
      d0 is centred so f changes sign inside the box (non-vacuous win sets).
  (3) Coupled coefficients: (tw, Kg, a, Ks) all functions of one hidden parameter p (non-monotone); the
      screening box is the per-coefficient bounding box. Inclusion is tested for many p. Then the hazard
      that DOES break C5: corners taken in p (evaluate p_lo, p_hi) instead of per coefficient.
  (4) lambda double-counting hazard (d0 interval already net of lambda, lambda subtracted again).
Claims: C4, C5. Conventions: brief (win = f < 0; f contains -lam). Exact Fractions, 60-digit mpmath.
Run: <gms-local>/.venv/bin/python r3_c4_c5_monotone.py   (fixed seed)
Level: derived.
"""
import math
import random
from fractions import Fraction as Fr

import mpmath as mp

mp.mp.dps = 60
NAMES = ["a", "Kg", "Ks", "d0", "R", "tw", "lam"]


def M(q):
    q = Fr(q)
    return mp.mpf(q.numerator) / q.denominator


def floor_div(x, y):
    x, y = Fr(x), Fr(y)
    return (x.numerator * y.denominator) // (x.denominator * y.numerator)


def f_exact(tau, p, conv="floor"):
    tau, tw = Fr(tau), Fr(p["tw"])
    m = floor_div(tau, tw)
    if conv == "ceil-1" and m >= 1 and m * tw == tau:
        m -= 1
    dt = tau - m * tw
    return (M(p["a"]) * M(tau) + M(p["Kg"]) * mp.sqrt(M(dt)) - M(p["Ks"]) * mp.sqrt(M(tau)) + M(p["d0"])
            - M(p["lam"]) + m * M(p["R"]) + m * M(p["Kg"]) * mp.sqrt(M(tw)))


def G_tw(tau, s, Kg, R, conv):
    p = dict(a=0, Kg=Kg, Ks=0, d0=0, R=R, tw=s, lam=0)
    return f_exact(tau, p, conv)


def part1(rng):
    viol = {"floor": 0, "ceil-1": 0}
    npts = 0
    for _ in range(150):
        tau = Fr(rng.choice([1, 3, 10 ** 3, 10 ** 9, 10 ** 10])) if rng.random() < 0.3 else Fr(10 ** rng.uniform(0, 10))
        Kg = Fr(0) if rng.random() < 0.2 else Fr(10 ** rng.uniform(-3, 3))
        R = Fr(0) if rng.random() < 0.2 else Fr(10 ** rng.uniform(-3, 6))
        ks = list(range(1, 61)) + [10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6, 999, 1001, 12345, 777777]
        e = Fr(1, 10 ** 30)
        ss = set()
        for k in ks:
            s0 = tau / k
            ss.update([s0, s0 * (1 - e), s0 * (1 + e)])
        ss.update(tau * Fr(rng.random()) for _ in range(60))
        ss.update(tau * (1 + Fr(rng.random()) * 10) for _ in range(10))
        ss.discard(Fr(0))
        sl = sorted(ss)
        for conv in ("floor", "ceil-1"):
            prev = None
            for s in sl:
                g = G_tw(tau, s, Kg, R, conv)
                npts += 1
                if prev is not None and g > prev + mp.mpf(10) ** -40 * (1 + abs(prev)):
                    viol[conv] += 1
                prev = g
    print("(1) C4 tie scan: G(s) = Kg[m sqrt s + sqrt(tau - m s)] + m R evaluated at", npts,
          "points (150 tau, all s = tau/k for 68 k, +-1e-30 neighbours, random s incl. s > tau)")
    print("    increases of G with s (violations of 'non-increasing in tw'): floor convention",
          viol["floor"], "; ceil-1 convention", viol["ceil-1"])


def rand_box(rng):
    """Fully non-degenerate box; d0 centred so that f changes sign within the box at a reference tau."""
    lo, hi = {}, {}
    tw_lo = 10 ** rng.uniform(0, 8)
    tw_hi = tw_lo * 10 ** rng.uniform(1e-6, 3)
    lo["tw"], hi["tw"] = tw_lo, tw_hi
    for n, (l, h) in dict(a=(-1e-3, 1e-3), Kg=(-3, 3), Ks=(-3, 3), R=(-3, 4), lam=(-3, 4)).items():
        if n == "a":
            x, y = sorted([rng.uniform(l, h), rng.uniform(l, h)])
            if x == y:
                y = x + 1e-6
        else:
            x0 = 10 ** rng.uniform(l, h)
            x, y = x0, x0 * 10 ** rng.uniform(1e-6, 1)
            if rng.random() < 0.2:
                x = 0.0  # lower bound exactly 0 (Kg = 0, R = 0, lam = 0 reachable) while hi > 0
        lo[n], hi[n] = x, y
    tref = tw_lo * 10 ** rng.uniform(-1, 3)
    mid = {n: (lo[n] + hi[n]) / 2 for n in NAMES if n != "d0"}
    mid["d0"] = 0.0
    c = float(f_exact(Fr(tref), mid))
    w = abs(c) * 10 ** rng.uniform(-3, 0) + 1e-6
    lo["d0"], hi["d0"] = -c - w, -c + w
    return lo, hi, tref


def corners(lo, hi):
    pess = dict(a=hi["a"], Kg=hi["Kg"], Ks=lo["Ks"], d0=hi["d0"], R=hi["R"], tw=lo["tw"], lam=lo["lam"])
    opt = dict(a=lo["a"], Kg=lo["Kg"], Ks=hi["Ks"], d0=lo["d0"], R=lo["R"], tw=hi["tw"], lam=hi["lam"])
    return pess, opt


def check_inclusion(t, pess, pts, opt, stats):
    fp, fo = f_exact(t, pess), f_exact(t, opt)
    tol = mp.mpf(10) ** -40 * (1 + abs(fp) + abs(fo))
    for x in pts:
        fx = f_exact(t, x)
        stats["evals"] += 1
        if not (fp >= fx - tol and fx >= fo - tol):
            stats["order_viol"] += 1
        if fp < 0 and not fx < 0:
            stats["incl_viol"] += 1
        if fx < 0 and not fo < 0:
            stats["incl_viol"] += 1
        stats["x wins"] += fx < 0
        stats["x ties f==0"] += fx == 0
    stats["pess wins"] += fp < 0
    stats["opt wins, pess not"] += (fo < 0) and not (fp < 0)


def part2(rng):
    stats = dict(boxes=0, evals=0, order_viol=0, incl_viol=0, **{"x wins": 0, "x ties f==0": 0,
                 "pess wins": 0, "opt wins, pess not": 0, "tau_cross_segment": 0})
    for _ in range(120):
        lo, hi, tref = rand_box(rng)
        assert all(lo[n] < hi[n] for n in NAMES)
        stats["boxes"] += 1
        pess, opt = corners(lo, hi)
        pts = []
        for v in range(128):
            pts.append({n: (hi[n] if (v >> i) & 1 else lo[n]) for i, n in enumerate(NAMES)})
        for _ in range(24):
            pts.append({n: lo[n] + rng.random() * (hi[n] - lo[n]) for n in NAMES})
        taus = [Fr(0), Fr(tref), Fr(lo["tw"]) * Fr(rng.random()), Fr(lo["tw"]) + Fr(rng.random()) * (Fr(hi["tw"]) - Fr(lo["tw"]))]
        j = rng.randint(1, 2000)
        for tw in (lo["tw"], hi["tw"], pts[-1]["tw"], pts[-2]["tw"]):
            taus.append(Fr(j) * Fr(tw))
            x = j * tw
            taus += [Fr(math.nextafter(x, 0.0)), Fr(x), Fr(math.nextafter(x, math.inf))]
        for t in taus:
            ms = {floor_div(t, Fr(x["tw"])) for x in pts}
            stats["tau_cross_segment"] += len(ms) > 1
            check_inclusion(t, pess, pts, opt, stats)
    print("(2) C5 on fully non-degenerate product boxes:", stats)


def part3(rng):
    viol = 0
    n = 0
    hazard_ex = None
    for _ in range(200):
        tlo = 10 ** rng.uniform(0, 6)
        thi = tlo * 10 ** rng.uniform(0.01, 2)
        klo = 10 ** rng.uniform(-2, 1)
        khi = klo * 10 ** rng.uniform(0.01, 1)
        alo, ahi = sorted([rng.uniform(-1e-3, 1e-3), rng.uniform(-1e-3, 1e-3)])
        R, Ks, lam = 10 ** rng.uniform(-2, 3), 10 ** rng.uniform(-2, 2), 0.0
        w = rng.uniform(3, 20)

        def x_of(p):  # non-monotone coupling to the hidden parameter p in [0,1]
            return dict(tw=tlo + p * (thi - tlo), Kg=klo + (khi - klo) * abs(math.sin(w * p)),
                        a=alo + (ahi - alo) * (2 * p - 1) ** 2, Ks=Ks, R=R, lam=lam, d0=0.0)
        tref = thi * 10 ** rng.uniform(0, 2)
        d0 = -float(f_exact(Fr(tref), x_of(0.5)))
        lo = dict(tw=tlo, Kg=klo, a=alo, Ks=Ks, R=R, lam=lam, d0=d0)
        hi = dict(tw=thi, Kg=khi, a=ahi, Ks=Ks, R=R, lam=lam, d0=d0)
        pess, opt = corners(lo, hi)
        ps = [rng.random() for _ in range(30)] + [0.0, 1.0]
        pts = []
        for p in ps:
            x = x_of(p)
            x["d0"] = d0
            pts.append(x)
        for t in [Fr(tref), Fr(tref) * Fr(rng.random()), Fr(rng.randint(1, 500)) * Fr(pts[0]["tw"])]:
            fp, fo = f_exact(t, pess), f_exact(t, opt)
            for x in pts:
                n += 1
                fx = f_exact(t, x)
                if fp < 0 and not fx < 0 or fx < 0 and not fo < 0:
                    viol += 1
            # hazard: corners in p-space (worse of p=0, p=1) instead of per coefficient
            fpp = max(f_exact(t, pts[-2]), f_exact(t, pts[-1]))
            worst_inside = max(f_exact(t, x) for x in pts)
            if hazard_ex is None and fpp < 0 <= worst_inside:
                hazard_ex = (float(t), mp.nstr(fpp, 8), mp.nstr(worst_inside, 8), tlo, thi, klo, khi, alo, ahi, R, Ks, d0, w)
    print("(3) coupled coefficients (tw, Kg, a functions of hidden p, non-monotone), per-coefficient bounding box:")
    print("    inclusion checks:", n, "; violations:", viol)
    if hazard_ex:
        print("    corners taken in p (p=0, p=1) instead of per coefficient BREAKS inclusion, e.g. tau=%.6g:"
              " max(f(p=0), f(p=1)) = %s < 0 but max over interior p = %s >= 0" % hazard_ex[:3])
        print("      (tw in [%.6g, %.6g], Kg in [%.6g, %.6g] via |sin(%.4g p)|, a in [%.3g, %.3g] via (2p-1)^2, R=%.4g, Ks=%.4g, d0=%.10g)"
              % (hazard_ex[3], hazard_ex[4], hazard_ex[5], hazard_ex[6], hazard_ex[12], hazard_ex[7], hazard_ex[8],
                 hazard_ex[9], hazard_ex[10], hazard_ex[11]))
    else:
        print("    no p-corner hazard example found (UNSURE)")


def part4():
    # d0 interval already net of lambda (d0 = D - lam); screening subtracts lam again
    base = dict(a=0.0, Kg=1.0, Ks=0.0, R=0.0, tw=1.0, lam=0.0)
    D_minus_lam_hi = -0.3    # pessimistic d0 already includes the credit
    lam_lo = 0.5
    t = Fr(1, 4)             # dt = 1/4: Kg sqrt(dt) = 0.5
    true_pess = dict(base, d0=D_minus_lam_hi, lam=0.0)
    wrong_pess = dict(base, d0=D_minus_lam_hi, lam=lam_lo)
    print("(4) lambda double count: tau = 1/4, Kg = 1, tw = 1, d0_hi (net of lambda) = -0.3, lam_lo = 0.5:")
    print("    f at the true worst input =", mp.nstr(f_exact(t, true_pess), 6),
          "(loses); f at a pessimistic corner that subtracts lam again =", mp.nstr(f_exact(t, wrong_pess), 6),
          "(claims a win) -> win set(pess) is not a subset of win set(any)")


def main():
    rng = random.Random(55)
    part1(rng)
    part2(rng)
    part3(rng)
    part4()


if __name__ == "__main__":
    main()
