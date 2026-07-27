#!/usr/bin/env python3
"""
梅花易數核心邏輯測試 — 起卦、體用、五行、卦德、互/變/錯/綜。

補上原本只有農曆轉換的測試缺口。所有期望值皆人工依易理推定（非照抄程式輸出），
以免把 bug 一起鎖進測試。用 unittest（標準庫，無外部依賴）。
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import meihua_calc as mc


class TestNumberMapping(unittest.TestCase):
    def test_num_to_gua_mod8_with_zero_as_eight(self):
        self.assertEqual(mc.num_to_gua(7), 7)
        self.assertEqual(mc.num_to_gua(8), 8)
        self.assertEqual(mc.num_to_gua(16), 8)   # 餘0當8
        self.assertEqual(mc.num_to_gua(9), 1)

    def test_num_to_yao_mod6_with_zero_as_six(self):
        self.assertEqual(mc.num_to_yao(5), 5)
        self.assertEqual(mc.num_to_yao(6), 6)
        self.assertEqual(mc.num_to_yao(12), 6)   # 餘0當6
        self.assertEqual(mc.num_to_yao(11), 5)


class TestBinaryGeometry(unittest.TestCase):
    def test_get_hexagram_binary_is_upper_then_lower(self):
        # 山雷頤：上艮(100) 下震(001)
        self.assertEqual(mc.get_hexagram_binary(7, 4), "100001")

    def test_apply_change_counts_from_bottom(self):
        # 頤 100001，動第5爻 → index 6-5=1 翻轉 → 110001 (益)
        self.assertEqual(mc.apply_change("100001", 5), "110001")
        # 動初爻(1) → 翻最後一位
        self.assertEqual(mc.apply_change("100001", 1), "100000")

    def test_binary_to_gua_pair_roundtrip(self):
        self.assertEqual(mc.binary_to_gua_pair("100001"), (7, 4))  # 上艮 下震

    def test_hu_gua(self):
        # 頤 100001 的互卦：2-4爻、3-5爻 → 坤坤
        self.assertEqual(mc.get_hu_gua("100001"), (8, 8))


class TestWuxing(unittest.TestCase):
    """五行生剋五種關係全覆蓋（體=木為例）。"""
    def test_bi_he(self):
        self.assertEqual(mc.analyze_wuxing("木", "木"), "比和（吉）")

    def test_yong_sheng_ti(self):
        # 用水 生 體木
        self.assertEqual(mc.analyze_wuxing("木", "水"), "用生體（大吉）")

    def test_ti_sheng_yong(self):
        # 體木 生 用火
        self.assertEqual(mc.analyze_wuxing("木", "火"), "體生用（耗洩）")

    def test_ti_ke_yong(self):
        # 體木 克 用土
        self.assertEqual(mc.analyze_wuxing("木", "土"), "體克用（吉）")

    def test_yong_ke_ti(self):
        # 用金 克 體木
        self.assertEqual(mc.analyze_wuxing("木", "金"), "用克體（凶）")


class TestGuade(unittest.TestCase):
    """卦德互補透鏡（新增功能）。"""
    def test_all_eight_trigrams_have_de(self):
        for num, info in mc.BAGUA.items():
            self.assertIn("de", info, f"卦 {num} 缺 de")
        # 說卦傳卦德對照
        self.assertEqual(mc.BAGUA[1]["de"], "健")  # 乾
        self.assertEqual(mc.BAGUA[6]["de"], "陷")  # 坎
        self.assertEqual(mc.BAGUA[7]["de"], "止")  # 艮

    def test_guade_64_combinations_nonempty_and_named(self):
        for ti in range(1, 9):
            for yo in range(1, 9):
                s = mc.analyze_guade(ti, yo)
                self.assertTrue(s)
                self.assertIn(mc.BAGUA[ti]["de"], s)
                self.assertIn(mc.BAGUA[yo]["de"], s)
                self.assertNotIn("大吉", s)   # 不下吉凶判決
                self.assertNotIn("凶", s)

    def test_same_de_reports_concord(self):
        # 體用同為震(動) → 同德相應
        self.assertIn("同德相應", mc.analyze_guade(4, 4))


class TestCuoZong(unittest.TestCase):
    """錯卦（陰陽全反）/綜卦（上下顛倒）——新增功能，期望值依易理。"""
    def _cuo_zong(self, upper, lower, dong=1):
        r = mc._analyze_hexagram(upper, lower, dong)
        return r["錯卦"]["名稱"], r["綜卦"]["名稱"]

    def test_qian_cuo_kun_zong_self(self):
        cuo, zong = self._cuo_zong(1, 1)         # 乾
        self.assertEqual(cuo, "坤為地")
        self.assertEqual(zong, "乾為天")          # 乾綜自身

    def test_yi_cuo_daguo_zong_self(self):
        cuo, zong = self._cuo_zong(7, 4)         # 頤(山雷)
        self.assertEqual(cuo, "澤風大過")
        self.assertEqual(zong, "山雷頤")          # 頤綜自身

    def test_zhun_zong_meng(self):
        # 水雷屯：上坎(6) 下震(4)。綜卦=山水蒙；錯卦=火風鼎
        cuo, zong = self._cuo_zong(6, 4)
        self.assertEqual(zong, "山水蒙")
        self.assertEqual(cuo, "火風鼎")

    def test_jiji_cuo_and_zong_both_weiji(self):
        # 既濟：上坎(6) 下離(3) = 010101。錯與綜皆為未濟
        cuo, zong = self._cuo_zong(6, 3)
        self.assertEqual(cuo, "火水未濟")
        self.assertEqual(zong, "火水未濟")


class TestAnalyzeHexagram(unittest.TestCase):
    def test_tiyong_assignment_by_moving_line(self):
        # 動爻在上卦(>3) → 下卦為體
        r = mc._analyze_hexagram(7, 4, 5)          # 上艮 下震，動5
        self.assertTrue(r["體用"]["體卦"].startswith("震"))
        self.assertTrue(r["體用"]["用卦"].startswith("艮"))
        # 動爻在下卦(<=3) → 上卦為體
        r2 = mc._analyze_hexagram(7, 4, 2)
        self.assertTrue(r2["體用"]["體卦"].startswith("艮"))

    def test_result_has_all_sections(self):
        r = mc._analyze_hexagram(7, 4, 5)
        for k in ("本卦", "體用", "互卦", "變卦", "錯卦", "綜卦"):
            self.assertIn(k, r)
        for k in ("生克關係", "卦德關係"):
            self.assertIn(k, r["體用"])

    def test_moving_line_structured_fields(self):
        # 重構後本卦應帶結構化動爻位/陰陽（供 print_result 直接使用，免字串還原）
        r = mc._analyze_hexagram(7, 4, 5)   # 頤 100001，第5爻 → binary[1]='0' → 陰
        ben = r["本卦"]
        self.assertEqual(ben["動爻位"], 5)
        self.assertEqual(ben["動爻陰陽"], "陰")


class TestQiguaEndToEnd(unittest.TestCase):
    def test_qigua_by_numbers_known(self):
        r = mc.qigua_by_numbers(7, 4, 11)        # 上艮 下震，動爻 (7+4+11)%6=4
        self.assertEqual(r["本卦"]["名稱"], "山雷頤")
        self.assertEqual(r["本卦"]["動爻"], "第4爻")
        self.assertEqual(r["變卦"]["名稱"], "火雷噬嗑")
        self.assertEqual(r["錯卦"]["名稱"], "澤風大過")

    def test_qigua_by_numbers_two_args_dong_from_sum(self):
        # 無第三數 → 動爻 = (num1+num2)%6
        r = mc.qigua_by_numbers(6, 8)            # (6+8)%6 = 2
        self.assertEqual(r["本卦"]["動爻"], "第2爻")

    def test_three_numbers_use_total_not_third(self):
        # 原書「總數除六」：三數起卦動爻取三數之和，非只取第三數。
        # 若退回只取 num3，(6,8,9) 會得第3爻而非第5爻——此斷言即為那道防線。
        r = mc.qigua_by_numbers(6, 8, 9)         # (6+8+9)=23, 23%6=5
        self.assertEqual(r["本卦"]["動爻"], "第5爻")
        self.assertIn("(6+8+9)", r["計算過程"]["動爻"])

    def test_numbers_with_date_add_wangshuai_but_not_change_the_hexagram(self):
        # 占時只定時令。若日期漏進起卦之數，本卦或動爻就會與無日期版本不同——
        # 這組斷言就是那道防線。旺衰是加出來的一節，不是換掉的一卦。
        plain = mc.qigua_by_numbers(6, 8, 9)
        dated = mc.qigua_by_numbers_at(2026, 1, 20, 14, 6, 8, 9)  # 農曆十二月・冬
        self.assertEqual(dated["本卦"], plain["本卦"])
        self.assertEqual(dated["變卦"], plain["變卦"])
        self.assertNotIn("卦氣旺衰", plain)
        self.assertEqual(dated["卦氣旺衰"]["時令"], "冬（水旺）")
        self.assertIn("不入起卦之數", dated["計算過程"]["占時"])

    def test_numbers_at_23h_takes_the_next_lunar_day(self):
        # 日始於子時：數字卦的占時也走同一條推日規則，否則同一時刻的時間卦與
        # 數字卦會落在不同農曆日、可能給出不同時令。
        r = mc.qigua_by_numbers_at(2026, 4, 17, 23, 1, 1)  # 農曆三月初一 23時 → 初二
        self.assertIn("農曆2026年3月2日", r["計算過程"]["占時"])
        self.assertIn("日始於子時", r["計算過程"]["占時"])

    def test_qigua_by_time_runs(self):
        r = mc.qigua_by_time(2026, 5, 4, 14)
        self.assertIn("本卦", r)
        self.assertIn("計算過程", r)

    def test_zishi_rolls_the_day_forward(self):
        # 原書「日始於子時」：23 時已入次日子時，日數必須取次日，否則
        # 23:30 與 22:30 會落在同一日數上，子時整段被歸錯天。
        early = mc.qigua_by_gregorian_time_precise(2024, 1, 18, 22, 30, 0)
        late = mc.qigua_by_gregorian_time_precise(2024, 1, 18, 23, 30, 0)
        self.assertEqual(early["計算過程"]["日數"], 8)
        self.assertEqual(late["計算過程"]["日數"], 9)
        self.assertIn("子時推日", late["計算過程"])
        self.assertNotIn("子時推日", early["計算過程"])
        self.assertIn("日始於子時", late["日期轉換"]["說明"])

    def test_zishi_rolls_into_a_leap_month(self):
        # 2023 閏二月：二月最後一天的子時應進入「閏二月初一」，不是三月初一。
        last = mc._month_days(mc.YEAR_INFOS[2023 - 1900], 2, False)
        self.assertEqual(mc.lunar_next_day(2023, 2, last, False), (2023, 2, 1, True))

    def test_qian_kun_hu_gua_comes_from_the_bian_gua(self):
        # 乾/坤六爻皆同，直接取互會得本卦自身（無所取象），原書規定改從變卦取互。
        qian = mc.qigua_by_numbers(1, 1, 1)      # 乾為天，動爻 (1+1+1)%6=3
        self.assertEqual(qian["本卦"]["名稱"], "乾為天")
        self.assertTrue(qian["互卦"]["取自變卦"])
        self.assertNotEqual(qian["互卦"]["名稱"], "乾為天")

        # 一般卦不受影響，仍從本卦取互。
        other = mc.qigua_by_numbers(7, 4, 11)
        self.assertFalse(other["互卦"]["取自變卦"])

    def test_qigua_by_gregorian_adds_conversion(self):
        r = mc.qigua_by_gregorian_time(2026, 6, 18, 14)
        self.assertIn("日期轉換", r)
        self.assertIn("本卦", r)

    def test_full_64x6_coverage_no_keyerror(self):
        for u in range(1, 9):
            for l in range(1, 9):
                for d in range(1, 7):
                    r = mc._analyze_hexagram(u, l, d)
                    self.assertNotEqual(r["錯卦"]["名稱"], "未知卦")
                    self.assertNotEqual(r["綜卦"]["名稱"], "未知卦")


class TestPreciseTimeCasting(unittest.TestCase):
    """秒精度起卦（今人擴充）——解決同一時辰同卦問題。"""

    def test_known_precise_value(self):
        # 農曆 2026/5/4 14:30:45 → 年數午(7)、時辰未(8)
        # 上=(7+5+4+8)=24%8→坤8；下=(24+30)=54%8→坎6；動=(54+45)=99%6=3
        r = mc.qigua_by_time_precise(2026, 5, 4, 14, 30, 45)
        self.assertEqual(r["本卦"]["名稱"], "地水師")
        self.assertEqual(r["本卦"]["動爻"], "第3爻")

    def test_deterministic(self):
        a = mc.qigua_by_time_precise(2026, 5, 4, 14, 30, 45)
        b = mc.qigua_by_time_precise(2026, 5, 4, 14, 30, 45)
        self.assertEqual(a["本卦"], b["本卦"])

    def test_second_changes_moving_line(self):
        # +1 秒 → 動爻 3→4（同一時辰、同一分鐘內也能區分）
        r45 = mc.qigua_by_time_precise(2026, 5, 4, 14, 30, 45)
        r46 = mc.qigua_by_time_precise(2026, 5, 4, 14, 30, 46)
        self.assertEqual(r45["本卦"]["動爻"], "第3爻")
        self.assertEqual(r46["本卦"]["動爻"], "第4爻")

    def test_minute_changes_lower_trigram(self):
        # 不同分鐘 → 下卦不同（同一時辰內本卦即不同）
        r30 = mc.qigua_by_time_precise(2026, 5, 4, 14, 30, 45)
        r31 = mc.qigua_by_time_precise(2026, 5, 4, 14, 31, 45)
        self.assertNotEqual(r30["本卦"]["名稱"], r31["本卦"]["名稱"])

    def test_gregorian_precise_adds_conversion(self):
        r = mc.qigua_by_gregorian_time_precise(2026, 6, 18, 14, 30, 45)
        self.assertIn("日期轉換", r)
        self.assertIn(":", r["日期轉換"]["西曆"])  # 含時分秒

    def test_same_shichen_canonical_collides_but_precise_does_not(self):
        # 證明問題與修復：同一時辰兩個時刻
        #   canonical（時辰精度）→ 完全相同（年月日時辰皆同）
        #   precise（秒精度）→ 整體卦象（本卦+動爻）不同
        # 註：mod 運算仍可能讓「本卦名稱」相同，故比較有意義的單位＝(本卦, 動爻)。
        c1 = mc.qigua_by_time(2026, 5, 4, 14)
        c2 = mc.qigua_by_time(2026, 5, 4, 14)
        self.assertEqual((c1["本卦"]["名稱"], c1["本卦"]["動爻"]),
                         (c2["本卦"]["名稱"], c2["本卦"]["動爻"]))
        p1 = mc.qigua_by_time_precise(2026, 5, 4, 14, 10, 0)
        p2 = mc.qigua_by_time_precise(2026, 5, 4, 14, 50, 30)
        self.assertNotEqual((p1["本卦"]["名稱"], p1["本卦"]["動爻"]),
                            (p2["本卦"]["名稱"], p2["本卦"]["動爻"]))


class TestYearDizhi(unittest.TestCase):
    def test_known_years(self):
        self.assertEqual(mc.get_year_dizhi(1900), (1, "子"))   # 庚子
        self.assertEqual(mc.get_year_dizhi(2020), (1, "子"))   # 庚子
        self.assertEqual(mc.get_year_dizhi(1901), (2, "丑"))


class TestYaoPositions(unittest.TestCase):
    """爻位盤：當位/得中/應/承乘。期望值依易理人工推定。

    用澤火革（兌上離下，binary 011101）：六爻自下而上＝
    初九陽·六二陰·九三陽·九四陽·九五陽·上六陰。
    這組關係正是當初解卦漏報、後來補進 script 的內容——
    測試鎖住「九四唯一失正、二五中正相應、陰乘陽偵測、動爻無應」這些判讀依據。
    """

    def setUp(self):
        self.yp = mc.analyze_yao_positions("011101", 1)  # 革，動初九
        self.lines = {ln["位"]: ln for ln in self.yp["六爻"]}

    def test_dangwei_only_fourth_line_fails(self):
        # 革六爻僅九四（陽居陰位）失正，其餘五爻得正——卦體甚正
        失正 = [i for i in range(1, 7) if self.lines[i]["當位"] == "失正"]
        self.assertEqual(失正, [4])

    def test_dezhong_is_two_and_five(self):
        self.assertEqual(self.lines[2]["得中"], "得中")
        self.assertEqual(self.lines[5]["得中"], "得中")
        self.assertEqual(self.lines[1]["得中"], "")

    def test_ying_requires_opposite_polarity(self):
        self.assertFalse(self.lines[1]["有應"])   # 初九↔九四 同陽，無應
        self.assertTrue(self.lines[2]["有應"])    # 六二↔九五 一陰一陽，有應
        self.assertTrue(self.lines[3]["有應"])    # 九三↔上六 有應

    def test_zhongzheng_xiangying_flag(self):
        # 二有應且二五皆得正 → 最強外援徵象
        self.assertTrue(self.yp["二五中正相應"])

    def test_chengcheng_detects_yin_over_yang(self):
        # 六二乘初九、上六乘九五 → 陰乘陽（柔凌剛）
        self.assertTrue(self.lines[2]["承乘"].startswith("陰乘陽"))
        self.assertTrue(self.lines[6]["承乘"].startswith("陰乘陽"))
        # 九三居六二之上 → 下陰承陽（柔承剛）。古法「乘」專指陰居陽上，
        # 反向並無「陽乘陰」一說，故此處用承不用乘。
        self.assertTrue(self.lines[3]["承乘"].startswith("下陰承陽"))

    def test_moving_line_summary_captures_isolation(self):
        # 動爻初九：得正卻無應、且上被六二陰乘——此刻勿動的結構依據
        s = self.yp["動爻摘要"]
        self.assertIn("初九", s)
        self.assertIn("得正", s)
        self.assertIn("無應", s)
        self.assertIn("陰乘", s)


if __name__ == "__main__":
    unittest.main(verbosity=2)


class TestWangShuai(unittest.TestCase):
    """卦氣旺衰：解卦流程第四步，過去只在 references 裡當表給 LLM 查，現改為計算。"""

    # references/yingqi-calc.md §3.1 的原表，順序＝旺相休囚死
    TABLE = {
        "春": ("木", "火", "水", "金", "土"),
        "夏": ("火", "土", "木", "水", "金"),
        "秋": ("金", "水", "土", "火", "木"),
        "冬": ("水", "木", "金", "土", "火"),
        "四季末": ("土", "金", "火", "木", "水"),
    }

    def test_matches_the_source_table(self):
        # 推導（當令旺／令生相／生令休／剋令囚／令剋死）必須逐格重現原表，
        # 否則旺衰就只是好聽的字，不是那份古法。
        for season, elements in self.TABLE.items():
            for element, want in zip(elements, ("旺", "相", "休", "囚", "死")):
                self.assertEqual(mc.analyze_wangshuai(element, season), want,
                                 f"{season}·{element}")

    def test_every_element_has_exactly_one_state_per_season(self):
        for season in self.TABLE:
            states = [mc.analyze_wangshuai(e, season) for e in ("木", "火", "土", "金", "水")]
            self.assertCountEqual(states, ["旺", "相", "休", "囚", "死"], season)

    def test_sijimo_is_the_last_18_days_of_months_3_6_9_12(self):
        # 四季末（土旺）是唯一讓坤艮當令的時令；漏了它，土就永遠不旺。
        for month in (3, 6, 9, 12):
            length = mc._month_days(mc.YEAR_INFOS[2024 - 1900], month, False)
            self.assertEqual(mc.get_season(2024, month, length), "四季末")
            self.assertNotEqual(mc.get_season(2024, month, length - 18), "四季末")
        self.assertEqual(mc.get_season(2024, 1, 15), "春")
        self.assertEqual(mc.get_season(2024, 5, 15), "夏")
        self.assertEqual(mc.get_season(2024, 8, 15), "秋")
        self.assertEqual(mc.get_season(2024, 11, 15), "冬")

    def test_time_cast_reports_it_and_number_cast_does_not(self):
        # 數字起卦無日期即無時令，該節從缺——不可用「現在」或預設值蒙混。
        timed = mc.qigua_by_gregorian_time_precise(2024, 4, 20, 14, 30, 0)
        self.assertIn("卦氣旺衰", timed)
        self.assertIn("時令", timed["卦氣旺衰"])
        self.assertIsInstance(timed["卦氣旺衰"]["體卦得令"], bool)
        self.assertNotIn("卦氣旺衰", mc.qigua_by_numbers(6, 8, 7))
