"""rv04: Task 5 of the Prompt 8 S5 review: stress cases (i)-(vi) against every alternative rule.

TRUE MODEL (assumptions, all made up): products k with N_k positions and d_k = Sigma_g - Sigma_s (J/K per
position, CExC(x) excluding every part of B_infra, so no overlap); N_out outside positions that never switch;
rebound rho in [0,1]: outside users absorb rho of the draw freed by switchers (only when N_out > 0);
draw(S) = N_out + sum_{k not in S} N_k + rho * sum_{k in S} N_k * [N_out > 0];
avoidable infrastructure B_av(draw) = 0 if draw == 0 else alpha F + v draw + F_step ceil(draw/Q) + b draw^2;
sunk part (1 - alpha) F is never saved but is inside the spec's B_infra (it includes "establishing").
W(S) = [B_av(draw(empty)) - B_av(draw(S))]/T - sum_{k in S} N_k d_k  (J/K saved; optimum by enumeration).

RULES (what each analyst sees):
 R1 E16 (current spec, CExC source without capital goods): lambda_avg = B_infra/(T N_alloc) with
    N_alloc = all positions incl. outside; if no outside users and every product passes d_k < lambda_avg -> all;
    otherwise lambda = 0 and S = {d_k < 0}.
 R2 average share without the gate: S = {d_k < lambda_avg}.
 R3 marginal only: S = {d_k < v_seen/T}, v_seen = dB/dN at the current draw (= v for linear and steps).
 R4 the answer's rule with full information: S_m = {d_k < v_seen/T}; add all products if there are no outside
    users and sum phi_k < 1, phi_k = N_k (d_k - v_seen/T) T / F_av_seen, F_av_seen = B_av(N) - v_seen N
    (clipped at 0). Unconditional verdicts: pass if d_k < v_seen/T, fail if d_k > v_seen/T + F_av_seen/(T N_k).
 R5 reviewer's spec-symbol bracket (proposal, not in the answer): pass if d_k < 0; fail if
    d_k > B_av(N)/(T N_k); all-exit test sum N_k d_k < B_av(N)/T when there are no outside users.
"Wrong" = loss W(opt) - W(S_rule) > 1e-9 relative, or a wrong unconditional verdict (R4, R5).
Level `derived` (unverified). numpy only. Run: python rv04_stress_cases.py
"""
import itertools
import math
import numpy as np

T = 298.15


class Case:
    def __init__(s, N, d, F=4e13, v=2e4, alpha=1.0, N_out=0.0, rho=0.0, F_step=0.0, Q=1e30, b=0.0):
        s.N, s.d = np.array(N, float), np.array(d, float)
        s.F, s.v, s.alpha, s.N_out, s.rho, s.F_step, s.Q, s.b = F, v, alpha, N_out, rho, F_step, Q, b
        s.n = len(N)
        s.Nall = s.N.sum() + N_out

    def B_av(s, draw):
        if draw <= 0:
            return 0.0
        return s.alpha * s.F + s.v * draw + s.F_step * math.ceil(draw / s.Q - 1e-12) + s.b * draw ** 2

    def draw(s, S):
        out = s.N_out + sum(s.N[k] for k in range(s.n) if k not in S)
        if s.N_out > 0:
            out += s.rho * sum(s.N[k] for k in S)
        return out

    def W(s, S):
        return (s.B_av(s.draw(())) - s.B_av(s.draw(S))) / T - sum(s.N[k] * s.d[k] for k in S)

    def all_subsets(s):
        return [S for r in range(s.n + 1) for S in itertools.combinations(range(s.n), r)]

    def opt(s):
        vals = {S: s.W(S) for S in s.all_subsets()}
        best = max(vals.values())
        tol = 1e-9 * (abs(best) + s.B_av(s.Nall) / T + 1)
        return best, [S for S, w in vals.items() if w >= best - tol], tol

    # --- what the analyst sees
    def lam_avg(s):
        return ((1 - s.alpha) * s.F + s.B_av(s.Nall)) / (T * s.Nall)

    def v_seen(s):
        return s.v + 2 * s.b * s.Nall

    def F_av_seen(s):
        return max(0.0, s.B_av(s.Nall) - s.v_seen() * s.Nall)

    # --- rules
    def R1(s):
        la = s.lam_avg()
        if s.N_out == 0 and all(s.d < la):
            return tuple(range(s.n))
        return tuple(k for k in range(s.n) if s.d[k] < 0)

    def R2(s):
        return tuple(k for k in range(s.n) if s.d[k] < s.lam_avg())

    def R3(s):
        return tuple(k for k in range(s.n) if s.d[k] < s.v_seen() / T)

    def R4(s):
        lo = s.v_seen() / T
        Sm = tuple(k for k in range(s.n) if s.d[k] < lo)
        Fa = s.F_av_seen()
        if s.N_out == 0 and Fa > 0:
            phi = np.maximum(0, s.N * (s.d - lo)) * T / Fa
            if phi.sum() < 1:
                return tuple(range(s.n))
        return Sm

    def R4_uncond(s):
        lo = s.v_seen() / T
        Fa = s.F_av_seen() if s.N_out == 0 else 0.0
        return {k: ("pass" if s.d[k] < lo else "fail" if s.d[k] > lo + Fa / (T * s.N[k]) else "cond") for k in range(s.n)}

    def R5(s):
        S0 = tuple(k for k in range(s.n) if s.d[k] < 0)
        if s.N_out == 0 and (s.N * s.d).sum() < s.B_av(s.Nall) / T:
            return tuple(range(s.n))
        return S0

    def R5_uncond(s):
        up = s.B_av(s.Nall) / T
        return {k: ("pass" if s.d[k] < 0 else "fail" if s.d[k] > up / s.N[k] else "cond") for k in range(s.n)}

    def report(s, label):
        best, opts, tol = s.opt()
        print(f"  [{label}] optimum W = {best:+.4e} J/K at {[[k+1 for k in S] for S in opts]}; "
              f"lambda_avg = {s.lam_avg():.2f}, v_seen/T = {s.v_seen()/T:.2f} J/K")
        res = {}
        for name in ("R1", "R2", "R3", "R4", "R5"):
            S = getattr(s, name)()
            loss = best - s.W(S)
            wrong = loss > tol
            res[name] = wrong
            print(f"    {name}: S = {[k+1 for k in S]}, W = {s.W(S):+.4e}, loss = {loss:.4e} J/K {'WRONG' if wrong else 'ok'}")
        for name in ("R4", "R5"):
            unc = getattr(s, name + "_uncond")()
            bad = [k + 1 for k, u in unc.items() if (u == "pass" and not all(k in S for S in opts))
                   or (u == "fail" and any(k in S for S in opts))]
            res[name + "_badunc"] = bool(bad)
            print(f"    {name} unconditional verdicts {dict((k+1, u) for k, u in unc.items())}; wrong unconditional: {bad}")
        allwrong = all(res[r] for r in ("R1", "R2", "R3", "R4"))
        print(f"    every alternative R1-R4 wrong: {allwrong}")
        return res


print("== base: rv03 case (linear) ==")
Case([9e8, 1e8], [150, 400]).report("base")

print("\n== (i) F partly avoidable, alpha sweep (d = 150, 400) and (d = 150, 190) ==")
for a in (1.0, 0.9, 0.81, 0.80, 0.5, 0.0):
    c = Case([9e8, 1e8], [150, 400], alpha=a)
    print(f"  alpha={a}: W(all) = {c.W((0, 1)):+.4e} J/K; R4 -> {[k+1 for k in c.R4()]}; R1 -> {[k+1 for k in c.R1()]}")
Case([9e8, 1e8], [150, 190], alpha=0.5).report("(i) alpha=0.5, d=(150,190): E16 credits sunk F")

print("\n== (ii) discrete capacity steps ==")
Case([4e8, 3e8, 3e8], [200, 120, 400], F=2e13, F_step=1e13, Q=3.5e8).report("(ii) partial exit of product 2 saves a step")
# lower bound v/T under steps: any exit saves at least v N_k
c = Case([4e8, 3e8, 3e8], [200, 120, 400], F=2e13, F_step=1e13, Q=3.5e8)
mins = min((c.B_av(c.draw(S)) - c.B_av(c.draw(tuple(sorted(S + (k,)))))) / (c.N[k] * c.v)
           for S in c.all_subsets() for k in range(3) if k not in S)
print(f"  (ii) min over S,k of [saving of adding k]/(v N_k) = {mins:.4f} (>= 1 means v/T is a lower bound)")

print("\n== (iii) outside users that stay, with market rebound rho ==")
for rho in (0.0, 0.5, 1.0):
    c = Case([4e8, 1e8], [50, 20], N_out=5e8, rho=rho)
    sv = [(c.B_av(c.draw(())) - c.B_av(c.draw((k,)))) / (T * c.N[k]) for k in range(2)]
    print(f"  rho={rho}: true lone-exit saving per position = {sv[0]:.2f} J/K (v/T = {c.v/T:.2f})")
Case([4e8, 1e8], [50, 20], N_out=5e8, rho=0.5).report("(iii) rho=0.5, d=(50,20)")
Case([4e8, 1e8], [50, 20], N_out=5e8, rho=1.0).report("(iii) rho=1.0, d=(50,20)")

print("\n== (v) convex B_infra(N) = F0 + a N + b N^2 (a = 5e3, b = 7.5e-6 J, B'(N=1e9) = 2e4 J) ==")
c = Case([9e8, 1e8], [55, 5000], F=4e13, v=5e3, b=7.5e-6)
print(f"  lone exit of product 1: true saving per position = {(c.B_av(c.draw(()))-c.B_av(c.draw((0,))))/(T*9e8):.4f} J/K; "
      f"v_seen/T = B'(N)/T = {c.v_seen()/T:.4f} J/K")
c.report("(v) d=(55,5000)")
Case([6e8, 3e8, 1e8], [55, 20, 5000], F=4e13, v=5e3, b=7.5e-6).report("(v) 3 products d=(55,20,5000)")


# ------------------------------------------------------------------ random search for 'every alternative wrong'
def gen(kind, rng):
    n = 3
    N = 10 ** rng.uniform(7.5, 9, n)
    kw = dict(F=10 ** rng.uniform(12.5, 14), v=10 ** rng.uniform(3.5, 4.7))
    if kind == "alpha":
        kw["alpha"] = rng.uniform(0, 1)
    if kind == "steps":
        kw["F_step"] = kw["F"] * rng.uniform(0.1, 1)
        kw["Q"] = N.sum() * rng.uniform(0.2, 0.7)
    if kind == "outside":
        kw["N_out"] = N.sum() * rng.uniform(0.1, 2)
        kw["rho"] = rng.uniform(0, 1)
    if kind == "convex":
        Nt = N.sum()
        kw["b"] = kw["v"] * rng.uniform(0.2, 3) / (2 * Nt)
    c0 = Case(N, np.zeros(n), **kw)
    scale = c0.lam_avg() * rng.uniform(0.1, 2.5)
    d = rng.uniform(-0.2, 1.0, n) * scale
    return Case(N, d, **kw)


rng = np.random.default_rng(815)
print("\n== random search (3 products, 4000 profiles per regime) ==")
for kind in ("linear", "alpha", "steps", "outside", "convex"):
    cnt = {r: 0 for r in ("R1", "R2", "R3", "R4", "R5", "R4_badunc", "R5_badunc", "allwrong")}
    maxloss, example = {r: 0.0 for r in ("R1", "R2", "R3", "R4", "R5")}, None
    M = 4000
    for _ in range(M):
        c = gen(kind, rng)
        best, opts, tol = c.opt()
        wr = {}
        for r in ("R1", "R2", "R3", "R4", "R5"):
            loss = best - c.W(getattr(c, r)())
            wr[r] = loss > tol
            cnt[r] += wr[r]
            maxloss[r] = max(maxloss[r], loss)
        for r in ("R4", "R5"):
            unc = getattr(c, r + "_uncond")()
            bad = any((u == "pass" and not all(k in S for S in opts)) or (u == "fail" and any(k in S for S in opts))
                      for k, u in unc.items())
            cnt[r + "_badunc"] += bad
        if all(wr[r] for r in ("R1", "R2", "R3", "R4")):
            cnt["allwrong"] += 1
            if example is None:
                example = c
    print(f"  {kind:8s}: wrong-verdict share R1 {cnt['R1']/M:.3f}, R2 {cnt['R2']/M:.3f}, R3 {cnt['R3']/M:.3f}, "
          f"R4 {cnt['R4']/M:.3f}, R5 {cnt['R5']/M:.3f}; wrong unconditional R4 {cnt['R4_badunc']/M:.3f}, "
          f"R5 {cnt['R5_badunc']/M:.3f}; all of R1-R4 wrong {cnt['allwrong']/M:.3f}")
    print(f"            max loss J/K: " + ", ".join(f"{r} {maxloss[r]:.3e}" for r in maxloss))
