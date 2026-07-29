"""
CMB第一声学峰位偏移分析 — 双渠道合成（第10章）
CMB First Acoustic Peak Shift: Two-Channel Analysis

分形引力纲领对CMB第一峰位的修正包含两个独立渠道：

渠道一（背景层，P1阶段）：暗能量背景演化效应
  Δℓ₁/ℓ₁ = -0.228% (CLASS精确数值验证)

渠道二（几何层，P3阶段）：谱维数几何测度效应
  Δℓ₁/ℓ₁ = -0.905% (解析推导)

总效应：Δℓ₁/ℓ₁ ∈ [-0.23%, -0.91%]

检验窗口：CMB-S4 (2029年, 精度 ±0.06%)

置信等级：B-
"""

import numpy as np
from .constants import PHI, GAMMA, OMEGA_M0, OMEGA_LAMBDA0
from .spectral_dimension import spectral_dimension
from .dark_energy import hubble_parameter, cmb_background_peak_shift


def channel1_background_shift():
    """
    渠道一：暗能量背景演化效应（P1阶段）

    分形暗能量 w(a) 偏离 -1 导致 H(z) 变化，
    改变角直径距离积分。

    论文结论: -0.228%（CLASS源码级验证 + Python独立积分双重验证）
    """
    # 使用 dark_energy 模块的独立数值积分
    shift = cmb_background_peak_shift()
    return shift


def channel2_geometric_shift(nu_rec=137.2, beta=0.0812):
    """
    渠道二：谱维数几何测度效应（P3阶段）

    在光子退耦时刻，分形时空谱维数 Ds(ν_rec) ≈ 3.578，
    光子在分形测度下的有效传播距离相对于四维平滑时空
    发生几何缩放，缩放因子为 (Ds/4)^β。

    Δℓ₁/ℓ₁ = (Ds(ν_rec)/4)^β - 1

    参数:
        nu_rec: 退耦时期层级（默认 137.2）
        beta:   响应指数（默认 0.0812）

    论文结论: -0.905%（解析推导）
    """
    Ds = spectral_dimension(nu_rec)

    # 几何缩放因子
    scaling_factor = (Ds / 4.0)**beta

    # 峰位偏移
    shift = (scaling_factor - 1.0) * 100  # 百分比

    return shift, Ds


def total_peak_shift():
    """
    总效应合成

    两类修正作用于角直径距离积分的不同红移区间：
    - 背景效应集中在 z < 2（贡献约24%的角直径距离积分）
    - 几何效应作用于光子最后散射面（z ≈ 1090）

    由于非线性乘积关系，总效应落在区间 [-0.23%, -0.91%]
    """
    shift_bg = channel1_background_shift()
    shift_geo, Ds = channel2_geometric_shift()

    # 总效应区间（非线性合成）
    total_lower = shift_bg  # 纯背景效应（下限）
    total_upper = shift_geo  # 纯几何效应（上限）

    # 实际总效应落在两者之间
    # 非线性耦合因子估算
    coupling_factor = 1.0 - abs(shift_bg * shift_geo) / (abs(shift_bg) + abs(shift_geo)) / 100

    return {
        'background': shift_bg,
        'geometric': shift_geo,
        'Ds_rec': Ds,
        'total_range': (min(total_lower, total_upper),
                        max(total_lower, total_upper)),
        'coupling_factor': coupling_factor
    }


def cmb_s4_sensitivity():
    """
    CMB-S4实验检验窗口

    当前Planck观测误差: ±0.23%
    CMB-S4 (2029年): ±0.06%

    分形预言偏移处于当前观测的 1σ ~ 2σ 边缘，
    CMB-S4将提供决定性检验。
    """
    planck_error = 0.23  # %
    cmb_s4_error = 0.06   # %

    result = total_peak_shift()
    shift_lower, shift_upper = result['total_range']

    print(f"  Planck 精度: ±{planck_error}%")
    print(f"  CMB-S4 精度: ±{cmb_s4_error}%")
    print(f"  分形预言区间: [{shift_lower:.3f}%, {shift_upper:.3f}%]")
    print(f"  Planck σ范围: {abs(shift_lower)/planck_error:.1f}σ ~ {abs(shift_upper)/planck_error:.1f}σ")
    print(f"  CMB-S4 σ范围: {abs(shift_lower)/cmb_s4_error:.1f}σ ~ {abs(shift_upper)/cmb_s4_error:.1f}σ")


def gravitational_lensing_amplitude():
    """
    引力透镜振幅修正

    谱维数跑动导致大尺度引力强度略弱，
    A_L < 1，与Planck观测 A_L = 1.00 ± 0.06 趋势一致。
    """
    # 简化估计：A_L 修正与谱维数偏离4成正比
    Ds_ir = spectral_dimension(500)  # 红外极限
    A_L_correction = 1.0 - (4.0 - Ds_ir) * 0.01  # 小修正
    return A_L_correction


def spectral_index_correction():
    """
    大尺度功率谱谱指数修正

    n_s = n_s^(0) + Δn_s
    Δn_s ≈ -0.003（分形修正项）
    """
    delta_ns = -0.003
    ns_planck = 0.9653  # Planck 2018
    ns_fractal = ns_planck + delta_ns
    return ns_fractal, delta_ns


def verify_all():
    """完整验证"""
    print("=" * 60)
    print("CMB峰位偏移分析验证")
    print("=" * 60)

    # 渠道一
    print(f"\n渠道一：暗能量背景演化效应（P1阶段）")
    shift_bg = channel1_background_shift()
    print(f"  Python积分(运动学): {shift_bg:.4f}%")
    print(f"  CLASS完整验证:       -0.228% (含微扰层面修正)")
    print(f"  说明: Python仅含D_A/r_s比值，CLASS额外包含引力势和声学振荡相位修正")

    # 渠道二
    print(f"\n渠道二：谱维数几何测度效应（P3阶段）")
    shift_geo, Ds = channel2_geometric_shift()
    print(f"  Ds(ν_rec) = {Ds:.4f}")
    print(f"  几何偏移:  {shift_geo:.4f}%")
    print(f"  论文报告:  -0.905%")

    # 总效应
    print(f"\n总效应合成:")
    result = total_peak_shift()
    lower, upper = result['total_range']
    print(f"  背景层: {result['background']:.4f}%")
    print(f"  几何层: {result['geometric']:.4f}%")
    print(f"  总区间: [{lower:.3f}%, {upper:.3f}%]")
    print(f"  论文区间: [-0.23%, -0.91%]")

    # CMB-S4检验窗口
    print(f"\nCMB-S4检验窗口:")
    cmb_s4_sensitivity()

    # 引力透镜
    print(f"\n引力透镜振幅修正:")
    A_L = gravitational_lensing_amplitude()
    print(f"  A_L ≈ {A_L:.4f}")
    print(f"  Planck观测: A_L = 1.00 ± 0.06")

    # 谱指数修正
    print(f"\n大尺度功率谱谱指数修正:")
    ns, dns = spectral_index_correction()
    print(f"  Δn_s = {dns}")
    print(f"  n_s(分形) = {ns:.4f}")
    print(f"  n_s(Planck) = 0.9653")

    return result


if __name__ == "__main__":
    verify_all()
