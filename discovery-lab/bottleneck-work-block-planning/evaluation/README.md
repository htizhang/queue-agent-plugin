# Evaluation evidence

This note reports archived research results. This entry did not rerun the
simulation study. The [compact projection](archived-flow-means.json) and its
verifier recompute the reported values from archived objective data. The
policy smoke test checks decision logic only.

## Study design

**Policies.** The study compared 22 policies on identical workloads:

- bottleneck-work block planning with the fixed weight $\beta=8$
- ten baseline variants: FCFS, SEPT, least remaining route work, SPSU, SPTNS,
  FCFSNS, MMS, WORK, and PR in raw and in normalized time units
- two current-operation-only planners
- the proposed policy with the nine other weights of the sensitivity grid

All policies receive the same state. The rules use different parts of it. The
ablation planners receive the same routes and means as the proposed policy.
They plan with the current-operation mean $p_j$ instead of the remaining
bottleneck work $w_j$.

**Configurations.** The study used 27 synthetic configurations: three network
layouts, three setup contrasts, and three pairs of setup ratio and load per
layout. Each layout has three products. Station 0 or 1 is the single-server
bottleneck.

| Layout | Servers per station | Bottleneck | Recipes | Arrivals | Service | Initial recipe | Asymmetry |
| --- | --- | ---: | --- | --- | --- | --- | ---: |
| Two stations, four recipes | 1, 2 | 0 | A1, A2, B1, B2 | Poisson | exponential | B2 | 0 |
| Three stations, six recipes | 2, 1, 2 | 1 | A1, A2, B1, B2, C1, C2 | renewal, SCV 2 | lognormal, SCV 2.25 | C2 | +0.25 |
| Four stations, six recipes | 1, 3, 2, 2 | 0 | A1, A2, A3, B1, B2, B3 | renewal, SCV 2 | gamma, SCV 2 | B3 | −0.25 |

SCV is the squared coefficient of variation. Renewal interarrival times are
gamma distributed. Each route step below is `station:mean` or
`station:mean:recipe`:

| Layout | Product (probability): route |
| --- | --- |
| Two stations | A (0.35): 0:14:A1, 1:20, 0:6:A2, 1:12 · B (0.30): 0:10:B1, 1:16, 0:8:A1 · C (0.35): 0:12:A2, 1:18, 0:7:B2, 1:9 |
| Three stations | A (0.40): 0:16, 1:20:A1, 2:14, 1:10:A2, 2:8 · B (0.35): 0:12, 1:18:B1, 2:10, 1:6:C1 · C (0.25): 0:10, 1:14:C2, 2:12, 1:9:B2 |
| Four stations | A (0.40): 0:12:A1, 1:30, 2:16, 0:10:A2, 3:18, 0:8:A3 · B (0.35): 0:14:B1, 1:24, 2:12, 0:6:B2 · C (0.25): 0:9:A3, 3:15, 0:5:B3 |

The letter of a recipe names its family. The unit setup time from recipe $a$
to recipe $b \ne a$ is 1 inside a family. Across families, it is the contrast
times $1+\text{asymmetry}$ when $a<b$ in label order, and times
$1-\text{asymmetry}$ otherwise. The generator then scales the matrix. Draw two
recipes independently, each with its frequency among bottleneck visits. Their
expected setup time equals the setup ratio times the mean duration of a
bottleneck operation. A higher contrast therefore moves setup time between
changes inside and across families. It does not change this reference average.

The arrival rate makes the busiest station's processing-only load per server
equal to the nominal load. That station is the bottleneck. The nominal load
excludes the setup work that a policy causes. A Latin square pairs the setup
ratio and load levels. The grid crosses each pair with the contrasts 1, 4, and
12:

| Layout | (setup ratio, nominal load) pairs |
| --- | --- |
| Two stations | (0.05, 0.55), (0.20, 0.70), (0.50, 0.85) |
| Three stations | (0.05, 0.70), (0.20, 0.85), (0.50, 0.55) |
| Four stations | (0.05, 0.85), (0.20, 0.55), (0.50, 0.70) |

This is a compact grid, not a full factorial design. Each layout also fixes
routes, product mix, variability, asymmetry, and the initial recipe.
Comparisons between layouts therefore do not isolate one cause.

**Randomness and runs.** Each configuration used 16 fresh seeds, listed in the
projection. A seed fixes the arrivals, product classes, and service times, so
one configuration and seed form a workload. Every policy ran on the same 432
workloads. Each run generated 400 warm-up arrivals, 1,500 measured arrivals,
and 1,200 further arrivals. The simulation then continued without arrivals
until all 3,100 jobs left. The objective counts the fixed 1,500-job cohort.
All 9,504 runs completed their cohorts.

**Parameter selection.** The study fixed all settings before the validation
runs:

- The study selected $\beta=8$ on eight development seeds of the same 27
  configurations. It used the grid 1, 2, 4, 5, 6, 8, 12, 16, 24, 32. The
  margin was small: 210.269 at $\beta=8$ and 210.285 at $\beta=12$.
- A calibration on development data chose PR's $\theta=5$ in raw time and
  $\theta=16$ in normalized time. The raw value is the largest value of its
  search grid. The normalized value is an interior optimum.
- A selection on the same eight development seeds chose $\beta=6$ for the
  second current-operation-only planner, in 2,160 runs (217.337, against
  217.668 at $\beta=8$).

A scan of the earlier experiment files found no prior use of the 16 validation
seeds. The validation runs are fresh realizations of the development
configurations. They are not evidence about unseen layouts or another queue
family.

## Aggregation

For policy $P$, let $\bar F_P$ be the arithmetic mean of its 432 run-level mean
flow times. Every configuration and seed has equal weight. The reduction
relative to comparator $B$ is

```math
100\,\bigl(1-\bar F_P/\bar F_B\bigr)\,\%.
```

A positive value favors the proposed policy. The reduction compares pooled
means. It is not an average of configuration percentages and not a geometric
mean of ratios. Configurations with long flow times therefore have more
influence.

A configuration counts as won when the policy has the lower mean over its 16
seeds. A difference within $10^{-10}$ percent counts as a tie.

Each interval is a paired percentile bootstrap with 20,000 resamples of the 16
seeds. A sampled seed carries all 27 configurations and both policies, so the
comparison stays paired. Each resample computes the reduction from the pooled
means of its drawn seeds. The intervals describe uncertainty over random
realizations of this fixed grid. For the ten baselines, 99.5% intervals give an
approximate Bonferroni adjustment for ten comparisons. Layout rows repeat these
calculations on the 9 configurations of one layout.

## Results

### Baseline panel

The proposed policy has pooled mean flow time **215.606**. Normalized PR has
the lowest mean among the baselines, at 237.251. Relative to it, the
reduction is **9.12%**, with 95% interval **[6.88%, 12.09%]**.

| Baseline | Mean flow time | Reduction | 95% interval | 99.5% interval | Configurations won / 27 |
| --- | ---: | ---: | ---: | ---: | ---: |
| PR, normalized, $\theta=16$ | 237.251 | 9.12% | [6.88%, 12.09%] | [6.55%, 13.54%] | 23 |
| PR, raw time, $\theta=5$ | 238.941 | 9.77% | [8.16%, 11.77%] | [7.80%, 12.70%] | 23 |
| SPTNS | 238.997 | 9.79% | [8.30%, 11.77%] | [7.98%, 12.74%] | 26 |
| MMS | 249.604 | 13.62% | [12.26%, 15.42%] | [11.99%, 16.29%] | 27 |
| FCFSNS | 282.824 | 23.77% | [21.96%, 25.95%] | [21.55%, 26.98%] | 27 |
| SPSU | 330.381 | 34.74% | [30.37%, 38.38%] | [28.40%, 39.63%] | 24 |
| Least remaining route work | 1,423.082 | 84.85% | [83.83%, 85.78%] | [83.37%, 86.11%] | 24 |
| SEPT | 1,529.660 | 85.91% | [85.12%, 86.65%] | [84.75%, 86.93%] | 24 |
| WORK | 2,001.243 | 89.23% | [88.58%, 89.79%] | [88.25%, 90.02%] | 27 |
| FCFS | 2,065.088 | 89.56% | [89.00%, 90.09%] | [88.73%, 90.33%] | 27 |

All 20 intervals have positive lower bounds. The proposed policy loses 4 of
the 27 configurations to each PR variant and 1 to SPTNS. It loses 3 to each of
SPSU, least remaining route work, and SEPT. The comparison concerns these
implementations and settings, not every published policy.

SEPT, least remaining route work, and WORK still had measured jobs in the
system when arrivals stopped in 48, 48, and 31 runs. The largest such backlog
was 298 jobs. The study drained and kept these runs. Their large reductions are
finite-horizon results and do not establish steady-state behavior.

| Layout | Reduction vs normalized PR | 95% interval | Configurations won / 9 |
| --- | ---: | ---: | ---: |
| Two stations, four recipes | 3.07% | [2.40%, 3.71%] | 5 |
| Three stations, six recipes | 6.71% | [5.78%, 7.69%] | 9 |
| Four stations, six recipes | 14.98% | [10.07%, 20.03%] | 9 |

All four losses to normalized PR occur in the two-station layout. The
advantage is an aggregate result, not a win in every configuration.

### Contribution of remaining bottleneck work

The current-operation-only planner keeps the types, the exact search, the
score, the tie rule, one-operation execution, and SEPT at setup-free stations.
Only its planning duration differs. The matched version uses $\beta=8$. The
second version uses its own development-selected $\beta=6$.

| Current-operation-only planner | Mean flow time | Reduction | 95% interval | Configurations won / 27 |
| --- | ---: | ---: | ---: | ---: |
| Matched, $\beta=8$ | 224.348 | 3.90% | [2.56%, 5.80%] | 25 |
| Development-selected, $\beta=6$ | 224.284 | 3.87% | [2.46%, 5.89%] | 25 |

| Layout | Reduction vs matched $\beta=8$ | Reduction vs selected $\beta=6$ | Won / 9 (both) |
| --- | ---: | ---: | ---: |
| Two stations | 0.95% [0.58%, 1.34%] | 0.84% [0.68%, 1.01%] | 9 |
| Three stations | −0.31% [−1.02%, 0.42%] | −0.61% [−1.02%, −0.17%] | 7 |
| Four stations | 9.76% [7.00%, 12.67%] | 10.01% [7.01%, 13.16%] | 9 |

The gain is largest in the four-station layout, where one product visits
the bottleneck three times. In the three-station layout, the proposed policy
has a slightly higher mean than both planners. The interval includes zero
against the matched planner and excludes zero against the selected planner.

The gain is not only fewer changeovers. Over each complete run of 3,100 jobs,
the matched planner averaged 3,363 changeovers and the proposed policy 3,601.
These counts come from archived whole-run diagnostics, not from cohort
objective values.

### Setup-weight sensitivity

The rows repeat the 432 workloads with other weights. They describe
sensitivity and do not select a new weight. The change is
$100(\bar F_\beta/\bar F_8-1)\%$, so positive values are worse than
$\beta=8$. Development means come from the eight earlier seeds, so their level
differs from the validation means.

| $\beta$ | Development mean | Validation mean | Change vs $\beta=8$ | 95% interval |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 271.527 | 301.277 | +39.74% | [+31.27%, +48.30%] |
| 2 | 234.756 | 247.968 | +15.01% | [+11.29%, +18.73%] |
| 4 | 215.353 | 222.109 | +3.02% | [+2.05%, +3.92%] |
| 5 | 212.711 | 218.525 | +1.35% | [+0.84%, +1.82%] |
| 6 | 211.185 | 217.007 | +0.65% | [+0.33%, +0.97%] |
| **8** | **210.269** | **215.606** | **0.00%** | -- |
| 12 | 210.285 | 215.285 | −0.15% | [−0.48%, +0.20%] |
| 16 | 211.461 | 216.416 | +0.38% | [−0.14%, +0.92%] |
| 24 | 213.555 | 218.169 | +1.19% | [+0.46%, +1.90%] |
| 32 | 215.349 | 219.816 | +1.95% | [+1.12%, +2.72%] |

For the weights 6, 12, and 16, the validation means differ from $\beta=8$ by
less than 0.66%. The lowest validation mean is at $\beta=12$. It is only 0.15%
below $\beta=8$, and its interval includes zero. The weight itself still
matters. At $\beta=1$, the policy averaged 4,236 changeovers per complete run
and flow time was 39.74% higher. At $\beta=32$, changeovers fell to 3,267, but
flow time was 1.95% higher.

### Further qualifications

- The simulation code and the statistical plan were frozen before the first
  validation run. The analysis script was written while the validation runs
  were in progress. It implements the frozen plan.
- Contrast 1 is the low-structure control. With zero asymmetry, every change
  between different recipes takes the same time. With asymmetry, a change
  across families and its reverse can have different durations.
- Drained finite cohorts do not establish stability for any policy.

## Recalculate the reported values

[archived-flow-means.json](archived-flow-means.json) is a field projection of
the archived analysis. For each policy, it keeps the pooled mean, the 27
configuration means, and the 16 seed means. For each layout, it keeps the seed
means of the four policies in the layout comparisons. It also keeps the
reported reductions, intervals, and configuration counts of 31 comparisons.
The projection copies values without rounding. A check against the raw run
values found every stored mean within $10^{-15}$ relative error. The projection
omits individual runs, secondary metrics, and other subgroups.

From this entry's directory, run:

```text
python3 evaluation/verify_archived.py
```

This check needs only the Python 3.10+ standard library. It recomputes every
pooled mean, reduction, and configuration count. It also asserts the interval
signs and other statements cited above. It does not recompute the intervals.

With NumPy installed, this command also recomputes all 41 archived intervals:

```text
python3 evaluation/verify_archived.py --bootstrap
```

It regenerates the archived draws with this call:

```python
numpy.random.default_rng(1011).integers(0, 16, size=(20000, 16))
```

It takes the 0.025 and 0.975 quantiles of the resampled reductions. For the
baselines, it also takes the 0.0025 and 0.9975 quantiles. NumPy's default
linear quantile method applies. The archived analysis used NumPy 1.26.4. For
this entry, NumPy 1.26.4 and 2.4.6 both reproduced every interval exactly.

## Checks run for this entry

These checks test the extraction, not performance:

- **Smoke test:** `python3 implementation/smoke_test.py` runs 14 tests with
  hand-calculated fixtures and a brute-force comparison on 300 random queues.
- **Decision parity:** the portable policy matched the frozen source,
  `make(fixed_beta=β)`, in 34,065 comparisons of a state and a weight. The
  7,485 states included 1,458 simulator-built bottleneck queues from all 27
  configurations, with 1 to 55 jobs and up to 7 types. They also included
  6,000 random states outside the family, with up to 12 types, and 27 states
  without an installed recipe. No call changed its input state.
- **Unused record:** the frozen source updates an occupancy record that a
  fixed weight never reads. A static check of the source shows that the record
  cannot change a decision. Source instances with arbitrary earlier records
  also made the same choices as fresh instances.
- **Simulation sample:** on three archived workloads, one per layout at its
  highest load, the portable policy ran all ten weights. The 30 dispatch
  sequences (391,480 decisions) and all 11 metrics of each run equal the
  archived validation rows. At $\beta=8$, the frozen source agreed at all
  39,148 decisions.

This entry did not replay the full validation grid with the portable code.

## Provenance

The `source_sha256` field in [the bundled data](archived-flow-means.json)
identifies the evaluated code, simulator, configuration generator, and result
files. These hashes are not runtime dependencies. The archived runs used
Python 3.12.12. This entry retains the objective-data projection, not the full
simulation campaign.
