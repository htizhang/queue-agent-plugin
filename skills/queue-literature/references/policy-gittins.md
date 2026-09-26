# Gittins Policy for Unknown Job Sizes

| Field | Value |
| --- | --- |
| ID | policy.gittins_unknown_size |
| Kind | policy |
| Stage relevance | Stage 1, Stage 2 |
| Aliases | Gittins index, Gittins rank, attained-service index, unknown-size scheduling |
| Sources | scully_harchol_balter_2021_gittins |
| Review | source-checked |
| Reviewed on | 2026-09-25 |
| Legacy origin | queue-research a0dc5cc: policy.gittins_unknown_size |

## Mechanism

For the classical unknown-size, mean-response-time case, let $S$ be the service-time random variable and let $x$ be a job's attained service. Its Gittins index is

$$
I(x)=\sup_{y>x}
\frac{\Pr(S\le y\mid S>x)}
{\mathbb{E}[\min\{S,y\}-x\mid S>x]}.
$$

The numerator is the conditional probability of completion before attained service reaches $y$; the denominator is the expected additional service spent before completion or that stopping age. Serve a job of maximal $I(x)$ at every decision time, breaking ties arbitrarily. Equivalently, define rank $R(x)=1/I(x)$ and serve minimum rank ([scully_harchol_balter_2021_gittins](sources.json), Definition IV.2, Example IV.3, and Section IV.B).

## Applicability

This formula applies when actual job sizes are unknown, attained service is observable, and the service-time law used in the index is known. The exact specialization recorded here is a stable single-server M/G/1-like queue, unit holding cost, all states preemptible, and zero-cost, zero-delay preempt-resume. In the source's model, arrivals occur at Poisson batch epochs and $\rho<1$. Job states evolve only during service, independently of arrivals and other jobs' evolution; the scheduler knows these dynamics ([scully_harchol_balter_2021_gittins](sources.json), Section III.A–III.C and III.F).

A noisy point estimate of total size is a different information structure. It may define predicted-SRPT, or enter a richer posterior state if that state and its dynamics are modeled. Different known class-conditional size laws can yield different indices even for jobs with attained service zero. A nonpreemptive approximation or multiserver index policy is outside this card's guarantee; weighted holding cost and slowdown require the corresponding cost model and index.

## Evidence

Example III.2 identifies attained service as the state for unknown job sizes. Example IV.3 gives the displayed index. Theorem V.1 proves equilibrium mean-holding-cost optimality among nonclairvoyant policies in the $M_B/G_{MP}/1$ model; the unit-cost attained-service case is a specialization. Nonclairvoyant means using only the declared current and past states, not necessarily unknown sizes: the general theorem also contains the known-size SRPT case. This is an **exact steady-state theorem** ([scully_harchol_balter_2021_gittins](sources.json), Examples III.2 and IV.3, Section V, Theorem V.1).

## Use in this Plugin

Stage 1 should determine what job information is available, establish the relevant service-time distribution, and verify that attained service and preemption are represented. Stage 2 can evaluate $I(x)$ or use a disclosed numerical approximation; a finite lookup table is not automatically the exact index policy. Distribution estimation, censoring, model drift, and preemption overhead need application-specific checks. Compare with [SRPT](policy-srpt.md) when actual remaining sizes are known.
