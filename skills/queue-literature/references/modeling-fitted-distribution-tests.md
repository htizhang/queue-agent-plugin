# Goodness-of-Fit After Parameter Estimation

## Method and applicability

Estimating distribution parameters from the tested sample changes the null
distribution of an empirical-distribution statistic. Ordinary fixed-parameter
KS cutoffs are therefore not generally valid after fitting.

For a parametric-bootstrap check, fit the specified family, simulate samples
from that fitted distribution, **refit each simulated sample**, and recompute
the same statistic against its refitted distribution. Use the simulated
statistics to calibrate the observed discrepancy.

Babu and Rao justify bootstrap calibration asymptotically for i.i.d. samples
from continuous families under estimator and distribution regularity conditions.
Their nonparametric construction also needs a centering correction. Neither
result licenses ordinary resampling of dependent or censored queue records.

## Evidence

[babu_rao_2004_fitted_gof](sources.json), Sections 1-2.2, Equations (2.2)-(2.3)
and Theorems 4.1-4.2: composite-null problem, refitted bootstrap construction,
assumptions and asymptotic justification.

## Use in this Plugin

Record how parameters and cutoffs were obtained, not just a p-value. Treat a
distributional check as evidence about that marginal model, not validation of
the queue's routing, discipline or independence assumptions.
