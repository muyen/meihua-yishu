#!/usr/bin/env python3
"""
梅花易數起卦計算工具
Meihua Yishu (Plum Blossom Numerology) Calculator

內建農曆轉換功能，無需外部依賴。
"""

from datetime import datetime, date
from typing import Tuple, Dict, Optional

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
# "de" = 卦德（說卦傳第七章）：易經原始的八卦屬性，與五行並列作為「參考透鏡」。
BAGUA = {
    1: {"name": "乾", "symbol": "☰", "binary": "111", "element": "金", "family": "父",   "de": "健"},
    2: {"name": "兌", "symbol": "☱", "binary": "011", "element": "金", "family": "少女", "de": "說"},
    3: {"name": "離", "symbol": "☲", "binary": "101", "element": "火", "family": "中女", "de": "麗"},
    4: {"name": "震", "symbol": "☳", "binary": "001", "element": "木", "family": "長男", "de": "動"},
    5: {"name": "巽", "symbol": "☴", "binary": "110", "element": "木", "family": "長女", "de": "入"},
    6: {"name": "坎", "symbol": "☵", "binary": "010", "element": "水", "family": "中男", "de": "陷"},
    7: {"name": "艮", "symbol": "☶", "binary": "100", "element": "土", "family": "少男", "de": "止"},
    8: {"name": "坤", "symbol": "☷", "binary": "000", "element": "土", "family": "母",   "de": "順"},
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
    # 1900年是庚子年，地支為子(1)。(% 12) + 1 恆落在 1-12。
    dizhi_num = ((lunar_year - 1900) % 12) + 1
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


def lunar_next_day(year: int, month: int, day: int,
                   is_leap: bool = False) -> Tuple[int, int, int, bool]:
    """農曆日期加一天，正確處理月長與閏月轉入。

    子時起卦需要它：原書「日始於子時」，23 時的卦屬次日。
    """
    index = year - 1900
    if not 0 <= index < len(YEAR_INFOS):
        # 超出曆表範圍：僅遞增日數，讓餘數計算仍可進行
        return year, month, day + 1, is_leap

    year_info = YEAR_INFOS[index]
    if day < _month_days(year_info, month, is_leap):
        return year, month, day + 1, is_leap
    # 月末：若本月為正月份且該月有閏，次日進入閏月
    if not is_leap and month == (year_info & 0xF):
        return year, month, 1, True
    if month < 12:
        return year, month + 1, 1, False
    return year + 1, 1, 1, False


def get_cuo_gua(binary: str) -> Tuple[int, int]:
    """計算錯卦（陰陽全反：六爻每位翻轉）→ 上下卦數"""
    flipped = "".join("0" if b == "1" else "1" for b in binary)
    return binary_to_gua_pair(flipped)


def get_zong_gua(binary: str) -> Tuple[int, int]:
    """計算綜卦（上下顛倒：整卦翻轉）→ 上下卦數"""
    return binary_to_gua_pair(binary[::-1])


# 五行相生相剋（模組層級，供生剋與旺衰共用一份真相）
WUXING_SHENG = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
WUXING_KE = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}

# 時令當旺之五行（references/yingqi-calc.md §3.1）
SEASON_ELEMENT = {"春": "木", "夏": "火", "秋": "金", "冬": "水", "四季末": "土"}

_MONTH_SEASON = {1: "春", 2: "春", 3: "春", 4: "夏", 5: "夏", 6: "夏",
                 7: "秋", 8: "秋", 9: "秋", 10: "冬", 11: "冬", 12: "冬"}


def get_season(year: int, month: int, day: int, is_leap: bool = False) -> str:
    """由農曆月日定時令。

    四季末（土旺）＝農曆三、六、九、十二月的最後18天；其餘依月份分四季。
    """
    if month in (3, 6, 9, 12):
        index = year - 1900
        length = (_month_days(YEAR_INFOS[index], month, is_leap)
                  if 0 <= index < len(YEAR_INFOS) else 30)
        if day > length - 18:
            return "四季末"
    return _MONTH_SEASON[month]


def analyze_wangshuai(element: str, season: str) -> str:
    """某五行在該時令的旺相休囚死。

    純推導，不查表：當令者旺、令生者相、生令者休、剋令者囚、令剋者死。
    """
    se = SEASON_ELEMENT[season]
    if element == se:
        return "旺"
    if WUXING_SHENG[se] == element:
        return "相"
    if WUXING_SHENG[element] == se:
        return "休"
    if WUXING_KE[element] == se:
        return "囚"
    if WUXING_KE[se] == element:
        return "死"
    return "未知"


def analyze_wuxing(ti_element: str, yong_element: str) -> str:
    """分析體用五行生克關係"""
    sheng = WUXING_SHENG
    ke = WUXING_KE

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


# 卦德的「意向」——用象的關係語言描述，不下吉凶判決。
# 「你（體）傾向…，處境（用）正在…」——讓占者自己在脈絡中讀。
GUADE_INTENT = {
    "健": "剛健主導、進取不息",
    "說": "和悅交流、取悅外應",
    "麗": "附麗顯明、依託而光",
    "動": "起而行動、振奮求變",
    "入": "漸進順入、謙伏滲透",
    "陷": "涉險應變、勞心趨流",
    "止": "靜止守成、止於其所",
    "順": "柔順承載、包容隨順",
}
# 少數最鮮明的對極，給一句脈絡提示；其餘走通則。皆為描述，非吉凶。
_GUADE_POLAR = {
    frozenset({"健", "順"}): "一剛一柔：主導與承載之間，看你要推進還是承接",
    frozenset({"動", "止"}): "一動一靜：進與守的拉扯，急動或久守都不易",
    frozenset({"陷", "麗"}): "一陷一明：身處險而前方有明，關鍵在能否脫險見光",
    frozenset({"說", "入"}): "一悅一巽：外和而內順，宜柔不宜剛",
}


def analyze_guade(ti_gua: int, yong_gua: int) -> str:
    """以卦德交互給出『象的關係』描述（互補於五行生剋，皆為參考透鏡，非判決）。"""
    ti_de, yong_de = BAGUA[ti_gua]["de"], BAGUA[yong_gua]["de"]
    head = (f"你（體・{BAGUA[ti_gua]['name']}）傾向「{GUADE_INTENT[ti_de]}」，"
            f"處境（用・{BAGUA[yong_gua]['name']}）正在「{GUADE_INTENT[yong_de]}」")
    if ti_de == yong_de:
        note = "同德相應，內外方向一致，順勢即可"
    else:
        note = _GUADE_POLAR.get(frozenset({ti_de, yong_de}),
                                "兩股力性質不同，端看你如何在其間取捨")
    return f"{head}。{note}（{ti_de}遇{yong_de}）"


def _yao_name(position: int, is_yang: bool) -> str:
    """爻的傳統名稱，如 初九、六二、九五、上六。"""
    yinyang = "九" if is_yang else "六"
    if position == 1:
        return "初" + yinyang
    if position == 6:
        return "上" + yinyang
    return yinyang + {2: "二", 3: "三", 4: "四", 5: "五"}[position]


def analyze_yao_positions(binary: str, dong_yao: int) -> Dict:
    """結構性爻位盤：六爻當位(得正)/得中/應(對爻)/承乘。

    純結構決定性分析（非文本統計），每次起卦必出。
    binary 為頂到底字串：index0=第6爻(上)，index5=第1爻(初)。

    ※ 出處說明：當位/得中/相應/承乘出自《周易》義理（彖象傳一路的爻位學），
    《梅花易數》原書並不使用。本專案有意加掛這一層作為結構性補充——它是後加的
    透鏡，不是邵雍原法；錯卦/綜卦同理（屬卦變之學）。勿當作原書步驟引述。
    """
    is_yang = {i: binary[6 - i] == "1" for i in range(1, 7)}

    lines = []
    for i in range(1, 7):
        yang = is_yang[i]
        # 當位（得正）：陽居奇位、陰居偶位
        dangwei = (yang and i % 2 == 1) or (not yang and i % 2 == 0)
        # 應（對爻）：初四、二五、三上，一陰一陽為有應
        partner = i + 3 if i <= 3 else i - 3
        lines.append({
            "位": i,
            "名稱": _yao_name(i, yang),
            "陰陽": "陽" if yang else "陰",
            "當位": "得正" if dangwei else "失正",
            "得中": "得中" if i in (2, 5) else "",
            "應位": partner,
            "應爻名稱": _yao_name(partner, is_yang[partner]),
            "有應": is_yang[i] != is_yang[partner],
        })

    # 承乘：相鄰兩爻，標記兩極。標於上爻。
    # 古法「乘」只用於陰居陽上（柔乘剛），故陰乘陽為本名；反之陽居陰上，其古名
    # 是下方之陰「承」上方之陽（陰承陽），並無「陽乘陰」一詞——舊版自創該詞，已改。
    # 標記掛在上爻，故以「下陰承陽」點明是下爻在承。
    chengcheng = {}
    for i in range(2, 7):
        if not is_yang[i] and is_yang[i - 1]:
            chengcheng[i] = "陰乘陽（柔凌剛·最不穩）"
        elif is_yang[i] and not is_yang[i - 1]:
            chengcheng[i] = "下陰承陽（柔承剛·最順）"
    for ln in lines:
        ln["承乘"] = chengcheng.get(ln["位"], "")

    # 二五中正相應：二有應且二五皆得正——最強外援徵象
    er, wu = lines[1], lines[4]
    zhongzheng = er["有應"] and er["當位"] == "得正" and wu["當位"] == "得正"

    # 動爻處境摘要
    d = lines[dong_yao - 1]
    parts = [d["當位"]]
    parts.append("有應" if d["有應"] else f"無應(↔{d['應爻名稱']}同性)")
    if d["承乘"]:
        parts.append(d["承乘"])
    # 動爻是否被上爻陰乘（柔凌剛壓於其上）
    if dong_yao < 6 and chengcheng.get(dong_yao + 1, "").startswith("陰乘陽"):
        parts.append(f"上被{lines[dong_yao]['名稱']}陰乘")
    dong_summary = f"{d['名稱']}（動）：" + "·".join(parts)

    return {
        "六爻": lines,
        "二五中正相應": zhongzheng,
        "動爻摘要": dong_summary,
    }


def _analyze_hexagram(upper_gua: int, lower_gua: int, dong_yao: int,
                      season: Optional[str] = None) -> Dict:
    """分析卦象（本卦、體用、互卦、變卦）。

    season 為時令（見 get_season）；有時令才輸出【卦氣旺衰】。數字起卦無日期，
    故無時令可據，該節從缺——不猜。
    """
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

    # 互卦。乾為天（六陽）、坤為地（六陰）六爻皆同，互卦得本卦自身，無所取象；
    # 原書因此規定此二卦改從變卦取互。
    hu_from_bian = hexagram_binary in ("111111", "000000")
    hu_upper, hu_lower = get_hu_gua(bian_binary if hu_from_bian else hexagram_binary)
    hu_info = HEXAGRAMS.get((hu_upper, hu_lower), (0, "未知卦"))

    # 錯卦（陰陽全反）：看「同一處境的完全相反面」。
    cuo_upper, cuo_lower = get_cuo_gua(hexagram_binary)
    cuo_info = HEXAGRAMS.get((cuo_upper, cuo_lower), (0, "未知卦"))

    # 綜卦（上下顛倒）：看「對方/旁觀者眼中的同一件事」。
    zong_upper, zong_lower = get_zong_gua(hexagram_binary)
    zong_info = HEXAGRAMS.get((zong_upper, zong_lower), (0, "未知卦"))

    # 動爻陰陽（從下往上數，bit 6-dong_yao）；陽爻=1
    moving_is_yang = hexagram_binary[6 - dong_yao] == "1"

    # 五行生克
    ti_element = BAGUA[ti_gua]["element"]
    yong_element = BAGUA[yong_gua]["element"]

    out = {
        "本卦": {
            "序號": hexagram_info[0],
            "名稱": hexagram_info[1],
            "上卦": f"{BAGUA[upper_gua]['name']} {BAGUA[upper_gua]['symbol']}",
            "下卦": f"{BAGUA[lower_gua]['name']} {BAGUA[lower_gua]['symbol']}",
            "二進位": hexagram_binary,
            "動爻": f"第{dong_yao}爻",
            "動爻位": dong_yao,
            "動爻陰陽": "陽" if moving_is_yang else "陰",
        },
        "體用": {
            "體卦": f"{BAGUA[ti_gua]['name']}（{ti_pos}）- {ti_element}・{BAGUA[ti_gua]['de']}",
            "用卦": f"{BAGUA[yong_gua]['name']}（{yong_pos}）- {yong_element}・{BAGUA[yong_gua]['de']}",
            "生克關係": analyze_wuxing(ti_element, yong_element),
            "卦德關係": analyze_guade(ti_gua, yong_gua),
        },
        "爻位盤": analyze_yao_positions(hexagram_binary, dong_yao),
        "互卦": {
            "名稱": hu_info[1],
            "上互": BAGUA[hu_upper]['name'],
            "下互": BAGUA[hu_lower]['name'],
            "取自變卦": hu_from_bian,
        },
        "變卦": {
            "序號": bian_info[0],
            "名稱": bian_info[1],
            "二進位": bian_binary,
        },
        "錯卦": {
            "名稱": cuo_info[1],
            "上卦": BAGUA[cuo_upper]['name'],
            "下卦": BAGUA[cuo_lower]['name'],
            "讀法": "陰陽全反——同一處境的完全相反面，照出你沒看到的另一端",
        },
        "綜卦": {
            "名稱": zong_info[1],
            "上卦": BAGUA[zong_upper]['name'],
            "下卦": BAGUA[zong_lower]['name'],
            "讀法": "上下顛倒——換對方/旁觀者的角度看同一件事",
        },
    }
    if season:
        ti_state = analyze_wangshuai(ti_element, season)
        out["卦氣旺衰"] = {
            "時令": f"{season}（{SEASON_ELEMENT[season]}旺）",
            "體卦旺衰": f"{BAGUA[ti_gua]['name']}{ti_element}・{ti_state}",
            "用卦旺衰": f"{BAGUA[yong_gua]['name']}{yong_element}・"
                     f"{analyze_wangshuai(yong_element, season)}",
            "體卦得令": ti_state in ("旺", "相"),
            "讀法": "體卦旺相則事易成、可為；休囚死則力弱、宜緩。旺相加吉，休囚減力——"
                  "為程度修正，非獨立吉凶。",
        }
    return out


def _apply_zishi(year: int, month: int, day: int, hour: int,
                 is_leap: bool) -> Tuple[int, int, int, bool, bool]:
    """原書「日始於子時」：23 時已入次日子時，日數取次日。

    唯一的推日處：農曆起卦函式都經過這裡，西曆入口只負責轉換後透傳
    is_leap，故不會重複推日。夜子時一派主張仍算當日——本專案取日始於
    子時，此為明確取捨，非疏漏。
    """
    if hour != 23:
        return year, month, day, is_leap, False
    year, month, day, is_leap = lunar_next_day(year, month, day, is_leap)
    return year, month, day, is_leap, True


def qigua_by_time(year: int, month: int, day: int, hour: int,
                  is_leap: bool = False) -> Dict:
    """以農曆時間起卦"""
    year, month, day, is_leap, rolled = _apply_zishi(year, month, day, hour, is_leap)
    year_num, year_dizhi = get_year_dizhi(year)
    shichen_num, shichen_name = get_shichen(hour)

    upper_sum = year_num + month + day
    lower_sum = upper_sum + shichen_num

    upper_gua = num_to_gua(upper_sum)
    lower_gua = num_to_gua(lower_sum)
    dong_yao = num_to_yao(lower_sum)

    season = get_season(year, month, day, is_leap)
    result = _analyze_hexagram(upper_gua, lower_gua, dong_yao, season)
    result["計算過程"] = {
        "年數": f"{year_dizhi}年 ({year_num})",
        "月數": month,
        "日數": day,
        "時辰": f"{shichen_name}時 ({shichen_num})",
        "上卦數": f"{upper_sum} mod 8 = {upper_gua}",
        "下卦數": f"{lower_sum} mod 8 = {lower_gua}",
        "動爻數": f"{lower_sum} mod 6 = {dong_yao}",
    }
    if rolled:
        result["計算過程"]["子時推日"] = "日始於子時，23時已入次日，日數取次日"
    return result


def _lunar_display(year: int, month: int, day: int, hour: int,
                   is_leap: bool) -> Tuple[str, bool]:
    """日期轉換要顯示「實際起卦所用」的農曆日，即子時推日之後的那一天。

    重算一次 _apply_zishi（純函式、同輸入同輸出）比把用到的日期從
    qigua_by_time 回傳出來更省事，兩處必然一致。
    """
    y, m, d, leap, rolled = _apply_zishi(year, month, day, hour, is_leap)
    return f"{y}年{'閏' if leap else ''}{m}月{d}日", rolled


def qigua_by_gregorian_time(year: int, month: int, day: int, hour: int) -> Dict:
    """以西曆時間起卦（自動轉換為農曆）"""
    lunar_year, lunar_month, lunar_day, is_leap = gregorian_to_lunar(year, month, day)
    result = qigua_by_time(lunar_year, lunar_month, lunar_day, hour, is_leap)

    lunar_text, rolled = _lunar_display(lunar_year, lunar_month, lunar_day, hour, is_leap)
    note = "梅花易數使用農曆計算"
    if rolled:
        note += "；23時屬次日子時，農曆日已推次日（日始於子時）"
    result["日期轉換"] = {
        "西曆": f"{year}年{month}月{day}日",
        "農曆": lunar_text,
        "說明": note,
    }
    return result


def qigua_by_time_precise(year: int, month: int, day: int,
                          hour: int, minute: int, second: int,
                          is_leap: bool = False) -> Dict:
    """以農曆時間 + 分秒起卦（今人精確擴充，非邵雍原法）。

    解決純時辰起卦的問題：同一時辰（2小時）內任何時刻同卦。
    分入下卦、秒入動爻，使同一時辰內不同時刻得不同卦。
    年/月/日為農曆；時/分/秒為時鐘讀數。
    """
    year, month, day, is_leap, rolled = _apply_zishi(year, month, day, hour, is_leap)
    year_num, year_dizhi = get_year_dizhi(year)
    shichen_num, shichen_name = get_shichen(hour)

    upper_sum = year_num + month + day + shichen_num
    lower_sum = upper_sum + minute
    dong_sum = lower_sum + second

    upper_gua = num_to_gua(upper_sum)
    lower_gua = num_to_gua(lower_sum)
    dong_yao = num_to_yao(dong_sum)

    season = get_season(year, month, day, is_leap)
    result = _analyze_hexagram(upper_gua, lower_gua, dong_yao, season)
    result["計算過程"] = {
        "年數": f"{year_dizhi}年 ({year_num})",
        "月數": month,
        "日數": day,
        "時辰": f"{shichen_name}時 ({shichen_num})",
        "分": minute,
        "秒": second,
        "上卦數": f"(年+月+日+時辰)={upper_sum} mod 8 = {upper_gua}",
        "下卦數": f"(上+分)={lower_sum} mod 8 = {lower_gua}",
        "動爻數": f"(下+秒)={dong_sum} mod 6 = {dong_yao}",
        "備註": "分入下卦、秒入動爻（今人精確擴充，非邵雍原法）",
    }
    if rolled:
        result["計算過程"]["子時推日"] = "日始於子時，23時已入次日，日數取次日"
    return result


def qigua_by_gregorian_time_precise(year: int, month: int, day: int,
                                    hour: int, minute: int, second: int) -> Dict:
    """以西曆時間 + 分秒起卦（自動轉農曆；今人精確擴充）。"""
    lunar_year, lunar_month, lunar_day, is_leap = gregorian_to_lunar(year, month, day)
    result = qigua_by_time_precise(lunar_year, lunar_month, lunar_day,
                                   hour, minute, second, is_leap)
    lunar_text, rolled = _lunar_display(lunar_year, lunar_month, lunar_day, hour, is_leap)
    note = "梅花易數使用農曆計算（分秒為今人精確擴充）"
    if rolled:
        note += "；23時屬次日子時，農曆日已推次日（日始於子時）"
    result["日期轉換"] = {
        "西曆": f"{year}年{month}月{day}日 {hour:02d}:{minute:02d}:{second:02d}",
        "農曆": lunar_text,
        "說明": note,
    }
    return result


def qigua_by_numbers(num1: int, num2: int, num3: Optional[int] = None) -> Dict:
    """以數字起卦。

    動爻恆取「總數除六」（原書 卷一・數字占）：兩數則 (num1+num2)、三數則
    (num1+num2+num3)。三數時只取 num3 是常見的今人簡法，非原書之法。
    """
    upper_gua = num_to_gua(num1)
    lower_gua = num_to_gua(num2)
    total = num1 + num2 + (num3 if num3 is not None else 0)
    dong_yao = num_to_yao(total)

    result = _analyze_hexagram(upper_gua, lower_gua, dong_yao)
    dong_expr = f"({num1}+{num2}) mod 6 = {dong_yao}" if num3 is None \
        else f"({num1}+{num2}+{num3}) mod 6 = {dong_yao}"
    result["計算過程"] = {
        "第一數": f"{num1} → {num1} mod 8 = {upper_gua} → {BAGUA[upper_gua]['name']}",
        "第二數": f"{num2} → {num2} mod 8 = {lower_gua} → {BAGUA[lower_gua]['name']}",
        "動爻": dong_expr,
    }
    return result


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
    print(f"  生克（五行・參考）：{ty['生克關係']}")
    if "卦德關係" in ty:
        print(f"  卦德（參考・解釋力更強）：{ty['卦德關係']}")

    if "卦氣旺衰" in result:
        ws = result["卦氣旺衰"]
        print("\n【三之二、卦氣旺衰】")
        print(f"  時令：{ws['時令']}")
        print(f"  體：{ws['體卦旺衰']}　用：{ws['用卦旺衰']}")
        print(f"  {'體卦得令' if ws['體卦得令'] else '體卦失令'}——{ws['讀法']}")

    print("\n【四、互卦】")
    hu = result["互卦"]
    src = "（本卦六爻皆同，依原書改從變卦取互）" if hu.get("取自變卦") else ""
    print(f"  {hu['名稱']}（上{hu['上互']}下{hu['下互']}）{src}")

    print("\n【五、變卦】")
    bian = result["變卦"]
    print(f"  第 {bian['序號']} 卦：{bian['名稱']}")
    print(f"  二進位：{bian['二進位']}")

    if "錯卦" in result:
        cuo = result["錯卦"]
        print("\n【六、錯卦（反爻・互補面）】")
        print(f"  {cuo['名稱']}（上{cuo['上卦']}下{cuo['下卦']}）— {cuo['讀法']}")
    if "綜卦" in result:
        zong = result["綜卦"]
        print("\n【七、綜卦（反爻・對方視角）】")
        print(f"  {zong['名稱']}（上{zong['上卦']}下{zong['下卦']}）— {zong['讀法']}")

    if "爻位盤" in result:
        yp = result["爻位盤"]
        dong = ben['動爻位']
        print("\n【八、爻位盤（結構・每卦必出）】")
        for ln in reversed(yp["六爻"]):  # 從上爻往下顯示
            mark = "★" if ln["位"] == dong else "　"
            zhong = f"·{ln['得中']}" if ln["得中"] else ""
            ying = ("應↔" if ln["有應"] else "無應↔") + ln["應爻名稱"]
            cc = f"·{ln['承乘']}" if ln["承乘"] else ""
            print(f"  {mark}{ln['名稱']}（{ln['陰陽']}）：{ln['當位']}{zhong}·{ying}{cc}")
        if yp["二五中正相應"]:
            print("  ※ 二五中正相應——最強外援徵象")
        print(f"  → 動爻處境：{yp['動爻摘要']}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] in ("time", "time-precise"):
            # 預設秒精度：避免同一時辰（2hr）重複得同卦
            now = datetime.now()
            result = qigua_by_gregorian_time_precise(
                now.year, now.month, now.day, now.hour, now.minute, now.second)
            print(f"\n起卦時間：{now.strftime('%Y年%m月%d日 %H:%M:%S')}（西曆，秒精度・預設）")
        elif sys.argv[1] == "time-shichen":
            # 傳統時辰精度（2hr）
            now = datetime.now()
            result = qigua_by_gregorian_time(now.year, now.month, now.day, now.hour)
            print(f"\n起卦時間：{now.strftime('%Y年%m月%d日 %H時')}（西曆，傳統時辰精度）")
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
            print("  python meihua_calc.py time                     # 當前時間起卦（秒精度・預設）")
            print("  python meihua_calc.py time-shichen             # 當前時間起卦（傳統時辰精度）")
            print("  python meihua_calc.py gregorian 2024 1 18 14   # 以西曆日期起卦")
            print("  python meihua_calc.py lunar 2024 12 8 14       # 以農曆日期起卦")
            print("  python meihua_calc.py num 6 8 9                # 以數字起卦")
            print("  python meihua_calc.py convert 2024 1 18        # 僅轉換日期")
            sys.exit(1)
    else:
        now = datetime.now()
        result = qigua_by_gregorian_time_precise(
            now.year, now.month, now.day, now.hour, now.minute, now.second)
        print(f"\n起卦時間：{now.strftime('%Y年%m月%d日 %H:%M:%S')}（西曆，秒精度・預設）")

    print_result(result)
