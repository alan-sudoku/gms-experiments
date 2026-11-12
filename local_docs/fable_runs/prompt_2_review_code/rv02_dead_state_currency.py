"""Reviewer check of the BLOCKER (answer L1, plan C8/D5, rows R24-R25) and of V5's
"same decisions" claim. All results are claims at level `derived` (unverified).

Question: is the framework's (CExC - b)/T0 a logic error, or a different, also defensible,
currency? Two currencies for a ledger whose losses occur in environments at different T0,k:
  entropy basis   : S = sum_k W_k / T0,k                 (answer's correction)
  lost-work basis : B = sum_k W_k  (each loss valued in its own environment)
The framework writes Sigma = W_earth/T0 + S_op with S_op = W_op/T0 in orbit, i.e.
Sigma = (W_earth + W_op)/T0 = B/T0: the lost-work basis divided by one constant.
Run: python3 rv02_dead_state_currency.py > outputs/rv02_dead_state_currency.txt
"""
import numpy as np

TREF, T0 = 298.15, 200.0
Wg, Ws = 900e3, 600e3            # Earth-side lost work [J] (R25 inputs)
Sg, Ss = 1500.0, 2700.0          # orbital entropy generation [J/K] (R25 inputs)

ent_g, ent_s = Wg / TREF + Sg, Ws / TREF + Ss
fw_g, fw_s = Wg / T0 + Sg, Ws / T0 + Ss
lw_g, lw_s = Wg + T0 * Sg, Ws + T0 * Ss                   # lost work, orbit losses at T0
print(f"entropy basis      : g-s = {ent_g-ent_s:+.3f} J/K  -> {'g wins' if ent_g<ent_s else 'g loses'}")
print(f"framework          : g-s = {fw_g-fw_s:+.3f} J/K  -> {'g wins' if fw_g<fw_s else 'g loses'}")
print(f"lost-work basis    : g-s = {lw_g-lw_s:+.1f} J    -> {'g wins' if lw_g<lw_s else 'g loses'}")
print(f"lost-work / T0     : g-s = {(lw_g-lw_s)/T0:+.3f} J/K (identical to framework)")
# V5 / plan D5(1): "exergy basis against one declared T0*, B = T0* * Sigma_total, same ordering"
for Tstar in (200.0, 298.15):
    print(f"V5 'exergy basis' T0*={Tstar}: T0* x entropy margin = {Tstar*(ent_g-ent_s):+.1f} J (same sign as entropy basis by construction)")

# random sweep: how often do the two currencies disagree?
rng = np.random.default_rng(0)
N = 100000
T0r = rng.uniform(150, 290, N)
Wg_, Ws_ = rng.uniform(0, 2e6, N), rng.uniform(0, 2e6, N)
Sg_, Ss_ = rng.uniform(0, 1e4, N), rng.uniform(0, 1e4, N)
ent = (Wg_ - Ws_) / TREF + (Sg_ - Ss_)
lw = (Wg_ - Ws_) + T0r * (Sg_ - Ss_)
fw = (Wg_ - Ws_) / T0r + (Sg_ - Ss_)
print(f"sweep T0 in [150,290] K: framework sign == lost-work sign in {np.mean(np.sign(fw)==np.sign(lw))*100:.2f} % of cases")
print(f"sweep: entropy-basis and lost-work-basis verdicts disagree in {np.mean(np.sign(ent)!=np.sign(lw))*100:.2f} % of cases")
