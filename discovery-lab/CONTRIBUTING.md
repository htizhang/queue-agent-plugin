# Contributing a discovered policy

Use this path for a method developed through LLM-agent research. Source-grounded
explanations of existing methods belong in
[`queue-literature`](../skills/queue-literature/SKILL.md); cite those methods here
as related work or baselines rather than adding them as discovery entries.
Publication status can be recorded, but it does not change a method's provenance.

## Make the entry usable

Add a descriptive directory and link its `policy.md` from [the index](index.md).
Keep the following material together:

- **`policy.md`:** define the queue family, objective, constraints, observations,
  and allowed actions. Explain the algorithm precisely enough to implement it,
  with pseudocode or formulas where helpful. Identify what changes relative to
  prior work and where applicability remains untested.
- **`implementation/`:** provide the policy and the small dependency slice needed
  to run it, or an immutable accessible source with clear dependencies and usage.
  Use the entry's natural interface; a shared simulator or SDK is not required.
- **`evaluation/`:** explain the reported comparison, parameter selection,
  configurations and randomness, aggregation, and important qualifications.
  Include compact evidence and a runnable check. Distinguish archived campaign
  results from checks actually rerun for the contribution.

Use enough provenance to identify the tested implementation and evidence, such
as source hashes and a frozen configuration. Keep large traces, search histories,
credentials, private user data, and machine-specific paths outside the entry.
Attribute reused code and preserve applicable license notices. Report only the
novelty and performance claims supported by the available sources and tests;
a useful extension or combination is welcome without claiming universal novelty.

## Check the contribution

Read the diff as a standalone entry: can another person understand the method,
run the supplied check, and locate the evidence behind each reported result?
Verify local links, execute the documented lightweight check, and reconcile the
implementation with its description. Name any validation gap rather than
silently substituting another algorithm or presenting a smoke test as a full
reproduction. A new contribution need not repeat an entire research campaign.

Use [queue-contribute](../skills/queue-contribute/SKILL.md) for the user's requested
draft or PR workflow. Maintainers review the entry for inclusion; acceptance does
not certify the policy as a peer-reviewed baseline.
