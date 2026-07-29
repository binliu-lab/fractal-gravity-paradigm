"""
通用工具函数
Utility functions for formatting and output
"""

import numpy as np


def format_scientific(value, sig_figs=4):
    """格式化科学计数法"""
    if value == 0:
        return "0"
    exp = int(np.floor(np.log10(abs(value))))
    mantissa = value / 10**exp
    return f"{mantissa:.{sig_figs}f}e{exp:+d}"


def print_separator(char="=", width=60):
    """打印分隔线"""
    print(char * width)


def print_header(title, width=60):
    """打印标题"""
    print("=" * width)
    print(title)
    print("=" * width)


def print_table(headers, rows, col_widths=None):
    """打印表格"""
    if col_widths is None:
        col_widths = [15] * len(headers)

    # 表头
    header_line = ""
    for h, w in zip(headers, col_widths):
        header_line += f"{h:<{w}}"
    print(header_line)
    print("-" * sum(col_widths))

    # 数据行
    for row in rows:
        line = ""
        for val, w in zip(row, col_widths):
            if isinstance(val, float):
                line += f"{val:<{w}.4f}"
            else:
                line += f"{str(val):<{w}}"
        print(line)


def jeffreys_interpretation(ln_B):
    """Jeffreys贝叶斯因子判据"""
    abs_b = abs(ln_B)
    if abs_b < 1:
        return "不显著 (not significant)"
    elif abs_b < 2.5:
        return "弱证据 (substantial)"
    elif abs_b < 5:
        return "强证据 (strong)"
    else:
        return "决定性证据 (decisive)"
