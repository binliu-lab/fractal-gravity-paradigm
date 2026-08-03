"""
普适几何常数模块
Universal Geometric Constants for the Qi-Field Fractal Gravity Framework

论文《炁场分形引力框架》全局符号与规范说明中定义的全部常数。
所有常数均为精确数学表达式的数值实现，无拟合参数。
"""

import numpy as np

# ============================================================
# 普适几何常数（论文符号表第1节）
# ============================================================

# 黄金分割常数 φ = (1+√5)/2
PHI = (1.0 + np.sqrt(5.0)) / 2.0

# 二分迭代普适标度指数 γ = ln2 / lnφ
GAMMA = np.log(2.0) / np.log(PHI)

# 分形规范常数 K = φ^(-4)（电荷-偏移判据）
K_FRACTAL = PHI ** (-4.0)

# 时间分数阶导数阶数 α_t = 1/φ
ALPHA_T = 1.0 / PHI

# 空间分数阶指数（默认值，随尺度跑动）
ALPHA_S = 1.0 / PHI

# ============================================================
# 三类 κ 参数（论文符号表第2节）
# ============================================================

# 退相干频率标度指数（A-级，精确值）
KAPPA_OMEGA = 3.0

# 退相干层级标度指数 κ_ν = 3γ（B级）
KAPPA_NU = 3.0 * GAMMA

# 带电轻子饱和增益指数 κ_s = 3φ^5（B+级，附录E严格证明）
KAPPA_S = 3.0 * PHI ** 5.0

# ============================================================
# 四把锁核心参数（附录E）
# ============================================================

# 第一把锁：增益动态范围 A = φ^6 - φ
A_GAIN = PHI ** 6.0 - PHI

# 第二把锁：饱和增益指数 κ_s = 3φ^5（同上）
# KAPPA_S 已定义

# 第三把锁：半饱和点 n_0 = 2（共振方程唯一整数解）
N_0 = 2.0

# 第四把锁：增长类型判据 κ_c = φ^3
KAPPA_C = PHI ** 3.0

# ============================================================
# 物理基准常数
# ============================================================

# 普朗克质量（MeV，基准锚定常数，非拟合参数）
# m_P = 1.2209 × 10^22 MeV
M_PLANCK_MEV = 1.2209e22  # MeV

# 普朗克长度（m）
L_PLANCK = 1.616e-35  # m

# 普朗克能量（GeV）
E_PLANCK_GEV = 1.2209e19  # GeV

# 电子质量（MeV，实验锚定常数）
M_ELECTRON_MEV = 0.510998950  # MeV (PDG2024)

# 电子根层级基准 ν_e（精确恒等式：ν_e = log₂(m_P/m_e)）
# 不是拟合参数，而是普朗克标度到电子标度的二分迭代层数
NU_E = 74.34

# ============================================================
# 宇宙学基准参数（Planck 2018 TT+TE+EE+lensing）
# ============================================================

# 哈勃常数 H_0 (km/s/Mpc)
H_0 = 67.66  # km/s/Mpc

# 物质密度参数
OMEGA_M0 = 0.3111

# 暗能量密度参数
OMEGA_LAMBDA0 = 0.6889

# 辐射密度参数
OMEGA_R0 = 9.2e-5

# 光速（m/s）
C_LIGHT = 2.99792458e8

# 玻尔兹曼常数（eV/K）
K_B = 8.617333e-5

# ============================================================
# 舒曼共振参数
# ============================================================

# 舒曼共振基频（Hz）
SCHUMANN_FREQ = 7.83  # Hz

# 舒曼共振对应层级
NU_SCHUMANN = 190.0

# ============================================================
# 五量合一与五边形嵌套常数（第19-20章新增）
# ============================================================

# 五边形终极不变量 Ω = 4/(5φ) = 2(√5-1)/5
OMEGA = 4.0 / (5.0 * PHI)

# 五边形嵌套信息容量极限 I_total(∞) = Σ φ^(-2k) = φ
I_TOTAL_LIMIT = PHI  # 1/(1-φ^(-2)) = φ

# 五边形形状因子 F(φ) = 5sin(π/5)/π
PENTAGON_SHAPE_FACTOR = 5.0 * np.sin(np.pi / 5.0) / np.pi

# 五边形特征回音周期因子 φ^(-2) * F(φ)
ECHO_PERIOD_FACTOR = PHI ** (-2.0) * PENTAGON_SHAPE_FACTOR

# 最小损耗原理：层间传输效率 η = φ/2
ETA_OPTIMAL = PHI / 2.0

# 最小损耗原理：信息压缩率 r = 1/φ
R_OPTIMAL = 1.0 / PHI

# 脑电γ波核心频率（Hz）
GAMMA_WAVE_FREQ = 40.0  # Hz

# CMB退耦红移
Z_REC = 1100.0

# CMB退耦对应五边形层级
K_REC = np.log(Z_REC + 1.0) / (2.0 * np.log(PHI))

# ============================================================
# 三才尺度（§4.5 精确推导，2026-08-02新增）
# ============================================================

# 人（电子质量标度）：ν_人 = log₂(m_P/m_e) = 74.34（精确）
NU_HUMAN = NU_E  # 74.34

# 地（谱维数过渡点）：ν_地 = φ² × ν_人 = 194.7（黄金比例自洽）
NU_EARTH = PHI ** 2 * NU_HUMAN  # ≈ 194.7

# 天（宇宙学标度）：ν_天 = 2 × ν_地 = 389.4
NU_HEAVEN = 2.0 * NU_EARTH  # ≈ 389.4

# ν*自洽值（从三才推导）：ν_地 × lnφ/ln2 = 135.2
NU_STAR_SELF_CONSISTENT = NU_EARTH * np.log(PHI) / np.log(2.0)  # ≈ 135.2

# ν*CMB校准值（从谱维数跑动方程反解）
NU_STAR_CMB = 135.3  # 由 Ds(ν_rec=137.2)≈3.578 反解

# 光谱层级换算因子：ν_f = γ × ν_m
NU_SPECTRAL_CONVERSION = GAMMA  # γ = ln2/lnφ ≈ 1.441


def print_constants():
    """打印所有几何常数的数值，用于验证"""
    print("=" * 60)
    print("炁场分形引力框架 — 普适几何常数")
    print("=" * 60)
    print(f"φ (黄金分割)           = {PHI:.10f}")
    print(f"γ (标度指数)           = {GAMMA:.10f}")
    print(f"K (分形规范常数)       = {K_FRACTAL:.10f}")
    print(f"α_t (时间分数阶)       = {ALPHA_T:.10f}")
    print(f"κ_ω (退相干频率)       = {KAPPA_OMEGA:.1f}")
    print(f"κ_ν (退相干层级)       = {KAPPA_NU:.6f}")
    print(f"κ_s (饱和增益)         = {KAPPA_S:.6f}")
    print(f"A = φ^6-φ (增益范围)   = {A_GAIN:.6f}")
    print(f"n_0 (半饱和点)         = {N_0:.1f}")
    print(f"κ_c (增长判据)         = {KAPPA_C:.6f}")
    print(f"m_P (普朗克质量, MeV)   = {M_PLANCK_MEV:.4e}")
    print(f"ν_e (电子根层级基准)    = {NU_E}")
    print(f"H_0 (哈勃常数)         = {H_0} km/s/Mpc")
    print(f"Ω_m0                   = {OMEGA_M0}")
    print(f"Ω_Λ0                   = {OMEGA_LAMBDA0}")
    print(f"Ω (五量合一不变量)       = {OMEGA:.10f}")
    print(f"I_total(∞) (信息容量极限)= {I_TOTAL_LIMIT:.10f}")
    print(f"F(φ) (五边形形状因子)    = {PENTAGON_SHAPE_FACTOR:.6f}")
    print(f"η_opt (最小损耗传输效率) = {ETA_OPTIMAL:.10f}")
    print(f"k_rec (CMB退耦层级)      = {K_REC:.2f}")
    print(f"\n三才尺度 (§4.5):")
    print(f"  ν_人 (电子标度)        = {NU_HUMAN}")
    print(f"  ν_地 (过渡点)          = {NU_EARTH:.1f}")
    print(f"  ν_天 (宇宙学标度)       = {NU_HEAVEN:.1f}")
    print(f"  ν*(自洽)               = {NU_STAR_SELF_CONSISTENT:.1f}")
    print(f"  ν*(CMB校准)             = {NU_STAR_CMB}")
    print(f"  交叉验证偏差             = {abs(NU_STAR_SELF_CONSISTENT - NU_STAR_CMB)/NU_STAR_CMB*100:.2f}%")
    print("=" * 60)

    # 验证关键恒等式
    print("\n关键恒等式验证:")
    print(f"  φ^2 = φ + 1          : {PHI**2:.10f} vs {PHI+1:.10f}  {'✓' if abs(PHI**2 - PHI - 1) < 1e-10 else '✗'}")
    print(f"  φ^6 - φ = Σφ^k(k=0..4): {A_GAIN:.10f} vs {sum(PHI**k for k in range(5)):.10f}  {'✓' if abs(A_GAIN - sum(PHI**k for k in range(5))) < 1e-10 else '✗'}")
    print(f"  K = φ^(-4)           : {K_FRACTAL:.10f}")
    print(f"  κ_c = φ^3            : {KAPPA_C:.10f}")


if __name__ == "__main__":
    print_constants()
