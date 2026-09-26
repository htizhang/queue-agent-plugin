# Choosing and Checking Time-Varying Arrival Models


## Method and applicability

First check timestamp resolution and rates over time and across comparable days.
A rate histogram shows rate variation; it does not validate Poisson arrivals.
Keep three questions apart:

- **Timing within windows.** Test conditional timing where the rate is roughly
  constant (transform: [Arrival, service, and patience inference](modeling-call-center-primitives.md)).
  The plain conditional-uniform KS test reacts more than Lewis's refinement to
  rate change inside a window, but has little power against non-exponential gaps,
  where Lewis is stronger. Rounding creates zero gaps that make Lewis reject; Kim
  and Whitt unround second-level data with small uniform offsets, but with coarse
  timestamps unrounding can hide non-Poisson behaviour.
- **Counts across comparable days.** Per-day tests allow each day its own rate,
  so a pass does not show fixed rates. Investigating random rates (a Cox process)
  needs the same window's counts on repeated comparable days, net of holidays and
  trends, compared with Poisson variation.
- **Serial dependence.** These tests have little power against it; windows cut
  dependence at their boundaries; exponential-looking gaps can still be dependent.

Treat outcomes as evidence under window, rounding and power assumptions, not
model identification. Non-rejection is not confirmation; large samples reject
small departures.

**One sample path.** With an unknown, flexible intensity, Λ(t) can be fitted,
but the candidate Poisson tests Nelson and Leemis examine fail; testing against a
prespecified rate is a different test. Otherwise justify the model by arrival
mechanism and run sensitivity analysis.

## Evidence

[kim_whitt_2014_nhpp_tests](sources.json): Sections 1.1, 1.3-1.7, 4.1, 5.1,
5.5 and 9.2. [kim_whitt_2014_call_center_hospital_nhpp](sources.json):
Sections 1.2-1.4, 2, 3.1, 4, 5.4 and 7.
[nelson_leemis_2020_nspp_one_sample_path](sources.json): Sections 3-6.
Scope and interpretation statements are synthesis; the cited papers give the
test constructions and results.

## Use in this Plugin

Record resolution, windows, comparable days and tests; report each check's scope,
and with one path label an NHPP an assumption.
