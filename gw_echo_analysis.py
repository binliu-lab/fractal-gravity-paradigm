"""
#5: Gravitational Wave Echo: 8*pi vs 8*ln(3) Baseline Comparison
Analyze the pentagonal correction factor 0.357 and its relation to standard QNM results.
"""
import numpy as np

phi = (1 + np.sqrt(5)) / 2
gamma = np.log(2) / np.log(phi)

print("=== #5: Gravitational Wave Echo Baseline Comparison ===")
print(f"phi = {phi:.10f}")
print()

# 1. Standard QNM in eikonal limit
print("--- 1. Standard GR QNM (eikonal limit) ---")
print("  omega_R = (l + 1/2) / M  (real part)")
print(f"  omega_I = -ln(3)/(8*pi*M)  (imaginary part)")
ln3 = np.log(3)
print(f"  ln(3) = {ln3:.10f}")
print(f"  8*pi = {8*np.pi:.10f}")
print(f"  ln(3)/(8*pi) = {ln3/(8*np.pi):.10f}")
print(f"  This is the standard Motl-Neitzke monodromy result")
print()

# 2. Einstein field equation: 8*pi*G
print("--- 2. Einstein Field Equation ---")
print("  G_munu + Lambda*g_munu = 8*pi*G * T_munu")
print(f"  8*pi = {8*np.pi:.10f}")
print(f"  This appears in the IR limit of fractal gravity (Eq. GR_limit)")
print()

# 3. Pentagonal correction factor 0.357
print("--- 3. Pentagonal Echo Correction Factor ---")
phi_inv2 = phi**(-2)
F_phi = 5 * np.sin(np.pi/5) / np.pi
correction = phi_inv2 * F_phi

print(f"  phi^(-2) = {phi_inv2:.10f}")
print(f"  F(phi) = 5*sin(pi/5)/pi = {F_phi:.10f}")
print(f"  sin(pi/5) = sin(36 deg) = {np.sin(np.pi/5):.10f}")
print(f"  Correction = phi^(-2) * F(phi) = {correction:.10f}")
print(f"  Paper claims: 0.357")
print(f"  Match: {abs(correction - 0.357) < 0.001}")
print()

# 4. Decomposition of 0.357
print("--- 4. Factor Decomposition ---")
print(f"  0.357 = phi^(-2) * F(phi)")
print(f"  = {phi_inv2:.6f} * {F_phi:.6f}")
print()
print("  Physical meaning:")
print(f"    phi^(-2) = 1/phi^2 = 2-phi = {2-phi:.10f}")
print(f"    This is the scale ratio between consecutive pentagon layers")
print(f"    F(phi) = 5*sin(pi/5)/pi is the pentagon shape factor")
print(f"      = ratio of pentagon perimeter to circumscribed circle circumference")
print(f"      = 5*(side_length) / (2*pi*R) where side = 2*R*sin(pi/5)")
print()

# 5. Standard echo delay (no fractal correction)
print("--- 5. Standard vs Fractal Echo Delay ---")
print("  Standard (photon sphere):")
print(f"    delta_t = 2*r_s/c * (1 + ln(2)) approximately")
print(f"    Or more precisely: delta_t ~ 2*r_s/c * (geometric factor)")
print()
print("  Fractal (pentagon):")
print(f"    delta_t_echo = (2*r_s/c) * phi^(-2) * F(phi)")
print(f"                 = (2*r_s/c) * {correction:.6f}")
print(f"    Standard photon sphere delay ~ 2*r_s/c * ~0.5 (order of magnitude)")
print(f"    Ratio: fractal/standard ~ {correction/0.5:.4f}")
print()

# 6. QNM frequency modification
print("--- 6. QNM Frequency Modification ---")
print("  Standard QNM: omega_I = -ln(3)/(8*pi*M)")
print(f"    ln(3) comes from SL(2,R) monodromy trace = 3")
print()
print("  Pentagon monodromy candidate:")
print(f"    |D_5| = 10 (group order)")
print(f"    ln(10) = {np.log(10):.6f}")
print(f"    ln(|D_5|)/ln(3) = {np.log(10)/ln3:.6f}")
print()
print(f"    5*ln(phi) = {5*np.log(phi):.6f}")
print(f"    5*ln(phi)/ln(3) = {5*np.log(phi)/ln3:.6f}")
print()
print(f"    phi^5 = {phi**5:.6f}")
print(f"    ln(phi^5) = {np.log(phi**5):.6f}")
print()

# 7. The key comparison
print("--- 7. Key Comparison: 8*pi vs 8*ln(3) ---")
print("  In Einstein field equation: 8*pi*G appears")
print("    This is KEPT in the IR limit of fractal gravity")
print("    => 8*pi is the IR (low-energy) coupling structure")
print()
print("  In QNM eikonal: ln(3)/(8*pi*M) appears")
print("    ln(3) comes from BH monodromy at the photon sphere")
print("    => ln(3) encodes the UV (near-horizon) structure")
print()
print("  Pentagon modification:")
print(f"    If monodromy trace 3 -> |D_5| = 10:")
print(f"      ln(3) -> ln(10) = {np.log(10):.6f}")
print(f"      Ratio: ln(10)/ln(3) = {np.log(10)/ln3:.4f}")
print(f"      omega_I_fractal/omega_I_GR = ln(10)/ln(3) = {np.log(10)/ln3:.4f}")
print()
print(f"    If monodromy trace 3 -> 5 (pentagon vertices):")
print(f"      ln(3) -> ln(5) = {np.log(5):.6f}")
print(f"      Ratio: ln(5)/ln(3) = {np.log(5)/ln3:.4f}")
print()
print(f"    If monodromy trace 3 -> phi^5 (golden pentagon):")
print(f"      ln(3) -> ln(phi^5) = {5*np.log(phi):.6f}")
print(f"      Ratio: 5*ln(phi)/ln(3) = {5*np.log(phi)/ln3:.4f}")
print()

# 8. The 0.357 factor: detailed derivation
print("--- 8. Detailed Derivation of 0.357 ---")
print("  Echo delay = (2*r_s/c) * phi^(-2) * F(phi)")
print()
print("  Step 1: Pentagon layer scale")
print(f"    k-th layer radius: R_k = r_s * phi^(-2k)")
print(f"    First layer: R_1 = r_s * phi^(-2) = r_s * {phi_inv2:.6f}")
print()
print("  Step 2: Pentagon shape factor")
print(f"    F(phi) = 5*sin(pi/5)/pi")
print(f"    = (pentagon perimeter) / (circumscribed circle circumference)")
print(f"    = 5 * 2*R*sin(pi/5) / (2*pi*R)")
print(f"    = 5*sin(pi/5)/pi = {F_phi:.6f}")
print()
print("  Step 3: Combined correction")
print(f"    phi^(-2) * F(phi) = {phi_inv2:.6f} * {F_phi:.6f} = {correction:.6f}")
print(f"    This is the factor 0.357 in the paper")
print()

# 9. Numerical verification of echo periods
print("--- 9. Echo Period Numerical Verification ---")
c = 3e8  # m/s
G = 6.674e-11
M_sun = 1.989e30
r_s_factor = 2 * G * M_sun / c**2  # Schwarzschild radius per solar mass

for M_Msun in [10, 30, 1e6]:
    r_s = r_s_factor * M_Msun
    dt_echo = 2 * r_s / c * correction * 1000  # ms
    f_mod = 1 / (2 * r_s / c * phi_inv2 * F_phi) / 1000  # kHz
    print(f"  M={M_Msun:.0f} Msun: r_s={r_s:.1f} m, "
          f"echo period={dt_echo:.2f} ms, mod freq={f_mod:.2f} kHz")

print()
print("Done.")
