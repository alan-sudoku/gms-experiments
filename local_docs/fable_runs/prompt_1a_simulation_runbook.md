# Prompt 1a: external simulation runbook

Date: 2026-11-13. Status: test run partly done and stopped on 2026-11-13. Done: tool installs, step 2 sanity checks (20/21 pass), L1 pilot end points only. Results and toolchain findings: `prompt_1a_external/README.md`.

**This is a test run.** Its main purpose is to find out whether the local physics-simulation toolchain works on this machine: tools install, sanity cases pass, run times and memory fit. Its second purpose is to record data from the open checks in `prompt_1a_review.md` ("What still needs external checking") as a record. The real test comes later, with its own plan.

The AI writes the **input generators, run scripts and result parsers**. The solvers themselves are third-party code.

Context: synthesis decision D3 stays at option (a): the 3-D lattice check is deferred to Phase 6. This test run does not replace that check and does not reopen D3. The spec does not depend on the outcome (D1(a)). Results go into `local_docs/` as a record only.

Validation level: **every result here is `derived`, and stays `derived`.** A computer simulation is not real data, whichever solver runs it and however well it agrees with 1a. No result from this runbook is promoted to a higher level. Real data means measurement (for example review item 4: printed lattice conductivity and R(f) of a printed bar).

Pass/fail columns below are the criteria the later real test would use. In this test run a "fail" is recorded as a finding to investigate (toolchain, mesh, or 1a), not as a verdict on Claim A.

---

## 1. Machine and tools

Local machine: Pop!_OS 24.04, 24 cores, 30 GB RAM, `gcc`, `make`, `cmake`, `wine`, `uv`, network access. No numpy in the system Python or in the project `.venv`. FreeCAD 1.1.1 AppImage at `<disk>/Program Files/` bundles `gmsh` and `ccx` (CalculiX: structural and thermal only, no electromagnetics).

| Tool | What it is | Used for | Install | Needs sudo |
|---|---|---|---|---|
| **FastHenry2** (github.com/ediloren/FastHenry2) | 3-D quasi-static filament (PEEC) solver with multipole acceleration, from Kamon, Tsuk and White 1994 | 3-D node-connected lattice (L1, C1) | `git clone`, `make` in `src/` (gcc only) into `~/opt/sim/fasthenry2/` | No |
| **GetDP 3.5.0** + **gmsh** | General finite-element solver (getdp.info, prebuilt static binary `getdp-3.5.0-Linux64c.tgz`) and mesher (`pip install gmsh`) | 2-D eddy-current finite elements (L2, L3) | Unpack to `~/opt/sim/getdp/`; gmsh into the sim venv | No |
| **Python sim venv** | numpy, scipy, gmsh, matplotlib | Generators and parsers | `uv venv ~/opt/sim/venv && uv pip install --python ~/opt/sim/venv numpy scipy gmsh matplotlib` | No |
| **FEMM 4.2** (femm.info, `femm42bin_x64_22oct2023.exe`) | 2-D finite-element magnetics, Windows | Third 2-D solver; the writer's A4.1 setup targets it directly (L4) | Run the installer under `wine` into the user wine prefix; drive by `wine femm.exe -lua-script=<file>` | No |
| **Elmer FEM** (`ppa:elmer-csc-ubuntu/elmer-csc-ppa`, has `noble` builds) | Finite-element multiphysics; `MagnetoDynamics2DHarmonic` (2-D) and `WhitneyAVHarmonicSolver` (3-D, edge elements, MPI) | 3-D lattice by finite elements (L5 pilot, C2); also lets FreeCAD's FEM workbench run magnetodynamics | `sudo apt` (see §2) | **Yes** |

Actual install state, versions and entry points (`~/opt/sim/bin/`): see `prompt_1a_external/README.md`.

Not used: CalculiX (no electromagnetics), FreeCAD alone (front end only; useful with Elmer for a GUI view of L2 cases).

## 2. Installs that need sudo (the user runs these)

Ask the user before each. Nothing in L1 to L4 needs them.

```bash
# S1. Elmer FEM, for L5 and C2, and for FreeCAD FEM magnetodynamics
sudo add-apt-repository ppa:elmer-csc-ubuntu/elmer-csc-ppa
sudo apt update
sudo apt install elmerfem-csc        # add elmerfem-csc-eg for ElmerGUI
ElmerSolver -v                       # check
```

In FreeCAD (optional): Edit → Preferences → FEM → Elmer, set the `ElmerSolver` and `ElmerGrid` paths (usually `/usr/bin/`).

## 3. Folder layout and script rules

```
local_docs/fable_runs/prompt_1a_external/
  README.md            how to run, tool versions, machine
  common/              shared geometry and material constants (same values as 1a)
  L1_fasthenry_lattice/  gen_*.py → *.inp → run.sh → parse.py → outputs/
  L2_getdp_busbar/       gen_*.py → *.geo, *.pro → run.sh → parse.py → outputs/
  L3_getdp_winding/
  L4_femm_busbar/        gen_*.py → *.lua → run.sh → parse.py → outputs/
  L5_elmer_pilot/
  C_cloud/               setup_vm.sh, the C1 and C2 inputs
```

Rules, so the runs are reproducible like the 1a scripts:

- Every case is generated from a Python script. No hand-edited solver input.
- `run.sh` records the tool version, command line, wall time and peak memory (`/usr/bin/time -v`) in `outputs/`.
- `parse.py` prints a table of computed value, expected value from §6 and pass/fail against the stated tolerance. A fail is reported as a fail, never retuned away.
- Materials: σ_Cu = 59.6 MS/m, σ_Al = 37.7 MS/m (65 % IACS, as in 1a), μ_r = 1. Results in µΩ/m (equal to W/m at 1 kA rms).
- Each tool runs a **sanity case with an exact answer first** (round wire against the Bessel solution for 2-D tools; DC resistance and a long thin wire's inductance for FastHenry). Do not run the real cases until the sanity case passes.

## 4. Local runs (fit 24 cores / 30 GB)

Run order: L1 first (the review's single most decisive check), then L2, L3, then L4 and L5 as extra cross-solvers.

### L1. FastHenry2: 3-D node-connected Al lattice (review item 1, finding 3)

The only part of 1a where lattice geometry itself was never computed.

- **Lattice:** simple-cubic, aluminium, pitch p = 0.5 mm, square struts of side t. Fill ρ̄ = 0.3 gives 3(t/p)² − 2(t/p)³ = 0.3, so t/p ≈ 0.363 (t ≈ 0.18 mm). Every strut is one FastHenry segment. Nodes at every lattice point.
- **Envelope:** 12 cells across the thickness (T = 6 mm) × 24 cells across the width (12 mm). This keeps the review's minimum of 12 cells across the thickness at a 2:1 aspect instead of the real 10:1, which needs the cloud (C1).
- **End effects:** two lengths, 24 and 48 cells. Report R′ = (R₄₈ − R₂₄)/(12 mm). Each end face is shorted to one node (`.equiv`), the port is between the two end nodes.
- **Size:** about 25 × 13 × 49 ≈ 16 000 nodes and 48 000 segments for the long bar. Start with 1 filament per strut (strut-level loss is under 5 % for t/δ ≤ 0.5), then rerun the two frequencies nearest T = 6 δ_eff with 2 × 2 filaments.
- **References, same tool, same envelope and lengths:** (a) solid bar with σ chosen to give the lattice's own DC resistance (homogenised, equal R_dc); (b) solid Al; (c) solid Cu. Solid bars are single segments with `nhinc`, `nwinc` and `rh`, `rw` refinement until R changes by under 0.5 %.
- **Frequency sweep:** take σ_eff from the lattice DC run, then choose about 15 log-spaced frequencies so that T/δ_eff runs from 0.5 to 10.
- **Pilot first:** 4 × 8 × (8 and 16) cells, to measure run time and memory, and to scale up.
- **Check against 2-D:** reference (a) at long length must match `eddy2d.py` for the same 6 × 12 mm cross-section within 2 %. If not, the reference is wrong and nothing else counts.

**Falsifies the 1a verdict** (from the review): the lattice's R_ac/R_dc is more than 20 % below reference (a)'s at T ≥ 6 δ_eff with struts thinner than δ; or the lattice's R′ falls below reference (c), solid Cu, at any frequency.

Expected outcome under 1a: lattice R_ac/R_dc within a few per cent of reference (a); lattice R′ above solid Cu everywhere, by roughly sqrt(σ_Cu/σ_eff) in the thick limit. Note that 12 cells only satisfy "pitch ≤ δ_eff/2" up to T = 6 δ_eff. Points above that are reported but flagged as under-resolved.

Estimated cost: unknown until the pilot runs. FastHenry is single-threaded; run frequencies as parallel processes, memory permitting.

### L2. GetDP: 2-D busbar values (review items 2 and 5, A4.1)

Geometry: 100 × 10 mm envelope in a circular air region of radius 300 mm, A_z = 0 on the outer boundary (only shifts L, not R). Net current imposed through a global current constraint. Mesh: element size ≤ δ/3 within 3 δ of every conductor surface, checked by one refinement.

| Case | Expected 10 kHz | Expected 100 kHz | Tolerance | Source |
|---|---|---|---|---|
| Round wire (sanity) | Bessel exact | Bessel exact | 0.5 % | — |
| Solid Cu | 178.4 | 564.7 | ±2 % | A4.1 |
| Solid Al | 224.7 | 709 | ±2 % | A3 |
| Homogenised lattice, 0.3 σ_Al | 414.5 | 1294 | ±2 % | A3 |
| Al tube, wall 1.399 mm (equal mass to lattice) | 212.1 | 709.4 | ±3 % | A4.1 |
| Cu tube, wall 0.414 mm (equal mass and envelope) | 265 | 541 | ±3 % | review finding 2 |
| Cu tube, wall 1.6 δ_Cu (0.33 mm at 100 kHz) | — | 524.8 | ±3 % | review `r1` |
| Explicit bundle, 240 × 24 strands of 0.228 mm, pitch 0.4167 mm, parallel | 409.4 | 1143.3 | ±5 % | A4.1 case 3 |
| Same bundle, ideal transposition (equal current per strand) | 91.4 | 382 (2 × 2 sub-cells); 484 expected fully resolved | 85–100 at 10 kHz; report 100 kHz | A4.1 case 4, A2.7, review finding 8 |

The 100 kHz bundle rows are the review's unconverged items (findings 8 and 10). Run them at two mesh levels and report the change. The review expects the 484 µΩ/m extrapolation to be a few per cent high.

Note: the transposed bundle needs one global current per strand (5 760 global unknowns). If GetDP is slow on that, use the quarter-symmetry of the bundle (1 440 strands).

### L3. GetDP: multi-layer winding in an imposed field (review item 3, finding 1)

Geometry: a 2-D core window with m series-connected foil layers spanning the full window height (Dowell's assumption), high-μ core (μ_r = 10⁴) on three sides. Each layer is its own conductor carrying the same current.

Cases per (m, f, h): solid Cu layer of thickness h, solid Al of thickness h, homogenised Al lattice (0.3 σ_Al) of thickness h, and solid Cu foils swept in thickness from 0.05 h to h to find the best thinner foil.

| m, f, h | Expected R(lattice)/R(Cu, same h) | Source |
|---|---|---|
| 4, 100 kHz, 0.5 mm | 0.61 | review `r3` §E |
| 8, 100 kHz, 0.5 mm | 0.48 | " |
| 4, 10 kHz, 2 mm | 0.86 | " |
| 8, 10 kHz, 2 mm | 0.77 | " |
| 4, 10 kHz, 1 mm | 0.79 | " |
| 8, 10 kHz, 1 mm | 0.38 (best thinner Cu foil 0.13) | " |

Also expected: solid Al / solid Cu at the same h between 0.74 and 0.99; best thinner Cu foil 0.06 to 0.35, beating the lattice by 2.3× to 13×. Tolerance ±3 % against the 1-D values when the layers span the window. Then add a 1 mm gap at each end of the layers to show how much the 2-D field changes the ratios (no expected value; report only).

### L4. FEMM under wine: third 2-D solver (optional)

The writer's A4.1 setup, cases 1 to 4 as listed there, with the same expected values as L2. FEMM's open-boundary shells replace the A_z = 0 circle. Case 4 is one series circuit over all strand blocks (review's note on A4.1). Use FEMM only as a cross-solver: if L2 and L4 disagree by more than 2 % on a solid bar, investigate before using either.

### L5. Elmer 3-D pilot (needs S1; optional locally)

Same lattice as the L1 pilot (4 × 8 × 16 cells), solved with `WhitneyAVHarmonicSolver` on a gmsh tetrahedral mesh of struts and surrounding air, MPI on 24 cores. Purpose: an independent 3-D method (finite elements, not filaments) on a case small enough to run here, and a dry run for C2. Pass: R′ within 3 % of FastHenry's pilot at three frequencies. The full 12-cell lattice is not expected to fit in 30 GB with a resolved air mesh; that is C2.

## 5. Cloud runs (exceed local memory)

**Not part of this test run.** Kept as notes for the later real test. The local pilots (L1, L5) supply the run-time and memory figures needed to size these.

Any provider, plain Ubuntu 24.04 VM. `C_cloud/setup_vm.sh` installs exactly the same tool versions as §1 (and Elmer via the PPA; sudo is normal on a rented VM). Inputs are generated locally and uploaded; only the text outputs come back. Shut the VM down after each run.

| Run | What | Why not local | VM size (estimate, confirm with the L1/L5 pilots) |
|---|---|---|---|
| **C1** | FastHenry2, lattice at the real 10:1 aspect: 12 × 120 cells × (24, 48) long; and 24 × 48 cells across (pitch ≤ δ_eff/2 up to T = 12 δ_eff) | about 230 000 segments; with 2 × 2 filaments near a million filaments | High memory, few cores (FastHenry is single-threaded; run frequencies in parallel): 256–512 GB RAM |
| **C2** | Elmer `WhitneyAVHarmonicSolver`, the L1 envelope (12 × 24 cells) with a resolved air mesh | millions of edge-element unknowns | 64–96 cores, 256–512 GB RAM, MPI |

Pass and falsification criteria are the L1 criteria. C2 against L1 at the same envelope is the strongest available check: two unrelated 3-D methods on the same geometry.

Cost is not estimated here. Check the provider's price for the chosen VM before starting, and confirm with the user.

## 6. Reporting

When the runs are done:

1. `prompt_1a_external/README.md`: tool versions, machine, wall times, peak memory, which tools worked and which did not, and the pass/fail tables from each `parse.py`. Every number is labelled `derived`.
2. A toolchain verdict: which tools are ready for the real test, what broke, and how big a lattice fits locally (this sizes the cloud runs).
3. A short addendum to `prompt_1a_synthesis.md`: any result that contradicts 1a, stated plainly with the numbers. D3 is unchanged.

Nothing from this run goes into `data/anchors/` or raises a validation level.

## 7. Order of work and what the user is asked

| Step | Action | Ask the user? |
|---|---|---|
| 1 | Create the sim venv; build FastHenry2; unpack GetDP | No (user-level installs in `~/opt/sim/`) |
| 2 | Sanity cases for FastHenry and GetDP | No |
| 3 | L1 pilot, then L1 full | No |
| 4 | L2, L3 | No |
| 5 | Install FEMM under wine; L4 | Yes, optional |
| 6 | S1 Elmer install (sudo); L5 | Yes, user runs the sudo commands |
| 7 | C1 / C2 on a rented VM | Not in this test run; part of the later real test |
