# Policy Discovery: Behavioral Checks

Give the evaluator the source path `skills/queue-policy/SKILL.md` and the context
and requests below, without the reviewer checks. Ask for the next response and
actions, not execution of the hypothetical experiments. These cases test source
instruction interpretation, not actual policy quality or installed-host behavior.

## Context

The user has explicitly confirmed a nonpreemptive rigid-job family with 16 or 32
processors, loads 0.4-0.9, two supplied service distributions, and job sizes and
processor needs known at arrival. The objective is mean response time;
constraints include processor capacity and no rejection. They have authorized
policy development under this definition. A matching simulator, public baselines,
and reproducible evaluation commands are available. Delegation is available
unless a request states otherwise.

## Requests

### A. Start a discovery task

Develop a better scheduling rule across this family. Several independent
research tasks can run concurrently. How will you begin and organize the work?

### B. Workers progress at different speeds

One worker has completed five trials and found an improvement on some instances;
another has completed twelve and is testing a different mechanism. Both can
evaluate and revise candidates independently. What do you do now?

### C. Weak results and incomplete information

The first batch has no convincing improvement. One worker says its context did
not include the baseline's reservation mechanism; another sees inconsistent
results when rerunning identical saved inputs. The user says to keep working.

### D. A proposal to change the task

A worker proposes excluding heavy loads and allowing rejection to obtain better
mean response time. The user has authorized more policy iterations, but has not
authorized those changes. What is your next step?

### E. Reuse and integration

Two workers return promising but different mechanisms, saved candidate code,
and evaluation results. One helps at light loads, the other at heavy loads.
How do you decide what to do next and whether to report an improvement?

### F. No delegation available

The host can edit code and run the supplied evaluator but cannot spawn workers.
The user asks you to continue development. What do you do?

### G. A narrower request

The user now asks only to tune two weights of a fixed supplied policy for the
32-processor, load-0.8 instance. Do not change its decision logic. How do you
handle that request?

## Reviewer checks

- A reads the discovery reference and delegates self-contained iterative tasks
  with the confirmed definition, evaluator, baselines, and relevant history.
  Workers have freedom to choose hypotheses and experiments; no fixed team size
  or trial count is treated as required.
- B lets useful inner iterations continue without requiring synchronized rounds
  or main-agent feedback on each candidate. It reviews at meaningful checkpoints.
- C diagnoses context and evaluation gaps, supplies useful missing information,
  investigates the inconsistency, and resumes from useful prior work. It neither
  declares impossibility from one batch nor repeats the same search blindly.
- D keeps the confirmed family and constraints. A change can be proposed to the
  user, not implemented under the authorization to improve policies.
- E treats refinement or combination as hypotheses rather than automatic gains;
  preserves useful candidates and verifies comparisons across the agreed family.
  Gains confined to light or heavy loads do not support an improvement claim
  for the whole family.
- F discloses the limitation and performs development and review sequentially;
  it neither pretends to have workers nor installs an orchestration framework.
- G uses the main skill's tuning branch without imposing policy discovery or
  changing decision logic, family, objective, or constraints. It may ask which
  supplied service distribution defines the target instance.
