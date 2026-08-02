"""#9: Key Numerical Identity Verification"""
import numpy as np

phi = (1 + np.sqrt(5)) / 2
gamma = np.log(2) / np.log(phi)

print("=== #9: Key Numerical Identity Verification ===")
print(f"phi = {phi:.15f}")
print(f"1/phi = {1/phi:.15f}")
print(f"phi-1 = {phi-1:.15f}")
print(f"1/phi == phi-1: {abs(1/phi - (phi-1)) < 1e-15}")
print()

print("--- Pentagon Theorem (iv): sum phi^(-2k) ---")
print("Claim: sum(phi^(-2k), k=1..inf) = 1/(phi^2-1) = 1/phi")
for n in [3, 5, 10, 20, 50, 100]:
    s = sum(phi**(-2*k) for k in range(1, n+1))
    print(f"  n={n:3d}: S={s:.15f}, dev_from_1/phi={abs(s - 1/phi):.2e}")
S_inf = 1 / (phi**2 - 1)
print(f"  Analytic: 1/(phi^2-1) = {S_inf:.15f}")
print(f"  1/phi = {1/phi:.15f}")
print(f"  Match: {abs(S_inf - 1/phi) < 1e-15}")
print()

print("--- A = phi^6 - phi ---")
A = phi**6 - phi
print(f"A = {A:.10f}")
print(f"A/2 = {A/2:.10f}")
print()

print("--- gamma/25 ---")
print(f"gamma = ln2/ln(phi) = {gamma:.10f}")
print(f"gamma/25 = {gamma/25:.10f}")
print()

print("--- Information capacity limit ---")
print(f"Claim: I_total(inf) = sum(phi^(-2k), k=1..inf)")
print(f"  = 1/(phi^2-1) = {S_inf:.15f}")
print(f"  = 1/phi = {1/phi:.15f}")
print(f"  phi = {phi:.15f}")
print(f"  NOTE: sum = 1/phi, NOT phi. Paper says phi. Need to check.")
print()

print("--- Omega = 4/(5*phi) ---")
Omega = 4 / (5 * phi)
print(f"Omega = 4/(5*phi) = {Omega:.10f}")
print()

print("--- D5 group theory checks ---")
print(f"A = phi^6 - phi = {A:.6f}")
print(f"tr(A^5) = 5*A^5 = {5*A**5:.6f} (claim: 100=|D5|^2)")
print(f"  |D5| = 10, |D5|^2 = 100")
print(f"  Match: {abs(5*A**5 - 100) < 0.001}")
print(f"chi_E1(C2) = phi-1 = {phi-1:.6f}")
print(f"chi_E1(C3) = -phi = {-phi:.6f}")
print(f"|lambda_E1| = A+1 = {A+1:.6f} (claim ~6.236)")
print(f"|lambda_E2| = sqrt((A-1)^2+1) = {np.sqrt((A-1)**2+1):.6f} (claim ~4.041)")
print()

print("--- Coupling scaling (Node 3) ---")
print("Correct: g_i = g_0 * phi^(d_i/2)")
for d, name in [(0, 'gravity'), (1, 'EM'), (2, 'weak'), (3, 'strong')]:
    ratio = phi**(d/2)
    print(f"  d={d} {name:8s}: g_i/g_0 = phi^({d}/2) = {ratio:.6f}")
print()

print("--- GUT scale ---")
M_P = 1.22e19  # GeV
for N in [14, 15, 36]:
    val = M_P * phi**(-N)
    print(f"  N={N:3d}: phi^(-N) = {phi**(-N):.6e}, Lambda_GUT = {val:.4e} GeV")
print(f"  Target: ~1e16 GeV")
print()

print("--- Slow-roll relation check ---")
w0_derived = -1 + (2/3) * (gamma/25)
Omega_m = 0.311
Omega_Lambda = 0.689
factor = Omega_Lambda / (Omega_m + Omega_Lambda)
w0_formula = -1 + (gamma/25) * factor
print(f"w0 from 1+w=2eps/3 (constant): {w0_derived:.6f}")
print(f"w0 from w(a) at a=1:          {w0_formula:.6f}")
print(f"Discrepancy: {abs(w0_derived - w0_formula):.6f} ({abs(w0_derived - w0_formula)/abs(w0_formula)*100:.2f}%)")
