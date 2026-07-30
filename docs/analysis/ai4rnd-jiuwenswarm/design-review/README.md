# Detailed-design review package

This directory is a focused review increment below the report's high-level
architecture. It opens the major system boxes and shows component contracts,
control flow, state ownership, blocking behavior, and interactions.

Start with [`diagram-review.html`](diagram-review.html). The five review plates
are:

1. `07-openjiuwen-deepagent-turn-design.svg` — JiuwenSwarm request resolution,
   OpenJiuwen agent construction, nested task/ReAct loops, Rails, services, and
   state written during a turn.
2. `08-openjiuwen-orchestration-state-design.svg` — Direct DeepAgent, Core
   Workflow/Pregel, SwarmFlow, and Dynamic Team/NativeHarness controllers,
   work units, durability, and outputs.
3. `09-ai4rnd-planning-execution-design.svg` — current AI4RnD intake, planning,
   TaskGraph readiness, Capsule/Operator binding, tmux carrier, and gate return
   path.
4. `06-capability-capsule-design.svg` — Capsule definition, Planner-facing
   partial plan, replaceable bindings, and separate lifecycle/readiness/
   assurance status axes.
5. `10-ai4rnd-evidence-data-rsi-design.svg` — evidence lineage, evaluator/gate
   authority, typed data projections, GEPA, and governed RSI.

`build_design.py` is the deterministic SVG generator. The YAML file is the
initial target Capsule template; it is a proposal, not current runtime behavior.

These diagrams are review inputs, not a replacement for source verification.
Current-state, target-state, and inferred claims should be checked against the
repositories and the 142-feature workbook before they are incorporated into the
canonical report.
