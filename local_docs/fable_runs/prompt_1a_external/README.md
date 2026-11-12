# Prompt 1a external simulation: test run

Plan: `../prompt_1a_simulation_runbook.md`. This is a **test run** of the local simulation toolchain. All results are level `derived`; no simulation result here is real data.

## Tool install state (2026-11-13)

Machine: Pop!_OS 24.04, 24 cores, 30 GB RAM, gcc 13.3.0, wine 9.0.

All tools are user-level installs under `~/opt/sim/` (about 420 MB). Use the entry points in `~/opt/sim/bin/`.

| Tool | Version | Entry point | Source | State |
|---|---|---|---|---|
| Python sim venv | Python 3.12; numpy 2.5.4, scipy 1.18.1, gmsh 4.15.2, matplotlib 3.11.2 | `~/opt/sim/venv/bin/python` | PyPI via `uv` | Installed |
| gmsh | 4.15.2 (pip wheel) | `~/opt/sim/bin/gmsh` (wrapper; the venv's own `gmsh` script calls the system Python and fails) | PyPI | Installed |
| GetDP | 3.5.0, prebuilt `getdp-3.5.0-Linux64c.tgz` | `~/opt/sim/bin/getdp` | getdp.info | Installed, smoke test passed |
| FastHenry2 | github.com/ediloren/FastHenry2, commit `363e43e` (2015-09-08) | `~/opt/sim/bin/fasthenry` | Built from source | Built, smoke test passed |
| FEMM 4.2 | `femm42bin_x64_22oct2023.exe` (sha256 `fdc5047d…9eb17253`) | `~/opt/sim/wine_femm/drive_c/femm42/bin/femm.exe` (wine prefix `~/opt/sim/wine_femm`) | femm.info | Installed by the user (2026-11-13). Files present; not yet run. |
| Elmer FEM | package `elmerfem-csc 9.0-0ppa0-202611102349~16093051a~ubuntu24.04.1` (solver reports version 26.2, compiled 2026-11-10) | `/usr/bin/ElmerSolver`, `ElmerSolver_mpi`, `ElmerGrid`; `mpirun` present; modules `MagnetoDynamics.so` (3-D, includes the Whitney AV solvers), `MagnetoDynamics2D.so`, `CircuitsAndDynamics.so` in `/usr/share/elmersolver/lib/` | Ubuntu PPA | Installed by the user (2026-11-13). Version check only; not yet run. ElmerGUI not installed (not needed). |

FastHenry2 build: `make fasthenry CFLAGS="-O2 -DFOUR -m64 -std=gnu89 -fcommon -w -Wno-error=implicit-function-declaration -Wno-error=implicit-int -Wno-error=incompatible-pointer-types -Wno-error=int-conversion"`. The 2015 source does not build under gcc 13 defaults. Warnings are suppressed (`-w`), so 64-bit pointer bugs would not show at compile time; the smoke test is the check.

## Smoke tests (toolchain only, not physics checks)

| Tool | Test | Result |
|---|---|---|
| FastHenry2 | Bundled example `pin-con7.inp` (7 pins, 1 Hz), output against the shipped reference `Zc_pin_con7.mat` | Identical, all 111 lines. 7.6 s, 25 MB. |
| GetDP + gmsh | Bundled example `magnet.pro` (2-D magnetostatics), meshed with gmsh 4.15.2, solved with both the scalar (φ) and vector (a) potential formulations | Both solve on 2 957 triangles. ∫\|B\|² dA = 3.761e-3 (φ) and 3.821e-3 (a), 1.6 % apart on this coarse mesh, the expected size of the gap between the two formulations. |

These show the tools run. They do not check eddy-current accuracy; that is step 2 below.

## Step 2: sanity checks (`s2_sanity/`)

Script `s2_sanity/s2_sanity.py`, output `s2_sanity/outputs/s2_sanity.txt`, shared driver `common/simtools.py`. Total run time 22 s. **20 of 21 checks pass.** Level `derived`.

| Check | What | Result |
|---|---|---|
| G1 | GetDP, isolated round Cu wire, R_ac/R_dc against the exact Bessel solution, a/δ = 0.5 to 8, surface elements δ/4 and δ/8 | All pass. Finer mesh within 0.084 % (worst, a/δ = 8). |
| G2 | GetDP against the 1a solver `eddy2d.py`, 10 × 10 mm Cu bar, 1/10/100 kHz | All within +0.10 %. Two unrelated methods (finite elements vs volume integral equation). |
| F1 | FastHenry DC resistance of one bar against L/(σA) | Exact. |
| F2 | FastHenry partial self-inductance, 1 × 1 mm × 1 m bar, against the GMD formula | +0.001 %. |
| F3 | FastHenry 10 × 10 mm Cu bar, R′ by length differencing (1 m, 2 m) against `eddy2d.py` | 41 × 41 graded filaments: +0.025 %, −0.044 %, −0.75 % at 1/10/100 kHz (all pass). 21 × 21: −3.5 % at 100 kHz (**FAIL**, filaments too wide for δ; recorded, expected). |

Toolchain lessons from step 2:

- **GetDP sign convention:** its global U is the drop with E = −(∂A/∂t + ur), so Z = −U/I. R from U/I and from the integrated loss agree to 11 digits.
- **FastHenry exit code is junk** (123 on success). The 2015 `main()` has no `return`. Success is judged by "All impedance matrices dumped" in the log.
- **FastHenry multipole on a single bar is slow.** It splits a single bar into 8 pieces along its length; a 41 × 41 bar ran > 10 min at 2.2 GB. For single bars use the direct solver: `-s ludecomp -m direct -a off` (seconds).
- **FastHenry length differencing needs L ≳ 4 × the bar width.** Test at 2.26 MHz on a 1.18 mm square bar against the 2-D value: L = 2/4 mm gives −4.2 %, 8/16 mm −0.7 %, 30/60 mm −0.1 % (graded filaments).

## Installs done by the user

Both installed on 2026-11-13 with these commands.

FEMM under wine (optional, L4). Installs into its own wine prefix so `~/.wine` is untouched:

```bash
export WINEPREFIX=$HOME/opt/sim/wine_femm WINEARCH=win64
wineboot -i
wine ~/opt/sim/femm_dl/femm42bin_x64_22oct2023.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART '/DIR=C:\femm42'
```

Elmer FEM (L5 pilot; also lets FreeCAD's FEM workbench run magnetodynamics):

```bash
sudo add-apt-repository ppa:elmer-csc-ubuntu/elmer-csc-ppa
sudo apt update
sudo apt install elmerfem-csc        # elmerfem-csc-eg adds ElmerGUI
ElmerSolver -v
```

## L1 pilot: stopped early (`L1_fasthenry_lattice/`)

Status: **stopped on 2026-11-13 at the user's request, before the 12-frequency sweep ran.** Script `L1_fasthenry_lattice/l1_lattice.py`; the finished cases are recorded by `l1_partial_record.py` in `outputs/l1_pilot_partial.txt`. Level `derived`. This is a toolchain test, not a verdict on Claim A.

Pilot geometry: simple-cubic Al lattice, 8 × 4 cells, pitch 0.5 mm, strut 0.1816 mm (fill 0.3), envelope 4.18 × 2.18 mm. Lengths 32 and 64 cells (16 and 32 mm), R′ by length differencing. References in the same tool: equal-DC solid (`hom`), solid Al, solid Cu.

### Results that finished

| Quantity | Value |
|---|---|
| Lattice DC R′ against exact 1/(σ t² N_lines) | 17 868.00 against 17 868.04 µΩ/m (−0.0002 %) |
| σ of the equal-DC solid | 0.1627 σ_Al. This is the axial metal fraction of this small envelope (45 axial lines). It is above the infinite-lattice value (t/p)² = 0.132 because of the edge lines, and above the 1a isotropic estimate 0.100 σ_Al (τ = 3). |
| T/δ_eff = 0.5 (2.17 kHz), per-length | R′: lattice 17 877, equal-DC solid 17 876, Al 2 966, Cu 1 931 µΩ/m. Lattice R/R_dc over equal-DC solid R/R_dc = 1.0001. Lattice/Cu = 9.26. Near-DC regime, so close agreement is expected. |
| T/δ_eff = 10 (868 kHz) | **No per-length lattice value**: the 64-cell lattice case was stopped. Single 32-cell length only, ends included (not a per-length result): lattice/equal-DC solid 0.962, lattice/Cu 3.14. This point is outside the falsifier regime anyway: struts 2.06 δ_Al thick, pitch 2.3 δ_eff, so no homogenisation is expected. |
| Falsifier C1 (T ≥ 6 δ_eff with struts thinner than δ) | Not reachable at pilot size, as the runbook expected. |
| Falsifier C2 (lattice R′ below Cu) | Not triggered at the points computed (9.26 per length; about 3.1 single length). Only 2 of 12 frequencies ran. |
| Equal-DC solid against the 2-D solver (`hom/2D` column) | Not produced: the run stopped before the table step. |

### Toolchain findings

1. **FastHenry's default preconditioner is unusable on a lattice.** For a 3 796-filament lattice it spent about 900 s building the preconditioner and 0.5 s in GMRES. Timed options on the same deck: `-p off` 2.4 s; `-p diag` 181 s; `-p seg` 228 s; `-p shells` over 300 s (timed out); direct solve (`-s ludecomp -m direct -a off`) 11 s. All finished options give R = 0.000286009 Ω, identical to 6 digits (direct: 0.00028601). X differs by 0.06 % between multipole and direct. `l1_lattice.py` now uses `-p off` by default.
2. **Memory is about 51 kB per filament** with multipole and `-p off`: 94 900 filaments (3 796 segments × 25) finished at 4.97 GB in 460 s; 191 700 filaments reached 9.8 GB (still iterating after more than 8 min when stopped). `l1_lattice.py` now schedules jobs within a memory budget (`--mem-gb`, default 14), biggest first.
3. **DC lattice by direct solve:** 64-cell length (3 796 segments) took 98 s and 0.94 GB.
4. **Single-bar references are cheap:** solid bars with up to 41 × 41 filaments solve directly in about 2–3 s and about 0.1 GB.
5. **Sizing the full L1 check (estimate, from finding 2; not run).** Length differencing needs lengths of at least about 4× the bar width (step 2). In the falsifier regime, struts are 0.5 to 1.5 δ_Al thick, which needs 3 × 3 filaments per strut.
   - 12 × 24 cells (W = 12.2 mm, lengths 100/200 cells): about 187 000 segments, about 1.7 million filaments, about 90 GB.
   - 12 × 12 cells (W = 6.2 mm, lengths 50/100 cells): about 48 000 segments, about 430 000 filaments, about 22 GB.

   Neither fits beside the 15–17 GB free on this machine. **The decisive 12-cell check therefore belongs on the cloud (C1) or in Elmer (C2), as the runbook planned.** A 12 × 12 run on a 64 GB machine looks feasible.

### Not done in this test run

- The full 12-frequency pilot sweep, and the `hom/2D` cross-check against `eddy2d.py`.
- L2 and L3 (GetDP), L4 (FEMM), L5 (Elmer). FEMM and Elmer are installed but have not run.
