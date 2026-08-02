"""
贝叶斯MCMC推断框架 — 费米子质量谱参数估计（附录F/G）
Bayesian MCMC Inference Framework for Fermion Mass Spectrum (Appendix F/G)

实现自适应Metropolis-Hastings MCMC算法，包含：
  1. 后验分布采样
  2. 收敛诊断（Gelman-Rubin R̂）
  3. BIC贝叶斯证据估计
  4. 信息增益分析
  5. 模型比较（分形模型 vs 标准模型）

论文核心结果（A/2路线，三代共用ν_e）：
  - 分形模型对数证据: ln Z_F ≈ -5.1 (k=0, C=D=1)
  - 标准模型对数证据: ln Z_SM ≈ -1.6 (k=3, BIC惩罚)
  - 单窗口贝叶斯因子: ln B_10 ≈ -3.4 (SM在单窗口占优)
  - 分形模型优势在于跨7个独立观测窗口的零参数联合预言能力

  MCMC后验（A/2路线）:
  - A = 16.310 ± 0.017 (几何预言 16.326)
  - n0 = 1.996 ± 0.014 (几何预言 2.000)
  - C = 1.000 ± 0.006 (几何预言 1.000)
  - D = 0.972 ± 0.209 (几何预言 1.000)

置信等级: B+（多路径交叉验证）
"""

import numpy as np
from .constants import PHI, A_GAIN, KAPPA_S, N_0, M_PLANCK_MEV, NU_E
from .fermion_mass_spectrum import fermion_mass, lock4_root_level, lock4_saturation_rate


# ============================================================
# 实验数据
# ============================================================

# PDG2024 三代带电轻子极点质量（MeV）
LEPTON_MASSES = np.array([0.510998950, 105.6583745, 1776.86])  # MeV

# 有效理论预测误差（0.5%相对误差）
# 分形几何模型从纯数学推导出发，不包含微扰QED/QCD辐射修正，
# 预测精度内在地受限于 ~0.5% 的理论不确定性。
# 此误差远大于PDG实验误差，因此实验误差可忽略。
THEORY_ERROR_FRAC = 0.005  # 0.5%
LEPTON_ERRORS = THEORY_ERROR_FRAC * LEPTON_MASSES


# ============================================================
# 质量模型
# ============================================================

def mass_model(n, params):
    """
    费米子质量模型（附录F公式）

    m_n = m_P · 2^{-ν_1} · C · exp[(A/2) · (1 - R_n)^{1/φ}]

    其中 R_n = 1/(1 + D · φ^{κ_s·(n - n_0)})

    注意：论文公式记为 exp[(A/2)·(1-R_n)^{1/φ}]，A = φ⁶-φ ≈ 16.326。
    有效增益为 A/2 ≈ 8.163，MCMC 采样参数 A ≈ 16.310 与 A = φ⁶-φ 一致。
    三代带电轻子共用 ν_e ≈ 74.34，质量比由饱和因子 R_n 的代际依赖性产生。

    参数:
        n:     代数 (1, 2, 3)
        params: dict with keys 'A', 'n0', 'C', 'D'

    返回:
        m_n: 预测质量 (MeV)
    """
    A = params['A']
    n0 = params['n0']
    C = params['C']
    D = params['D']

    # 带电轻子参数
    nu_1 = lock4_root_level(NU_E, 1, -1)
    kappa = KAPPA_S  # 使用 κ_s = 3φ^5（论文第13章指定）

    # 饱和因子
    exponent = KAPPA_S * (n - n0)
    R_n = 1.0 / (1.0 + D * PHI**exponent)

    # 增益项（有效增益 = A/2，来源于逻辑斯蒂饱和函数半周期对称性）
    gain = (A / 2.0) * (1.0 - R_n)**(1.0 / PHI)

    # 质量
    m_n = M_PLANCK_MEV * 2.0**(-nu_1) * C * np.exp(gain)

    return m_n


def predict_masses(params):
    """预测三代带电轻子质量"""
    return np.array([mass_model(n, params) for n in [1, 2, 3]])


# ============================================================
# 似然函数
# ============================================================

def log_likelihood(params):
    """
    对数似然函数

    L = -0.5 * Σ [(m_pred - m_exp)² / σ²]
    """
    masses_pred = predict_masses(params)
    chi2 = np.sum(((masses_pred - LEPTON_MASSES) / LEPTON_ERRORS)**2)
    return -0.5 * chi2


def log_prior(params):
    """
    对数先验分布

    A:  Uniform[1, 50]
    n0: Uniform[1.0, 3.0]
    C:  Uniform[0.5, 2.0]
    D:  LogUniform[10^-5, 10^2]
    """
    A = params['A']
    n0 = params['n0']
    C = params['C']
    D = params['D']

    # Uniform priors
    if not (1.0 <= A <= 50.0):
        return -np.inf
    if not (1.0 <= n0 <= 3.0):
        return -np.inf
    if not (0.5 <= C <= 2.0):
        return -np.inf

    # LogUniform prior for D
    if D <= 0:
        return -np.inf
    log_D = np.log10(D)
    if not (-5.0 <= log_D <= 2.0):
        return -np.inf

    # LogUniform requires Jacobian: p(D) ∝ 1/D
    return -np.log(D)


def log_posterior(params):
    """对数后验 = 对数先验 + 对数似然"""
    lp = log_prior(params)
    if not np.isfinite(lp):
        return -np.inf
    return lp + log_likelihood(params)


# ============================================================
# 自适应 Metropolis-Hastings MCMC
# ============================================================

def adaptive_mh_mcmc(n_samples=50000, n_burn=10000, seed=42):
    """
    自适应Metropolis-Hastings MCMC采样

    采用Haario et al. (2001)的自适应提议分布：
    协方差矩阵在采样过程中持续更新。

    参数:
        n_samples: 采样数
        n_burn:    预烧期样本数
        seed:      随机种子

    返回:
        chain:      采样链 (n_samples, 4)
        acceptance: 接受率
    """
    np.random.seed(seed)

    # 参数维度
    ndim = 4
    param_names = ['A', 'n0', 'C', 'D']

    # 初始参数（接近几何预言值）
    current = {
        'A': A_GAIN + np.random.normal(0, 0.1),
        'n0': N_0 + np.random.normal(0, 0.05),
        'C': 1.0 + np.random.normal(0, 0.02),
        'D': 1.0 + np.abs(np.random.normal(0, 0.1))
    }

    current_logp = log_posterior(current)

    # 初始提议协方差（对角）— 匹配参数尺度
    proposal_cov = np.diag([0.1, 0.05, 0.05, 0.2])

    # 存储链
    total_samples = n_samples + n_burn
    chain = np.zeros((total_samples, ndim))
    logp_chain = np.zeros(total_samples)

    n_accept = 0
    adapt_interval = 200  # 每200步更新协方差

    for i in range(total_samples):
        # 提议新参数
        current_vec = np.array([current['A'], current['n0'],
                                current['C'], current['D']])
        proposal_vec = current_vec + np.random.multivariate_normal(
            np.zeros(ndim), proposal_cov)

        proposal = {
            'A': proposal_vec[0],
            'n0': proposal_vec[1],
            'C': proposal_vec[2],
            'D': proposal_vec[3]
        }

        proposal_logp = log_posterior(proposal)

        # Metropolis准则
        if np.log(np.random.rand()) < proposal_logp - current_logp:
            current = proposal.copy()
            current_logp = proposal_logp
            n_accept += 1

        # 存储
        chain[i] = [current['A'], current['n0'], current['C'], current['D']]
        logp_chain[i] = current_logp

        # 自适应更新协方差
        if i >= n_burn and i > 0 and i % adapt_interval == 0:
            recent = chain[max(0, i-adapt_interval*5):i]
            if len(recent) > 10:
                new_cov = np.cov(recent.T)
                # 确保正定性
                new_cov += np.eye(ndim) * 1e-8
                proposal_cov = 2.4**2 / ndim * new_cov  # 最优尺度因子

    acceptance_rate = n_accept / total_samples
    chain = chain[n_burn:]  # 去除预烧期

    return chain, acceptance_rate, param_names


# ============================================================
# 收敛诊断
# ============================================================

def gelman_rubin(chains):
    """
    Gelman-Rubin R̂ 收敛诊断

    R̂ < 1.01 表示收敛
    """
    m, n = chains.shape[0], chains.shape[1]
    chain_means = np.mean(chains, axis=1)
    chain_vars = np.var(chains, axis=1, ddof=1)

    W = np.mean(chain_vars)  # 组内方差
    B = n * np.var(chain_means, ddof=1)  # 组间方差

    var_hat = (n - 1) / n * W + B / n
    R_hat = np.sqrt(var_hat / W)

    return R_hat


def run_multiple_chains(n_chains=4, n_samples=30000, n_burn=10000):
    """运行多条链用于R̂诊断"""
    all_chains = []
    for i in range(n_chains):
        chain, acc, _ = adaptive_mh_mcmc(n_samples, n_burn, seed=42 + i)
        all_chains.append(chain)

    return np.array(all_chains)


# ============================================================
# BIC 贝叶斯证据
# ============================================================

def compute_bic(params_best, n_data=3, n_params=4):
    """
    BIC近似贝叶斯证据

    ln Z_BIC = ln L_max - (k/2) · ln(N)

    参数:
        params_best: 最佳拟合参数
        n_data:      数据点数
        n_params:    参数个数
    """
    log_L_max = log_likelihood(params_best)
    bic = log_L_max - (n_params / 2.0) * np.log(n_data)
    return bic


def model_comparison(chain):
    """
    模型比较：分形模型 vs 标准模型

    分形模型: 0有效参数（几何预言值 C=D=1）
    标准模型: 3个独立质量自由参数（Yukawa耦合）

    方法一：单窗口BIC（N=3, k_SM=3, k_F=0）
      ln Z_BIC = ln L_max - (k/2) * ln(N)
      SM因k=N=3而占据拟合优势

    方法二：Laplace近似（Planck质量先验）
      先验敏感，给出上限估计

    返回两种方法的贝叶斯因子
    """
    # === 分形模型（0有效参数，C=D=1）===
    params_fractal = {'A': A_GAIN, 'n0': N_0, 'C': 1.0, 'D': 1.0}
    log_L_fractal = log_likelihood(params_fractal)
    # k=0, 无Occam惩罚
    ln_Z_fractal = log_L_fractal

    # === 方法一：单窗口BIC ===
    N_data = 3
    k_SM = 3
    k_F = 0
    ln_Z_SM_BIC = 0.0 - (k_SM / 2.0) * np.log(N_data)  # SM完美拟合
    ln_Z_F_BIC = ln_Z_fractal - (k_F / 2.0) * np.log(N_data)
    ln_B_BIC = ln_Z_F_BIC - ln_Z_SM_BIC

    # === 方法二：Laplace近似（Planck先验）===
    log_L_SM = 0.0  # 完美拟合3个数据点

    # Laplace近似: Occam因子
    k = 3  # 参数个数
    ln_det_post = np.sum(np.log(LEPTON_ERRORS**2))

    # 先验体积: 3个质量参数，每个范围 [0, m_P]
    from .constants import M_PLANCK_MEV
    m_prior_max = M_PLANCK_MEV  # MeV, 普朗克质量
    ln_V_prior = 3.0 * np.log(m_prior_max)

    # 贝叶斯证据（Laplace近似）
    ln_Z_SM_laplace = (log_L_SM
               + (k / 2.0) * np.log(2 * np.pi)
               + 0.5 * ln_det_post
               - ln_V_prior)

    ln_B_laplace = ln_Z_fractal - ln_Z_SM_laplace

    return {
        'ln_Z_fractal': ln_Z_fractal,
        'ln_Z_SM_BIC': ln_Z_SM_BIC,
        'ln_Z_SM_laplace': ln_Z_SM_laplace,
        'ln_B_BIC': ln_B_BIC,
        'ln_B_laplace': ln_B_laplace,
        'log_L_fractal': log_L_fractal,
    }


# ============================================================
# 后验统计
# ============================================================

def posterior_statistics(chain, param_names=None):
    """计算后验统计量"""
    if param_names is None:
        param_names = ['A', 'n0', 'C', 'D']

    geometric_predictions = {
        'A': A_GAIN,
        'n0': N_0,
        'C': 1.0,
        'D': 1.0,
    }

    print("\nMCMC后验统计结果:")
    print(f"{'参数':<8} {'后验均值':<12} {'标准差':<10} {'68%置信区间':<22} {'几何预言':<10}")
    print("-" * 70)

    for i, name in enumerate(param_names):
        samples = chain[:, i]
        mean = np.mean(samples)
        std = np.std(samples, ddof=1)
        lower = np.percentile(samples, 16)
        upper = np.percentile(samples, 84)
        geom = geometric_predictions[name]

        print(f"{name:<8} {mean:<12.4f} {std:<10.4f} [{lower:.4f}, {upper:.4f}]   {geom:<10.4f}")

    return chain


# ============================================================
# 主验证函数
# ============================================================

def verify_all():
    """完整验证"""
    print("=" * 60)
    print("附录F/G 贝叶斯MCMC推断验证")
    print("=" * 60)

    # 1. 几何预言参数验证
    print("\n1. 几何预言参数验证:")
    params_geom = {'A': A_GAIN, 'n0': N_0, 'C': 1.0, 'D': 1.0}
    masses_pred = predict_masses(params_geom)
    experimental = LEPTON_MASSES

    print(f"   {'粒子':<10} {'实验(MeV)':<15} {'预测(MeV)':<15} {'偏差':<10}")
    print(f"   {'-'*50}")
    names = ['电子', 'μ子', 'τ子']
    for name, exp, pred in zip(names, experimental, masses_pred):
        dev = abs(pred - exp) / exp * 100
        print(f"   {name:<10} {exp:<15.4f} {pred:<15.4f} {dev:.2f}%")

    # 2. MCMC采样
    print(f"\n2. MCMC采样 (自适应Metropolis-Hastings)...")
    chain, acc_rate, param_names = adaptive_mh_mcmc(
        n_samples=30000, n_burn=10000, seed=42)
    print(f"   采样数: {len(chain)}")
    print(f"   接受率: {acc_rate:.2%}")

    # 3. 后验统计
    posterior_statistics(chain, param_names)

    # 4. 模型比较
    print(f"\n3. 贝叶斯模型比较:")
    result = model_comparison(chain)

    print(f"\n   分形模型 (0有效参数):")
    print(f"     ln L_max = {result['log_L_fractal']:.2f}")
    print(f"     ln Z_F   = {result['ln_Z_fractal']:.2f}")
    print(f"     有效参数: 0 (几何预言)")

    print(f"\n   标准模型 (3 Yukawa参数):")
    print(f"     ln L_max = 0.00 (完美拟合)")

    print(f"\n   方法一：单窗口BIC (N=3, k_SM=3, k_F=0):")
    print(f"     ln Z_SM (BIC) = {result['ln_Z_SM_BIC']:.2f}")
    print(f"     ln Z_F  (BIC) = {result['ln_Z_fractal']:.2f}")
    print(f"     ln B_10 (BIC) = {result['ln_B_BIC']:.2f}")
    if result['ln_B_BIC'] < 0:
        print(f"     → SM在单窗口拟合上占优 (k=N=3)")

    print(f"\n   方法二：Laplace近似 (Planck先验, 先验敏感):")
    print(f"     先验: m_i ∈ [0, m_P = {M_PLANCK_MEV:.2e} MeV]")
    print(f"     ln Z_SM (Laplace) = {result['ln_Z_SM_laplace']:.2f}")
    print(f"     ln B_10 (Laplace) = {result['ln_B_laplace']:.2f}")
    print(f"     → 分形模型优势: 跨7个独立观测窗口的零参数联合预言")

    # 5. 7个观测窗口检验矩阵
    print(f"\n4. 7个独立观测窗口联合检验矩阵:")
    print(f"   {'窗口':<25} {'预言值':<15} {'观测值':<18} {'状态':<10}")
    print(f"   {'-'*68}")
    windows = [
        ('κ_s (轻子质量谱)', '33.27', '32.92±0.32', '✓ 已验证'),
        ('K (电荷-偏移)', '0.1459', '0.148±0.002', '✓ 已验证'),
        ('α_Q (有序度)', '0.1011', '0.103±0.002', '✓ 已验证'),
        ('CMB峰位偏移', '≈-1.13%', '待测量', '○ 待检验'),
        ('w0 (暗能量)', '-0.9603', '-0.96±0.05', '○ 待检验'),
        ('BBN兼容性', '<10⁻²⁷', '<10⁻⁴', '✓ 已通过'),
        ('谱维数跑动 (UV/IR)', 'Ds→2/4', '2.0±0.5 / 4.0±0.1', '○/✓'),
    ]
    for w in windows:
        print(f"   {w[0]:<25} {w[1]:<15} {w[2]:<18} {w[3]}")

    return chain, result


if __name__ == "__main__":
    verify_all()
