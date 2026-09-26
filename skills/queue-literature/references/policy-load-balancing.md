# Load-Balancing Dispatch: JSQ, SED, JSW, and Power-of-d

Routing rules are defined as much by what the dispatcher observes as by how
they choose a server. Before selecting a policy, distinguish exact queue
counts, service ages, exact remaining work, sampled state, predicted work, and
stale state.

## Mechanisms

- **Join the shortest queue (JSQ):** route to a server with the fewest jobs,
  including the job in service.
- **Shortest expected delay (SED):** route where the arriving job has the
  smallest expected delay, conditional on available information such as queue
  length and elapsed service. Specify whether delay means waiting or response time.
- **Join the shortest workload (JSW), or least work remaining:** route to the
  server with the least total unfinished work. This requires the exact sizes of
  queued jobs and the remaining work of the job in service.
- **JSQ(d), or power-of-d:** sample `d` servers and join the sampled server
  with the fewest jobs.
- **LL(d):** sample `d` servers and join the sampled server with the least
  remaining work.

A job count is not a workload. A shorter queue may contain more work, and a
routing by predicted workload defines an approximation, not exact JSW or LL(d).

## Exact finite-system results

In Weber's model, servers are identical, each has a separate FIFO queue, and
jobs do not switch queues. For exponential service and an arbitrary arrival
process, JSQ maximizes the number of completions by every time in stochastic
order. In continuous time, under Weber's nondecreasing, continuous,
differentiable service-hazard assumptions, the optimal rule also uses service
ages: among equally short nonempty queues, it selects the queue whose job in
service is oldest. If ages are unavailable and random tie-breaking is required,
Weber retains optimality within that restriction
([weber_1978_optimal_assignment](sources.json)).

That restriction matters. When queues are distinguishable, Whitt shows that a
fixed queue order can improve random tie-breaking in his example and notes that
ordered ties can also improve shortest-line routing for IFR service; he does
not claim that ordered ties are always optimal. Whitt also gives
separate-queue, FCFS, no-jockeying counterexamples in which JSQ fails to
minimize long-run average delay. Even with elapsed service observed, the SED
rule that minimizes the arriving job's expected delay need not minimize
long-run average delay for all jobs
([whitt_1986_which_queue_counterexamples](sources.json)).

For exact-work routing, Harchol-Balter, Crovella, and Murta study identical
hosts with Poisson arrivals and FCFS nonpreemptive service. With exact queued
work and exact remaining work for the job in service, JSW can be coupled to a
central FCFS `M/G/h` queue: under the same arrival stream and consistent
tie-breaking, every job starts and finishes service at the same time in both
systems
([harchol_balter_crovella_murta_1998_task_assignment](sources.json)).
This gives a direct central-queue baseline. The equivalence does not extend
unchanged to estimated sizes, heterogeneous speeds, or a different local
service discipline.

## Large-system limits

The classical supermarket result has a specific model: `N` homogeneous
servers, total Poisson arrival rate `N * lambda`, mean-one exponential service,
fixed `d`, uniform sampling with replacement, and `lambda < 1`. For `d = 2`,
Vvedenskaya, Dobrushin, and Karpelevich prove in stationarity that the expected
fraction of queues with at least `i` jobs converges to

```text
lambda^(2^i - 1).
```

([vvedenskaya_dobrushin_karpelevich_1996_two_queues](sources.json))

For `d >= 2`, Mitzenmacher derives the fixed point

```text
lambda^((d^i - 1) / (d - 1)),
```

but his finite-system bounds are for a fixed time horizon from an empty initial
state
([mitzenmacher_2001_power_of_two](sources.json)).
Use the expression as a large-`N` model result, not as a finite-system
steady-state guarantee or as a formula for general service times.

Finite-size error also needs conditions. Gast proves `O(1/N)` error for
suitable smooth expected performance functionals under regularity assumptions;
the stationary result additionally needs an exponentially stable attracting
fixed point and a concentration condition. These conditions are verified for
stationary mean queue length in the two-choice model. The result is not a
generic `O(1/N)` error bar for every queueing model, and its numerical study
shows that finite-size effects can become material near saturation
([gast_2017_mean_field_1_over_n](sources.json)).

When the sample size changes with `N`, the limit changes too. In a subcritical
homogeneous system, `d(N) -> infinity` gives the same fluid limit as full JSQ;
the same paper also proves convergence of the stationary occupancy measure on
the fluid scale. In the Halfin-Whitt regime,
`d(N) / (sqrt(N) log N) -> infinity` gives the JSQ diffusion limit over finite
time horizons, but that result does not establish stationary diffusion
convergence
([mukherjee_borst_van_leeuwaarden_whiting_2018_universality](sources.json)).
For full JSQ with identical servers, Poisson arrivals, and exponential service,
Braverman separately establishes the steady-state Halfin-Whitt limit
([braverman_2020_jsq_halfin_whitt_steady_state](sources.json)).

For exact sampled workloads, LL(d) is not merely another name for JSQ(d).
With mean-one exponential jobs and FCFS service, its large-`N` limiting mean
response time is smaller than that of SQ(d). Late binding realizes the same
selection only when fetch or network delay is negligible, or when that delay is
included explicitly as workload overhead
([hellemans_van_houdt_2018_least_loaded](sources.json)).

## Heterogeneous servers

The identical-server theorems above do not justify uniform sampling when
servers have different capacities. In a large processor-sharing model,
Mukhopadhyay and Mazumdar show that uniform SQ(2) can have a smaller stability
region than the system's total capacity permits. Their hybrid first chooses a
speed class with a capacity-aware probability, then applies SQ(2) within that
class; suitable class probabilities recover the maximal stability region
([mukhopadhyay_mazumdar_2016_heterogeneous_jsq](sources.json)).
This guarantee is specific to that large processor-sharing model. For another
service discipline or capacity model, include a capacity-aware baseline and
verify stability rather than transferring the theorem by analogy.

## Stale and estimated information

Fresh-state conclusions need not survive delayed observations. In
Mitzenmacher's periodic bulletin-board model, numerical solutions of the
limiting equations, checked by simulation, show that routing to the apparently
shortest queue can perform worse than random routing even at fairly short
update intervals. Two sampled choices are robust over a wider range, while
random routing is preferable when the snapshot becomes sufficiently old. This
is numerical evidence, not a universal ordering theorem
([mitzenmacher_2000_old_information](sources.json)).

Predicted work introduces a different error. Simulations and trace-driven
experiments show cases where routing by predicted least load performs worse
than routing by queue count. In those experiments, recomputing predicted
remaining work after departures materially outperforms updating workload only
on arrivals
([mitzenmacher_dellamico_2022_predicted_sizes](sources.json)).
Treat both conclusions as empirical design guidance and retain JSQ or JSQ(d) as
a count-based control.

## Model-matching checklist

1. **Name the observation:** all queue counts, `d` sampled counts, exact
   remaining work, predicted work, service ages, or a stale snapshot.
2. **Match the server model:** identical or heterogeneous speeds, FCFS or
   another local discipline, preemptive or nonpreemptive service.
3. **Match the claim's regime:** finite exact, fixed-load mean field,
   finite-horizon diffusion, stationary fluid, or stationary Halfin-Whitt.
4. **Use direct baselines:** JSQ for complete count state, JSQ(d) for sampled
   counts, JSW plus central `M/G/k` FCFS for exact work, and LL(d) for sampled
   exact work. Add a capacity-aware policy for unequal speeds and random
   routing for stale state.
5. **Evaluate at the target size and load:** report mean and tail response
   time, stability, and sensitivity to estimation or update error. An
   asymptotic formula is not a substitute for finite-system evaluation.

