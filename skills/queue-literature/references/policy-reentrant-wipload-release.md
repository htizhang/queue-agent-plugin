# WIPLOAD Release Control for Reentrant Fabs

## Mechanism and applicability

This is release control, not station dispatch. For product `m` at step `j`,
define nominal remaining processing work

`R_m(j) = Σ_{j'=j}^{J_m} P_m(j')`.

With `W_m(j,t)` lots there, system WIPLOAD is

`L(t) = Σ_m Σ_j W_m(j,t) R_m(j)`.

Choose reference `L_bar` and update `L(t)` on releases and operation
completions. The source's flowchart selects the highest-priority external lot of
product `m`, computes `e(t)=L_bar-L(t)`, and releases it only when
`e(t) >= R_m(1)`. Otherwise it remains outside. Required information is each
lot's product and step, complete routes, nominal operation times, fresh events,
and an external-lot priority.

Unlike CONWIP's job-count cap, WIPLOAD weights an early, long-route lot more
than a nearly completed lot. It also differs from bottleneck-only workload
regulation. `L_bar` needs output-level calibration; no universal default exists.

## Evidence

[qi_et_al_2007_wipload_release](sources.json), proceedings p. 1738, Section 2,
Equations (1)-(2) and Figures 1-2, defines the state, update events, and release
gate.

At matched throughput, Sections 3-4 and Tables 5-7 report replicated simulations
on simplified and real-fab-derived models. Results vary by scenario; no
stability, cycle-time optimum, or universal dominance is proved.

## Use in this Plugin

Use only when lots can be held outside and route progress is observable. Report
`L_bar`, priority and update semantics; keep station dispatch separate.
