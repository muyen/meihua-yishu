# Qualitative Match Experiment — Batch 4 Protocol

**Started**: 2026-05-07
**Predecessors**: Batch 1 (mechanical, n=12, excluded as non-blinded baseline), Batch 2 (取象法 LLM, n=20, p=0.011), Batch 3 (取象法 skill, n=15 of 30 scored, p=0.096)

## What this batch is for

Batches 2 and 3 produced p=0.006 combined (n=35) but the strongest critique remains: **the 取象法 procedure uses event semantics to pick the hexagram, while controls are drawn uniformly at random**. That makes the test partly tautological — "does a hexagram chosen using event imagery beat one chosen with no event input?"

Batch 4 is designed primarily to **kill that critique** by using **displaced 取象法 controls** — both real and control hexagrams come from the same imagery-driven procedure, applied to different events. If real still beats control under this design, the tautology dismissal no longer applies.

It also adds a **forced binary prediction** at casting time, giving us a real predictive test built into the experiment (not a post-hoc lookup like the failed ji_rate analysis).

## Headline design changes vs. Batch 3

| Aspect | Batch 3 | **Batch 4** |
|---|---|---|
| Sample size | 30 (15 scored so far) | **60** (locked in advance) |
| Control source | Uniform random hexagram | **Displaced 取象法 (different event)** |
| Resolution window | ~6 weeks (Apr-May) | **14 days (May 8-23)** |
| Predictive test | Post-hoc only (ji_rate) | **Forced binary prediction at casting time** |
| Scorer | Same agent as narrator | **Different cold session, no access to casting reasoning** |
| Rubric | 0-5, intuitive | **0-5 with locked anchored examples** |
| Pre-registration | Implicit (git history) | **Explicit n + stop rule + rubric written before casting** |

## Sample size and stop rule

- **n = 60**, locked. No early stopping on a good number, no extension on a bad number.
- If any events fail to resolve within the 14-day window (e.g. launch deferred, postponed game), they are dropped and replacement events are NOT added. Final n is whatever resolved.
- Wilcoxon signed-rank, one-tailed, H₁: real > control, ties dropped (zero_method="wilcox").
- Binary prediction accuracy reported as raw hit rate vs. 50% null + binomial p-value.

## Domain mix (event registry)

Target distribution across 60 events:

| Domain | Target | Resolution time | Sources |
|---|---:|---|---|
| Sports | 18 | 1-3 days | NBA Conference Finals games, NHL playoff games, MLB games, French Open Round 1, Champions League final, Euro qualifiers |
| Markets / Earnings | 10 | 1 day | Q1 2026 earnings beats/misses, single-day stock moves on news |
| Politics | 8 | 1 day | UK council, Cape Verde, Colombia round 1, parliamentary votes |
| Culture | 8 | 3 days | Movie opening weekends, Eurovision, Cannes openers, awards |
| Tech | 8 | 1-2 days | Google I/O, Dell Tech World, Microsoft Build, AWS re:Inforce |
| Science / misc | 8 | 1-7 days | Rocket launches, scheduled experiments, weather extremes |

## Casting protocol

### Real hexagrams
For each event X, run the meihua-yishu skill with event_X title + description as input. Record full skill output (取象理由, 體用, 策略, 爻位風險, ji_rate).

### Displaced controls (NEW)
For each event X, generate the control hexagram by running the **same 取象法 skill on a different event Y**, where the X→Y pairing is determined by `pairing_seed` before any casting begins. This means:

- Both real and control come from the same imagistic procedure
- Both are equally "creative" / equally "loaded with event imagery"
- The only difference is whether the imagery comes from the *correct* event or a *random other* event
- If real still beats control, it's no longer "we used event semantics on one side and not the other"

Pairing rules:
- Each event Y is used as a control source for at most one event X (no reuse)
- An event cannot be its own control (X ≠ Y)
- Pairing is deterministic from `pairing_seed`

### Forced binary prediction
At casting time, the interpreter (using only the real hexagram + event description) outputs **one explicit binary prediction** about the event outcome. Examples:
- "Knicks win Game 5: YES"
- "NVDA beats Q1 EPS estimate: NO"
- "Sub-2:00 marathon set: YES"

The prediction is recorded in the casting record alongside the hexagram. After resolution, predictions are scored as hit/miss/N/A.

## Blinding

- **Blinding seed**: deterministic A/B label randomization per event
- **Blinding key**: sealed JSON file in `interpretations/blinding_key_batch4.json`, NOT to be opened until all scoring is complete
- Both real and control interpretations are written without revealing which is which

## Roles (separate cold sessions)

To break the narrator/scorer leak risk:

1. **Caster/Interpreter**: full session with skill, knows real vs. control mapping. Writes the two interpretation files (A/B labeled).
2. **Narrator**: fresh session, given ONLY event title + post-event factual sources (web research). Writes purely factual narrative. NO access to interpretations or casting reasoning.
3. **Scorer**: fresh session, given event narrative + interpretations A and B. Knows the rubric. NO access to casting reasoning, NO access to which is real.
4. **Unblinder + Statistician**: opens blinding key, computes Wilcoxon and binary accuracy. Last role.

Each role is a separate Claude session with no carry-over context.

## Locked rubric (0-5 scale)

| Score | Anchor |
|---|---|
| **0** | Opposite tone OR contradicts what happened. Reading says "decline / retreat" but the event was a clear advance. |
| **1** | Significantly off. Reading describes a domain or character clearly different from what occurred. |
| **2** | Vaguely related. Some surface words match but no specific imagery hits. Could fit many events. |
| **3** | General tonal fit. Captures the energy or arc but doesn't match specific details. |
| **4** | Clear specific match. At least one piece of imagery in the reading maps cleanly onto a specific feature of what happened. |
| **5** | Striking match. Multiple specific imagery hits AND/OR a single hit that would surprise a skeptical reader. |

The scorer is shown these anchors at the start of every scoring session.

## Binary prediction scoring

For each event with a forced binary prediction:
- **Hit**: prediction matches outcome
- **Miss**: prediction contradicts outcome
- **N/A**: event drift (didn't resolve in window) OR prediction was ambiguous given the actual resolution

Reported metrics:
- Raw hit rate (hits / (hits + misses))
- Binomial p-value vs. 50% null
- Hit rate among events where qualitative score was high (≥4) — does descriptive fit correlate with predictive accuracy?

## Timeline

| Day | Activity |
|---|---|
| **Day 0** (May 7) | Source 60 events. Lock event registry. Generate pairing_seed and blinding_seed. |
| **Day 0** (May 7) | Write protocol, rubric anchors, prediction format. SEAL THIS FILE. |
| **Day 1** (May 8) | Cast 60 real hexagrams + 60 displaced controls. Write 120 interpretation files. Record forced binary predictions. Seal blinding key. |
| **Days 1-14** (May 8-22) | Events resolve in real time. No interim peeking. |
| **Days 15-18** (May 22-25) | Narrator (cold session) writes 60 factual narratives. |
| **Days 18-21** (May 25-28) | Scorer (cold session) scores 120 interpretations using locked rubric. |
| **Day 21** (May 28) | Unblind. Compute Wilcoxon. Compute binary accuracy. Write up. |

## File structure

```
experiments/qualitative-match/
├── protocol_batch4.md                          (this file — SEAL after writing)
├── events/
│   └── event_registry_batch4.json              (60 events with binary outcome definitions)
├── hexagrams/
│   ├── pairing_seed_batch4.txt                 (seed for displaced control pairing)
│   ├── pairings_batch4.json                    (X→Y mapping)
│   ├── blinding_seed_batch4.txt                (seed for A/B randomization)
│   ├── generate_batch4.py                      (pairing + blinding generation)
│   └── casting_records_batch4.json             (real + control + binary predictions)
├── interpretations/
│   ├── E63_A.md ... E122_B.md                  (120 blinded interpretation files)
│   └── blinding_key_batch4.json                (SEALED until scoring complete)
├── evaluations/
│   ├── narratives_batch4.md                    (factual narratives, written cold)
│   └── scoring_batch4.md                       (scores, written cold)
└── analysis/
    └── batch4_results.md                       (final unblinded analysis)
```

## Pre-registered hypotheses

**H1 (descriptive fit, primary)**: Real hexagram interpretations score higher than displaced-control interpretations on the locked 0-5 rubric. One-tailed Wilcoxon p < 0.05 declares the result significant.

**H2 (predictive accuracy, secondary)**: Forced binary predictions made from real hexagrams hit at a rate above 50%. Binomial p < 0.05 declares the result significant.

**H3 (correlation, exploratory)**: Among events where the real interpretation scored ≥4, the binary prediction hit rate is higher than among events where it scored ≤2. (Tests whether descriptive fit and predictive accuracy track each other.)

## What a positive result here would mean

A win on H1 alone (under displaced controls) would be substantially stronger than Batches 2-3, because it can no longer be explained by "we used event semantics on real but not control." It would demonstrate that 取象法 *applied to the right event* produces better-fitting interpretations than 取象法 *applied to a wrong event* — even when both procedures use equally rich imagery generation.

A win on H2 (binary predictive accuracy) would be the first directly profitable result in the experiment series — and the first that ji_rate failed to deliver post-hoc.

## What a null result here would mean

A null on H1 with displaced controls (after positive results on uniformly-random controls) would be **strong evidence** that the prior signal was the tautology effect — and the I Ching's apparent descriptive power was the LLM finding semantic affinities in any imagistically-rich text, not a property of the *correct* hexagram for an event.

That's also a publishable finding. Both directions teach something.

## Pre-registration commitment

This protocol is committed to git BEFORE event registry is finalized and BEFORE casting begins. n=60, rubric anchors, and analysis plan are locked. Any deviation requires an amendment commit explicitly acknowledging the change and reason.
