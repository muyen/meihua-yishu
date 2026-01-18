#!/usr/bin/env python3
"""
梅花易數起卦計算工具
Meihua Yishu (Plum Blossom Numerology) Calculator
"""

from datetime import datetime
from typing import Tuple, Dict

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

# 六十四卦名稱（按上卦*8+下卦的順序）
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
    0: (1, "子"), 1: (1, "子"), 2: (2, "丑"), 3: (2, "丑"), 4: (3, "寅"), 5: (3, "寅"),
    6: (4, "卯"), 7: (4, "卯"), 8: (5, "辰"), 9: (5, "辰"), 10: (6, "巳"), 11: (6, "巳"),
    12: (7, "午"), 13: (7, "午"), 14: (8, "未"), 15: (8, "未"), 16: (9, "申"), 17: (9, "申"),
    18: (10, "酉"), 19: (10, "酉"), 20: (11, "戌"), 21: (11, "戌"), 22: (12, "亥"), 23: (1, "子"),
}


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
    # 二進位從左到右對應上爻到初爻
    # yao_position 1 對應最右邊（index 5）
    index = 6 - yao_position
    bit_list = list(binary)
    bit_list[index] = "0" if bit_list[index] == "1" else "1"
    return "".join(bit_list)


def binary_to_gua_pair(binary: str) -> Tuple[int, int]:
    """二進位轉上下卦數"""
    upper_bin = binary[:3]
    lower_bin = binary[3:]
    
    # 反查二進位對應的卦數
    for num, info in BAGUA.items():
        if info["binary"] == upper_bin:
            upper = num
        if info["binary"] == lower_bin:
            lower = num
    return upper, lower


def get_hu_gua(binary: str) -> Tuple[int, int]:
    """計算互卦（取2-4爻為下互，3-5爻為上互）"""
    # binary index: 0=上爻, 1=五爻, 2=四爻, 3=三爻, 4=二爻, 5=初爻
    upper_hu = binary[1:4]  # 5,4,3爻
    lower_hu = binary[2:5]  # 4,3,2爻
    
    for num, info in BAGUA.items():
        if info["binary"] == upper_hu:
            hu_upper = num
        if info["binary"] == lower_hu:
            hu_lower = num
    return hu_upper, hu_lower


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


def qigua_by_time(year: int, month: int, day: int, hour: int) -> Dict:
    """以時間起卦"""
    # 計算年數（各位數相加）
    year_sum = sum(int(d) for d in str(year))
    
    # 獲取時辰
    shichen_num, shichen_name = get_shichen(hour)
    
    # 計算上卦、下卦、動爻
    upper_sum = year_sum + month + day
    lower_sum = upper_sum + shichen_num
    
    upper_gua = num_to_gua(upper_sum)
    lower_gua = num_to_gua(lower_sum)
    dong_yao = num_to_yao(lower_sum)
    
    # 獲取卦象
    hexagram_binary = get_hexagram_binary(upper_gua, lower_gua)
    hexagram_info = HEXAGRAMS.get((upper_gua, lower_gua), (0, "未知卦"))
    
    # 判斷體用（動爻在上卦則上卦為用，反之下卦為用）
    if dong_yao > 3:  # 動爻在上卦
        ti_gua = lower_gua
        yong_gua = upper_gua
        ti_pos = "下卦"
        yong_pos = "上卦"
    else:  # 動爻在下卦
        ti_gua = upper_gua
        yong_gua = lower_gua
        ti_pos = "上卦"
        yong_pos = "下卦"
    
    # 計算變卦
    bian_binary = apply_change(hexagram_binary, dong_yao)
    bian_upper, bian_lower = binary_to_gua_pair(bian_binary)
    bian_info = HEXAGRAMS.get((bian_upper, bian_lower), (0, "未知卦"))
    
    # 計算互卦
    hu_upper, hu_lower = get_hu_gua(hexagram_binary)
    hu_info = HEXAGRAMS.get((hu_upper, hu_lower), (0, "未知卦"))
    
    # 分析體用生克
    ti_element = BAGUA[ti_gua]["element"]
    yong_element = BAGUA[yong_gua]["element"]
    wuxing_relation = analyze_wuxing(ti_element, yong_element)
    
    return {
        "計算過程": {
            "年數": year_sum,
            "月數": month,
            "日數": day,
            "時辰": f"{shichen_name}時 ({shichen_num})",
            "上卦數": f"{upper_sum} mod 8 = {upper_gua}",
            "下卦數": f"{lower_sum} mod 8 = {lower_gua}",
            "動爻數": f"{lower_sum} mod 6 = {dong_yao}",
        },
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
            "生克關係": wuxing_relation,
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


def qigua_by_numbers(num1: int, num2: int, num3: int = None) -> Dict:
    """以數字起卦"""
    upper_gua = num_to_gua(num1)
    lower_gua = num_to_gua(num2)
    
    if num3 is not None:
        dong_yao = num_to_yao(num3)
    else:
        dong_yao = num_to_yao(num1 + num2)
    
    # 獲取卦象
    hexagram_binary = get_hexagram_binary(upper_gua, lower_gua)
    hexagram_info = HEXAGRAMS.get((upper_gua, lower_gua), (0, "未知卦"))
    
    # 判斷體用
    if dong_yao > 3:
        ti_gua = lower_gua
        yong_gua = upper_gua
        ti_pos = "下卦"
        yong_pos = "上卦"
    else:
        ti_gua = upper_gua
        yong_gua = lower_gua
        ti_pos = "上卦"
        yong_pos = "下卦"
    
    # 計算變卦
    bian_binary = apply_change(hexagram_binary, dong_yao)
    bian_upper, bian_lower = binary_to_gua_pair(bian_binary)
    bian_info = HEXAGRAMS.get((bian_upper, bian_lower), (0, "未知卦"))
    
    # 計算互卦
    hu_upper, hu_lower = get_hu_gua(hexagram_binary)
    hu_info = HEXAGRAMS.get((hu_upper, hu_lower), (0, "未知卦"))
    
    # 分析體用生克
    ti_element = BAGUA[ti_gua]["element"]
    yong_element = BAGUA[yong_gua]["element"]
    wuxing_relation = analyze_wuxing(ti_element, yong_element)
    
    return {
        "計算過程": {
            "第一數": f"{num1} → {num1} mod 8 = {upper_gua} → {BAGUA[upper_gua]['name']}",
            "第二數": f"{num2} → {num2} mod 8 = {lower_gua} → {BAGUA[lower_gua]['name']}",
            "動爻": f"({num1}+{num2}) mod 6 = {dong_yao}" if num3 is None else f"{num3} mod 6 = {dong_yao}",
        },
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
            "生克關係": wuxing_relation,
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


def print_result(result: Dict):
    """格式化輸出結果"""
    print("\n" + "=" * 50)
    print("📿 梅花易數起卦結果")
    print("=" * 50)
    
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
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "time":
            # 使用當前時間起卦
            now = datetime.now()
            result = qigua_by_time(now.year, now.month, now.day, now.hour)
            print(f"\n起卦時間：{now.strftime('%Y年%m月%d日 %H:%M')}")
        elif sys.argv[1] == "num" and len(sys.argv) >= 4:
            # 使用數字起卦
            num1 = int(sys.argv[2])
            num2 = int(sys.argv[3])
            num3 = int(sys.argv[4]) if len(sys.argv) > 4 else None
            result = qigua_by_numbers(num1, num2, num3)
        else:
            print("用法：")
            print("  python meihua_calc.py time           # 以當前時間起卦")
            print("  python meihua_calc.py num 6 8 9      # 以數字起卦")
            sys.exit(1)
    else:
        # 默認使用當前時間
        now = datetime.now()
        result = qigua_by_time(now.year, now.month, now.day, now.hour)
        print(f"\n起卦時間：{now.strftime('%Y年%m月%d日 %H:%M')}")
    
    print_result(result)
