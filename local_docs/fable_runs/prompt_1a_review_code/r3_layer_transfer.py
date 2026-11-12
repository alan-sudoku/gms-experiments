"""Reviewer check R3: exact 1-D layered eddy-current solutions (transfer method).

Purpose
    Independent of the writer's 2-D solver (eddy2d.py), test with an exact 1-D model:
      A. Dowell's layer formula (and Claim A's m = 1 factor) against the direct solution.
      B. Homogenisation of a stack of thin, mutually insulated, parallel-connected foils
         (the most favourable z-invariant 'lattice') against a homogeneous slab with
         sigma_eff = fill*sigma, and the writer's strut-level ratio fill*(t/delta)^2/6.
      C. The same foils forced to carry equal currents (ideal transposition) against the
         writer's Litz ratio fill^2 T^2 t^2/(36 delta^4) (1-D, i.e. g = 1).
      D. Monotonicity of R(sigma) at fixed geometry for an isolated slab (field on both
         faces) and for a slab with field on one face.
      E. A regime the writer did not examine: a multi-layer, series-connected winding
         (proximity-dominated, field imposed by the other layers).  Is a homogenised Al
         lattice layer ever better than a solid Cu layer of the SAME thickness?  And is it
         ever better than a thinner solid foil (macro-shape)?
      G. The writer's strut-level loss ratio, isolated as the intra-foil part of the loss.
      F. The interleaved go/return Al foil stacks of the writer's a2_laminations.py, solved
         exactly in 1-D (parallel connection within each polarity), to cross-check the
         writer's 2-D values 56.89, 53.28, 107.14, 53.96 uOhm/m.

Model and assumptions
    Infinitely wide layers (field H_x(y), current J_z(y)), mu = mu0, sinusoidal steady
    state, peak phasors.  In each layer A_z'' = -mu0*sigma*(V'_g - j*omega*A_z), where V'_g
    is the voltage drop per metre of the 'group' the layer belongs to (layers of one group
    are connected in parallel; each group carries a prescribed net current).  Gaps have
    sigma = 0.  H at the bottom face is prescribed (beta*I_total/w; beta = 0.5 isolated
    slab, beta = 0 field on one face only).  Losses are integrated directly
    (sigma*|E|^2/2) with Gauss-Legendre quadrature on sub-layers <= delta/4 thick.
    R' is quoted for a width w = 100 mm (to compare with the 10 x 100 mm bar where useful);
    a 1-D model has no edge crowding, so absolute values are below the 2-D ones.
    Conductivities: Cu 5.96e7 S/m, Al 3.77e7 S/m (as in the prompt).

numpy only.  Run: python3 r3_layer_transfer.py  (a few seconds).
"""
import math

import numpy as np

MU0 = 4e-7 * math.pi
S_CU, S_AL = 5.96e7, 3.77e7
W = 0.1  # width used to quote R' [m]
GL_X, GL_W = np.polynomial.legendre.leggauss(8)
DETAIL = []   # per conducting layer of the last solve: (t, sigma, t*|J_mean|^2, int |J - J_mean|^2 dy)


def delta(s, f):
    return math.sqrt(1 / (math.pi * f * MU0 * s))


def solve_stack(layers, f, currents, beta):
    """layers: list of (thickness, sigma, group) from bottom to top.
    currents: dict group -> net current [A, peak] (per width W).
    beta: H(bottom) = beta * I_total / W.
    Returns (total loss per metre [W/m], dict group -> V'_g).

    Global linear system (numerically stable): in a conducting layer
    A = V'_g/(j w) + a*exp(-k y') + b*exp(k (y' - t)), y' in [0, t];
    in a gap A = a + b*y'.  Unknowns: (a, b) per layer and V'_g per group.
    Equations: A(bottom) = 0 (gauge), A'(bottom) = mu0*H0, continuity of A and A'
    at every interface, prescribed current of every group."""
    w = 2 * math.pi * f
    groups = sorted(currents, key=str)
    gi = {g: i for i, g in enumerate(groups)}
    G = len(groups)
    L = len(layers)
    Itot = sum(currents.values())
    H0 = beta * Itot / W
    N = 2 * L + G
    M = np.zeros((N, N), complex)
    rhs = np.zeros(N, complex)

    def row_A(l, end):
        """coefficients (dict col -> value) of A and A' at the bottom (end=0) or top (end=1) of layer l."""
        t, s, g = layers[l]
        ca, cb = 2 * l, 2 * l + 1
        if s == 0:
            y = 0.0 if end == 0 else t
            return {ca: 1.0, cb: y}, {cb: 1.0}
        k = np.sqrt(1j * w * MU0 * s)
        y = 0.0 if end == 0 else t
        ea, eb = np.exp(-k * y), np.exp(k * (y - t))
        cv = 2 * L + gi[g]
        return {ca: ea, cb: eb, cv: 1 / (1j * w)}, {ca: -k * ea, cb: k * eb}

    r = 0
    A0, Ap0 = row_A(0, 0)
    for c, v in A0.items():
        M[r, c] += v
    r += 1
    for c, v in Ap0.items():
        M[r, c] += v
    rhs[r] = MU0 * H0
    r += 1
    for l in range(L - 1):
        At, Apt = row_A(l, 1)
        Ab, Apb = row_A(l + 1, 0)
        for c, v in At.items():
            M[r, c] += v
        for c, v in Ab.items():
            M[r, c] -= v
        r += 1
        for c, v in Apt.items():
            M[r, c] += v
        for c, v in Apb.items():
            M[r, c] -= v
        r += 1
    # group currents: sum over layers of -(W/mu0)*(A'(top) - A'(bottom))
    for l, (t, s, g) in enumerate(layers):
        if s == 0:
            continue
        _, Apt = row_A(l, 1)
        _, Apb = row_A(l, 0)
        rr = r + gi[g]
        for c, v in Apt.items():
            M[rr, c] += -W / MU0 * v
        for c, v in Apb.items():
            M[rr, c] -= -W / MU0 * v
    for g in groups:
        rhs[r + gi[g]] = currents[g]
    sol = np.linalg.solve(M, rhs)
    loss = 0.0
    DETAIL.clear()
    for l, (t, s, g) in enumerate(layers):
        if s == 0:
            continue
        k = np.sqrt(1j * w * MU0 * s)
        a, b = sol[2 * l], sol[2 * l + 1]
        nsub = max(1, int(math.ceil(t / (delta(s, f) / 4))))
        edges = np.linspace(0, t, nsub + 1)
        ys = (0.5 * (edges[1:] - edges[:-1])[:, None] * GL_X[None, :] + 0.5 * (edges[1:] + edges[:-1])[:, None]).ravel()
        wts = (0.5 * (edges[1:] - edges[:-1])[:, None] * GL_W[None, :]).ravel()
        u = a * np.exp(-k * ys) + b * np.exp(k * (ys - t))      # = A - V'/(j w)
        loss += 0.5 * s * w * w * np.sum(wts * np.abs(u) ** 2) * W
        J = -1j * w * s * u
        Jm = np.sum(wts * J) / t
        DETAIL.append((t, s, abs(Jm) ** 2 * t, np.sum(wts * np.abs(J - Jm) ** 2)))
    return loss, {g: sol[2 * L + gi[g]] for g in groups}


def R_of(layers, f, currents, beta, Inorm):
    loss, _ = solve_stack(layers, f, currents, beta)
    return loss / (0.5 * Inorm ** 2)


def F1(x):
    return x * (math.sinh(2 * x) + math.sin(2 * x)) / (math.cosh(2 * x) - math.cos(2 * x))


def dowell(x, m):
    return x * ((math.sinh(2 * x) + math.sin(2 * x)) / (math.cosh(2 * x) - math.cos(2 * x))
                + 2 * (m * m - 1) / 3 * (math.sinh(x) - math.sin(x)) / (math.cosh(x) + math.cos(x)))


def parallel_foils(T, fill, t, s, group=0):
    """Foils of thickness t centred in pitches p = t/fill filling thickness T (n = T/p)."""
    p = t / fill
    n = int(round(T / p))
    p = T / n
    t = fill * p
    out = []
    for _ in range(n):
        out += [((p - t) / 2, 0.0, None), (t, s, group), ((p - t) / 2, 0.0, None)]
    return out, n, t


if __name__ == "__main__":
    print("== A. Dowell layer formula vs exact 1-D solution (m layers in series, field on one side)")
    f = 1e5
    s = S_CU
    d = delta(s, f)
    for m in (1, 2, 4):
        for xi in (0.3, 1.0, 1.57, 3.0):
            h = xi * d
            layers = []
            cur = {}
            for k in range(m):
                layers.append((h, s, k))
                cur[k] = 1.0
            R = R_of(layers, f, cur, 0.0, 1.0) / m          # per layer
            Rdc = 1 / (s * h * W)
            print(f"   m={m} xi={xi:4.2f}: exact Rac/Rdc={R/Rdc:8.4f}  Dowell={dowell(xi, m):8.4f}")

    print("\n== B. isolated slab T = 10 mm, fill 0.3 Al: parallel-connected insulated foils vs homogenised")
    T, fill = 10e-3, 0.3
    for f in (1e4, 1e5):
        dA = delta(S_AL, f)
        Rh = R_of([(T, fill * S_AL, 0)], f, {0: 1.0}, 0.5, 1.0)
        Rcu = R_of([(T, S_CU, 0)], f, {0: 1.0}, 0.5, 1.0)
        print(f"   f={f:.0f}: homogenised {Rh*1e6:8.2f} uOhm/m (w=100 mm, no edges); solid Cu {Rcu*1e6:8.2f};"
              f" ratio {Rh/Rcu:.3f}")
        for t_target in (0.05e-3, 0.1e-3, 0.228e-3, 0.5e-3, 1e-3, 2e-3):
            layers, n, t = parallel_foils(T, fill, t_target, S_AL)
            R = R_of(layers, f, {0: 1.0}, 0.5, 1.0)
            print(f"      foils t={t*1e3:6.3f} mm n={n:4d} t/delta={t/dA:5.2f}: R={R*1e6:8.2f}  R/R_homog-1={R/Rh-1:+.4f}"
                  f"  writer fill*(t/d)^2/6={fill*(t/dA)**2/6:.4f}  R/R_Cu={R/Rcu:.3f}")

    print("\n== C. same foils, equal current per foil (ideal transposition), isolated slab")
    for f in (1e4, 1e5):
        dA = delta(S_AL, f)
        for t_target in (0.05e-3, 0.1e-3, 0.228e-3):
            layers, n, t = parallel_foils(T, fill, t_target, S_AL)
            lay2 = []
            cur = {}
            k = 0
            for (tt, ss, g) in layers:
                if ss > 0:
                    lay2.append((tt, ss, k))
                    cur[k] = 1.0 / n
                    k += 1
                else:
                    lay2.append((tt, ss, None))
            R = R_of(lay2, f, cur, 0.5, 1.0)
            Rdc = 1 / (fill * S_AL * T * W)
            est = fill ** 2 * T ** 2 * t ** 2 / (36 * dA ** 4)
            print(f"   f={f:.0f} t={t*1e3:6.3f} mm t/delta={t/dA:5.2f}: R/Rdc-1 exact={R/Rdc-1:8.4f}  writer 1-D est={est:8.4f}")

    print("\n== D. monotonicity of R(sigma) at fixed thickness (sweep 1e5..1.2e8 S/m)")
    for beta, name in ((0.5, "isolated (field both faces)"), (0.0, "field on one face")):
        for f in (1e4, 1e5):
            sg = np.geomspace(1e5, 1.2e8, 60)
            Rs = [R_of([(10e-3, s_, 0)], f, {0: 1.0}, beta, 1.0) for s_ in sg]
            mono = all(Rs[i + 1] < Rs[i] for i in range(len(Rs) - 1))
            print(f"   {name:28s} f={f:.0f}: strictly decreasing in sigma: {mono}")

    print("\n== E. multi-layer series winding (m layers, each carries I, field builds up on one side)")
    print("   R per layer relative to a solid Cu layer of the SAME thickness h (equal envelope)")
    for m in (1, 2, 4, 8):
        for f, h in ((1e5, 0.5e-3), (1e5, 1.0e-3), (1e4, 2.0e-3), (1e4, 1.0e-3)):
            def Rlayer(s_, hh=h, extra=None):
                layers = []
                cur = {}
                for k in range(m):
                    if extra is None:
                        layers.append((hh, s_, k))
                    else:
                        for (tt, ss, g) in extra:
                            layers.append((tt, ss, k if ss > 0 else None))
                    cur[k] = 1.0
                return R_of(layers, f, cur, 0.0, 1.0) / m
            rcu = Rlayer(S_CU)
            ral = Rlayer(S_AL)
            rlat = Rlayer(0.3 * S_AL)
            foils, nf, tf = parallel_foils(h, 0.3, h / 8 * 0.3, S_AL)
            rlat_x = Rlayer(None, extra=foils)
            # best solid Cu and Al foil of thickness <= h (macro-shape optimum)
            best_cu = min((Rlayer(S_CU, hh=x * h), x) for x in np.linspace(0.05, 1, 96))
            best_al = min((Rlayer(S_AL, hh=x * h), x) for x in np.linspace(0.05, 1, 96))
            print(f"   m={m} f={f:.0e} h={h*1e3:.1f} mm xi_Cu={h/delta(S_CU,f):4.2f}: Al/Cu={ral/rcu:5.3f} "
                  f"lattice(homog 0.3sAl)/Cu={rlat/rcu:5.3f}  lattice(8 parallel foils/layer)/Cu={rlat_x/rcu:5.3f}  "
                  f"best Cu foil (t={best_cu[1]:.2f}h)/Cu={best_cu[0]/rcu:5.3f}  best Al foil (t={best_al[1]:.2f}h)/Cu={best_al[0]/rcu:5.3f}")

    print("\n== G. strut-level (intra-foil) loss share in the parallel-connected stack of B")
    print("   loss of the deviation of J from each foil's mean J, divided by the loss of the mean J")
    for f in (1e4, 1e5):
        dA = delta(S_AL, f)
        for t_target in (0.05e-3, 0.1e-3, 0.228e-3, 0.5e-3):
            layers, n, t = parallel_foils(T, fill, t_target, S_AL)
            R_of(layers, f, {0: 1.0}, 0.5, 1.0)
            mean_part = sum(d_[2] for d_ in DETAIL)
            dev_part = sum(d_[3] for d_ in DETAIL)
            print(f"   f={f:.0f} t/delta={t/dA:5.2f}: intra-foil/mean-current loss = {dev_part/mean_part:.4f}"
                  f"   writer fill*(t/delta)^2/6 = {fill*(t/dA)**2/6:.4f}")

    print("\n== F. interleaved go/return Al foil stacks (writer's a2_laminations.py case b), exact 1-D")
    for f in (1e4, 1e5):
        for t, g, ngo in ((1.0e-3, 0.2e-3, 5), (0.25e-3, 0.1e-3, 20)):
            npl = 2 * ngo
            layers = []
            for k in range(npl):
                layers.append((t, S_AL, "go" if k % 2 == 0 else "ret"))
                if k < npl - 1:
                    layers.append((g, 0.0, None))
            loss, V = solve_stack(layers, f, {"go": 1.0, "ret": -1.0}, 0.0)
            Rgo = loss / 2 / 0.5
            print(f"   f={f:.0f} {ngo}+{ngo} foils t={t*1e3:.2f} mm: exact 1-D R'_go={Rgo*1e6:8.2f} uOhm/m"
                  f"  (equal-current model F(t/d)/(n s t w)={F1(t/delta(S_AL,f))/(ngo*S_AL*t*W)*1e6:8.2f})")
