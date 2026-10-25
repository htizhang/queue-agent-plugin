# Shared writing skill: behavioral checks

These are source-loaded review cases, not installed-host discovery tests. Give
the reviewer the relevant Stage skill, the writing skill, and each request.
Ask for the intended rewrite and next action. Do not run the hypothetical
research tasks. Keep reviewer expectations separate from the input prompts.

## Requests

1. **Stage 1 explanation:** "Explain this model for a new collaborator: jobs
   visit station A, then B, then A again. Each station has one server. Jobs wait
   when the required server is busy. Define reentrance. Do not change the model."
2. **Stage 2 report:** "Clarify this result: on 27 tested configurations, the
   policy reduced mean flow time by 9.12% relative to normalized PR. This does
   not establish improvement for every member of the model family."
3. **Planning versus execution:** "Clarify this policy description: for each
   waiting job, the planner sums the mean durations of its current and later
   visits to the bottleneck. It chooses an order using these planning durations,
   but starts only one current operation before planning again."
4. **Assumption preservation:** "Simplify: when all jobs are initially available,
   no new jobs arrive, and each job has one remaining operation, the stated
   bound applies only to schedules that keep each type contiguous."
5. **Technical distinctions:** "Clarify our two checks: verification asks whether
   the simulator implements the model. Validation asks whether the model is
   adequate for its intended use. Keep the names of both checks."
6. **Unsupported mechanism:** "Clarify: this score may improve flow time.
   The source gives no definition of the score and no performance evidence."
7. **Format boundary:** "Improve the prose around this code block, preserving
   its executable code, field names, and LaTeX equation exactly."
8. **Scope boundary:** "Fix a simulator bug and run its unit tests. Do not
   rewrite its documentation or existing reports."

## Reviewer expectations

- 1 explains the route before notation. It defines reentrance as a return to a
  previously visited station without adding arrival or service distributions.
- 2 preserves the number of configurations, objective, comparator, effect size,
  and tested scope. It does not turn the experiment into a universal guarantee.
- 3 separates planning durations from actual service and preserves the
  one-operation commitment. It does not imply physical batching or immediate
  execution of future visits.
- 4 retains every condition and the restricted comparison class.
- 5 keeps verification and validation distinct, even if a synonym-rotation
  heuristic flags their use. Technical meaning takes priority over lint scores.
- 6 identifies missing information without inventing a causal explanation or
  upgrading "may improve" to "improves."
- 7 preserves code, identifiers, equations, and requested document structure.
- 8 stays a coding task. The writing skill does not start a report rewrite,
  simulation campaign, or extra Stage.
- Explanatory prose defaults to STE-flavored writing. Unambiguous text needs no
  forced rewrite. English writing guidance does not require translating other
  requested output languages.

## Automated checks

Run `python3 -m unittest discover -s tests/asd-ste100 -p 'test_*.py'` from the
repository root. The tests check bundled assets, provenance, local links, entry
and Stage pointers, upstream linter self-tests, and CLI behavior from an
unrelated directory. They do not assess the model's scientific claims, prove
meaning preservation, or certify STE compliance.
