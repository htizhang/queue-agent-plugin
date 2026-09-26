# Queue Model Adequacy and Validation

A queue model is adequate when it is accurate enough for a stated decision over a stated operating domain. Adequacy is therefore tied to the intended use: a model for weekly staffing may aggregate details that a real-time routing controller must retain. Validation supplies evidence about that adequacy; it does not prove that a model is a true description of the real system. Law and Sargent both frame validity relative to objectives, variables of interest, operating conditions, and required accuracy [law_2022_valid_credible_simulation](sources.json) [sargent_2013_simulation_vv](sources.json).

## Distinguish the questions being checked

**Verification** asks whether equations, event logic, data transformations, and software implement the specified model correctly. **Validation** asks whether the specified model reproduces the relevant behavior of the target system accurately enough for its intended use. A verified implementation can faithfully execute a poor queue model; a plausible output plot cannot by itself show that the implementation is correct [sargent_2013_simulation_vv](sources.json).

**Input fit** asks whether selected descriptions of arrivals, service, patience, routing, or availability agree with their corresponding records. **Output fit** asks whether their interaction through the queue produces the observed congestion and flow. Good marginal fits do not establish the dependence structure, time variation, discipline, resource constraints, or output behavior. In an emergency-department study, an overall length-of-stay distribution missed a pronounced time-of-day departure surge and distorted occupancy, while a time-varying length-of-stay model reproduced those profiles much better [whitt_zhang_2017_ed_model](sources.json).

## Make uncertainty and observation explicit

A useful schematic decomposition is

$$
Y^{\mathrm{obs}}
=H_{\mathcal O}\!\left(X^{M,\theta}_{0:T}\right)
+\delta_M+\varepsilon .
$$

Here $M$ is the structural choice—state variables, topology, discipline, dependence, and transition mechanisms—while $\theta$ contains parameters within that structure. $X^{M,\theta}$ is the latent queue path. The observation map $H_{\mathcal O}$ says what the operational system records: timestamp semantics, aggregation interval, censoring, class coarsening, rounding, missing events, and the initial and final window treatment. The discrepancy $\delta_M$ represents behavior the selected structure does not capture, and $\varepsilon$ represents measurement or recording error. The additive form is only a schematic adaptation of Kennedy and O'Hagan's separation of calibration parameters, model inadequacy, and observation error; many queue summaries have nonlinear observation maps [kennedy_ohagan_2001_calibration](sources.json).

Do not let parameter calibration conceal structural uncertainty. Different combinations of service rate, abandonment, hidden capacity, class mixture, and observation error can produce similar observed queue lengths. Kennedy and O'Hagan show more generally that a calibrated “best-fitting” parameter need not equal its physical value when model discrepancy is present. A discrepancy term records mismatch; it does not identify which queue mechanism is missing.

Write $H_{\mathcal O}$ before comparing model and data. For example, Whitt and Zhang's recorded emergency-department length of stay ended at the admission decision, not at the later physical transfer, so it excluded boarding. Treating that timestamp as physical departure would validate the wrong observable [whitt_zhang_2017_ed_model](sources.json).

## Check conservation before stochastic fit

Accounting identities catch event loss, double counting, class leakage, and inconsistent timestamp semantics without relying on a distributional assumption. For each class over $[0,T]$,

$$
N_i(T)-N_i(0)
=A_i(T)-C_i(T)-R_i(T)-O_i(T)+I_i(T),
$$

where $A_i,C_i,R_i,O_i,I_i$ are external arrivals, completions that leave the modeled system, abandonments, routed outflows, and routed inflows. Adapt the terms to the boundary of the modeled system, but account for every way a customer crosses it. Resource-time categories must be mutually exclusive as well as exhaustive. One explicit convention is to give each server exactly one primary label at each instant: off-shift, unavailable without a job, busy-paused by an outage, setup, blocked, busy-active, or idle-available. Their durations then partition calendar server-time over the horizon; secondary attributes should be tracked in separate balances rather than double-counted.

Little's law needs special care in a finite observation window. Let

$$
\bar L(T)=\frac1T\int_0^T L(t)\,dt,\qquad
\bar\lambda(T)=\frac{A(T)}T,
$$

and let $\bar W_A(T)$ be the average complete system time of arrivals during $[0,T]$, including portions after $T$. Kim and Whitt's extended finite-time identity can be written

$$
\bar\lambda(T)\bar W_A(T)-\bar L(T)
=
\frac{T_W^{(r)}(T)-T_W^{(r)}(0)}{T},
$$

where $T_W^{(r)}(t)$ is the total remaining system time of customers present at boundary $t$. The familiar finite-window equality holds exactly when the two boundary residual totals are equal. Empty endpoints make both terms zero and are therefore sufficient, but zero is not necessary. Truncating all customer histories to the interior of the window can force an equality, but changes the estimand [kim_whitt_2013_littles_law_statistics](sources.json).

Thus, a finite-window balance is not interchangeable with a stationary or long-run law. It is also primarily a consistency check when every term is computed from the same event log. Agreement with independently sampled occupancy snapshots or external throughput totals is stronger evidence because it can reveal common transformation errors. The latter point is a synthesis from the accounting identity, not a theorem in the cited paper.

## Compare the observables the decision depends on

Use data not used to tune the same model where feasible: later periods for a predictive check, or held-out days, weeks, sites, or operating conditions for a historical check. Sargent distinguishes historical and predictive validation and recommends comparing system and model output behavior over the intended domain [sargent_2013_simulation_vv](sources.json). The comparison should apply the same observation map $H_{\mathcal O}$ to real and replicated model paths, with compatible initial state, horizon, calendar, censoring, and aggregation.

The following practical diagnostic guide is a synthesis rather than a one-to-one result from a source:

| Observable | What a mismatch can expose |
| --- | --- |
| queue length, number in system, and busy servers over time | capacity, service, dispatch, or missing-customer errors |
| waiting and sojourn distributions, including tails | discipline, class mixing, service, abandonment, or censoring errors |
| completions, abandonments, and throughput | flow conservation, capacity, or transition-rate errors |
| class-specific counts and outcome distributions | routing, priority, compatibility, or class-definition errors |
| hour-of-day and day-of-week profiles, peak timing, and lag | omitted nonstationarity, schedules, or time-dependent behavior |

Compare distributions and temporal shape, not only an overall mean. Means can agree while upper waiting-time quantiles, abandonment, or peak congestion—the quantities driving the policy decision—do not. For dependent time series, ordinary independent-sample formulas may be inappropriate; Law specifically warns that system outputs are often nonstationary and autocorrelated [law_2022_valid_credible_simulation](sources.json).

Replicated data should answer “what would this fitted model tend to produce?” rather than merely overlay one convenient path. In posterior predictive assessment, replicated datasets are generated under the fitted model and compared through discrepancies $T(Y)$ chosen to reveal scientifically relevant failures:

$$
T(Y^{\mathrm{obs}})
\quad\text{versus}\quad
\{T(Y^{\mathrm{rep},b})\}_{b=1}^B .
$$

The discrepancies may be a peak-hour queue profile, a class-specific waiting-time quantile, a throughput-to-capacity ratio, or a joint pattern. Gelman, Meng, and Stern emphasize choosing discrepancies that reflect the inferential purpose and comparing observed values with their replicated distribution, not treating such checks as a proof that the model is true [gelman_meng_stern_1996_posterior_predictive](sources.json).

Beware of self-confirming output checks. Whitt and Zhang found near-perfect agreement after estimating a time-varying model from the same data, but explained much of it as a time-varying Little's-law consistency relation rather than genuine prediction. Held-out time periods or independently observed outputs are needed for a stronger claim [whitt_zhang_2017_ed_model](sources.json).

## Use structural sensitivity when the log cannot identify one model

When several structures remain plausible, carry them forward instead of selecting one by fit alone. Vary consequential assumptions as well as parameters: queue discipline, class aggregation, dependence, time-varying rates, patience behavior, hidden capacity, interruption rules, and boundary treatment. Law explicitly includes distribution choice and subsystem detail, not just scalar parameters, in sensitivity analysis [law_2022_valid_credible_simulation](sources.json).

A practical sensitivity synthesis is to summarize, for a candidate policy $\pi$ against incumbent $\pi_0$, the range

$$
\mathcal R_\pi=
\left\{
J_{M,\theta}(\pi)-J_{M,\theta}(\pi_0):
(M,\theta)\in\mathcal C
\right\},
$$

where $\mathcal C$ contains structures and parameter values still compatible with the evidence. If the sign and operational size of the policy effect are stable across $\mathcal C$, the recommendation is less dependent on an unresolved modeling choice. If the range crosses zero or changes which class benefits, report the policy conclusion as structure-contingent and identify the observation that would discriminate the alternatives.

This is particularly important when all records were generated under one incumbent policy. Such data may reproduce that policy's outputs while leaving the response to a new priority or routing rule unidentified. Validation under the incumbent is necessary evidence, but it does not by itself validate a policy counterfactual. This conclusion is a queue-modeling synthesis of the structural-discrepancy and intended-use principles.

Choose detail by the action being evaluated. Weekly capacity planning may need accurate time-varying offered load and abandonment without individual server identities. Skill-based routing may require compatibility, server state, and class-specific queues. Deadline or age-based control requires waiting ages that a count model discards. Add detail when it changes feasible actions, information available to the controller, or policy-relevant outputs; otherwise it can add weakly identified parameters without improving the decision.

## Source references

- [sargent_2013_simulation_vv](sources.json), §1, pp. 12–13; §3, pp. 14–15; §4, pp. 16–17; §6, pp. 17–18; §8–§8.2, pp. 18–21: verification, conceptual and operational validation, intended domain, held-out/predictive comparison, and output techniques.
- [law_2022_valid_credible_simulation](sources.json), §1–§1.1, pp. 1283–1286; §2.1, p. 1287; §2.4, pp. 1288–1289; §2.7, p. 1290; §2.8, pp. 1291–1292: objective-relative validity, model detail, input modeling, structural sensitivity, and output comparison.
- [kennedy_ohagan_2001_calibration](sources.json), Summary and §2.1, PDF pp. 1–3; §4.2–§4.3, PDF pp. 11–13, especially (5)–(6): parameter uncertainty, model inadequacy, observation error, and limits on physical interpretation of calibrated parameters.
- [gelman_meng_stern_1996_posterior_predictive](sources.json), §2.1–§2.3, pp. 737–742, especially (2)–(5), and §4.3, pp. 757–758: replicated observations and purpose-selected discrepancy checks.
- [whitt_zhang_2017_ed_model](sources.json), §2, pp. 2–3; §4.1–§4.2, pp. 8–9; §6.1 and §6.3, pp. 11–12: timestamp meaning, failure of an overall length-of-stay model, time-profile comparisons, and same-data consistency versus prediction.
- [kim_whitt_2013_littles_law_statistics](sources.json), §2.1, (1)–(3), p. 1032; §2.2, Theorems 1–2 and (4)–(7), pp. 1033–1034; §2.3, p. 1034: finite-window definitions, edge effects, and forced-equality alternatives.
