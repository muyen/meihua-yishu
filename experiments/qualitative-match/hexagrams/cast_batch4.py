#!/usr/bin/env python3
"""Batch 4 casting: 取象法 numbers -> full hexagram analysis for all 60 events.

The two trigram numbers and the moving-line number are the ONLY human judgment
here; they are chosen from each event's imagery (先天八卦數: 乾1 兌2 離3 震4
巽5 坎6 艮7 坤8) and recorded with a written rationale so every cast is auditable.

Control hexagram for event X = the real hexagram of event Y, where Y = pairing[X]
(displaced 取象法). Because the pairing is a single-cycle derangement, each cast is
used exactly once as a real and exactly once as a control.

Outputs: casting_records_batch4.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "scripts"))
from meihua_calc import qigua_by_numbers  # noqa: E402

REGISTRY = os.path.join(HERE, "..", "events", "event_registry_batch4.json")
PAIRINGS = os.path.join(HERE, "pairings_batch4.json")
OUT = os.path.join(HERE, "casting_records_batch4.json")

# event_id: (upper_num, lower_num, line_num, 取象 rationale)
QUXIANG = {
    "E63": (8, 3, 2, "上坤：列國聚集的獎牌榜為眾、為土；下離：競技的展示與光采。動爻取閉幕日 8/2 之 2"),
    "E64": (7, 2, 4, "上艮：地主蘇格蘭立於自家山門、承接他人退出的擔子；下兌：主場的喜悅。動爻取 10 金門檻"),
    "E65": (4, 3, 4, "上震：接力的足與速度、雷動；下離：閉幕夜的燈火與展示。動爻取 4x100 之 4"),
    "E66": (1, 4, 3, "上乾：拳擊的金屬與剛擊；下震：突發的動作。動爻取 3 金門檻"),
    "E67": (5, 1, 4, "上巽：場地自行車的風與穿行；下乾：輪為圓、為金。動爻取團體追逐 4 人"),
    "E68": (7, 8, 2, "上艮：柔道的手與制止；下坤：摔向地面。動爻取 8/2 之 2"),
    "E69": (2, 4, 3, "上兌：少年之戲與喜悅；下震：快攻之動。動爻取 3x3 之 3"),
    "E70": (6, 2, 3, "上坎：泳池之水；下兌：澤。動爻取 15 金門檻 mod 6"),
    "E71": (8, 2, 2, "上坤：團隊為眾；下兌：手與悅。動爻取 8/2 之 2"),
    "E72": (7, 1, 1, "上艮：舉重之重、之靜止；下乾：金與剛力。動爻取榜首之 1"),
    "E73": (2, 4, 6, "上兌：交易為口舌、為金錢；下震：突發的異動。動爻取截止時刻 6pm"),
    "E74": (1, 8, 4, "上乾：領先者居首；下坤：戰績表為地。動爻取 8/10 之 10 mod 6"),
    "E75": (3, 5, 5, "上離：罕見的光采；下巽：無安打之「無」、風之空。動爻取巽數 5"),
    "E76": (5, 6, 3, "上巽：客場的遠行；下坎：資格賽的險阻。動爻取第三輪"),
    "E77": (7, 4, 6, "上艮：名人堂為門、為紀念的靜止；下震：球賽之動。動爻取 8/6 之 6"),
    "E78": (1, 5, 4, "上乾：頭號種子；下巽：籤表如網。動爻取 8/10 之 10 mod 6"),
    "E79": (4, 3, 1, "上震：休賽後重啟之動；下離：賽事的展演。動爻取「第一場」之 1"),
    "E80": (5, 1, 6, "上巽：體操的柔韌與器械之木；下乾：全能為圓、為天。動爻取六項器械"),
    "E81": (1, 2, 5, "上乾：聯準會為君、為權威；下兌：記者會的口舌。動爻取 7/29 之 29 mod 6"),
    "E82": (3, 2, 6, "上離：蘋果的螢幕與品牌光采；下兌：銷售與金錢。動爻取 7/30 之 30 mod 6"),
    "E83": (1, 5, 5, "上乾：企業市場的支配；下巽：雲端如風、如網絡。動爻取 7/29 mod 6"),
    "E84": (8, 5, 6, "上坤：物流與倉儲為地、為眾；下巽：AWS 之風與遍布。動爻取 7/30 mod 6"),
    "E85": (5, 3, 6, "上巽：社群網絡為風、為傳言；下離：螢幕與展示。動爻取 7/30 mod 6"),
    "E86": (8, 7, 1, "上坤：勞動大眾為眾；下艮：報告為定數、為止。動爻取 8/7 mod 6"),
    "E87": (1, 6, 4, "上乾：幣為金、為圓；下坎：隱流與波動之險。動爻取 8/10 mod 6"),
    "E88": (3, 1, 2, "上離：指數高點的光；下乾：大者之集。動爻取 500 mod 6"),
    "E89": (1, 7, 4, "上乾：黃金為金、為天；下艮：山中之藏、之靜。動爻取 8/10 mod 6"),
    "E90": (6, 5, 4, "上坎：殖利率如水之流與深；下巽：十年為長、為入。動爻取 8/10 mod 6"),
    "E91": (2, 8, 1, "上兌：島嶼為澤、初選為口舌；下坤：選民為眾。動爻取 8/1 之 1"),
    "E92": (6, 2, 4, "上坎：密西根為湖水之州；下兌：競選的言說。動爻取 8/4 之 4"),
    "E93": (6, 1, 4, "上坎：密西根之湖；下乾：州長為君、席位開放。動爻取 10 個百分點門檻 mod 6"),
    "E94": (8, 7, 4, "上坤：州為地；下艮：現任者為止、為守。動爻取 8/4 之 4"),
    "E95": (8, 5, 4, "上坤：堪薩斯平原為地；下巽：風行平原、未定之勢。動爻取 8/4 之 4"),
    "E96": (2, 6, 2, "上兌：前二名制之「二」與口舌；下坎：普吉特海灣之水。動爻取「二」"),
    "E97": (7, 8, 6, "上艮：田納西之山；下坤：選民為眾。動爻取 8/6 之 6"),
    "E98": (3, 6, 2, "上離：夏威夷之日與火山；下坎：環繞之洋。動爻取 8/8 mod 6"),
    "E99": (5, 3, 1, "上巽：蜘蛛絲為繩直、為入；下離：銀幕的展演。動爻取 7/31 之 31 mod 6"),
    "E100": (5, 2, 6, "上巽：蛛網之線；下兌：票房為金錢。動爻取 1.5 億門檻 150 mod 6"),
    "E101": (4, 7, 3, "上震：新片入場之動；下艮：在位者守成不動。動爻取 8/9 mod 6"),
    "E102": (4, 2, 4, "上震：音樂節之雷與聲；下兌：群眾之悅。動爻取四日之 4"),
    "E103": (2, 7, 2, "上兌：歌為口舌；下艮：續居榜首為止、為不動。動爻取 8/8 mod 6"),
    "E104": (2, 4, 2, "上兌：音樂；下震：新輯空降之震。動爻取 200 mod 6"),
    "E105": (3, 8, 3, "上離：串流螢幕；下坤：大眾收視為眾。動爻取 8/9 mod 6"),
    "E106": (3, 7, 2, "上離：電影；下艮：艮為狗、為小（片名 Buddy）。動爻取 2000 萬門檻 20 mod 6"),
    "E107": (6, 3, 6, "上坎：漏洞為隱、為盜；下離：揭露之光。動爻取 8/6 之 6"),
    "E108": (2, 6, 3, "上兌：兌為毀折、為講談；下坎：入侵之隱。動爻取 8/9 mod 6"),
    "E109": (5, 2, 2, "上巽：摺疊為巽之柔木、之入；下兌：零售與金錢。動爻取 Fold 8 mod 6"),
    "E110": (1, 3, 4, "上乾：前沿為天、為創始；下離：智能之明。動爻取 8/10 mod 6"),
    "E111": (5, 6, 2, "上巽：雲端為風；下坎：陷落之險。動爻取兩小時門檻"),
    "E112": (3, 1, 4, "上離：晶片為火、為明；下乾：硬體霸權之金。動爻取 8/10 mod 6"),
    "E113": (1, 7, 4, "上乾：政府為君；下艮：監管為止、為限。動爻取 8/10 mod 6"),
    "E114": (7, 3, 3, "上艮：發表會之門未開、為待；下離：公告之顯。動爻取九月之 9 mod 6"),
    "E115": (1, 4, 5, "上乾：天為蒼穹；下震：發射之動與雷。動爻取 CRS-35 之 35 mod 6"),
    "E116": (1, 5, 2, "上乾：太空為天；下巽：反覆出入如風。動爻取 8 次門檻 mod 6"),
    "E117": (1, 6, 4, "上乾：天；下坎：試飛之險與未定。動爻取 8/10 mod 6"),
    "E118": (5, 6, 4, "上巽：颶風為風；下坎：海為水。動爻取 8/10 mod 6"),
    "E119": (7, 4, 1, "上艮：地與山；下震：地震之雷動。動爻取規模 7 mod 6"),
    "E120": (3, 4, 3, "上離：極光之明；下震：地磁擾動之電。動爻取 G3 之 3"),
    "E121": (3, 8, 4, "上離：高溫之火；下坤：國土為地。動爻取 8/10 mod 6"),
    "E122": (7, 1, 4, "上艮：延誤為止；下乾：航太機構之大業。動爻取 8/10 mod 6"),
}


def summarize(res: dict) -> dict:
    """Pull the fields the interpreter needs; drop the printable chrome."""
    return {
        "upper_trigram": res["本卦"]["上卦"],
        "lower_trigram": res["本卦"]["下卦"],
        "changing_line": res["本卦"]["動爻位"],
        "primary_hexagram": {
            "number": res["本卦"]["序號"],
            "name": res["本卦"]["名稱"],
        },
        "changed_hexagram": {
            "number": res["變卦"]["序號"],
            "name": res["變卦"]["名稱"],
        },
        "mutual_hexagram": {"name": res["互卦"]["名稱"]},
        "cuo_hexagram": {"name": res["錯卦"]["名稱"]},
        "zong_hexagram": {"name": res["綜卦"]["名稱"]},
        "ti_yong": {
            "ti": res["體用"]["體卦"],
            "yong": res["體用"]["用卦"],
            "wuxing": res["體用"]["生克關係"],
            "guade": res["體用"]["卦德關係"],
        },
        "moving_line_position": res["爻位盤"]["動爻摘要"],
    }


def main():
    with open(REGISTRY) as f:
        registry = json.load(f)
    with open(PAIRINGS) as f:
        pairings = {d["event_id"]: d["control_source"] for d in json.load(f)["pairings"]}

    events = {e["event_id"]: e for e in registry["events"]}
    missing = set(events) - set(QUXIANG)
    if missing:
        sys.exit(f"ERROR: no 取象 for {sorted(missing)}")

    casts = {}
    for eid, (n1, n2, n3, why) in QUXIANG.items():
        res = qigua_by_numbers(n1, n2, n3)
        casts[eid] = {
            "numbers": [n1, n2, n3],
            "quxiang_rationale": why,
            **summarize(res),
        }

    records = []
    for eid in sorted(events, key=lambda x: int(x[1:])):
        control_src = pairings[eid]
        records.append(
            {
                "event_id": eid,
                "event_title": events[eid]["title_en"],
                "event_domain": events[eid]["domain"],
                "expected_date": events[eid]["expected_date"],
                "binary_outcome_definition": events[eid]["binary_outcome"],
                "real_hexagram": casts[eid],
                "control_hexagram": {"displaced_from": control_src, **casts[control_src]},
            }
        )

    doc = {
        "generated": "2026-07-27",
        "batch": 4,
        "method": "取象法 numbers -> meihua_calc.qigua_by_numbers; displaced 取象法 controls",
        "note": (
            "Interpretation text is written ONCE per cast and reused: the text for event Y's "
            "real hexagram is the same text served as event X's control, where Y = pairing[X]. "
            "Identical hexagram, identical reading — this removes any chance of the caster "
            "writing weaker prose for controls."
        ),
        "total_events": len(records),
        "events": records,
    }
    with open(OUT, "w") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print(f"Wrote {OUT} ({len(records)} events)")

    seen = {}
    for r in records:
        seen.setdefault(r["real_hexagram"]["primary_hexagram"]["name"], []).append(r["event_id"])
    dupes = {k: v for k, v in seen.items() if len(v) > 1}
    print(f"Distinct primary hexagrams among 60 real casts: {len(seen)}")
    if dupes:
        print("Repeated primaries:", json.dumps(dupes, ensure_ascii=False))


if __name__ == "__main__":
    main()
