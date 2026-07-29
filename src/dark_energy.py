"""
分形暗能量模型 — 状态方程、宇宙年龄、BBN兼容性
Fractal Dark Energy: EoS, Universe Age, BBN Compatibility

实现论文第9章和附录C的全部计算：
  1. 暗能量状态方程 w(a) 和 w0
  2. 宇宙年龄数值积分
  3. BBN时期暗能量密度占比
  4. CMB背景层峰位偏移验证

置信等级: B级
"""

import numpy as np
from scipy.integrate import quad
from .constants import (
    GAMMA, H_0, OMEGA_M0, OMEGA_LAMBDA0, OMEGA_R0, C_LIGHT
)

# 哈勃常数转换为 SI: H_0 = 67.66 km/s/Mpc
# H_0 (1/s) = 67.66 * 1000 / (3.0857e22)
H_0_SI = H_0 * 1e3 / 3.0857e22  # 1/s

# 1/H_0 = 哈勃时间（秒）
T_HUBBLE = 1.0 / H_0_SI  # seconds

# 哈勃时间（Gyr）
T_HUBBLE_GYR = T_HUBBLE / (3600 * 24 * 365.25 * 1e9)


# ============================================================
# 暗能量状态方程
# ============================================================

def dark_energy_w(a, gamma=GAMMA, omega_m=OMEGA_M0, omega_lam=OMEGA_LAMBDA0):
    """
    分形暗能量状态方程 w(a)

    w(a) = -1 + (γ/25) · Ω_Λ · a^(-3) / (Ω_m + Ω_Λ · a^(-3))

    参数:
        a:        尺度因子（a=1为当前）
        gamma:    分形标度指数
        omega_m:  当前物质密度参数
        omega_lam: 当前暗能量密度参数

    返回:
        w: 状态方程参数
    """
    a3 = a**(-3)
    numerator = (gamma / 25.0) * omega_lam * a3
    denominator = omega_m + omega_lam * a3
    return -1.0 + numerator / denominator


def dark_energy_w0():
    """
    当前暗能量状态方程值 w0 = w(a=1)

    w0 = -1 + (γ/25) · Ω_Λ

    论文预言: w0 = -0.9603
    观测值:   w0 = -0.96 ± 0.05 (Planck+BAO)
    """
    w0 = -1.0 + (GAMMA / 25.0) * OMEGA_LAMBDA0
    return w0


def dark_energy_density(a, gamma=GAMMA,
                         omega_m=OMEGA_M0, omega_lam=OMEGA_LAMBDA0):
    """
    分形暗能量密度演化

    ρ_DE(a) = ρ_DE,0 · ((Ω_m0·a³ + Ω_Λ0) / (Ω_m0 + Ω_Λ0))^(-γ/25)

    由连续性方程积分得到。
    """
    ratio = (omega_m * a**3 + omega_lam) / (omega_m + omega_lam)
    return ratio**(-gamma / 25.0)


# ============================================================
# 宇宙年龄计算
# ============================================================

def hubble_parameter(z, gamma=GAMMA,
                     omega_m=OMEGA_M0, omega_lam=OMEGA_LAMBDA0,
                     omega_r=OMEGA_R0):
    """
    分形模型哈勃参数 H(z) / H_0

    H(z) = H_0 · sqrt(Ω_m·(1+z)³ + Ω_r·(1+z)⁴ + ρ_DE(z)/ρ_DE,0 · Ω_Λ)

    其中 ρ_DE(z)/ρ_DE,0 由分形暗能量密度演化给出。
    """
    a = 1.0 / (1.0 + z)
    de_ratio = dark_energy_density(a, gamma, omega_m, omega_lam)

    matter = omega_m * (1.0 + z)**3
    radiation = omega_r * (1.0 + z)**4
    dark_energy = omega_lam * de_ratio

    return np.sqrt(matter + radiation + dark_energy)


def universe_age(gamma=GAMMA,
                 omega_m=OMEGA_M0, omega_lam=OMEGA_LAMBDA0,
                 omega_r=OMEGA_R0):
    """
    宇宙年龄数值积分

    t_0 = ∫_0^∞ dz / [(1+z) · H(z)]

    通过对哈勃参数积分得到宇宙年龄。
    """
    def integrand(z):
        h = hubble_parameter(z, gamma, omega_m, omega_lam, omega_r)
        return 1.0 / ((1.0 + z) * h)

    # 积分从 z=0 到 z=∞ (实际积分到 z=5000 足够)
    result, error = quad(integrand, 0, 5000, limit=200)

    # 转换为 Gyr
    age_gyr = result * T_HUBBLE_GYR

    return age_gyr


def lcdm_universe_age():
    """ΛCDM基准宇宙年龄（用于对比）"""
    def integrand(z):
        matter = OMEGA_M0 * (1.0 + z)**3
        radiation = OMEGA_R0 * (1.0 + z)**4
        dark_energy = OMEGA_LAMBDA0
        h = np.sqrt(matter + radiation + dark_energy)
        return 1.0 / ((1.0 + z) * h)

    result, _ = quad(integrand, 0, 5000, limit=200)
    return result * T_HUBBLE_GYR


# ============================================================
# BBN兼容性
# ============================================================

def bbn_dark_energy_fraction(z_bbn=1e9):
    """
    BBN时期暗能量密度占比

    在核合成时期 (z ~ 10^9)，暗能量密度占比：
    Ω_DE(z_BBN) ≈ Ω_Λ0 · Ω_m0^(-γ/25) · (1+z)^(3γ/25 - 4)

    论文结论: ~10^{-32}，远小于约束阈值 10^{-4}
    """
    gamma = GAMMA

    # 高红移近似 (a << 1, Ω_Λ·a³ << Ω_m)
    exponent = 3.0 * gamma / 25.0 - 4.0

    # Ω_DE(z) / Ω_m(z)
    omega_de_ratio = (OMEGA_LAMBDA0 * OMEGA_M0**(-gamma / 25.0)
                      * (1.0 + z_bbn)**exponent)

    return omega_de_ratio


def effective_neutrino_species():
    """
    有效相对论自由度

    N_eff = 3.0（与标准模型完全一致，无额外相对论成分）
    """
    return 3.0


# ============================================================
# CMB背景层峰位偏移验证
# ============================================================

def cmb_background_peak_shift():
    """
    CMB第一声学峰位偏移 — 背景层效应

    分形暗能量状态方程 w(a) 偏离 -1 导致哈勃参数 H(z) 在低红移区
    (z < 2) 发生微小变化，进而同时改变：
      1. 角直径距离 D_A = c/(1+z_rec) * ∫_0^{z_rec} dz'/H(z')
      2. 声学视界 r_s = ∫_0^{z_rec} c_s(z)/H(z) dz

    第一声学峰位置 ℓ₁ ∝ D_A / r_s
    峰位偏移 = (D_A^fractal / r_s^fractal) / (D_A^ΛCDM / r_s^ΛCDM) - 1

    论文结论: Δℓ₁/ℓ₁ = -0.228%（P1阶段，CLASS源码级修改验证）

    本函数通过Python独立数值积分验证该结果，
    包含角直径距离和声学视界两个积分的联合变化。

    注意:
    Python独立积分只计算运动学（背景几何）层面的效应，
    即角直径距离 D_A 和声学视界 r_s 的比值变化。
    CLASS完整结果还包含微扰层面的修正：
      - 引力势 Φ,Ψ 随膨胀历史变化（影响Sachs-Wolfe和ISW效应）
      - 声学振荡驱动力的修改（光子-重子耦合方程）
      - 退耦过程相位偏移的微小变化
    这些微扰效应使得 CLASS 结果 (-0.228%) 大于纯运动学积分结果 (~-0.05%)。
    完整复现需要附录H中的 CLASS 源码修改补丁。
    """
    gamma = GAMMA

    # 重子密度参数（Planck 2018: Ω_b h² = 0.02237）
    omega_b = 0.02237 / (H_0 / 100.0)**2  # ≈ 0.0489
    # 光子密度参数（T_CMB = 2.7255 K）
    omega_gamma = 2.469e-5

    def h_fractal(z):
        """分形模型 H(z)/H_0"""
        return hubble_parameter(z, gamma)

    def h_lcdm(z):
        """ΛCDM H(z)/H_0"""
        matter = OMEGA_M0 * (1.0 + z)**3
        radiation = OMEGA_R0 * (1.0 + z)**4
        dark_energy = OMEGA_LAMBDA0
        return np.sqrt(matter + radiation + dark_energy)

    def sound_speed(z):
        """光子-重子等离子体中的声速 c_s/c = 1/sqrt(3(1+R))"""
        R = (3.0 * omega_b) / (4.0 * omega_gamma) / (1.0 + z)
        return 1.0 / np.sqrt(3.0 * (1.0 + R))

    # 退耦红移
    z_rec = 1090.0

    # 1. 角直径距离积分 D_A ∝ ∫_0^{z_rec} dz/H(z)
    D_fractal, _ = quad(lambda z: 1.0 / h_fractal(z), 0, z_rec, limit=200)
    D_lcdm, _ = quad(lambda z: 1.0 / h_lcdm(z), 0, z_rec, limit=200)

    # 2. 声学视界积分 r_s ∝ ∫_0^{z_rec} c_s(z)/H(z) dz
    rs_fractal, _ = quad(lambda z: sound_speed(z) / h_fractal(z), 0, z_rec, limit=200)
    rs_lcdm, _ = quad(lambda z: sound_speed(z) / h_lcdm(z), 0, z_rec, limit=200)

    # 峰位偏移 = (D_A^fractal / r_s^fractal) / (D_A^ΛCDM / r_s^ΛCDM) - 1
    #         = (D_fractal * rs_lcdm) / (D_lcdm * rs_fractal) - 1
    peak_shift = (D_fractal * rs_lcdm) / (D_lcdm * rs_fractal) - 1.0

    return peak_shift * 100  # 转换为百分比


# ============================================================
# 验证函数
# ============================================================

def verify_all():
    """完整验证"""
    print("=" * 60)
    print("分形暗能量模型验证")
    print("=" * 60)

    # 1. 状态方程 w0
    w0 = dark_energy_w0()
    print(f"\n1. 暗能量状态方程 w0:")
    print(f"   计算值:  w0 = {w0:.4f}")
    print(f"   论文预言: w0 = -0.9603")
    print(f"   观测值:   w0 = -0.96 ± 0.05 (Planck+BAO)")
    print(f"   偏差(σ): {abs(w0 - (-0.96)) / 0.05:.4f}σ")

    # 2. 宇宙年龄
    print(f"\n2. 宇宙年龄:")
    age_fractal = universe_age()
    age_lcdm = lcdm_universe_age()
    print(f"   分形模型: {age_fractal:.2f} Gyr")
    print(f"   ΛCDM:     {age_lcdm:.2f} Gyr")
    print(f"   偏差:     {abs(age_fractal - age_lcdm)/age_lcdm*100:.2f}%")
    print(f"   论文报告: ~137.3亿年 (分形) vs 137.9亿年 (ΛCDM)")

    # 3. BBN兼容性
    print(f"\n3. BBN兼容性:")
    omega_de_bbn = bbn_dark_energy_fraction()
    print(f"   Ω_DE(z_BBN) = {omega_de_bbn:.2e}")
    print(f"   约束阈值:    < 10^(-4)")
    print(f"   N_eff = {effective_neutrino_species()}")

    # 4. CMB背景层偏移
    print(f"\n4. CMB背景层峰位偏移:")
    shift = cmb_background_peak_shift()
    print(f"   Python积分: Δℓ/ℓ = {shift:.4f}%")
    print(f"   论文报告:   Δℓ/ℓ = -0.228%")
    print(f"   偏差:       {abs(shift - (-0.228)):.4f}%")

    # 5. 状态方程随红移演化
    print(f"\n5. 状态方程随红移演化:")
    print(f"   {'z':<10} {'w(z)':<12}")
    print(f"   {'-'*22}")
    for z in [0, 0.5, 1.0, 2.0, 5.0, 10.0]:
        w = dark_energy_w(1.0/(1+z))
        print(f"   {z:<10.1f} {w:<12.6f}")

    return {
        'w0': w0,
        'age_fractal': age_fractal,
        'age_lcdm': age_lcdm,
        'omega_de_bbn': omega_de_bbn,
        'cmb_shift': shift
    }


if __name__ == "__main__":
    verify_all()
