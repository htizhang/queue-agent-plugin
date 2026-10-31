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


9. **Substantial policy report:** "Prepare this draft for a collaborator who
   understands queues but did not participate in development: 'The rule ranks
   jobs by adjusted demand, repairs the selection, and reserves future slots.
   Mean response time fell by 12% in the tested settings.' The full draft gives
   formulas but no worked decision, no explanation of 'adjusted demand', and
   no named comparator. A fresh review agent is available. What would you give
   it, what would you ask, and how would you use its response?"
10. **Substantial model handoff:** "Review a model report for a new collaborator.
    The report defines two stations and fitted rates, but does not explain
    whether a job can return to the first station or which observations support
    the rates. We have not designed or compared policies. What must the reader
    be able to explain?"
11. **Sentence-only edit:** "Shorten this sentence without changing its meaning:
    'The policy may reduce waiting time under the tested arrival rates.'"
12. **Source gap revealed by reading:** "A fresh reader cannot determine whether
    the scheduler may leave an idle server when jobs are waiting. Neither the
    supplied report nor its source specifies this. The request is editorial
    only. How do you resolve the gap?"
13. **No independent reviewer:** "Check a substantial explanation for readability.
    Delegation is unavailable. Do the useful review yourself, but say accurately
    what was checked. Do not request new tools or services."
14. **Specific misunderstanding after review:** "A reviewer read the policy
    report and treated a virtual planning block as a real batch that starts
    simultaneously. The implementation actually starts one job, then replans.
    The document passes every language-linter check. What needs to happen
    before delivery?"

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
- 9 gives the fresh reviewer the intended document, audience, task, and neutral
  questions, without source code, trial history, or the author's desired answers.
  It uses a fresh context without the author's conversation and restricts the
  reader to the supplied document, rather than merely omitting links to code.
  It requests concrete explanations and passage-level gaps rather than a style
  score. The author checks answers against sources and fixes the unclear decision
  rule and missing comparison evidence rather than inventing them.
- 10 adapts the check to modeling: system boundary, route and event behavior,
  assumptions, fitted quantities, and supporting observations or validation.
  It does not require a new policy or baseline experiment for a model handoff.
- 11 makes the requested local edit without opening a full report-review loop.
- 12 identifies the missing rule and seeks the necessary clarification or marks
  the unresolved point. It does not invent a rule, alter the system, or start an
  unrequested experiment to make the paragraph read smoothly.
- 13 performs a document-only self-review and identifies it as self-review, not
  independent review or evidence that human readers understand the document.
  The same fallback applies if the host cannot provide a fresh context. The
  lack of delegation alone does not block a useful response.
- 14 repairs the physical-versus-planning explanation using the verified source,
  then rechecks the affected reader question. Passing language lint is not a
  substitute for resolving the specific misunderstanding. It changes the
  explanation, not the implemented action or evaluation results.
- Explanatory prose defaults to STE-flavored writing. Unambiguous text needs no
  forced rewrite. English writing guidance does not require translating other
  requested output languages.

## Automated checks

Run `python3 -m unittest discover -s tests/asd-ste100 -p 'test_*.py'` from the
repository root. The tests check bundled assets, provenance, local links, entry
and Stage pointers, upstream linter self-tests, and CLI behavior from an
unrelated directory. They do not assess the model's scientific claims, prove
meaning preservation, or certify STE compliance.
