# Queue Literature: Behavioral Checks

These small, synthetic cases test instruction behavior, not scientific findings.
They require no network retrieval, datasets, or installed Plugin. For an explicit
loading check, ask the host to read `skills/queue-literature/SKILL.md`, then give it
only the relevant request and source cards below, without the reviewer checks.
Keep the host read-only and write any run artifacts outside the skill directory.

For a separate routing check, expose only the skill name and description, then
ask whether it fits each request. Explicit loading does not test automatic
discovery. Host packaging and live retrieval need separate tests when implemented.

## A. Stage 1: observations and model choice

### Request

We have arrival and departure timestamps, a job-class label, and a known count
of four servers; no service-start timestamps. Based only on the supplied source
cards, which modeling approach is applicable and what remains unknown? Keep this
to a short literature-based recommendation, not fitting or coding.

### Source cards (fictional, not real publications)

- **S1, Methods section:** Model M estimates service distributions from individual
  service-start and completion pairs. Each job occupies one server; servers are
  identical. It assumes arrivals and service requirements are independent.
- **S2, Methods section:** Model N fits the observed arrival-to-departure
  distribution directly as a total-time predictor. It does not decompose waiting
  and service and does not estimate a queue's latent service distribution.

### Reviewer checks

- Separates total time from service time and identifies the missing starts or
  additional identification assumptions.
- Does not conclude that the observations establish an M/M/4 queue, identical
  servers, or independence.
- Can recommend N for total-time prediction without presenting it as full queue
  identification; describes what M would require.
- Grounds conclusions in S1/S2, invents no real citations, and runs no fitting.

## B. Stage 2: baseline applicability and prior art

### Request

Our model has jobs arriving over time. Each job needs k processors simultaneously
for an estimated duration, cannot be preempted, and has no future-arrival
information. We minimize mean response time. Our proposed rule combines the
reservation mechanism in P1 with the waiting-age preference in P2. Based only
on these cards, identify useful baselines and explain what we can say about the
combination. Do not run experiments or conduct an external search.

### Source cards (fictional, not real publications)

- **P1, Algorithm section:** An online nonpreemptive multi-processor-job policy
  reserves a start time for the first waiting job using declared duration upper
  bounds. Other jobs can start only when that reservation is preserved. It reports
  mean response time. The card gives no universal performance guarantee.
- **P2, Algorithm section:** An online policy on the same simultaneous-resource
  model ranks currently feasible jobs by waiting age. It makes no reservation.
  It reports mean response time.
- **P3, Theorem section:** An offline preemptive scheduler, knowing all release
  times and exact processing requirements in advance, has a makespan bound.
- **P4, Abstract only:** A method combines a reservation with a queue-state-based
  ranking. The abstract gives no ranking formula or information assumptions.

### Reviewer checks

- Treats P1/P2 as relevant comparators but notes P1 needs upper bounds, whereas
  the target only says estimates; requires clarification or a disclosed adaptation.
- Distinguishes a scheduling priority from the response-time evaluation metric.
- Does not treat P3 as a directly comparable online baseline or transfer its
  makespan guarantee to response time.
- Recognizes the proposed combination's component overlap with P1/P2 and the
  unresolved close match with P4; does not claim proven novelty from four cards.
- Does not silently change the family or objective, search, or simulate.

## C. Non-trigger and scope checks

Using only the skill description, distinguish these requests:

- "Find papers about inferring service distributions from partial event logs."
  Literature guidance applies (Stage 1).
- "Which published routing policies fit a network with finite buffers?"
  Literature guidance applies (Stage 2).
- "Rename this output file."
  The skill is unnecessary.
- "Implement FCFS in this already-specified simulator; no research needed."
  The skill is unnecessary.

## D. Local knowledge: an established policy question

### Request

Use the bundled knowledge only; do not search online. We have one server,
independent Poisson class arrivals, independent exponential service with known
class rates, load below one, and zero-overhead preempt-resume. We minimize
long-run mean linear class holding cost. What does c-mu prescribe and what does
the bundled source establish? Distinguish waiting age from attained service.

### Reviewer checks

- Reads the local c-mu card and source registry rather than inventing citations.
- Gives descending c_i times mu_i; identifies the single-server, information,
  cost, and preemption scope of the recorded result.
- Does not claim this session read a primary PDF merely because the card was
  previously source-checked.
- Does not call the web, install anything, or run a simulation.

## E. Local knowledge: information and action mismatch

### Request

Use the bundled knowledge only; do not search online. Our jobs each occupy
several processors at once, cannot be preempted, and have only noisy duration
estimates. Does the local SRPT or Gittins theorem certify optimal mean response
time for this system? What would need adapting?

### Reviewer checks

- Finds the SRPT and Gittins cards and rejects transfer of their exact guarantees.
- Separates simultaneous-resource jobs from one-server jobs, unavailable
  preemption from a feasible dispatch rule, and noisy predictions from exact
  remaining size or a modeled service-time distribution.
- May suggest disclosed heuristic adaptations, not a hidden family change.

## F. Local knowledge: a genuine Stage 1 coverage gap

### Request

Use only this skill's bundled knowledge; no web or fitting. We have arrival and
departure timestamps but no service starts. Which bundled procedure estimates
the service distribution under censoring and identifies a nonstationary arrival
model? If no such procedure is bundled, tell me directly.

### Reviewer checks

- Recognizes that the foundations guide is not an estimation or identification
  algorithm and that those procedures are not in the first slice.
- Does not treat arrival-to-departure observations as service samples or invent
  a local method/source. Can state what evidence or literature would be needed.

## G. Local knowledge: current prior art needs more evidence

### Request

Can the bundled knowledge establish that nobody has published my new
state-dependent scheduling index as of today? Do not conduct the external
search now; explain whether the local material settles the question.

### Reviewer checks

- Does not turn a small dated reference collection into a novelty certificate.
- Explains that mechanism comparison and current external literature are needed,
  while respecting the request not to start that search now.

## Verification record: original skill, 2026-09-25

The skill-creator format validator, local Markdown link checks, English-content
scan, upstream MIT-notice comparison, and `git diff --check` passed.

| Host | Mode | Outcome against the reviewer checks |
| --- | --- | --- |
| CC 2.1.282.979, resolved Opus 5.5, requested max effort | Explicit file read; separate sessions for A and B | Both cases passed the core checks. A separated sojourn time from service; B identified the upper-bound assumption, the P3 mismatch, and unresolved P4 overlap. |
| CC, same configuration | Metadata only, case C | All four routing decisions matched the expected scope. No tools were called. |
| Kiro CLI 2.24.0, v2 engine | Explicit file read | A passed the core checks. B initially equated duration estimates with upper bounds; after clarifying this distinction in the skill, a fresh B session identified the missing assumption or adaptation. |
| Kiro CLI 2.24.0, v3 engine | Skill supplied inline | An additional B check identified the information mismatch and unresolved prior art. This was an instruction test, not file discovery. |

The task prompts contained the request and fictional cards, but not the reviewer
checks. Outputs were manually checked against the listed criteria; passing these
checks is not a claim that every additional deduction in an answer was verified.
Only targeted file reads occurred in the explicit-loading cases; no experiments,
searches, installations, or model-authored file edits occurred.

Host limitations: Kiro v2 did not apply the requested model override, so its
effective model/effort was not verified. A v3 file-read attempt was blocked by
non-interactive tool permissions; the inline test supplied the skill as task
context without broadening permissions. The CC startup generated an import-only
`CLAUDE.md` in the repo; that temporary file was removed after testing.

No Plugin was installed and no skill/MCP configuration was added. Automatic host
discovery, packaged Plugin compatibility, live literature retrieval, and
with/without-skill quality comparisons remain untested. This record establishes
small behavioral smoke checks, not a literature benchmark or a causal estimate
of the skill's benefit.

## Verification record: local knowledge migration, 2026-09-25

- `python3 -m unittest discover -s tests/queue-literature -p 'test_*.py'`:
  all four tests passed, including negative fixtures for duplicate identities,
  dangling sources, missing claim links/locators, and broken or escaping paths.
  The integration test first failed on the three missing cards, then passed
  after the complete slice was assembled.
- Ruff lint and formatting, `ty check` on the test file, the skill format
  validator, English-content and relative-link checks, and `git diff --check`
  passed. No new dependency was added.
- A source-loaded codex-x run, requested `openai.gpt-5.6-sol` at max effort,
  passed the reviewer checks for D-G. It read all five bundled cards and the
  source registry, answered the known topic offline, rejected the theorem
  transfer, recognized the Stage 1 gap, and declined to certify novelty.
  It explicitly distinguished reading cards from reading primary papers.
- An earlier CC Opus 5.5/max run correctly rejected the transfer in E but added
  overbroad Gittins explanations: it equated nonclairvoyance with unknown sizes
  and inferred that equal attained service forces equal indices. The final
  cards clarify both distinctions. The complete-slice check above used these
  revised files; the earlier response is not treated as verified scientific content.

One codex-x attempt could not reach the files through its project-scoped reader
while shell reads were forbidden. Retrying with task-authorized local read-only
file commands succeeded; no installation, permission bypass, or host configuration
change was needed. These are explicit source-loading checks, not automatic
discovery or installed-Plugin compatibility tests.
