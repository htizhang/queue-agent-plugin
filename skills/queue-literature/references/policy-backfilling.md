# EASY and Conservative Backfilling

## Mechanism and applicability

Jobs occupy fixed-size processor partitions and supply runtime estimates.
**EASY** protects the first queued job's reservation. In the studied algorithm,
scan later jobs in arrival order: backfill one that fits now and either finishes
by the reserved start or uses only capacity left over at that start.
**Conservative backfilling** reserves every queued job; compression must preserve
existing start-time commitments rather than rebuild them carelessly.

The runtime bound needs enforcement or a valid upper bound; a statistical
prediction alone does not ensure reservation safety. The paper discusses killing
jobs that overrun their requested duration. Its performance comparisons depend
on workload and metric, not a universal ordering of the policies.

## Evidence

[mualem_feitelson_2001_backfilling](sources.json), Sections 2.1-2.2, 3.3 and 4.

## Use in this Plugin

Specify reservation depth, queue order and overrun handling alongside the name.
