# Detailed-design review package

This directory is a focused review increment below the report's high-level
architecture. It opens the major system boxes and shows component contracts,
control flow, state ownership, blocking behavior, and interactions.

Start with [`diagram-review.html`](diagram-review.html). Read the target contract
plate first, then use the five subsystem plates to inspect the evidence beneath it:

1. [`11-integration-contracts-design.svg`](11-integration-contracts-design.svg) —
   the complete target round trip: ready plan slice, fail-closed binding,
   normalized common execution specification with an explicit mechanism, native attempt, typed receipt,
   evaluation/gate record, and recovery outcomes. Its normative definitions are
   in [`integration-contract-design.md`](integration-contract-design.md).
2. `07-openjiuwen-deepagent-turn-design.svg` — JiuwenSwarm request resolution,
   OpenJiuwen agent construction, nested task/ReAct loops, Rails, services, and
   state written during a turn.
3. `08-openjiuwen-orchestration-state-design.svg` — Direct DeepAgent, Core
   Workflow/Pregel, SwarmFlow, and Dynamic Team/NativeHarness controllers,
   work units, durability, and outputs.
4. `09-ai4rnd-planning-execution-design.svg` — current AI4RnD intake, planning,
   TaskGraph readiness, Capsule/Operator binding, tmux carrier, and gate return
   path.
5. `06-capability-capsule-design.svg` — Capsule definition, Planner-facing
   partial plan, replaceable bindings, and separate lifecycle/readiness/
   assurance status axes.
6. `10-ai4rnd-evidence-data-rsi-design.svg` — evidence lineage, evaluator/gate
   authority, typed data projections, GEPA, and governed RSI.

`build_design.py` is the deterministic SVG generator. The YAML file is the
initial target Capsule template; it is a proposal, not current runtime behavior.
The adversarial findings and their disposition are recorded in
[`adversarial-review.md`](adversarial-review.md).

These diagrams are review inputs, not a replacement for source verification.
Current-state, target-state, and inferred claims should be checked against the
repositories and the 142-feature workbook before they are incorporated into the
canonical report.
