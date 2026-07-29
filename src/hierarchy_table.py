"""
ν轴完整层级表（附录D）
Complete ν-Axis Hierarchy Table

从普朗克紫外基底到可观测宇宙全域的完整层级谱系。

标度规则:
  ν=0: 普朗克尺度, Ds=2
  ν 每增加1: 空间尺度放大φ倍, 能量标度降低φ倍
  l(ν) = l_P · φ^ν
  E(ν) = E_P · φ^(-ν)
"""

import numpy as np
from .constants import PHI, GAMMA, L_PLANCK, E_PLANCK_GEV
from .spectral_dimension import spectral_dimension


def scale_length(nu, l0=L_PLANCK):
    """空间尺度 l(ν) = l_P · φ^ν"""
    return l0 * PHI**nu


def scale_energy(nu, e0=E_PLANCK_GEV):
    """能量标度 E(ν) = E_P · φ^(-ν)"""
    return e0 * PHI**(-nu)


def find_nu_for_length(target_length, l0=L_PLANCK):
    """找到对应特定空间尺度的ν值"""
    return np.log(target_length / l0) / np.log(PHI)


def find_nu_for_energy(target_energy, e0=E_PLANCK_GEV):
    """找到对应特定能量标度的ν值"""
    return -np.log(target_energy / e0) / np.log(PHI)


def key_anchors():
    """论文附录D关键锚点表"""
    anchors = [
        ('普朗克尺度', 0, 1.6e-35, 1.2e19),
        ('电弱尺度', 80, 2e-18, 100),
        ('原子尺度', 117, 5e-11, 25e-6),
        ('宏观尺度', 167, 1.0, 1e-12),
        ('舒曼共振', 190, 1e4, 1e-10),
        ('可观测宇宙', 295, 1e26, 1e-32),
    ]

    print("\n附录D 关键层级锚点:")
    print(f"{'尺度':<15} {'ν值':<8} {'空间尺度(m)':<18} {'能量标度(eV)':<18} {'Ds':<8}")
    print("-" * 67)

    for name, nu, length, energy_gev in anchors:
        length_m = scale_length(nu)
        energy_ev = scale_energy(nu) * 1e9  # GeV -> eV
        Ds = spectral_dimension(nu)
        print(f"{name:<15} {nu:<8} {length_m:<18.2e} {energy_ev:<18.2e} {Ds:<8.4f}")

    return anchors


def full_hierarchy_table(nu_min=0, nu_max=300, step=10):
    """生成完整层级表"""
    print(f"\n完整ν轴层级表 (ν={nu_min}~{nu_max}, 步长{step}):")
    print(f"{'ν':<6} {'l(m)':<15} {'E(GeV)':<15} {'Ds':<8}")
    print("-" * 44)

    for nu in range(nu_min, nu_max + 1, step):
        l = scale_length(nu)
        E = scale_energy(nu)
        Ds = spectral_dimension(nu)
        print(f"{nu:<6} {l:<15.3e} {E:<15.3e} {Ds:<8.4f}")


def fermion_hierarchy():
    """费米子家族的层级分布"""
    from .constants import NU_E
    from .fermion_mass_spectrum import lock4_root_level

    families = [
        ('带电轻子', 1, -1),
        ('上型夸克', 3, 2.0/3.0),
        ('下型夸克', 3, -1.0/3.0),
    ]

    print(f"\n费米子家族层级分布:")
    print(f"{'家族':<12} {'ν_1':<10} {'l(m)':<15} {'E(GeV)':<15}")
    print("-" * 52)

    for name, Nc, Q in families:
        nu_1 = lock4_root_level(NU_E, Nc, Q)
        l = scale_length(nu_1)
        E = scale_energy(nu_1)
        print(f"{name:<12} {nu_1:<10.2f} {l:<15.3e} {E:<15.3e}")


def verify_all():
    """完整验证"""
    print("=" * 60)
    print("附录D ν轴完整层级表")
    print("=" * 60)

    print(f"\n标度规则:")
    print(f"  l(ν) = l_P · φ^ν")
    print(f"  E(ν) = E_P · φ^(-ν)")
    print(f"  γ = ln2/lnφ = {GAMMA:.6f}")

    key_anchors()
    fermion_hierarchy()


if __name__ == "__main__":
    verify_all()
