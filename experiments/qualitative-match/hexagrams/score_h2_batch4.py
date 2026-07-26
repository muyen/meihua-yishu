#!/usr/bin/env python3
"""H2 scoring for batch 4, against the pre-registered base rates rather than 50%.

Run now (no outcomes): prints the null expectation the hexagram calls must beat.
Run after resolution: add `outcomes_batch4.json` mapping event_id -> "YES"/"NO"
(omit an event to drop it, per the protocol's drop-don't-replace stop rule).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EVENTS = os.path.join(HERE, "..", "events")
PREDS = json.load(open(os.path.join(HERE, "predictions_batch4.json")))["predictions"]
RATES = json.load(open(os.path.join(EVENTS, "base_rates_batch4.json")))["base_rates"]
OUTCOMES = os.path.join(EVENTS, "outcomes_batch4.json")


def poisson_binomial(ps):
    """Exact PMF of the number of successes for independent, unequal ps."""
    pmf = [1.0]
    for p in ps:
        nxt = [0.0] * (len(pmf) + 1)
        for k, v in enumerate(pmf):
            nxt[k] += v * (1 - p)
            nxt[k + 1] += v * p
        pmf = nxt
    return pmf


def main():
    ids = sorted(PREDS, key=lambda e: int(e[1:]))
    resolved = None
    if os.path.exists(OUTCOMES):
        resolved = json.load(open(OUTCOMES))
        ids = [e for e in ids if e in resolved]

    # Null probability that each hexagram-derived call is correct, given base rates only.
    q = [RATES[e]["p_yes"] if PREDS[e]["call"] == "YES" else 1 - RATES[e]["p_yes"] for e in ids]
    pmf = poisson_binomial(q)
    exp_hits = sum(q)
    n = len(ids)

    print(f"n = {n}")
    print(f"coin-flip baseline      : {n * 0.5:.1f} hits ({50.0:.1f}%)")
    print(f"base-rate null          : {exp_hits:.1f} hits ({100 * exp_hits / n:.1f}%)")
    print(f"  -> the base rates alone are worth {100 * (exp_hits / n - 0.5):+.1f}pt over a coin,")
    print("     which is the free lunch H2-vs-50% would have credited to the hexagrams.")

    subj = [e for e in ids if RATES[e]["method"] == "subjective"]
    print(f"  ({len(subj)}/{n} of the base rates are tagged `subjective` — the soft part of this test)")

    if resolved is None:
        print("\nNo outcomes_batch4.json yet. Window closes 2026-08-10; re-run then.")
        return

    hits = sum(1 for e in ids if PREDS[e]["call"] == resolved[e])
    p = sum(pmf[hits:])  # one-tailed: P(null does this well or better)
    print(f"\nobserved hits           : {hits} ({100 * hits / n:.1f}%)")
    print(f"one-tailed p vs base-rate null: {p:.4f}")
    print("H2 supported" if p < 0.05 else "H2 not supported")


if __name__ == "__main__":
    # Self-check: a fair coin over 10 events must centre the PMF on 5.
    _pmf = poisson_binomial([0.5] * 10)
    assert abs(sum(_pmf) - 1.0) < 1e-9 and _pmf.index(max(_pmf)) == 5
    main()
