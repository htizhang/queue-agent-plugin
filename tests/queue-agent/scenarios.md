# Queue Agent: Routing Checks

These are source-loaded instruction tests, not installed-host discovery tests.
Give the evaluating agent the entry skill and the requests below, but not the
reviewer checks. Ask for the intended first response and next action; do not
execute the hypothetical research tasks or install anything.

## Requests

1. "Here are a clinic's event logs and operating description. Build a simulator
   so that we can later try different dispatch policies."
2. "We already have a tested simulator and configuration for our batch queue.
   Improve mean response time by developing scheduling rules on top of it."
3. "Study nonpreemptive parallel-server queues with known job sizes and variable
   processor requirements. Arrivals and service distributions are specified
   mathematically. Build an evaluator and compare scheduling policies; there are
   no operational logs."
4. "Before coding anything, explain the distinction between arrival-to-departure
   observations and service requirements, and give sources."
5. "We finished modeling earlier. Now hold that model fixed and compare FCFS
   with shortest-job-first."
6. "I have an old simulator, but it does not match the supplied logs. Check what
   it assumes and revise the model before we use it for decisions."
7. "Change this unrelated web page's heading to 'Contact us'."
8. "Use these service-center records to build a model and then compare routing
   rules. We have no simulator yet."

## Reviewer checks

- 1 starts with Stage 1 and replaceable policy support, not a policy-search
  campaign the user did not request.
- 2 starts Stage 2 from the available simulator; it can inspect its interface
  without demanding a new Stage 1 or operational logs.
- 3 treats evaluator construction as preparation for the specified Stage 2
  problem, rather than equating all simulator code with data-driven inference.
- 4 uses shared knowledge/literature and respects discussion-only scope.
- 5 changes the active task to Stage 2 without recalibrating the fixed model.
- 6 uses Stage 1 despite the existence of a simulator.
- 7 does not force either Stage or queue literature onto an unrelated task.
- 8 starts with Stage 1 and retains the requested policy comparison as the next
  task, rather than stopping permanently at modeling or pretending a model exists.
- Missing details produce targeted questions, not a mandatory intake template.

## Automated checks

`test_session_start.py` executes the actual hook command with each documented
root-variable convention, from an unrelated working directory and a Plugin path
containing spaces. It checks the JSON context envelope, the entry-skill path,
and that lifecycle inputs do not select or persist task state. These checks do
not establish host discovery, hook trust, or Windows shell support.

## Verification record: 2026-09-26

- Skill format validation, Ruff lint/format, `ty check`, Markdown local-link
  checks, three hook tests, and seven existing knowledge tests passed.
- A source-loaded CC review used `claude-opus-5-5[1m]` with max effort requested.
  Its eight responses matched the routing checks above, including direct Stage 2
  evaluator construction without logs, model repair despite an existing
  simulator, discussion-only work, and the unrelated request. This checked
  proposed next actions, not execution or scientific quality of those tasks.
- The reviewer identified two ambiguities in the short hook text. It now says
  Stage 1 works from data and a system description, and describes the Stages as
  capabilities rather than a mandatory sequence. Automated checks were rerun
  after those edits; the wording revision was not a second live-agent test.
- No Plugin was installed or enabled. Automatic skill discovery and host-managed
  hook loading remain untested. Local review artifacts are in the ignored
  `output/queue-agent-entry/` directory.
