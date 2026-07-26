#!/usr/bin/env python3
"""Emit the 120 blinded interpretation files for batch 4.

One interpretation body is written per CAST (keyed by the event whose imagery
produced it, in bodies_batch4_*.json). Event X's real file gets BODIES[X];
event X's control file gets BODIES[pairing[X]] — the identical text that serves
as event Y's real reading. Same hexagram, same words: the caster cannot write
weaker prose for controls even unconsciously.

A/B assignment comes from the pre-committed blinding key.
"""
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CASTS = os.path.join(HERE, "casting_records_batch4.json")
PAIRINGS = os.path.join(HERE, "pairings_batch4.json")
BLINDING = os.path.join(HERE, "..", "interpretations", "blinding_key_batch4.json")
OUTDIR = os.path.join(HERE, "..", "interpretations")

HEADER = """EVENT: {title}
HEXAGRAM LABEL: {label}
PRIMARY: {pnum} {pname} -> CHANGED: {cnum} {cname} (Line {line})
MUTUAL: {mutual}
"""


def load_bodies():
    bodies = {}
    for path in sorted(glob.glob(os.path.join(HERE, "bodies_batch4_*.json"))):
        with open(path) as f:
            bodies.update(json.load(f))
    return bodies


def main():
    with open(CASTS) as f:
        casts = json.load(f)
    with open(PAIRINGS) as f:
        pairing = {d["event_id"]: d["control_source"] for d in json.load(f)["pairings"]}
    with open(BLINDING) as f:
        blind = {d["event_id"]: d["real_is_A"] for d in json.load(f)["events"]}

    bodies = load_bodies()
    events = {r["event_id"]: r for r in casts["events"]}

    missing = [e for e in events if e not in bodies]
    if missing:
        print(f"WARNING: {len(missing)} bodies not yet written: {missing}")

    written = 0
    for eid, rec in events.items():
        if eid not in bodies or pairing[eid] not in bodies:
            continue
        real_h = rec["real_hexagram"]
        ctrl_h = rec["control_hexagram"]
        pairs = [
            ("A" if blind[eid] else "B", real_h, bodies[eid]),
            ("B" if blind[eid] else "A", ctrl_h, bodies[pairing[eid]]),
        ]
        for label, h, body in pairs:
            head = HEADER.format(
                title=rec["event_title"],
                label=label,
                pnum=h["primary_hexagram"]["number"],
                pname=h["primary_hexagram"]["name"],
                cnum=h["changed_hexagram"]["number"],
                cname=h["changed_hexagram"]["name"],
                line=h["changing_line"],
                mutual=h["mutual_hexagram"]["name"],
            )
            path = os.path.join(OUTDIR, f"{eid}_{label}.md")
            with open(path, "w") as f:
                f.write(head + "\n" + body.strip() + "\n")
            written += 1

    print(f"Wrote {written} interpretation files ({written // 2} events complete)")


if __name__ == "__main__":
    main()
