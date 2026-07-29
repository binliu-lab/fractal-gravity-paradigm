"""
主运行脚本 — 复现论文全部数值结果
Main Reproduction Script

运行所有模块，验证论文中的关键数值预言。
"""

import sys
import os
import time

# Windows GBK encoding fix for Unicode output
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# 添加src到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    print("\n" + "╔" + "═" * 60 + "╗")
    print("║" + "  分形引力纲领：全部数值结果复现".center(48) + "║")
    print("║" + "  Fractal Gravity Paradigm: Full Reproduction".center(48) + "║")
    print("╚" + "═" * 60 + "╝\n")

    start_time = time.time()

    # ============================================================
    # 模块1: 普适几何常数
    # ============================================================
    print("\n" + "█" * 60)
    print("█  模块 1/7: 普适几何常数")
    print("█" * 60)
    from src.constants import print_constants
    print_constants()

    # ============================================================
    # 模块2: 谱维数跑动（附录A）
    # ============================================================
    print("\n\n" + "█" * 60)
    print("█  模块 2/7: 谱维数跑动（附录A）")
    print("█" * 60)
    from src.spectral_dimension import verify_all as verify_ds
    verify_ds()

    # ============================================================
    # 模块3: ν轴层级表（附录D）
    # ============================================================
    print("\n\n" + "█" * 60)
    print("█  模块 3/7: ν轴层级表（附录D）")
    print("█" * 60)
    from src.hierarchy_table import verify_all as verify_hierarchy
    verify_hierarchy()

    # ============================================================
    # 模块4: 费米子质量谱（附录E 四把锁）
    # ============================================================
    print("\n\n" + "█" * 60)
    print("█  模块 4/7: 费米子质量谱 — 四把锁（附录E）")
    print("█" * 60)
    from src.fermion_mass_spectrum import verify_all_locks
    verify_all_locks()

    # ============================================================
    # 模块5: 分形暗能量（第9章、附录C）
    # ============================================================
    print("\n\n" + "█" * 60)
    print("█  模块 5/7: 分形暗能量（第9章、附录C）")
    print("█" * 60)
    from src.dark_energy import verify_all as verify_de
    de_results = verify_de()

    # ============================================================
    # 模块6: CMB峰位偏移分析（第10章）
    # ============================================================
    print("\n\n" + "█" * 60)
    print("█  模块 6/7: CMB峰位偏移分析（第10章）")
    print("█" * 60)
    from src.cmb_analysis import verify_all as verify_cmb
    verify_cmb()

    # ============================================================
    # 模块7: 贝叶斯MCMC推断（附录F/G）
    # ============================================================
    print("\n\n" + "█" * 60)
    print("█  模块 7/7: 贝叶斯MCMC推断（附录F/G）")
    print("█" * 60)
    from src.bayesian_inference import verify_all as verify_bayes
    verify_bayes()

    # ============================================================
    # 总结
    # ============================================================
    elapsed = time.time() - start_time
    print("\n\n" + "╔" + "═" * 60 + "╗")
    print("║" + "  全部计算完成".center(48) + "║")
    print("╠" + "═" * 60 + "╣")
    print(f"║  耗时: {elapsed:.1f} 秒")
    print("║")
    print("║  关键结果摘要:")
    print(f"║  ✓ 暗能量 w0 = {de_results['w0']:.4f} (论文: -0.9603)")
    print(f"║  ✓ 宇宙年龄 = {de_results['age_fractal']:.1f} Gyr (论文: ~137.3)")
    print(f"║  ✓ BBN Ω_DE = {de_results['omega_de_bbn']:.1e} (约束: <1e-4)")
    print(f"║  ✓ CMB背景偏移 = {de_results['cmb_shift']:.3f}% (运动学积分; CLASS完整验证: -0.228%)")
    print("╚" + "═" * 60 + "╝")


if __name__ == "__main__":
    main()
