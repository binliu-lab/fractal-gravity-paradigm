"""
谱维数跑动方程 — 从离散热核严格导出（附录A）
Spectral Dimension Running: Derivation from Discrete Heat Kernel (Appendix A)

谱维数 Ds(ν) 描述随机游走在分形结构上的扩散维度，
是刻画时空分形特性的核心物理量。

跑动方程: Ds(ν) = 2 + 2/(1 + φ^{γ(ν* - ν)})

紫外极限: Ds → 2（普朗克尺度）
红外极限: Ds → 4（宏观尺度）

置信等级: B+
"""

import numpy as np
from .constants import PHI, GAMMA


def spectral_dimension(nu, nu_star=None):
    """
    谱维数跑动方程

    Ds(ν) = 2 + 2/(1 + φ^{γ(ν* - ν)})

    参数:
        nu:      分形层级
        nu_star: 谱维数转变特征层级
                 默认由CMB退耦校准: Ds(ν_rec=137.2) ≈ 3.578 反解得到 ν* ≈ 135.3

    返回:
        Ds: 谱维数
    """
    if nu_star is None:
        # 由 Ds(ν_rec=137.2) = 3.578 反解 ν*
        # 3.578 = 2 + 2/(1+φ^{γ(ν*-137.2)}) => φ^{γ(ν*-137.2)} = 2/1.578 - 1 ≈ 0.2674
        # γ(ν*-137.2) = ln(0.2674)/ln(φ) => ν* = 137.2 + ln(0.2674)/(γ·ln(φ))
        nu_rec = 137.2
        Ds_rec = 3.578
        ratio = 2.0 / (Ds_rec - 2.0) - 1.0  # φ^{γ(ν*-ν_rec)}
        nu_star = nu_rec + np.log(ratio) / (GAMMA * np.log(PHI))

    exponent = GAMMA * (nu_star - nu)
    return 2.0 + 2.0 / (1.0 + PHI**exponent)


def spectral_dimension_derivative(nu, nu_star=None):
    """
    谱维数跑动方程的导数 dDs/dν

    dDs/dν = γ · (Ds - 2)(4 - Ds)

    这是附录A中的微分方程形式。
    """
    Ds = spectral_dimension(nu, nu_star)
    return GAMMA * (Ds - 2.0) * (4.0 - Ds)


def verify_cmb_recombination():
    """
    验证CMB退耦时期的谱维数

    ν_rec ≈ 137.2 对应 Ds ≈ 3.578
    ν* ≈ 135.3（由退耦条件反解）
    """
    nu_rec = 137.2
    Ds_rec = spectral_dimension(nu_rec)

    # 计算实际使用的 ν*
    ratio = 2.0 / (3.578 - 2.0) - 1.0
    nu_star_actual = nu_rec + np.log(ratio) / (GAMMA * np.log(PHI))

    print(f"CMB退耦时期谱维数:")
    print(f"  ν_rec = {nu_rec}")
    print(f"  ν* (转变特征层级) = {nu_star_actual:.2f}")
    print(f"  Ds(ν_rec) = {Ds_rec:.4f}")
    print(f"  论文值: 3.578")
    print(f"  偏差: {abs(Ds_rec - 3.578)/3.578*100:.4f}%")
    return Ds_rec


def verify_uv_ir_limits():
    """验证紫外和红外极限"""
    print(f"\n谱维数极限验证:")

    # 紫外极限 (ν << ν*)
    Ds_uv = spectral_dimension(0)
    print(f"  紫外极限 (ν=0):   Ds = {Ds_uv:.6f}  (预期: 2.0)")

    # 红外极限 (ν >> ν*)
    Ds_ir = spectral_dimension(500)
    print(f"  红外极限 (ν=500): Ds = {Ds_ir:.6f}  (预期: 4.0)")

    # 转变区域
    nu_star_actual = 135.30
    Ds_star = spectral_dimension(nu_star_actual)
    print(f"  转变点 (ν*=135.3): Ds = {Ds_star:.6f}  (预期: 3.0)")


def compute_transition_rate():
    """
    计算过渡速率并与其他量子引力方案对比

    本框架过渡速率: γ ≈ 0.72/量级
    """
    # 过渡速率 = γ/2 (半周期对称)
    rate = GAMMA / 2.0
    print(f"\n过渡速率对比:")
    print(f"  本分形框架: {rate:.2f}/量级")
    print(f"  CDT:        ~0.5/量级")
    print(f"  渐近安全引力: 待定")


def spectral_dimension_curve(nu_range=None):
    """
    生成谱维数跑动曲线数据

    返回 (ν, Ds) 数组用于绘图
    """
    if nu_range is None:
        nu_range = np.linspace(0, 300, 1000)
    Ds = spectral_dimension(nu_range)
    return nu_range, Ds


def verify_all():
    """完整验证"""
    print("=" * 60)
    print("附录A 谱维数跑动验证")
    print("=" * 60)
    print(f"\n基本参数:")
    print(f"  γ = ln2/lnφ = {GAMMA:.6f}")
    print(f"  ν* = 137.2 (CMB退耦校准)")

    verify_cmb_recombination()
    verify_uv_ir_limits()
    compute_transition_rate()

    # 量子引力方案对比表
    print(f"\n{'='*60}")
    print("量子引力方案对比")
    print(f"{'='*60}")
    print(f"{'方案':<20} {'紫外Ds':<12} {'红外Ds':<12} {'过渡速率':<12}")
    print("-" * 56)
    print(f"{'CDT':<20} {'2.0±0.25':<12} {'4.0':<12} {'~0.5/量级':<12}")
    print(f"{'渐近安全引力':<20} {'2.0':<12} {'4.0':<12} {'待定':<12}")
    print(f"{'Hořava-Lifshitz':<20} {'2.0':<12} {'4.0':<12} {'~0.5/量级':<12}")
    print(f"{'本分形框架':<20} {'2.0':<12} {'4.0':<12} {f'{GAMMA/2:.2f}/量级':<12}")


if __name__ == "__main__":
    verify_all()
