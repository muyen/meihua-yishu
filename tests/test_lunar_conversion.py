#!/usr/bin/env python3
"""
農曆轉換測試 - 驗證內建農曆數據的準確性
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from meihua_calc import gregorian_to_lunar

# 已驗證的日期轉換對照表
# 來源：香港天文台、中央氣象局萬年曆
KNOWN_CONVERSIONS = [
    # (西曆年, 西曆月, 西曆日, 農曆年, 農曆月, 農曆日, 是否閏月)
    # 2024 年
    (2024, 1, 1, 2023, 11, 20, False),     # 2024年元旦
    (2024, 2, 10, 2024, 1, 1, False),      # 2024年春節
    (2024, 9, 17, 2024, 8, 15, False),     # 2024年中秋節
    (2024, 2, 24, 2024, 1, 15, False),     # 2024年元宵節

    # 2025 年
    (2025, 1, 29, 2025, 1, 1, False),      # 2025年春節
    (2025, 1, 1, 2024, 12, 2, False),      # 2025年元旦

    # 2023 年
    (2023, 1, 22, 2023, 1, 1, False),      # 2023年春節
    (2023, 9, 29, 2023, 8, 15, False),     # 2023年中秋節

    # 閏月測試 (2023年閏二月)
    (2023, 3, 22, 2023, 2, 1, True),       # 2023年閏二月初一
    (2023, 4, 19, 2023, 2, 29, True),      # 2023年閏二月廿九

    # 2020 年 (2020年閏四月)
    (2020, 1, 25, 2020, 1, 1, False),      # 2020年春節
    (2020, 5, 23, 2020, 4, 1, True),       # 2020年閏四月初一

    # 歷史日期
    (2000, 2, 5, 2000, 1, 1, False),       # 2000年春節
    (1990, 1, 27, 1990, 1, 1, False),      # 1990年春節

    # 2026 年
    (2026, 2, 17, 2026, 1, 1, False),      # 2026年春節
    (2026, 1, 18, 2025, 11, 30, False),    # 今天 (2026-01-18) - 春節前30天
]


def test_known_conversions():
    """測試已知的日期轉換"""
    passed = 0
    failed = 0

    for g_year, g_month, g_day, l_year, l_month, l_day, is_leap in KNOWN_CONVERSIONS:
        try:
            result = gregorian_to_lunar(g_year, g_month, g_day)
            lunar_year, lunar_month, lunar_day, lunar_is_leap = result

            if (lunar_year == l_year and lunar_month == l_month and
                lunar_day == l_day and lunar_is_leap == is_leap):
                print(f"✓ {g_year}/{g_month}/{g_day} → {l_year}/{'閏' if is_leap else ''}{l_month}/{l_day}")
                passed += 1
            else:
                print(f"✗ {g_year}/{g_month}/{g_day}")
                print(f"  預期: {l_year}/{'閏' if is_leap else ''}{l_month}/{l_day}")
                print(f"  實際: {lunar_year}/{'閏' if lunar_is_leap else ''}{lunar_month}/{lunar_day}")
                failed += 1
        except Exception as e:
            print(f"✗ {g_year}/{g_month}/{g_day} - 錯誤: {e}")
            failed += 1

    print(f"\n結果: {passed} 通過, {failed} 失敗")
    return failed == 0


def test_date_range():
    """測試日期範圍邊界"""
    print("\n=== 日期範圍測試 ===")

    # 下限
    try:
        result = gregorian_to_lunar(1900, 1, 31)
        print(f"✓ 1900/1/31 → {result[0]}/{result[1]}/{result[2]}")
    except Exception as e:
        print(f"✗ 1900/1/31 - 錯誤: {e}")

    # 上限
    try:
        result = gregorian_to_lunar(2100, 12, 31)
        print(f"✓ 2100/12/31 → {result[0]}/{result[1]}/{result[2]}")
    except Exception as e:
        print(f"✗ 2100/12/31 - 錯誤: {e}")


def test_cli():
    """測試命令行功能"""
    import subprocess

    print("\n=== CLI 測試 ===")

    # 測試 convert 命令
    result = subprocess.run(
        ['python3', 'scripts/meihua_calc.py', 'convert', '2024', '2', '10'],
        capture_output=True, text=True
    )
    print(f"convert 2024/2/10:")
    print(result.stdout)

    # 測試 time 命令
    result = subprocess.run(
        ['python3', 'scripts/meihua_calc.py', 'time'],
        capture_output=True, text=True
    )
    print(f"time 命令輸出 (前10行):")
    for line in result.stdout.split('\n')[:10]:
        print(line)


if __name__ == "__main__":
    print("=== 農曆轉換測試 ===\n")
    success = test_known_conversions()
    test_date_range()
    test_cli()

    sys.exit(0 if success else 1)
