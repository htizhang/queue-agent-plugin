# Paired Common-Random-Number Policy Evaluation

Define the quantity being compared. For replication `r`, run both policies from
the stated initial state using matched exogenous inputs `U_r` (for example,
arrivals and job service requirements), and form `D_r = Y_Ar - Y_Br` for the same
objective. Use independent replication bundles; the two outputs within a pair
are deliberately dependent.

Inference should use these paired differences, not overlap of marginal confidence
intervals. A paired-t interval requires independent, identically designed
replication differences, finite variance and an adequate normal/CLT approximation;
small, skewed samples can give poor coverage.

**Seed equality is not alignment.** Separate random streams by source and align
matching primitives. When policies change event order or random-call counts,
pre-generated inputs or stable keys such as job and visit identifiers can retain
the intended pairing. Use disjoint streams/substreams across replications.

Positive covariance reduces the variance of the difference; negative covariance
increases it. Multiclass competition or preemption can disrupt event-order
monotonicity. Check paired variance and correlation rather than assuming CRN helps.

Finite-horizon comparisons measure transient performance for a stated initial
state and stopping event. Steady-state comparisons target the same long-run
quantity, with defensible initialization deletion for each policy and documented
CRN alignment. A common deletion is appropriate only if adequate for both policies.

## References

[glasserman_yao_1992_crn](sources.json), Sections 1, 2.3, 4.4 and Example 4.8;
[lecuyer_simard_chen_kelton_2002_streams](sources.json), expanded Sections 1.2,
3-4; [nakayama_2006_output_analysis](sources.json), Sections 2-4.2.

Stable-key construction, application of replication-level inference to `D_r`,
and cross-policy warm-up guidance are implementation synthesis from these sources,
not additional theorems stated in them.
