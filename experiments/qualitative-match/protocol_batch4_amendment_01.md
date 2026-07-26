# Batch 4 — Amendment 01: date window and event registry

**Date**: 2026-07-26
**Amends**: `protocol_batch4.md` (sealed 2026-05-07)
**Status of the original**: written, sealed, committed — **never executed**.

---

## What changed

| Item | Original (2026-05-07) | Amended |
|---|---|---|
| Casting day | 2026-05-08 | **2026-07-27** |
| Resolution window | 2026-05-08 → 05-23 (14 days) | **2026-07-27 → 08-10 (14 days)** |
| Event registry | Never built | Built 2026-07-26 from events scheduled in the new window |
| Narration / scoring | ~May 22-28 | ~Aug 11-17 |

**Window length is unchanged at 14 days.** The events are different because they must be.

## What did NOT change

Everything that could bias the result:

- **n = 60, locked.** No early stop, no extension, no replacement of dropped events.
- **Displaced 取象法 controls** — the design feature this batch exists to test.
- **Both seeds.** `pairing_seed_batch4.txt` (20260507) and `blinding_seed_batch4.txt` (20260508)
  were committed 2026-05-07 and are **untouched**. The pairing derangement and the A/B blinding
  assignment are functions of the seed and the event-ID list (E63–E122), both of which were fixed
  before this amendment. The randomization was pre-committed and is not being re-rolled now.
- **Locked 0–5 rubric anchors.**
- **Three separate cold sessions** for caster / narrator / scorer.
- **H1, H2, H3** as pre-registered. Wilcoxon one-tailed, ties dropped, `zero_method="wilcox"`.

## Why the dates had to move

Batch 4's whole purpose is to remove two confounds from the n=62 result. Retrospective casting
would introduce a third and worse one: the caster (an LLM with web access and a training cutoff
inside the original window) could know the outcomes. Prospective casting is load-bearing for
this design, so a lapsed window cannot be reused. New window, same everything else.

## Known weakness introduced by this amendment

The event registry was assembled on 2026-07-26 by the same agent that will do the casting.
That was also true of batch 3, and it is not what batch 4 was built to fix — but it should be
recorded rather than discovered later. Mitigations:

1. Every event carries an outcome definition that resolves from public record, written before casting.
2. Each event is tagged `source_confidence`: `verified` (date confirmed by search on 2026-07-26)
   or `inferred` (scheduled event whose exact date/format was not separately confirmed).
3. The registry is committed **before** any hexagram is cast.
4. Per the original stop rule: events that fail to resolve in the window are **dropped, not replaced**.
   Final n is whatever resolves. If drop-out is heavy, the reported n falls and the power falls with it.

## Clarification: interpretation text is written once per cast

The original protocol says the control hexagram for event X comes from running 取象法 on event
Y = pairing[X]. Because the pairing is a single-cycle derangement over the same 60 events, Y's
control hexagram *is* Y's real hexagram. The interpretation text is therefore written **once per
cast** and used twice: as Y's real reading and as X's control reading, byte-identical.

This is a tightening, not a loosening. If control readings were written separately, the caster
could — without intending to — write thinner prose for the ones they know are controls. Reusing
the identical text makes that impossible. `verify_batch4_seal.py` asserts the byte-identity.

## Prior expectation, recorded before casting

Stating this so it cannot be adjusted afterwards. The two strongest signals already in hand both
point at null: batch 3 completed null (mean diff +0.23, p = 0.27), and the final 15 events —
the only ones scored with the narrator/scorer roles genuinely separated — came in **negative**
(−0.40, 5–7–3 favouring the control). **The expectation for batch 4 is a null on H1.**

A null here, under displaced controls, is the informative outcome: it would attribute the
earlier p = 0.021 to the tautology effect — imagistically rich text fitting events regardless of
which hexagram produced it. The protocol already says both directions are publishable. This
amendment does not change that and does not lower the bar for calling a positive result.
