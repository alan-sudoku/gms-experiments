"""L05: convert Opila & Hann 1997 (J. Am. Ceram. Soc. 80, 197) paralinear constants
from mass units (read by OCR from data/raw/opila_hann_1997.pdf, Tables III and IV)
to oxide-thickness units, to compare with the planner range
k_p' 1e-17..1e-15 m^2/s and k_l 1e-12..1e-10 m/s.
Assumptions (mine, not from the paper): SiC + 1.5 O2 -> SiO2 + CO, so net O-uptake
mass per mol SiO2 = 1.5*32 - 28 = 20 g, alpha = 60.08/20; rho(SiO2) = 2.2 g/cm3.
Mass-to-thickness: x = alpha*dw/rho, so kp_thick = alpha^2 kp_mass / rho^2 ."""
h = 3600.0
alpha = 60.08 / (1.5*32.00 - 28.01)
rho = 2.2
for kp_mg in (1.05e-3, 1.37e-3, 3.80e-3, 5.57e-3):   # Table III range, mg^2/(cm^4 h)
    kp = kp_mg*1e-6/h            # g^2 cm^-4 s^-1
    kp_t = alpha**2*kp/rho**2    # cm^2/s
    print(f"kp_mass {kp_mg:.2e} mg2/cm4/h -> {kp_t*1e-4:.2e} m^2/s")
for kl_mg in (1.43e-3, 1.60e-3, 5.05e-3, 7.75e-3):   # Table IV range, mg SiO2/(cm^2 h)
    kl = kl_mg*1e-3/h/rho        # cm/s
    print(f"kl_mass {kl_mg:.2e} mg/cm2/h -> {kl*1e-2:.2e} m/s")
print("alpha", alpha)
