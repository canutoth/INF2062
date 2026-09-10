# Dataset Family Framing

This note aligns the dataset taxonomy with the current manuscript.

The paper should not be organized around artifact names such as
`NewRuns`, `Twins`, `workload-impact`, `LCBench`, or `Linux`. It should be
organized around **families of evidence** that each play a distinct scientific
role:

1. `REPLICATION`
2. `ENERGY`
3. `WORKLOAD`
4. `LCBENCH`
5. `LINUX`

These labels are short enough for tables and figures, but still encode what is
methodologically different across the studies.

## Short version

| Family | Intuition | Main datasets | Distinctive contribution | Main limitation |
|---|---|---|---|---|
| `REPLICATION` | Revisit published sampling studies with empirical cost instead of sample count | Kaltenecker/NewRuns corpus; x264 ICPE 2020 matrix | Closest link to prior sampling literature because published sample traces already exist | Hard to mix cost and prediction properties outside the scenarios already published |
| `ENERGY` | Change the meaning of cost itself | Twins / Green Configuration | Tests whether conclusions survive when cost is energy instead of runtime | Sampling strategies must be regenerated; not a direct replication of published sample traces |
| `WORKLOAD` | Change the context in which the same configurable system is exercised | Workload-impact ICSE 2023 | Strongest support for workload/input sensitivity inside configurable software systems | Sampling strategies must be regenerated; still a configurable-software family |
| `LCBENCH` | External validation on non-pure software systems | LCBench full lightweight archive | Shows the count-vs-cost gap survives outside pure configurable software performance corpora | Not a configurable-software system family in the SPL sense; interpretation should stay separate |
| `LINUX` | Stress-test the thesis on a very large configuration space | Linux kernel cross-version study | Unique large-space / high-feature / storage-cost stress test | Cost is essentially size/storage; generated sampling protocol is custom |

## Comparison table

| Family | Suggested subtitle | Datasets in scope | Sampling source | Cost dimension | Prediction targets | Main RQs supported | Strengths | Weaknesses / caveats |
|---|---|---|---|---|---|---|---|---|
| `REPLICATION` | Published-sampling replications | NewRuns/Kaltenecker corpus; x264 ICPE 2020 matrix | Published sample traces already exist | Mostly runtime-like empirical cost from published measurements | Published performance properties; x264 matrix also allows time vs size asymmetry | `RQ1`-`RQ4`, part of `RQ5` on x264 | Best historical continuity with the sampling literature; minimal protocol invention; strongest “same experiment, different cost model” story | Limited by what the original studies measured; less freedom to construct new cost-target combinations; x264 matrix remains one-system evidence |
| `ENERGY` | Property-cost generated-sampling experiments | Twins / Green Configuration | Sampling must be generated over measured configuration universes | Runtime and energy | Runtime and energy, naturally forming 2x2 cost/target scenarios | `RQ1`-`RQ4`, plus discussion support for `RQ5` | Introduces a genuinely different cost property; strong evidence that “cost” is not synonymous with runtime; good bridge to multi-objective reasoning | Not a published-sampling replication; generated protocol must be justified; energy is a special cost property and should not be over-generalized |
| `WORKLOAD` | Context-sensitivity generated-sampling experiments | Workload-impact ICSE 2023 | Sampling must be generated over measured configurable-system universes | Usually runtime; sometimes throughput must be oriented first | Runtime or workload-conditioned targets | Primarily `RQ5`, with useful secondary evidence for `RQ2`-`RQ4` | Best direct support for context sensitivity inside configurable software systems; many systems and many workloads; shows whether conclusions survive inside a fixed system when workload changes | Generated protocol rather than published traces; still one conceptual family of configurable-software evidence |
| `LCBENCH` | External-validation generated-sampling experiments | LCBench full lightweight archive: 35 OpenML datasets, 2000 configurations each | Sampling must be generated over measured hyperparameter-performance tables | Runtime learning-curve cost (`time_total`) | Final validation accuracy | `RQ1`-`RQ5`, especially external validation of `RQ2`-`RQ5` | Demonstrates that the mismatch between count and empirical cost survives outside pure configurable software systems; stronger and more systematic calibration/ranking effects than the configurable-software workload family | Not a pure software-system benchmark; should be presented as external validation, not pooled naively with configurable-software families |
| `LINUX` | Large-space stress test | Linux kernel cross-version study | Sampling must be generated; custom pool-based protocol | Storage size / binary size | Kernel image size and related outputs in the current study | Strong `RQ1`-`RQ4` stress test; indirect support for `RQ5` through version variation | Very large configuration space; very high-dimensional feature space; shows the thesis survives outside the small/medium-system regime | Cost is size-like rather than runtime-like; protocol differs more from the earlier corpora; interpretation should stay separate from the trace-based replications |

## Why these names work

### `REPLICATION`

This family says, immediately, what the reader should remember:
the evidence comes from the **sampling literature itself**, but replayed
with an empirical cost model.

It is the right home for:
- the multi-system Kaltenecker / NewRuns replication
- the x264 ICPE 2020 matrix

Why this is useful:
- it foregrounds continuity with the original research question
- it makes the contribution easy to state:
  “we keep the sampling study, but replace count with empirical cost”

Why not call this `AllRuns` or `NewRuns`:
- those are artifact names, not scientific categories
- a reader cannot infer the methodological role from the name

### `ENERGY`

This family is intuitive because the novelty is obvious:
**cost is no longer just runtime**.

It is the right home for:
- Twins / Green Configuration

Why this is useful:
- it isolates a different notion of cost
- it gives a simple discussion hook:
  “the same sampling question changes when cost means energy”

Why not call this `Twins`:
- `Twins` is the dataset name
- `ENERGY` tells the reader why it matters

### `WORKLOAD`

This family is intuitive because the central question is:
**does the answer change when the same configurable system is run under another workload or input?**

It is the right home for:
- Workload-impact ICSE 2023

Why this is useful:
- it is the strongest configurable-software family for `RQ5`
- it isolates workload/input sensitivity cleanly

Important nuance:
- once `LCBENCH` exists as a separate external-validation family, `WORKLOAD`
  should stay focused on configurable software systems rather than becoming a
  catch-all for every context-sensitive dataset

### `LCBENCH`

This family is intuitive because its role is explicit:
**external validation on non-pure software systems**.

It is the right home for:
- LCBench full lightweight archive

Why this is useful:
- it shows that the count-vs-empirical-cost gap is not confined to SPL-style
  configurable software corpora
- it diversifies the evidence without pretending that LCBench is “just another
  workload dataset”
- it gives the paper an out-of-domain check with real runtime metadata

Why not merge it into `WORKLOAD`:
- the scientific object is different: hyperparameter configurations over OpenML
  datasets rather than configurable software systems under varying workloads
- the contribution is not just “more workload sensitivity,” but
  **cross-domain external validation**

### `LINUX`

This family is intuitive because Linux is not just another dataset.
It is the **large-scale stress test**.

Why this is useful:
- everyone immediately understands that Linux is the “extreme case”
- it justifies keeping Linux separate from the other generated-sampling datasets

Why not merge it into `WORKLOAD`, `ENERGY`, or `LCBENCH`:
- its distinctive contribution is not workload, energy, or external validation
- it is the scale, dimensionality, and custom protocol that make it valuable

## Suggested paper narrative

A clean narrative is:

1. `REPLICATION`: does empirical cost change the conclusions of the
   published sampling literature?
2. `ENERGY`: what happens when cost itself is a different property?
3. `WORKLOAD`: what happens when workload/input changes inside a configurable
   system?
4. `LCBENCH`: does the same phenomenon survive outside pure configurable
   software systems?
5. `LINUX`: does the thesis still hold at very large scale?

This gives each family a distinct job:

| Family | Job in the paper |
|---|---|
| `REPLICATION` | Core replication argument |
| `ENERGY` | Cost-property diversification |
| `WORKLOAD` | Context-sensitivity argument inside configurable software |
| `LCBENCH` | External validation outside pure configurable software |
| `LINUX` | Large-scale stress test |

## Suggested one-line descriptions

These are short enough to reuse in figures or section intros.

- `REPLICATION`: same published sampling studies, different cost model
- `ENERGY`: same sampling question, different notion of cost
- `WORKLOAD`: same configurable system, changing workload/input context
- `LCBENCH`: same count-vs-cost question, outside pure configurable software
- `LINUX`: same thesis, extreme configuration-space scale

## Pros and cons by family

### `REPLICATION`

Pros:
- strongest continuity with the original literature
- easiest replication story to defend
- avoids accusations that the protocol was redesigned to favor the thesis
- best source for the headline “sample size is not sampling cost”

Cons:
- constrained by what the original artifacts expose
- cost-target asymmetry is not always available
- one part of the evidence remains x264-centric

### `ENERGY`

Pros:
- introduces a truly different cost semantics
- makes the paper less tied to “runtime only”
- directly strengthens the claim that cost is a modeling choice

Cons:
- requires generated sampling
- can drift toward multi-objective optimization territory if not carefully framed
- less directly comparable to ICPE-style replications

### `WORKLOAD`

Pros:
- strongest configurable-software family for `RQ5`
- easy to explain to readers
- demonstrates that local validity can differ from aggregate validity
- scales naturally from one system to many systems

Cons:
- generated sampling must be justified
- easy to blur workload sensitivity with broader external validation if the framing is not disciplined
- should no longer absorb unrelated context-sensitive datasets now that `LCBENCH` exists

### `LCBENCH`

Pros:
- genuine diversification beyond pure software systems
- still uses real runtime measurements rather than synthetic surrogate cost
- shows stronger and more systematic calibration/ranking sensitivity than the configurable-software workload family
- gives a concrete “external validation” section with real empirical weight

Cons:
- not an SPL/configurable-software benchmark in the narrow sense
- easy for reviewers to interpret as out-of-scope if the paper does not frame it explicitly as external validation
- should not dominate the main configurable-systems narrative

### `LINUX`

Pros:
- unique stress-test value
- demonstrates the thesis beyond medium-sized experimental SPL datasets
- high feature count and huge valid-configuration space make the result memorable

Cons:
- custom protocol
- cost is size/storage, not runtime
- should not be pooled casually with the other families

## Practical recommendation

If the paper uses the full current taxonomy, use exactly:

1. `REPLICATION`
2. `ENERGY`
3. `WORKLOAD`
4. `LCBENCH`
5. `LINUX`

If the paper needs formal subtitles under each short label:

| Short label | Formal subtitle |
|---|---|
| `REPLICATION` | Published-sampling replications |
| `ENERGY` | Property-cost generated-sampling experiments |
| `WORKLOAD` | Context-sensitivity generated-sampling experiments |
| `LCBENCH` | External-validation generated-sampling experiments |
| `LINUX` | Large-space stress test |

## Bottom line

This framing clarifies four things:

1. the paper now has **five** top-level families, not four;
2. `LCBENCH` deserves its own family because it is not just another workload dataset, but an external-validation step on non-pure software systems;
3. `WORKLOAD` should stay focused on configurable software systems under changing workloads/inputs;
4. the paper is easier to read when dataset names become examples inside a family, rather than the organizing principle of the whole results section.
