# Maximum Pressure in Processing Networks

| Field | Value |
| --- | --- |
| ID | policy.maximum_pressure_network |
| Kind | policy |
| Stage relevance | Stage 1, Stage 2 |
| Aliases | MaxWeight, backpressure, downstream congestion, EAA |
| Sources | dai_lin_2005_maximum_pressure |
| Review | source-checked |
| Reviewed on | 2026-09-25 |
| Legacy origin | New contribution |

## Mechanism and applicability

With buffer vector `z` and net-consumption matrix `R`, maximize `z' R a` over
feasible extreme resource allocations `a`. Feasibility includes available jobs,
not just processor capacity. Ties may be resolved consistently.

Dai-Lin's base theorem assumes preemption and processor splitting and requires
the EAA structural assumption, primitive-process limits and planning-LP condition.
Its conclusion is **pathwise rate stability**, `Z_i(t)/t -> 0` almost surely;
this is not a stationary mean-delay guarantee.

The non-splitting result remains preemptive and uses a separate static-allocation
condition. The nonpreemptive extension
requires reversed-Leontief structure and additional service-time assumptions;
it does not cover arbitrary simultaneous-multiprocessor jobs.

## Evidence

[dai_lin_2005_maximum_pressure](sources.json), Sections 2-4, Definitions 1-2,
Theorem 2; Sections 7-8, Theorems 8-9. Relevant full text inspected.

## Use in this Plugin

Match resource activities and actions before selecting this baseline. Distinguish
throughput guarantees from the response-time objective actually being evaluated.
