---
name: queue-modeling
description: Build, calibrate, and validate executable queue simulators from data and system descriptions. Use for Stage 1 queue modeling, including revising an existing simulator against observations and preparing it for policy evaluation.
---

# Queue Modeling

Turn the supplied data and system description into an executable queueing model
that can generate trajectories and simulate the consequences of different
policies. Work at the scope the user requests: discuss modeling choices when
asked to discuss, and construct or revise the simulator when asked to implement.

## Establish what the model represents

Identify jobs or customers, resource pools, routing, capacity, and the system
boundary. Determine what decisions a controller can make, when those decisions
occur, and what information is available at that time.

Inspect the records before fitting: event meanings, units, identifiers, logging
windows, missing events, and censoring. Distinguish observed quantities from
latent mechanisms. Arrival-to-departure time includes waiting; it is not a direct
service-time sample. Separate the historical policy that generated the data from
the system mechanisms that should remain in place when policies change.

Use available evidence to choose a working model. Make consequential assumptions
explicit; ask the user when a missing detail would materially change the model.
Where observations support several plausible explanations, retain the relevant
alternatives or expose the uncertain component for sensitivity checks.

## Construct an executable model

Choose a representation and simulation tool suited to the system and available
environment. Reuse an existing simulator when it fits the required mechanisms.

- Represent state and event timing sufficiently to execute the modeled dynamics;
  elapsed service, waiting ages, or scheduled events may matter beyond queue
  lengths.
- Implement system rules separately from statistical estimates of arrivals,
  service, routing, abandonment, or other uncertain mechanisms. Fit estimates
  using methods appropriate to the observations and their dependencies.
- Expose policy decisions through a clear interface: decision timing, observable
  information, feasible actions, and how actions affect the system. Keep latent
  simulator state distinct from information available to a policy.
- Keep system dynamics, replaceable policies, and performance measurements
  separate. Model any action-dependent changes to the stochastic mechanisms
  rather than assuming every fitted distribution stays unchanged under control.
- Make configurations and random seeds explicit. Produce trajectories or event
  records that support both comparison with the input data and downstream policy
  evaluation.

Run a small case as soon as the model is executable. Use failures to improve the
representation or implementation before expanding the experiment.

## Obtain independent, executable feedback

Prefer a separate validation subagent when the host supports delegation. Give it
the original data and system description, observation definitions, candidate
simulator, and execution instructions. Ask it to develop checks from that
evidence, rather than merely confirm the builder's explanation.

The validator should run the simulator and report concrete discrepancies, their
supporting observations or test outputs, and how to reproduce them. Useful checks
depend on the system:

- **Mechanics:** flow accounting, capacity, event ordering, routing, and action
  feasibility; hand-checkable cases or analytical special cases when applicable.
- **Data agreement:** compare simulated and observed quantities under matching
  observation windows, logging rules, and the historical policy. Use held-out
  periods or records where feasible, preserving relevant temporal dependence.
  Compare stochastic behavior distributionally rather than requiring identical
  random trajectories.
- **Policy use:** exercise alternative feasible actions and check that constraints
  and information boundaries remain valid. Distinguish behavior supported by the
  observed data from extrapolation to new policies or operating conditions.

Adapt the checks and delegation to the task. The main agent owns integration:
resolve feedback against evidence, revise the code or modeling assumptions, and
rerun affected checks. Keep feedback-driven iteration focused on issues that
change the model's adequacy for its intended use.

## Reuse the shared knowledge

When a modeling choice needs domain guidance, use
[queue-literature](../queue-literature/SKILL.md). Its Stage 1 topic map covers
system primitives, state and dynamics, log semantics, identification, statistical
fitting, and model validation. Read the relevant local note first; use its
literature workflow when the available evidence leaves a material question open.

## Deliver a usable simulator

Provide the executable model, fitted configuration, and concise instructions to
run it, set randomness, and supply a policy. Include a short account of the
modeled system, material assumptions, validation results, and remaining issues
that affect its use. Keep generated artifacts in the user's task workspace.

Completion means the simulator runs through its documented interface and the
checks support the intended modeling use. Report unresolved failures explicitly.
The user can then use the model for Stage 2; policy search remains a separate
task.
