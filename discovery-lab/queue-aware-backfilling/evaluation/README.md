# Evaluation evidence

This note reports an archived simulation campaign. The campaign was not rerun
for this entry. The bundled projection keeps the objective values and seed
ratios needed to recompute every number below. Separate checks, described at
the end, test that the portable code makes the evaluated decisions.

## Experimental design

The campaign used 81 synthetic configurations on two grids. Each grid crosses
its workloads with three capacities, `n` in {32, 128, 512}, and three load
targets, `ℓ` in {0.55, 0.75, 0.90}. The code-formatted labels are the
identifiers in the bundled data.

- **Workload-type grid, 45 configurations.** Widths are {1, n/8, n/2, 3n/4}.
  The first two types below use a 60-second mean for every class. The other
  three use class means of 30, 60, 120, and 240 seconds, in increasing order of
  width.
  - `balanced`: exponential service with equal class means.
  - `wide`: a larger share of wide jobs.
  - `correlated`: gamma service.
  - `heavy`: lognormal service.
  - `bursty`: alternating fast and slow blocks of 80 arrivals.
- **Width-mix grid, 36 configurations.** Four width mixes have four to six
  widths: powers of two (`pow2_5`), the four-level mix above (`v1like`), and
  two irregular mixes (`nonharm5`, `coprime6`). These workloads use Poisson
  arrivals, exponential service with a 60-second mean, and exact requests.

Requests are exact in 63 configurations. In the 18 `heavy` and `bursty`
configurations, each request is the actual duration multiplied by a factor
drawn from {1, 2, 4, 8}. The load target accounts for which widths can run
together. It measures the minimum fraction of time that feasible job packings
need to serve the mean demand of every class. It is not an observed
utilization.

Each run starts empty, generates 20,000 jobs, and continues until all of them
complete. The objective is the mean response time of the 17,000 jobs after the
first 3,000 arrivals. Each configuration uses eight seeds, so each policy has
81 × 8 = 648 workload realizations. In each realization, all policies receive
the same arrivals, job attributes, and class profiles.

The study froze the policy source, its parameter values κ = 2 and η = 1/8, and
the eight seeds before these runs. The configurations, however, were development
configurations. The results are therefore evidence about new realizations of
the same grid. They are not tests on unseen configurations or workload types.

## Aggregation

A comparison involves a candidate policy `P`, a comparator `B`, and a group
`C` of configurations. For seed `r`, the seed ratio is

```math
R_r=\exp\left\{\frac{1}{|C|}\sum_{c\in C}\log\frac{\bar T^{P}_{c,r}}{\bar T^{B}_{c,r}}\right\},
```

where `T̄` is the mean response time of one run. Each configuration has equal
weight. The reported reduction is `100 * (1 - mean of the eight R_r)`. A
positive reduction favors the candidate. The ablation and sensitivity tables
report the change in mean response time instead, which is the same quantity
with the opposite sign. Each interval is a pointwise 95% Student-t interval
across the eight seed ratios, with no adjustment for multiple comparisons.

## Results

### Published baselines

All 14 implementations of published methods are local implementations under
the same information and objective. LOS uses a lookahead depth of 50 jobs.
Selective reservation uses a slowdown threshold of 5.6848, calibrated on
separate development runs.

| Baseline | Reduction | 95% interval |
| --- | ---: | ---: |
| FCFS | 94.20% | [93.82%, 94.59%] |
| First-Fit | 35.55% | [33.50%, 37.61%] |
| MSF | 42.81% | [40.63%, 44.98%] |
| EASY-FCFS | 36.99% | [35.20%, 38.78%] |
| EASY-SJF | 41.74% | [40.44%, 43.05%] |
| **EASY-WFP3** | **26.43%** | **[25.10%, 27.76%]** |
| EASY-F1 | 59.74% | [58.62%, 60.85%] |
| Conservative FCFS | 28.16% | [26.55%, 29.76%] |
| Selective reservation | 27.36% | [25.70%, 29.03%] |
| LOS, short-job merit | 45.33% | [42.44%, 48.23%] |
| LOS, slowdown merit | 44.41% | [41.48%, 47.34%] |
| Adaptive Quickswap | 56.64% | [55.34%, 57.94%] |
| Balanced Splitting, FCFS | 94.12% | [93.76%, 94.48%] |
| SMASH, W = 200 | 42.47% | [40.37%, 44.58%] |

EASY-WFP3 is the strongest published baseline under this aggregation. The
reduction against it is 24.94% on the workload-type grid and 28.24% on the
width-mix grid.

### Forecast-assisted EASY-WFP3

The proposed policy uses public class means in its planning durations. To check
that this information alone does not explain the result, the campaign also constructed
controls that use these means in existing baselines. It tested two planning durations for
waiting jobs: the class mean, and the harmonic expression
`request * mean / (request + mean)`. It used them either everywhere a baseline
uses a waiting job's request or only in reservation calculations. These 26
settings (24 distinct) are locally constructed controls, not published
algorithms. Running jobs kept their raw requests in every control.

The strongest observed control keeps the EASY-WFP3 order and running-job
releases, and uses the harmonic expression only for the calendar durations of
waiting jobs. This **forecast-assisted EASY-WFP3** improves on original
EASY-WFP3 by 4.52% [4.05%, 5.00%]. The proposed policy improves on it by
**22.95% [21.73%, 24.17%]**. Against the 26 settings, the reductions range from
22.95% to 74.19%.

| Group of configurations | Configurations | Reduction | 95% interval |
| --- | ---: | ---: | ---: |
| All | 81 | 22.95% | [21.73%, 24.17%] |
| Workload-type grid | 45 | 22.92% | [21.07%, 24.76%] |
| Width-mix grid | 36 | 22.98% | [22.25%, 23.70%] |
| `n` = 32 | 27 | 21.24% | [20.02%, 22.46%] |
| `n` = 128 | 27 | 23.79% | [22.55%, 25.03%] |
| `n` = 512 | 27 | 23.79% | [22.55%, 25.03%] |
| Load target 0.55 | 27 | 2.96% | [2.77%, 3.15%] |
| Load target 0.75 | 27 | 13.41% | [12.35%, 14.46%] |
| Load target 0.90 | 27 | 45.53% | [43.45%, 47.62%] |
| Exact requests | 63 | 24.40% | [23.87%, 24.92%] |
| Conservative requests | 18 | 17.56% | [13.14%, 21.98%] |

The rows for `n` = 128 and `n` = 512 are equal only after rounding. The two
request groups contain different workload types, so their difference does not
isolate the effect of request accuracy. For each configuration, the geometric
mean of the eight paired ratios is below one in all 81 configurations against
forecast-assisted EASY-WFP3. The least favorable configuration has a change of
−0.65%. Against original EASY-WFP3, the ratio is also below one in all 81
configurations.

### Packing-repair ablation

This variant removes the packing repair and keeps the priority score, planning
durations, and calendar unchanged.

| Group of configurations | Change after removing the repair | 95% interval |
| --- | ---: | ---: |
| All | +0.80% | [+0.56%, +1.04%] |
| Workload-type grid | +0.95% | [+0.55%, +1.35%] |
| Width-mix grid | +0.62% | [+0.38%, +0.85%] |

Without the repair, the policy still improves on forecast-assisted EASY-WFP3
by 22.33% [21.16%, 23.51%]. The two parameters therefore control a small
additional correction, not most of the advantage.

### Parameter sensitivity

The sensitivity study ran all 25 combinations of κ in {1, 1.5, 2, 3, 4} and η
in {0, 1/16, 1/8, 1/4, 1/2}. It used the same 648 workload realizations, and
only the two constants changed. The table gives the change in mean response
time relative to the default (κ, η) = (2, 1/8). Positive values are worse. This
was a sensitivity study of frozen parameters, not a further selection step.

| κ \ η | 0 | 1/16 | 1/8 | 1/4 | 1/2 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | +3.67 | +0.57 | +0.52 | +0.51 | +0.80 |
| 1.5 | +4.54 | +0.43 | +0.24 | +0.25 | +0.80 |
| 2 | +4.77 | +0.36 | **0.00** | +0.18 | +0.80 |
| 3 | +5.32 | +0.33 | −0.19 | +0.01 | +0.80 |
| 4 | +5.62 | +0.57 | −0.28 | −0.09 | +0.80 |

- With a positive gain threshold, the 20 settings change the result by −0.28%
  to +0.80%. Each remains 22.33% to 23.17% better than forecast-assisted
  EASY-WFP3. In the nearby region κ in {1.5, 2, 3} and η in {1/16, 1/8, 1/4},
  the changes are −0.19% to +0.43%. The negative entries do not establish that
  those settings are better than the default.
- A zero threshold increases the result by 3.67% to 5.62%, and by 4.77%
  [4.06%, 5.48%] at κ = 2. Because the gain test uses ≥, η = 0 allows
  reorderings that fill no more servers than the priority order.
- The η = 1/2 column equals the result without the packing repair.
- Single configurations can be more sensitive. For the `nonharm5` mix at
  `n` = 512 and load target 0.90, the settings (3, 1/16) and (4, 1/16) increase
  mean response time by 21.68% and 25.36%. Each value is the geometric mean of
  the eight paired ratios in that configuration.

## Limits of the evidence

- The evidence covers mean response time only. It makes no claim about tail
  response time, slowdown, or fairness.
- Every policy received exact population class means. No test used means
  estimated from finite data.
- In the 63 exact-request configurations, the request already equals the actual
  duration. There, the harmonic expression is a planning device. It does not
  supply better knowledge of durations.
- Planning durations are not upper bounds on actual durations. Neither the
  proposed policy nor the forecast-assisted controls inherit the reservation
  guarantees of backfilling with upper-bound requests.
- The strongest-control designation is a descriptive choice from the reported
  panel. It does not exhaust possible redesigns of the baselines.

## Recompute the archived results

From this entry's directory, run:

```bash
python3 evaluation/verify_archived.py
```

The verifier needs Python 3.9 or later and only the standard library. It runs no
simulation. It recomputes the values above from
[`archived_mean_response.json`](archived_mean_response.json) and compares them
with the archived analysis values:

- It recomputes seed ratios, reductions, intervals, and per-configuration
  ratios from 2,592 bundled mean-response values. These values come from four
  policies on all 648 realizations: the proposed policy, the policy without
  the packing repair, EASY-WFP3, and forecast-assisted EASY-WFP3.
- It also uses the archived seed ratios for the other 13 published baselines,
  the 26 forecast-assisted settings, and the 25 sensitivity settings. From these
  ratios, it recomputes point estimates and intervals.
- It computes the Student-t quantile with the standard library. The archived
  analysis used SciPy for this quantile.
- It recomputes the single-configuration sensitivity values from 24 bundled
  mean-response values.

The projection keeps only the mean-response objective. It omits the remaining
policies' per-run values, other metrics, traces, and the simulator.

## Checks run for this entry

These checks test decisions, not performance. No new simulation campaign was
run for this entry.

- `python3 implementation/smoke_test.py` runs 15 deterministic tests with the
  standard library. Hand-built states check each mechanism. A further 300
  seeded states (474 policy calls, including repeated calls at one time) must
  reproduce decisions recorded from the evaluated source.
- During preparation, the portable policy and the evaluated source made
  identical decisions on a sample of 4,360 states (8,513 calls, including
  repeated calls). In 112 of these states, which had very large clock values,
  both implementations raised the same error. With the parameters changed, the
  portable policy also matched each of the 24 non-default sensitivity variants
  on 300 states (13,777 calls in total). This comparison needs the original
  source, so it is not shipped.

## Provenance

The `source_sha256` field in [the bundled data](archived_mean_response.json)
identifies the evaluated code, generators, result files, and analyses. These
hashes are not runtime dependencies. The forecast-control and sensitivity runs
each reproduced the proposed policy's 648 results exactly.
