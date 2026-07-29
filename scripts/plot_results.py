"""
可视化脚本 — 生成论文中的关键图表
Visualization: Generate Key Figures from the Paper
"""

import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Windows GBK encoding fix for Unicode output
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.constants import PHI, GAMMA, A_GAIN, KAPPA_S, N_0, NU_E, OMEGA_M0, OMEGA_LAMBDA0
from src.spectral_dimension import spectral_dimension, spectral_dimension_curve
from src.dark_energy import dark_energy_w, dark_energy_w0, hubble_parameter
from src.fermion_mass_spectrum import predict_charged_lepton_masses, saturation_factor
from src.constants import M_PLANCK_MEV

# 设置中文字体和图表样式
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150


def plot_spectral_dimension(savepath='results/spectral_dimension.png'):
    """图1: 谱维数跑动曲线"""
    fig, ax = plt.subplots(figsize=(10, 6))

    nu = np.linspace(0, 300, 1000)
    Ds = spectral_dimension(nu)

    ax.plot(nu, Ds, 'b-', linewidth=2.5, label=r'$D_s(\nu) = 2 + \frac{2}{1+\phi^{\gamma(\nu^*-\nu)}}$')

    # 标注关键点
    ax.axhline(y=2, color='r', linestyle='--', alpha=0.5, label=r'UV limit: $D_s=2$')
    ax.axhline(y=4, color='g', linestyle='--', alpha=0.5, label=r'IR limit: $D_s=4$')

    # CMB退耦点
    nu_rec = 137.2
    Ds_rec = spectral_dimension(nu_rec)
    ax.plot(nu_rec, Ds_rec, 'ro', markersize=10, zorder=5)
    ax.annotate(f'CMB退耦\nν={nu_rec}, Ds={Ds_rec:.3f}',
                xy=(nu_rec, Ds_rec), xytext=(nu_rec+20, Ds_rec-0.5),
                arrowprops=dict(arrowstyle='->', color='red'),
                fontsize=11, color='red')

    ax.set_xlabel(r'$\nu$ (分形层级)', fontsize=14)
    ax.set_ylabel(r'$D_s$ (谱维数)', fontsize=14)
    ax.set_title('谱维数跑动方程 (附录E)', fontsize=16)
    ax.legend(fontsize=12)
    ax.set_xlim(0, 300)
    ax.set_ylim(1.8, 4.2)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    os.makedirs(os.path.dirname(savepath), exist_ok=True)
    plt.savefig(savepath, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  已保存: {savepath}")


def plot_dark_energy_eos(savepath='results/dark_energy_w0.png'):
    """图2: 暗能量状态方程随红移演化"""
    fig, ax = plt.subplots(figsize=(10, 6))

    z = np.linspace(0, 5, 500)
    a = 1.0 / (1.0 + z)
    w = dark_energy_w(a)

    ax.plot(z, w, 'b-', linewidth=2.5, label=r'$w(a)_{\mathrm{fractal}}$')
    ax.axhline(y=-1.0, color='gray', linestyle='--', alpha=0.5, label=r'$w=-1$ ($\Lambda$CDM)')

    # 标注当前值
    w0 = dark_energy_w0()
    ax.plot(0, w0, 'ro', markersize=10, zorder=5)
    ax.annotate(f'$w_0 = {w0:.4f}$\n(Planck+BAO: $-0.96\\pm0.05$)',
                xy=(0, w0), xytext=(0.5, w0-0.03),
                arrowprops=dict(arrowstyle='->', color='red'),
                fontsize=11, color='red')

    # 观测约束区域
    ax.axhspan(-1.01, -0.91, alpha=0.1, color='green', label='Planck+BAO 1σ')

    ax.set_xlabel('红移 z', fontsize=14)
    ax.set_ylabel('w(z)', fontsize=14)
    ax.set_title('分形暗能量状态方程 (第9章)', fontsize=16)
    ax.legend(fontsize=11, loc='lower right')
    ax.set_xlim(0, 5)
    ax.set_ylim(-1.05, -0.93)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    os.makedirs(os.path.dirname(savepath), exist_ok=True)
    plt.savefig(savepath, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  已保存: {savepath}")


def plot_fermion_masses(savepath='results/fermion_masses.png'):
    """图3: 三代带电轻子质量预测对比"""
    fig, ax = plt.subplots(figsize=(10, 6))

    # 实验值
    exp_masses = np.array([0.511, 105.658, 1776.86])
    pred_masses = predict_charged_lepton_masses()

    names = ['电子 (e)', 'μ子 (μ)', 'τ子 (τ)']
    x = np.arange(len(names))
    width = 0.35

    # 对数尺度比较
    log_exp = np.log10(exp_masses)
    log_pred = np.log10(pred_masses)

    bars1 = ax.bar(x - width/2, log_exp, width, label='实验值', color='steelblue', alpha=0.8)
    bars2 = ax.bar(x + width/2, log_pred, width, label='分形预言', color='coral', alpha=0.8)

    # 标注数值
    for bar, val in zip(bars1, exp_masses):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f'{val:.1f}', ha='center', va='bottom', fontsize=10)
    for bar, val in zip(bars2, pred_masses):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f'{val:.1f}', ha='center', va='bottom', fontsize=10)

    ax.set_ylabel(r'$\log_{10}$(mass/MeV)', fontsize=14)
    ax.set_title('三代带电轻子质量：实验值 vs 分形预言 (附录C)', fontsize=16)
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=12)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    os.makedirs(os.path.dirname(savepath), exist_ok=True)
    plt.savefig(savepath, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  已保存: {savepath}")


def plot_saturation_curve(savepath='results/saturation_curve.png'):
    """图4: 逻辑斯蒂饱和函数曲线"""
    fig, ax = plt.subplots(figsize=(10, 6))

    n = np.linspace(0, 4, 500)
    R = saturation_factor(n)

    ax.plot(n, R, 'b-', linewidth=2.5, label=r'$R_n = \frac{1}{1+\phi^{\kappa_s(n-n_0)}}$')

    # 标注三代
    for gen in [1, 2, 3]:
        R_val = saturation_factor(gen)
        ax.plot(gen, R_val, 'ro', markersize=10, zorder=5)
        ax.annotate(f'n={gen}\nR={R_val:.4f}',
                    xy=(gen, R_val), xytext=(gen+0.2, R_val+0.1),
                    fontsize=10, color='red')

    # 第四代
    R4 = saturation_factor(4)
    ax.plot(4, R4, 'rx', markersize=12, markeredgewidth=3, zorder=5)
    ax.annotate(f'n=4\nR≈{R4:.1e}\n(被压制)',
                xy=(4, R4), xytext=(3.2, 0.3),
                arrowprops=dict(arrowstyle='->', color='red'),
                fontsize=10, color='red')

    ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=N_0, color='gray', linestyle='--', alpha=0.5, label=r'$n_0={:.0f}$ (half-sat)'.format(N_0))

    ax.set_xlabel('代数 n', fontsize=14)
    ax.set_ylabel('饱和因子 R_n', fontsize=14)
    ax.set_title(r'Logic Saturation ($\kappa_s = 3\phi^5 \approx {:.2f}$)'.format(KAPPA_S), fontsize=16)
    ax.legend(fontsize=12)
    ax.set_xlim(0, 4.5)
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    os.makedirs(os.path.dirname(savepath), exist_ok=True)
    plt.savefig(savepath, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  已保存: {savepath}")


def plot_cmb_summary(savepath='results/cmb_summary.png'):
    """图5: CMB峰位偏移总结图"""
    fig, ax = plt.subplots(figsize=(10, 6))

    # 预言区间
    ax.barh(0, 0.91-0.23, left=0.23, height=0.3, color='coral', alpha=0.7,
            label='分形预言区间 [-0.23%, -0.91%]')

    # Planck误差
    ax.errorbar(0.23, 0, xerr=0.23, fmt='s', color='blue', markersize=10,
                capsize=5, label='Planck ±0.23%')

    # CMB-S4误差
    ax.errorbar(0.23, -0.4, xerr=0.06, fmt='D', color='green', markersize=10,
                capsize=5, label='CMB-S4 ±0.06% (2029)')

    ax.axvline(x=0, color='black', linestyle='-', alpha=0.3)

    ax.set_xlabel(r'$|\Delta\ell_1/\ell_1|$ (%)', fontsize=14)
    ax.set_yticks([0, -0.4])
    ax.set_yticklabels(['Planck\n(当前)', 'CMB-S4\n(2029)'], fontsize=12)
    ax.set_title('CMB第一声学峰位偏移检验窗口', fontsize=16)
    ax.legend(fontsize=11, loc='upper right')
    ax.set_xlim(0, 1.2)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    os.makedirs(os.path.dirname(savepath), exist_ok=True)
    plt.savefig(savepath, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  已保存: {savepath}")


def main():
    print("=" * 60)
    print("生成可视化图表")
    print("=" * 60)

    plot_spectral_dimension()
    plot_dark_energy_eos()
    plot_fermion_masses()
    plot_saturation_curve()
    plot_cmb_summary()

    print(f"\n所有图表已保存到 results/ 目录")


if __name__ == "__main__":
    main()
