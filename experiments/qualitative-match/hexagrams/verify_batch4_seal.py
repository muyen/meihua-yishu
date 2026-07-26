#!/usr/bin/env python3
"""Pre-resolution integrity check for batch 4, and merge of the forced binary predictions.

Fails loudly if the sealed state is inconsistent. Run before the window closes;
re-run after scoring to confirm nothing was edited in between.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "scripts"))
INTERP = os.path.join(HERE, "..", "interpretations")
CASTS = os.path.join(HERE, "casting_records_batch4.json")
PREDS = os.path.join(HERE, "predictions_batch4.json")

errors = []


def check(cond, msg):
    if not cond:
        errors.append(msg)


def main():
    casts = json.load(open(CASTS))
    pairing = {d["event_id"]: d["control_source"]
               for d in json.load(open(os.path.join(HERE, "pairings_batch4.json")))["pairings"]}
    blind = {d["event_id"]: d["real_is_A"]
             for d in json.load(open(os.path.join(INTERP, "blinding_key_batch4.json")))["events"]}
    preds = json.load(open(PREDS))["predictions"]

    events = {r["event_id"]: r for r in casts["events"]}
    check(len(events) == 60, f"expected 60 events, got {len(events)}")

    bodies = {}
    for eid, rec in events.items():
        for label in ("A", "B"):
            path = os.path.join(INTERP, f"{eid}_{label}.md")
            check(os.path.exists(path), f"{eid}_{label}.md missing")
            if not os.path.exists(path):
                continue
            text = open(path).read()
            head, _, body = text.partition("\n\n")
            is_real = (label == "A") == blind[eid]
            h = rec["real_hexagram"] if is_real else rec["control_hexagram"]
            want = f"{h['primary_hexagram']['number']} {h['primary_hexagram']['name']}"
            check(want in head, f"{eid}_{label}: header hexagram mismatch (want {want})")
            bodies[(eid, "real" if is_real else "control")] = body.strip()

    # The control body for X must be byte-identical to the real body of pairing[X].
    for eid in events:
        src = pairing[eid]
        check(
            bodies.get((eid, "control")) == bodies.get((src, "real")),
            f"{eid}: control body is not identical to {src}'s real body",
        )

    check(set(preds) == set(events), "predictions do not cover exactly the 60 events")
    calls = [p["call"] for p in preds.values()]
    check(all(c in ("YES", "NO") for c in calls), "non-binary prediction found")

    # Reproducibility: the stored casts must still fall out of scripts/meihua_calc.py.
    # A sibling session already stripped 224 lines from that module once; without this
    # the seal could be silently orphaned and we would only find out at scoring time.
    from cast_batch4 import QUXIANG, summarize
    from meihua_calc import qigua_by_numbers

    fields = set(summarize(qigua_by_numbers(1, 1, 1)))

    def hexagram_only(d):
        """Drop provenance keys (numbers, rationale, displaced_from) — compare the cast itself."""
        return {k: v for k, v in d.items() if k in fields}

    for eid, rec in events.items():
        up, low, line, _ = QUXIANG[eid]
        fresh = summarize(qigua_by_numbers(up, low, line))
        check(
            fresh == hexagram_only(rec["real_hexagram"]),
            f"{eid}: 取象 ({up},{low},{line}) no longer reproduces the stored cast",
        )
        src = pairing[eid]
        check(hexagram_only(rec["control_hexagram"]) == hexagram_only(events[src]["real_hexagram"]),
              f"{eid}: control hexagram is not {src}'s real hexagram")

    # Merge predictions into the casting record so resolution has one file to read.
    for eid, rec in events.items():
        rec["forced_binary_prediction"] = preds[eid]["call"]
        rec["prediction_basis"] = preds[eid]["basis"]
    casts["predictions_merged"] = True
    json.dump(casts, open(CASTS, "w"), ensure_ascii=False, indent=2)

    if errors:
        print(f"FAILED: {len(errors)} problem(s)")
        for e in errors[:20]:
            print("  -", e)
        sys.exit(1)

    yes = calls.count("YES")
    print("SEALED STATE OK")
    print(f"  60 events, 120 interpretation files, headers match blinding key")
    print(f"  all 60 取象 triples still reproduce from scripts/meihua_calc.py")
    print(f"  every control body identical to its displaced source's real body")
    print(f"  forced binary predictions: {yes} YES / {len(calls) - yes} NO")


if __name__ == "__main__":
    main()
