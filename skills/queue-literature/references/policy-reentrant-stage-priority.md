# FBFS and LBFS Stage-Priority Dispatch in Reentrant Lines

| Field | Value |
| --- | --- |
| ID | policy.reentrant_stage_priority_fbfs_lbfs |
| Kind | policy |
| Stage relevance | Stage 1, Stage 2 |
| Aliases | FBFS, LBFS, First-Buffer-First-Served, Last-Buffer-First-Served, stage-index priority |
| Sources | dai_weiss_1996_reentrant_stability |
| Review | source-checked |
| Reviewed on | 2026-09-25 |
| Legacy origin | New contribution |

## Mechanism and applicability

Dai and Weiss study an open single-route reentrant line with one buffer per
stage, infinite buffer capacity (no blocking), and one reliable server per station.
Among nonempty buffers at a station,
FBFS chooses the smallest route-stage index and LBFS the largest; use FIFO
within a stage.

The rule is work-conserving and **preemptive-resume**: a higher-priority arrival
interrupts lower-priority service, which later resumes. It observes stage
identity, nonempty buffers, and the station-stage map.

The stochastic model assumes i.i.d. interarrival/service vectors with finite
means, spread-out unbounded interarrivals, and possibly dependent service times
across stages. With arrival rate normalized to one, each nominal station workload
must satisfy
`ρ_i = Σ_{k:σ(k)=i} E[S_k] < 1`.

Theorems 4.3-4.4 prove fluid stability; with Theorem 1.1 this implies positive
Harris recurrence, not cycle-time optimality. Section 5 gives a subcritical-load
fluid instability example; it does not establish the converse stochastic
instability implication. These guarantees do not cover nonpreemptive service,
sequence-dependent setups, batching, parallel or unreliable machines, or multiple
routes.

## Evidence

[dai_weiss_1996_reentrant_stability](sources.json), journal pp. 115-119,
Definitions 1.1-1.3 and Theorem 1.1; pp. 122-125, Definition 4.1 and Theorems
4.3-4.4; pp. 125-128, Theorem 5.1. Relevant full text inspected.

## Use in this Plugin

Use as a comparator only when route and preemption assumptions fit. Otherwise
label it FBFS-style or LBFS-style without importing the theorem.
