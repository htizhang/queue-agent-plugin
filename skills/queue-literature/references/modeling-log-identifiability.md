# What queue logs can and cannot identify

Separate three levels of evidence:

- **Observed:** read directly from records after event semantics are validated.
- **Reconstructed:** calculated deterministically under stated queue mechanics
  and a known initial state.
- **Model-conditional:** a distribution, expectation, or posterior obtained only
  after adding stochastic assumptions.

Calling all three "observed" hides the main uncertainty in queue-log analysis.

## Complete linked lifecycles

With trustworthy, job-linked arrival or queue-entry, execution, and exit events,
one can directly calculate waits to first service, elapsed execution episodes,
and sojourns. The occupancy path follows from arrivals and exits if the initial
population is known. Active service work still needs the pause, preemption, and
resource-sharing qualifications in
[Reading Queue Event Logs Correctly](modeling-event-log-semantics.md).

Even a perfect record of arrival and start order does not identify the scheduling
rule. FCFS, a priority rule whose priorities happened to agree with arrival order,
and several tie-breaking rules can produce the same trace. Use such agreement as
a compatibility check, not proof of a discipline.

## Linked arrivals and departures, but no starts

The wait/service split is not observed. It can be reconstructed when the queue
mechanics are known.

For a single-server, work-conserving, nonpreemptive FCFS queue, order jobs by
arrival and use

`u_j = max(a_j, d_(j-1))`, `w_j = u_j - a_j`, and `s_j = d_j - u_j`,

provided the server's availability before the first recorded job is known. If the
window begins with an unknown job in service or an unknown backlog, this recursion
does not have a known starting point.

For a multiserver FCFS queue, reconstruction additionally needs:

- the server count, or more generally the capacity schedule;
- the availability of every server at the start, or complete earlier history;
- linked departures for the recorded jobs;
- work-conserving FCFS entry to service, nonpreemptive exclusive execution, and
  no hidden pauses or setup states; and
- a defined rule for simultaneous events and server-availability ties.

Each arrival starts when it arrives or when the earliest eligible server becomes
free, and its service is departure minus that reconstructed start. Sutton and
Jordan give this deterministic departure-time transformation for a fixed
`K`-processor FCFS model ([sutton_jordan_2011_queue_inference](sources.json)).
The calculation is valid under the model; a good fit does not establish that the
real discipline or server count was that model.

## Service starts and completions only: classic transactional-data inference

The classic Queue Inference Engine (QIE) studies logs containing service starts
and completions but not the arrivals that occurred while all servers were busy.
A completion followed almost immediately by a new start is treated as evidence
that a customer was waiting. Runs of these replacements define congestion
periods.

Under homogeneous Poisson admitted arrivals and the assumption that all servers
are busy whenever anyone waits, the method conditions on the observed
congestion-period signature. It estimates:

- the conditional distribution or conditional expectation of cumulative hidden
  arrivals and queue length over that congestion period;
- an expected time-average queue length and aggregate mean waiting time; and
- a conditional distribution of queue length seen by an arrival.

These are not the realized hidden arrival times or the observed queue trajectory.
The homogeneous Poisson rate cancels after conditioning on the number of arrivals;
that does not make the result arrival-model-free. Larson's slowly varying-rate
extension is approximate. Bertsimas and Servi's nonhomogeneous Poisson extension
requires the cumulative intensity, and their renewal extension requires the
interarrival distribution
([larson_1990_queue_inference](sources.json);
[bertsimas_servi_1992_queue_inference_revisited](sources.json)).

The aggregate queue-length inference does not require a service-time
distribution or FCFS; it does require the work-conserving congestion signature
and the chosen arrival model. Per-customer waiting times need an additional
qualification. In Bertsimas and Servi's notation, the proof uses
`W_k = t_k - X_k`: it pairs the kth ordered arrival with the kth service start.
Interpret that as the actual kth starter's wait only when this pairing is
justified, for example by FCFS or reliable customer linkage. Otherwise it is a
rank-paired model quantity, not an observed individual wait.

Because the arrivals of interest are missing, the same transactional records
cannot by themselves validate the Poisson premise. Report sensitivity to
plausible arrival models and, where possible, compare the inferred queue with an
independent occupancy sample.

## Unlinked arrival and departure streams

If both boundary streams are complete, cumulative arrivals minus cumulative
departures reconstructs changes in occupancy. Absolute occupancy still needs the
initial count. Without job linkage, individual sojourns are not observed; order
agreement alone does not supply the links. Aggregate time-in-system estimates
must use the population, window, and boundary accounting described in
[Reading Queue Event Logs Correctly](modeling-event-log-semantics.md).

There is a narrow model-specific exception. Brown proves consistent recovery of
the service-time distribution from unlinked arrival and departure epochs for an
equilibrium `M/G/infinity` system: stationary Poisson arrivals, independent and
identically distributed service times, infinitely many servers, and finite mean
service. The arrival rate and initial number in service need not be known
([brown_1970_mginf_estimation](sources.json)). This is not a general result for
finite-server queues, non-Poisson input, or arbitrary operational logs.

With departures alone, throughput and interdeparture times are observed, but
service requirements, arrival demand, queue length, discipline, and server count
are not generally identified.

## What to report

For every inferred quantity, state:

1. the events and links actually observed;
2. the initial state and capacity information available;
3. the discipline, work-conservation, pause, sharing, and arrival assumptions;
4. whether the result is observed, reconstructed, or model-conditional;
5. the population and averaging viewpoint; and
6. which assumptions received sensitivity checks or independent validation.

Prefer direct occupancy and start records when the downstream policy depends on
queue state or service order. Do not use a conditional reconstruction as
ground-truth labels for evaluating the assumptions that created it.

## References

[sutton_jordan_2011_queue_inference](sources.json), arXiv v3, Section 2,
equation (1), pp. 5-6; Section 2.1, equations (2)-(3), pp. 6-7; Section 2.4,
p. 10;
[larson_1990_queue_inference](sources.json), abstract and Section 1; Sections
4.3-4.7; Section 5;
[bertsimas_servi_1992_queue_inference_revisited](sources.json), abstract and
introduction, p. S217; Section 1.1, p. S218; Theorem 2 and proof,
pp. S222-S223; Theorem 4 and following remark, p. S224;
[brown_1970_mginf_estimation](sources.json), Section 0, p. 651; Section 1,
pp. 652-653, especially Theorem 1.
