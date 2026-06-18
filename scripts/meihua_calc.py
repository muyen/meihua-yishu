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
# "de" = 卦德（說卦傳第七章）：易經原始的八卦屬性。姊妹專案 iching 實證卦德的解釋力
# 約為五行的 5 倍（docs/KEY_DISCOVERIES.md），故在此作為與五行並列的「參考透鏡」。
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


def get_cuo_gua(binary: str) -> Tuple[int, int]:
    """計算錯卦（陰陽全反：六爻每位翻轉）→ 上下卦數"""
    flipped = "".join("0" if b == "1" else "1" for b in binary)
    return binary_to_gua_pair(flipped)


def get_zong_gua(binary: str) -> Tuple[int, int]:
    """計算綜卦（上下顛倒：整卦翻轉）→ 上下卦數"""
    return binary_to_gua_pair(binary[::-1])


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

    # 承乘：相鄰兩爻，標記兩極——陰乘陽(最危)、陽乘陰(最順)。標於上爻。
    chengcheng = {}
    for i in range(2, 7):
        if not is_yang[i] and is_yang[i - 1]:
            chengcheng[i] = "陰乘陽（柔凌剛·最不穩）"
        elif is_yang[i] and not is_yang[i - 1]:
            chengcheng[i] = "陽乘陰（剛統柔·最順）"
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

    return {
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


def qigua_by_time_precise(year: int, month: int, day: int,
                          hour: int, minute: int, second: int) -> Dict:
    """以農曆時間 + 分秒起卦（今人精確擴充，非邵雍原法）。

    解決純時辰起卦的問題：同一時辰（2小時）內任何時刻同卦。
    分入下卦、秒入動爻，使同一時辰內不同時刻得不同卦。
    年/月/日為農曆；時/分/秒為時鐘讀數。
    """
    year_num, year_dizhi = get_year_dizhi(year)
    shichen_num, shichen_name = get_shichen(hour)

    upper_sum = year_num + month + day + shichen_num
    lower_sum = upper_sum + minute
    dong_sum = lower_sum + second

    upper_gua = num_to_gua(upper_sum)
    lower_gua = num_to_gua(lower_sum)
    dong_yao = num_to_yao(dong_sum)

    result = _analyze_hexagram(upper_gua, lower_gua, dong_yao)
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
    return result


def qigua_by_gregorian_time_precise(year: int, month: int, day: int,
                                    hour: int, minute: int, second: int) -> Dict:
    """以西曆時間 + 分秒起卦（自動轉農曆；今人精確擴充）。"""
    lunar_year, lunar_month, lunar_day, is_leap = gregorian_to_lunar(year, month, day)
    result = qigua_by_time_precise(lunar_year, lunar_month, lunar_day, hour, minute, second)
    result["日期轉換"] = {
        "西曆": f"{year}年{month}月{day}日 {hour:02d}:{minute:02d}:{second:02d}",
        "農曆": f"{lunar_year}年{'閏' if is_leap else ''}{lunar_month}月{lunar_day}日",
        "說明": "梅花易數使用農曆計算（分秒為今人精確擴充）",
    }
    return result


def qigua_by_numbers(num1: int, num2: int, num3: Optional[int] = None) -> Dict:
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
# 爻辭文本指標 (Yaoci Text Metrics)
# 來源：muyen/decoding-iching 姊妹研究專案（文本分析）
#   - 爻位/關係指標：docs/YAO_INTERACTION_TABLES.md、HEXAGRAM_RELATIONSHIPS_SUMMARY.md
#   - 卦象標籤：data/analysis/corrected_yaoci_labels.json（384 爻辭關鍵字評分）
# ⚠️ 這些數值衡量「古典爻辭文本的吉凶用語密度」，
#    非真實事件的成功機率。內部輔助參考用，不影響起卦邏輯，不直接呈現給用戶。
# ==============================================================================

# 爻位係數（Position Coefficients）— (吉率−凶率)/2，源自 384 爻辭文本標籤
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
    (3, True): -0.375, (3, False): -0.062,  # 三位陽爻：爻辭文本最偏凶語
    (4, True): 0.281, (4, False): 0.250,
    (5, True): 0.344, (5, False): 0.500,
    (6, True): 0.000, (6, False): 0.062,
}

# 64卦策略分類
# 類型: 吸引子(留), 排斥子(走), 福地(守), 困境(變), 陷阱(慎), 一般(觀)
# 變卦路徑「變N爻」一律以自下而上的爻位表示（初爻=1 … 上爻=6），與
# apply_change 的約定一致；tests/test_strategy_paths.py 驗證每條路徑的
# 變爻確實能將本卦變為所標示的目標卦。
HEXAGRAM_STRATEGY = {
    1: ("排斥子", "走", 0, "乾 → 履（變3爻）"),
    2: ("一般", "觀", 33, "坤 → 謙（變3爻）"),
    3: ("一般", "觀", 33, "屯 → 比（變1爻）"),
    4: ("一般", "觀", 33, "蒙 → 損（變1爻）"),
    5: ("吸引子", "留", 67, None),
    6: ("吸引子", "留", 67, None),
    7: ("排斥子", "走", 17, "師 → 臨（變1爻）"),
    8: ("吸引子", "留", 67, None),
    9: ("一般", "觀", 33, "小畜 → 家人（變2爻）"),
    10: ("福地", "守", 50, None),
    11: ("一般", "觀", 33, "泰 → 臨（變3爻）"),
    12: ("福地", "守", 50, None),
    13: ("排斥子", "走", 17, "同人 → 遯（變1爻）"),
    14: ("一般", "觀", 33, "大有 → 鼎（變1爻）"),
    15: ("吸引子", "留", 83, None),  # 謙卦 - 唯一全吉卦
    16: ("困境", "變", 17, "豫 → 晉（變6爻）"),
    17: ("一般", "觀", 33, "隨 → 萃（變1爻）"),
    18: ("排斥子", "走", 17, "蠱 → 鼎（變4爻）"),
    19: ("吸引子", "留", 83, None),  # 臨卦 - 關鍵轉折點
    20: ("排斥子", "走", 0, "觀 → 比（變6爻）"),
    21: ("排斥子", "走", 17, "噬嗑 → 晉（變1爻）"),
    22: ("一般", "觀", 33, "賁 → 家人（變5爻）"),
    23: ("困境", "變", 17, "剝 → 晉（變4爻）"),
    24: ("一般", "觀", 33, "復 → 臨（變2爻）"),
    25: ("一般", "觀", 33, "无妄 → 否（變1爻）"),
    26: ("福地", "守", 50, None),
    27: ("福地", "守", 50, None),
    28: ("一般", "觀", 33, "大過 → 夬 → 革"),
    29: ("排斥子", "走", 0, "坎 → 比（變2爻）"),
    30: ("一般", "觀", 33, "離 → 豐（變6爻）"),
    31: ("困境", "變", 17, "咸 → 遯（變6爻）"),
    32: ("排斥子", "走", 0, "恆 → 升（變4爻）"),
    33: ("吸引子", "留", 67, None),
    34: ("吸引子", "留", 50, None),
    35: ("吸引子", "留", 67, None),
    36: ("排斥子", "走", 17, "明夷 → 謙（變1爻）"),
    37: ("吸引子", "留", 67, None),
    38: ("一般", "觀", 33, "睽 → 未濟（變1爻）"),
    39: ("排斥子", "走", 17, "蹇 → 謙（變5爻）"),
    40: ("吸引子", "留", 50, None),
    41: ("福地", "守", 50, None),
    42: ("福地", "守", 50, None),
    43: ("排斥子", "走", 0, "夬 → 需（變4爻）"),
    44: ("排斥子", "走", 17, "姤 → 遯（變2爻）"),
    45: ("福地", "守", 50, None),
    46: ("吸引子", "留", 67, None),
    47: ("排斥子", "走", 17, "困 → 訟（變6爻）"),
    48: ("困境", "變", 17, "井 → 需（變1爻）"),
    49: ("吸引子", "留", 50, None),
    50: ("吸引子", "留", 67, None),
    51: ("陷阱", "慎", 17, "震 → 豐（變3爻）"),
    52: ("一般", "觀", 33, "艮 → 謙（變6爻）"),
    53: ("福地", "守", 50, None),
    54: ("一般", "觀", 33, "歸妹 → 臨（變4爻）"),
    55: ("吸引子", "留", 50, None),
    56: ("排斥子", "走", 0, "旅 → 鼎（變2爻）"),
    57: ("一般", "觀", 33, "巽 → 漸（變2爻）"),
    58: ("吸引子", "留", 50, None),
    59: ("一般", "觀", 33, "渙 → 訟（變4爻）"),
    60: ("排斥子", "走", 17, "節 → 臨（變5爻）"),
    61: ("排斥子", "走", 17, "中孚 → 益（變2爻）"),
    62: ("排斥子", "走", 0, "小過 → 謙（變4爻）"),
    63: ("排斥子", "走", 0, "既濟 → 需（變2爻）"),
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
            'warning': '⚠️ 三位陽爻在爻辭中多凶語，動於此位宜格外謹慎'
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
            'warning': '⚠️ 此爻位於爻辭中偏向凶語，宜謹慎'
        }
    else:
        return {
            'coefficient': coef,
            'risk_level': '中等',
            'warning': None
        }


def get_hexagram_strategy(hex_num: int) -> Optional[dict]:
    """
    獲取卦的策略建議

    Args:
        hex_num: 卦序 (1-64)

    Returns:
        dict: {
            'type': 類型（吸引子/排斥子/福地/困境/陷阱/一般）,
            'advice': 建議（留/走/守/變/慎/觀）,
            'ji_rate': 爻辭吉語比例（文本指標，非結果機率）,
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


STRATEGY_NEXT_STEPS = {
    "留": "【下一步】維持現狀，不宜改變。目前位置有利，變動反而損失。",
    "走": "【下一步】積極改變，離開當前狀態。此位置不利久留，宜主動求變。",
    "守": "【下一步】穩守不動，靜觀其變。位置尚可，不主動出擊，等待時機。",
    "變": "【下一步】必須改變，不變則困。當前困境需主動突破，猶豫更糟。",
    "慎": "【下一步】謹慎行事，小心陷阱。周圍環境不佳，任何動作都要三思。",
    "觀": "【下一步】觀察局勢，再做決定。情況中等，需要更多信息才能判斷。",
}


def print_strategy_advice(hex_num: int):
    """打印卦的策略建議"""
    strategy = get_hexagram_strategy(hex_num)
    if not strategy:
        return

    print(f"\n【策略建議】")
    print(f"  類型：{strategy['type']}")
    print(f"  建議：{strategy['advice']}")
    if strategy['change_path']:
        print(f"  變卦路徑：{strategy['change_path']}")

    # 輸出具體下一步建議
    advice = strategy['advice']
    if advice in STRATEGY_NEXT_STEPS:
        print(f"\n{STRATEGY_NEXT_STEPS[advice]}")


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

    print("\n【四、互卦】")
    hu = result["互卦"]
    print(f"  {hu['名稱']}（上{hu['上互']}下{hu['下互']}）")

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

    # 添加策略建議
    hex_num = ben['序號']
    if hex_num in HEXAGRAM_STRATEGY:
        print_strategy_advice(hex_num)

        # 動爻文本傾向（爻辭用語統計・非機率），不論吉凶皆出，免靜默漏報
        dong_yao = ben['動爻位']
        is_yang = ben['動爻陰陽'] == '陽'
        risk = get_position_risk(dong_yao, is_yang)
        print("\n【動爻文本傾向】（爻辭用語統計・非機率，參考）")
        print(f"  風險等級：{risk['risk_level']}")
        if risk['warning']:
            print(f"  {risk['warning']}")

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
