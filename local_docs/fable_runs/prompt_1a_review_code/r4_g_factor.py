"""Reviewer check R4: the field factor g used in the writer's Litz proximity estimate.

Purpose
    The writer's ideal-Litz estimate (answer A2.4, A2.7) multiplies the 1-D mean-square
    field inside a uniform-current W x T bundle, <H^2>_1D = (I/W)^2/12, by a factor
    g = <|H|^2>_2D / <H^2>_1D, reported as 1.552 for 100 x 10 mm (0.776 + 0.776) and
    -> 2 for a thin strip.  The writer computed it from closed-form rectangle fields.
    Here it is recomputed by brute force: the rectangle is divided into n x m equal cells,
    each replaced by a line current at its centre, and the field at every cell centre is the
    sum over all other cells (FFT convolution; the self-cell contributes zero at its own
    centre by symmetry).  The result is extrapolated in cell size (error ~ h^2).

Assumptions
    Magnetostatics of a uniform current density, mu = mu0, isolated bundle.
    numpy only.  Run: python3 r4_g_factor.py  (a few seconds).
"""
import numpy as np


def g_factor(Wd, Td, n):
    m = max(4, int(round(n * Td / Wd)))
    hx, hy = Wd / n, Td / m
    I_cell = 1.0 / (n * m)                       # total current 1 A
    ix = np.arange(-(n - 1), n)
    iy = np.arange(-(m - 1), m)
    DX, DY = np.meshgrid(ix * hx, iy * hy, indexing="ij")
    r2 = DX ** 2 + DY ** 2
    r2[n - 1, m - 1] = np.inf                    # self term zero
    kx = -DY / (2 * np.pi * r2)                  # Hx per unit current
    ky = DX / (2 * np.pi * r2)
    shape = (3 * n, 3 * m)
    src = np.zeros(shape)
    src[:n, :m] = I_cell
    Fs = np.fft.rfft2(src)
    Hx = np.fft.irfft2(Fs * np.fft.rfft2(kx, shape), shape)[n - 1:2 * n - 1, m - 1:2 * m - 1]
    Hy = np.fft.irfft2(Fs * np.fft.rfft2(ky, shape), shape)[n - 1:2 * n - 1, m - 1:2 * m - 1]
    one_d = 1.0 / (12 * Wd * Wd)
    return np.mean(Hx ** 2) / one_d, np.mean(Hy ** 2) / one_d


if __name__ == "__main__":
    for Wd, Td in ((100.0, 10.0), (100.0, 1.0)):
        res = []
        for n in (500, 1000, 2000):
            gx, gy = g_factor(Wd, Td, n)
            res.append((n, gx, gy))
            print(f"{Wd:.0f} x {Td:g}: n={n:5d}  g_parallel={gx:.4f}  g_normal={gy:.4f}  g={gx+gy:.4f}")
        (n1, a1, b1), (n2, a2, b2) = res[-2], res[-1]
        ga = (4 * (a2 + b2) - (a1 + b1)) / 3
        print(f"   Richardson-extrapolated g = {ga:.4f}   (writer: 1.552 for 100 x 10, 1.910 for 100 x 1)")
