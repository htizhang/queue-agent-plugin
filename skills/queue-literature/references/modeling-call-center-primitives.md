# Arrival, Service, and Patience Inference

## Method and applicability

Brown et al. analyze three primitives separately:

- **Arrivals:** within approximately constant-rate blocks, condition on arrival
  counts and transform ordered event times to standard exponential variables.
  This tests within-block timing, not equality of rates across blocks.
- **Service:** inspect durations and covariates. Their near-lognormal fit is
  empirical, not a universal service assumption; large samples rejected exact fit.
- **Patience:** observe the minimum of patience and virtual waiting time, plus
  whether abandonment occurred. Served calls censor patience; abandonment censors
  virtual waiting. Kaplan-Meier estimation requires conditional independence of
  those latent times given relevant covariates.

## Evidence

[brown_et_al_2005_call_center](sources.json), journal Sections 3.1, 4.3 and 5.1.

## Use in this Plugin

Treat these as separate modeling questions. Preserve censoring indicators and
logging resolution; do not fit patience using abandoned callers alone or declare
every arrival stream Poisson because one diagnostic does not reject it.
