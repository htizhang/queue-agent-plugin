# Evaluation evidence

This entry preserves a compact account of an archived campaign and supplies a
fresh deterministic migration check. The archived campaign was not rerun for
this contribution.

## Archived fresh-seed campaign

The frozen policy was compared with 15 baseline variants, two tuned optimism
controls, and one constant-discount ablation:

- 45 capacity-grid and 36 width-grid synthetic configurations;
- capacities 32, 128, and 512 and target loads 0.55, 0.75, and 0.90;
- 20 new seeds generated after policy selection;
- 20,000 arrivals per run, 3,000 warmup arrivals, and full drain;
- 19 policies × 81 configurations × 20 seeds = 30,780 valid runs;
- identical job streams across policies within each case and seed; and
- equal-case geometric response ratios within each seed, averaged over seed
  blocks, with 95% percentile intervals from 10,000 whole-seed bootstrap
  resamples.

Positive reductions below mean lower mean response for queue-aware optimistic
backfilling.

| Comparator | Capacity grid | Width grid |
| --- | ---: | ---: |
| EASY-WFP3 | 24.23% [23.30, 25.19] | 26.04% [25.21, 26.90] |
| Selective reservation | 30.01% [28.88, 31.12] | 22.11% [21.31, 23.01] |
| Uniform discounted calendar | 26.24% [25.18, 27.22] | 29.94% [28.89, 30.95] |
| Selective-duration optimism | 27.83% [26.66, 28.83] | 30.65% [29.56, 31.71] |
| Constant-discount ablation | 0.71% [0.48, 0.94] | 0.45% [0.34, 0.57] |

The archived analysis reports lower aggregate mean response than every tested
baseline and control on both grids. Against EASY-WFP3, it also reports a lower
20-seed case-average ratio for all 45 capacity configurations and all 36 width
configurations. This is a comparison with the evaluated EASY-WFP3
implementation and synthetic grids, not a universal dominance claim.

These results support the mean-response comparison only. They do not establish
guarantees for tail response, slowdown, fairness, or another objective.

## Recalculate the objective comparison

[`archived_mean_response.json`](archived_mean_response.json) contains the
original full-precision, within-grid geometric candidate/comparator ratio for
each of the 20 seeds and five displayed comparisons. It is a field projection
of the frozen paired-analysis summary, not a new simulation. Seed order,
reported aggregates, confidence intervals, and the source hashes are retained;
unrelated policies, case-level ratios, subgroups, and secondary metrics are
omitted.

From this entry's directory, reproduce the point estimates and seed-block
counts:

```bash
python3 evaluation/verify_archived.py
```

Optionally reproduce the reported bootstrap intervals:

```bash
python3 evaluation/verify_archived.py --bootstrap
```

## What was and was not held out

The evidence is **fresh-seed evidence**: policy source and parameters were
frozen before the 20 stochastic streams were generated, and no tuning used
their outcomes.

It is **not unseen-configuration evidence**. All 81 model configurations were
already development configurations. The width cases originated as transfer
probes, but they were part of development before this final frozen run.
Performance in another queue or configuration therefore requires a new
evaluation.

An archived canary on an earlier seed reproduced 76 metric vectors exactly.
The final verification records complete paired coverage, zero failures, source
hash agreement, and no policy retuning.

## Fresh migration check

From this entry's directory:

```bash
python3 implementation/smoke_test.py
```

The check needs Python 3.10+ with only the standard library. It verifies the
queue-count duration formula, the maximum-fill reorder, and a backfill admitted by the shortened planning window
before an unshortened running-job release. It is a deterministic regression
fixture, not a rerun of the 30,780-run campaign.

During migration, the portable policy was also compared with the frozen source
on one deterministic 400-arrival stream for each of the 81 final
configurations. All 74,420 policy callbacks and resulting metric dictionaries
matched exactly. A second comparison on the four archived 20,000-arrival
canary cases matched another 213,438 callbacks and all metrics. These
source-oracle checks verify the extraction, not performance on new workloads.

## Provenance

These hashes identify the archived sources; they are not runtime dependencies.

| Source role | SHA-256 |
| --- | --- |
| Frozen policy wrapper | `7fcfa228c6492f9e1cc9b08214909b36e34e0d6b578e71d86b4e5120e9765672` |
| Frozen policy builder | `d955cfdd3e86791f012ceaf0ef92442f7fd93d68d360b805099a4b0f1f879db6` |
| Evaluation protocol | `d5166ecda499a4c32436fe9bb858983f451208e8d8a60575d47a4348c49bca7a` |
| Full simulation result | `81d8929f1f7dd828f2312c65a1223e44c5ec5f8a19cdc752b9376ca7e7cc5dbb` |
| Full paired-analysis summary | `820efb9f6c4ef592f4065c9197a8c26928580e1e304d3ebf17f45b74a5600441` |
| Compact campaign summary | `556c5146746f2b0f12a03c6fd073bc655e1b5012fc7bfbf2cc52275e8d850741` |
