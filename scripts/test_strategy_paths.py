#!/usr/bin/env python3
"""HEXAGRAM_STRATEGY 變卦路徑回歸測試（獨立、無第三方依賴）。

每條「變N爻」必須以自下而上的爻位（初爻=1 … 上爻=6，與 apply_change 的
約定一致）真正將本卦變為所標示的目標卦，且標註吉率＝目標卦自身的吉率。

此測試會在「變N爻」被誤以自上而下（上爻=1）編號時失敗。可單獨執行：
    python -m unittest scripts.test_strategy_paths
    python scripts/test_strategy_paths.py
"""
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from meihua_calc import (  # noqa: E402
    HEXAGRAM_STRATEGY,
    HEXAGRAMS,
    apply_change,
    binary_to_gua_pair,
    get_hexagram_binary,
)

SHORT = {
    1: "乾", 2: "坤", 3: "屯", 4: "蒙", 5: "需", 6: "訟", 7: "師", 8: "比",
    9: "小畜", 10: "履", 11: "泰", 12: "否", 13: "同人", 14: "大有", 15: "謙",
    16: "豫", 17: "隨", 18: "蠱", 19: "臨", 20: "觀", 21: "噬嗑", 22: "賁",
    23: "剝", 24: "復", 25: "无妄", 26: "大畜", 27: "頤", 28: "大過", 29: "坎",
    30: "離", 31: "咸", 32: "恆", 33: "遯", 34: "大壯", 35: "晉", 36: "明夷",
    37: "家人", 38: "睽", 39: "蹇", 40: "解", 41: "損", 42: "益", 43: "夬",
    44: "姤", 45: "萃", 46: "升", 47: "困", 48: "井", 49: "革", 50: "鼎",
    51: "震", 52: "艮", 53: "漸", 54: "歸妹", 55: "豐", 56: "旅", 57: "巽",
    58: "兌", 59: "渙", 60: "節", 61: "中孚", 62: "小過", 63: "既濟", 64: "未濟",
}


class TestStrategyChangePaths(unittest.TestCase):
    def test_change_paths_use_bottom_up_yao(self):
        num_to_ul = {n: (u, lo) for (u, lo), (n, _) in HEXAGRAMS.items()}
        name_to_num = {v: k for k, v in SHORT.items()}
        checked = 0
        for num, (_type, _advice, _rate, path) in HEXAGRAM_STRATEGY.items():
            if not path:
                continue
            m = re.search(r"變(\d)爻得(\d+)%", path)
            if not m:
                continue  # 多段路徑（如 大過 → 夬 → 革）無單一變爻
            yao = int(m.group(1))
            rate = int(m.group(2))
            target = re.match(r"\s*([^（(]+)", re.split(r"→", path)[-1]).group(1).strip()
            self.assertIn(target, name_to_num,
                          f"卦{num}：無法解析目標卦名 {target!r} ← {path!r}")
            changed = apply_change(get_hexagram_binary(*num_to_ul[num]), yao)
            got = HEXAGRAMS[binary_to_gua_pair(changed)][0]
            self.assertEqual(
                got, name_to_num[target],
                f"卦{num} {SHORT[num]}：變{yao}爻得 {SHORT.get(got)}({got})，"
                f"但路徑宣稱變為 {target}({name_to_num[target]})：{path!r}")
            self.assertEqual(
                rate, HEXAGRAM_STRATEGY[name_to_num[target]][2],
                f"卦{num}：路徑得{rate}% 但目標卦 {target} 吉率="
                f"{HEXAGRAM_STRATEGY[name_to_num[target]][2]}%")
            checked += 1
        self.assertGreaterEqual(checked, 38,
                                f"可解析的變卦路徑應 ≥38 條，實得 {checked}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
