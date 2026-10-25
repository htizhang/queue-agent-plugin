# Bottleneck-work block planning

> **Discovery Lab status:** This is an agent-discovered policy for exploratory
> research. It is not peer-reviewed queueing knowledge or an authoritative
> baseline. Its evidence applies only to the configurations and comparators in
> the [evaluation note](evaluation/README.md).

## Problem

The policy dispatches jobs in an open multiclass reentrant network. Jobs arrive
from outside, follow the fixed route of their product class, and leave after
their last operation. A job can visit the same station several times. An
arriving job belongs to product class $c$ with probability $q_c$. Class $c$ has
the route

```math
\mathcal R_c=\bigl((s_{c1},p_{c1},r_{c1}),\ldots,(s_{cL_c},p_{cL_c},r_{cL_c})\bigr).
```

Operation $\ell$ takes place at station $s_{c\ell}$ and has mean processing time
$p_{c\ell}>0$. Actual processing times are random. At the bottleneck station
$b$, the operation also needs recipe $r_{c\ell}$, which is a machine setting.

The bottleneck has one server and keeps its installed recipe between jobs. A
change from recipe $r$ to recipe $r'$ is a changeover. It takes the
deterministic setup time $S_{rr'}\ge 0$, with $S_{rr}=0$. The setup matrix $S$
can be asymmetric. All other stations are setup-free and can have several
identical servers.

Every policy obeys four rules:

1. Changeovers and operations are nonpreemptive.
2. A dispatch selects a job that is already waiting. The bottleneck changes
   directly to the job's recipe and then processes the job's current operation.
3. A changeover cannot start for an operation that is not yet waiting.
4. A free server must start a waiting job. The policy cannot keep a server
   idle, reject work, or start a batch.

The objective is the mean whole-network flow time of a fixed cohort
$\mathcal J$ of scored jobs:

```math
\overline F=\frac{1}{|\mathcal J|}\sum_{j\in\mathcal J}(d_j-a_j).
```

Here $a_j$ is the external arrival time of job $j$ and $d_j$ is its final
departure time. Flow time includes all waiting, setup, and processing along the
route.

### Observations and actions

At each decision, every compared policy can observe:

- the current time and the queues at all stations
- the number of servers at each station and the recipe installed at the
  bottleneck
- each waiting job's product class, current operation, and station-arrival
  time, which is the time at which the job joined its current queue
- the product probabilities, the routes, and the mean processing times
- the setup matrix

No policy sees future arrivals, the actual processing times of unfinished
operations, or scheduled completion times. A decision occurs when a server is
free and its queue is not empty. The action is the identifier of one waiting
job. The simulator then performs the required changeover and the operation.

This policy reads only the queue at the deciding station, the installed recipe,
the routes, the mean processing times, and the setup matrix. Station-arrival
times and job identifiers break ties. A choice does not depend on earlier
decisions.

## Policy

At a setup-free station, the policy uses SEPT (shortest expected processing
time). It starts the job with the smallest current-operation mean $p_j$. Equal
means go to the earliest station-arrival time, then to the smallest identifier.

At the bottleneck, each decision balances two delays. A changeover uses
capacity without processing a job. Staying on the installed recipe makes the
jobs that need other recipes wait. To compare these delays, the policy builds a
virtual plan: a schedule of the whole bottleneck queue that exists only inside
the policy. It then starts one real operation and plans again at the next
decision.

### 1. Count the return visits

A job with a short current operation can still need long operations at later
bottleneck visits. For job $j$ of product $c_j$ at operation $\ell_j$, the
policy uses the remaining bottleneck work

```math
w_j=\sum_{\substack{\ell_j\le \ell\le L_{c_j}\\ s_{c_j\ell}=b}} p_{c_j\ell}.
```

The sum includes the current operation and every later operation at the
bottleneck. It excludes work at other stations. The quantity $w_j$ is a
planning duration only. It does not predict when the job leaves the bottleneck
or the network.

### 2. Plan job types as blocks

A type is the set of waiting jobs with the same product and the same current
operation. The route fixes the recipe of that operation. All jobs of type $g$
therefore share the recipe $r_g$ and the same remaining work. Let

```math
n_g=|g|,\qquad W_g=\sum_{j\in g}w_j .
```

The first job of a type is the job with the earliest station-arrival time, then
the smallest identifier.

In the virtual plan, each type is one contiguous block. Two types are different
blocks even when they need the same recipe. For example, one job can need
recipe A now and return later. Another job can need A for its last visit. Their
remaining work can differ, but a grouping by recipe alone would merge them.
Consecutive blocks with the same recipe need no setup time, because $S_{rr}=0$.

### 3. Score a block order

Let $\sigma=(g_1,\ldots,g_M)$ be an order of all $M$ present types. Let
$N_k=\sum_{h\ge k}n_{g_h}$ be the number of jobs in block $k$ and the later
blocks. The installed recipe $r_0$ precedes the first block. The score of the
order is

```math
K_\beta(\sigma)=\sum_{k=1}^{M}\Bigl[N_k\,\beta\,S_{r_{g_{k-1}}r_{g_k}}
+\bigl(N_k-n_{g_k}\bigr)W_{g_k}\Bigr],\qquad r_{g_0}=r_0,\quad \beta=8.
```

The first term charges the changeover before block $k$. That changeover delays
all $N_k$ jobs that remain in the plan, and the weight $\beta$ multiplies its
setup time. The second term charges the processing of block $k$. Its planned
work $W_{g_k}$ delays every job in the later blocks.

The score has a direct meaning. Consider a virtual schedule in which job $j$
lasts $w_j$ and each changeover lasts $\beta S$. The total completion time of
the waiting jobs in that schedule equals $K_\beta(\sigma)$ plus a term that
does not depend on the order. A lower
score is therefore a lower total virtual completion time. The virtual schedule
only ranks the options. It is not a forecast, and the policy does not claim to
minimize actual network flow time.

The policy uses one weight, $\beta=8$, for all decisions and configurations.
The study selected it on development runs before validation. A physical
changeover still takes $S_{rr'}$, not $8S_{rr'}$. A larger weight makes the
plan avoid changeovers more strongly. In the evaluation, a much smaller or much
larger weight increased mean flow time.

### 4. Search every order exactly

$M$ types have $M!$ orders. The policy finds the best order by dynamic
programming over subsets of types. For a set $U$ of unplanned types that
follows recipe $r$, let $N(U)=\sum_{g\in U}n_g$. The smallest cost that these
blocks can add is

```math
V(\varnothing,r)=0,\qquad
V(U,r)=\min_{g\in U}\Bigl\{N(U)\,\beta\,S_{r\,r_g}
+\bigl[N(U)-n_g\bigr]W_g+V\bigl(U\setminus\{g\},r_g\bigr)\Bigr\}.
```

Let $\mathcal G$ be the set of present types and $N$ the number of waiting jobs.
The score of type $g$ as the first block is

```math
N\,\beta\,S_{r_0r_g}+(N-n_g)\,W_g+V\bigl(\mathcal G\setminus\{g\},r_g\bigr).
```

The policy selects the first block with the smallest score. Equal scores go to
the block whose first job has the earliest station-arrival time, then the
smallest identifier. The policy returns the first job of that block.

The number of subsets doubles with each additional type. In the tested layouts,
at most seven types can be present, so the search uses at most $2^7=128$
subsets.

### 5. Start one operation, then plan again

The policy commits only the selected job's current operation and its physical
changeover. It commits neither the rest of the block nor the job's later
visits. At the next bottleneck decision, it builds a new plan from the new
queue. New arrivals, returning jobs, and realized service times therefore
affect later choices without forecasts.

### Pseudocode

```text
Input:  station s with a nonempty queue Q; routes, mean processing times,
        setup matrix S, and installed bottleneck recipe r0
Output: one waiting job
Fixed setting: beta = 8

if s is not the bottleneck:
    return argmin over j in Q of (p[j], station_arrival[j], id[j])
if Q has one job:
    return that job
for each job j in Q:
    w[j] <- sum of the means of j's current and later bottleneck operations
group Q into types by (recipe, product, current operation)
for each type g:
    n[g] <- number of jobs in g
    W[g] <- sum of w[j] over the jobs in g
    r[g] <- recipe of g
    first[g] <- job of g with the earliest station arrival, then the smallest id
N <- number of jobs in Q
for each type g:
    score[g] <- N*beta*S[r0][r[g]] + (N - n[g])*W[g] + V(all types except g, r[g])
g_best <- argmin over g of (score[g], station_arrival[first[g]], id[first[g]])
return first[g_best]

The simulator performs one physical changeover S[r0][r[g_best]] and one operation.
The policy plans again at the next decision.
```

Here `V` is the recurrence of step 4.

### Edge cases

- A single waiting job at the bottleneck starts at once, with any installed
  recipe.
- The evaluated simulator always installs an initial recipe. If the bottleneck
  has no recipe and two or more jobs wait, the plan has no setup row to start
  from. The evaluated source and the portable code both raise `KeyError`.
  Neither falls back to another rule.
- Scores are floating-point sums. The tie rule applies to exactly equal
  computed scores.

## Worked example

The bottleneck uses recipe A, and $S_{AB}=S_{BA}=1$. Three jobs wait. One job
needs recipe A. Its current operation has mean 1, and it returns to the
bottleneck later for 19 more units of mean work. Two jobs of one product need
recipe B. Each has mean 4 and no later bottleneck work.

| Type (recipe) | Jobs $n_g$ | Current mean $p_j$ | Later bottleneck work | $w_j$ | $W_g$ |
| --- | ---: | ---: | ---: | ---: | ---: |
| A | 1 | 1 | 19 | 20 | 20 |
| B | 2 | 4 | 0 | 4 | 8 |

With $\beta=8$, each changeover adds $8\times1=8$ to the plan. Two orders
exist:

```math
K_\beta(A\to B)=2\cdot 20+2\cdot 8=56,\qquad
K_\beta(B\to A)=3\cdot 8+1\cdot 8+1\cdot 8=40 .
```

If A comes first, its work of 20 delays both B jobs. The change to B then
delays both B jobs by 8. If B comes first, the first change delays all three
jobs by 8. The B block's work of 8 and the change back to A then delay only the
A job.

The order B, then A, has the lower score, so the policy selects a B job. The A
job has the shorter current operation and needs no changeover. However, it has
much more bottleneck work left. The virtual schedules behind the two scores are:

| Order | Virtual schedule | Completion times | Sum |
| --- | --- | --- | ---: |
| A, then B | A job 0–20, change 20–28, B jobs 28–32 and 32–36 | 20, 32, 36 | 88 = 56 + 32 |
| B, then A | change 0–8, B jobs 8–12 and 12–16, change 16–24, A job 24–44 | 12, 16, 44 | 72 = 40 + 32 |

Both sums exceed the score by the same 32. This part comes from each job's own
work and the work of earlier jobs in its block, so the order does not change
it. The A job's 20 planned units include its later work as if it followed at
once. In the real system, the job leaves after its current operation and
returns later.

A planner with only current-operation means would use $W_A=1$. Its scores are
$2\cdot1+2\cdot8=18$ for A first and 40 for B first, so it starts the A job.
The return work reverses the decision.

The machine now makes one changeover of duration 1, not 8. It then starts the
current operation of the B job with the earlier station arrival. That operation
has mean 4, and its actual duration is random. The policy does not commit the
second B job. It plans again at the next decision.

### Why the whole queue matters

The bottleneck uses recipe A. One job needs recipe B and three jobs need
recipe C. Each job has $w_j=1$. The setup times are $S_{AB}=1$, $S_{AC}=2$,
$S_{BC}=6$, and $S_{CB}=1$. A score of the first block alone favors the cheap
change to B: $4\cdot8\cdot1+3\cdot1=35$, against $4\cdot8\cdot2+1\cdot3=67$
for C first.

The complete plan also prices the next changeover. B, then C, costs
$35+3\cdot8\cdot6=179$. C, then B, costs $67+1\cdot8\cdot1=75$. The policy
therefore starts a C job. A cheap immediate changeover can be unattractive if
it leaves expensive changeovers for many waiting jobs.

## Relationship to baselines and related work

The evaluation compares the policy with ten variants of published dispatching
rules. The setup-oriented rules follow
[Xanthopoulos et al. (2016), Table 2 and Eq. (7)](https://doi.org/10.5267/j.ijiec.2016.2.002).
Each rule ranks the waiting jobs by a simple index:

- FCFS uses the station-arrival order.
- SEPT uses the current mean.
- Least remaining route work uses the mean work left on the whole route.
- SPSU, SPTNS, FCFSNS, and MMS combine the immediate setup time with the
  current mean, the arrival order, or the number of waiting jobs per recipe.
- WORK selects the recipe with the most queued work.
- PR adds an exponential setup penalty to the current mean. The evaluation uses
  raw and normalized time units.

The source study assumes known processing requirements. The evaluated versions
use the public means. The normalized PR variant is a study-specific
adaptation, not a separate published algorithm.

These rules rank one job at a time. Bottleneck-work block planning scores an
order of the whole bottleneck queue, and it uses remaining bottleneck work
instead of the current operation. The closest comparator is a study-specific
ablation: the same planner with $p_j$ in place of $w_j$. All policies receive
the same information. The two planners use different parts of it.

Setup-aware sequence planning has a long history.
[Psaraftis (1980)](https://doi.org/10.1287/opre.28.6.1347) sequences groups of
identical jobs by dynamic programming.
[Karabatı and Akkan (2006)](https://doi.org/10.1057/palgrave.jors.2601989)
minimize total completion time on one machine with sequence-dependent family
setups. [Tran et al. (2013)](https://doi.org/10.1609/icaps.v23i1.13552)
combine queueing and scheduling models for dynamic parallel machines with
sequence-dependent setups.
[Arzi and Raviv (1998)](https://doi.org/10.1080/095372898233696) study
dispatching at a workstation of a reentrant line with sequence-dependent
setups.

This policy combines classical grouped sequencing with a measure of remaining
work for reentrant flow. Its contribution is the dispatch rule, not a new
dynamic-programming method. This entry makes no claim of literature-wide
novelty.

## Evidence in brief

On fresh seeds of the 27 development configurations, the pooled mean flow time
was 9.12% lower than that of normalized PR. That rule was the strongest of ten
baseline variants. The 95% interval was 6.88% to 12.09%, and the policy lost 4
of the 27 configurations to that baseline. Against an otherwise identical
planner with current-operation means, remaining bottleneck work reduced pooled
mean flow time by 3.90%, mostly in the four-station layout. The
[evaluation note](evaluation/README.md) gives the design, the aggregation, and
the limits.

## Applicability and limits

- **Tested setting:** one single-server bottleneck with deterministic
  sequence-dependent setups, setup-free other stations, nonpreemptive service,
  no idling or batching, and mean information only. The tests used three
  synthetic layouts with 2–4 stations, three products, 4–6 recipes, and two or
  three bottleneck visits per product.
- **One fixed weight:** the study selected $\beta=8$ for this grid. The policy
  has this one setting and is not parameter-free. Another queue family can need
  a new selection on its own development data.
- **Planning scope:** the plan ignores work at other stations and future
  arrivals.
- **Untested cases:** several setup-sensitive servers, interruptible setups,
  batching, deliberate idling, due-date or tail objectives, and other
  information boundaries need a new evaluation.
- **Computation:** the search grows exponentially with the number of present
  types. The tests had at most seven types. No test timed larger type counts.

## Portable implementation

[implementation/policy.py](implementation/policy.py) needs only the Python 3.10+
standard library:

```python
from policy import make_policy

choose = make_policy()              # beta = 8, the evaluated setting
job_id = choose(state, station_id)  # identifier of one waiting job
```

The callback reads these state fields:

- `state["bottleneck"]`: the setup-sensitive station
- `state["setup"][r][r2]`: the setup time from recipe `r` to recipe `r2`
- `state["stations"][station_id]["recipe"]`: the installed recipe
- `state["products"][product]["route"]`: a sequence of operations with
  `station` and `mean_service`
- `state["queues"][station_id]`: the waiting jobs with `id`, `product`,
  `operation` (route index), `recipe`, `station_arrival`, and
  `expected_current`

It returns an identifier and does not change the state. The simulator or system
performs the changeover and the operation. `make_policy(beta)` accepts another
weight of at least 1. The evaluated sensitivity grid used
weights 1, 2, 4, 5, 6, 8, 12, 16, 24, and 32. This interface is not a
recommendation to tune $\beta$ for each queue.

From this entry's directory, run the dependency-free check:

```text
python3 implementation/smoke_test.py
```

It checks hand-calculated fixtures, including both examples above. It also
compares the policy with a brute-force search over every block order on 300
random queues. It does not rerun the simulation study.
