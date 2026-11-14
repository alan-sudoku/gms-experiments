"""Rainflow routine of plan 3.2 (used by B5 and A11; reusable by the final pass).

rainflow(samples, cyclic=True) -> (cycles, residue, stack_final)
  cycles: list of (range, mean); residue: stack points left (must be 1 point).
Steps (plan 3.2): (1) reduce to turning points (sign change of first difference;
repeats dropped); (2) rotate to start at the global maximum and append that maximum
at the end; (3) stack: while >= 3 points, X=|S[-1]-S[-2]|, Y=|S[-2]-S[-3]|; if X>=Y count
a full cycle of range Y, mean (S[-2]+S[-3])/2, delete S[-2], S[-3]; else stop inner loop.
(4) final stack must hold one point, else residue reported.
Assumption: samples cover exactly one period of a periodic history, so the turning
point test in step 1 is applied cyclically (first/last samples are neighbours).
Basquin: N = 0.5 (sigma_ar/sigma_f')^(1/b); damage per cycle 1/N.
"""
import numpy as np

SF = 900.0      # M02 MPa
B = -0.102      # M03
N0 = 5e8        # M04
SIGMA_A0 = SF * (2 * N0) ** B   # C1 baseline amplitude (MPa)


def turning_points_cyclic(x):
    x = np.asarray(x, float)
    # drop cyclic repeats
    keep = np.ones(len(x), bool)
    keep[1:] = x[1:] != x[:-1]
    x = x[keep]
    while len(x) > 1 and x[0] == x[-1]:
        x = x[:-1]
    d_prev = x - np.roll(x, 1)
    d_next = np.roll(x, -1) - x
    tp = (d_prev * d_next) < 0
    return x[tp]


def rainflow(samples, cyclic=True):
    if cyclic:
        tp = turning_points_cyclic(samples)
    else:
        x = np.asarray(samples, float)
        x = x[np.concatenate(([True], x[1:] != x[:-1]))]
        d = np.diff(x)
        idx = np.where(d[1:] * d[:-1] < 0)[0] + 1
        tp = np.concatenate(([x[0]], x[idx], [x[-1]]))
    if len(tp) < 2:
        return [], list(tp), list(tp)
    k = int(np.argmax(tp))
    tp = np.concatenate((tp[k:], tp[:k], [tp[k]]))
    stack, cycles = [], []
    for v in tp:
        stack.append(float(v))
        while len(stack) >= 3:
            X = abs(stack[-1] - stack[-2])
            Y = abs(stack[-2] - stack[-3])
            if X >= Y:
                cycles.append((Y, 0.5 * (stack[-2] + stack[-3])))
                del stack[-3:-1]
            else:
                break
    return cycles, (stack if len(stack) != 1 else []), stack


def basquin_N(sigma_ar, sf=SF, b=B):
    """Cycles to failure for amplitude sigma_ar (MPa): 0.5 (s/sf)^(1/b)."""
    return 0.5 * (np.asarray(sigma_ar, float) / sf) ** (1.0 / b)


def damage(cycles, variant='a', sf=SF, b=B):
    """Miner damage of counted cycles.  variant 'a': sigma_ar = sigma_a;
    'b': SWT sigma_ar = sqrt((sigma_m + sigma_a) sigma_a) if sigma_m+sigma_a > 0 else zero damage."""
    D = 0.0
    for rng, mean in cycles:
        sa = 0.5 * rng
        if variant == 'a':
            sar = sa
        else:
            v = (mean + sa) * sa
            sar = np.sqrt(v) if (mean + sa) > 0 else 0.0
        if sar > 0:
            D += 1.0 / float(basquin_N(sar, sf, b))
    return D
