# Reading queue event logs correctly

A timestamp becomes a queueing measurement only after its event meaning and
system boundary are fixed. Do this before fitting arrival or service
distributions.

## Define the lifecycle

Use an event dictionary for each source system. At minimum, distinguish:

| Log event | Queue interpretation | Common mistake |
| --- | --- | --- |
| Request offered | A demand reaches the system, including work later rejected, blocked, or abandoned before admission | Calling admitted work the full demand stream |
| Request admitted or enqueued | A job enters the modeled population or waiting room | Treating admission as service start |
| Scheduled or assigned | Work is planned for, or reserved to, a resource | Counting reservation time as processing |
| Start or resume | An execution episode begins | Assuming a field named `start` has this meaning |
| Suspend, preempt, or release | The job stops receiving this resource's capacity but may remain in the system | Leaving paused time inside a service sample |
| Complete | An activity or service episode finishes | Treating an intermediate activity completion as system exit |
| Abandon, reject, cancel, transfer, or exit | The job leaves a queue, activity, or system boundary | Combining operationally different exits without choosing an estimand |

The XES lifecycle vocabulary makes similar distinctions among `schedule`,
`assign`, `start`, `suspend`, `resume`, `complete`, `withdraw`, and abort events
([tfpm_xes_lifecycle_extension](sources.json)). It is a useful vocabulary, not
proof that a vendor field follows those semantics. Verify the mapping from system
documentation, examples, and record linkage.

Keep offered and admitted arrivals separate. Capacity controls, appointment
rules, retries, and rejection can make the admitted stream very different from
the demand presented to the system. Also state whether an exit ends the whole
customer journey or only one station visit.

## Separate elapsed occupation from service work

For nonpreemptive work on one exclusive resource, a verified execution start and
resource release can define an elapsed service interval. Even then, check whether
setup, handoff, or after-work belongs to the service definition.

With suspensions or preemption, add the active execution episodes rather than
using the first start to final completion. With a shared processor, elapsed time
and intrinsic work are different quantities. In the normalized
processor-sharing model, a job's required work is the integral of its capacity
share; with equal sharing this is
`integral from arrival to departure of 1/N(t) dt`, not simply
`departure - arrival` ([sutton_jordan_2011_queue_inference](sources.json)).
Parallel execution similarly requires resource-allocation records if the target
is processor time rather than wall-clock latency.

Therefore `complete - start` is not automatically an exclusive service
requirement. Record whether it represents wall-clock occupation, active resource
time, or modeled intrinsic work.

## Choose the population and the averaging viewpoint

These summaries answer different questions:

- A **time population** contains every job present at each time, including jobs
  already present when the window opens.
- An **arrival cohort** contains jobs admitted during the window. Full sojourns
  require following those jobs after the window closes.
- A **departure cohort** contains jobs that leave during the window.
- A **completed-inside cohort** contains only jobs whose arrival and departure
  both fall inside the window; it preferentially excludes long durations.

Likewise, a time average of queue length, an average queue length seen just before
arrivals, and a customer average of waits are not interchangeable. Under the
lack-of-anticipation condition, homogeneous Poisson arrivals see the long-run
time average when the relevant limits exist. On a finite interval, Wolff equates
the expected number of arrivals that see a state with the arrival rate times the
expected time spent in that state. A realized arrival average need not equal the
realized time average. With time-varying Poisson arrivals, arrivals see an
arrival-rate-weighted time average instead of the plain time average
([wolff_1982_pasta](sources.json)). Admission control can also break the premise
even when offered arrivals are Poisson.

## Use exact finite-window accounting

Let job `j` be in the modeled system on `[a_j, d_j)`, and let `N(t)` count every
job present, including initial jobs. For any observation window `[0,T]`,

`integral_0^T N(t) dt = sum_j |[a_j,d_j) intersect [0,T]|`,

where each clipped contribution is

`max(0, min(d_j,T) - max(a_j,0))`.

This is a pathwise area identity. It remains valid with nonempty endpoints if all
jobs that intersect the window are included. The right side contains clipped
occupancy contributions, not the full mean sojourn of the arrivals in the window.

For the arrival cohort, let `A(T)` be the number of arrivals in `[0,T]`,
`lambda_bar = A(T)/T`, and `W_A` the average **full** sojourn of those arrivals.
For `A(T) > 0`, Kim and Whitt's boundary relation can be written as

`L_bar/lambda_bar - W_A = [R(0) - R(T)]/A(T)`,

where `R(0)` is the total remaining sojourn after time 0 of jobs already present
at 0, and `R(T)` is the total remaining sojourn after time `T` of jobs present at
`T`. Thus empty endpoints are sufficient for the usual finite-window equality,
but they are not necessary: nonzero boundary terms can cancel. If the future
departures are unavailable, the full arrival-cohort correction is not observed.
Replacing full sojourns with clipped intervals forces an accounting equality but
turns them into censored or partial durations
([kim_whitt_2013_littles_law_statistics](sources.json)).

## Practical audit

Before using a log:

1. State the modeled boundary, job identifier, offered/admitted arrival, queue
   entry, execution events, and every exit type.
2. Check clock basis, timestamp resolution, ties, duplicate events, retries, and
   missing lifecycle transitions.
3. Record the initial population, final population, and capacity changes.
4. Name the cohort and whether each statistic is a time, arrival, or departure
   average.
5. Treat open jobs as censored for full-duration estimation rather than silently
   dropping or clipping them.
6. Distinguish an accounting check from validation. Recomputing both sides from
   the same linked events checks implementation consistency; an independent
   occupancy or resource-busy signal can also test whether the event mapping is
   credible.

## References

[tfpm_xes_lifecycle_extension](sources.json), standard lifecycle transition
model page, transition definitions;
[sutton_jordan_2011_queue_inference](sources.json), arXiv v3, Section 2.3,
equation (7), pp. 7-8;
[kim_whitt_2013_littles_law_statistics](sources.json), Section 2.1 and
Section 2.2, equations (4)-(7) and Theorems 1-2, pp. 1032-1034; Section 2.3,
equations (8)-(9) and Theorem 3, p. 1034;
[wolff_1982_pasta](sources.json), lack-of-anticipation assumption and Theorem 1,
p. 225; equation (3) and Remark 4, p. 226; Section 3 and Theorem 2,
pp. 227-228.
