"""
#4: Vortex Energy in Fractal Measure - Dimensionless Version
Compute normalized vortex energy E(Ds)/E_ref to check saturation.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import gamma as gamma_func

phi = (1 + np.sqrt(5)) / 2
gamma_val = np.log(2) / np.log(phi)

def vortex_ode(r, y, Ds):
    """Abelian-Higgs vortex equations in D_s dimensions."""
    f, fp, a, ap = y
    rs = max(r, 1e-8)
    # Correct signs: force from V=(1/4)(f^2-1)^2 is (1-f^2)f
    fpp = f * (1 - f**2) / 2 + f * a**2 / rs**2 - (Ds - 1) / rs * fp
    app = (1 - f**2) * a - (Ds - 3) / rs * ap
    return [fp, fpp, ap, app]

def solve_vortex(Ds, r_end=12.0):
    """Find vortex solution by shooting method."""
    r0 = 0.001
    
    def residual(c):
        y0 = [c * r0, c, 1.0, 0.0]
        try:
            sol = solve_ivp(lambda r, y: vortex_ode(r, y, Ds), [r0, r_end], y0,
                          method='RK45', rtol=1e-8, atol=1e-10, max_step=0.02)
            if not sol.success:
                return -100.0
            return sol.y[0, -1] - 1.0
        except:
            return -100.0
    
    # Scan for sign change
    c_list = np.linspace(0.05, 3.0, 40)
    f_list = [residual(c) for c in c_list]
    
    for i in range(len(c_list)-1):
        if f_list[i] * f_list[i+1] < 0:
            try:
                c_sol = brentq(residual, c_list[i], c_list[i+1], xtol=1e-8)
                y0 = [c_sol * r0, c_sol, 1.0, 0.0]
                sol = solve_ivp(lambda r, y: vortex_ode(r, y, Ds), [r0, r_end], y0,
                              method='RK45', rtol=1e-9, atol=1e-11, max_step=0.01,
                              dense_output=True)
                if sol.success:
                    return sol, r0, r_end
            except:
                continue
    return None, r0, r_end

def compute_normalized_energy(Ds):
    """Compute dimensionless vortex energy: E_norm = integral(eps * r^Ds-1) / integral(r^Ds-1)."""
    sol, r0, r_end = solve_vortex(Ds)
    if sol is None:
        return None
    
    r = np.linspace(r0, r_end, 3000)
    y = sol.sol(r)
    f, fp, a, ap = y
    
    # Energy density (dimensionless, in units of v^2)
    eps = 0.5 * fp**2 + 0.5 * ap**2 + (a/np.maximum(r, 1e-10))**2 * f**2 + 0.25 * (f**2 - 1)**2
    
    # Volume-weighted energy
    vol_weight = r**(Ds - 1)
    E_weighted = np.trapezoid(eps * vol_weight, r)
    V_total = np.trapezoid(vol_weight, r)
    
    # Normalized energy = average energy density
    E_norm = E_weighted / V_total
    
    return E_norm, E_weighted, V_total

# Main computation
print("=== #4: Normalized Vortex Energy E(Ds) ===")
print(f"phi = {phi:.6f}, gamma = {gamma_val:.6f}")
print()
print(f"{'Ds':>6s}  {'E_norm':>12s}  {'E_weighted':>14s}  {'Status':>8s}")
print("-" * 50)

Ds_values = np.linspace(2.0, 4.0, 11)
results = []

for Ds in Ds_values:
    res = compute_normalized_energy(Ds)
    if res is not None:
        E_norm, E_w, V = res
        if E_norm > 0 and np.isfinite(E_norm):
            results.append((Ds, E_norm, E_w))
            print(f"{Ds:6.2f}  {E_norm:12.6f}  {E_w:14.4e}  {'OK':>8s}")
        else:
            print(f"{Ds:6.2f}  {'invalid':>12s}  {'N/A':>14s}  {'FAIL':>8s}")
    else:
        print(f"{Ds:6.2f}  {'N/A':>12s}  {'N/A':>14s}  {'FAIL':>8s}")

if len(results) >= 4:
    Ds_arr = np.array([r[0] for r in results])
    E_arr = np.array([r[1] for r in results])
    
    print()
    print("=== Saturation Analysis ===")
    print(f"  E_norm at Ds=2: {E_arr[0]:.6f}")
    print(f"  E_norm at Ds=3: {E_arr[len(E_arr)//2]:.6f}")
    print(f"  E_norm at Ds=4: {E_arr[-1]:.6f}")
    
    # Check monotonicity
    dE = np.diff(E_arr)
    mono = all(dE > 0)
    print(f"  Monotonic increase: {mono}")
    
    if len(dE) >= 2:
        s1 = dE[0] / np.diff(Ds_arr)[0]
        s2 = dE[-1] / np.diff(Ds_arr)[-1]
        print(f"  Slope(Ds~2) = {s1:.6f}")
        print(f"  Slope(Ds~4) = {s2:.6f}")
        print(f"  Slope ratio = {s2/s1:.4f}")
    
    # Try logistic fit
    from scipy.optimize import curve_fit
    try:
        def logistic(x, A, k, x0, off):
            return A / (1 + np.exp(-k*(x - x0))) + off
        popt, _ = curve_fit(logistic, Ds_arr, E_arr, 
                           p0=[E_arr[-1]-E_arr[0], 2, 3, E_arr[0]], maxfev=10000)
        E_fit = logistic(Ds_arr, *popt)
        rms = np.sqrt(np.mean((E_arr - E_fit)**2))
        print()
        print(f"  Logistic fit: E = {popt[0]:.4f}/(1+exp(-{popt[1]:.4f}*(Ds-{popt[2]:.4f}))) + {popt[3]:.4f}")
        print(f"  RMS: {rms:.6f} ({rms/np.mean(E_arr)*100:.2f}%)")
        
        # Compare with spectral dimension formula
        # Ds(nu) = 2 + 2/(1 + phi^(gamma*(nu_star-nu)))
        # If E ~ Ds, then E should follow similar logistic form
        print()
        print("  Compare with spectral dim formula: Ds = 2 + 2/(1+phi^(gamma*(nu*-nu)))")
        print(f"  If E_norm ~ Ds, then E should saturate like Ds(nu)")
        print(f"  Ds range: 2 -> 4, E_norm range: {E_arr[0]:.4f} -> {E_arr[-1]:.4f}")
    except Exception as e:
        print(f"  Logistic fit failed: {e}")
    
    np.savez('vortex_energy_results.npz', Ds=Ds_arr, E_norm=E_arr)
    print("\nResults saved.")

print("\nDone.")
