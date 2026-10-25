# Discovery Lab

Agent-discovered queueing policies, with runnable implementations and bounded
experimental evidence. This collection is separate from the literature knowledge
base: entries are research leads, not established recommendations or a catalog
of classical algorithms. Repository review is not scientific peer review.

For research, the [Stage 2 access rule](../skills/queue-policy/SKILL.md#discovery-lab-access)
determines when to explore this collection. For a requested contribution, read
the [contribution guide](CONTRIBUTING.md).

## Entries

| Method | Model family and objective | Mechanism |
| --- | --- | --- |
| [Queue-aware optimistic backfilling](queue-aware-backfilling/policy.md) | Nonpreemptive multiserver jobs with simultaneous resource requirements; mean response time | Ranks jobs by runtime request, width, and queue counts; repairs poor packing; plans reservations using requests and public class means. Two parameters control the packing repair. |
| [Bottleneck-work block planning](bottleneck-work-block-planning/policy.md) | Multiclass reentrant networks with sequence-dependent setups; mean flow time | Groups the whole waiting queue by job type, plans the group order using remaining bottleneck work and setup times, then dispatches one job. The evaluated policy fixes the setup weight at 8. |

Each entry separates its method description, implementation, and evaluation.
Start with the description; inspect code or results when they answer a concrete
question for the confirmed problem. Evidence applies to the configurations and
comparators named in that entry, not automatically to another queue family.
