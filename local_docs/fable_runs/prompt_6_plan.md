# Prompt 6 plan (S1): combining degradation mechanisms (OQ-20)

Status: S1 planner output. Everything here is a claim at level `derived` (unverified).

**Provenance.**
- Files read: `local_docs/fable_questions.md`, section "Prompt 6: combining degradation mechanisms (OQ-20)", the fenced text block (lines 231–252), plus the two context lines above it. The directory listing of `local_docs/fable_runs/` was printed (file names only; no other file was opened). `CLAUDE.md` was supplied automatically.
- No code was run. No web search was made. No spec file (`docs/spec/`) was read, so statements about what GMS-220 and GMS-230 contain rest only on the prompt's summary.
- All numbers below are planner hand arithmetic. They are given as **UNSURE expected values**; the implementer's computed values supersede them. Every number is tied to a spec row (section 3) by row id. Literature values that no row computes are marked "literature, UNSURE" and go to the citation checker.
- Tags: **MEMORY** = value quoted from the planner's memory (registry `Mxx`, section 3.1). **LOOKUP** = value the implementer or citation checker must read from a named source (registry `Lxx`). **UNSURE** = not verified.

**Notation used throughout.**
- `t` age of the unit (s). `τ₀` fatigue life at the pristine section (s). `t_c` time for recession to consume the whole load-bearing section (s). `ρ = τ₀/t_c` (dimensionless; not density, which is written `ρ_m`).
- `x(t)` fraction of the load-bearing dimension lost (0 to 1). `x_e = x(τ)` at end of life. `x_allow` allowed fraction (static strength, perforation).
- `m = −1/b` Basquin life exponent. `p` exponent of stress on remaining section, `σ_a ∝ (1−x)^(−p)`. `q = p·m`.
- `F_cur = τ(current rule)/τ(coupled)`; `F_min = τ(minimum of separate mechanisms)/τ(coupled)`. F > 1 means the simple rule overstates life (non-conservative for the side it is applied to).
- Year convention: 1 yr = 365.25 d = 3.15576e7 s.

---

## 1. Claims

Format: statement; confidence; falsifier; spec rows. Derivations are in section 2.

### M1: additivity of rates

**M1.1 Additivity is exact as bookkeeping; the error is in the state at which each term is evaluated.**
Σ̇_total(t) = Σ_i Σ̇_i(state(t)) holds exactly when each term is a distinct flux-times-force product and each is evaluated at the actual coupled state (section thickness, scale thickness, temperature, damage). The current rule evaluates every term at the pristine, isothermal state. So the question "is the sum exact, a bound, or wrong" is a question about the sign of each coupling, not about summation.
Confidence: high. Falsifier: a coupled case where the total differs from the sum of terms evaluated at the coupled state (would indicate a missing or double-counted term). Rows: A1, A7, A8.

**M1.2 The sum over-counts (upper bound, by a double count) when Σ̇_op is taken from a measured input–output power balance that already contains hysteresis or Joule terms.** The prompt's rule that reaction heat inside b_degrad is not counted again is correct, and the reaction heat is too small to matter as self-heating (ΔT below 0.01 K for the worked example).
Confidence: high (first sentence), high (second). Falsifier: A12 gives ΔT above 0.1 K. Rows: A12.

**M1.3 Direction. At fixed duty (fixed current, heat flow, mass flow, load amplitude) with monotone degradation, the pristine-state sum is a lower bound on the true total. The direction reverses in at least four cases:** constant-voltage operation (P ∝ 1/R); wall recession that widens a flow channel at fixed mass flow; displacement-controlled cyclic loading; self-heating that dries a surface in atmospheric corrosion. So "the sum is a lower bound" is not a general rule; it needs a per-coupling sign.
Confidence: high for the fixed-duty direction, medium for the list being complete. Falsifier: any A4 or A9 case with the opposite sign to the one stated in section 2.2. Rows: A1, A2, A4, A9, C15.

**M1.4 (a) Section thinning and scale thickening.** For a rate that scales as (1−x)^(−p), the life-averaged multiplier over linear recession is M = [(1−x_e)^(1−p) − 1]/((p−1)·x_e) (p ≠ 1) or −ln(1−x_e)/x_e (p = 1); for parabolic recession with p = 1 it is −2·(a + ln(1−a))/a² with a = x_e. First-order error of the pristine-state value: p·x_e/2 (linear), 2·p·x_e/3 (parabolic). The sum is adequate to 5 % when x_e < 0.094/p (linear; exact p = 1 value) or x_e < 0.071 (parabolic, p = 1). A resistance in series (fouling, oxide film) adds linearly: multiplier 1 + R_f/R₀.
Confidence: high (mathematics); medium (that p is 1 for Joule heating at constant current and n−1 for hysteresis in a wall, see 2.2). Falsifier: A1/A2 closed forms disagree with quadrature by more than tolerance; A3 thresholds outside the stated ranges. Rows: A1, A2, A3, A5.

**M1.5 (b) Hysteresis rising with damage.** It is a bounded multiplier on one term: life-average factor 1 + β/(γ+1) for ψ = ψ₀·(1 + β·D^γ). No public anchor for β, γ is known to the planner; the effect on the total is the fatigue share times this factor. For the worked example the fatigue-hysteresis share is about 0.10 (E3), so even β = 5, γ = 1 changes the total by about 25 %.
Confidence: low (magnitude), high (form). Falsifier: measured ψ(N/N_f) data with a life-average factor outside [1, 1+β_max]; or E3 share far from 0.1. Rows: A10, E3.

**M1.6 Summing hysteresis over load cases is exact only for linear (viscoelastic) damping at distinct frequencies or for sequential cases. For rate-independent hysteresis (the usual metal behaviour), concurrent cases give more than the sum even for exponent n = 2**, because the closed loops are those of the combined history: ratio ≈ (1 + 2s + φ·s²)/(1 + φ·s²) for n = 2 (s = σ₂/σ₁, φ = ν₂/ν₁), maximum 1 + 1/√φ at s = 1/√φ. For same-frequency in-phase loads the ratio is (1+s)²/(1+s²), up to 2. An upper bound is ν_max·V·J·(Σσ_l)^n/T₀.
Confidence: medium. Falsifier: A11 rainflow dissipation equal to the separate sum within 2 % for n = 2 at s = 1/3, φ = 9. Rows: A11 (uses B5).

**M1.7 (c) Scale loss. The pure parabolic law is a lower bound on metal consumed whenever scale is lost; "parabolic + linear" is an upper bound, and max(parabolic, linear) is a lower bound.** For the Tedmon paralinear model the sum overstates by at most about 1.37 (near θ = k_l²·t/k_p′ ≈ 3.4) and the max understates by at most about 1.47 (at θ = 2). For periodic complete spallation the sum overstates by 1 + 1/√N (N spall events; 2 at N = 1) and the pure parabolic law understates by √N. Both bounds fail if the regrown scale is less protective than the first (breakaway chemistry change).
Confidence: high (bounds within the two models), medium (extremal values, hand computed). Falsifier: any θ in D1 with U < m or m < L; maximum of U/m outside [1.35, 1.39]. Rows: D1, D2, D3, D4, D8.

**M1.8 (c) Criteria for scale cracking and spallation.** Parabolic kinetics must be rejected when (i) scale thickness at end of life exceeds δ_c = G_c·(1−ν_ox)/(E_ox·ε²), ε the in-plane mismatch strain, or (ii) the cyclic strain amplitude σ_a/E exceeds the scale cracking strain ε_c = K_Ic/(f·E_ox·√(π·c)). For the worked-example strain amplitude (about 1.5e-3) the crossover flaw size is about 0.8 µm for an alumina-like scale; a nanometre native film on aluminium is far below it, a thermally grown scale of several µm is above it.
Confidence: medium (form), low (input values). Falsifier: published critical strains for alumina or chromia scales outside 1e-3 to 1e-2 (literature, UNSURE). Rows: D5, D6.

**M1.9 (d) Temperature coupling.** With part temperature T = T_env + R_th·P(T, x), a rate with activation energy Q is multiplied by exp[(Q/R)·(1/T_env − 1/T)]. The sum is adequate to fraction ε when ΔT < ε·R·T²/Q (0.73 K for Q = 50 kJ/mol at 300 K; 2.9 K for 200 kJ/mol at 1200 K, both for ε = 5 %; twice these for K_ox, which goes as √k_p). Electro-thermal loop: ΔT = ΔT₀/(1 − x − α·ΔT₀), runaway at x = 1 − α·ΔT₀. With ΔT₀ = 5 K and Q = 50 kJ/mol the time to lose half the section is about 0.64 of the isothermal-at-T_env value; with ΔT₀ = 20 K about 0.19.
Confidence: high (form), medium (numbers). If the model prescribes the part temperature rather than the environment temperature the coupling is already included; which of the two GMS uses is not known to the planner (UNSURE). Falsifier: A6 thresholds or A8 ratios outside the stated ranges. Rows: A6, A7, A8.

**M1.10 (d) For atmospheric (wet-film) corrosion the Arrhenius direction can be wrong: self-heating of about 3 K takes a surface from 95 % to below 80 % relative humidity and can switch the corrosion off.** So for g or s in humid air, "isothermal" can overstate corrosion.
Confidence: medium. Falsifier: A9 threshold above 10 K. Rows: A9.

**M1.11 Summing K_ox over separate surface patches is exact if all patches share one clock and one temperature. It is wrong (low) when patches are renewed at different times, because K·√t is concave in t.**
Confidence: high. Falsifier: D4 long-run slope differing from √(2·k_p·F_A/Δt) by more than tolerance. Rows: D3, D4.

**M1.12 Adequacy criterion.** The pristine-state sum is adequate to ε when Σ_i w_i·e_i ≤ ε, with w_i the share of term i and e_i its first-order coupling error (p_i·x_e/2 for section loss; Q·ΔT/(R·T²) for self-heating; R_f/R₀ averaged for series resistances; √N − 1 for spallation). The fatigue life is far more sensitive than any rate: its coupling error is q·ρ/2 with q ≈ 10 to 20.
Confidence: medium. Falsifier: E5 first-order estimate differing from the exact multipliers by more than 30 % of the error at x_e ≤ 0.1. Rows: E5, A3.

### M2: wearout under several mechanisms

**M2.1 Sequential load cases: τ_Miner ≤ τ_min ≤ L·τ_Miner (L = number of load cases).** The minimum is never conservative relative to Miner and is off by at most the number of load cases.
Confidence: high. Falsifier: any B1/B2 sample with ratio outside [1, L]. Rows: B1, B2.

**M2.2 The Miner–minimum gap is usually small because S–N curves are steep.** The ratio exceeds 1.1 only when two frequency-normalised stress amplitudes lie within a factor 10^(±1/m) of the equal-life point (±26 % for m = 9.8).
Confidence: high. Falsifier: B1 window width outside [0.76, 0.82] to [1.22, 1.30]. Rows: B1, B6.

**M2.3 Concurrent load cases: both the minimum and Miner-over-cases are non-conservative, by up to about (1+s)^m relative to the dominant case alone** (2.5 for s = 0.1; 6 for s = 0.2; about 890 for s = 1, m = 9.8), because the damaging cycle is the envelope cycle of the combined history. Cycle counting on the combined history is required. This is a larger defect than "no Miner summation" if GMS-220's load cases can act at the same time (the hysteresis rule's wording "distinct frequencies or uncorrelated loads" suggests they can; UNSURE).
Confidence: high (mathematics), medium (applicability). Falsifier: B5 rainflow damage within 20 % of the separate-case Miner sum at s = 0.2. Rows: B4, B5.

**M2.4 Miner itself is uncertain by a factor of about 3 to 5.** Under the Manson–Halford damage-curve approach, the Miner sum at failure for two-level loading ranges from about 0.67 to 1.33 (life ratio 10), 0.41 to 1.59 (100), 0.22 to 1.78 (1000); high-then-low is the non-conservative order. Design codes use allowable sums of 0.3 to 0.5 (literature, UNSURE).
Confidence: medium. Falsifier: B3 extrema outside ±0.02 of these values (would show a planner arithmetic error); two-level test data with sums far outside the band (would show the approach itself is wrong). Rows: B3.

**M2.5 Section loss under load control. With linear recession and Miner accumulation the coupled life has a closed form: τ_c = t_c·{1 − [1 + (q−1)·ρ]^(−1/(q−1))}.** "Minimum of separate mechanisms" (fatigue at pristine section; recession through the section) overstates life by at most 1/(1 − q^(−1/(q−1))), reached at ρ = 1: about 4.4 for a wall under membrane load (q = 9.8), 6.8 for an axially loaded round strut (q = 19.6). With an allowable section loss x_allow = 0.2 the maximum falls to about 1.8. With parabolic recession (oxidation) the maximum at ρ = 1 is larger, about 12 for q = 9.8.
Confidence: high (closed form), medium (physical validity of Miner under continuously rising stress; see M2.10). Falsifier: C5 numerical first-passage time differs from C4 by more than 0.1 %; C6 maximum not at ρ = 1 or outside [4.2, 4.6]. Rows: C4, C5, C6, C7, C9.

**M2.6 The current rule (fatigue only; recession not modelled) is worse than "minimum of separate mechanisms": F_cur is unbounded as ρ → ∞.** A lightly stressed thin feature has τ₀ → ∞ but is consumed at t_c. Missing recession wearout is a larger defect than missing Miner summation.
Confidence: high. Falsifier: C6 shows F_cur bounded as ρ grows (expected instead: F_cur ≥ ρ, about 1.55·ρ at ρ = 1e3 for q = 9.8). Rows: C4, C6.

**M2.7 Environment-modified S–N behaviour dominates.** For an aluminium alloy in saline environment at a stress amplitude equal to the air fatigue strength at 5e8 cycles, with knockdowns on stress of 0.9 at 1e5 cycles and 0.4 at 1e8 cycles (L01, UNSURE), the life factor is about 150 (about 40 to 350 for a 1e8 knockdown of 0.6 to 0.25). The factor grows as stress falls and is unbounded for a material with a fatigue limit in air. For welded steel a public design code gives 3 at high stress, rising to about 9 at 30 MPa and 21 at 20 MPa (L03). For humid air relative to laboratory air the factor is small, because laboratory-air S–N data already contain a moist-air effect (literature, UNSURE, low confidence).
Confidence: medium (direction and order of magnitude), low (aluminium input values). Falsifier: L01 lookup gives k₈ > 0.8 (then the factor is below 10). Rows: C10, C16.

**M2.8 The effects do not multiply.** Once the environment S–N curve is used, the life is so short that section loss matters only at low frequency or very thin sections: additional factor about 1.02 at 1 Hz, 1.15 at 0.1 Hz, 2.3 at 0.01 Hz for a 0.3 mm wall attacked on both sides at 10 µm/yr.
Confidence: medium. Falsifier: C11 values outside ±15 % of these. Rows: C11.

**M2.9 For passive alloys (aluminium), localised attack matters more than uniform section loss.** Treating a pit as a crack-like defect (Kitagawa–El Haddad), a 100 µm pit lowers the endurance stress to about 0.74 of pristine (a₀ ≈ 120 µm), a life factor of about 20 at the air slope; with pit depth = PF·r·t and PF = 10, r = 10 µm/yr the coupled life factor is about 12, and a 0.3 mm strut is perforated in 1.5 yr.
Confidence: low to medium (model form medium; PF, ΔK_th, pit growth law low). Falsifier: pre-pitted fatigue data (L06) showing life factors below 2 for 100 µm pits. Rows: C12, C13.

**M2.10 "Minimum of separate mechanisms" is not always non-conservative.** It is conservative or neutral when: (i) loading is displacement-controlled (bending under imposed curvature: fatigue never governs for ρ > 1/(m+1) ≈ 0.093, and for ρ = 0.05 the true life is 1.39·τ₀); (ii) Basquin is used without an endurance limit for a material that has one in a benign environment (unbounded conservatism); (iii) stress rises monotonically, where nonlinear accumulation predicts Miner sums above 1 (up to about 1.8); (iv) dissolution outruns short cracks (ν below about 3e-3 Hz at 10 µm/yr); (v) oxide-induced crack closure raises the near-threshold resistance in moist environments (literature, UNSURE); (vi) the separate lives were taken from design (lower-bound) curves.
Confidence: high for (i), (ii); medium for (iii); low for (iv), (v). Falsifier: C15 ratio below 1; C14 ratio below 1. Rows: C14, C15, C17, B7.

**M2.11 Screening rule for τ_wearout (provisional; see section 5).** τ_M = [Σ_l ν_l/N_l]⁻¹ from an S–N curve valid for the service environment (after cycle counting if cases are concurrent); t_c = h₀/(n_s·r); τ_wearout = min(τ_c(τ_M, t_c, q), x_allow·t_c). Ignore section loss when q·τ_M/(2·t_c) < 0.05. Bounds: max over x* of min(x*·t_c, τ_M·(1−x*)^q) ≤ τ_c ≤ min(τ_M, t_c).
Confidence: medium. Falsifier: C8 finds any ρ with lower bound above τ_c. Rows: C4, C7, C8.

**M2.12 Oxidation-assisted initiation gives a time-based cap independent of cycle count:** t_i = a_tr²/(2·k_p′) with a_tr = (1/π)·(ΔK_th/(Y·Δσ))². About 90 days for k_p′ = 1e-16 m²/s, Δσ = 400 MPa, ΔK_th = 5 MPa√m.
Confidence: low. Falsifier: high-temperature fatigue data where initiation life does not scale with 1/k_p′. Rows: D7.

### M3: direction of error per side

**M3.1 A life error matters through the embodied (replacement) share.** With shares at the modelled life (w_emb + w_ox + w_lin = 1), c_true/c_model = w_emb·F + w_ox·√F + w_lin·M, F the life overstatement and M the rate multiplier.
Confidence: high, conditional on the cost having the form (embodied + K_ox·√τ + ∫rates)/τ, which the planner infers from the prompt and has not read in the spec (UNSURE). Rows: E1.

**M3.2 Direction table (section 2.7).** Simplifications that understate a side's cost: pristine-state rates at fixed duty; parabolic-only oxidation; minimum over load cases; separate treatment of concurrent loads; air S–N curve in an aggressive environment; no section-loss coupling; no recession wearout; no pitting; isothermal oxidation. Simplifications that overstate it: paralinear sum; Basquin without endurance limit; isothermal wet corrosion with self-heating; double-counted Σ̇_op. Neutral: reaction heat counted once.
Confidence: medium. Falsifier: any row whose sign contradicts the table. Rows: A1, A4, A9, B7, C4, C10, C15, D1.

**M3.3 Every coupling number scales as 1/h₀ (or as surface/volume), so ignoring couplings favours the side with thinner features.** If g is the thin-featured side, the current rule is non-conservative for the claim "g is better". For the worked pair (g: 0.3 mm strut; s: 3 mm wall, one side attacked; same alloy, stress, 10 µm/yr), life is overstated by about 7.0 for g and 1.24 for s; the cost ratio g/s is understated by about 5.7 at w_emb = 1 and 3.6 at w_emb = 0.5.
Confidence: medium (that g is the thin side is an assumption, UNSURE). Rows: E2, E5.

**M3.4 A one-directional bound construction exists but is conditional.** Lower bound on cost (use for s): pristine-state rates, life = min(τ_M, t_c), oxidation = max(parabolic, linear). Upper bound (use for g): end-of-life rates, life = the C8 lower bound with an environment S–N curve and a reduced damage sum, oxidation = parabolic + linear. It is valid only where each coupling is monotone-accelerating; for the sign-reversal cases of M1.3 the two ends swap. No finite upper bound exists without environment data (S–N in environment, pitting factor, spall onset): there the model must reject, not bound.
Confidence: medium. Falsifier: C8 bound violated; any sign-reversal case not in the list. Rows: C8, D1, E4.

**M3.5 Common-mode errors cancel only partly.** A knockdown common to both sides (same alloy, same environment) cancels in the ratio only if both sides have the same shares and the same h₀; with different geometry it does not (E2).
Confidence: medium. Rows: E2.

**M3.6 The bound is loose for thin features.** For the worked g unit the upper-bound cost is about 5.5 times the modelled cost (w_emb = 0.5), so a robust "g is better" needs a modelled cost ratio g/s below about 0.18. A third verdict class "undetermined" is needed.
Confidence: medium. Rows: E4.

### M4: default rules

**M4.1 Rates default: pristine-state sum at fixed duty and prescribed part temperature, with oxidation as parabolic + linear, valid while every coupling number is small (x_e ≤ 0.1/p, ΔT_self ≤ 0.05·R·T²/Q, no spall or scale cracking, no concurrent correlated loads); error then ≤ about 5 % per term.**
Confidence: medium. Rows: A3, A6, D5, D6, E5.

**M4.2 Wearout default: Miner sum over load cases with an environment-valid S–N curve, coupled to linear section loss through the closed form of M2.5, capped by x_allow·t_c.** It reduces to the current rule when one case dominates and ρ → 0, and to the recession life when ρ → ∞.
Confidence: medium. Rows: C4, C5, C7, C8.

**M4.3 Anchors exist for each rule but the aluminium corrosion-fatigue S–N anchor is not identified with certainty.** Rates: paralinear data (Tedmon 1966; Opila and Hann 1997), electrical-resistance corrosion probes for R ∝ 1/(h₀ − h). Wearout: air versus free-corrosion design S–N curves for welded steel (DNV-RP-C203), pre-pitted aluminium fatigue tests (L06).
Confidence: low to medium (UNSURE on availability and exact tables). Rows: C16, D1 (L05), C13 (L06).

**M4.4 Must reject or flag:** concurrent load cases without cycle counting; S–N data from a milder environment than service; pitting alloys with only a uniform rate; x_e above 0.1/p for any rate; scale thickness above δ_c or strain above ε_c; self-heating above the M1.9 threshold; constant-voltage or displacement-controlled function (sign reversal); breakaway chemistry.
Confidence: medium. Rows: A4, A9, C15, D5, D6, D8.

---

## 2. Derivations

All at level `derived`. Each ends with the rows that test it.

### 2.1 Why the sum is exact in form (M1.1, M1.2)

Local entropy production is a sum of flux-times-force products, σ_s = Σ_k J_k·X_k, and the Gouy–Stodola relation gives the lifecycle cost as exergy destroyed over T₀. A lumped total is therefore Σ̇(t) = Σ_i Σ̇_i(S(t)) with S the state vector (remaining section h₀ − h, scale thickness δ, part temperature T, damage D). The current rule is Σ̇ ≈ Σ_i Σ̇_i(S₀). Error = Σ_i [Σ̇_i(S(t)) − Σ̇_i(S₀)], which to first order is Σ_i Σ_j (∂Σ̇_i/∂S_j)·ΔS_j. Its sign is the sign of each partial derivative at fixed duty. Double counting arises only if a term is measured at the system boundary (input power minus useful output) and another term is a component of that same loss.

### 2.2 Section-loss multipliers and exponents (M1.3, M1.4)

Let x(t) be the lost fraction of the controlling dimension and let a rate scale as (1−x)^(−p).

- Joule heating at constant current in a wall or foil of thickness h₀ attacked on n_s sides: R ∝ 1/(h₀ − n_s·h), so p = 1 with x = n_s·h/h₀. Round wire of diameter d₀: area ∝ (d₀ − 2h)², p = 2 with x = 2h/d₀.
- Constant voltage: P = V²/R ∝ (1−x)^(+1): p = −1 (sign reversal).
- Hysteresis under load control with specific damping energy per cycle D_s = J·σ_a^n (n = 2 reproduces the prompt's ψ·σ_a²/(2E) with constant ψ): wall, σ_a ∝ (1−x)^(−1), V ∝ (1−x): rate ∝ (1−x)^(1−n), p = n − 1. Round strut: σ_a ∝ (1−x)^(−2), V ∝ (1−x)²: p = 2n − 2.
- Pumping at fixed mass flow in a tube of diameter D: ΔP ∝ D^(−5) (turbulent, constant friction factor) or D^(−4) (laminar). Wall recession h with scale removed: D → D + 2h (loss falls). Adherent scale with Pilling–Bedworth ratio PBR: metal surface recedes by h, scale surface advances by (PBR − 1)·h, D → D − 2·(PBR − 1)·h (loss rises).

Life-averaged multiplier for linear recession x = x_e·t/τ:
M_lin(x_e, p) = (1/x_e)·∫₀^{x_e} (1−x)^(−p) dx = [(1−x_e)^(1−p) − 1]/((p−1)·x_e) for p ≠ 1; = −ln(1−x_e)/x_e for p = 1.
Series: M_lin = 1 + p·x_e/2 + p·(p+1)·x_e²/6 + …

Parabolic recession x = x_e·√(t/τ), p = 1: M_par = ∫₀¹ du/(1 − a·√u) with a = x_e; substituting s = √u gives M_par = −2·(a + ln(1−a))/a² = 1 + 2a/3 + a²/2 + 2a³/5 + …
General p: M_par = 2·∫₀¹ s·(1 − a·s)^(−p) ds (quadrature).

Series resistance (fouling layer, oxide film on a contact or a heat-transfer wall) at fixed duty: Σ̇ ∝ R₀ + R_f(t). For heat transfer across a wall between two reservoirs at small ΔT: Σ̇ = Q̇·ΔT/(T_h·T_c), ΔT = Q̇·(1/U_clean + R_f)/A, so the multiplier is 1 + R_f·U_clean. Life average of R_f: 1/2 of the end value for linear growth, 2/3 for parabolic growth.

Rows: A1, A2, A3, A4, A5.

### 2.3 Concurrent load cases and hysteresis (M1.6)

Linear viscoelastic damping: ε(t) = Σ_l (σ_l/E)·sin(ω_l·t − δ), mean power per volume = (1/T)·∫σ·ε̇ dt = Σ_l ω_l·σ_l²·sin δ/(2E) over a common period when the ω_l are distinct (cross terms average to zero). Per cycle this is π·σ_l²·sin δ/E, i.e. ψ = 2π·sin δ. So the load-case sum is exact.

Rate-independent hysteresis: dissipation per closed loop depends on the loop amplitude, and the closed loops of a combined history are the rainflow cycles. For σ = σ₁·sin(ω₁t) + σ₂·sin(φ·ω₁t), φ ≫ 1, one slow period contains about one cycle of amplitude σ₁ + σ₂ and φ − 1 cycles of amplitude about σ₂. With D_s = J·σ_a^n the ratio to the separate sum is [(1+s)^n + (φ−1)·s^n]/(1 + φ·s^n). For n = 2 this is (1 + 2s + φ·s²)/(1 + φ·s²); the excess 2s/(1 + φ·s²) is largest at s = 1/√φ, where the ratio is 1 + 1/√φ.
Upper bound: the number of reversals per unit time of a sum of sinusoids is at most that of the highest frequency component, and every amplitude is at most Σσ_l, so Σ̇_fat ≤ ν_max·V·J·(Σ_l σ_l)^n/T₀.

Rows: A11 (with B5).

### 2.4 Paralinear and spalling oxidation (M1.7, M1.11)

Tedmon form. Scale thickness δ obeys dδ/dt = k_p′/δ − k_l (k_p′ in m²/s defined by δ·dδ/dt = k_p′ without loss; k_l in m/s the scale loss rate). Metal consumed, expressed as equivalent scale thickness, grows at the growth term only: dm/dt = k_p′/δ. Hence m(t) = δ(t) + k_l·t. Dimensionless: y = k_l·δ/k_p′, θ = k_l²·t/k_p′; then dθ/dy = y/(1−y), θ = −y − ln(1−y), m̃ = y + θ.

- Upper bound: dδ/dt ≤ k_p′/δ gives δ(t) ≤ √(2·k_p′·t), so m ≤ √(2·k_p′·t) + k_l·t, i.e. m̃ ≤ U = √(2θ) + θ.
- Lower bound: δ(t) ≤ √(2·k_p′·t) also gives dm/dt = k_p′/δ ≥ d/dt √(2·k_p′·t), so m ≥ √(2·k_p′·t); and m ≥ k_l·t since δ ≥ 0. So m̃ ≥ L = max(√(2θ), θ).
- Width: U/L ≤ 2, with equality at θ = 2. Limits: θ → 0: m̃ ≈ √(2θ) + θ/3; θ → ∞: m̃ → θ + 1.
- Conversion to metal recession: divide thicknesses by Φ (scale thickness per unit metal recession; equals PBR for a planar scale); the dimensionless result is unchanged.

Periodic complete spallation with interval Δt: m(N·Δt) = N·√(2·k_p·Δt). Long-run rate r_eff = √(2·k_p/Δt). Pure parabolic at the same time: √N·√(2·k_p·Δt): low by √N. Sum bound with linear rate r_eff: (√N + N)·√(2·k_p·Δt): high by 1 + 1/√N.
Fractional spallation: area fraction F_A spalls each interval, patches in rotation (each patch every n₀ = 1/F_A intervals): long-run rate √(2·k_p·F_A/Δt); crossover with the parabolic law at t× = n₀·Δt.
Breakaway at t_b to a linear rate r_b = κ·(parabolic rate at t_b) = κ·h_b/(2·t_b): h(τ)/h_par(τ) = [1 + κ·(τ/t_b − 1)/2]/√(τ/t_b) for τ > t_b.

Cracking and spall onset. Equal-biaxial mismatch strain ε in a scale of thickness δ stores W = E_ox·ε²·δ/(1−ν_ox) per unit area; spall when W ≥ G_c: δ_c = G_c·(1−ν_ox)/(E_ox·ε²), ε = Δα·ΔT (+ mechanical strain, added as a bound). Through-scale cracking under tensile strain: ε_c = K_Ic/(f·E_ox·√(π·c)), c the flaw size (of the order of the scale thickness), f = 1.12.

Rows: D1, D2, D3, D4, D5, D6, D8.

### 2.5 Temperature coupling (M1.9, M1.10)

Rate multiplier for a temperature rise ΔT above T_env: exp[(Q/R)·(1/T_env − 1/(T_env + ΔT))] ≈ exp[Q·ΔT/(R·T²)]. Exact threshold for a relative change ε: ΔT = T²·c/(1 − T·c), c = R·ln(1+ε)/Q.
Electro-thermal loop at constant current with resistivity ρ_e = ρ_e0·(1 + α·(T − T_env)) and section loss x: ΔT = R_th·P₀·(1 + α·ΔT)/(1−x) with ΔT₀ = R_th·P₀, so ΔT = ΔT₀/(1 − x − α·ΔT₀). Loop gain G = α·ΔT₀/(1−x); runaway at x_run = 1 − α·ΔT₀.
Coupled recession: dx/dt = (1/t_c)·exp[(Q/R)·(1/T_env − 1/(T_env + ΔT(x)))], separable: t(x_a) = t_c·∫₀^{x_a} exp[−(Q/R)·(1/T_env − 1/(T_env + ΔT(x)))] dx. The uncoupled value is x_a·t_c.
Drying: surface relative humidity RH_s = RH_amb·p_sat(T_env)/p_sat(T_env + ΔT). Wet-film corrosion needs RH_s above a critical value (80 % in the time-of-wetness convention, M13).

Rows: A6, A7, A8, A9.

### 2.6 Wearout: Miner, minimum, coupled (M2.1 to M2.11)

**Sequential load cases.** Basquin: N_l = (1/2)·(σ_a,l/σ_f′)^(−m), m = −1/b; τ_l = N_l/ν_l with ν_l the mean rate of case l over service time. Miner: 1/τ_M = Σ_l 1/τ_l. Then τ_min/τ_M = τ_min·Σ_l 1/τ_l ∈ [1, L]. Two cases: ratio 1 + τ_min/τ_max; equal lives at s* = φ^(−1/m) (s = σ₂/σ₁, φ = ν₂/ν₁); ratio > 1.1 iff (s/s*)^m ∈ [0.1, 10].

**Concurrent load cases.** Idealised block per slow period: one cycle at σ₁ + σ₂ and φ − 1 cycles at σ₂. Damage per slow period d = 1/N(σ₁+σ₂) + (φ−1)/N(σ₂). Relative to case 1 alone the life falls by about (1+s)^m when the first term dominates. Mean stress of the small cycles (Smith–Watson–Topper: σ_ar = √(σ_max·σ_a) for σ_max > 0) raises their damage further.

**Nonlinear accumulation (damage-curve approach, M14).** D = (n/N)^((N/N_ref)^0.4). Two levels: n₂/N₂ = 1 − (n₁/N₁)^((N₁/N₂)^0.4). Miner sum at failure f(u) = u + 1 − u^a, a = (N₁/N₂)^0.4, u = n₁/N₁; extremum at u* = a^(1/(1−a)). Note f_max(a) + f_min(1/a) = 2 (a derived identity, not a check).
Continuous form for varying N(t): let u be the cycle ratio at the current level. At fixed level du = ν·dt/N. At a level change D is conserved: d[N^0.4·ln u] = 0, so du = −0.4·u·ln(u)·d ln N. Together: du/dt = ν/N(t) − 0.4·u·ln(u)·(d ln N/dt), u(0) = 0 (with u·ln u → 0), failure at u = 1. For rising stress d ln N/dt < 0 and ln u < 0, so the second term is negative: life longer than Miner.

**Section loss, load control, linear recession.** σ_a(t) = σ_a0·(1 − t/t_c)^(−p), t_c = h₀/(n_s·r) (wall) or d₀/(2r) (round strut). Miner: dD/dt = (1/τ₀)·(1 − t/t_c)^(−q), q = p·m. Integrating to D = 1:
(t_c/(q−1))·[(1 − τ/t_c)^(1−q) − 1] = τ₀, so **τ_c = t_c·{1 − [1 + (q−1)·ρ]^(−1/(q−1))}**, ρ = τ₀/t_c. (q = 1: τ_c = t_c·(1 − e^(−ρ)).)
Limits: ρ → 0: τ_c ≈ τ₀·(1 − q·ρ/2). ρ → ∞: τ_c → t_c from below (slowly). D diverges as t → t_c, so τ_c < t_c always.
F_cur = τ₀/τ_c = ρ/(1 − [1+(q−1)ρ]^(−1/(q−1))): increasing in ρ, unbounded.
F_min = min(τ₀, t_c)/τ_c: increasing for ρ < 1, decreasing for ρ > 1; maximum at the kink ρ = 1: F_min,max = 1/(1 − q^(−1/(q−1))) ≈ (q−1)/ln q for large q.
With allowable loss x_allow: recession life τ_rec = x_allow·t_c; coupled life min(τ_c, τ_rec); F_min = min(τ₀, τ_rec)/min(τ_c, τ_rec); maximum at ρ = x_allow; F_min = 1 for ρ ≥ ρ₁ = [(1−x_allow)^(−(q−1)) − 1]/(q−1).

**Lower bound on the coupled life.** For any x* ∈ (0,1): up to t = x*·t_c the damage rate is at most 1/(τ₀·(1−x*)^q), so D(t) ≤ t/(τ₀·(1−x*)^q) and failure cannot occur before min(x*·t_c, τ₀·(1−x*)^q). Best x* solves x*·t_c = τ₀·(1−x*)^q, i.e. x* = ρ·(1−x*)^q. τ_LB = x*·t_c ≤ τ_c ≤ min(τ₀, t_c).

**Parabolic recession (oxidation).** x = √(t/t_c), t_c = h₀²/(2·k_p·n_s²). D(τ) = (2·t_c/τ₀)·{[W^(1−q) − 1]/(q−1) − [W^(2−q) − 1]/(q−2)}, W = 1 − √(τ/t_c) (q ≠ 1, 2). Small-τ check: D → τ/τ₀.

**Displacement control (bending under imposed curvature).** ε_a ∝ remaining thickness: σ_a ∝ (1−x)^(+1). dD/dt = (1/τ₀)·(1 − t/t_c)^m; D(t_c) = t_c/((m+1)·τ₀). Fatigue failure occurs only if ρ < 1/(m+1); then τ = t_c·{1 − [1 − (m+1)·ρ]^(1/(m+1))} > τ₀.

**Environment S–N curve.** Air: σ_air(N) = σ_f′·(2N)^b. Environment curve through two knockdown points: σ_env(1e5) = k₅·σ_air(1e5), σ_env(1e8) = k₈·σ_air(1e8); b_env = log₁₀[σ_env(1e8)/σ_env(1e5)]/3; N_env(σ) = 1e5·(σ_env(1e5)/σ)^(−1/b_env). F_env = N_air(σ)/N_env(σ). Curves cross where k(N) = 1; for k₅ < 1 the crossing is below 1e5 cycles.

**Pit as a crack-like defect.** El Haddad: threshold stress range for a defect of depth a is Δσ_th(a) = ΔK_th/(Y·√(π·(a + a₀))), a₀ = (1/π)·(ΔK_th/(Y·Δσ_e))². Knockdown K(a) = √(a₀/(a₀ + a)). Assumption (medium to low confidence): near the endurance level the whole S–N curve scales with K, so the effective amplitude is σ_a0/K and dD/dt = (1/τ₀)·(1 + a(t)/a₀)^(m/2). Linear pit growth a = PF·r·t, t_a = a₀/(PF·r): τ = t_a·{[1 + (m/2+1)·τ₀/t_a]^(1/(m/2+1)) − 1}. Cube-root growth a = A·t^(1/3): quadrature. Perforation: t_perf = h₀/(n_s·PF·r).

Rows: B1 to B7, C1 to C17.

### 2.7 Error direction per side (M3)

Assumed cost per unit service time of side i (UNSURE, inferred from the prompt): c_i = [Σ_emb,i + K_ox,i·√τ_i + ∫₀^{τ_i} Σ̇_lin,i dt]/τ_i. If the true life is τ/F and true linear rates are M times the modelled ones: c_true/c_model = w_emb·F + w_ox·√F + w_lin·M (shares w at the modelled life).

Direction table. "Understates" means the simplification makes the side it is applied to look cheaper. Applied to g it favours g; applied to s it favours s. An error is non-conservative for the claim "g is better" when it understates g or overstates s.

| # | Simplification | Effect on that side's cost | Bound on size | Lower bound available | Upper bound available |
|---|---|---|---|---|---|
| 1 | Rates at pristine state, fixed duty | understates | (1−x_e)^(−p) at end of life | pristine value | end-of-life value |
| 2 | Same, constant voltage or channel widening | overstates | (1−x_e)^(+1) etc. | end-of-life value | pristine value |
| 3 | Paralinear sum | overstates | ≤ 2 (≤ about 1.37 Tedmon) | max(parabolic, linear) | the sum |
| 4 | Parabolic only, scale lost | understates | √N | the parabolic law | needs loss rate or spall interval |
| 5 | Minimum over sequential cases | understates | ≤ L on life | min rule (as life upper bound) | Miner with D_crit < 1 |
| 6 | Concurrent cases treated separately | understates | about (1+s)^m on life | separate treatment | envelope amplitude Σσ_l at ν_max |
| 7 | Air S–N curve in aggressive environment | understates | 10 to 1e3 on life; unbounded with a fatigue limit | air curve | needs environment S–N data |
| 8 | No section-loss coupling | understates | ≤ 1/(1 − q^(−1/(q−1))) vs min rule | min(τ_M, t_c) | τ_LB of 2.6 |
| 9 | No recession wearout | understates | unbounded | — | x_allow·t_c |
| 10 | Uniform rate for a pitting alloy | understates | about PF on recession life | uniform rate | needs PF |
| 11 | Basquin without endurance limit, benign environment | overstates | unbounded | Basquin extension | cut-off curve |
| 12 | Displacement control treated as load control | overstates (life understated) | see C15 | load-control life | recession life |
| 13 | Isothermal, high-temperature oxidation | understates | exp[Q·ΔT/(R·T²)] | isothermal | needs R_th and P |
| 14 | Isothermal, wet-film corrosion with self-heating | overstates | up to total (drying) | zero if dried | isothermal |
| 15 | Constant ψ | understates | 1 + β/(γ+1) | constant ψ | needs β |
| 16 | Reaction heat counted once | exact | — | — | — |
| 17 | Σ̇_op from a boundary power balance plus component terms | overstates | the duplicated term | subtract duplicate | — |

Bound construction for the claim "g is better": cost of g from the "upper bound" column, cost of s from the "lower bound" column; the verdict holds if U_g < L_s. Rows 7, 9, 10, 13 have no upper bound without data, so the construction needs those data or must return "undetermined". For the reverse claim ("g is worse") swap the columns. Because coupling numbers scale as 1/h₀, the thin-featured side has the wider interval.

Rows: E1 to E5.

---

## 3. Computation spec

Implementation: numpy and plain Python only. Double precision. All "expected" values are planner hand arithmetic (UNSURE); where the implementer's value differs beyond the stated tolerance, report both and do not adjust the method to match.

### 3.1 Input registry

**Conventions (not memory):** 1 yr = 3.15576e7 s; 1 µm/yr = 3.16881e-14 m/s; 1 ksi = 6.894757 MPa. Geometry, rate and frequency grids come from the prompt or are planner-chosen sweeps.

**MEMORY inputs (citation checker verifies these first).**

| Id | Quantity | Value and unit | Source as remembered | Used in |
|---|---|---|---|---|
| M01 | Gas constant R | 8.314462618 J/(mol·K) | SI 2019 exact value | A6, A8, A9, E5 |
| M02 | Basquin coefficient σ_f′, 2024-T4 | 900 MPa | Dowling textbook table of stress–life constants (table number UNSURE) | C1 and all rows using σ_a0 |
| M03 | Basquin exponent b, 2024-T4 | −0.102 (m = 9.804) | same; UNSURE | B, C, E |
| M04 | Cycle count at which aluminium fatigue strength is quoted | 5e8 cycles | common handbook convention | C1 |
| M05 | Young's modulus, 2024 | 73 GPa | handbook | A11, D6, E3 |
| M06 | Density ρ_m, 2024 | 2780 kg/m³ | handbook | A12, C3, E3 |
| M07 | Molar mass of Al | 26.98 g/mol | periodic table | A12, E3 |
| M08 | ISO 9223 aluminium corrosion-rate class limits | C2 ≤ 0.6; C3 ≤ 2; C4 ≤ 5; C5 ≤ 10; CX > 10 g/(m²·yr) | ISO 9223:2012 Table 2 (UNSURE) | C3 |
| M09 | Temperature coefficient of resistivity α | Cu 0.0039 /K; Al 0.0040 /K (20 °C) | handbook; UNSURE ±0.0003 | A7, A8 |
| M10 | Pilling–Bedworth ratios | Al₂O₃/Al 1.28; Cr₂O₃/Cr 2.07; NiO/Ni 1.65 | textbook values; UNSURE | A4 |
| M11 | Fouling resistances | 1e-4, 2e-4, 5e-4 m²·K/W | TEMA-type tabulations; UNSURE | A5 |
| M12 | Magnus saturation pressure | p_sat = 610.94 Pa·exp(17.625·ϑ/(ϑ + 243.04)), ϑ in °C | Magnus form with Alduchov–Eskridge-type coefficients; UNSURE | A9 |
| M13 | Time-of-wetness humidity threshold | RH > 80 % (at T > 0 °C) | ISO 9223 convention; UNSURE | A9 |
| M14 | Damage-curve exponent | 0.4 | Manson and Halford 1981 | B3, C14 |
| M15 | Geometry factors | Y = 2·1.12/π = 0.713 (semicircular surface crack); f = 1.12 (edge crack) | fracture mechanics handbooks | C12, D6, D7 |
| M16 | Operational crack-growth threshold rate | 1e-10 m/cycle | ASTM E647 definition | C17 |
| M17 | α-alumina elastic constants | E_ox = 380 GPa; ν_ox = 0.25 | handbook; UNSURE | D5, D6 |
| M18 | Expansion mismatch metal − alumina | 7e-6 /K (range 5e-6 to 8e-6) | UNSURE | D5 |
| M19 | Oxide scale fracture toughness grid | 0.5, 1, 2, 4 MPa√m | order of magnitude from scale-mechanics literature; UNSURE | D6 |
| M20 | Scale–metal interface fracture energy grid | 1, 5, 20, 100 J/m² | UNSURE | D5 |
| M21 | Specific damping capacity ψ of aluminium alloy | 2e-3 (loss factor η 1e-4 to 1e-3, ψ = 2π·η) | UNSURE | E3 |
| M22 | Damping exponent n in D_s = J·σ_a^n | 2 to 3 below the cyclic stress sensitivity limit, higher above | Lazan 1968; UNSURE | A1 (choice of p), A11 |
| M23 | Reference temperature T₀ | 298.15 K | convention | E3 |
| M24 | Pitting factor grid PF (deepest pit / mean penetration) | 1, 3, 10, 30 | UNSURE | C13 |
| M25 | Pit depth growth exponent | 1/3 (depth ∝ t^(1/3)) | Godard 1960 | C13 |
| M26 | Reduced allowable Miner sum | 0.3 | FKM guideline, non-welded steel; UNSURE | E4 |
| M27 | Embodied exergy of primary aluminium | 200 MJ/kg (range 150 to 220) | UNSURE | E3 |
| M28 | S–N slopes for comparison | m = 3 (welded joints); m = 12 (smooth steel, b ≈ −0.085) | UNSURE | B6, B7 |
| M29 | Corrosion-fatigue strength of Al alloys in sea water at 1e8 cycles | 25 to 35 % of the air value | ASM handbook statement; UNSURE (sets the range of L01) | C10 |
| M30 | Reaction enthalpy per mole Al oxidised to Al₂O₃ | 837.9 kJ/mol Al (from ΔH_f(Al₂O₃) = −1675.7 kJ/mol) | thermochemical tables | A12 |
| M31 | Threshold ΔK_th, high-temperature structural alloy | 5 MPa√m | UNSURE | D7 |
| M32 | Oxide thermal conductivity grid | 2, 10, 30 W/(m·K) | UNSURE | A5 |

**LOOKUP inputs (implementer or citation checker reads the named source; planner values are UNSURE expected ranges only).**

| Id | Quantity | Named source | Planner's UNSURE expectation | Used in |
|---|---|---|---|---|
| L01 | Knockdown on fatigue strength, saline environment vs laboratory air, for a 2xxx or 7xxx aluminium alloy, R = −1: k₅ at 1e5 cycles, k₈ at 1e8 cycles (and humid air vs laboratory air if available) | ASM Handbook Vol. 19 "Fatigue and Fracture" (1996), corrosion-fatigue articles (figure numbers UNSURE); any equivalent public S–N pair in air and in 3.5 % NaCl. Source not identified with certainty | k₅ 0.8 to 1.0; k₈ 0.25 to 0.6 | C10, C11 |
| L02 | ΔK_th of the same alloy (state R ratio and whether full range or tensile part is used) | ASM Handbook Vol. 19, or NASGRO material database | 2 to 5 MPa√m; baseline 3.0 | C12, C13 |
| L03 | DNV-RP-C203 S–N constants, curve D: air (two slopes), free corrosion | DNV-RP-C203 "Fatigue design of offshore steel structures", S–N tables for air and for free corrosion (table numbers and edition UNSURE) | air log a₁ = 12.164 (m = 3), log a₂ = 15.606 (m = 5), knee at 1e7 cycles (52.63 MPa); free corrosion log a = 11.687 (m = 3, no knee) | C16 |
| L04 | Standard chemical exergy of Al | Szargut, Morris and Steward 1988 tables, or the later revised tables | 795.7 or 888.2 kJ/mol (which is current: UNSURE) | E3 |
| L05 | Paralinear constants k_p′, k_l for one anchor system | Tedmon 1966 (Cr or Fe–Cr, 1100 to 1200 °C) or Opila and Hann 1997 (SiC in water vapour) | k_p′ 1e-17 to 1e-15 m²/s; k_l 1e-12 to 1e-10 m/s | D2 |
| L06 | Fatigue life reduction of pre-pitted aluminium specimens versus pit depth | Sankaran, Perez and Jata 2001; Dolley, Lee and Wei 2000 | life factor 2 to 10 or more for pits of order 100 µm | C12, C13 (comparison only) |
| L07 | Equivalent-stress S–N equation for unnotched 2024-T3 sheet | MIL-HDBK-5J, 2024-T3 S–N figure (figure number UNSURE) | log₁₀N = 11.1 − 3.97·log₁₀(S_eq − 15.8), S_eq = S_max·(1−R)^0.56, ksi | C2 |

### 3.2 Numerical rules for all rows

- **Roots, crossovers, first-passage times:** bisection (or bisection-safeguarded secant). Evaluate the function at both bracket ends first; if there is no sign change, do not report a root: report the two end values and extend the bracket once by a factor 10 (or to the stated limit). Stop at relative bracket width 1e-12.
- **Extrema:** coarse grid first; the extremum must lie strictly inside the grid (not at either end). Then golden-section on the bracketing interval to 1e-10. If the extremum is at a grid end, report that and extend the grid by one decade per side, once.
- **Quadrature:** composite Simpson, starting at 64 intervals, doubling until the relative change is below the row tolerance (default 1e-8).
- **ODEs:** classical RK4, fixed step, step halved until the reported quantity changes by less than 0.1 % (unless the row says otherwise). Event times located by bisection inside the bracketing step.
- **Rainflow routine (B5, A11):** (1) reduce samples to turning points (sign change of the first difference; drop repeats); (2) rotate the list to start at the global maximum and append that maximum at the end; (3) push points on a stack; while the stack holds at least three points, let X = abs(S[−1] − S[−2]), Y = abs(S[−2] − S[−3]); if X ≥ Y count one full cycle of range Y and mean (S[−2] + S[−3])/2 and delete S[−2] and S[−3]; otherwise stop the inner loop; (4) at the end the stack must hold one point; if not, report the residue. Damage per cycle 1/N with N = 0.5·(σ_ar/σ_f′)^(1/b); σ_ar = σ_a (variant a) or √((σ_m + σ_a)·σ_a) if σ_m + σ_a > 0, else zero damage (variant b, Smith–Watson–Topper).
- **Checks:** a check that compares an expression with itself is not a check. Rows say which comparisons are independent (closed form versus quadrature or ODE; bound versus exact solution) and which are plausibility ranges only. The implementer flags any check that turns out to be an identity.
- **Random numbers:** `numpy.random.default_rng(20261115)`.

### 3.3 Spec table

Row-id prefixes: A = rate additivity and coupled rates; B = wearout and damage summation; C = corrosion-fatigue worked example and section loss; D = oxidation, paralinear, spallation; E = error direction per side and bound construction. "Needs" names rows whose outputs are required.

| Row | Quantity | Method or formula | Inputs with units | Sanity check or expected range | Tolerance | Supports claim |
|---|---|---|---|---|---|---|
| A1 | Life-averaged rate multiplier M_lin(x_e, p), linear recession | Closed form of 2.2; independently composite Simpson of (1−x)^(−p) on [0, x_e] divided by x_e | x_e ∈ {0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9} (–); p ∈ {−1, 1, 2, 4, 5} (–) | p = 1: 1.0536 (0.1), 1.3863 (0.5), 2.5584 (0.9). p = 2: 1/(1−x_e). p = −1: 1 − x_e/2. Closed form and quadrature are independent | closed vs quadrature rel. diff < 1e-6; hand values ±0.1 % | M1.1, M1.3, M1.4 |
| A2 | Life-averaged multiplier M_par(a, p), parabolic recession | p = 1: −2·(a + ln(1−a))/a²; all p: Simpson of 2·s·(1 − a·s)^(−p) on s ∈ [0, 1] | a = x_e ∈ same set as A1; p ∈ {1, 2, 4} | p = 1: 1.0721 (0.1), 1.5452 (0.5), 3.463 (0.9) | as A1 | M1.3, M1.4 |
| A3 | Section-loss fraction at which the multiplier error equals ε | Bisection on x_e ∈ [1e-6, 0.99] of M − 1 − ε for M_lin and M_par | ε ∈ {0.02, 0.05, 0.10}; p ∈ {1, 2, 4} | p = 1 linear: 0.039, 0.094, 0.176; p = 1 parabolic: 0.029, 0.071, 0.135; p = 2 linear: ε/(1+ε) exactly. Report ratio to first-order rules 2ε/p (linear), 3ε/(2p) (parabolic) | hand values ±3 % | M1.4, M1.12, M4.1 |
| A4 | Sign-reversal multipliers (end-of-life values) | (i) constant voltage: (1 − x_e); (ii) channel widening at fixed mass flow: (1 + 2h/D)^(−k); (iii) adherent scale narrowing: (1 − 2·(PBR−1)·h/D)^(−k); k = 5 turbulent, 4 laminar | x_e ∈ {0.1, 0.5}; D ∈ {1, 10} mm; h ∈ {10, 100} µm; PBR from M10 | D = 1 mm, h = 100 µm, k = 5: widening 0.402; narrowing 3.33 (PBR 2.07), 1.33 (PBR 1.28). D = 10 mm, h = 100 µm: widening 0.906. Signs: (i), (ii) below 1; (iii) above 1 | ±1 % | M1.3, M3.2, M4.4 |
| A5 | Series-resistance multiplier at fixed duty | 1 + R_f·U_clean; oxide layer R_f = δ/k_ox; life-average excess = 1/2 (linear growth) or 2/3 (parabolic growth) of the end excess | U_clean ∈ {100, 1000, 5000} W/(m²·K); R_f from M11; δ ∈ {1, 10, 100} µm; k_ox from M32 | U = 1000, R_f = 2e-4: 1.20. Oxide 100 µm, k_ox = 2: R_f = 5e-5 m²·K/W, 1.05 at U = 1000. Plausibility only | ±0.5 % | M1.4 |
| A6 | Self-heating ΔT that changes an Arrhenius rate by ε | Exact: ΔT = T²·c/(1 − T·c), c = R·ln(1+ε)/Q; independently bisection on ΔT ∈ [0, 500 K] of exp[(Q/R)·(1/T − 1/(T+ΔT))] − (1+ε) | Q ∈ {50, 100, 200, 300} kJ/mol; T ∈ {300, 600, 900, 1200, 1500} K; ε ∈ {0.05, 0.10}; R = M01 | ε = 0.05: 0.73 K (50 kJ/mol, 300 K); 2.9 K (200, 1200); 3.0 K (300, 1500); 18 to 19 K (50, 1500). No sign change in the bracket: extend to 5000 K and report | closed vs bisection 1e-6; hand values ±3 % | M1.9, M4.1 |
| A7 | Electro-thermal temperature rise and runaway section loss | Closed form ΔT = ΔT₀/(1 − x − α·ΔT₀); x_run = 1 − α·ΔT₀; independently fixed-point iteration ΔT ← ΔT₀·(1 + α·ΔT)/(1−x) from ΔT₀ until change < 1e-10 K (report divergence when loop gain G = α·ΔT₀/(1−x) ≥ 1) | ΔT₀ ∈ {1, 5, 20, 50, 100} K; α ∈ {0, 0.0039, 0.0040} /K (M09); x ∈ {0, 0.2, 0.5, 0.8} | x_run = 0.80 (ΔT₀ = 50 K, α = 0.004), 0.60 (100 K). ΔT₀ = 5 K, x = 0.5, α = 0.004: 10.42 K | closed vs iteration 1e-8 where G < 0.9 | M1.1, M1.9 |
| A8 | Time to lose fraction x_a of the section with self-heating, relative to isothermal at T_env | (a) Simpson of exp[−(Q/R)·(1/T_env − 1/(T_env + ΔT(x)))] on [0, x_a], divided by x_a; (b) independently RK4 on dx/dt (2.5) in time, step t_c/200, halved until the time to x_a changes < 0.1 %, event by bisection | T_env = 300 K; Q = 50 kJ/mol; ΔT₀ ∈ {0, 1, 5, 20} K; α ∈ {0, 0.004} /K; x_a = 0.5; R = M01. **Needs A7** for ΔT(x) | α = 0: 1.000 (ΔT₀ = 0, null case), 0.91 (1 K), 0.64 (5 K), 0.19 (20 K). Also report the "isothermal at ΔT₀" value (0.72 at 5 K). With α = 0.004 and ΔT₀ = 20 K check x_run = 0.92 > x_a | (a) vs (b) < 0.2 %; hand values ±5 % | M1.1, M1.9 |
| A9 | Self-heating ΔT that dries a surface below the critical humidity | Bisection on ΔT ∈ [0, 30 K] of RH_amb·p_sat(ϑ)/p_sat(ϑ + ΔT) − RH_crit, p_sat from M12; then Arrhenius multiplier at that ΔT for Q = 50 kJ/mol | ϑ ∈ {5, 20, 35} °C; RH_amb ∈ {0.85, 0.95, 1.00}; RH_crit ∈ {0.6, 0.8} (0.8 = M13) | 20 °C: 0.95 → 0.80 needs 2.6 to 3.0 K; 1.00 → 0.80 needs 3.4 to 3.8 K; 1.00 → 0.60 needs about 8.3 K. Arrhenius multiplier at 2.8 K about 1.2 | ±5 % on hand values | M1.3, M1.10, M4.4 |
| A10 | Life-average factor for damage-dependent hysteresis | 1 + β/(γ+1) for ψ = ψ₀·(1 + β·(t/τ)^γ); effect on total 1 + w_fat·β/(γ+1) | β ∈ {0.5, 1, 5, 10}; γ ∈ {1, 3, 10}; w_fat ∈ {0.01, 0.1, 0.5} and the E3 value. **Needs E3** for the worked w_fat | β = 5, γ = 1, w_fat = 0.1: 1.25. Parametric; no anchor; plausibility only | exact arithmetic | M1.5 |
| A11 | Hysteresis under two concurrent load cases versus the separate-case sum | (a) Linear viscoelastic: trapezoid mean of σ·ε̇ over one common period, 4096 points per fast period, ε = Σ(σ_l/E)·sin(ω_l·t − δ), versus Σ ω_l·σ_l²·sin δ/(2E). (b) Rate-independent: rainflow cycles of the combined history (routine of 3.2), dissipation Σ_k σ_a,k^n per slow period versus σ₁^n + φ·σ₂^n; also the idealised ratio and the upper bound of 2.3 | σ₁ = 100 MPa; s ∈ {0.1, 1/3, 1}; φ ∈ {1 (same frequency, in phase), 3, 9, 33}; n ∈ {2, 3} (M22); tan δ = 1e-3; E = M05; ν₁ = 1 Hz. **Needs the B5 routine** | (a) ratio 1.000 for φ ≠ 1; (1+s)²/(1+s²) for φ = 1 (2.0 at s = 1). (b) n = 2: about 1.33 (s = 1/3, φ = 9), 1.18 (s = 0.1, φ = 9); n = 3, s = 1/3, φ = 9: about 2.0. Rainflow within 10 % of the idealised ratio (UNSURE, plausibility). Real test: upper bound ≥ rainflow value in every case | (a) 1e-6; (b) < 0.5 % change on doubling the sampling | M1.6 |
| A12 | Self-heating by reaction heat | q″ = r·(ρ_m/M)·ΔH; ΔT = q″/h_c | r ∈ {1, 10} µm/yr; ρ_m = M06; M = M07; ΔH = M30; h_c ∈ {5, 10, 100} W/(m²·K) | q″ ≈ 0.027 W/m² at 10 µm/yr; ΔT ≈ 2.7e-3 K at h_c = 10. Plausibility: all cases below 0.01 K | ±2 % | M1.2 |
| B1 | Miner versus minimum, two sequential load cases | τ_l = N_l/ν_l (Basquin); R = τ_min·(1/τ₁ + 1/τ₂). Equal-life point s* by bisection on ln τ₁ − ln τ₂; edges of the window R ≥ 1.1 by bisection on each side of s* | σ₁ = σ_a0 of C1 (ratio does not depend on it); s = σ₂/σ₁ ∈ [0.25, 1.4], step 0.005; φ = ν₂/ν₁ ∈ {10, 100, 1000}; M02, M03 | s* = 0.791, 0.625, 0.494. Window edges at s/s* = 0.791 and 1.265, both inside the sweep. Real test: 1 ≤ R ≤ 2 at every grid point. (R = 2 at s* is true by construction.) | edges ±1 % | M2.1, M2.2 |
| B2 | Miner versus minimum, L sequential cases (Monte Carlo) | σ_l = σ_ref·exp(U_l), U_l uniform on [−w, w]; equal ν; R = τ_min·Σ 1/τ_l; 1e5 samples | L ∈ {2, 5, 10, 20}; w ∈ {0.05, 0.1, 0.2}; m = 9.804 (M03) | Real test: 1 ≤ R ≤ L in every sample. Median plausibility: L = 5, w = 0.1: 1.5 to 3 (UNSURE) | report median and 95th percentile; Monte Carlo standard error < 1 % | M2.1 |
| B3 | Extremes of the Miner sum at failure, two-level loading, damage-curve approach | f(u) = u + 1 − u^a, a = (N₁/N₂)^0.4; coarse grid u ∈ [1e-4, 1 − 1e-4], confirm interior extremum, golden-section; compare with u* = a^(1/(1−a)) | N₁/N₂ ∈ {1e-3, 1e-2, 1e-1, 10, 100, 1000}; M14 | Minima (high then low): 0.222 (u = 0.052), 0.405 (0.112), 0.673 (0.217). Maxima (low then high): 1.327 (0.544), 1.595 (0.707), 1.778 (0.830) | golden vs analytic 1e-6; hand values ±0.005 | M2.4 |
| B4 | Life under two concurrent load cases, idealised block | Damage per slow period d = 1/N(σ₁+σ₂) + (φ−1)/N(σ₂); τ_blk = 1/(ν₁·d); ratios τ₁/τ_blk, min(τ₁, τ₂)/τ_blk, τ_Miner(cases)/τ_blk | σ₁ = 108.7 MPa (C1 value); ν₁ = 1 Hz; s ∈ {0.05, 0.1, 0.2, 0.5, 1}; φ ∈ {9, 33, 129, 1025}; M02, M03 | τ₁/τ_blk ≥ (1+s)^m = 1.61, 2.55, 5.97, 53.3, 894 | ±1 % on (1+s)^m | M2.3 |
| B5 | Rainflow verification of B4 | Synthesise σ(t) = σ₁·sin(2π·ν₁·t) + σ₂·sin(2π·φ·ν₁·t) over one slow period; n_pts per fast period = 256, 512, 1024; rainflow routine of 3.2; Miner damage, variants a and b; compare with B4 | Grid of B4 with φ ∈ {9, 33, 129} (peaks align) and φ ∈ {10, 32, 128} (no alignment). **Needs B4** | Largest counted amplitude = σ₁ + σ₂ within 0.1 % for aligned φ. Counted cycles ≤ φ. Variant a damage / B4 damage within [0.7, 1.05] where the envelope cycle dominates (UNSURE; plausibility). Variant b ≥ variant a. If the ratio is outside the range, the rainflow value is authoritative | damage change < 0.5 % on doubling n_pts | M2.3, M1.6 |
| B6 | Stress change equivalent to a factor 2 and a factor 10 in life | 2^(1/m), 10^(1/m) | m ∈ {3, 5, 9.804, 12, 19.608} (M03, M28) | 2^(1/m): 1.260, 1.149, 1.073, 1.059, 1.036. 10^(1/m) for m = 9.804: 1.265 | exact | M2.2 |
| B7 | Conservatism of Basquin without an endurance limit | N/N_e = (σ/σ_e)^(−m) (extension); (σ/σ_e)^(−(2m−1)) (Haibach slope); ∞ (cut-off) | σ/σ_e ∈ {0.95, 0.9, 0.8, 0.7, 0.5}; m ∈ {5, 12} (M28) | m = 12: 3.54 (0.9), 14.6 (0.8), 4096 (0.5); Haibach: 11.3, 169, 8.4e6 | ±1 % | M2.10, M3.2 |
| C1 | Baseline stress amplitude and air fatigue life | σ_a0 = σ_f′·(2·N₀)^b, N₀ = 5e8; m = −1/b; τ₀ = N₀/ν | M02, M03, M04; ν ∈ {0.01, 0.1, 1, 10} Hz | σ_a0 = 108.7 MPa (accept 105 to 112); m = 9.804; τ₀ = 1584, 158.4, 15.84, 1.584 yr | ±0.5 % | M2.5 and all C, E rows |
| C2 | Cross-check of the baseline against an independent air S–N curve | Evaluate the L07 equation at R = −1, S_max = σ_a0; report N and N/N₀ | L07; σ_a0 from C1. **Needs C1** | N ≈ 4e7, N/N₀ ≈ 0.09 (UNSURE). Plausibility only: flag the baseline if N/N₀ is outside [0.03, 30]; report the implied shift in ρ | none (report) | M2.5 (robustness) |
| C3 | Recession-through time and ρ | Wall: t_c = h₀/(n_s·r); round strut: t_c = d₀/(2r); ρ = τ₀/t_c; mass-loss rate r·ρ_m for class placement | h₀, d₀ ∈ {0.3, 1, 3} mm; r ∈ {1, 3, 10} µm/yr; n_s ∈ {1, 2}; ν ∈ {0.1, 1, 10} Hz; M06; M08. **Needs C1** | Wall n_s = 2: t_c = 150, 50, 15 yr (0.3 mm); 500, 166.7, 50 yr (1 mm); 1500, 500, 150 yr (3 mm). ρ at 1 Hz from 0.0106 to 1.056. 1 to 10 µm/yr = 2.8 to 27.8 g/(m²·yr): classes C4 to CX (UNSURE) | ±0.5 % | M2.5 |
| C4 | Coupled life with linear section loss, closed form | τ_c = t_c·{1 − [1 + (q−1)·ρ]^(−1/(q−1))}, q = p·m; F_cur = τ₀/τ_c; F_min = min(τ₀, t_c)/τ_c | Grid of C3; p = 1 (wall, membrane load), p = 2 (round strut, axial load). **Needs C1, C3** | Wall n_s = 2, 1 Hz, F_cur for r = 1, 3, 10 µm/yr: 1.47, 2.26, 4.54 (0.3 mm); 1.15, 1.42, 2.26 (1 mm); 1.05, 1.15, 1.47 (3 mm). Wall n_s = 1, 3 mm: 1.026 (r = 1), 1.24 (r = 10). Strut 0.3 mm, r = 10: τ_c = 2.25 yr, F_cur = 7.0, F_min = 6.7 | hand values ±2 % | M2.5, M2.6, M3.3, M4.2 |
| C5 | Numerical verification of C4 | First-passage time of D = 1 for dD/dt = (1/τ₀)·(1 − t/t_c)^(−q): RK4, step min(τ₀, t_c)/400, halved until the time changes < 0.1 %; event by bisection inside the bracketing step (upper limit t_c·(1 − 1e-12)) | (ρ, q) ∈ {(0.01, 9.804), (0.1, 9.804), (1, 9.804), (10, 9.804), (1, 19.608), (1, 4.5585)}. **Needs C4** for comparison | Independent of the closed form; must agree with C4 | rel. diff < 0.1 % | M2.5, M4.2 |
| C6 | Worst case of F_min over ρ | F_min(ρ) on ρ ∈ [1e-3, 1e3], 20 points per decade; confirm interior maximum; golden-section on ln ρ on each side of the kink; compare with 1/(1 − q^(−1/(q−1))) | q ∈ {3, 5, 9.804, 15, 19.608, 29.412} | Maximum at ρ = 1: 2.37, 3.02, 4.38, 5.69, 6.77, 8.91. Also report F_cur at ρ = 1e3 (expected ≥ ρ; about 1.55·ρ for q = 9.804, since τ_c/t_c ≈ 0.64 there). Maximum at a grid end: extend and report | ±1 % | M2.5, M2.6 |
| C7 | Effect of an allowable section loss | τ_rec = x_allow·t_c; F_min = min(τ₀, τ_rec)/min(τ_c, τ_rec); sweep ρ as C6; locate the maximum; ρ₁ = [(1−x_allow)^(−(q−1)) − 1]/(q−1) | x_allow ∈ {0.2, 0.5, 0.8, 1.0}; q ∈ {9.804, 19.608} | q = 9.804: maximum 1.84 at ρ = 0.2; 2.87 at 0.5; 3.79 at 0.8; 4.38 at 1.0. ρ₁ = 0.70 for x_allow = 0.2; F_min = 1 for ρ ≥ ρ₁ | ±2 % | M2.5, M2.11, M4.2 |
| C8 | Lower bound on the coupled life | x* by bisection on x − ρ·(1−x)^q over (0, 1) (values −ρ and +1 at the ends); τ_LB = x*·t_c; ratio τ_LB/τ_c on the ρ grid of C6; locate the minimum ratio | q ∈ {4.5585, 9.804, 19.608}. **Needs C4** | Real test of the bound: ratio ≤ 1 at every ρ. q = 9.804: 0.73 at ρ = 1 (x* = 0.167); about 0.80 at ρ = 100; → 1 as ρ → 0. q = 19.608, ρ = 1.056: x* = 0.109 | report minimum to 3 digits | M2.11, M3.4 |
| C9 | Coupled life with parabolic section loss (oxidation) | Bisection on τ/t_c ∈ (0, 1) of D(τ) − 1 with the closed form of 2.6; independently Simpson of 2·s·(1−s)^(−q) on [0, √(τ/t_c)] | ρ ∈ {0.01, 0.1, 1, 10}; q ∈ {9.804, 19.608}. Dimensional illustration: h₀ = 0.3 mm, n_s = 2, k_p = 1e-16 m²/s (parametric) gives t_c = 1.125e8 s = 3.56 yr | q = 9.804, ρ = 1: τ/t_c ≈ 0.086, F_min ≈ 11.7 (accept 10.5 to 13) | closed vs quadrature 1e-6; hand value ±5 % | M2.5 |
| C10 | Life factor from an environment S–N curve | Formulas of 2.6; F_env = N_air(σ)/N_env(σ) at σ = σ_a0; sweep σ ∈ [100, 400] MPa (61 log-spaced points); crossover F_env = 1 by bisection on σ | k₅ ∈ {0.8, 0.9, 1.0}; k₈ ∈ {0.25, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0} (L01, M29); M02, M03. **Needs C1** | Baseline (0.9, 0.4): b_env = −0.219, N_env = 3.2e6, F_env = 154 (accept 130 to 180). k₅ = 0.9 and k₈ = 0.25, 0.3, 0.5, 0.6, 0.8: 351, 269, 84, 43, 8.2. Crossover for (0.9, 0.4) near 284 MPa (N ≈ 4.1e4). k₅ = 1.0: crossover at N = 1e5 by construction (not a check). k₅ = k₈ = 1: F = 1 (null case). No crossover in the sweep: report | ±5 % | M2.7 |
| C11 | Environment curve and section loss together | τ₀,env = N_env/ν; q_env = p·(−1/b_env); τ_c from the C4 formula; F_sec,env = τ₀,env/τ_c; frequency at which F_sec,env = 1.05 by bisection on ln ν ∈ [ln 0.01, ln 10] | Baseline (k₅, k₈) = (0.9, 0.4); wall 0.3 mm n_s = 2 and strut 0.3 mm; r = 10 µm/yr (then the full C3 grid); ν ∈ {0.01, 0.1, 1, 10} Hz. **Needs C3, C10** | Wall: 2.34 (0.01 Hz), 1.15 (0.1 Hz), 1.016 (1 Hz), 1.002 (10 Hz); the 1.05 threshold lies between 0.1 and 1 Hz | hand values ±15 % | M2.8 |
| C12 | Pit as a crack-like defect: intrinsic length and knockdown | a₀ = (1/π)·(ΔK_th/(Y·Δσ_e))², Δσ_e = 2·σ_a0; K(a) = √(a₀/(a₀ + a)); life factor K^(−m) | ΔK_th ∈ {2, 3, 5} MPa√m (L02; baseline 3.0); Y = M15; a ∈ {10, 30, 100, 300} µm. **Needs C1** | a₀ = 119 µm (53 µm and 331 µm for ΔK_th = 2 and 5). Baseline K: 0.960, 0.894, 0.737, 0.533; life factors 1.49, 3.0, 19.9, 478. Compare with L06 (plausibility) | ±3 % | M2.9 |
| C13 | Life with a growing pit; perforation time | (a) a = PF·r·t: τ = t_a·{[1 + (m/2+1)·τ₀/t_a]^(1/(m/2+1)) − 1}, t_a = a₀/(PF·r). (b) a = A·t^(1/3), A set so that a(1 yr) = PF·r·(1 yr): bisection on τ ∈ (0, τ₀] of D(τ) − 1, D = (1/τ₀)·∫(1 + a(t)/a₀)^(m/2) dt by Simpson in v = t^(1/3). (c) t_perf = h₀/(n_s·PF·r); life = min | a₀ baseline from C12; PF from M24; r ∈ {1, 10} µm/yr; ν = 1 Hz; h₀ = 0.3 mm, n_s = 2; M25. **Needs C1, C12** | (a) PF = 10, r = 10: τ = 1.31 yr, F = 12.1; PF = 1, r = 10: 5.3 yr, F = 3.0; PF = 1, r = 1: 12.3 yr, F = 1.29. t_perf = 1.5 yr (PF = 10, r = 10). (b) report; expect longer than (a) for τ > 1 yr | (a) ±3 %; (b) Simpson 1e-6 | M2.9 |
| C14 | Nonlinear accumulation under continuously rising stress | ODE of 2.6: du/dt = ν/N(t) + 0.4·q·u·ln(u)/(t_c − t), N(t) = N₀·(1 − t/t_c)^q, u(0) = 0 with u·ln u = 0 at u = 0; RK4, step min(τ₀, t_c)/1000, halved until the time to u = 1 changes < 0.1 %; keep u in [0, 1] | q ∈ {0 (null case), 9.804}; ρ ∈ {0.01, 0.1, 1, 10}; M14. **Needs C4** | Null case returns τ₀ within 0.1 %. Ratio τ_DCA/τ_c ∈ [1.0, 2.5] (UNSURE). A ratio below 1 contradicts the sign argument of 2.6: report it | 0.1 % convergence | M2.10, M2.4 |
| C15 | Displacement-controlled counter-case | Threshold ρ* = 1/(m+1); for ρ < ρ*: τ = t_c·{1 − [1 − (m+1)·ρ]^(1/(m+1))}; D(t_c) = 1/((m+1)·ρ); verify one case by Simpson plus bisection | m = 9.804; ρ ∈ {0.01, 0.05, 0.09, 0.095, 0.1, 1} | ρ* = 0.0926, bracketed by the sweep: D(t_c) > 1 for ρ = 0.09 and < 1 for ρ = 0.095. τ/τ₀ = 1.053 (ρ = 0.01), 1.39 (0.05) | ±1 % | M2.10, M1.3, M3.2 |
| C16 | Welded-steel code anchor: air versus free corrosion | N_air = 10^(log a₁)/Δσ³ above the knee stress, 10^(log a₂)/Δσ⁵ below; N_fc = 10^(log a_fc)/Δσ³; factor N_air/N_fc | L03; Δσ ∈ {100, 80, 52.63, 40, 30, 20} MPa | Factor 3.0 at and above 52.63 MPa; 5.2 (40), 9.2 (30), 20.7 (20). Real check on the looked-up constants: both air branches give 1e7 cycles at the knee within 1 % | ±2 % | M2.7, M4.3 |
| C17 | Frequency below which uniform dissolution outruns a threshold crack | ν_crit = r/(da/dN)_th | r ∈ {1, 10} µm/yr; M16 | 3.2e-4 Hz and 3.2e-3 Hz. Plausibility only | ±1 % | M2.10 |
| D1 | Tedmon paralinear solution and its bounds | For each θ solve θ = −y − ln(1−y) on y ∈ [0, 1) by bisection (use log1p; for θ > 30 use y = 1 − exp(−θ − 1) and say so); m̃ = y + θ; U = √(2θ) + θ; L = max(√(2θ), θ); maxima of U/m̃ (golden-section on ln θ) and of m̃/L (kink at θ = 2) | θ ∈ [1e-4, 1e4], 20 points per decade | Real test: L ≤ m̃ ≤ U at every θ. Max U/m̃ ≈ 1.369 near θ ≈ 3.4 (accept 1.35 to 1.39, θ ∈ [2.5, 4.5]). Max m̃/L ≈ 1.474 at θ = 2 (y = 0.9475). Limits: m̃ − √(2θ) → θ/3 (small θ); m̃ − θ → 1 (large θ). Maximum at a grid end: extend and report | bisection 1e-12; hand values ±1 % | M1.7, M3.2, M3.4 |
| D2 | Independent integration of the paralinear ODE; dimensional example | RK4 on dy/dθ = (1−y)/y from y₀ = √(2θ₀) − (2/3)·θ₀ at θ₀ = 1e-6, geometric step growth, halved until y at θ ∈ {0.1, 1, 2, 3.5, 10, 100} changes < 0.1 %; δ_lim = k_p′/k_l; t(θ = 2) = 2·k_p′/k_l² | L05; fallback (parametric): k_p′ = 1e-17 m²/s, k_l = 1e-12 m/s. **Needs D1** | y(1) = 0.8414, y(2) = 0.9475, y(3.5) = 0.9888. Fallback: δ_lim = 10 µm, t(θ = 2) = 2e7 s | 0.1 % vs D1 | M1.7, M4.3 |
| D3 | Periodic complete spallation | m(t) = [floor(t/Δt) + √(frac(t/Δt))]·√(2·k_p·Δt); compare with parabolic √(2·k_p·t) and with U = √(2·k_p·t) + t·√(2·k_p/Δt) on a grid of 100 points per interval | N = t/Δt up to 1000, reported at N ∈ {1, 2, 5, 10, 100, 1000}; k_p = 1e-17 m²/s, Δt = 3600 s (cancel in ratios) | Real test: parabolic ≤ m ≤ U at every grid point. At t = N·Δt: m/parabolic = √N; U/m = 1 + 1/√N (2 at N = 1) | 1e-9 | M1.7, M1.11 |
| D4 | Fractional spallation ensemble | n₀ = 1/F_A equal patches; patch j spalls completely at intervals j, j + n₀, …; m_ens(t) = mean over patches; long-run slope by least squares over [10·n₀, 20·n₀] intervals versus √(2·k_p·F_A/Δt); ratio m_ens/parabolic at t = n₀·Δt, 10·n₀·Δt, 100·n₀·Δt | F_A ∈ {0.001, 0.01, 0.1}; k_p, Δt as D3. **Needs the D3 routine** | Slope ratio 1 within 2 %; m_ens/parabolic ≈ √(t/(n₀·Δt)) for t ≫ n₀·Δt (about 3.2 at 10·n₀·Δt). Consistency check of an asymptote, not an independent proof | 2 % | M1.11, M1.7 |
| D5 | Critical scale thickness for spallation and time to reach it | δ_c = G_c·(1−ν_ox)/(E_ox·ε²), ε = Δα·ΔT + ε_mech; t_sp = δ_c²/(2·k_p′) | G_c from M20; E_ox, ν_ox = M17; Δα = M18; ΔT ∈ {200, 500, 1000} K; ε_mech ∈ {0, 1.5e-3}; k_p′ ∈ {1e-18, 1e-17, 1e-16} m²/s (parametric) | δ_c = 0.20 µm (G_c = 5, ΔT = 1000 K, ε_mech = 0); 0.81 µm (5, 500 K); 16 µm (100, 500 K). Plausibility: spall thicknesses of order 1 to 10 µm for alumina scales (literature, UNSURE) | ±2 % | M1.8, M4.1, M4.4 |
| D6 | Scale cracking strain versus cyclic strain amplitude | ε_c = K_Ic/(f·E_ox·√(π·c)); crossover flaw size c× = (1/π)·(K_Ic/(f·E_ox·ε_a))², confirmed by bisection on ln c over [1e-9, 1e-3] m | K_Ic from M19; f = M15; E_ox = M17; c ∈ {0.01, 0.1, 1, 10, 100} µm; ε_a = σ_a0/E (C1, M05). **Needs C1** | ε_a = 1.49e-3. ε_c = 1.33e-3 at c = 1 µm, K_Ic = 1. c× = 0.79 µm (K_Ic = 1), 0.20 µm (0.5), 12.7 µm (4); all inside the bracket | ±2 % | M1.8, M4.1, M4.4 |
| D7 | Time for an oxide notch to reach the crack threshold | a_tr = (1/π)·(ΔK_th/(Y·Δσ))²; t_i = a_tr²/(2·k_p′) | ΔK_th = M31; Y = 1.12 (M15); Δσ ∈ {200, 400, 800} MPa; k_p′ ∈ {1e-18, 1e-17, 1e-16} m²/s | Δσ = 400 MPa, k_p′ = 1e-16: a_tr = 39.7 µm, t_i = 7.9e6 s (91 d). t_i ∝ Δσ^(−4) | ±2 % | M2.12 |
| D8 | Breakaway: metal loss relative to the parabolic law | h(τ)/h_par(τ) = [1 + κ·(τ/t_b − 1)/2]/√(τ/t_b) for τ > t_b, else 1 | τ/t_b ∈ {0.5, 0.9, 1.0, 1.1, 2, 10, 100}; κ ∈ {1, 10, 100} | 1 for τ/t_b ≤ 1 (sweep brackets the onset). κ = 1: 1.06 (2), 1.74 (10). κ = 10: 14.5 (10) | exact | M1.7, M4.4 |
| E1 | Cost sensitivity to life and rate errors | c_true/c_model = w_emb·F + w_ox·√F + w_lin·M | F ∈ {1.05, 1.5, 2, 4.4, 7, 150}; w_emb ∈ {0.1, 0.5, 0.9}; w_ox ∈ {0, 0.1}; w_lin = 1 − w_emb − w_ox; M ∈ {1, 1.1, 1.5} | w_emb = 0.5, w_ox = 0, F = 4.4, M = 1: 2.70 | exact | M3.1 |
| E2 | Error of the verdict ratio for a thin g and a thick s | F_g, F_s from C4; verdict error = [w_emb·F_g + (1 − w_emb)]/[w_emb·F_s + (1 − w_emb)] | g: round strut d₀ = 0.3 mm, p = 2; s: wall h₀ = 3 mm, n_s = 1, p = 1; both r = 10 µm/yr, ν = 1 Hz, same alloy; w_emb ∈ {0.1, 0.5, 0.687, 1.0}. **Needs C4, E1** (and E3 for 0.687) | F_g = 7.0, F_s = 1.24. Verdict error 5.7 (w_emb = 1), 3.6 (0.5), 1.56 (0.1) | ±3 % | M3.3, M3.5 |
| E3 | Shares of fatigue hysteresis, corrosion and embodied cost for the worked strut | Σ̇_fat = ν·V·ψ·σ_a0²/(2·E·T₀); Σ̇_corr = r·A·(ρ_m/M)·b_ch/T₀; Σ̇_emb = e_emb·ρ_m·V/(T₀·τ₀); V = π·d₀²·ℓ/4, A = π·d₀·ℓ | d₀ = 0.3 mm; ℓ = 3 mm; ν = 1 Hz; r = 10 µm/yr; ψ = M21; E = M05; T₀ = M23; ρ_m = M06; M = M07; b_ch = L04; e_emb = M27. **Needs C1** | Σ̇_fat ≈ 1.15e-10 W/K; Σ̇_corr ≈ 2.5e-10 W/K (2.75e-10 with the higher b_ch); Σ̇_emb ≈ 7.9e-10 W/K; shares ≈ 0.10, 0.21, 0.69. Plausibility only (wide-range MEMORY inputs) | arithmetic ±3 % | M1.5, M3.1 |
| E4 | Width of the cost bound for g and the margin needed for a robust verdict | c_U/c_model = w_emb·(τ₀/τ_LB) + w_ox·√(τ₀/τ_LB) + w_lin·(1 − τ_c/t_c)^(−p_r); required modelled ratio c_g/c_s < 1/(c_U/c_model) when s is taken at its modelled (lower-bound) cost; repeat with τ₀ replaced by 0.3·τ₀ in the τ_LB step (M26) | g of E2 (ρ = 1.056, q = 19.608); p_r ∈ {1, 2}; shares as E1. **Needs C4, C8, E1** | τ_LB = 1.64 yr (x* = 0.109); w_emb = 0.5, w_lin = 0.5, p_r = 2: c_U/c_model ≈ 5.5, margin ≈ 0.18 (accept 0.15 to 0.25). With the reduced damage sum: τ_LB ≈ 1.09 yr, margin ≈ 0.125 | ±5 % | M3.4, M3.6 |
| E5 | Coupling numbers and first-order error estimate for g and s | x_e = τ_c/t_c; rate error p·x_e/2 versus M_lin(x_e, p) − 1; life error q·ρ/2 versus F_cur − 1; thermal number Q·ΔT/(R·T²) versus the exact multiplier − 1 for ΔT ∈ {1, 5} K, Q = 50 kJ/mol, T = 300 K; weighted sum with E3 shares | g and s of E2. **Needs A1, A6, C4, E3** | g: x_e = 0.150; rate (p = 2) 0.150 first-order vs 0.177 exact; life 10.4 first-order vs 6.0 exact (first-order invalid near ρ = 1: report). s: x_e = 0.042; rate (p = 1) 0.0212 vs 0.0218; life 0.259 vs 0.244 | report | M1.12, M3.3, M4.1 |

### 3.4 Row dependencies

| Row | Needs |
|---|---|
| A8 | A7 |
| A10 | E3 (worked w_fat only) |
| A11 | B5 routine |
| B5 | B4 |
| C2, C3, C10, C12 | C1 |
| C4 | C1, C3 |
| C5, C8, C14 | C4 |
| C11 | C3, C10 |
| C13 | C1, C12 |
| D2 | D1 |
| D4 | D3 routine |
| D6 | C1 |
| E2 | C4, E1 (E3 for one share value) |
| E3 | C1 |
| E4 | C4, C8, E1 |
| E5 | A1, A6, C4, E3 |

Cross-domain dependencies if the implementer is split: A10 and A11 need E3 and B5; D6 needs C1 (one number, σ_a0 = 108.7 MPa, can be passed as a constant); all E rows need C4 (and C8 for E4). Rows with no dependency: A1 to A7, A9, A12, B1 to B4, B6, B7, C1, C6, C7, C9, C15, C16, C17, D1, D3, D5, D7, D8, E1.

Row count: A 12, B 7, C 17, D 8, E 5; total 49. MEMORY registry entries: 32. LOOKUP registry entries: 7.

---

## 4. Citation list

All from the planner's memory; none was opened or checked. "UNSURE" marks any element (volume, pages, table or figure number, or the attributed content) the planner is not certain of. Where no equation or figure number is given, none is relied on.

| # | Author, year | Title and source | Cited for | Eq., fig., table relied on | Certainty |
|---|---|---|---|---|---|
| 1 | de Groot, Mazur, 1962 | Non-Equilibrium Thermodynamics, North-Holland | Entropy production as a sum of flux-times-force products (2.1) | chapter on entropy balance; number UNSURE | book certain |
| 2 | Bejan, 1996 | Entropy Generation Minimization, CRC Press | Gouy–Stodola relation; heat-transfer irreversibility Q̇·ΔT/(T_h·T_c) (2.2) | none | book certain |
| 3 | Basquin, 1910 | The exponential law of endurance tests, Proc. ASTM 10, 625–630 | Basquin relation | none | pages UNSURE |
| 4 | Palmgren, 1924 | Die Lebensdauer von Kugellagern, VDI-Zeitschrift 68, 339–341 | Linear damage rule | none | pages UNSURE |
| 5 | Miner, 1945 | Cumulative damage in fatigue, J. Appl. Mech. 12, A159–A164 | Linear damage rule; scatter of damage sums | none | certain |
| 6 | Manson, Halford, 1981 | Practical implementation of the double linear damage rule and damage curve approach for treating cumulative fatigue damage, Int. J. Fracture 17, 169–192 | Damage-curve exponent (N₁/N₂)^0.4 (M14; B3, C14) | equation number UNSURE | exponent 0.4 fairly certain |
| 7 | Fatemi, Yang, 1998 | Cumulative fatigue damage and life prediction theories: a survey of the state of the art for homogeneous materials, Int. J. Fatigue 20, 9–34 | Survey; sequence effects and range of Miner sums | none | certain |
| 8 | Schütz, 1996 | A history of fatigue, Eng. Fract. Mech. 54, 263–300 | Empirical range of Miner sums at failure | none | content UNSURE |
| 9 | Haibach, 1970 | Modifizierte lineare Schadensakkumulations-Hypothese zur Berücksichtigung des Dauerfestigkeitsabfalls mit fortschreitender Schädigung, LBF Technische Mitteilung TM 50/70 | Slope 2m − 1 below the knee (B7) | none | UNSURE |
| 10 | FKM, 2012 | Analytical Strength Assessment of Components (FKM guideline), 6th ed., VDMA | Reduced allowable damage sum 0.3 (M26) | section UNSURE | value UNSURE |
| 11 | ASTM E1049-85 | Standard Practices for Cycle Counting in Fatigue Analysis | Rainflow counting (3.2) | section number UNSURE | standard certain |
| 12 | Smith, Watson, Topper, 1970 | A stress–strain function for the fatigue of metals, J. Materials 5, 767–778 | Mean-stress parameter √(σ_max·σ_a) (B5) | none | certain |
| 13 | Dowling | Mechanical Behavior of Materials (4th ed., 2013), Pearson | Basquin constants for 2024-T4 (M02, M03) | table of stress–life constants; number UNSURE | values UNSURE |
| 14 | US DoD, 2003 | MIL-HDBK-5J, Metallic Materials and Elements for Aerospace Vehicle Structures | Equivalent-stress S–N equation for 2024-T3 sheet (L07) | figure number UNSURE | constants UNSURE |
| 15 | Lazan, 1968 | Damping of Materials and Members in Structural Mechanics, Pergamon | Damping energy D = J·σ^n; stress-history effect (M22; M1.5, M1.6) | none | numbers UNSURE |
| 16 | Wagner, 1933 | Beitrag zur Theorie des Anlaufvorgangs, Z. Phys. Chem. B21, 25–41 | Parabolic oxidation law | none | pages UNSURE |
| 17 | Pilling, Bedworth, 1923 | The oxidation of metals at high temperatures, J. Inst. Metals 29, 529–591 | Pilling–Bedworth ratio (M10) | none | values in M10 are textbook, UNSURE |
| 18 | Tedmon, 1966 | The effect of oxide volatilization on the oxidation kinetics of Cr and Fe–Cr alloys, J. Electrochem. Soc. 113, 766–768 | Paralinear rate equation dδ/dt = k_p′/δ − k_l (2.4; D1, D2; L05) | equation number UNSURE | certain on form |
| 19 | Opila, Hann, 1997 | Paralinear oxidation of CVD SiC in water vapor, J. Am. Ceram. Soc. 80, 197–205 | Paralinear data set as anchor (L05) | none | certain |
| 20 | Lowell, Barrett, Palmer, Auping, Probst, 1991 | COSP: a computer model of cyclic oxidation, Oxid. Met. 36, 81–112 | Cyclic oxidation with spallation (2.4; D3, D4) | none | certain |
| 21 | Smialek, 2003 | A deterministic interfacial cyclic oxidation spalling model, Acta Mater. 51, 469–483 | Fractional-area spalling model; long-run linear rate (D4) | none; the planner's rate formula is derived in 2.4, not copied | attribution UNSURE |
| 22 | H. E. Evans, 1995 | Stress effects in high temperature oxidation of metals, Int. Mater. Rev. 40, 1–40 | Strain-energy spallation criterion (2.4; D5) | none; placement of (1−ν) derived in 2.4 | certain on topic |
| 23 | Schütze, 1997 | Protective Oxide Scales and Their Breakdown, Wiley | Critical strains for scale cracking (M1.8; D6) | none | values UNSURE |
| 24 | Hancock, Nicholls, 1988 | Application of fracture mechanics to failure of surface oxide scales, Mater. Sci. Technol. 4, 398–406 | ε_c = K_Ic/(f·E·√(π·c)) (D6) | equation number UNSURE | certain on form |
| 25 | Kitagawa, Takahashi, 1976 | Applicability of fracture mechanics to very small cracks or the cracks in the early stage, Proc. 2nd Int. Conf. Mechanical Behavior of Materials, Boston, 627–631 | Threshold stress versus defect size (C12) | none | certain |
| 26 | El Haddad, Topper, Smith, 1979 | Prediction of non propagating cracks, Eng. Fract. Mech. 11, 573–584 | Intrinsic length a₀ (C12, C13, D7) | none | certain |
| 27 | Kondo, 1989 | Prediction of fatigue crack initiation life based on pit growth, Corrosion 45, 7–11 | Pit-to-crack transition (M2.9) | none | certain |
| 28 | Harlow, Wei, 1994 | Probability approach for prediction of corrosion and corrosion fatigue life, AIAA J. 32, 2073–2079 | Pit growth then crack growth model (M2.9) | none | certain |
| 29 | Godard, 1960 | The corrosion behavior of aluminum in natural waters, Can. J. Chem. Eng. 38, 167–173 | Pit depth ∝ t^(1/3) (M25) | none | exponent fairly certain |
| 30 | Sankaran, Perez, Jata, 2001 | Effects of pitting corrosion on the fatigue behavior of aluminum alloy 7075-T6: modeling and experimental studies, Mater. Sci. Eng. A 297, 223–229 | Pre-pitted fatigue life reduction (L06) | none | factor UNSURE |
| 31 | Dolley, Lee, Wei, 2000 | The effect of pitting corrosion on fatigue life, Fatigue Fract. Eng. Mater. Struct. 23, 555–560 | Pre-pitted 2024-T3 fatigue lives (L06) | none | certain on topic |
| 32 | Gangloff, 1990 | Corrosion fatigue crack propagation in metals, in Environment-Induced Cracking of Metals, NACE-10, 55–109 | Frequency and time dependence of corrosion fatigue (flag in 5.2) | none | certain |
| 33 | Wei, Landes, 1969 | Correlation between sustained-load and fatigue crack growth in high-strength steels, Mater. Res. Stand. 9, 25–27 | Superposition of cycle- and time-dependent growth (flag in 5.2) | none | pages UNSURE |
| 34 | Suresh, Zamiski, Ritchie, 1981 | Oxide-induced crack closure: an explanation for near-threshold corrosion fatigue crack growth behavior, Metall. Trans. A 12, 1435–1443 | Environment can slow near-threshold growth (M2.10 v) | none | certain |
| 35 | ISO 9223:2012 | Corrosion of metals and alloys — Corrosivity of atmospheres — Classification, determination and estimation | Aluminium corrosion-rate classes; time-of-wetness humidity threshold (M08, M13) | Table 2 UNSURE | values UNSURE |
| 36 | DNV (DNV GL), 2016 or later | DNV-RP-C203 (DNVGL-RP-C203), Fatigue design of offshore steel structures | Air and free-corrosion S–N curves (L03; C16) | S–N tables for air and free corrosion; numbers UNSURE | constants UNSURE |
| 37 | ASM International, 1996 | ASM Handbook Vol. 19, Fatigue and Fracture | Corrosion-fatigue strength of aluminium alloys in saline environments (L01, M29); ΔK_th (L02) | figure numbers UNSURE | attribution of M29 UNSURE |
| 38 | Szargut, Morris, Steward, 1988 | Exergy Analysis of Thermal, Chemical, and Metallurgical Processes, Hemisphere | Standard chemical exergy of Al (L04) | table of standard chemical exergies; number UNSURE | value UNSURE |
| 39 | ASTM E647 | Standard Test Method for Measurement of Fatigue Crack Growth Rates | Operational threshold at 1e-10 m/cycle (M16) | none | certain |
| 40 | ASTM G96 | Standard Guide for Online Monitoring of Corrosion in Plant Equipment (Electrical and Electrochemical Methods) | Electrical-resistance probes as an anchor for R ∝ 1/(h₀ − h) (M4.3) | none | UNSURE |
| 41 | Alduchov, Eskridge, 1996 | Improved Magnus form approximation of saturation vapor pressure, J. Appl. Meteorol. 35, 601–609 | Magnus coefficients (M12; A9) | coefficients 17.625, 243.04 °C, 610.94 Pa | fairly certain |
| 42 | CEN | EN 1999-1-3, Eurocode 9: Design of aluminium structures — Structures susceptible to fatigue | Reduction of detail category with exposure condition (possible anchor for M4.3) | table number UNSURE | content UNSURE |
| 43 | TEMA | Standards of the Tubular Exchanger Manufacturers Association | Fouling resistances (M11) | table UNSURE | values UNSURE |

Citation count: 43. No reference was invented knowingly; items 9, 10, 40, 42, 43 are the least certain and should be checked first, together with the values of M02, M03, M08, M29, L03 and L07.

---

## 5. Provisional M4 default rules and open points

**PROVISIONAL. Level `derived`. Not to be adopted before the spec rows are computed and the citations checked.**

### 5.1 Provisional default for rates

Rule R (one default):
Σ̇_total = Σ̇_corr + Σ̇_fat + Σ̇_op + d/dt[K_ox·√t_age] (+ linear scale-loss term where a loss rate is declared),
each term computed separately, at the pristine section, at the prescribed part temperature, at fixed duty. Oxidation with declared scale loss uses parabolic + linear.

Validity range (all must hold; thresholds provisional, from A3, A6, D5, D6):
- section-loss fraction at end of life x_e ≤ 0.1/p for every rate (p from 2.2);
- self-heating ΔT ≤ 0.05·R·T²/Q for every thermally activated term, when the environment temperature (not the part temperature) is the prescribed quantity;
- scale thickness at end of life below δ_c and cyclic strain amplitude below ε_c (no cracking or spallation);
- load cases not concurrent, or damping linear.

Must flag (rule still usable with a stated multiplier): x_e between 0.1/p and 0.3/p (apply M_lin or M_par of A1, A2); series resistance R_f/R₀ above 0.1 (apply 1 + R_f/R₀); paralinear regime (state the band [max(parabolic, linear), parabolic + linear]).
Must reject: constant-voltage or other non-fixed-duty function; displacement-controlled loading; spallation or breakaway without a declared loss rate; loop gain α·ΔT₀/(1−x) above 0.5; Σ̇_op taken from a boundary power balance together with component terms.
Bound mode for a verdict: s at the rule value (lower bound, where couplings are accelerating); g with each term at its end-of-life state (upper bound).

### 5.2 Provisional default for wearout life

Rule W (one default):
τ_M = [Σ_l ν_l/N_l]⁻¹ (Miner over load cases; N_l from an S–N curve valid for the service environment);
t_c = h₀/(n_s·r) for a wall, d₀/(2r) for a round strut (r the recession rate, linear);
τ_c = t_c·{1 − [1 + (q−1)·τ_M/t_c]^(−1/(q−1))}, q = p·m;
τ_wearout = min(τ_c, x_allow·t_c).
It reduces to the current rule when one load case dominates and τ_M ≪ t_c, and to the recession life when τ_M ≫ t_c.

Validity range: load cases sequential (or cycle-counted on the combined history first); load-controlled stress; uniform recession (no pitting); S–N curve measured in the service environment at a frequency not above the service frequency.
Must flag: only an air S–N curve available (then τ_wearout is an upper bound on life; state it); parabolic recession (use C9 instead of the closed form); q·τ_M/(2·t_c) below 0.05 (section loss may be ignored).
Must reject: concurrent load cases without cycle counting; pitting alloy with only a uniform rate and no pitting factor; displacement-controlled loading treated as load-controlled; environment more aggressive than that of the S–N data with no knockdown.
Bound mode: s at min(τ_M, t_c) with the air curve (upper bound on life); g at the C8 lower bound with the environment curve and a reduced damage sum.

### 5.3 Anchors (provisional; availability UNSURE)

- Rule R: paralinear data (Tedmon 1966; Opila and Hann 1997) for the oxidation band; electrical-resistance corrosion probes for the section-loss multiplier; a cyclic-oxidation mass-change series for the spallation flag.
- Rule W: air versus free-corrosion S–N curves of DNV-RP-C203 (welded steel) as the public code anchor; pre-pitted aluminium fatigue data (Sankaran et al. 2001; Dolley et al. 2000); a paired air and 3.5 % NaCl S–N set for one aluminium alloy (source not identified with certainty, L01).
- Proposed test if no dataset is found: load-controlled fatigue of thin struts (0.3 to 1 mm) in salt fog and in laboratory air at two frequencies, life ratio compared with C10, C11 and C13.

### 5.4 Open points

1. Are GMS-220 load cases sequential or concurrent? If concurrent, M2.3 (factor (1+s)^m) outranks every other finding, and Rule W needs cycle counting in front.
2. No public aluminium corrosion-fatigue S–N pair is identified with certainty; k₅, k₈ (L01) are UNSURE, and the aluminium life factor (about 40 to 350) rests on them.
3. Miner under continuously rising stress: the damage-curve approach predicts longer lives than the closed form (C14); which is closer is not anchored, nor is the reduced damage sum (0.3).
4. Uniform recession is a poor model for aluminium (pitting): pitting factor, pit growth law and ΔK_th are low-confidence inputs; additive-manufactured surfaces are not covered.
5. The cost form and the verdict form (ratio or difference; whether an "undetermined" class exists) were inferred, not read from the spec; M3 depends on them.

