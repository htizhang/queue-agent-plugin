# Congestion-priced lookahead with a closing cost

This is an agent-discovered exploratory policy, not peer-reviewed queueing
knowledge. It is included as an opt-in research lead. Its archived evidence
applies only to the configurations and comparators described in
[the evaluation note](evaluation/README.md).

## Problem boundary

The policy was designed for an open multiclass reentrant network. Product class
\(c\) has probability \(q_c\) and a fixed route

\[
\mathcal R_c=((s_{c1},p_{c1},r_{c1}),\ldots,(s_{cL_c},p_{cL_c},r_{cL_c})),
\]

where \(s_{c\ell}\) is a station, \(p_{c\ell}\) is the mean service time, and
\(r_{c\ell}\) is the recipe used at the setup-sensitive station. Stations may
be revisited. One bottleneck station has one server, a persistent current
recipe, and deterministic sequence-dependent setup times \(S_{rr'}\). Other
stations have no setup state and may have parallel servers.

Service and setup are nonpreemptive. Whenever a server is free and its queue is
nonempty, the policy selects one waiting job. It cannot idle deliberately,
reject jobs, preempt work, or request a batch. The surrounding simulator or
system performs the setup and service.

For a fixed scored cohort \(\mathcal J\), the objective is mean whole-network
flow time,

\[
\overline F=\frac{1}{|\mathcal J|}\sum_{j\in\mathcal J}(d_j-a_j).
\]

### Observations

At a decision, the policy uses:

- the current time, queues, station capacities, and bottleneck recipe;
- each waiting job's class, route position, station-arrival time, expected
  current service, expected remaining route work, and required recipe;
- class probabilities, routes, service means, and the complete setup matrix;
- its own previous bottleneck dispatches.

It does not use future arrivals, realized unfinished service requirements,
scheduled completion times, workload identifiers, or randomness identifiers.
A fresh policy instance is required for each independent replication.

## Decision rule

For a job \(j\) waiting at station \(s\), let

\[
W_j^{(s)}
=\sum_{\substack{\ell\text{ remaining}\\s_{c_j\ell}=s}}p_{c_j\ell},
\qquad
w_j=W_j^{(s)}+0.10\left(R_j-W_j^{(s)}\right),
\]

where \(R_j\) is all remaining mean route work. Thus \(W_j^{(s)}\) includes the
current operation and later returns to the same station. At a setup-free
station, select the smallest tuple
\((w_j,\text{station arrival}_j,\text{id}_j)\).

At the bottleneck, first compute a congestion multiplier. Let \(u\) be the
class-mixture-weighted mean duration of a bottleneck visit, counting repeat
visits. Initialize virtual busy work \(B=40u\), virtual span \(D=50u\), and no
virtual finish time. Before a dispatch,

\[
\widehat\rho=B/D,\qquad
\beta=
\begin{cases}
32,&\widehat\rho\ge 1,\\
\min\{32,\max\{1,(1-\widehat\rho)^{-1}\}\},&\widehat\rho<1.
\end{cases}
\]

This is a virtual-work occupancy proxy, not measured utilization.

Partition the waiting queue by recipe. Keep at most three jobs per recipe,
ordered by \((w_j,\text{station arrival}_j,\text{id}_j)\). From this shortlist,
enumerate every ordered sequence of distinct jobs of length

\[
h=\min\{3,\text{shortlist size}\}.
\]

For a sequence \(\sigma=(j_1,\ldots,j_h)\), current recipe \(r_0\), and
\(r_k=r_{j_k}\), define

\[
C_0=0,\qquad
C_k=C_{k-1}+w_{j_k}+\beta S_{r_{k-1},r_k}.
\]

If \(Q\) is the full queue and \(N=|Q|\), score the sequence by

\[
J(\sigma)=
\sum_{k=1}^{h}C_k
+(N-h)C_h
+\beta\sum_{j\in Q\setminus\sigma}S_{r_h,r_j}.
\]

The first term rewards early progress in the selected sequence. The second
charges the planned duration to every job left waiting. The closing term prices
one outgoing setup from the sequence's final recipe for each unselected job,
using the residual queue's actual recipe composition. It is a continuation
surrogate, not an exact value function. Symmetry or balanced recipe counts alone
do not make this term zero.

Choose the sequence minimizing
\((J,\text{first-job station arrival},\text{first-job id})\), start only its
first job, and replan at the next dispatch. If the bottleneck has no current
recipe, select the smallest \(w_j\); a singleton queue has a forced choice.

After selecting bottleneck job \(j\) at time \(t\), let

\[
x=S_{r_0,r_j}+p_j.
\]

On the first update, set \(v=t+x\) and add \(x\) to both \(B\) and \(D\). On
later updates,

\[
v'=\max\{t,v\}+x,\qquad
B\leftarrow B+x,\qquad
D\leftarrow D+(v'-v),\qquad
v\leftarrow v'.
\]

The current decision always uses the tracker before this update.

### Frozen settings

The migrated policy fixes search depth and per-recipe shortlist size at 3,
closing weight and left-queue weight at 1, other-station work weight at 0.10,
sequence discount at 1, and the setup multiplier to the clipped inverse-slack
formula above. These are the settings evaluated in the archived report.

## Portable implementation

[implementation/policy.py](implementation/policy.py) preserves the archived
mapping-based callback:

```python
from policy import make_policy

choose = make_policy()             # create once per independent replication
job_id = choose(state, station_id) # return one waiting job identifier
```

The state must provide:

- `now`, `bottleneck`, and the square `setup` mapping;
- `stations[station_id]` with `servers` and `recipe`;
- `products[product]` with `probability` and a remaining-readable `route`;
- `queues[station_id]`, whose jobs contain `id`, `product`, `operation`,
  `station_arrival`, `expected_current`, `expected_remaining`, `recipe`, and
  the immediate `setup_cost`.

`expected_remaining` includes the current operation. Each route operation
contains `station` and `mean_service`. The policy returns an identifier only;
queue mutation, setup execution, and service remain the evaluator's
responsibility.

Run the dependency-free fixture from the repository root:

```text
python3 discovery-lab/congestion-priced-lookahead/implementation/smoke_test.py
```

## Relationship to published methods

The ingredients have substantial precedent. Setup-aware priority rules trade
processing and changeover costs, including the rules summarized by
[Xanthopoulos et al. (2016)](https://doi.org/10.5267/j.ijiec.2016.2.002).
[Tran et al. (2013)](https://doi.org/10.1609/icaps.v23i1.13552) combine
queueing guidance with short-horizon scheduling under sequence-dependent
setups. Terminal penalties for rolling schedules also predate this work; see
[Wang, Xi, and Gu (2005)](https://doi.org/10.1016/j.cor.2004.11.004).

The exploratory contribution is the particular executable composition of
remaining-station work, a virtual-work congestion price on setups, job-level
depth-three sequence search, and a residual-queue outgoing-setup closing cost.
A bounded internal prior-art review found no substantively identical complete
rule, but that search does not establish universal novelty.

## Applicability and limits

This policy is most relevant when a persistent recipe state, material
changeover times, and repeated visits make myopic processing-time rules
shortsighted. It reads the numerical setup matrix directly; recipe-family
labels are unnecessary.

Evaluate it anew before use with multiple setup-sensitive servers, interruptible
setups, batching, deliberate idling, due-date objectives, finite buffers, or a
different information boundary. The archived study used 4--6 recipes and at
most 18 shortlisted jobs, so each bottleneck decision considered at most
\(18\cdot17\cdot16=4{,}896\) sequences. Runtime grows cubically with the number
of shortlisted jobs at the fixed depth.

The 0.10 other-station weight was retained for fidelity even though its archived
ablation did not support a benefit. Previous performance therefore remains a
lead to test, not a recommendation for a new setting.

## Frozen provenance

The portable code is a focused extraction of the archived candidate
`shadow_close_v1.py`, instantiated with `close=1.0` and
`close_basis="rest"`; its SHA-256 is
`36f4e9194591a6ec20cd737606586560e5d1c511225090225c75085a70efa738`.
The evaluated family generator `masksets.py` has SHA-256
`94732ffa0062cacda24732da559bb922eb820422ca3d83ea0ab2fc43c793534d`.
The archived analysis payload has SHA-256
`78036a75ce910ea261c922c490c26ce572dc6214315b04bdb3c99ee43127b625`.
Large campaign artifacts are not bundled with this entry.
