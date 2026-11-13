# Prompt 1b plan (stage S1, planner)

Context file (`local_docs/`, never cited by the spec). Written 2026-11-13. Question: `local_docs/fable_questions.md`, section "Prompt 1b", fenced block. Format: `local_docs/orchestration/fable_delegation_plan.md` §3.

**Status of everything here: claim at level `derived` (unverified).** No code was written or run and no source was looked up. Every number in this file is a hand estimate by S1 from memory and mental arithmetic. The numbers that count are the ones S2 produces from the spec in §3. Where an "expected range" is missed, that is information for S4, not an S2 error.

Three kinds of item are marked UNSURE:

- correlation constants quoted from memory (S3 should confirm them against the source; S2 implements them as written here in any case),
- material and kinetic input values quoted from memory,
- citations whose existence or details I am not certain of.

---

## 0. Scope and conventions

- Claim B is tested for the case the prompt gives: Q = 100 W, base 60 mm × 60 mm, fin height 30 mm, air cooling. I add: fully ducted flow along one 60 mm side (no bypass), base thickness 5 mm, inlet air at T₀ = 298.15 K, laminar flow, fan air power V̇·ΔP between 0.01 and 1 W. These additions are assumptions, stated in §3.0.
- "Equal envelope" means the same 60 × 60 × 30 mm fin volume and the same base thickness. "Equal fan power" means equal air power P_air = V̇·ΔP. A second comparison uses the same fan curve, and a third uses equal volume flow, because "equal fan power" is not the only fair constraint.
- R_fa is the thermal resistance from fin root to inlet air, (T_root − T_in)/Q. It includes the air temperature rise. R_hot adds the base.
- Three candidate architectures are compared with the Cu plate-fin incumbent: (a) the same plate-fin architecture in aluminium, (b) AM AlSi10Mg cylindrical pin fins, (c) an AM AlSi10Mg sheet-gyroid lattice. Case (a) is not in the prompt. It is included because it is the comparison a designer would make first, and it decides whether the lattice is needed at all.
- Claim C uses current densities per cm² because the electrochemical literature does. "Real" area means electrochemically active area. J is the apparent (projected) current density, j_loc = J/R_f.
- Symbols: k solid conductivity; h heat transfer coefficient; C = ρ·V̇·c_p air capacity rate; NTU = η_o·h·A_wet/C; f_F Fanning friction factor; j = St·Pr^(2/3) Colburn factor; b = RT/(αF) the natural Tafel slope; b10 = 2.303·b.

---

## 1. Claims

Confidence is my confidence that the claim survives S2, S3 and S5. "Row" refers to §3.2.

### B1: the entropy expression

| ID | Claim | Confidence | Falsified by |
|---|---|---|---|
| B1.1 | The two-temperature expression is exact only as a dead-state closure: with T_coolant = T₀ (inlet and ambient) it equals the sum of base conduction, fin conduction, film, and exhaust-mixing generation, Ṡ_th = Q(1/T₀ − 1/T_hot). No separate terms for base, fins or air temperature rise are needed in that form; they are a partition of it (derivation D1). | high | Row B16: the four separately integrated terms do not sum to Q(1/T₀ − 1/T_hot) within 0.5 %. |
| B1.2 | If T_coolant is read as the local or mean air temperature (the usual reading of "coolant temperature"), the expression leaves out the mixing of warm exhaust with ambient, C·[(T_out − T₀)/T₀ − ln(T_out/T₀)]. For the worked case this is 25–45 % of the thermal term, so it is not a small correction. The exact "coolant temperature" for the sink alone is the logarithmic mean (T_out − T_in)/ln(T_out/T_in). | medium | Row B16: mixing share below 10 % for the optimised Cu sink at P_air = 0.1 W. |
| B1.3 | Evaluating pumping work at T₀ is right in the dead-state closure and only there. Locally the dissipation generates V̇ΔP/T_air; the remainder appears when the exhaust is brought to T₀. Mixing T₀ for the pump with a local T_coolant for the heat is inconsistent. The size of the inconsistency in the pump term is below 10 % of that term. | high | Row B18: ideal-gas entropy flux ṁ·R·ln(p_in/p_out) differs from V̇ΔP/T_in by more than 0.1 %; or a derivation showing the remainder is not recovered at T₀. |
| B1.4 | V̇·ΔP is air power, not the work input. The term should be W_fan,elec/T₀ = V̇ΔP/(η_fan·T₀); for small axial fans η_fan is roughly 0.1–0.4, so the prompt's pump term is low by a factor 2.5–10. | high for the structure, medium for the η_fan range | A fan data source showing total efficiency above 0.6 for 60 mm class fans. |
| B1.5 | For a non-uniform base, the T_hot that makes the entropy term exact is the heat-flux-weighted harmonic mean temperature of the heat-input surface. It differs from the flux-weighted arithmetic mean by about 0.1 K or less here. The temperature that defines the function (device limit) is the maximum, a different number, several kelvin higher for a concentrated source. One temperature cannot serve both purposes. | high | Row B17: harmonic and arithmetic means differ by more than 0.5 K, or T_max − T_mean below 0.5 K for the 20 mm source. |
| B1.6 | Adversarial point against the framework's use of this term. Counted from the electrical work dissipated in the device, total generation is (Q + W_fan)/T₀ for every heat sink. The "sink" term Q(1/T₀ − 1/T_hot) only says how much of Q/T₀ is generated outside the device rather than inside it. A worse sink (hotter device) has a larger sink term; a better sink a smaller one; the total is unchanged. So the thermal term cannot rank sinks. At equal function (same Q, same T_max) the operating difference between candidates is ΔW_fan/T₀ and nothing else. | high | A balance in which two sinks at equal Q and equal W_fan give different total generation with the exhaust returned to T₀ (would need Q to depend on temperature, see B1.7). |
| B1.7 | What the thermal term omits that does depend on the sink: temperature-dependent device losses (Q rises with T), device life (a replacement term in Σ, not an operating term), and the thermal interface. These, not the Ṡ expression, are where a hotter base costs something. | medium | Not computable here; S4 to state as scope. |
| B1.8 | The pump term is small against the thermal term: about 1 % for air power, about 5 % for electrical fan power, at P_air = 0.1 W. Radiation from the envelope is below 3 % of Q under forced flow. | medium | Rows B16, B19. |

### B2: can the Al lattice match the Cu fin sink

| ID | Claim | Confidence | Falsified by |
|---|---|---|---|
| B2.1 | Governing groups (derivation D4, D5): fin parameter mH with (mH)² = h·P_f·H²/(k·A_c); NTU = 4·η_o·St·L/D_h; the surface group j/f_F^(1/3) with A_wet^(2/3) at fixed pumping power; the capacity group A_flow^(2/3)·D_h^(1/3)·f_F^(−1/3); for the base, ε = a_s/b_p, τ = t_b/b_p and Bi = 1/(π·k·b_p·R_fa). Bejan number Be = ΔP·L²/(μ·α) sets the optimal plate spacing. | high for the derivation | Row B05: optimal plate gap outside 0.6–1.6 × the Bejan–Sciubba value; row B10: exponent of R_fa against P_air outside −0.15 to −0.40. |
| B2.2 | "Larger wetted area compensates for the lower conductivity" is true only in a square-root sense and only for a long fin. For mH ≫ 1 the conductance per base area tends to sqrt(h·a_sf·k_eff), so a factor 2.2–3.9 in k needs the same factor in h·a_sf. For mH ≪ 1, k does not matter and area is everything. At H = 30 mm in air all practical designs sit at mH ≈ 0.8–2.5, between the limits. | high | Row B01: closed-form η_f disagrees with a finite-difference fin solution by more than 0.5 %. |
| B2.3 | Material swap at fixed geometry (0.4 mm fins, about 1.5 mm gaps): fin efficiency falls from about 0.79 (Cu) to about 0.52–0.64 (k = 100–180 W/m/K), but R_fa rises only about 8–25 %, because roughly two thirds to three quarters of R_fa is the caloric resistance 1/C, which does not depend on the solid. | medium | Row B04: R_fa ratio Al/Cu above 1.35 at k = 150. |
| B2.4 | With thicker fins and a re-optimised count, an aluminium plate-fin sink reaches within about 5–20 % of the optimised Cu plate-fin R_fa at equal fan power (k = 150–200). So the fair incumbent for an AM lattice is an aluminium plate-fin sink, which needs no AM. The substitution of Cu by Al in heat sinks does not depend on a lattice. | medium | Row B05: optimised Al (k = 150) R_fa more than 30 % above optimised Cu at P_air = 0.1 W. |
| B2.5 | AM Al pin fins, fully ducted, equal envelope and equal fan power: R_fa is higher than for optimised plate fins of either metal, by roughly 20–70 % at P_air = 0.1 W, even with the more favourable of two friction correlations and the more favourable Nusselt correlation. The cause is form drag: flow rate falls and the caloric limit 1/C rises. | medium | Row B07: best pin-fin R_fa at or below best Cu plate-fin R_fa at any P_air in 0.01–1 W. |
| B2.6 | Gyroid lattice, same constraints: with packed-bed-like (Ergun) friction the caloric limit 1/C alone exceeds the Cu plate-fin R_fa, so no heat-transfer coefficient can rescue it. A match needs both friction within about 3–10 × smooth-channel values (c_f ≤ 0.3 in row B09) and j/f_F ≥ about 0.25, which is the value for smooth channels and above what bluff or tortuous surfaces usually reach (0.05–0.2). I therefore expect: no match. This rests on a parametric model, not on a validated gyroid correlation. | low to medium | Row B09 gives χ_min below 0.15 for c_f ≥ 0.3; or published gyroid air data (B3) with j/f_F ≥ 0.25 at Re_h 200–2000 and friction within 3 × channel flow. |
| B2.7 | Answer to B2 as posed: no, not at equal envelope and equal fan power in ducted laminar flow. Al plate fins come close (B2.4); pins and lattices do not. Regimes where a lattice can win are different constraints: equal volume flow with pressure to spare, impinging or unducted or natural-convection flow, a mass limit instead of a volume limit, or very short flow length. | medium | Rows B05, B07, B09, B11, B13 taken together. |
| B2.8 | With a concentrated source (20 × 20 mm on the 60 × 60 × 5 mm base) the base adds about 0.08 K/W in Cu and about 0.16–0.30 K/W in AlSi10Mg (k = 180–100). The Al penalty of 0.1–0.2 K/W is as large as the whole fin-side difference between architectures, and sits upstream of the fins, so no wetted area can compensate it. Geometry can help only as base thickness, or by adding a spreader (heat pipe, vapour chamber, Cu insert). | medium | Row B14: Al-minus-Cu base penalty below 0.04 K/W at k = 150. |
| B2.9 | AlSi10Mg conductivity: as-built LPBF about 100–130 W/m/K (direction dependent); after stress relief or T6 about 150–180. The prompt's 120–180 is right at the top and somewhat high at the bottom. Thin walls with porosity and rough surfaces sit lower again. | medium | S3: the supplier data sheet or Yang et al. 2018 / Sélo et al. 2020 give as-built values above 140. |
| B2.10 | Worked estimate, Cu plate fins at P_air = 0.1 W: about 30 fins of 0.3–0.5 mm, gap 1.2–1.8 mm, V̇ ≈ 3.5–5 L/s, ΔP ≈ 18–32 Pa, air rise 15–25 K, R_fa ≈ 0.24–0.31 K/W, so the base runs about 24–31 K above inlet. | medium | Row B03 and B05 outside these ranges. |
| B2.11 | "The price is fan exergy" is incomplete in two ways. (i) At equal function, the extra fan electricity over a 5-year life is of the same order as the primary-metal embodied energy of either sink (tens of MJ each). (ii) Primary Al and primary Cu have roughly equal cumulative energy demand per unit volume, and LPBF processing adds more, so Σ_init does not obviously favour the AM Al part. | low (input data UNSURE) | Row B20 with S3-confirmed inputs: life fan-energy penalty below 10 % of the embodied-energy difference, or Al/Cu CED per volume outside 0.4–2. |
| B2.12 | The 1-D fin model assumes the air is mixed over the fin height. In real plate channels and lattices it is not; the air near the root overheats while the air near the tip is under-used. This bias favours low-η designs (Al, lattice), so the model is, if anything, generous to the candidate. | medium | A 2-D conjugate calculation or measured data showing the opposite sign. Not in this spec (no 2-D solver). |

### B3: anchors

| ID | Claim | Confidence | Falsified by |
|---|---|---|---|
| B3.1 | Plate-fin and pin-fin sinks have closed-form models validated against air data: Teertstra et al. 2000 and Culham & Muzychka 2001 (plate), Khan et al. 2005 and Žukauskas 1972 (pin), Jonsson & Moshfegh 2001 (plate, strip and pin, with bypass). These are equations in papers, not datasets; the journals are not open access. | medium | S3. |
| B3.2 | Air-side measurements on AM aluminium heat sinks and lattices exist (Wong et al. 2009; Ho et al. 2020), with thermal resistance or Nu against pressure drop or pumping power. I know of no public repository holding such data; I expect figures and tables only. | medium for existence, low for "no repository" | S3 finds a repository or supplementary data file with R_th–ΔP data. |
| B3.3 | TPMS and gyroid Nu and friction correlations exist in several papers (list in §4), but each is tied to one geometry family, porosity, wall thickness, fluid and Re range, with differing length scales; several are CFD only and several are for liquids or two-fluid exchangers. There is no general validated gyroid correlation for air at Re_h of order 10²–10³. | medium | S3 finds a correlation covering air, Re_h 200–2000, with experimental validation. |
| B3.4 | Effective conductivity of AM AlSi10Mg TPMS lattices has been measured (Catchpole-Smith et al. 2019; Sélo et al. 2020) and falls at or below the Hashin–Shtrikman upper bound 2ρ̄/(3 − ρ̄). | medium | S3. |
| B3.5 | Metal-foam correlations (Calmidi & Mahajan 2000; Boomsma et al. 2003) are the nearest well-established analogue and show friction far above channel flow at equal hydraulic diameter. | medium | S3. |

### C1: is the substitution like-for-like

| ID | Claim | Confidence | Falsified by |
|---|---|---|---|
| C1.1 | No. Pt is the benchmark for hydrogen evolution (and for fuel-cell hydrogen oxidation and oxygen reduction). NiFe (oxy)hydroxide is the benchmark for oxygen evolution in alkaline electrolyte. The scarce incumbent for oxygen evolution is Ir or Ru oxide in acid, not Pt. | high | A source showing NiFe foam used as the primary cathode catalyst replacing Pt at 1 A/cm² with comparable overpotential. |
| C1.2 | The pH regimes differ. NiFe (oxy)hydroxide is not stable in acid. Pt hydrogen evolution in alkali is about two orders of magnitude slower than in acid. A Pt-to-NiFe comparison therefore compares systems (acid membrane cell with Pt, Ir, Ti hardware against alkaline or anion-membrane cell with Ni-based electrodes and KOH), not materials at one electrode. | high | S3: Sheng et al. 2010 does not report the acid/alkaline ratio as two orders. |
| C1.3 | If one electrode and one electrolyte are enforced (alkaline hydrogen evolution), the non-noble comparators are Ni, NiMo and Raney Ni. NiFe has modest hydrogen-evolution activity (about 0.2 V at 10 mA/cm² geometric on foam). | medium | S3. |
| C1.4 | For alkaline oxygen evolution, NiFe on a geometric-area basis already beats Pt by several hundred mV at 1 A/cm² and is comparable with Ir oxide, without any roughness argument. Framed as Pt → NiFe for this reaction, the substitution claim is vacuous. | medium | Row C05 with S3-confirmed inputs gives NiFe within 0.1 V of Pt for oxygen evolution. |

### C2: required roughness factor and its limits

| ID | Claim | Confidence | Falsified by |
|---|---|---|---|
| C2.1 | With equal transfer coefficients the matching condition is R_f,cand/R_f,Pt = j₀,Pt/j₀,cand. It does not depend on J or on whether the arcsinh or the Tafel form is used. | high | Row C03: computed R_f differs from the ratio by more than 10⁻⁶ relative, or varies with J. |
| C2.2 | The Pt electrode is not flat. A Pt/C layer has R_f,Pt of order 100–200 (0.1–0.3 mg/cm² at 60–80 m²/g). Comparing a rough NiFe foam with flat Pt, as the prompt's expression invites, is unfair to Pt by that factor. | high | S3: typical Pt/C roughness below 20. |
| C2.3 | Numbers for hydrogen evolution with j₀ per real area: against Pt in alkali (j₀ ≈ 6 × 10⁻⁴ A/cm²), a candidate with j₀ = 10⁻⁵–10⁻⁶ needs R_f = 60–600 against flat Pt and 6 × 10³–6 × 10⁴ against Pt/C with R_f = 100. Against Pt/C in acid (j₀ ≈ 0.2 A/cm²) it needs 2 × 10⁶–2 × 10⁷. | medium (j₀ values uncertain by an order) | Row C03 arithmetic; S3 on j₀ values. |
| C2.4 | Pt/C in an acid cell at 1 A/cm² has a hydrogen-evolution activation overpotential of only 1–5 mV. "Matching Pt" in that system means near-zero activation loss, which no base-metal roughness reaches. | medium | S3: Bernt et al. 2018 reports tens of mV. |
| C2.5 | Electronic resistance of a metallic Ni foam is not a limit: below 1 mV through 1.6 mm at 1 A/cm², by either of two effective-conductivity models. | high | Row C06 above 1 mV. |
| C2.6 | Ionic resistance of the electrolyte in the pores is the first-order limit. With Tafel kinetics the reaction is confined to a depth L_eff = 2·κ_eff·b/J, about 0.1–0.6 mm at 1 A/cm² and 25 °C. A 1.6 mm foam uses roughly 10–35 % of its area (derivation D8). | medium | Row C07: utilisation above 0.6 for 30 wt% KOH at 25 °C, 1.6 mm, α = 0.5; or the closed form disagrees with numerical integration by more than 1 %. |
| C2.7 | Because of C2.6 there is a thickness-independent floor on overpotential, η_min = b·acosh(1 + J²/(4·κ_eff·a_v·j₀·b)). Matching Pt/C in alkali needs a_v·j₀ of order 2 × 10⁶ A/m³ or more (for example 0.1 µm pores with j₀ = 10⁻⁵ A/cm², or 1 µm pores with 10⁻⁴). Matching Pt/C in acid is out of reach for any pore size above the nanometre range. So "reachable" depends on the reference: yes against flat Pt in alkali, marginal against Pt/C in alkali, no against Pt/C in acid. | low to medium (ignores gas in pores and concentration gradients, both of which make it worse) | Row C08. |
| C2.8 | Gas bubbles add two penalties not in C2.6–C2.7: surface coverage of about 0.3–0.4 at 1 A/cm² (about 20–25 mV at α = 0.5) and a lower κ_eff from gas hold-up. Sub-micron pores that give the area in C2.7 are the ones that vent gas worst. | low to medium | S3 on Vogt & Balzer 2005; row C10. |
| C2.9 | Reactant supply: alkaline oxygen evolution consumes OH⁻ and in 1 M KOH approaches the diffusion limit near 1 A/cm² for a 50 µm boundary layer; concentrated KOH (about 7 M) removes this. Alkaline hydrogen evolution consumes water and is not reactant-limited. Data taken in 1 M KOH at 10 mA/cm² therefore do not transfer to 1 A/cm². | medium | Row C09. |
| C2.10 | R_f itself is poorly defined for NiFe (oxy)hydroxide: double-layer capacitance does not measure its active area (the resting phase is a poor conductor), and j₀ per real area depends on Fe content. Reported R_f and j₀ pairs are uncertain by an order of magnitude each. | medium | S3 on Trasatti & Petrii 1991 and Wei et al. 2019. |

### C3: what the activation-only model omits

| ID | Claim | Confidence | Falsified by |
|---|---|---|---|
| C3.1 | The symmetric arcsinh form fixes the Tafel slope at 59.2/α mV per decade (118 mV at α = 0.5, 25 °C). NiFe oxygen evolution shows 30–40 mV per decade and Pt hydrogen evolution in acid about 30. With the measured slope, each decade of R_f buys only one Tafel slope of overpotential, so area is a weak lever exactly where the kinetics are already good. | high | Row C01, C04; S3 on reported slopes. |
| C3.2 | Omitted losses are larger than the activation difference at issue: ohmic loss across separator and electrolyte (0.1–0.3 V at 1 A/cm²), the other electrode (oxygen evolution, 0.3–0.4 V), bubble and concentration overpotentials, and contact resistances. The verdict depends on cell voltage, not on one electrode's activation term. | high | Row C11. |
| C3.3 | Σ̇_act = I·η/T₀ overstates the generation. The heat is released at cell temperature, so the local generation is I·η/T_cell (0.84 of the prompt's value at 80 °C); below the thermoneutral voltage that heat is absorbed by the endothermic reaction and never reaches T₀. | medium | Derivation D10 shown wrong. |
| C3.4 | Durability is omitted and enters Σ through replacements: Fe loss from NiFe, layer detachment under gas evolution at 1 A/cm², reverse-current damage on shutdown. The framework's wear-out term, not Σ̇_act, may decide. | medium (qualitative) | Not computable here. |
| C3.5 | On an energy basis alone the substitution cannot pay: the embodied energy of a 0.3 mg/cm² Pt loading equals the extra electricity from about 0.5 mV of overpotential held for 40 000 h at 1 A/cm². Any realistic NiFe-for-Pt penalty (tens of mV) repays the Pt in days. The case for substitution has to rest on scarcity (the framework's λ term), and that case is stronger for Ir than for Pt. | low to medium (embodied-energy value UNSURE) | Row C13 with S3-confirmed Pt cumulative energy demand: break-even above 10 mV. |
| C3.6 | Temperature is omitted: j₀ and κ both rise strongly from 25 to 80 °C, so 25 °C inputs understate both the kinetics and the penetration depth. The ratios in C2.1–C2.3 are less sensitive than the absolute values. | medium | Not computed; S4 to note. |

---

## 2. Derivations

### D1. Complete entropy balance for the heat sink

Control volume 1: base, fins, and the air between duct inlet (T_in, p_in) and outlet (T_out, p_out). Steady state, heat Q enters through the heat-input surface with local flux q″ and local temperature T_s. Entropy balance, air as an ideal gas:

  Ṡ_gen,1 = ṁ·c_p·ln(T_out/T_in) + ṁ·R_air·ln(p_in/p_out) − ∫ (q″/T_s) dA.

Define T_hot by ∫ (q″/T_s) dA = Q/T_hot (see D2). With ΔP ≪ p, ṁ·R_air·ln(p_in/p_out) = V̇·ΔP/T_in to first order (D3). With Q = C·(T_out − T_in) and the logarithmic mean air temperature T_lm = (T_out − T_in)/ln(T_out/T_in):

  Ṡ_gen,1 = Q·(1/T_lm − 1/T_hot) + V̇·ΔP/T_in.

So for the sink alone the expression in the prompt is exact when T_coolant = T_lm. Inside this term, by location:

- base: Q·(1/T_root − 1/T_hot) for an isothermal root;
- fin conduction: ∫ q″_w·(1/T_w − 1/T_root) dA over the wetted surface, T_w the local wall temperature;
- film: ∫ q″_w·(1/T_air − 1/T_w) dA, T_air the local bulk air temperature;
- the sum of the last two is C·ln(T_out/T_in) − Q/T_root.

Control volume 2: the exhaust plume returning to T₀ at p₀ (with T_in = T₀):

  Ṡ_mix = Q/T₀ − C·ln(T_out/T₀) = C·[(T_out − T₀)/T₀ − ln(T_out/T₀)] = Q·(1/T₀ − 1/T_lm).

Sum of both control volumes: Ṡ_th = Q·(1/T₀ − 1/T_hot). The pumping work adds its lost work over T₀ (D3). Add the fan's own losses and the total is

  Ṡ_gen = Q·(1/T₀ − 1/T_hot) + W_fan,elec/T₀,  W_fan,elec = V̇·ΔP/η_fan.

One level up, control volume 0 is the device, which turns electrical work Q into heat at T_hot: Ṡ_dev = Q/T_hot. The grand total is (Q + W_fan,elec)/T₀, independent of the sink (claim B1.6).

Not in this balance: transverse non-uniformity of air temperature inside a channel (it is inside the film term once bulk temperature is used), radiation (row B19), interface resistance (row B15), bypass flow (excluded by the ducted assumption).

### D2. The right T_hot

Entropy enters the sink at rate ∫ q″/T_s dA. So T_hot = Q / ∫ (q″/T_s) dA, the flux-weighted harmonic mean over the heat-input surface. Expanding about the flux-weighted arithmetic mean T̄: T_hot ≈ T̄ − Var_q(T_s)/T̄. With a temperature range ΔT_r over the source, Var ≤ ΔT_r²/4, so T̄ − T_hot ≤ ΔT_r²/(4·T̄). For ΔT_r = 10 K at 330 K this is 0.08 K. The design constraint, however, is T_max. Using T_max in the entropy term overstates it by Q·(1/T̄ − 1/T_max). Recommendation to carry forward: entropy term with the source-area mean temperature; function constraint on T_max; both reported.

### D3. Pumping term

Viscous dissipation Φ = V̇·ΔP occurs in air at local temperature T_air ∈ [T_in, T_out], generating Φ/T_air there. The dissipated energy leaves with the exhaust and is rejected to T₀, generating Φ·(1/T₀ − 1/T_air). The total is Φ/T₀ (Gouy–Stodola), independent of where the dissipation happened. Ideal-gas check: ṁ·R_air·ln(p_in/p_out) = (p·V̇/T)·ln(1 + ΔP/p_out) ≈ V̇·ΔP/T·(1 − ΔP/(2p)); the correction is 10⁻⁴ at ΔP = 25 Pa. The fan converts W_elec into V̇·ΔP plus heat; all of it ends at T₀, so the fan term is W_elec/T₀.

### D4. Fin efficiency, discrete and homogenised

Discrete fin, uniform h, adiabatic tip (the duct shroud): θ″ = m²·θ, m² = h·P_f/(k·A_c), η_f = tanh(mH)/(mH). Plate fin: m² = 2h/(k·t). Cylindrical pin: m² = 4h/(k·d).

Homogenised lattice treated as a porous fin standing on the base: solid-phase energy balance k_eff·θ″ = h·a_sf·θ, with a_sf the wetted area per unit volume and k_eff the effective conductivity of the lattice in the height direction. So m² = h·a_sf/k_eff and the same η. For parallel plates a_sf = 2/(s + t) and k_eff = k·t/(s + t), which returns m² = 2h/(k·t); this is the limiting case used as a code check (row B08). For a sheet gyroid, a_sf = 2·3.0915/a (two sides of a thin sheet, cell size a) and k_eff ≤ k·2ρ̄/(3 − ρ̄) (Hashin–Shtrikman upper bound with non-conducting voids).

Conductance per unit base area: G″ = sqrt(h·a_sf·k_eff)·tanh(mH).

- Short fin (mH ≪ 1): G″ → h·a_sf·H. Conductivity is irrelevant; area is everything.
- Long fin (mH ≫ 1): G″ → sqrt(h·a_sf·k_eff). To hold G″ when k_eff falls by a factor r, h·a_sf must rise by r. The height beyond about 1.5/m is dead material.

At equal h, an Al plate fin has the same η as a Cu fin when t_Al = t_Cu·k_Cu/k_Al (2.2–3.9 × thicker for k = 180–100). The extra thickness is paid in open flow area.

### D5. Equal fan power: what is conserved and what scales

Definitions: A_wet = 4·A_flow·L/D_h (definition of D_h for a uniform passage); ΔP = f_F·(4L/D_h)·(ρu²/2) with f_F the apparent Fanning factor including form drag; V̇ = A_flow·u; St = h/(ρ·u·c_p); j = St·Pr^(2/3). Then

  P_air = V̇·ΔP = f_F·A_wet·ρ·u³/2,
  C = ρ·c_p·A_flow·u = ρ·c_p·A_flow·[2·P_air/(f_F·ρ·A_wet)]^(1/3),
  NTU = η_o·h·A_wet/C = 4·η_o·St·L/D_h,
  R_fa = 1/(C·(1 − exp(−NTU))).

Limits:

- Low NTU: R_fa → 1/(η_o·h·A_wet) with h·A_wet = (j/f_F^(1/3))·A_wet^(2/3)·(2·P_air)^(1/3)·ρ^(2/3)·c_p·Pr^(−2/3). Here area helps as A_wet^(2/3) and the surface is ranked by j/f_F^(1/3).
- High NTU: R_fa → 1/C ∝ f_F^(1/3)·A_wet^(1/3)/A_flow. Here more area makes things worse; what counts is open, low-drag passage.

For this geometry at P_air ≈ 0.1 W, NTU ≈ 1–2 for the good designs, so both limits matter. A surface that adds area by adding form drag moves toward the caloric limit. This is the quantitative content of "the price is fan exergy": the price is paid as lost flow rate, not only as fan power.

Optimal plate spacing at fixed ΔP (Bejan & Sciubba 1992): s_opt ≈ 2.7·L·Be^(−1/4), Be = ΔP·L²/(μ·α). Used as an independent check on the swept optimum.

### D6. Base spreading

Closed form of Lee, Song, Au and Moran (1995) for a centred source of area A_s on a plate of area A_p, thickness t_b, conductivity k, with a uniform resistance R₀ on the far side (model M-SP in §3.1; constants from memory, UNSURE). Limits used as checks: ε → 1 gives the slab t_b/(k·A_p); a small source on a thick plate gives the half-space results R_max = 1/(π·k·a_s) (exact for uniform flux) and R_avg = 8/(3π²·k·a_s) (exact; the model gives 0.2821/(k·a_s), 4.4 % high).

### D7. Activation model and the matching condition

Butler–Volmer with α_a = α_c = α: j = j₀·[exp(αFη/RT) − exp(−αFη/RT)] = 2·j₀·sinh(η/b), b = RT/(αF). So η = b·asinh(j/(2j₀)), as in the prompt. Limits: η → b·ln(j/j₀) for j ≫ j₀ (Tafel); η → b·j/(2j₀) for j ≪ j₀ (linear).

Matching a candidate (subscript c) to a Pt reference at the same J:

  b_c·asinh(J/(2·R_c·j₀c)) = b_Pt·asinh(J/(2·R_Pt·j₀Pt)) = η_Pt
  ⇒ R_c = J / (2·j₀c·sinh(η_Pt/b_c)).

If b_c = b_Pt this reduces to R_c = R_Pt·j₀Pt/j₀c for every J. If the slopes differ the answer depends on J; in the Tafel regime R_c ≈ (J/j₀c)·exp(−η_Pt/b_c). Each tenfold increase in R_c lowers η by b10 (Tafel regime).

### D8. Utilisation of a porous electrode

One-dimensional porous electrode, thickness L, separator at x = 0, current collector at x = L, solid phase equipotential (justified by D9), no concentration gradients, volumetric area a_v, Tafel kinetics j = j₀·exp(η/b). Ionic current balance: κ_eff·η″ = a_v·j₀·exp(η/b), with −κ_eff·η′(0) = J and η′(L) = 0. Solution: η/b = c + 2·ln sec(θ·(1 − x/L)), with θ ∈ (0, π/2) from

  2·θ·tan θ = δ,  δ = J·L/(κ_eff·b).

Utilisation (ratio of the uniform-reaction current to the actual front-face rate, equal to effective over total roughness):

  E = sin(2θ)/(2θ);  E → 1 − δ/3 for δ ≪ 1;  E → 2/δ for δ ≫ 1.

So for a thick electrode the active depth is L_eff = E·L → 2·κ_eff·b/J, and the overpotential penalty against full use of the same area is b·ln(1/E).

Thickness-independent floor, symmetric Butler–Volmer kinetics, semi-infinite electrode. First integral of κ_eff·η″ = 2·a_v·j₀·sinh(η/b): (κ_eff/2)·η′² = 2·a_v·j₀·b·(cosh(η/b) − 1). At the front, κ_eff·abs(η′) = J:

  η_min = b·acosh(1 + J²/(4·κ_eff·a_v·j₀·b)).

Tafel limit: J = sqrt(2·κ_eff·a_v·j₀·b)·exp(η/(2b)) (the known doubling of the Tafel slope). Linear limit: η = J·sqrt(b/(2·κ_eff·a_v·j₀)). η_min includes the ionic drop inside the pores; it is the electrode's polarisation seen from the separator face.

Pore-scale inputs: κ_eff = κ·(ε·(1 − ε_g))^1.5 (Bruggeman, ε porosity, ε_g gas fraction of the pore space); a_v ≈ 4·ε/d_pore for cylindrical pores.

### D9. Electronic drop in the foam

Uniform reaction through the thickness, current collected at the back: the electronic current density rises linearly from 0 to J, so the drop across the foam is J·L/(2·σ_eff). Two models for σ_eff bracket an open-cell foam: Lemlich, σ_eff = σ·ρ̄/3, and a power law σ_eff = σ·ρ̄^1.7 (assumed exponent, in the range usually quoted for open-cell metal foams, UNSURE).

### D10. Entropy accounting for the overpotential, and the break-even

The overpotential heat I·η is released at T_cell. Local generation is I·η/T_cell. If the heat is later rejected to T₀ a further I·η·(1/T₀ − 1/T_cell) is generated, giving I·η/T₀ in total. In an electrolyser below the thermoneutral voltage the reaction absorbs heat at T_cell (T·ΔS of the reaction), so overpotential heat is consumed at T_cell and the second part does not occur. The lost work is then T₀·I·η/T_cell, a factor T₀/T_cell of the prompt's value.

Break-even overpotential difference for removing a scarce catalyst on an energy basis: Δη_be = e_x·m″_x/(J·τ_op), with e_x the cumulative energy demand per kg of element x, m″_x the loading per area and τ_op the operating time. This compares primary energy with electricity one-for-one, which favours the substitution (electricity costs more primary energy than that).

---

## 3. Computation spec

### 3.0 Common inputs

All values SI unless stated. "assumed" means my choice; S5 may challenge it.

| Symbol | Value | Unit | Source |
|---|---|---|---|
| Q | 100 | W | prompt |
| W (across flow), L (along flow) | 0.060, 0.060 | m | prompt (60 × 60 mm base) |
| H | 0.030 | m | prompt |
| t_b | 0.005 | m | assumed |
| T₀ = T_in | 298.15 | K | assumed |
| p₀ | 101325 | Pa | assumed |
| ρ (air) | 1.1614 | kg/m³ | air at 300 K, 1 atm (Incropera et al., Table A.4; UNSURE last digit) |
| c_p | 1007 | J/kg/K | same |
| μ | 1.846e-5 | Pa·s | same |
| k_a | 0.0263 | W/m/K | same |
| Pr | 0.707 | – | same |
| R_air | 287.05 | J/kg/K | standard |
| α_a = k_a/(ρ·c_p) | computed | m²/s | – |
| k_Cu | 390 | W/m/K | prompt |
| k_Al set | 100, 120, 150, 180, 200 | W/m/K | 120–180 prompt; 100 as-built low end (assumed); 200 wrought 6063 reference (assumed). Nominal 150 |
| ρ_Cu, ρ_Al | 8960, 2670 | kg/m³ | handbook values |
| P_air set | 0.01, 0.03, 0.1, 0.3, 1.0 | W | assumed. Nominal 0.1 |
| η_fan | 0.25 | – | assumed (range 0.1–0.4) |
| Fan curve | ΔP_fan = 60·(1 − V̇/0.012) | Pa, V̇ in m³/s | assumed generic 60 mm axial fan |
| Source case U | uniform over the full base | – | assumed |
| Source case S | 20 mm × 20 mm, centred, A_s = 4.0e-4 | m² | assumed |
| τ_life | 1.578e8 (5 years) | s | assumed |
| F, R | 96485.33, 8.314462 | C/mol, J/mol/K | CODATA |
| T (electrochemistry) | 298.15 | K | assumed; 353.15 K where a row says so |
| J | 1.0 A/cm² = 1.0e4 A/m² | – | prompt |

All air properties are constant (no temperature dependence). All flows are laminar; a design with Re above the stated limit is excluded from an optimum and listed.

### 3.1 Model definitions

Each model returns R_fa for a given volume flow V̇. Where a row fixes P_air, find V̇ by bisection on V̇ ∈ [1e-6, 0.2] m³/s such that V̇·ΔP(V̇) = P_air, relative tolerance 1e-8 (the product is monotone in V̇). Common closing relations for all three sink models:

- (X1) C = ρ·V̇·c_p; NTU = G/C; R_fa = 1/(C·(1 − exp(−NTU))); ΔT_air = Q/C; T_out = T_in + ΔT_air; T_root = T_in + Q·R_fa.
- (X2) R_base,1D = t_b/(k_base·W·L); base material = fin material.

**M-PF, plate fins.** Design variables: fin thickness t, number of fins N_f. End fins flush with the envelope.

- (PF1) N_ch = N_f − 1; s = (W − N_f·t)/N_ch.
- (PF2) A_flow = N_ch·s·H; u = V̇/A_flow.
- (PF3) D_h = 2·s·H/(s + H); Re = ρ·u·D_h/μ; β = s/H. Valid for Re < 2300.
- (PF4) fRe_fd = 24·(1 − 1.3553β + 1.9467β² − 1.7012β³ + 0.9564β⁴ − 0.2537β⁵) (Shah & London 1978; Fanning).
- (PF5) L⁺ = L/(D_h·Re); f_app = sqrt((3.44/sqrt(L⁺))² + fRe_fd²)/Re.
- (PF6) σ = N_ch·s/W; K_c = 0.42·(1 − σ²); K_e = (1 − σ²)².
- (PF7) ΔP = (4·f_app·L/D_h + K_c + K_e)·ρ·u²/2.
- (PF8) Nusselt number, parallel plates, simultaneously developing, isothermal walls, mean value on the log-mean temperature difference (Stephan 1959 as given in Shah & Bhatti 1987; constants UNSURE): Re_pp = ρ·u·(2s)/μ; x* = L/(2s·Re_pp·Pr); Nu = 7.55 + 0.024·x*^(−1.14)/(1 + 0.0358·Pr^0.17·x*^(−0.64)); h = Nu·k_a/(2s).
- (PF9) m = sqrt(2h/(k·t)); η_f = tanh(mH)/(mH).
- (PF10) A_fin = 2·N_ch·H·L; A_base = N_ch·s·L; G = h·(η_f·A_fin + A_base).
- (PF11) mass = ρ_s·(N_f·t·H·L + W·L·t_b).
- (PF12) Alternative method (Teertstra et al. 2000; constants UNSURE), same V̇ and geometry: Re_b = ρ·u·s/μ; Re_b* = Re_b·s/L; Nu_i = [(Re_b*·Pr/2)^(−3) + (0.664·sqrt(Re_b*)·Pr^(1/3)·sqrt(1 + 3.65/sqrt(Re_b*)))^(−3)]^(−1/3); h_T = Nu_i·k_a/s (referred to wall minus inlet temperature); η_T = tanh(m_T·H)/(m_T·H) with m_T = sqrt(2·h_T/(k·t)); R_fa,T = 1/(h_T·(η_T·A_fin + A_base)).
- Sweep sets. Cu (skived): t ∈ {0.3, 0.4, 0.5, 0.6, 0.8, 1.0} mm. Al: t ∈ {0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0} mm. N_f from 6 upward while s ≥ 0.8 mm (assumed manufacturing limits: Cu skived t ≥ 0.3 mm, LPBF Al t ≥ 0.4 mm, gap ≥ 0.8 mm).

**M-PIN, staggered cylindrical pin fins.** Design variables: d, pitch ratio p = S_T/d, with S_L = S_T.

- (PN1) S_T = S_L = p·d; N_T = floor(W/S_T); N_L = floor(L/S_L); N = N_T·N_L.
- (PN2) U_app = V̇/(W·H); U_max = U_app·S_T/(S_T − d); Re_d = ρ·U_max·d/μ.
- (PN3) Friction, version K (Khan, Culham & Yovanovich 2005, staggered; constants from memory, UNSURE, and I suspect the fit misbehaves for p > 2): K₁ = 1.175·(S_L/(S_T·Re_d^0.3124)) + 0.5·Re_d^0.0807; f_K = K₁·[378.6/p^(13.1/p)]/Re_d^(0.68/p^1.29).
- (PN4) Friction, version J (Jakob 1938 as given in Holman's textbook, staggered; UNSURE constants): f_J = 4·[0.25 + 0.118/((S_T − d)/d)^1.08]·Re_d^(−0.16).
- (PN5) ΔP = N_L·f·ρ·U_max²/2, with f = f_K or f_J. Inlet and exit losses omitted (favours pins).
- (PN6) Nusselt, version K (same 2005 paper; UNSURE constants): C₁ = 0.61·p^0.091·p^0.053/(1 − 2·exp(−1.09·p)); Nu_d = C₁·Re_d^0.5·Pr^(1/3).
- (PN7) Nusselt, version Z (Žukauskas as tabulated in Çengel's textbook; UNSURE constants): Re_d < 500: 1.04·Re_d^0.4·Pr^0.36; 500 ≤ Re_d < 1000: 0.71·Re_d^0.5·Pr^0.36; Re_d ≥ 1000: 0.35·(S_T/S_L)^0.2·Re_d^0.6·Pr^0.36.
- (PN8) h = Nu_d·k_a/d (same h on the exposed base); m = sqrt(4h/(k·d)); η_f = tanh(mH)/(mH).
- (PN9) A_pin = π·d·H·N; A_base = W·L − N·π·d²/4; G = h·(η_f·A_pin + A_base).
- (PN10) mass = ρ_s·(N·(π·d²/4)·H + W·L·t_b).
- Sweep: d ∈ {1.0, 1.5, 2.0, 3.0} mm (assumed LPBF limit d ≥ 1 mm at H/d ≤ 30); p ∈ {1.5, 1.75, 2.0, 2.5, 3.0}. Flag designs with Re_d outside 40–1000 or N_L < 10; keep them in the table but mark them.
- Primary pin result ("favourable"): Nusselt version K with whichever friction version gives the lower ΔP at the operating point. Also report the three other combinations.

**M-GYR, sheet-gyroid lattice as a homogenised porous fin.** Parametric: there is no validated correlation in this spec. Design variables: cell size a, relative density ρ̄. Model parameters: friction multiplier c_f, analogy factor χ = j/f_F.

- (GY1) s_G = 3.0915 (area of the gyroid minimal surface in a unit cube; UNSURE fourth digit). Wall thickness t_s = ρ̄·a/s_G; require t_s ≥ 0.3 mm (assumed). a_sf = 2·s_G/a; φ = 1 − ρ̄.
- (GY2) D_h = 4·φ/a_sf; A_wet = a_sf·W·L·H; A_flow = φ·W·H; u = V̇/A_flow; Re_h = ρ·u·D_h/μ.
- (GY3) f_D = c_f·(133.33/Re_h + 2.333) (Darcy; the Ergun 1952 equation rewritten with D_h and interstitial velocity, see note below); ΔP = f_D·(L/D_h)·ρ·u²/2.
- (GY4) h = χ·(f_D/4)·ρ·u·c_p·Pr^(−2/3).
- (GY5) k_eff = k_s·2·ρ̄/(3 − ρ̄) (Hashin–Shtrikman upper bound; favourable to the lattice).
- (GY6) m = sqrt(h·a_sf/k_eff); η_f = tanh(mH)/(mH); G = h·(η_f·A_wet + φ·W·L).
- (GY7) mass = ρ_s·(ρ̄·W·L·H + W·L·t_b).
- Sweep: a ∈ {3, 4, 5, 6, 8, 10, 12, 15} mm; ρ̄ ∈ {0.15, 0.20, 0.30}; c_f ∈ {1.0, 0.3, 0.1}; χ ∈ {0.05, 0.10, 0.20, 0.35}. Mark designs with H/a < 3 as "homogenisation doubtful".
- Note on (GY3). Ergun: ΔP/L = 150·μ·U_s·(1 − φ)²/(φ³·d_p²) + 1.75·ρ·U_s²·(1 − φ)/(φ³·d_p). With d_p = 6·(1 − φ)/a_sf = 1.5·(1 − φ)·D_h/φ and u = U_s/φ this becomes ΔP/L = 66.67·μ·u/D_h² + 1.1667·ρ·u²/D_h, i.e. f_D = 133.33/Re_h + 2.333. For reference, smooth parallel plates have f_D = 96/Re_h and χ ≈ 0.35.

**M-SP, base spreading (Lee et al. 1995; constants UNSURE).** Inputs A_s, A_p = W·L, t_b, k, R₀.

- (SP1) a_s = sqrt(A_s/π); b_p = sqrt(A_p/π); ε = a_s/b_p; τ = t_b/b_p; Bi = 1/(π·k·b_p·R₀).
- (SP2) λ = π + 1/(sqrt(π)·ε); Φ = (tanh(λτ) + λ/Bi)/(1 + (λ/Bi)·tanh(λτ)).
- (SP3) ψ_max = ε·τ/sqrt(π) + (1 − ε)·Φ/sqrt(π); ψ_avg = ε·τ/sqrt(π) + 0.5·(1 − ε)^1.5·Φ.
- (SP4) R_sp,max = ψ_max/(sqrt(π)·k·a_s); R_sp,avg = ψ_avg/(sqrt(π)·k·a_s). Both include the 1-D slab part. Source-to-inlet-air resistance = R_sp + R₀.

**M-ENT, entropy generation by mechanism.** Inputs from a solved sink design: h, m, NTU, C, A_f (finned or lattice wetted area: A_fin, A_pin or A_wet), A_b (exposed base area), T_root, T_out, R_base,1D.

- (EN1) T_air(x) = T_in + (T_root − T_in)·(1 − exp(−NTU·x/L)), x ∈ [0, L].
- (EN2) T_w(x, z) = T_air(x) + (T_root − T_air(x))·cosh(m·(H − z))/cosh(m·H), z ∈ [0, H]; on the base T_w = T_root.
- (EN3) q″(x, z) = h·(T_w − T_air). Area elements: dA_f = (A_f/(L·H))·dx·dz; dA_b = (A_b/L)·dx. Midpoint rule, 400 × 400 points for the fin, 400 for the base.
- (EN4) Q_num = ∫ q″ dA_f + ∫ q″ dA_b.
- (EN5) Ṡ_film = ∫ q″·(1/T_air − 1/T_w) dA over fin and base.
- (EN6) Ṡ_fin = ∫ q″·(1/T_w − 1/T_root) dA_f.
- (EN7) T_hot = T_root + Q·R_base,1D; Ṡ_base = Q·(1/T_root − 1/T_hot).
- (EN8) Ṡ_mix = C·[(T_out − T₀)/T₀ − ln(T_out/T₀)].
- (EN9) Ṡ_pump = P_air/T₀; Ṡ_fanloss = P_air·(1/η_fan − 1)/T₀.
- (EN10) Ṡ_th = Q·(1/T₀ − 1/T_hot); Ṡ_dev = Q/T_hot.
- (EN11) Prompt's expression for three readings of T_coolant: E(T_c) = Q·(1/T_c − 1/T_hot) + P_air/T₀ with T_c = T₀, T_c = (T_in + T_out)/2, T_c = T_lm = (T_out − T_in)/ln(T_out/T_in).

**M-EC, activation kinetics.** b(α, T) = R·T/(α·F); b10 = ln(10)·b. η(J, R_f, j₀, α) = b·asinh(J/(2·R_f·j₀)). Required roughness: R_c = J/(2·j₀c·sinh(η_ref/b_c)). Units: J and j₀ in A/cm².

**M-PE, porous electrode.** δ = J·L/(κ_eff·b); θ from 2·θ·tan θ = δ by bisection on (0, π/2), tolerance 1e-12; E = sin(2θ)/(2θ); L_eff = E·L; Δη_ion = b·ln(1/E); κ_eff = κ·(ε·(1 − ε_g))^1.5; η_min = b·acosh(1 + J²/(4·κ_eff·a_v·j₀·b)) with J, j₀ in A/m², a_v in m²/m³, κ in S/m.

### 3.2 Spec table

Checks are meant to be independent of the quantity they check: a limiting case with a known exact answer, a second method, or an outside range. Where the only available check is an identity, the row says so and it does not count as a check. "Hand range" means my estimate; a miss is a finding.

| Row | Quantity | Method or formula | Inputs with units | Sanity check or expected range | Tolerance | Supports claim |
|---|---|---|---|---|---|---|
| B01 | Fin efficiency of a plate fin against k, at fixed h | η_f = tanh(mH)/(mH), m = sqrt(2h/(k·t)). Table over k and h | H = 0.030 m; t = 0.4 mm; h ∈ {40, 75, 150} W/m²/K (assumed span); k ∈ {390, 200, 180, 150, 120, 100} W/m/K | Second method: solve θ″ = m²θ, θ(0) = 1, θ′(H) = 0 by central finite differences on 400 nodes, q_root = −k·t·θ′(0) per unit length (second-order one-sided difference), η_FD = q_root/(2·h·H); compare. Limits: k = 1e6 gives η within 1e-3 of 1; k = 1 gives η within 1 % of 1/(mH). Hand range at h = 75: 0.79 (Cu), 0.66, 0.64, 0.60, 0.56, 0.52 (k = 200, 180, 150, 120, 100), each ± 0.03 | abs(η − η_FD) ≤ 0.005 | B2.2, B2.3 |
| B02 | Al fin thickness that gives the Cu fin's η at equal h, and the open-area ratio lost | t_Al = t_Cu·k_Cu/k_Al; σ_Cu = 1 − N_f·t_Cu/W; σ_Al = 1 − N_f·t_Al/W | t_Cu = 0.4 mm; N_f = 32; k_Al set; W | Check by substituting t_Al into B01's function: η equal to the Cu value within 1e-9 (identity, not counted). Hand range: t_Al 0.78–1.56 mm; σ_Al 0.17–0.58 against σ_Cu 0.79 | exact | B2.2 |
| B03 | Cu plate-fin reference design at P_air = 0.1 W: V̇, u, Re, ΔP, Nu, h, η_f, NTU, ΔT_air, R_fa, 1/C, mass | M-PF (PF1–PF11), X1, bisection on V̇ | t = 0.4 mm; N_f = 32 (s = 1.523 mm); k = 390; P_air = 0.1 W | (i) Second method PF12: R_fa,T/R_fa within 0.85–1.15. (ii) Exact limit for the pressure-drop function: call it with H = 1000 m, L = 10 m, s = 1.5 mm, u = 1 m/s, K_c = K_e = 0; ΔP must equal 12·μ·u·L/s² within 1.5 %. (iii) Nu function with L = 100 m returns 7.55 ± 0.02 (exact fully developed value 7.541). (iv) Re < 2300. Hand range: V̇ 3.5–5.0e-3 m³/s; ΔP 18–32 Pa; h 60–90 W/m²/K; η_f 0.75–0.83; NTU 1.1–1.7; ΔT_air 17–25 K; R_fa 0.24–0.31 K/W | bisection 1e-8 rel.; checks as stated | B2.10, B2.3 |
| B04 | Material swap at fixed geometry: R_fa(k)/R_fa(Cu), η_f(k), share of 1/C in R_fa | M-PF as B03, geometry fixed, k varied | t = 0.4 mm; N_f = 32; k ∈ {390, 200, 180, 150, 120, 100}; P_air ∈ full set | V̇ and ΔP must be identical for all k at a given P_air (hydraulics do not depend on k; this checks the code path). Hand range at 0.1 W: ratio 1.08–1.14 (k = 180), 1.11–1.18 (150), 1.17–1.30 (100); 1/C is 0.6–0.8 of R_fa for Cu | – | B2.3 |
| B05 | Optimised plate fin for each material and each P_air: best (t, N_f, s), R_fa, V̇, ΔP, η_f, NTU, ΔT_air, mass; and ratio to the Cu optimum | M-PF, exhaustive search over the sweep sets, minimise R_fa, exclude Re ≥ 2300 | sweep sets of M-PF; k ∈ {390, 200, 180, 150, 120, 100}; P_air set | (i) Independent optimum: s_BS = 2.7·L·Be^(−1/4), Be = ΔP·L²/(μ·α_a) at the optimum's own ΔP; expect s/s_BS within 0.6–1.6 (Bejan & Sciubba assume thin isothermal plates at fixed ΔP, so exact agreement is not expected). (ii) Report whether the optimum lies on a boundary of the sweep (t at its minimum, s at 0.8 mm); a boundary optimum is a finding. (iii) PF12 at each optimum within 0.85–1.15. Hand range at 0.1 W: Cu 0.24–0.30 K/W; Al k = 150 within 1.05–1.25 × Cu; k = 200 within 1.03–1.15 × Cu | – | B2.1, B2.4, B2.10 |
| B06 | Pin-fin correlations at reference points: f_K, f_J, Nu_K, Nu_Z | PN3, PN4, PN6, PN7 evaluated directly | p ∈ {1.5, 2.0, 2.5, 3.0}; Re_d ∈ {100, 300, 500, 1000}; S_L = S_T; Pr | Outside range (Žukauskas charts for staggered banks, from memory): pressure-loss coefficient per row 0.3–1.2 for p = 1.5–2.5 at Re_d 300–1000. Cross-method: f_K/f_J within 0.65–1.6; Nu_Z/Nu_K within 0.55–1.05. Hand values at p = 2, Re_d = 500: f_K ≈ 0.70, f_J ≈ 0.54, Nu_K ≈ 17.4, Nu_Z ≈ 14.0 (500 falls in the middle branch of PN7). Report any (p, Re_d) where f_K rises with p (suspected defect in my recollection of PN3) | – | B2.5, B3.1 |
| B07 | Optimised Al pin fins for each k and P_air: best (d, p), N, R_fa, V̇, ΔP, Re_d, η_f, NTU, mass, for the favourable combination and for the other three | M-PIN, exhaustive search, minimise R_fa | sweep of M-PIN; k ∈ {200, 180, 150, 120, 100}; also k = 390 for reference; P_air set | Compare with B05: ratio to Cu plate-fin optimum and to Al plate-fin optimum at the same k and P_air. Hand range at 0.1 W, k = 150, favourable: R_fa 0.33–0.50 K/W, i.e. 1.2–1.8 × Cu plate fin. Flag if the four correlation combinations disagree by more than a factor 1.5 in R_fa | – | B2.5, B2.7 |
| B08 | Porous-fin code path reproduces the plate-fin result | Feed M-GYR's fin and NTU steps (GY6, X1) with plate inputs from B03: a_sf = 2·N_ch/W; φ = N_ch·s/W; k_eff = k·N_f·t/W; h, V̇ taken from B03 (bypass GY3–GY5) | B03 outputs | η_f within 2 % and R_fa within 3 % of B03 (the two differ only by the end-fin count N_ch/N_f = 31/32). This checks the implementation of the homogenised fin against the discrete one | 2 %, 3 % | B2.2, B2.6 |
| B09 | Gyroid sweep: for each (c_f, χ, k_s, P_air) the best (a, ρ̄), R_fa, 1/C, V̇, ΔP, Re_h, h, η_f, NTU, t_s, mass. Then χ_min(c_f, k_s, P_air): the smallest χ for which the best gyroid R_fa equals (1) the Cu plate-fin optimum of B05, (2) the Al plate-fin optimum at the same k | M-GYR exhaustive search; χ_min by bisection on χ ∈ [0.01, 1.0] (R_fa falls monotonically with χ); if R_fa at χ = 1.0 is still above target report "caloric-limited, no match" with min(1/C) | sweep of M-GYR; k_s ∈ {100, 150, 180}; P_air set | No independent correlation exists in this spec; B08 checks the code. Outside ranges for judging the result: χ ≈ 0.35 for smooth laminar channels; 0.2–0.3 for offset-strip fins; about 0.2 for the pin bank of B06 (compute it: χ_pin = [Nu_K/(Re_d·Pr^(1/3))]/[f_K·(S_T − d)/(π·d)] at p = 2, Re_d = 300, expect 0.1–0.3; the denominator is the pin bank's equivalent f_F from D5). Hand expectation: c_f = 1.0 gives no match at any χ for P_air ≤ 0.3 W; c_f = 0.3 and 0.1 give χ_min 0.2–0.6 | bisection 1e-4 in χ | B2.6, B2.7 |
| B10 | Exponent n in R_fa ∝ P_air^n for each optimised architecture | Least-squares slope of ln R_fa against ln P_air over the five P_air values, from B05, B07 (favourable), B09 (c_f = 0.3, χ = 0.2) | outputs of B05, B07, B09 | D5 predicts n between −1/3 (caloric and low-NTU limits, constant f and j) and about −0.15 (laminar developing flow, where f falls with u). Expect −0.15 to −0.40. A positive or near-zero n is an error | – | B2.1 |
| B11 | Equal volume flow instead of equal fan power: R_fa, ΔP and P_air of each architecture's 0.1 W optimum when driven at the Cu plate-fin optimum's V̇ | Evaluate the fixed designs from B05 (Cu, Al k = 150), B07 (k = 150, favourable), B09 (k_s = 150; c_f = 0.3, χ = 0.2 and c_f = 1.0, χ = 0.1) at V̇ = V̇_Cu,opt | outputs of B05, B07, B09 | Energy balance: ΔT_air identical for all (same C). R_fa ≥ 1/C for all. Expect pin and gyroid R_fa to approach or beat plate fins here while their P_air is several times 0.1 W; report the factor | – | B2.7 |
| B12 | Equal function: P_air each Al architecture needs to reach the Cu plate-fin optimum's R_fa at 0.1 W; extra electrical power and entropy rate; extra energy over τ_life | For each architecture, bisection on ln P_air ∈ [ln 0.01, ln 30] with re-optimisation of the design at each P_air (as B05, B07, B09) until min R_fa = target. ΔW_elec = (P_req − 0.1)/η_fan; ΔṠ = ΔW_elec/T₀; ΔE = ΔW_elec·τ_life | target from B05; Al plate (k = 100, 150, 180, 200), Al pin (k = 150, favourable), gyroid (k_s = 150, c_f = 0.3, χ = 0.2); η_fan; τ_life | Second estimate from B10: P_req ≈ 0.1·(R_Al/R_Cu)^(−1/n) using the architecture's own n and its R ratio at 0.1 W; agree within a factor 1.5. If no P_air ≤ 30 W reaches the target report "not reachable". Hand range for Al plate, k = 150: P_req 0.15–0.35 W, ΔW_elec 0.2–1.0 W, ΔE 30–160 MJ | bisection 1e-3 rel. | B1.6, B2.4, B2.11 |
| B13 | Same fan instead of same fan power: operating point and R_fa of each 0.1 W optimum on the assumed fan curve | Solve ΔP_sink(V̇) = 60·(1 − V̇/0.012) by bisection on V̇ ∈ (0, 0.012); then R_fa, P_air = V̇·ΔP | designs as in B11; fan curve of §3.0 | P_air at the operating point cannot exceed the fan's maximum air power ΔP_max·V̇_max/4 = 0.18 W (property of a linear fan curve, independent of the sink model). Expect the ranking of B05/B07/B09 to hold | bisection 1e-8 rel. | B2.7 |
| B14 | Base spreading resistance for the concentrated source, Cu and Al bases: R_sp,max, R_sp,avg, and the Al-minus-Cu penalty | M-SP | A_s = 4.0e-4 m²; A_p = 3.6e-3 m²; t_b = 0.005 m; also t_b = 0.010 m; k ∈ {390, 200, 180, 150, 120, 100}; R₀ = the material's own plate-fin optimum R_fa at 0.1 W from B05 | Exact limits: (i) A_s = A_p gives t_b/(k·A_p) within 1e-9. (ii) ε = 1e-4, τ = 5: R_sp,max·π·k·a_s = 1 within 0.5 %; R_sp,avg·k·a_s = 0.2702 (= 8/(3π²)) within 6 % (the model is a fit and is known to me as about 4 % high). Hand range: Cu 0.06–0.10 K/W; k = 150: 0.16–0.24 K/W; penalty 0.08–0.16 K/W | limits as stated | B2.8, B1.5 |
| B15 | Resistance budget, source to inlet air, uniform and concentrated source: base, fin side, total, with an interface term for scale | Case U: R_base,1D + R_fa. Case S: R_sp,max + R_fa. R_TIM = t_TIM/(k_TIM·A_contact) reported beside them (equal for all candidates) | designs: Cu plate, Al plate (k = 150), Al pin (k = 150, favourable), gyroid (k_s = 150; c_f = 0.3, χ = 0.2), all at 0.1 W; t_TIM = 50 µm, k_TIM = 3 W/m/K (assumed); A_contact = W·L (case U) or A_s (case S) | T_max − T_in = Q·R_total must be below 100 K for a design to count as functional (assumed device limit: 125 °C junction is not modelled; this is a plausibility bound only). Hand: R_TIM 0.005 K/W (U), 0.042 K/W (S) | – | B2.8, B1.7 |
| B16 | Entropy generation by mechanism for four designs: Ṡ_base, Ṡ_fin, Ṡ_film, Ṡ_mix, Ṡ_pump, Ṡ_fanloss, Ṡ_th, Ṡ_dev; shares; the three readings of the prompt's expression | M-ENT (EN1–EN11) | the four designs of B15, case U, P_air = 0.1 W; η_fan | (i) Energy closure: Q_num = Q within 0.2 % (quadrature against the ε-NTU closed form). (ii) Entropy closure: Ṡ_film + Ṡ_fin = C·ln(T_out/T_in) − Q/T_root within 0.5 % (quadrature against the stream balance). (iii) Series limit for mixing: Ṡ_mix within 10 % of Q·ΔT_air/(2·T₀²) when ΔT_air < 30 K. (iv) Ṡ_base + Ṡ_fin + Ṡ_film + Ṡ_mix = Ṡ_th follows algebraically from (ii) and Q = C·ΔT_air; print it but do not count it as a check. Likewise Ṡ_dev + Ṡ_th = Q/T₀ is an identity. Hand range for the Cu design: Ṡ_th 0.026–0.031 W/K; Ṡ_mix share 0.25–0.45; Ṡ_pump 3.4e-4 W/K (about 1 % of Ṡ_th); with fan losses 1.3e-3 W/K (about 5 %); E(T_lm) below E(T₀) by the mixing share | 0.2 %, 0.5 %, 10 % | B1.1, B1.2, B1.6, B1.8 |
| B17 | T_hot candidates for the concentrated source: source-mean temperature, maximum, bound on the harmonic–arithmetic gap, and the entropy-term error from using T_max | T_avg = T_in + Q·(R_fa + R_sp,avg); T_max = T_in + Q·(R_fa + R_sp,max); gap bound = (T_max − T_avg)²/T_avg (range over the source taken as 2·(T_max − T_avg), assumed); error = Q·(1/T_avg − 1/T_max) and its ratio to Q·(1/T₀ − 1/T_avg) | B14 outputs for Cu and Al (k = 150) with their plate-fin optimum R_fa | Hand range: T_max − T_avg 1–7 K; gap bound below 0.15 K; relative error of the entropy term 3–12 % | – | B1.5 |
| B18 | Pumping term: ideal-gas form against the incompressible form; local against dead-state temperature; air power against electrical | (a) ṁ·R_air·ln(p_in/p_out) with ṁ = ρ·V̇, p_out = p₀, p_in = p₀ + ΔP, against V̇·ΔP/T_ρ where T_ρ = p₀/(ρ·R_air) (the temperature consistent with the density used). (b) V̇·ΔP/T₀ against V̇·ΔP/T_lm. (c) V̇·ΔP/(η_fan·T₀) for η_fan ∈ {0.1, 0.25, 0.4} | Cu plate-fin optimum at 0.1 W from B05 | (a) relative difference equals ΔP/(2·p₀) within 10 % of that small number (second-order term of the logarithm; an independent prediction). (b) difference below 10 %. Note: T_ρ will be about 304 K, not 300 K, because the tabulated density and R_air are not exactly consistent; report it | – | B1.3, B1.4, B1.8 |
| B19 | Radiation from the envelope, for scale | Q_rad = ε_r·σ_SB·A_ext·(T_root⁴ − T₀⁴); A_ext = W·L + 2·L·H; σ_SB = 5.670e-8 W/m²/K⁴ | ε_r ∈ {0.05 (bare Cu, assumed), 0.8 (anodised Al, assumed)}; T_root from B05 for Cu and Al (k = 150) | Second method: linearised 4·ε_r·σ_SB·T_m³·A_ext·(T_root − T₀), T_m the mean of the two temperatures, within 2 %. Hand range: below 0.2 W (Cu), 0.8–1.8 W (Al) | 2 % | B1.8 |
| B20 | Mass and primary-metal embodied energy of each optimum; ratio of Al to Cu cumulative energy demand per volume; comparison with ΔE of B12 | mass from PF11, PN10, GY7; E_emb = mass·e; ratio = (e_Al·ρ_Al)/(e_Cu·ρ_Cu); E_LPBF = mass·e_LPBF for AM parts | masses of the B15 designs; e_Cu ∈ {30, 54, 70} MJ/kg; e_Al ∈ {131, 200} MJ/kg; e_LPBF ∈ {100, 400} MJ/kg of part (all UNSURE, from memory of Nuss & Eckelman 2014, Ashby 2012, Faludi et al. 2017, Kellens et al. 2017) | No independent check available; report only. Hand range: Cu sink 0.30–0.45 kg, Al plate sink 0.10–0.20 kg; per-volume CED ratio Al/Cu 0.5–2; E_emb of each sink 10–40 MJ | – | B2.11 |
| C01 | Natural and decadic Tafel slopes | b = R·T/(α·F); b10 = ln(10)·b | T ∈ {298.15, 353.15} K; α ∈ {0.5, 1.0, 1.5, 2.0} | Outside constant: b10 at 298.15 K, α = 1 is 59.16 mV (textbook value) within 0.02 mV. Hand: b = 51.39 mV at α = 0.5, 298.15 K | 1e-6 rel. | C3.1 |
| C02 | Activation overpotential of the Pt reference at J = 1 A/cm², four scenarios | M-EC: η = b·asinh(J/(2·R_f·j₀)) | α = 0.5; T = 298.15 K. P1 (hydrogen evolution, acid): j₀ = 0.2 A/cm²_Pt (range 0.1–1; UNSURE). P2 (hydrogen evolution, alkaline): j₀ = 6.0e-4 A/cm²_Pt (UNSURE). R_f,Pt ∈ {1, 100, 200} | Limits computed separately: Tafel form b·ln(J/(R_f·j₀)) within 1 % when J/(2·R_f·j₀) > 10; linear form b·J/(2·R_f·j₀) within 1 % when that ratio < 0.1. Hand: P2 flat 0.381 V; P2 with R_f = 100: 0.145 V; P1 flat 0.085 V; P1 with R_f = 100: 1.28 mV | 1 % on limits | C2.3, C2.4 |
| C03 | Roughness factor the candidate needs to match each Pt scenario, equal α | M-EC: R_c = J/(2·j₀c·sinh(η_ref/b)) with η_ref from C02 | j₀c ∈ {1e-7, 1e-6, 1e-5, 1e-4, 1e-3} A/cm²_real; Pt scenarios of C02; J ∈ {0.1, 1.0, 2.0} A/cm² | Closed form from D7: R_c = R_f,Pt·j₀Pt/j₀c; agree within 1e-6 relative, and identical for the three J values (the code uses asinh and sinh, the check uses neither). Hand: P2 flat with j₀c = 1e-5: 60; P2 with R_f = 100, j₀c = 1e-6: 6.0e4; P1 with R_f = 100, j₀c = 1e-5: 2.0e6 | 1e-6 rel. | C2.1, C2.3 |
| C04 | Same with unequal Tafel slopes, and the overpotential gained per decade of roughness | R_c = J/(2·j₀c·sinh(η_ref/b_c)); Δη per decade = η(R_c) − η(10·R_c) evaluated numerically with M-EC | α_c ∈ {0.5, 1.0, 1.5}; α_Pt = 0.5; j₀c ∈ {1e-6, 1e-5}; Pt scenarios P2 with R_f ∈ {1, 100}; J = 1 A/cm² | Reduces to C03 at α_c = 0.5 (1e-6). Second method in the Tafel regime: R_c ≈ (J/j₀c)·exp(−η_ref/b_c), within 2 % when η_ref/b_c > 3. Δη per decade equals b10(α_c) within 2 % when J/(2·R_c·j₀c) > 10 | 2 % | C3.1 |
| C05 | Oxygen evolution at 1 A/cm² by Tafel extrapolation: NiFe, Ir oxide, Pt | η(J) = η_ref + b10·log10(J/J_ref) for NiFe and Ir oxide; η = b10·log10(J/j₀) for flat Pt | NiFe (alkaline): η_ref ∈ {0.25, 0.30, 0.35} V at J_ref = 0.010 A/cm² geometric, b10 ∈ {0.030, 0.040, 0.060} V. Ir oxide (acid): η_ref = 0.30 V at 0.010 A/cm², b10 = 0.050 V. Pt: j₀ ∈ {1e-10, 1e-9, 1e-8} A/cm², b10 = 0.120 V. All UNSURE (typical values from memory of McCrory et al. 2013, 2015; Damjanovic et al. 1966) | Outside range: reported NiFe-on-foam overpotentials at 0.5–1 A/cm² are about 0.27–0.45 V before ohmic correction issues (Lu & Zhao 2015; UNSURE). Hand: NiFe 0.31–0.47 V; Ir oxide 0.40 V; Pt 0.96–1.20 V. Pure extrapolation over two decades; not a prediction | – | C1.4 |
| C06 | Ni foam: geometric roughness and electronic drop | R_f,geom = a_v·L. ΔV = J·L/(2·σ_eff) with σ_eff = σ_Ni·ρ̄/3 (Lemlich) and σ_eff = σ_Ni·ρ̄^1.7 (assumed power law). In-plane: ΔV_ip = J·w²/(8·σ_eff·L) | a_v ∈ {5e3, 1e4, 1.5e4} m²/m³ (assumed for 110 pores-per-inch foam, UNSURE); L = 1.6e-3 m; σ_Ni = 1.43e7 S/m; ρ̄ ∈ {0.03, 0.05, 0.10}; J = 1e4 A/m²; rib pitch w = 0.010 m (assumed) | Both models must give through-thickness ΔV < 1 mV for the claim. Lower bound from solid Ni: J·L/(2·σ_Ni) = 5.6e-7 V; all results must exceed it. ΔV_ip is reported separately and is not part of the claim (it depends on the assumed rib pitch; hand: 0.2–2 mV). Hand: R_f,geom 8–24; ΔV 1e-5 to 3e-4 V | – | C2.5 |
| C07 | Utilisation of a finite porous electrode: δ, θ, E, L_eff, Δη_ion | M-PE | L ∈ {0.3e-3, 1.6e-3} m; J = 1e4 A/m²; κ ∈ {20 (1 M KOH, 25 °C), 62 (30 wt% KOH, 25 °C), 140 (30 wt% KOH, 80 °C)} S/m (UNSURE, from memory of Gilliam et al. 2007); ε = 0.90; ε_g ∈ {0, 0.3}; b ∈ {0.05139 V (α = 0.5), 0.01737 V (40 mV/decade)}; use T = 298.15 K for b in all cases | Second method: integrate u″ = exp(u) (K = 1) on ξ ∈ [0, 1] with fourth-order Runge–Kutta, 2000 steps, from u′(1) = 0, shooting on u(1) by bisection in the bracket [−30, 1.596] (the solution blows up before ξ = 0 for u(1) ≥ ln(π²/2) = 1.5963; −u′(0) rises monotonically with u(1)) until −u′(0) = δ; then E_num = δ/exp(u(0)); compare for δ ∈ {0.5, 5, 50}. Limits: E within 1 % of 1 − δ/3 at δ = 0.01; within 1 % of 2/δ at δ = 100. Hand: L = 1.6 mm, κ = 62, ε_g = 0, α = 0.5: δ ≈ 5.9, E ≈ 0.29, Δη_ion ≈ 0.063 V; with b = 17.4 mV: E ≈ 0.11 | abs(E − E_num)/E ≤ 0.005 | C2.6 |
| C08 | Thickness-independent minimum overpotential of a porous candidate electrode, and whether it meets each Pt reference | M-PE: η_min = b·acosh(1 + J²/(4·κ_eff·a_v·j₀·b)); verdict "reaches" if η_min ≤ η_ref of C02. Also the equivalent effective roughness R_eff = J/(2·j₀·sinh(η_min/b)) (J, j₀ in the same units) | b = 0.05139 V; J = 1e4 A/m²; j₀ ∈ {0.01, 0.1, 1.0} A/m² (= 1e-6, 1e-5, 1e-4 A/cm²); a_v ∈ {1e4 (bare foam), 6.25e5 (foam with R_f,total = 1000 over 1.6 mm), 2e6 (1 µm pores, ε = 0.5), 2e7 (0.1 µm pores, ε = 0.5)} m²/m³; κ ∈ {62, 140} S/m; ε = 0.90 for the two foam cases and 0.50 for the two pore cases; ε_g ∈ {0, 0.3} | Second route: for the foam case with L = 0.016 m (ten times thicker, so δ is large) compute E from C07 and η_thick = b·ln(J/(a_v·j₀·L·E)); must agree with η_min within 2 % when η_min > 3·b (finite-thickness tangent solution against the semi-infinite first integral). Limits computed separately: Tafel form b·ln(J²/(2·κ_eff·a_v·j₀·b)) within 1 % when the argument exceeds 100. Hand: a_v = 2e6, j₀ = 0.1 A/m², κ = 62, ε = 0.5, ε_g = 0: η_min ≈ 0.28 V; a_v = 2e7: ≈ 0.16 V; compare η_ref 0.145 V (P2, R_f = 100) and 1.3 mV (P1, R_f = 100) | 2 %, 1 % | C2.7 |
| C09 | Diffusion-limited current for OH⁻ supply to an oxygen-evolving surface | j_lim = F·D·c/δ_N (one electron per OH⁻; no migration, so a lower bound) | D = 5.27e-9 m²/s (25 °C, dilute; standard value); c ∈ {1000, 6900} mol/m³; δ_N ∈ {10, 50, 100} µm (assumed) | Outside statement to test: 1 M with 50 µm should give about 1 A/cm² (1.0e4 A/m²). With migration in pure KOH the limit is higher by about 1/(1 − t_OH) with t_OH ≈ 0.73 (assumed); report both. Hand: 0.5–5 A/cm² (1 M), 3.5–35 A/cm² (6.9 M) without migration | – | C2.9 |
| C10 | Bubble coverage penalty | Θ = 0.023·(J/(1 A/m²))^0.3 (Vogt & Balzer 2005; constants UNSURE); Δη = b·ln(1/(1 − Θ)) | J ∈ {1e3, 1e4, 2e4} A/m²; b ∈ {0.05139, 0.01737} V | Θ must lie in (0, 1). Outside range (from memory): coverage 0.2–0.6 at 1 A/cm² on flat electrodes in stagnant electrolyte. Hand: Θ ≈ 0.36 at 1e4 A/m²; Δη ≈ 23 mV (α = 0.5), 8 mV (40 mV/decade). The formula is for flat electrodes; its use for a foam is an extrapolation | – | C2.8 |
| C11 | Ohmic losses for scale | η_Ω = J·ASR | J = 1 A/cm²; ASR ∈ {0.10, 0.15, 0.20} Ω·cm² (acid membrane, assumed range), {0.15, 0.25, 0.30} Ω·cm² (alkaline diaphragm with electrolyte gap, assumed range; UNSURE) | No check (one multiplication). The result is compared in S4 with the activation differences of C02 and C05 | – | C3.2 |
| C12 | Activation entropy rate per m² of electrode, with the prompt's T₀ and with T_cell | Σ̇″ = J·η/T₀ and J·η/T_cell | J = 1e4 A/m²; η ∈ {0.001, 0.05, 0.10, 0.145, 0.30} V; T₀ = 298.15 K; T_cell = 353.15 K | Ratio must equal T₀/T_cell = 0.844 (identity; not counted). For scale: fraction of the reversible power J·1.229 V. Hand: η = 0.1 V gives 1000 W/m², 3.35 W/K/m² | – | C3.3 |
| C13 | Break-even overpotential difference for removing Pt, energy basis | Δη_be = e_Pt·m″_Pt/(J·τ_op); payback time for a given penalty t_pb = e_Pt·m″_Pt/(J·Δη) | e_Pt ∈ {1.0e5, 2.4e5, 3.0e5} MJ/kg (UNSURE; middle value from memory of Nuss & Eckelman 2014); m″_Pt ∈ {0.5, 3.0, 5.0} g/m² (0.05, 0.3, 0.5 mg/cm²; assumed); J = 1e4 A/m²; τ_op = 1.44e8 s (40 000 h, assumed); Δη ∈ {0.01, 0.05, 0.1} V | Magnitude cross-check by a different route: hydrogen produced per m² over τ_op is J·τ_op/(2F) mol; times 241.8 kJ/mol (lower heating value) gives about 1.8e6 MJ/m²; e_Pt·m″_Pt should be about 4e-4 of it for the middle inputs. This shares the inputs J and τ_op, so it checks units and magnitude only. Hand: Δη_be ≈ 0.5 mV for the middle inputs (range 0.03–1.0 mV); payback 8 days at 0.1 V | – | C3.5 |

### 3.3 Notes for S2

- Group rows into scripts as convenient (for example one module with M-PF, M-PIN, M-GYR and the solver; one script per group of rows). Each script prints the inputs it used, the results, and PASS or FAIL for each check with the numbers behind it.
- Implement the formulas exactly as written, including those marked UNSURE. Do not correct a constant. If a formula produces nonsense (negative value, discontinuity, non-monotone trend), record it in `issues.md` with the numbers and continue.
- A check listed as "identity, not counted" is printed but not reported as a pass.
- "Hand range" misses go into `issues.md` as findings, with the computed value.
- Rows B05, B07, B09 and B12 are grid searches: print the full winning design and the next two runners-up, and say whether the winner sits on a sweep boundary.
- No row needs anything beyond numpy and the standard library. No 2-D solver is specified or wanted.

---

## 4. Citations

Columns: what it is cited for; whether I believe the paper or data is open; how sure I am that the reference exists as written. "sure" still needs S3. Nothing here was looked up. S3: for the entries in group B3, please also record the correlation form, the length scale and velocity used in Re, Nu and f, the fluid, and the Re range, if visible in open text.

### Entropy generation and heat-sink models

| ID | Author, year, title, venue | Cited for | Open? | Exists? |
|---|---|---|---|---|
| R01 | Bejan, A. (1996). Entropy Generation Minimization. CRC Press | Two-term entropy generation for convective surfaces; Gouy–Stodola | book, not open | sure |
| R02 | Bejan, A. (1982). Entropy Generation Through Heat and Fluid Flow. Wiley | Same; fin and duct entropy generation | book, not open | sure |
| R03 | Culham, J.R., Muzychka, Y.S. (2001). Optimization of plate fin heat sinks using entropy generation minimization. IEEE Trans. Components and Packaging Technologies 24(2), 159–165 | Entropy-generation form for a plate-fin sink; K_c, K_e and apparent-friction model (PF5–PF7) | paywalled; author copy may be on the Waterloo group site (UNSURE) | sure |
| R04 | Khan, W.A., Culham, J.R., Yovanovich, M.M. (2005). Optimization of pin-fin heat sinks using entropy generation minimization. IEEE Trans. Components and Packaging Technologies 28(2), 247–254 | PN3 and PN6 (constants UNSURE) | as R03 | sure; year and constants UNSURE |
| R05 | Teertstra, P., Yovanovich, M.M., Culham, J.R. (2000). Analytical forced convection modeling of plate fin heat sinks. J. Electronics Manufacturing 10(4), 253–261 | PF12 (alternative plate-fin model), validated against air data | as R03 | sure |
| R06 | Shah, R.K., London, A.L. (1978). Laminar Flow Forced Convection in Ducts. Academic Press | PF4 polynomial; developing-flow Nu tables | book | sure |
| R07 | Shah, R.K. (1978). A correlation for laminar hydrodynamic entry length solutions for circular and noncircular ducts. J. Fluids Engineering 100(2), 177–179 | The 3.44/sqrt(L⁺) term in PF5 | paywalled | fairly sure |
| R08 | Muzychka, Y.S., Yovanovich, M.M. (2009). Pressure drop in laminar developing flow in noncircular ducts: a scaling and modeling approach. J. Fluids Engineering 131(11), 111105 | Root-sum-square blending in PF5 | paywalled | fairly sure |
| R09 | Stephan, K. (1959). Wärmeübergang und Druckabfall bei nicht ausgebildeter Laminarströmung in Rohren und in ebenen Spalten. Chemie Ingenieur Technik 31(12), 773–778 | PF8 | paywalled | fairly sure; constants UNSURE |
| R10 | Shah, R.K., Bhatti, M.S. (1987). Laminar convective heat transfer in ducts. In Kakaç, Shah, Aung (eds), Handbook of Single-Phase Convective Heat Transfer, Wiley, ch. 3 | Secondary source for PF8 | book | sure |
| R11 | Kays, W.M., London, A.L. (1984). Compact Heat Exchangers, 3rd ed. McGraw-Hill | K_c, K_e; j and f data for plate-fin, strip-fin and pin surfaces (tabulated in the book) | book; data tabulated but not open | sure |
| R12 | Bejan, A., Sciubba, E. (1992). The optimal spacing of parallel plates cooled by forced convection. Int. J. Heat and Mass Transfer 35(12), 3259–3264 | s_opt ≈ 2.7·L·Be^(−1/4) (check in B05) | paywalled | sure |
| R13 | Webb, R.L. (1981). Performance evaluation criteria for use of enhanced heat transfer surfaces in heat exchanger design. Int. J. Heat and Mass Transfer 24(4), 715–726 | Ranking surfaces at fixed pumping power (D5) | paywalled | sure |
| R14 | Žukauskas, A. (1972). Heat transfer from tubes in crossflow. Advances in Heat Transfer 8, 93–160 | PN7; pressure-loss charts used as the outside range in B06 | paywalled; data as charts | sure |
| R15 | Jakob, M. (1938). Heat transfer and flow resistance in cross flow of gases over tube banks. Trans. ASME 60, 384–386 | PN4 | not open | fairly sure; constants via Holman UNSURE |
| R16 | Holman, J.P. (2010). Heat Transfer, 10th ed. McGraw-Hill | Secondary source for PN4 | book | sure |
| R17 | Çengel, Y.A., Ghajar, A.J. (2015). Heat and Mass Transfer: Fundamentals and Applications, 5th ed. McGraw-Hill | Secondary source for PN7 | book | sure |
| R18 | Incropera, F.P., DeWitt, D.P., Bergman, T.L., Lavine, A.S. (2007). Fundamentals of Heat and Mass Transfer, 6th ed. Wiley | Air properties (Table A.4); fin efficiency; ε-NTU | book | sure |
| R19 | Lee, S., Song, S., Au, V., Moran, K.P. (1995). Constriction/spreading resistance model for electronics packaging. Proc. 4th ASME/JSME Thermal Engineering Joint Conference, vol. 4, 199–206 | M-SP | conference paper; copies circulate (UNSURE) | sure; constants UNSURE |
| R20 | Jonsson, H., Moshfegh, B. (2001). Modeling of the thermal and hydraulic performance of plate fin, strip fin, and pin fin heat sinks: influence of flow bypass. IEEE Trans. Components and Packaging Technologies 24(2), 142–149 | Empirical correlations from wind-tunnel data for the three fin types (B3 anchor) | paywalled; data in figures and fitted constants | fairly sure |
| R21 | Kim, S.J., Kim, D.-K., Oh, H.H. (2008). Comparison of fluid flow and thermal characteristics of plate-fin and pin-fin heat sinks subject to a parallel flow. Heat Transfer Engineering 29(2), 169–177 | Plate against pin at fixed pumping power, ducted flow (direct test of B2.5) | paywalled | UNSURE (title and year) |
| R22 | Kim, D.-K., Kim, S.J., Bae, J.-K. (2009). Comparison of thermal performances of plate-fin and pin-fin heat sinks subject to an impinging flow. Int. J. Heat and Mass Transfer 52(15–16), 3510–3517 | Regime where pins can win (B2.7) | paywalled | fairly sure |
| R23 | Sparrow, E.M., Ramsey, J.W., Altemani, C.A.C. (1980). Experiments on in-line pin fin arrays and performance comparisons with staggered arrays. J. Heat Transfer 102(1), 44–50 | Pin-array air data | paywalled; figures | fairly sure |
| R24 | Ergun, S. (1952). Fluid flow through packed columns. Chemical Engineering Progress 48(2), 89–94 | GY3 | not open | sure |
| R25 | Hashin, Z., Shtrikman, S. (1962). A variational approach to the theory of the effective magnetic permeability of multiphase materials. J. Applied Physics 33(10), 3125–3131 | GY5 bound | paywalled | sure |
| R26 | Schoen, A.H. (1970). Infinite periodic minimal surfaces without self-intersections. NASA Technical Note D-5541 | Gyroid surface; the area value 3.0915 may not be in this report (UNSURE) | open (NASA technical reports server) | sure |

### AlSi10Mg conductivity and AM heat sinks (B2.9, B3)

| ID | Author, year, title, venue | Cited for | Open? | Exists? |
|---|---|---|---|---|
| R27 | EOS GmbH. EOS Aluminium AlSi10Mg material data sheet (various editions) | As-built about 103 (in plane) and 119 (build direction) W/m/K; about 173 after heat treatment (values from memory, UNSURE) | open PDF from the supplier | sure that a sheet exists; values UNSURE |
| R28 | Yang, P., Deibler, L.A., Bradley, D.R., Stefan, D.K., Carroll, J.D. (2018). Microstructure evolution and thermal properties of an additively manufactured, solution treatable AlSi10Mg part. J. Materials Research 33(23), 4040–4052 | Conductivity against heat treatment | paywalled; possibly an open report version (UNSURE) | fairly sure |
| R29 | Sélo, R.R.J., Catchpole-Smith, S., Maskery, I., Ashcroft, I., Tuck, C. (2020). On the thermal conductivity of AlSi10Mg and lattice structures made by laser powder bed fusion. Additive Manufacturing 34, 101214 | Bulk and lattice conductivity | UNSURE (may be open access) | fairly sure |
| R30 | Catchpole-Smith, S., Sélo, R.R.J., Davis, A.W., Ashcroft, I.A., Tuck, C.J., Clare, A. (2019). Thermal conductivity of TPMS lattice structures manufactured via laser powder bed fusion. Additive Manufacturing 30, 100846 | Measured k_eff of gyroid, diamond and primitive lattices against volume fraction (B3.4) | believed open access; data in figures and tables | fairly sure |
| R31 | Wong, M., Owen, I., Sutcliffe, C.J., Puri, A. (2009). Convective heat transfer and pressure losses across novel heat sinks fabricated by Selective Laser Melting. Int. J. Heat and Mass Transfer 52(1–2), 281–288 | Air-side measurements on SLM aluminium pin, fin and lattice heat sinks (B3.2) | paywalled; data in figures | sure |
| R32 | Wong, M., Tsopanos, S., Sutcliffe, C.J., Owen, I. (2007). Selective laser melting of heat transfer devices. Rapid Prototyping Journal 13(5), 291–297 | Earlier data from the same group | paywalled | fairly sure |
| R33 | Ho, J.Y., Leong, K.C., Wong, T.N. (2020). Additively-manufactured metallic porous lattice heat exchangers for air-side heat transfer enhancement. Int. J. Heat and Mass Transfer 150, 119262 | AlSi10Mg lattice, air side, Nu and pressure drop | paywalled; figures | fairly sure |
| R34 | Ho, J.Y., Wong, K.K., Leong, K.C., Wong, T.N. (2017). Convective heat transfer performance of airfoil heat sinks fabricated by selective laser melting. Int. J. Thermal Sciences 114, 213–228 | SLM AlSi10Mg fin heat sinks in air | paywalled | UNSURE |
| R35 | Calmidi, V.V., Mahajan, R.L. (2000). Forced convection in high porosity metal foams. J. Heat Transfer 122(3), 557–565 | Aluminium-foam Nu correlation in air (B3.5) | paywalled | sure |
| R36 | Bhattacharya, A., Calmidi, V.V., Mahajan, R.L. (2002). Thermophysical properties of high porosity metal foams. Int. J. Heat and Mass Transfer 45(5), 1017–1031 | Foam permeability, inertia coefficient, k_eff | paywalled | sure |
| R37 | Boomsma, K., Poulikakos, D., Zwick, F. (2003). Metal foams as compact high performance heat exchangers. Mechanics of Materials 35(12), 1161–1176 | Foam thermal resistance against pumping power | paywalled | sure |

### TPMS and gyroid Nu and friction correlations (B3.3)

| ID | Author, year, title, venue | Cited for | Open? | Exists? |
|---|---|---|---|---|
| R38 | Femmer, T., Kuehne, A.J.C., Wessling, M. (2015). Estimation of the structure dependent performance of 3-D rapid prototyped membranes. Chemical Engineering J. 273, 438–445 | Early TPMS heat and mass exchanger comparison with Nu against pressure drop | paywalled | fairly sure |
| R39 | Attarzadeh, R., Rovira, M., Duwig, C. (2021). Design analysis of the "Schwartz D" based heat exchanger: a numerical study. Int. J. Heat and Mass Transfer 177, 121415 | CFD Nu and f for a TPMS exchanger | believed open access | fairly sure |
| R40 | Cheng, Z., Xu, R., Jiang, P.-X. (2021). Morphology, flow and heat transfer in triply periodic minimal surface based porous structures. Int. J. Heat and Mass Transfer 170, 120902 | Friction and Nu against Re for several TPMS types | paywalled; figures | fairly sure |
| R41 | Iyer, J., Moore, T., Nguyen, D., Roy, P., Stolaroff, J. (2022). Heat transfer and pressure drop characteristics of heat exchangers based on triply periodic minimal and periodic nodal surfaces. Applied Thermal Engineering 209, 118192 | Nu and f correlations for gyroid, Schwarz-D and others (CFD) | UNSURE | fairly sure |
| R42 | Reynolds, B.W., Fee, C.J., Morison, K.R., Holland, D.J. (2023). Characterisation of heat transfer within 3D printed TPMS heat exchangers. Int. J. Heat and Mass Transfer 212, 124264 | Experimental Nu and f correlations for printed TPMS exchangers | UNSURE | fairly sure |
| R43 | Dixit, T., Al-Hajri, E., Paul, M.C., Nithiarasu, P., Kumar, S. (2022). High performance, microarchitected, compact heat exchanger enabled by 3D printing. Applied Thermal Engineering 210, 118339 | Gyroid exchanger measurements | UNSURE (may be open access) | fairly sure |
| R44 | Kaur, I., Singh, P. (2021). Flow and thermal transport characteristics of Triply-Periodic Minimal Surface (TPMS)-based gyroid and Schwarz-P cellular materials. Numerical Heat Transfer, Part A 79(8), 553–569 | Gyroid f and Nu in air (CFD) | paywalled | UNSURE |
| R45 | Kaur, I., Singh, P. (2021). State-of-the-art in heat exchanger additive manufacturing. Int. J. Heat and Mass Transfer 178, 121600 | Review; pointers to datasets | paywalled | fairly sure |
| R46 | Al-Ketan, O., Ali, M., Khalil, M., Rowshan, R., Khan, K.A., Abu Al-Rub, R.K. (2021). Forced convection computational fluid dynamics analysis of architected and three-dimensional printable heat sinks based on triply periodic minimal surfaces. J. Thermal Science and Engineering Applications 13(2), 021010 | TPMS heat sinks in air, CFD, thermal resistance against pressure drop | paywalled | fairly sure |
| R47 | Khalil, M., Ali, M.I.H., Khan, K.A., Abu Al-Rub, R. (2022). Forced convection heat transfer in heat sinks with topologies based on triply periodic minimal surfaces. Case Studies in Thermal Engineering 38, 102313 | TPMS heat sinks in forced air, experiment and CFD | journal is open access; data in figures | UNSURE (volume and article number) |
| R48 | Baobaid, N., Ali, M.I., Khan, K.A., Abu Al-Rub, R.K. (2022). Fluid flow and heat transfer of porous TPMS architected heat sinks in free convection environment. Case Studies in Thermal Engineering 33, 101944 | TPMS sinks in natural convection (regime of B2.7) | journal is open access | UNSURE (volume and article number) |
| R49 | Li, W., Yu, G., Yu, Z. (2020). Bioinspired heat exchangers based on triply periodic minimal surfaces for supercritical CO₂ cycles. Applied Thermal Engineering 179, 115686 | Gyroid and Schwarz-D Nu and f against printed-circuit exchangers | paywalled | fairly sure |
| R50 | Kim, J., Yoo, D.-J. (2020). 3D printed compact heat exchangers with mathematically defined core structures. J. Computational Design and Engineering 7(4), 527–550 | TPMS core Nu and f | journal is open access | UNSURE |
| R51 | Tang, W., and co-authors (2023). Analysis on the convective heat transfer process and performance evaluation of Triply Periodic Minimal Surface (TPMS) based on Diamond, Gyroid and Iwp. Int. J. Heat and Mass Transfer 201, 123642 | TPMS sink performance evaluation | paywalled | UNSURE (authors, volume) |
| R52 | No public repository of thermal-resistance-against-pressure-drop data for AM lattice or TPMS heat sinks is known to me | B3.2 | – | UNSURE; S3 to search |

### Electrocatalysis

| ID | Author, year, title, venue | Cited for | Open? | Exists? |
|---|---|---|---|---|
| R53 | Bard, A.J., Faulkner, L.R. (2001). Electrochemical Methods: Fundamentals and Applications, 2nd ed. Wiley, ch. 3 | Butler–Volmer, Tafel and linear limits (D7) | book | sure |
| R54 | Sheng, W., Gasteiger, H.A., Shao-Horn, Y. (2010). Hydrogen oxidation and evolution reaction kinetics on platinum: acid vs alkaline electrolytes. J. Electrochemical Society 157(11), B1529–B1536 | Pt j₀ in 0.1 M KOH about 0.6–0.7 mA/cm²_Pt at 294 K; acid about two orders higher | UNSURE | sure; values UNSURE |
| R55 | Durst, J., Simon, C., Hasché, F., Gasteiger, H.A. (2015). Hydrogen oxidation and evolution reaction kinetics on carbon supported Pt, Ir, Rh, and Pd electrocatalysts in acidic media. J. Electrochemical Society 162(1), F190–F203 | Pt/C j₀ in acid of order 0.1–1 A/cm²_Pt | believed open access | sure; values UNSURE |
| R56 | Durst, J., Siebel, A., Simon, C., Hasché, F., Herranz, J., Gasteiger, H.A. (2014). New insights into the electrochemical hydrogen oxidation and evolution reaction mechanism. Energy & Environmental Science 7, 2255–2260 | pH dependence of hydrogen kinetics on Pt, Ir, Pd | UNSURE | sure |
| R57 | Sheng, W., Myint, M., Chen, J.G., Yan, Y. (2013). Correlating the hydrogen evolution reaction activity in alkaline solutions with the hydrogen binding energy on monometallic surfaces. Energy & Environmental Science 6, 1509–1512 | j₀ of Ni and other metals in alkali (10⁻⁶–10⁻⁵ A/cm² range for Ni; UNSURE) | paywalled | sure |
| R58 | Bernt, M., Siebel, A., Gasteiger, H.A. (2018). Analysis of voltage losses in PEM water electrolyzers with low platinum group metal loadings. J. Electrochemical Society 165(5), F305–F314 | Cathode (Pt) overpotential of a few mV at A/cm² current densities; voltage-loss breakdown (C2.4, C3.2) | believed open access | sure |
| R59 | McCrory, C.C.L., Jung, S., Peters, J.C., Jaramillo, T.F. (2013). Benchmarking heterogeneous electrocatalysts for the oxygen evolution reaction. J. American Chemical Society 135(45), 16977–16987 | Overpotential at 10 mA/cm² and roughness factors, NiFeOx and IrOx; tables in the paper and its supporting information | paywalled; supporting information free | sure |
| R60 | McCrory, C.C.L., Jung, S., Ferrer, I.M., Chatman, S.M., Peters, J.C., Jaramillo, T.F. (2015). Benchmarking hydrogen evolving reaction and oxygen evolving reaction electrocatalysts for solar water splitting devices. J. American Chemical Society 137(13), 4347–4357 | Same, with hydrogen-evolution catalysts (Pt, NiMo) and roughness factors | paywalled; supporting information free | sure |
| R61 | Trotochaud, L., Young, S.L., Ranney, J.K., Boettcher, S.W. (2014). Nickel–iron oxyhydroxide oxygen-evolution electrocatalysts: the role of intentional and incidental iron incorporation. J. American Chemical Society 136(18), 6744–6753 | Fe dependence of NiFe activity; conductivity of the hydroxide (C2.10) | paywalled | sure |
| R62 | Gong, M., Li, Y., Wang, H., Liang, Y., Wu, J.Z., Zhou, J., Wang, J., Regier, T., Wei, F., Dai, H. (2013). An advanced Ni–Fe layered double hydroxide electrocatalyst for water oxidation. J. American Chemical Society 135(23), 8452–8455 | NiFe layered double hydroxide for alkaline oxygen evolution (C1.1) | paywalled | sure |
| R63 | Dionigi, F., Strasser, P. (2016). NiFe-based (oxy)hydroxide catalysts for oxygen evolution reaction in non-acidic electrolytes. Advanced Energy Materials 6(23), 1600621 | Review: reaction, electrolyte, Tafel slopes, stability (C1.1, C1.2, C3.1) | UNSURE | sure |
| R64 | Lu, X., Zhao, C. (2015). Electrodeposition of hierarchically structured three-dimensional nickel–iron electrodes for efficient oxygen evolution at high current densities. Nature Communications 6, 6616 | NiFe on Ni foam at 0.5–1 A/cm² (range used in C05) | open access | sure |
| R65 | Luo, J., Im, J.-H., Mayer, M.T., Schreier, M., Nazeeruddin, M.K., Park, N.-G., Tilley, S.D., Fan, H.J., Grätzel, M. (2014). Water photolysis at 12.3% efficiency via perovskite photovoltaics and Earth-abundant catalysts. Science 345(6204), 1593–1596 | NiFe hydroxide on Ni foam used at both electrodes; hydrogen-evolution overpotential about 0.2 V at 10 mA/cm² (C1.3; value UNSURE) | paywalled | sure |
| R66 | Damjanovic, A., Dey, A., Bockris, J.O'M. (1966). Kinetics of oxygen evolution and dissolution on platinum electrodes. Electrochimica Acta 11(7), 791–814 | Pt oxygen-evolution j₀ and Tafel slope (C05 inputs; values UNSURE) | paywalled | sure |
| R67 | Seh, Z.W., Kibsgaard, J., Dickens, C.F., Chorkendorff, I., Nørskov, J.K., Jaramillo, T.F. (2017). Combining theory and experiment in electrocatalysis: insights into materials design. Science 355(6321), eaad4998 | Which catalyst serves which reaction (C1.1) | paywalled | sure |
| R68 | Trasatti, S., Petrii, O.A. (1991). Real surface area measurements in electrochemistry. Pure and Applied Chemistry 63(5), 711–734 | Definition and measurement limits of the roughness factor (C2.10) | open (IUPAC) | sure |
| R69 | Wei, C., Sun, S., Mandler, D., Wang, X., Qiao, S.Z., Xu, Z.J. (2019). Approaches for measuring the surface areas of metal oxide electrocatalysts for determining their intrinsic electrocatalytic activity. Chemical Society Reviews 48(9), 2518–2534 | Unreliability of capacitance-based area for oxides and hydroxides (C2.10) | paywalled | fairly sure |
| R70 | Newman, J.S., Tobias, C.W. (1962). Theoretical analysis of current distribution in porous electrodes. J. Electrochemical Society 109(12), 1183–1191 | Porous-electrode solution with Tafel kinetics (D8) | paywalled | sure |
| R71 | Newman, J., Thomas-Alyea, K.E. (2004). Electrochemical Systems, 3rd ed. Wiley, ch. 22 | Same; Bruggeman correction | book | sure |
| R72 | Gilliam, R.J., Graydon, J.W., Kirk, D.W., Thorpe, S.J. (2007). A review of specific conductivities of potassium hydroxide solutions for various concentrations and temperatures. Int. J. Hydrogen Energy 32(3), 359–364 | κ of KOH (C07, C08 inputs; my values UNSURE) | paywalled; contains a fitted equation | sure |
| R73 | Vogt, H., Balzer, R.J. (2005). The bubble coverage of gas-evolving electrodes in stagnant electrolytes. Electrochimica Acta 50(10), 2073–2079 | C10 coverage formula (constants UNSURE) | paywalled | sure |
| R74 | Lemlich, R. (1978). A theory for the limiting conductivity of polyhedral foam at low density. J. Colloid and Interface Science 64(1), 107–110 | σ_eff = σ·ρ̄/3 (D9, C06) | paywalled | sure |
| R75 | Carmo, M., Fritz, D.L., Mergel, J., Stolten, D. (2013). A comprehensive review on PEM water electrolysis. Int. J. Hydrogen Energy 38(12), 4901–4934 | System comparison, loadings, membrane resistance (C1.2, C3.2) | paywalled | sure |
| R76 | Zeng, K., Zhang, D. (2010). Recent progress in alkaline water electrolysis for hydrogen production and applications. Progress in Energy and Combustion Science 36(3), 307–326 | Alkaline cell losses: ohmic, bubbles, electrodes (C3.2, C2.8) | paywalled | sure |
| R77 | Schalenbach, M., Kasian, O., Mayrhofer, K.J.J. (2018). An alkaline water electrolyzer with nickel electrodes enables efficient high current density operation. Int. J. Hydrogen Energy 43(27), 11932–11938 | Ni electrodes at high current density; separator resistance | UNSURE | fairly sure |
| R78 | Minke, C., Suermann, M., Bensmann, B., Hanke-Rauschenbach, R. (2021). Is iridium demand a potential bottleneck in the realization of large-scale PEM water electrolysis? Int. J. Hydrogen Energy 46(46), 23581–23590 | Scarcity case is about Ir more than Pt (C3.5) | believed open access | fairly sure |

### Embodied energy (B2.11, C3.5)

| ID | Author, year, title, venue | Cited for | Open? | Exists? |
|---|---|---|---|---|
| R79 | Nuss, P., Eckelman, M.J. (2014). Life cycle assessment of metals: a scientific synthesis. PLoS ONE 9(7), e101298 | Cumulative energy demand per kg for Cu, Al, Pt, Ir (my values UNSURE: Cu about 54, Al about 131, Pt about 2.4 × 10⁵ MJ/kg) | open access, with supplementary data tables | sure; values UNSURE |
| R80 | Ashby, M.F. (2012). Materials and the Environment: Eco-informed Material Choice, 2nd ed. Butterworth-Heinemann | Embodied-energy ranges for Cu and Al (second source) | book | sure |
| R81 | Faludi, J., Baumers, M., Maskery, I., Hague, R. (2017). Environmental impacts of selective laser melting: do printer, powder, or power dominate? J. Industrial Ecology 21(S1), S144–S156 | Energy per kg of LPBF aluminium parts | UNSURE | fairly sure |
| R82 | Kellens, K., Baumers, M., Gutowski, T.G., Flanagan, W., Lifset, R., Duflou, J.R. (2017). Environmental dimensions of additive manufacturing: mapping application domains and their environmental implications. J. Industrial Ecology 21(S1), S49–S68 | Specific energy ranges of AM processes | UNSURE | fairly sure |

---

## 5. Known weak points of this plan

1. **The gyroid model is parametric.** Rows B09–B13 say what friction and j/f a gyroid would need; they do not say what a gyroid has. Claim B2.6 stands or falls with published data (R38–R51), which S3 can only partly retrieve. S4 should place whatever S3 finds on the (c_f, χ) map and otherwise leave B2.6 at low confidence.
2. **Pin-fin correlations are from memory**, and my hand evaluation of PN3 gives a friction factor that rises again for pitch ratios above 2, which the Žukauskas charts do not show. The spec therefore carries two friction and two Nusselt versions and takes the combination most favourable to pins. If S3 finds PN3 mis-quoted, B07 should be re-run with the corrected constants.
3. **The fin model is 1-D and assumes height-mixed air** (B2.12), and the flow is fully ducted. Bypass, which is the normal case for a fan blowing on a sink, would change the ranking in favour of low-drag designs; it is out of scope here and should be stated as a limit of the verdict.
4. **Equal fan power is one of three fair constraints.** Rows B11–B13 give the other two. The verdict should quote all three.
5. **Exchange current densities and roughness factors are uncertain by an order of magnitude each.** The C2 conclusions are stated as ratios and thresholds for that reason. The oxygen-evolution numbers in C05 are Tafel extrapolations over two decades and are for scale only.
6. **Embodied-energy inputs (B20, C13) are from memory.** Both rows carry wide input ranges; the claims that depend on them (B2.11, C3.5) are at low confidence until S3 confirms the values.
7. **Several checks in §3.2 are identities** and are marked as such. The independent ones are: finite-difference fin (B01); Teertstra model, Poiseuille limit, fully developed Nu (B03); Bejan–Sciubba spacing (B05); cross-correlation and chart range (B06); plate inputs through the porous-fin path (B08); power-law estimate (B12); fan maximum air power (B13); slab and half-space limits (B14); quadrature closures and series limit (B16); second-order logarithm term (B18); linearised radiation (B19); textbook 59.16 mV (C01); Tafel and linear limits (C02); closed-form ratio and J-independence (C03); Tafel form (C04); two conductivity models and the solid bound (C06); Runge–Kutta shooting and both asymptotes (C07); finite-thickness against semi-infinite solution (C08). Rows B02, B04, B10, B11, B15, B17, B20, C05, C09–C13 have no independent check or only a plausibility range.
