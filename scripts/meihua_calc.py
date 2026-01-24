#!/usr/bin/env python3
"""
梅花易數起卦計算工具
Meihua Yishu (Plum Blossom Numerology) Calculator

內建農曆轉換功能，無需外部依賴。
"""

from datetime import datetime, date
from typing import Tuple, Dict

# 農曆數據表 (1900-2099)
# 編碼格式：
# - bit 16: 閏月是否為大月（30天=1，29天=0）
# - bits 4-15: 各月是否為大月（倒序：bit 15=1月，bit 4=12月）
# - bits 0-3: 閏月月份（0表示無閏月，1-12表示閏幾月）
# 數據來源：中國天文台農曆曆譜
YEAR_INFOS = [
    # 1900-1909
    0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2,
    # 1910-1919
    0x04ae0, 0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, 0x0d6a0, 0x0ada2, 0x095b0, 0x14977,
    # 1920-1929
    0x04970, 0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, 0x02b60, 0x09570, 0x052f2, 0x04970,
    # 1930-1939
    0x06566, 0x0d4a0, 0x0ea50, 0x06e95, 0x05ad0, 0x02b60, 0x186e3, 0x092e0, 0x1c8d7, 0x0c950,
    # 1940-1949
    0x0d4a0, 0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0, 0x092d0, 0x0d2b2, 0x0a950, 0x0b557,
    # 1950-1959
    0x06ca0, 0x0b550, 0x15355, 0x04da0, 0x0a5d0, 0x14573, 0x052d0, 0x0a9a8, 0x0e950, 0x06aa0,
    # 1960-1969
    0x0aea6, 0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260, 0x0f263, 0x0d950, 0x05b57, 0x056a0,
    # 1970-1979
    0x096d0, 0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250, 0x0d558, 0x0b540, 0x0b5a0, 0x195a6,
    # 1980-1989
    0x095b0, 0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, 0x06d40, 0x0af46, 0x0ab60, 0x09570,
    # 1990-1999
    0x04af5, 0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, 0x05ac0, 0x0ab60, 0x096d5, 0x092e0,
    # 2000-2009
    0x0c960, 0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0, 0x0abb7, 0x025d0, 0x092d0, 0x0cab5,
    # 2010-2019
    0x0a950, 0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, 0x0a5b0, 0x15176, 0x052b0, 0x0a930,
    # 2020-2029
    0x07954, 0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, 0x0a4e0, 0x0d260, 0x0ea65, 0x0d530,
    # 2030-2039
    0x05aa0, 0x076a3, 0x096d0, 0x04afb, 0x04ad0, 0x0a4d0, 0x1d0b6, 0x0d250, 0x0d520, 0x0dd45,
    # 2040-2049
    0x0b5a0, 0x056d0, 0x055b2, 0x049b0, 0x0a577, 0x0a4b0, 0x0aa50, 0x1b255, 0x06d20, 0x0ada0,
    # 2050-2059
    0x14b63, 0x09370, 0x049f8, 0x04970, 0x064b0, 0x168a6, 0x0ea50, 0x06aa0, 0x1a6c4, 0x0aae0,
    # 2060-2069
    0x092e0, 0x0d2e3, 0x0c960, 0x0d557, 0x0d4a0, 0x0da50, 0x05d55, 0x056a0, 0x0a6d0, 0x055d4,
    # 2070-2079
    0x052d0, 0x0a9b8, 0x0a950, 0x0b4a0, 0x0b6a6, 0x0ad50, 0x055a0, 0x0aba4, 0x0a5b0, 0x052b0,
    # 2080-2089
    0x0b273, 0x06930, 0x07337, 0x06aa0, 0x0ad50, 0x14b55, 0x04b60, 0x0a570, 0x054e4, 0x0d160,
    # 2090-2099
    0x0e968, 0x0d520, 0x0daa0, 0x16aa6, 0x056d0, 0x04ae0, 0x0a9d4, 0x0a2d0, 0x0d150, 0x0f252,
]

# 農曆1900年正月初一對應的西曆日期
LUNAR_START_DATE = date(1900, 1, 31)

# 先天八卦數對應
BAGUA = {
    1: {"name": "乾", "symbol": "☰", "binary": "111", "element": "金", "family": "父"},
    2: {"name": "兌", "symbol": "☱", "binary": "011", "element": "金", "family": "少女"},
    3: {"name": "離", "symbol": "☲", "binary": "101", "element": "火", "family": "中女"},
    4: {"name": "震", "symbol": "☳", "binary": "001", "element": "木", "family": "長男"},
    5: {"name": "巽", "symbol": "☴", "binary": "110", "element": "木", "family": "長女"},
    6: {"name": "坎", "symbol": "☵", "binary": "010", "element": "水", "family": "中男"},
    7: {"name": "艮", "symbol": "☶", "binary": "100", "element": "土", "family": "少男"},
    8: {"name": "坤", "symbol": "☷", "binary": "000", "element": "土", "family": "母"},
}

# 六十四卦名稱
HEXAGRAMS = {
    (1, 1): (1, "乾為天"),    (1, 2): (10, "天澤履"),   (1, 3): (13, "天火同人"), (1, 4): (25, "天雷无妄"),
    (1, 5): (44, "天風姤"),   (1, 6): (6, "天水訟"),    (1, 7): (33, "天山遯"),   (1, 8): (12, "天地否"),
    (2, 1): (43, "澤天夬"),   (2, 2): (58, "兌為澤"),   (2, 3): (49, "澤火革"),   (2, 4): (17, "澤雷隨"),
    (2, 5): (28, "澤風大過"), (2, 6): (47, "澤水困"),   (2, 7): (31, "澤山咸"),   (2, 8): (45, "澤地萃"),
    (3, 1): (14, "火天大有"), (3, 2): (38, "火澤睽"),   (3, 3): (30, "離為火"),   (3, 4): (21, "火雷噬嗑"),
    (3, 5): (50, "火風鼎"),   (3, 6): (64, "火水未濟"), (3, 7): (56, "火山旅"),   (3, 8): (35, "火地晉"),
    (4, 1): (34, "雷天大壯"), (4, 2): (54, "雷澤歸妹"), (4, 3): (55, "雷火豐"),   (4, 4): (51, "震為雷"),
    (4, 5): (32, "雷風恆"),   (4, 6): (40, "雷水解"),   (4, 7): (62, "雷山小過"), (4, 8): (16, "雷地豫"),
    (5, 1): (9, "風天小畜"),  (5, 2): (61, "風澤中孚"), (5, 3): (37, "風火家人"), (5, 4): (42, "風雷益"),
    (5, 5): (57, "巽為風"),   (5, 6): (59, "風水渙"),   (5, 7): (53, "風山漸"),   (5, 8): (20, "風地觀"),
    (6, 1): (5, "水天需"),    (6, 2): (60, "水澤節"),   (6, 3): (63, "水火既濟"), (6, 4): (3, "水雷屯"),
    (6, 5): (48, "水風井"),   (6, 6): (29, "坎為水"),   (6, 7): (39, "水山蹇"),   (6, 8): (8, "水地比"),
    (7, 1): (26, "山天大畜"), (7, 2): (41, "山澤損"),   (7, 3): (22, "山火賁"),   (7, 4): (27, "山雷頤"),
    (7, 5): (18, "山風蠱"),   (7, 6): (4, "山水蒙"),    (7, 7): (52, "艮為山"),   (7, 8): (23, "山地剝"),
    (8, 1): (11, "地天泰"),   (8, 2): (19, "地澤臨"),   (8, 3): (36, "地火明夷"), (8, 4): (24, "地雷復"),
    (8, 5): (46, "地風升"),   (8, 6): (7, "地水師"),    (8, 7): (15, "地山謙"),   (8, 8): (2, "坤為地"),
}

# 時辰對照（子時為23:00-00:59）
SHICHEN = {
    0: (1, "子"), 1: (2, "丑"), 2: (2, "丑"), 3: (3, "寅"), 4: (3, "寅"), 5: (4, "卯"),
    6: (4, "卯"), 7: (5, "辰"), 8: (5, "辰"), 9: (6, "巳"), 10: (6, "巳"), 11: (7, "午"),
    12: (7, "午"), 13: (8, "未"), 14: (8, "未"), 15: (9, "申"), 16: (9, "申"), 17: (10, "酉"),
    18: (10, "酉"), 19: (11, "戌"), 20: (11, "戌"), 21: (12, "亥"), 22: (12, "亥"), 23: (1, "子"),
}

# 二進位 → 卦數 反查表
BINARY_TO_GUA = {info["binary"]: num for num, info in BAGUA.items()}


def _year_days(year_info: int) -> int:
    """計算農曆年的總天數"""
    # 基礎天數: 12個月 × 29天
    days = 29 * 12
    # 如果有閏月，加29天
    leap_month = year_info & 0xF
    if leap_month:
        days += 29
        # 閏月是否為大月由 bit 16 決定
        if (year_info >> 16) & 1:
            days += 1
    # 檢查 12 個正常月份是否為大月（30天）
    # bits 4-15 對應月份 12-1（倒序）
    for month in range(1, 13):
        if (year_info >> (16 - month)) & 1:
            days += 1
    return days


def _month_days(year_info: int, month: int, is_leap: bool = False) -> int:
    """計算農曆某月的天數"""
    if is_leap:
        # 閏月天數由 bit 16 決定
        return 30 if (year_info >> 16) & 1 else 29

    # 正常月份天數由 bits 4-15 決定（月份1對應bit 15，月份12對應bit 4，倒序）
    return 30 if (year_info >> (16 - month)) & 1 else 29


def gregorian_to_lunar(year: int, month: int, day: int) -> Tuple[int, int, int, bool]:
    """
    將西曆日期轉換為農曆日期

    Args:
        year: 西曆年份 (1900-2099)
        month: 西曆月份
        day: 西曆日期

    Returns:
        Tuple[int, int, int, bool]: (農曆年, 農曆月, 農曆日, 是否閏月)
    """
    if year < 1900 or year > 2099:
        raise ValueError(f"年份 {year} 超出支援範圍 (1900-2099)")

    target_date = date(year, month, day)
    offset = (target_date - LUNAR_START_DATE).days

    if offset < 0:
        raise ValueError("日期早於1900年1月31日")

    # 逐年計算
    lunar_year = 1900
    year_index = 0

    while year_index < len(YEAR_INFOS):
        year_info = YEAR_INFOS[year_index]
        year_days = _year_days(year_info)

        if offset < year_days:
            break
        offset -= year_days
        lunar_year += 1
        year_index += 1

    if year_index >= len(YEAR_INFOS):
        raise ValueError("日期超出支援範圍")

    # 逐月計算
    year_info = YEAR_INFOS[year_index]
    leap_month = year_info & 0xF

    for m in range(1, 13):
        # 正常月份
        days = _month_days(year_info, m, False)
        if offset < days:
            return (lunar_year, m, offset + 1, False)
        offset -= days

        # 閏月（如果該月有閏月）
        if m == leap_month:
            days = _month_days(year_info, m, True)
            if offset < days:
                return (lunar_year, m, offset + 1, True)
            offset -= days

    # 不應該到達這裡
    raise ValueError("日期計算錯誤")


# 地支名稱對照
DIZHI = {
    1: "子", 2: "丑", 3: "寅", 4: "卯", 5: "辰", 6: "巳",
    7: "午", 8: "未", 9: "申", 10: "酉", 11: "戌", 12: "亥"
}


def get_year_dizhi(lunar_year: int) -> Tuple[int, str]:
    """
    獲取農曆年的地支數和名稱

    根據梅花易數原典，年數使用地支序數（1-12）
    1900年為庚子年，地支為子(1)
    """
    # 1900年是庚子年，地支為子(1)
    dizhi_num = ((lunar_year - 1900) % 12) + 1
    if dizhi_num == 13:  # 處理邊界情況
        dizhi_num = 1
    return dizhi_num, DIZHI[dizhi_num]


def get_shichen(hour: int) -> Tuple[int, str]:
    """獲取時辰數和名稱"""
    return SHICHEN[hour]


def num_to_gua(n: int) -> int:
    """數字轉卦數（餘0當8）"""
    remainder = n % 8
    return 8 if remainder == 0 else remainder


def num_to_yao(n: int) -> int:
    """數字轉動爻數（餘0當6）"""
    remainder = n % 6
    return 6 if remainder == 0 else remainder


def get_hexagram_binary(upper: int, lower: int) -> str:
    """獲取六爻二進位表示"""
    return BAGUA[upper]["binary"] + BAGUA[lower]["binary"]


def apply_change(binary: str, yao_position: int) -> str:
    """應用動爻變化（從下往上數，1-6）"""
    index = 6 - yao_position
    bit_list = list(binary)
    bit_list[index] = "0" if bit_list[index] == "1" else "1"
    return "".join(bit_list)


def binary_to_gua_pair(binary: str) -> Tuple[int, int]:
    """二進位轉上下卦數"""
    return BINARY_TO_GUA[binary[:3]], BINARY_TO_GUA[binary[3:]]


def get_hu_gua(binary: str) -> Tuple[int, int]:
    """計算互卦（取2-4爻為下互，3-5爻為上互）"""
    return BINARY_TO_GUA[binary[1:4]], BINARY_TO_GUA[binary[2:5]]


def analyze_wuxing(ti_element: str, yong_element: str) -> str:
    """分析體用五行生克關係"""
    sheng = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
    ke = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}

    if ti_element == yong_element:
        return "比和（吉）"
    elif sheng.get(yong_element) == ti_element:
        return "用生體（大吉）"
    elif sheng.get(ti_element) == yong_element:
        return "體生用（耗洩）"
    elif ke.get(ti_element) == yong_element:
        return "體克用（吉）"
    elif ke.get(yong_element) == ti_element:
        return "用克體（凶）"
    return "未知關係"


def _analyze_hexagram(upper_gua: int, lower_gua: int, dong_yao: int) -> Dict:
    """分析卦象（本卦、體用、互卦、變卦）"""
    hexagram_binary = get_hexagram_binary(upper_gua, lower_gua)
    hexagram_info = HEXAGRAMS.get((upper_gua, lower_gua), (0, "未知卦"))

    # 體用分析：動爻在上卦則下卦為體，動爻在下卦則上卦為體
    if dong_yao > 3:
        ti_gua, yong_gua = lower_gua, upper_gua
        ti_pos, yong_pos = "下卦", "上卦"
    else:
        ti_gua, yong_gua = upper_gua, lower_gua
        ti_pos, yong_pos = "上卦", "下卦"

    # 變卦
    bian_binary = apply_change(hexagram_binary, dong_yao)
    bian_upper, bian_lower = binary_to_gua_pair(bian_binary)
    bian_info = HEXAGRAMS.get((bian_upper, bian_lower), (0, "未知卦"))

    # 互卦
    hu_upper, hu_lower = get_hu_gua(hexagram_binary)
    hu_info = HEXAGRAMS.get((hu_upper, hu_lower), (0, "未知卦"))

    # 五行生克
    ti_element = BAGUA[ti_gua]["element"]
    yong_element = BAGUA[yong_gua]["element"]

    return {
        "本卦": {
            "序號": hexagram_info[0],
            "名稱": hexagram_info[1],
            "上卦": f"{BAGUA[upper_gua]['name']} {BAGUA[upper_gua]['symbol']}",
            "下卦": f"{BAGUA[lower_gua]['name']} {BAGUA[lower_gua]['symbol']}",
            "二進位": hexagram_binary,
            "動爻": f"第{dong_yao}爻",
        },
        "體用": {
            "體卦": f"{BAGUA[ti_gua]['name']}（{ti_pos}）- {ti_element}",
            "用卦": f"{BAGUA[yong_gua]['name']}（{yong_pos}）- {yong_element}",
            "生克關係": analyze_wuxing(ti_element, yong_element),
        },
        "互卦": {
            "名稱": hu_info[1],
            "上互": BAGUA[hu_upper]['name'],
            "下互": BAGUA[hu_lower]['name'],
        },
        "變卦": {
            "序號": bian_info[0],
            "名稱": bian_info[1],
            "二進位": bian_binary,
        },
    }


def qigua_by_time(year: int, month: int, day: int, hour: int) -> Dict:
    """以農曆時間起卦"""
    year_num, year_dizhi = get_year_dizhi(year)
    shichen_num, shichen_name = get_shichen(hour)

    upper_sum = year_num + month + day
    lower_sum = upper_sum + shichen_num

    upper_gua = num_to_gua(upper_sum)
    lower_gua = num_to_gua(lower_sum)
    dong_yao = num_to_yao(lower_sum)

    result = _analyze_hexagram(upper_gua, lower_gua, dong_yao)
    result["計算過程"] = {
        "年數": f"{year_dizhi}年 ({year_num})",
        "月數": month,
        "日數": day,
        "時辰": f"{shichen_name}時 ({shichen_num})",
        "上卦數": f"{upper_sum} mod 8 = {upper_gua}",
        "下卦數": f"{lower_sum} mod 8 = {lower_gua}",
        "動爻數": f"{lower_sum} mod 6 = {dong_yao}",
    }
    return result


def qigua_by_gregorian_time(year: int, month: int, day: int, hour: int) -> Dict:
    """以西曆時間起卦（自動轉換為農曆）"""
    lunar_year, lunar_month, lunar_day, is_leap = gregorian_to_lunar(year, month, day)
    result = qigua_by_time(lunar_year, lunar_month, lunar_day, hour)

    result["日期轉換"] = {
        "西曆": f"{year}年{month}月{day}日",
        "農曆": f"{lunar_year}年{'閏' if is_leap else ''}{lunar_month}月{lunar_day}日",
        "說明": "梅花易數使用農曆計算"
    }
    return result


def qigua_by_numbers(num1: int, num2: int, num3: int = None) -> Dict:
    """以數字起卦"""
    upper_gua = num_to_gua(num1)
    lower_gua = num_to_gua(num2)
    dong_yao = num_to_yao(num3) if num3 is not None else num_to_yao(num1 + num2)

    result = _analyze_hexagram(upper_gua, lower_gua, dong_yao)
    result["計算過程"] = {
        "第一數": f"{num1} → {num1} mod 8 = {upper_gua} → {BAGUA[upper_gua]['name']}",
        "第二數": f"{num2} → {num2} mod 8 = {lower_gua} → {BAGUA[lower_gua]['name']}",
        "動爻": f"({num1}+{num2}) mod 6 = {dong_yao}" if num3 is None else f"{num3} mod 6 = {dong_yao}",
    }
    return result


# ==============================================================================
# 統計輔助功能 (Statistical Helpers)
# 根據 384 爻數據分析添加，不影響起卦邏輯
# ==============================================================================

# 爻位係數（Position Coefficients）
POSITION_COEFFICIENTS = {
    5: 0.422,   # ★★ 最佳（九五之尊）
    2: 0.344,   # ★ 佳（得中）
    4: 0.266,   # 中
    1: 0.234,   # 中
    6: 0.031,   # 差
    3: -0.219,  # ✗✗ 最差（三多凶）
}

# 爻位 × 陰陽係數
POSITION_YINYANG_COEFFICIENTS = {
    # (position, is_yang): coefficient
    (1, True): 0.281, (1, False): 0.188,
    (2, True): 0.312, (2, False): 0.375,
    (3, True): -0.375, (3, False): -0.062,  # 三位陽爻最凶!
    (4, True): 0.281, (4, False): 0.250,
    (5, True): 0.344, (5, False): 0.500,
    (6, True): 0.000, (6, False): 0.062,
}

# 64卦策略分類
# 類型: 吸引子(留), 排斥子(走), 福地(守), 困境(變), 陷阱(慎), 一般(觀)
HEXAGRAM_STRATEGY = {
    1: ("排斥子", "走", 0, "乾 → 履（變4爻得50%）"),
    2: ("一般", "觀", 33, "坤 → 謙（變4爻得83%）"),
    3: ("一般", "觀", 33, "屯 → 比（變6爻得67%）"),
    4: ("一般", "觀", 33, "蒙 → 損（變6爻得50%）"),
    5: ("吸引子", "留", 67, None),
    6: ("吸引子", "留", 67, None),
    7: ("排斥子", "走", 17, "師 → 臨（變6爻得83%）"),
    8: ("吸引子", "留", 67, None),
    9: ("一般", "觀", 33, "小畜 → 家人（變5爻得67%）"),
    10: ("福地", "守", 50, None),
    11: ("一般", "觀", 33, "泰 → 臨（變4爻得83%）"),
    12: ("福地", "守", 50, None),
    13: ("排斥子", "走", 17, "同人 → 遯（變6爻得67%）"),
    14: ("一般", "觀", 33, "大有 → 鼎（變6爻得67%）"),
    15: ("吸引子", "留", 83, None),  # 謙卦 - 唯一全吉卦
    16: ("困境", "變", 17, "豫 → 晉（變1爻得67%）"),
    17: ("一般", "觀", 33, "隨 → 萃（變6爻得50%）"),
    18: ("排斥子", "走", 17, "蠱 → 鼎（變3爻得67%）"),
    19: ("吸引子", "留", 83, None),  # 臨卦 - 關鍵轉折點
    20: ("排斥子", "走", 0, "觀 → 比（變1爻得67%）"),
    21: ("排斥子", "走", 17, "噬嗑 → 晉（變6爻得67%）"),
    22: ("一般", "觀", 33, "賁 → 家人（變2爻得67%）"),
    23: ("困境", "變", 17, "剝 → 晉（變3爻得67%）"),
    24: ("一般", "觀", 33, "復 → 臨（變5爻得83%）"),
    25: ("一般", "觀", 33, "无妄 → 否（變6爻得50%）"),
    26: ("福地", "守", 50, None),
    27: ("福地", "守", 50, None),
    28: ("一般", "觀", 33, "大過 → 夬 → 革"),
    29: ("排斥子", "走", 0, "坎 → 比（變5爻得67%）"),
    30: ("一般", "觀", 33, "離 → 豐（變1爻得50%）"),
    31: ("困境", "變", 17, "咸 → 遯（變1爻得67%）"),
    32: ("排斥子", "走", 0, "恆 → 升（變3爻得67%）"),
    33: ("吸引子", "留", 67, None),
    34: ("吸引子", "留", 50, None),
    35: ("吸引子", "留", 67, None),
    36: ("排斥子", "走", 17, "明夷 → 謙（變6爻得83%）"),
    37: ("吸引子", "留", 67, None),
    38: ("一般", "觀", 33, "睽 → 未濟（變6爻得50%）"),
    39: ("排斥子", "走", 17, "蹇 → 謙（變2爻得83%）"),
    40: ("吸引子", "留", 50, None),
    41: ("福地", "守", 50, None),
    42: ("福地", "守", 50, None),
    43: ("排斥子", "走", 0, "夬 → 需（變3爻得67%）"),
    44: ("排斥子", "走", 17, "姤 → 遯（變5爻得67%）"),
    45: ("福地", "守", 50, None),
    46: ("吸引子", "留", 67, None),
    47: ("排斥子", "走", 17, "困 → 訟（變1爻得67%）"),
    48: ("困境", "變", 17, "井 → 需（變6爻得67%）"),
    49: ("吸引子", "留", 50, None),
    50: ("吸引子", "留", 67, None),
    51: ("陷阱", "慎", 17, "震 → 豐（變4爻得50%）"),
    52: ("一般", "觀", 33, "艮 → 謙（變1爻得83%）"),
    53: ("福地", "守", 50, None),
    54: ("一般", "觀", 33, "歸妹 → 臨（變3爻得83%）"),
    55: ("吸引子", "留", 50, None),
    56: ("排斥子", "走", 0, "旅 → 鼎（變5爻得67%）"),
    57: ("一般", "觀", 33, "巽 → 漸（變5爻得50%）"),
    58: ("吸引子", "留", 50, None),
    59: ("一般", "觀", 33, "渙 → 訟（變3爻得67%）"),
    60: ("排斥子", "走", 17, "節 → 臨（變2爻得83%）"),
    61: ("排斥子", "走", 17, "中孚 → 益（變5爻得50%）"),
    62: ("排斥子", "走", 0, "小過 → 謙（變3爻得83%）"),
    63: ("排斥子", "走", 0, "既濟 → 需（變5爻得67%）"),
    64: ("福地", "守", 50, None),
}


def get_position_risk(position: int, is_yang: bool = True) -> dict:
    """
    獲取爻位風險評估

    Args:
        position: 動爻位置 (1-6)
        is_yang: 動爻是否為陽爻

    Returns:
        dict: {
            'coefficient': 係數,
            'risk_level': 風險等級,
            'warning': 警告信息（若有）
        }
    """
    coef = POSITION_YINYANG_COEFFICIENTS.get((position, is_yang), 0)

    if position == 3 and is_yang:
        return {
            'coefficient': coef,
            'risk_level': '高風險',
            'warning': '⚠️ 三位陽爻是全表最凶的組合（-0.375）'
        }
    elif position == 5:
        return {
            'coefficient': coef,
            'risk_level': '最佳',
            'warning': None
        }
    elif position == 2:
        return {
            'coefficient': coef,
            'risk_level': '佳',
            'warning': None
        }
    elif coef < 0:
        return {
            'coefficient': coef,
            'risk_level': '較差',
            'warning': f'⚠️ 爻位係數為負值 ({coef:.3f})'
        }
    else:
        return {
            'coefficient': coef,
            'risk_level': '中等',
            'warning': None
        }


def get_hexagram_strategy(hex_num: int) -> dict:
    """
    獲取卦的策略建議

    Args:
        hex_num: 卦序 (1-64)

    Returns:
        dict: {
            'type': 類型（吸引子/排斥子/福地/困境/陷阱/一般）,
            'advice': 建議（留/走/守/變/慎/觀）,
            'ji_rate': 吉率百分比,
            'change_path': 推薦變卦路徑（若有）
        }
    """
    if hex_num not in HEXAGRAM_STRATEGY:
        return None

    type_, advice, ji_rate, change_path = HEXAGRAM_STRATEGY[hex_num]
    return {
        'type': type_,
        'advice': advice,
        'ji_rate': ji_rate,
        'change_path': change_path
    }


def print_strategy_advice(hex_num: int):
    """打印卦的策略建議"""
    strategy = get_hexagram_strategy(hex_num)
    if not strategy:
        return

    print(f"\n【策略建議】")
    print(f"  類型：{strategy['type']}")
    print(f"  建議：{strategy['advice']}")
    print(f"  吉率：{strategy['ji_rate']}%")
    if strategy['change_path']:
        print(f"  變卦路徑：{strategy['change_path']}")


def print_result(result: Dict):
    """格式化輸出結果"""
    print("\n" + "=" * 50)
    print("📿 梅花易數起卦結果")
    print("=" * 50)

    if "日期轉換" in result:
        print("\n【日期轉換】")
        conv = result["日期轉換"]
        print(f"  {conv['西曆']} → {conv['農曆']}")

    print("\n【一、起卦計算】")
    for key, value in result["計算過程"].items():
        print(f"  {key}：{value}")

    print("\n【二、本卦】")
    ben = result["本卦"]
    print(f"  第 {ben['序號']} 卦：{ben['名稱']}")
    print(f"  上卦：{ben['上卦']}")
    print(f"  下卦：{ben['下卦']}")
    print(f"  二進位：{ben['二進位']}")
    print(f"  {ben['動爻']}動")

    print("\n【三、體用分析】")
    ty = result["體用"]
    print(f"  體卦：{ty['體卦']}")
    print(f"  用卦：{ty['用卦']}")
    print(f"  生克：{ty['生克關係']}")

    print("\n【四、互卦】")
    hu = result["互卦"]
    print(f"  {hu['名稱']}（上{hu['上互']}下{hu['下互']}）")

    print("\n【五、變卦】")
    bian = result["變卦"]
    print(f"  第 {bian['序號']} 卦：{bian['名稱']}")
    print(f"  二進位：{bian['二進位']}")

    # 添加策略建議
    hex_num = ben['序號']
    if hex_num in HEXAGRAM_STRATEGY:
        print_strategy_advice(hex_num)

        # 檢查動爻位置風險
        dong_yao_str = ben['動爻']
        dong_yao = int(dong_yao_str.replace('第', '').replace('爻', ''))
        is_yang = ben['二進位'][6 - dong_yao] == '1'
        risk = get_position_risk(dong_yao, is_yang)
        if risk['warning']:
            print(f"\n【動爻風險提醒】")
            print(f"  {risk['warning']}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "time":
            now = datetime.now()
            result = qigua_by_gregorian_time(now.year, now.month, now.day, now.hour)
            print(f"\n起卦時間：{now.strftime('%Y年%m月%d日 %H:%M')}（西曆）")
        elif sys.argv[1] == "lunar" and len(sys.argv) >= 5:
            year = int(sys.argv[2])
            month = int(sys.argv[3])
            day = int(sys.argv[4])
            hour = int(sys.argv[5]) if len(sys.argv) > 5 else datetime.now().hour
            result = qigua_by_time(year, month, day, hour)
            print(f"\n起卦時間：農曆 {year}年{month}月{day}日 {hour}時")
        elif sys.argv[1] == "gregorian" and len(sys.argv) >= 5:
            year = int(sys.argv[2])
            month = int(sys.argv[3])
            day = int(sys.argv[4])
            hour = int(sys.argv[5]) if len(sys.argv) > 5 else datetime.now().hour
            result = qigua_by_gregorian_time(year, month, day, hour)
            print(f"\n起卦時間：西曆 {year}年{month}月{day}日 {hour}時")
        elif sys.argv[1] == "num" and len(sys.argv) >= 4:
            num1 = int(sys.argv[2])
            num2 = int(sys.argv[3])
            num3 = int(sys.argv[4]) if len(sys.argv) > 4 else None
            result = qigua_by_numbers(num1, num2, num3)
        elif sys.argv[1] == "convert" and len(sys.argv) >= 5:
            year = int(sys.argv[2])
            month = int(sys.argv[3])
            day = int(sys.argv[4])
            lunar_year, lunar_month, lunar_day, is_leap = gregorian_to_lunar(year, month, day)
            print(f"西曆: {year}年{month}月{day}日")
            print(f"農曆: {lunar_year}年{'閏' if is_leap else ''}{lunar_month}月{lunar_day}日")
            sys.exit(0)
        else:
            print("用法：")
            print("  python meihua_calc.py time                     # 以當前時間起卦")
            print("  python meihua_calc.py gregorian 2024 1 18 14   # 以西曆日期起卦")
            print("  python meihua_calc.py lunar 2024 12 8 14       # 以農曆日期起卦")
            print("  python meihua_calc.py num 6 8 9                # 以數字起卦")
            print("  python meihua_calc.py convert 2024 1 18        # 僅轉換日期")
            sys.exit(1)
    else:
        now = datetime.now()
        result = qigua_by_gregorian_time(now.year, now.month, now.day, now.hour)
        print(f"\n起卦時間：{now.strftime('%Y年%m月%d日 %H:%M')}（西曆）")

    print_result(result)
