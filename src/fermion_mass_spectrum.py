"""
费米子质量谱的分形几何计算 — 四把锁完整实现
Fermion Mass Spectrum: Four-Lock Geometric Derivation (Appendix E)

本模块实现论文附录E的四把锁定理，从黄金分割分形几何严格导出
三代费米子质量谱，零自由参数。

四把锁：
  1. A = φ^6 - φ  （增益动态范围，几何级数求和）
  2. R_n = 1/(1+φ^{κ(n-n₀)})  （逻辑斯蒂饱和函数）
  3. n₀ = 2  （共振方程唯一整数解）
  4. ν₁ = ν_e + φ³·ln(N_c/|Q|)  （根层级映射）

置信等级：B+
"""

import numpy as np
from .constants import (
    PHI, GAMMA, KAPPA_S, A_GAIN, N_0, KAPPA_C,
    M_PLANCK_MEV, M_ELECTRON_MEV, NU_E, K_FRACTAL
)


# ============================================================
# 第一把锁：A = φ^6 - φ
# ============================================================

def lock1_gain_range():
    """
    第一把锁：质量增益动态范围 A = φ^6 - φ

    证明：五态循环累积耦合强度为等比级数
      S = Σ_{k=0}^{4} φ^k = (φ^5 - 1)/(φ - 1) = φ(φ^5 - 1) = φ^6 - φ

    返回:
        A: 增益动态范围
    """
    # 方法1：直接计算 φ^6 - φ
    A_direct = PHI**6 - PHI

    # 方法2：等比级数求和 Σ_{k=0}^{4} φ^k
    A_series = sum(PHI**k for k in range(5))

    # 验证一致性
    assert abs(A_direct - A_series) < 1e-10, "第一把锁验证失败"

    return A_direct


# ============================================================
# 第二把锁：逻辑斯蒂饱和函数与 κ_s = 3φ^5
# ============================================================

def saturation_factor(n, kappa=KAPPA_S, n0=N_0, D=1.0):
    """
    第二把锁：逻辑斯蒂饱和因子

    R_n = 1 / (1 + D · φ^{κ·(n - n₀)})

    参数:
        n:   代数（1, 2, 3, ...）
        kappa: 饱和速率（默认 κ_s = 3φ^5）
        n0:  半饱和点（默认 n_0 = 2）
        D:   饱和强度因子（几何预言值 D = 1）

    返回:
        R_n: 饱和因子
    """
    exponent = kappa * (n - n0)
    return 1.0 / (1.0 + D * PHI**exponent)


def lock2_saturation_params():
    """
    第二把锁验证：κ_s = 3φ^5 的拓扑起源

    单维涡旋需五阶分形迭代达到稳定饱和，
    三维叠加后总指数为 3φ^5。
    """
    kappa_single = PHI**5  # 单维：φ^5
    kappa_total = 3 * kappa_single  # 三维：3φ^5

    assert abs(kappa_total - KAPPA_S) < 1e-10
    return kappa_total


# ============================================================
# 第三把锁：n_0 = 2
# ============================================================

def lock3_resonance_equation():
    """
    第三把锁：半饱和点 n_0 = 2 是五态-代际共振方程的唯一整数稳定解

    共振方程：φ^{n_0 - 2} = 2/m,  m ∈ Z+

    枚举验证：
      m=1: n_0 = 3.44（非整数）
      m=2: n_0 = 2（精确整数解）✓
      m≥3: n_0 < 2（与实验矛盾）
    """
    results = []
    for m in range(1, 6):
        # φ^{n_0 - 2} = 2/m  =>  n_0 = 2 + ln(2/m) / ln(φ)
        if 2.0 / m > 0:
            n0 = 2.0 + np.log(2.0 / m) / np.log(PHI)
            is_integer = abs(n0 - round(n0)) < 1e-6
            results.append({
                'm': m,
                'n_0': n0,
                'is_integer': is_integer,
                'valid': is_integer and n0 >= 2.0
            })

    # 验证 m=2 给出唯一整数解
    assert results[1]['is_integer'] and abs(results[1]['n_0'] - 2.0) < 1e-6

    return results


# ============================================================
# 第四把锁：量子数与分形参数的一一映射
# ============================================================

def lock4_root_level(nu_e, N_c, Q):
    """
    第四把锁-定理E.4.1：根层级映射

    ν₁ = ν_e + φ³ · ln(N_c / |Q|)

    参数:
        nu_e: 电子根层级基准（≈74.34）
        N_c:  色数（轻子=1, 夸克=3）
        Q:    电荷（轻子=-1, 上夸克=+2/3, 下夸克=-1/3）

    返回:
        ν_1: 根层级
    """
    return nu_e + PHI**3 * np.log(N_c / abs(Q))


def lock4_saturation_rate(Q, kappa_s=KAPPA_S, charge_sign='auto'):
    """
    第四把锁-定理E.4.2：饱和速率标度律

    正电荷费米子：κ_正 = κ_s · |Q|^6
    负电荷费米子：κ_负 = (κ_s/φ²) · (2/3)^6

    注意：负电荷公式中的 (2/3)^6 为普适六次标度因子（与上型夸克相同），
    而非使用负电荷自身的 |Q|^6。物理含义：
      κ_d = κ_u / φ² = κ_s·(2/3)^6 / φ²
    即下型夸克的饱和速率由上型夸克除以 φ² 得到。

    带电轻子（Q=-1）在质量公式中直接使用 κ_s = 3φ^5，
    不经过此标度律（论文第13章明确指定）。

    参数:
        Q:            电荷
        kappa_s:      基准饱和增益指数（默认 3φ^5）
        charge_sign:  'positive', 'negative', 或 'auto'（自动判断）

    返回:
        kappa: 饱和速率
    """
    if charge_sign == 'auto':
        sign = 'positive' if Q > 0 else 'negative'
    else:
        sign = charge_sign

    # 六次标度因子
    scaling_factor = (2.0 / 3.0)**6  # ≈ 0.0878

    if sign == 'positive':
        # κ_正 = κ_s · |Q|^6
        return kappa_s * abs(Q)**6
    else:
        # κ_负 = (κ_s/φ²) · (2/3)^6
        return (kappa_s / PHI**2) * scaling_factor


def lock4_growth_type(kappa, kappa_c=KAPPA_C):
    """
    第四把锁-定理E.4.3：增长类型判据

    κ_c = φ³ ≈ 4.236
    κ > κ_c: 强饱和，减速型（轻子）
    κ < κ_c: 弱饱和，加速型（夸克）
    """
    if kappa > kappa_c:
        return 'strong_saturation', 'decelerating (lepton-like)'
    else:
        return 'weak_saturation', 'accelerating (quark-like)'


# ============================================================
# 统一质量谱公式（核心计算）
# ============================================================

def fermion_mass(n, nu_1, kappa, A=A_GAIN, n0=N_0, D=1.0, C=1.0,
                m_P=M_PLANCK_MEV):
    """
    三代费米子质量谱的几何闭合公式（附录E综合结论）

    m_n = m_P · 2^{-ν_1} · C · exp[(A/2) · (1 - R_n)^{1/φ}]

    其中 R_n = 1/(1 + D · φ^{κ·(n - n₀)})

    参数:
        n:     代数（1, 2, 3）
        nu_1:  根层级（由量子数确定）
        kappa: 饱和速率（由电荷确定）
        A:     增益动态范围（默认 φ^6-φ）
        n0:    半饱和点（默认 2）
        D:     饱和强度因子（默认 1）
        C:     电子基态修正因子（默认 1）
        m_P:   普朗克质量（MeV）

    返回:
        m_n: 预测质量（MeV）

    注意:
        论文公式中记为 exp[(A/2)·(1-R_n)^{1/φ}]，其中 A = φ⁶-φ ≈ 16.326。
        有效增益为 A/2 ≈ 8.163，来源于逻辑斯蒂饱和函数的半周期对称性。
        MCMC 拟合参数 A ≈ 16.310 与几何预言 A = φ⁶-φ ≈ 16.326 一致，
        证实 A 为总范围参数，质量公式中取半值 A/2 作为有效增益。
        三代带电轻子共用 ν_e ≈ 74.34，质量比由饱和因子 R_n 的代际依赖性产生。
        零参数预言 (C=D=1) 平均偏差 0.74%，MCMC后验 C=1.000, D=0.972 均收敛于1。
    """
    # 计算饱和因子
    R_n = saturation_factor(n, kappa=kappa, n0=n0, D=D)

    # 计算增益项（有效增益 = A/2）
    gain = (A / 2.0) * (1.0 - R_n)**(1.0 / PHI)

    # 计算质量
    m_n = m_P * 2.0**(-nu_1) * C * np.exp(gain)

    return m_n


def predict_charged_lepton_masses(params=None):
    """
    预测三代带电轻子质量（零自由参数版本）

    使用几何预言参数：
      A = φ^6 - φ, n₀ = 2, κ_s = 3φ^5, D = 1, C = 1
      ν_1 = ν_e = 74.34（N_c=1, |Q|=1）

    注意：带电轻子使用 κ_s = 3φ^5（论文第13章明确指定），
    不使用 κ_负（后者用于负电荷夸克的退相干计算，非质量谱计算）。
    """
    if params is None:
        params = {
            'A': A_GAIN,
            'n0': N_0,
            'kappa': KAPPA_S,  # 使用 κ_s = 3φ^5
            'D': 1.0,
            'C': 1.0,
        }

    # 带电轻子参数
    N_c_lepton = 1  # 无色荷
    Q_lepton = -1    # 电荷
    nu_1 = lock4_root_level(NU_E, N_c_lepton, Q_lepton)
    kappa = params['kappa']  # 直接使用 κ_s = 3φ^5

    masses = []
    for n in [1, 2, 3]:
        m = fermion_mass(
            n=n, nu_1=nu_1, kappa=kappa,
            A=params['A'], n0=params['n0'],
            D=params['D'], C=params['C']
        )
        masses.append(m)

    return np.array(masses)


def predict_up_quark_masses(params=None):
    """
    预测三代上型夸克质量

    上型夸克：Q = +2/3, N_c = 3
    κ_u = κ_s · (2/3)^6 ≈ 2.92
    """
    if params is None:
        params = {
            'A': A_GAIN, 'n0': N_0, 'D': 1.0, 'C': 1.0,
        }

    N_c = 3
    Q = 2.0 / 3.0
    nu_1 = lock4_root_level(NU_E, N_c, Q)
    kappa = lock4_saturation_rate(Q, charge_sign='positive')

    masses = []
    for n in [1, 2, 3]:
        m = fermion_mass(n=n, nu_1=nu_1, kappa=kappa,
                         A=params['A'], n0=params['n0'],
                         D=params['D'], C=params['C'])
        masses.append(m)

    return np.array(masses)


def predict_down_quark_masses(params=None):
    """
    预测三代下型夸克质量

    下型夸克：Q = -1/3, N_c = 3
    κ_d = κ_u / φ²
    """
    if params is None:
        params = {
            'A': A_GAIN, 'n0': N_0, 'D': 1.0, 'C': 1.0,
        }

    N_c = 3
    Q = -1.0 / 3.0
    nu_1 = lock4_root_level(NU_E, N_c, Q)
    kappa = lock4_saturation_rate(Q, charge_sign='negative')

    masses = []
    for n in [1, 2, 3]:
        m = fermion_mass(n=n, nu_1=nu_1, kappa=kappa,
                         A=params['A'], n0=params['n0'],
                         D=params['D'], C=params['C'])
        masses.append(m)

    return np.array(masses)


# ============================================================
# 第四代相干度压制
# ============================================================

def fourth_generation_suppression():
    """
    第四代相干度压制计算

    R_4 = 1/(1 + φ^{κ_s*(4-2)}) = 1/(1 + φ^{2κ_s}) ≈ 10^{-14}

    第四代对应 n=4，半饱和点 n_0=2，故指数为 κ_s*(4-2) = 2κ_s。
    有效增益趋近于零，动力学上无法形成稳定费米子。
    """
    R_4 = 1.0 / (1.0 + PHI**(KAPPA_S * (4 - N_0)))
    return R_4


# ============================================================
# 验证函数
# ============================================================

def verify_all_locks():
    """验证四把锁的全部数值"""
    print("\n" + "=" * 60)
    print("附录E 四把锁验证")
    print("=" * 60)

    # 第一把锁
    A = lock1_gain_range()
    A_exp = 16.3262  # 论文给出值
    print(f"\n第一把锁: A = φ^6 - φ")
    print(f"  计算值: {A:.6f}")
    print(f"  论文值: {A_exp}")
    print(f"  实验拟合: 16.310 ± 0.017")
    print(f"  偏差(实验): {abs(A - 16.310)/16.310*100:.3f}%")

    # 第二把锁
    kappa = lock2_saturation_params()
    print(f"\n第二把锁: κ_s = 3φ^5")
    print(f"  计算值: {kappa:.6f}")
    print(f"  论文值: 33.27")
    print(f"  实验反推: 32.92 ± 0.32")
    print(f"  偏差(实验): {abs(kappa - 32.92)/32.92*100:.3f}%")

    # 第三把锁
    resonance = lock3_resonance_equation()
    print(f"\n第三把锁: n_0 = 2（共振方程）")
    for r in resonance:
        status = "✓ 唯一整数解" if r['valid'] else ("整数但无效" if r['is_integer'] else "非整数")
        print(f"  m={r['m']}: n_0 = {r['n_0']:.4f}  {status}")

    # 第四把锁
    print(f"\n第四把锁: 根层级与饱和速率映射")

    families = [
        ('带电轻子', 1, -1, 'negative'),
        ('上型夸克', 3, 2.0/3.0, 'positive'),
        ('下型夸克', 3, -1.0/3.0, 'negative'),
    ]

    for name, Nc, Q, sign in families:
        nu_1 = lock4_root_level(NU_E, Nc, Q)
        kappa_scale = lock4_saturation_rate(Q, charge_sign=sign)

        # 带电轻子在质量公式中直接使用 κ_s = 3φ^5
        # 夸克使用标度律计算的 κ
        if '轻子' in name:
            kappa_actual = KAPPA_S
            kappa_note = f"κ_s (质量公式直接使用)"
        else:
            kappa_actual = kappa_scale
            kappa_note = f"κ_{'正' if sign == 'positive' else '负'} (标度律)"

        growth_type, growth_desc = lock4_growth_type(kappa_actual)

        # 论文给出的验证值
        if '轻子' in name:
            nu_paper = 74.34
            dev = 0.0
        elif '上' in name:
            nu_paper = 80.71
            dev = 0.22
        else:
            nu_paper = 83.65
            dev = 0.12

        print(f"\n  {name}:")
        print(f"    Q = {Q:+.4f}, N_c = {Nc}")
        print(f"    ν_1 = {nu_1:.4f}  (论文: {nu_paper}, 偏差: {dev}%)")
        print(f"    κ   = {kappa_actual:.4f}  ({kappa_note})")
        if '轻子' not in name:
            print(f"         (标度律: {kappa_scale:.4f})")
        print(f"    增长类型: {growth_desc}")

    # 三代带电轻子质量验证
    print(f"\n{'='*60}")
    print("三代带电轻子质量验证")
    print(f"{'='*60}")

    masses = predict_charged_lepton_masses()
    experimental = np.array([0.511, 105.658, 1776.86])  # MeV
    names = ['电子 (e)', 'μ子 (μ)', 'τ子 (τ)']

    print(f"\n{'粒子':<15} {'实验(MeV)':<15} {'预测(MeV)':<15} {'相对偏差':<10}")
    print("-" * 55)

    for name, exp, pred in zip(names, experimental, masses):
        dev = abs(pred - exp) / exp * 100
        print(f"{name:<15} {exp:<15.3f} {pred:<15.3f} {dev:.2f}%")

    avg_dev = np.mean(np.abs(masses - experimental) / experimental * 100)
    max_dev = np.max(np.abs(masses - experimental) / experimental * 100)
    print(f"\n平均偏差: {avg_dev:.2f}%")
    print(f"最大偏差: {max_dev:.2f}%")
    print(f"论文报告: 平均0.74%, 最大1.35%")

    # 第四代压制
    print(f"\n{'='*60}")
    print("第四代相干度压制")
    print(f"{'='*60}")
    R4 = fourth_generation_suppression()
    print(f"  R_4 = 1/(1 + φ^(2κ_s)) = {R4:.2e}")
    print(f"  论文预言: ~10^(-14)")
    print(f"  解释: 第四代无法形成稳定费米子")

    return masses


if __name__ == "__main__":
    verify_all_locks()
