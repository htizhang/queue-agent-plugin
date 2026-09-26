# Generalized c-mu for Convex Delay Costs

## Mechanism

For each nonempty class $i$, let $a_i(t)$ be the age of its oldest waiting job,
$1/\mu_i(t)$ the average processing time, and $C_i(\tau)$ the cost of a job's
time $\tau$ in the system. Serve the oldest job in a class maximizing
$\mu_i(t)C_i'(a_i(t))$. The age is waiting age, not attained service.
With linear $C_i$, the score reduces to [c-mu](policy-c-mu.md).

## Applicability

The source's core model is a multiclass single-server system with nondecreasing
convex delay costs. The controller observes arrivals and queue contents, not
the actual service requirements of waiting jobs. The objective aggregates
per-job delay costs over a finite horizon; it is not an arbitrary tail-risk or
deadline objective.

The result is **heavy-traffic asymptotic optimality along a scaled sequence of
systems**, not exact optimality at a particular finite load. In the author
manuscript, Assumption 1 specifies input-process convergence,
Assumption 2 cost scaling, and Assumption 3 smooth strictly convex limiting
costs with an interior optimizer. The paper also discusses boundary cases;
this note does not replace those conditions by merely saying the load is high.

## Evidence

[van_mieghem_1995_gc_mu](sources.json): the author manuscript dated 1994-10-25,
Sections 1-2, defines the model and rule. Proposition 1 treats within-class
FIFO when service times are homogeneous and unobserved. Section 4.2,
Proposition 7 and the discussion following equation (54), connect generalized
c-mu to the asymptotic cost lower bound under Assumptions 1-3. Section 4.3
gives the stochastic extension. These are manuscript locators, not asserted
page or proposition numbers for the 1995 journal layout.

## Use in this Plugin

Stage 1 should establish the meanings of arrival time, job age, class, and
service rate. Stage 2 can use this rule as a convex-delay comparator, stating
the chosen cost function and available service actions. A quadratic penalty,
for example, creates age-dependent priorities; it does not inherit a finite-load
optimality guarantee from the asymptotic theorem. Multiserver and network
extensions need their own source and model checks.
