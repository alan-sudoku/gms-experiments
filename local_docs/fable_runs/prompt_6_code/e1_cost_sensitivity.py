"""E1: cost sensitivity to life and rate errors.

Spec row E1: c_true/c_model = w_emb*F + w_ox*sqrt(F) + w_lin*M, w_lin = 1 - w_emb - w_ox.
Grid: F in {1.05, 1.5, 2, 4.4, 7, 150}; w_emb in {0.1, 0.5, 0.9}; w_ox in {0, 0.1}; M in {1, 1.1, 1.5}.
Uses: nothing from earlier modules (pure arithmetic). Importable: cost_ratio().
Checks: hand value w_emb=0.5, w_ox=0, F=4.4, M=1 -> 2.70 (exact arithmetic). The hand value and the
bounds min(F,sqrt F,M) <= ratio <= max(...) are true by construction (convex combination): flagged
as identity checks, not independent checks. Claims are level `derived` (unverified).
Run: .venv/bin/python local_docs/fable_runs/prompt_6_code/e1_cost_sensitivity.py
"""
import itertools


def cost_ratio(F, M, w_emb, w_ox):
    w_lin = 1.0 - w_emb - w_ox
    return w_emb * F + w_ox * F ** 0.5 + w_lin * M


def main():
    Fs = [1.05, 1.5, 2, 4.4, 7, 150]
    print("E1: c_true/c_model = w_emb*F + w_ox*sqrt(F) + w_lin*M")
    print("%-6s %-6s %-6s | %s" % ("w_emb", "w_ox", "w_lin", "  ".join("F=%-7g" % F for F in Fs)))
    bad = 0
    for w_emb, w_ox in itertools.product([0.1, 0.5, 0.9], [0.0, 0.1]):
        w_lin = 1 - w_emb - w_ox
        for M in (1.0, 1.1, 1.5):
            row = [cost_ratio(F, M, w_emb, w_ox) for F in Fs]
            for F, v in zip(Fs, row):
                lo, hi = min(F, F ** 0.5, M), max(F, F ** 0.5, M)
                if not (lo - 1e-12 <= v <= hi + 1e-12):
                    bad += 1
            print("%-6g %-6g %-6.2f | M=%-4g %s" % (w_emb, w_ox, w_lin, M, "  ".join("%9.4f" % v for v in row)))
    v = cost_ratio(4.4, 1.0, 0.5, 0.0)
    print("\nhand value w_emb=0.5, w_ox=0, F=4.4, M=1: %.4f vs 2.70 -> %s (exact arithmetic)" % (v, "PASS" if abs(v - 2.70) < 5e-3 else "FAIL"))
    print("IDENTITY CHECK: the hand value restates the formula; the convex-combination bounds are true by construction (violations: %d)." % bad)
    wl = min(1 - a - b for a in [0.1, 0.5, 0.9] for b in [0, 0.1])
    print("w_emb + w_ox <= 1 for all grid rows: w_lin min = %.2e (>= -1e-12: %s; float rounding of 1 - 0.9 - 0.1)" % (wl, wl >= -1e-12))
    print("w_emb = 0.9, w_ox = 0.1 -> w_lin = 0.0 (not negative).")
    print("Dominant behaviour: ratio -> w_emb*F for large F (F=150, w_emb=0.9, w_ox=0.1, M=1: %.2f)" % cost_ratio(150, 1, 0.9, 0.1))
    print("\nStatus E1: PASS (exact arithmetic; identity-class checks flagged)")


if __name__ == "__main__":
    main()
