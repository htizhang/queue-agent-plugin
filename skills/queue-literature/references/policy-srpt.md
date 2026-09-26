# Shortest Remaining Processing Time (SRPT)

## Mechanism

At each decision point, SRPT serves the incomplete job with the smallest **actual remaining service requirement**. If job $j$ arrived with known service requirement $s_j$ and has received $a_j(t)$ units of service, its priority state is $r_j(t)=s_j-a_j(t)$. A newly arriving job or a change in remaining-service order may preempt the current job; service later resumes without lost work. Ties may be broken arbitrarily.

In the source's known-service model, a job's state is its remaining service. With unit holding cost and all states preemptible, the Gittins rank equals remaining service, so serving minimum rank reduces exactly to SRPT ([scully_harchol_balter_2021_gittins](sources.json), Example III.1 and Section IV.B).

## Applicability

The exact result recorded here concerns a stable, single-server M/G/1-like queue with true job sizes visible to the scheduler. The source's encompassing $M_B/G_{MP}/1$ model has Poisson batch-arrival epochs and load $\rho<1$; ordinary M/G/1 is a special case. Job states evolve only during service, independently of arrivals and other jobs' evolution. Service preemption has no cost or delay and is preempt-resume ([scully_harchol_balter_2021_gittins](sources.json), Section III.A–III.C).

This guarantee does **not** transfer automatically to:

- a noisy size estimate, which yields a predicted-SRPT heuristic rather than SRPT with known remaining work;
- unknown sizes observed only through attained service, for which the
  attained-service Gittins policy is the relevant note;
- multiserver, nonpreemptive, setup-cost, or lossy-preemption adaptations.

It also does not establish optimality for objectives other than the unit-holding-cost/mean-response-time objective used for this specialization.

## Evidence

The source models known sizes by deterministic remaining-service state (Example III.1), states that constant unit holding cost makes Gittins rank equal remaining service (Section IV.B), and proves that Gittins minimizes equilibrium mean holding cost among nonclairvoyant policies in its $M_B/G_{MP}/1$ model (Theorem V.1). Combining those source results gives an **exact steady-state result**, not a heavy-traffic or other asymptotic approximation ([scully_harchol_balter_2021_gittins](sources.json), Theorem V.1).

Here, nonclairvoyant means no information beyond the declared current and past states; those states include exact remaining service. No full text of Schrage's 1968 proof was reviewed, so this note does not assert an arbitrary-arrival, all-sample-path result.

## Use in this Plugin

Stage 1 should establish whether the actual total service requirement is available at decision time: a requested time limit or a prediction is not necessarily the actual size. Confirm that attained service is tracked and record preemption semantics and overhead. Stage 2 can use SRPT as an exact benchmark only when the applicability conditions hold. With estimates, label the candidate predicted-SRPT; with unknown sizes and a service-time distribution, consult the [Gittins note](policy-gittins.md).
