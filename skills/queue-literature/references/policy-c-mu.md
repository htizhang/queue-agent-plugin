# c-mu Priority for Linear Class Holding Costs

## Mechanism

For class $i$, let $c_i>0$ be the cost per unit time of keeping a job in the
system and $\mu_i$ its exponential service rate. Serve an available job in a
class maximizing $c_i\mu_i$. Ties can use a fixed rule. This is a priority
rule; the evaluation objective is mean holding cost, not the priority score.

## Applicability

The exact setting recorded here has one server, independent Poisson class
arrivals of rates $\lambda_i$, independent exponential service times,
$\sum_i\lambda_i/\mu_i<1$, and cost-free preempt-resume service. The controller
knows classes, rates, and costs, but not individual realized service requirements.
The objective is equilibrium $\mathbb E[\sum_i c_i N_i]$, where $N_i$ counts
class-$i$ jobs in the system.

Known class means alone do not establish exponential service or transfer this
guarantee to a general-service or pooled-multiserver system. The same score may
still be a useful heuristic there. Convex delay costs require a different
argument; see [generalized c-mu](policy-generalized-c-mu.md).

## Evidence

[scully_harchol_balter_2021_gittins](sources.json), arXiv v1 Section I,
identifies c-mu as the multiclass M/M/1 specialization of Gittins. Section III
specifies the information and service model; Theorem V.1 establishes equilibrium
mean-holding-cost optimality within that model. The exponential, constant-cost
specialization yields the static index $c_i\mu_i$ rather than an age-dependent
index. This is an exact result for the stated setting, not a guarantee based
only on estimated mean service rates.

## Use in this Plugin

Stage 1 should distinguish observed class means from an exponential-service
model and record when job information becomes available. Stage 2 can use c-mu
as a direct comparator when the assumptions match, or as a labeled heuristic
otherwise. Waiting age is elapsed waiting time; attained service is processing
already received. Neither enters this memoryless class index.
