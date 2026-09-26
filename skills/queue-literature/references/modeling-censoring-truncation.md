# Censoring and Truncation in Queue Event Logs

A right-censored job is logged but its end is known only to be later; a truncated
job is absent. Define the duration of interest before interpreting the log.
For an observation window `[0, T]` and a job's start time `s`:

- **Still open at T:** retain the job as right-censored at age `T - s`, with its
  event indicator. A completed-only sample silently removes these observations.
- **Running at 0, start known:** entry is left-truncated at age `-s`; the risk
  set at age `z` contains jobs with `entry age <= z <= exit or censoring age`.
  Durations below the population entry-age support cannot be recovered by this
  construction. If pre-window starts are unknown, known in-window starts form
  one total-duration cohort; separately enumerated and followed pre-window jobs
  may still inform residual duration rather than total duration.
- **Completion-only log:** for in-window starts, observation requires duration
  `X <= tau = T - s`. The reverse-time risk set is `{i: X_i <= z <= tau_i}`.
  Up to the sample limit `tau* = max_i tau_i`, the nonparametric construction
  estimates `F(x)/F(tau*)`, not `F(tau*)` or the upper tail. Population recovery
  depends on truncation-time support. Testing quasi-stationarity over start times
  does not establish full stationarity.

For **patience**, record served and abandoned entrants, not abandoned callers
alone. Let `W` be observed wait, the minimum of patience and offered wait, with
unambiguous exit type and no latent tie. These observations alone imply

`P(W > t) <= P(patience > t) <= 1 - P(abandon, W <= t)`.

These population bounds need no independence between patience and offered wait.
Their width is `P(served, W <= t)`, so they can be wide. Point estimates such as
Kaplan-Meier need an appropriate noninformative observation assumption, possibly
conditional on covariates; waits and exit types alone cannot establish it.

The cited sampling results assume independent observations. They do not supply
uncertainty intervals for arbitrary dependent queue records. Evictions or transfers
may terminate the target duration, censor it, or be intermediate transitions:
choose by the estimand, not the event name. An ordinary bootstrap does not repair
an inappropriate observation model.

## References

[woodroofe_1985_truncated_data](sources.json), pp. 164-172;
[tse_2003_ltrc_product_limit](sources.json), Section 1;
[kalbfleisch_lawless_1991_right_truncation](sources.json), Sections 1-2 and 5;
[tsiatis_1975_competing_risks](sources.json), Theorem 2;
[peterson_1976_competing_risk_bounds](sources.json), Theorems 1 and 3;
[brown_et_al_2005_call_center](sources.json), Sections 5.1-5.3.
The window, queue-exit and Peterson-to-patience mappings above are synthesis.
