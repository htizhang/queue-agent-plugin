# Queue State and Dynamics

A fitted arrival or service distribution is not yet a queue model. The model also needs a state, admissible actions, and transition rules. At decision epochs, a controlled state is sufficient when the next transition depends on the modeled past only through the current state and current action. If $H_n$ is the full modeled history through decision epoch $n$, $S_n$ is the state, and $A_n$ is the chosen action, this one-step property is

$$
\Pr\{S_{n+1}\in B\mid H_n,A_n=a\}
=K(B\mid S_n,a).
$$

The kernel $K$, together with later actions, generates the whole modeled future. For example, under a fixed Markov continuation policy $\pi$, later actions are $A_m=\pi(S_m)$. The current action alone does not determine those later choices. State sufficiency is therefore relative to the transition model, feasible actions, and policy information, not a claim that the state contains every real-world fact. Keep three objects distinct:

- the **physical state**, which may contain latent information needed to evolve the model;
- the **controller observation**, which contains only information available when a decision is made; and
- the **event calendar**, a computational record of already scheduled events, which may include future random times that a real controller cannot observe.

## When counts are enough

For Poisson arrivals, exponential service, and exponential patience, elapsed times do not change the corresponding residual distributions. This memorylessness can make queue counts, server occupancy, job class in service, and an availability indicator sufficient. The $M/M/N+M$ call-center model is a canonical example: its total population is a birth-and-death process, with service and abandonment departures determined by the current count [garnett_mandelbaum_reiman_2002_erlang_a](sources.json).

Counts cease to be sufficient when a transition hazard depends on elapsed time or history. If a duration has cdf $G$ and density $g$, its age-dependent hazard is

$$
h(a)=\frac{g(a)}{1-G(a)}.
$$

Unless $h(a)$ is constant, two customers with the same class and different ages generally have different next-event distributions. A useful state check is therefore:

| Mechanism | Count-state can suffice when | Information commonly needed otherwise |
| --- | --- | --- |
| Arrivals | constant-rate Poisson; nonhomogeneous Poisson after including the relevant clock | absolute time, renewal age, scheduled next arrival, or a finite history summary |
| Service | exponential within each modeled class | attained service or residual service for every job in service |
| Abandonment | exponential patience within each modeled class | waiting age, patience residual, or deadline |
| Availability | exponential up- and down-times | elapsed or residual repair, setup, vacation, or outage time |
| Queue order | customers within a class are exchangeable for the objective | ordered class sequence, priorities, deadlines, or customer identities |

For general service and patience distributions, Kang and Ramanan use measure-valued state components that retain service ages and potential waiting ages; they also retain the backward recurrence time of a renewal arrival process. Their descriptor $(\alpha_E,X,\nu,\eta)$ illustrates the principle: add precisely the age or history information on which future hazards depend [kang_ramanan_2010_many_server_reneging](sources.json). A finite list of ages is often the practical counterpart of their measure-valued representation.

Time itself may be part of the state. With arbitrary known time-varying primitives such as $\lambda(t)$, the queue can be treated as time-inhomogeneous in its physical state, or absolute clock time $t$ can be appended to form an augmented Markov state. If all policy-relevant time variation has a common period $P$, the phase $t\bmod P$ is sufficient instead; phase alone cannot represent an arbitrary trend or terminal date. Conversely, replacing a nonexponential service time by a fresh draw whenever service resumes silently changes the physical model. Preserve attained service or a sampled residual unless memorylessness or a stated restart rule justifies discarding it.

## Write the transition system before choosing a simulator

List every event that can change state, its enabling condition, its state update, and what future events it schedules or cancels. Typical queue events are:

- **arrival:** create a customer, assign class and attributes, join a queue or enter service, and schedule the next exogenous arrival when appropriate;
- **service start or assignment:** remove a waiting customer, occupy a compatible server, and establish a completion clock;
- **service completion:** release the server, record departure or routing, and create a new dispatch decision;
- **abandonment:** remove a still-waiting customer and cancel any obsolete patience event;
- **availability change:** fail, repair, begin or end a shift, setup, vacation, or break, with an explicit interruption rule.

A next-event representation stores future events in time order, advances the clock to the earliest event, applies that event's state update, and then schedules or cancels events. Simultaneous events need an explicit tie rule because “completion before abandonment” and “abandonment before completion” can produce different sample paths. Choi and Kang give this event/update/calendar decomposition and a single-server arrival-load-unload example [choi_kang_2014_discrete_event_simulators](sources.json).

The calendar is one way to execute the dynamics, not the dynamics themselves. The same model may instead be described by transition rates, stochastic recursions, or differential equations. Write those rules independently enough that a second implementation could check them.

## Separate physics, the incumbent policy, and the candidate controller

This separation is a modeling synthesis:

- **Physical requirements** constrain what can happen: capacity, compatibility, precedence, nonpreemption, travel time, outages, and whether intentional idling is possible.
- **The incumbent policy** describes how the observed system selected among physically feasible actions: FCFS, class priority, batching, manual overrides, or local routing habits. It is needed when reproducing historical outputs, but it is not automatically a law of nature.
- **A candidate controller** chooses from the admissible action set using only its stated observation. It must not use latent service requirements, future arrivals, or calendar entries unless those are genuinely available.

This prevents two common errors: optimizing over impossible actions and freezing today's operating rule into the “physical” model so that no alternative policy can be represented.

## Worked model: two classes and one unreliable server

Consider an original small model with class-$i$ Poisson arrivals of rate $\lambda_i$, an exponential required amount of server up-time with rate $\mu_i$, and exponential waiting-patience rate $\theta_i$, for $i\in\{1,2\}$. One server fails after an exponential up-time with rate $\beta$ and is repaired at rate $\gamma$. Service is nonpreemptive by the controller. A failure pauses the current job; repair resumes it. Because required service is exponential in accumulated up-time, no attained-service variable is needed for this pause-resume rule.

Use the state

$$
x=(q_1,q_2,j,u),
$$

where $q_i$ is the number of waiting class-$i$ customers, $j\in\{0,1,2\}$ is the class in service ($j=0$ means none), and $u\in\{0,1\}$ indicates whether the server is up. Define the action set on up-idle states; a nontrivial decision occurs when someone is waiting. For a work-conserving controller,

$$
\mathcal A(x)=
\begin{cases}
\{0\}, & q_1+q_2=0,\\
\{i:q_i>0\}, & q_1+q_2>0,
\end{cases}
$$

where action $i$ assigns that class and action $0$ leaves an empty server idle. Assignment is the instantaneous map

$$
\Phi_i(q_1,q_2,0,1)=(q_1-\mathbf 1\{i=1\},\ q_2-\mathbf 1\{i=2\},\ i,\ 1).
$$

If intentional idling is physically permitted and relevant to the policy question, add action $0$ in nonempty states; otherwise excluding it records the work-conserving requirement explicitly.

Between decisions, the raw stochastic transitions are

$$
\begin{array}{lll}
\text{class-}i\text{ arrival:} & q_i\leftarrow q_i+1, & \text{rate }\lambda_i,\\
\text{class-}i\text{ abandonment:} & q_i\leftarrow q_i-1, & \text{rate }\theta_iq_i,\\
\text{service completion:} & j\leftarrow0, & \text{rate }\mu_j\mathbf 1\{u=1,j\ne0\},\\
\text{failure:} & u\leftarrow0, & \text{rate }\beta\mathbf 1\{u=1\},\\
\text{repair:} & u\leftarrow1, & \text{rate }\gamma\mathbf 1\{u=0\}.
\end{array}
$$

At initialization and after any event that produces an up-idle state with a nonempty queue, dispatch is a decision epoch and the controller applies one admissible assignment. The service-completion clock runs only in server up-time: its rate is zero while $u=0$, and the exponential residual property permits service to resume after repair without an age variable. An event-calendar implementation may store sampled future event times, but the controller observes only $x$, or a stated function of $x$; it cannot use those future calendar entries.

The class-level conservation equation supplies an immediate check. With
$N_i(t)=q_i(t)+\mathbf 1\{j(t)=i\}$,

$$
N_i(t)=N_i(0)+A_i(t)-C_i(t)-R_i(t),
$$

where $A_i,C_i,R_i$ count arrivals, completed services, and abandonments. Dispatch, failure, and repair do not change $N_i$. Any sample path violating this equation has an event-accounting error.

The state is sufficient for class-selection decisions and class-level outcomes under the stated exponential assumptions. It is not sufficient to reproduce exact FCFS order or individual waiting-time ages; those questions require an ordered queue, customer records, or age information. That difference is a change in modeled granularity, not merely an implementation detail.

## Source references

- [garnett_mandelbaum_reiman_2002_erlang_a](sources.json), §1, pp. 208–211, and Appendix B, pp. 221–222: $M/M/N+M$ assumptions, count process, and state-dependent departure rates.
- [kang_ramanan_2010_many_server_reneging](sources.json), arXiv v1 electronic reprint, §1.1, pp. 2–4; §2.1–§2.2.4, pp. 7–15, especially (2.1) and (2.12)–(2.16); Appendix B, Lemma B.1, pp. 56–57: age measures, arrival age, balances, and Markov dynamics.
- [choi_kang_2014_discrete_event_simulators](sources.json), §1.1, pp. 147–148, and §2.1–§2.4, pp. 148–150: event state updates, future-event list, event routines, and next-event execution.
