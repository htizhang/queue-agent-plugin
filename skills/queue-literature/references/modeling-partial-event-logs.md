# Inferring Queues from Partially Logged Tasks

| Field | Value |
| --- | --- |
| ID | modeling.partial_event_logs |
| Kind | modeling-method |
| Stage relevance | Stage 1 |
| Aliases | missing events, queue inference, latent service, Bayesian reconstruction |
| Sources | sutton_jordan_2011_queue_inference |
| Review | source-checked |
| Reviewed on | 2026-09-25 |
| Legacy origin | New contribution |

## Method and applicability

Sutton and Jordan model queueing dynamics as a transformation from service times
to event times. Missing events become latent variables; MCMC supports Bayesian
parameter inference or stochastic EM. This is model-conditioned reconstruction,
not direct measurement of missing service times.

The implemented model specifies the network and queue disciplines and uses
independent exponential service times by queue. Broader service families are
discussed as extensions, not established by those experiments.

Their observation scheme randomly selects tasks for detailed logging, records
their per-job arrival, departure and queue, and records cumulative total task
entries at observed entries. Adaptive logging is outside that scheme. Do not
transfer it unchanged to logs lacking job linkage or workload-count information.

## Evidence

[sutton_jordan_2011_queue_inference](sources.json), arXiv v3 electronic reprint,
Sections 2.4, 3.1-3.2 and 6-8. Relevant full text inspected; reprint pagination differs
from the journal. No universal identifiability claim is made here.

## Use in this Plugin

Identify the observation mechanism before choosing an estimator. Keep inferred
service and waiting times labelled as posterior/model-dependent quantities.
