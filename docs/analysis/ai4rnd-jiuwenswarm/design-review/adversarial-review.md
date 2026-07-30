# Adversarial review — detailed-design package at 4b452f2

Reviewed artifacts: `design-review/README.md`, `design-review/diagram-review.html`,
plates `06`–`10` (rendered and visually inspected at natural size, 1440 px and 390 px
viewports, zero horizontal overflow, zero console errors), `design-review/build_design.py`
(all ten generators read in full), `design-review/capability-capsule.to-be.template.yaml`
(read in full, field by field).

Verification baselines: JiuwenSwarm source checkout (`jw-src`, a98d7ad), installed
`openjiuwen 0.1.15.post3` package, AI4Research checkout at d35c511, the 142-feature
workbook and the 142-row ownership matrix (`tools/ownership_data.py`), and the executed
probe evidence from earlier passes (probe_r1–r4, guardrail loader probe, capsule census).
Every count in this review was re-derived from source during this review, not carried
forward from prior documents.

Severity scheme: **BLOCKER** (must fix before the package can be presented or relied on),
**MAJOR** (materially wrong or missing; fix before design sign-off), **MINOR** (real but
low-consequence), **STYLE** (presentation only).

---

## 1. Overall verdict

The package is substantially accurate and unusually honest for a design deck. Its
strongest claims survive adversarial source verification: the DeepAgent turn plate's Rail
envelope matches the openjiuwen callback enum exactly (including the subtle after-only
ReAct hook), the construction chain names real classes, the four orchestration rows'
control/work-unit/durability/returns cells are each correct, and the AI4RnD control plate
is faithful to `graph_scheduler.py`/`graph_node_dispatcher.py` down to the
`no_matching_worker` string and the send-keys-then-Enter carrier it explicitly rejects.

It is not presentable as-is. The one line on plate 06 that is explicitly labeled
"Current source" — the capsule inventory — is wrong in three of its five numbers
(BLOCKER). Several behaviors that this analysis previously verified by execution and that
directly affect the design's safety claims (SwarmFlow's success-despite-step-failure,
the allocator's silent model fallback, the guardrail loader that loads zero rules in the
JiuwenSwarm layout) are absent from the plates, and one of them directly contradicts a
binding requirement printed on plate 06 ("Model: exact pool entry, no silent fallback").
The Capsule v2 template is a good proposal with four genuine migration defects, one of
which (dropping the id-level operator deny-list) is a safety regression.

## 2. Blockers

**B-1 (BLOCKER). Plate 06's "Current source" inventory line is factually wrong.**
Plate 06 invariant strip (generated at `build_design.py:267`) states: "Current source: 41
unique manifests; all carry 11 v1 sections. Registry: 34 entries (30 stable, 4 draft),
with 7 manifests unregistered." Recounted from source at d35c511:

- **42** unique manifests, not 41: 19 files in `harness/capability-capsules/` + 23 in
  `harness/config/capability-capsules/`, zero duplicate `capability_capsule_id`s across
  the two directories.
- Registry `harness/config/capability-capsules.registry.yaml`: **35** entries, not 34
  (32 `capability` + 1 `guard` + 2 `resource`); statuses **30 stable, 5 draft**, not
  30/4. The five drafts are the five `cap.understand-anything-*` capsules — the plate's
  count pattern (−1 manifest, −1 entry, −1 draft) is consistent with one of these five
  having been missed.
- "All carry 11 v1 sections" is **correct**: the intersection of top-level keys across
  all 42 manifests is exactly `{capability_capsule_id, capsule_kind, metadata,
  applicability, contract, composition, effects, bindings, verification,
  operator_compatibility, provenance}`. (23 manifests additionally carry `version`; 6
  carry `runtime_preferences` — see C-6.)
- "7 manifests unregistered" is **correct**: `adapter.artifact-type-bridge`,
  `adapter.patch-diff-to-verification-pack`, `adapter.requirement-ir-to-design-brief`,
  `cap.chatgpt-browser-agent`, `cap.gemini-enhanced-search`, `cap.notebooklm-enrichment`,
  `cap.skill-execution-bridge` (all in `harness/config/capability-capsules/`). All 35
  registry `manifest_path` values resolve to real files; there are no ghost entries.

The same stale "41 manifests; 34 registered" also appears in the plate-01 generator at
`build_design.py:126` (that plate is not part of the committed 06–10 set, but the
generator will reproduce the error if rerun).

**B-2 (BLOCKER). A "Current source"-labeled line must not be wrong anywhere in a package
whose stated purpose is review-grade traceability.** This is the same defect class the
whole analysis exists to prevent (labels asserted without re-verification). Fixing B-1
is a one-line change per site plus regeneration; until then the package fails its own
standard and section 16 below is conditional on it.

No other finding rises to blocker.

## 3. Major inaccuracies

**M-1 (MAJOR). Plate 06 §3 "Model: exact pool entry, no silent fallback" contradicts
verified current runtime behavior without saying so.** `resolve_member_model`
(`openjiuwen/agent_teams/models/allocator.py:387–423`) returns `None` when a member's
pool group is missing and the caller proceeds on the default model — a silent fallback,
verified by execution in the earlier team-services audit. As a *target requirement* the
plate's text is fine; presented inside "Replaceable execution bindings" with no
current/target marker it reads as a property of the binding layer. It must be marked as
a **fix-before-reuse** obligation on the allocator (or an AI4RnD-side wrapper that fails
closed), or the diagram claims a guarantee the runtime does not give.

**M-2 (MAJOR). Plate 06's "Planner blueprint" and the v2 YAML template disagree about
what a blueprint step references.** Plate 06 §1 says the blueprint lists "required and
optional Logical Operators"; the template's `planning_blueprint.steps[*]` carry
`skill_refs`, `tool_requirements`, `mcp_requirements`, `consumes`/`produces` — and no
logical-operator reference at all. In AI4RnD vocabulary the Logical Operator is the
typed action identity (`harness/config/logical-operators.json`; plate 09-C uses it
correctly), so these are two different contracts: steps-as-operator-instantiations
versus steps-as-skill-bundles. The package's two normative artifacts must agree; either
add `logical_operator_ref` to the step schema or reword plate 06.

**M-3 (MAJOR). The v2 template drops the id-level operator deny-list.** v1
`operator_compatibility.forbidden` is enforced today at
`capability_capsules.py:1286–1287` (`operator_id in set(operator_compat.get("forbidden"))`
→ `CapsuleResolutionError("operator_incompatible: …")`). v2 replaces it with kind-level
`forbidden_operator_kinds` and justifies removal of ids via `forbid_identity_pinning`.
Deny-by-id is not pinning — it is a deny-list, a safety control (e.g. "this browser
operator may never run the secret-handling capsule"). Kind-level granularity cannot
express it. Restore an id-level `forbidden_operators` field (deny only; allow-lists
remain kind/capability-based).

**M-4 (MAJOR). The v2 proposal conflicts with the current registry on day one.** Every
current registry entry carries `default_operator_profile` (e.g.
`mini-claude-sonnet-builder-2`) — an identity-pinned executor default that the resolver
returns today (`capability_capsules.py:1333` area, `operator_constraints.default_operator_profile`).
v2 declares `forbid_identity_pinning: true` and "model_requirements: capabilities/
constraints, not model IDs" but says nothing about migrating or retiring
`default_operator_profile`. Without an explicit migration rule (move defaults into the
Physical Operator registry keyed by capability, or delete them), every migrated capsule
violates the new invariant immediately.

**M-5 (MAJOR). The secrets-require-guard invariant is silently lost in v2.** The current
semantic validator (`capability_capsules.py:636–641`) rejects any manifest whose
`bindings.secret_refs` is non-empty without a `guard.*` reference, and the resolver
enforces it again at runtime (`capability_capsules.py:1302–1303`,
`policy_blocked: secret_refs without guard capsule`). v2 moves `secret_refs` to
`resources.secret_refs` and guard references to `composition.required_guard_capsules`
but states no secret→guard rule anywhere in the template. The invariant must be restated
in v2 (and the JSON schema + `validate_capability_capsule_semantics` updated), or the
strongest governance rule in the current capsule system disappears in migration.

**M-6 (MAJOR). Plate 10-A is target-state presented in current-state voice.** Subtitle:
"Evidence records preserve original content identity and exact support spans." The
harness evidence ledger (`harness/lib/evidence_ledger.py`, 117 LOC) stores scheduler
run entries with **no** content hashes, spans, or claim links. The described chain does
exist — but only in the research pipeline's SQLite schema
(`harness/lib/research/migrations/001_init.sql`: `research_sources.content_hash`,
`evidence_items.span_start/span_end/content_hash`, `claims`, `claim_evidence`), which is
not wired to the harness ledgers or the gate ledger. The plate needs a current/target
badge and a pointer to the actual substrate; small label errors compound the impression
of currency (see MI-3).

## 4. Important omissions

**O-1 (MAJOR). SwarmFlow's verified failure semantics are absent from plate 08.**
Executed probe (probe_r2): a step that fails after `rt.retries+1` attempts yields
`agent() → None` and the run **reports success**; the journal replays the `None`.
Plate 08's SwarmFlow row lists durability "journal/WAL + progress events" and returns
"script return · phase/run events" with no mention that a successful return can embed
silent step failures. Any AI4RnD adapter must treat `None` results as failed attempts;
this is exactly the class of "verified gap" the design must carry forward.

**O-2 (MAJOR). The guardrail loader gap is absent.** Executed probe: openjiuwen's tiered
policy loader (`openjiuwen/harness/security/tiered_policy.py`) resolves builtin rules
from the package path only; JiuwenSwarm writes `resources/builtin_rules.yaml`
(`jiuwenswarm/common/utils.py`, `init_workspace.py`) that nothing reads — **zero rules
load** in the deployed layout. Plate 07-E presents "Permission engine: allow · ask ·
deny" as a working shared service. The ALLOW/ASK/DENY enum is real
(`openjiuwen/harness/security/models.py:19–28`), but the deployed-rules gap is a
fix-before-reuse item and belongs on the plate or its caption.

**O-3 (MINOR). `AFTER_REACT_ITERATION` fires only on fully successful iterations** —
"Only fires on fully successful iterations, not on any break path"
(`openjiuwen/core/single_agent/rail/base.py:200–202`; fire site
`core/single_agent/agents/react_agent.py:1818`). Plate 07-D's "ReAct iteration: after"
is correct but Rails that meter or audit iterations will undercount unless this nuance
is stated.

**O-4 (MINOR). Core Workflow's zero-argument router constraint is absent.** Verified by
probe_r4: `add_conditional_connection(src, router)` invokes the router with **no
arguments** (`Router = Callable[..., Hashable | list[Hashable]]`), so routing state must
travel out-of-band. This constrains how an AI4RnD adapter expresses conditional DAG
slices and belongs in plate 08's Core Workflow row.

**O-5 (MINOR). The layer above mechanism choice is missing.** Plate 08's "Mechanism
selector: agent · workflow · flow · team" omits the session/intent controller
(`openjiuwen/core/controller/schema/intent.py`: `CREATE_TASK`/`PAUSE_TASK`/`RESUME_TASK`)
and JiuwenSwarm's cron/proactive triggers (`jiuwenswarm/gateway/cron`,
`server/runtime/proactive_adapter.py`) that decide *when* a mechanism is invoked at all.

**O-6 (MINOR). SwarmFlow resume is engine-API-only.** `SwarmflowTool` rejects
`resume_id`/`name` ("not supported yet", probe_r1); resume/journal replay works through
`run_workflow(..., resume=…)` only. Plate 08's durability cell implies resumability
without noting the tool-surface restriction.

## 5. Architecture-versus-design assessment

The package keeps the architecture decision (compose AI4RnD's semantic plane over
OpenJiuwen's execution plane; retire the tmux carrier) and descends into design detail
without re-arguing it — appropriate, since the corrective passes settled the decision
with the preservation gate. Where the package takes design positions, they are
consistent with the verified constraints:

- **Compilation boundary** (plate 08 caption: "compile a ready semantic slice into one
  mechanism; persist the mapping between project node/attempt and the mechanism's native
  run/checkpoint identifiers") — correct and necessary, and consistent with the verified
  journal keying (`{team}/sessions/{session_id}/workflows/{name}`) and checkpointer
  behavior. This is the single most load-bearing design rule in the package and it
  survives scrutiny.
- **Four-mechanism decomposition** — defensible. The four rows are exactly the four
  schedulers with distinct durability models in the installed package. The decomposition
  is challenged in two ways only: (a) sub-agent delegation inside a DeepAgent turn is an
  orchestration path of its own (plate 07 step 6 lists sub-agents as abilities, so it is
  implicitly mechanism 1, acceptable); (b) the intent/controller layer and scheduled
  triggers sit above all four and are absent (O-5). Neither breaks the four-way split;
  both should be named in the caption.
- **Separation of semantic completion from execution success** (plate 07-F caption,
  plate 09-E, plate 10-B "five separate decisions") — matches the verified failure modes
  that motivated it (SwarmFlow success-despite-failure, run-report semantics), even
  though plate 08 fails to show the motivating evidence (O-1).
- The design's honesty gradient is inverted in one place: the plate that most needed
  current/target badges (10) has none, while the plate least in doubt (09) carries the
  clearest marking ("rejected for the target").

## 6. Diagram-by-diagram findings

**Plate 06 — Capability Capsule.** BLOCKER B-1 (invariant strip numbers). MAJOR M-1
("no silent fallback" vs allocator behavior), M-2 (blueprint unit vs YAML). The
house-plan caption is fair but understates novelty: v1 capsules contribute **no plan
structure at all** today — there is no steps/blueprint field in any of the 42 manifests,
and `expand_logical_workflow` (`capability_capsules.py:813`) expands taxonomy templates
selected by `primary_class`, not capsule content. "Planning contribution" is a new
capability, not a refinement of an existing one; the plate should say so. Section 4's
three status axes are well-argued and the "do not compress … into one 'stable' flag"
subtitle is exactly right against the current single `status` field. Renders cleanly;
no overflow; readable.

**Plate 07 — OpenJiuwen DeepAgent turn.** The strongest plate; verified nearly line by
line. Confirmed exact: Rail envelope (11 events of `AgentCallbackEvent`,
`core/single_agent/rail/base.py:214–224` — invocation before/after, task iteration
before/after, ReAct **after only**, model before/after/exception, tool
before/after/exception; the `AgentRail` ABC at `base.py:456` exposes precisely these
overridables); construction chain (`DeepAgentSpec` at
`agent_teams/schema/deep_agent_spec.py:427` with `.build(context)` at `:561` and
`resolve_parts(context)` at `:479`; `BuildContext` at
`agent_teams/schema/build_context.py:27` with `derive()` and `build_context_from_seed`
for cross-process rebuild — matching the plate's "cross-process rebuild seed";
`DeepAgentConfig` at `harness/schema/config.py:163`; `DeepAgent` in
`harness/deep_agent.py`); permission enum (`harness/security/models.py:26–28`);
SysOperation and the auto-prepended `SysOperationRail` (`harness/factory.py:119–120`);
request resolution chain matches JiuwenSwarm layout (`gateway/app_gateway.py`,
`channel_manager`, `message_handler`; `server/app_agentserver.py`;
`server/runtime/agent_manager.py`). Defects: MINOR — step 6 draws permission checking
as a stage *after* "before-tool Rails," but enforcement itself lives in a before-tool
rail (`harness/rails/security/tool_security_rail.py` calling
`harness/security/core.py:145 check_permission`); O-2 (deployed guardrails load zero
rules) and O-3 (success-only ReAct hook) unstated. The closing integration note
("never treat a final message or checkpoint as a scientific verdict") is correct and
important.

**Plate 08 — Orchestration and state.** All sixteen mechanism cells verified correct
against source and prior probes. Defects are omissions, not errors: O-1 (silent step
failure — the most important), O-4 (zero-arg router), O-5 (intent layer), O-6
(tool-surface resume). "Dynamic Team / NativeHarness" as one row is acceptable
(NativeHarness is the runtime of dynamic teams), but the row could note TeamRole
includes `HUMAN_AGENT`/`BRIDGE_AGENT` — directly relevant to AI4RnD's HITL features.
Renders cleanly.

**Plate 09 — AI4RnD planning/binding/execution.** Faithful to source to an unusual
degree: `no_matching_worker` literal at `graph_scheduler.py:2386`; PM/产品经理 ·
Planner/规划者 · Builder/建设者 · Evaluator/审判官 role machine in
`graph_node_dispatcher.py` (e.g. `:7104`, `:7180`); tmux carrier exactly as drawn —
`send-keys` at `graph_node_dispatcher.py:7580/7605/7825/7948` with separate `Enter` at
`:7958`, busy-marker pane classification (`graph_scheduler.py:1937–1938`,
`_workers_with_used_panes_marked_busy` at `:2422`), mtime reconciliation
(`graph_node_dispatcher.py:3416–3433`); quarantine exists (`graph_scheduler.py:2724`);
capsule admission-before-scoring matches the resolver order in
`resolve_capability_capsule_for_task` (`capability_capsules.py:1281–1331`: precondition
admission → operator compatibility → attach guards → attach resources → policy checks →
bindings → verifier hooks); Physical Operator registry is real and consumed
(`harness/config/physical-operators.json`; `actor_registry.py:20/279/322`,
`apo_plan_compiler.py:35`). The red "rejected for the target" band is the best
current-versus-target treatment in the package. One caution (MINOR): section C reads as
a uniformly live pipeline; the capsule loader/stage-expansion path is only partially
wired into live dispatch (capsule-backed nodes exist and can strand as
`no_matching_worker` — the comment at `graph_scheduler.py:2253` documents exactly this —
but the end-to-end capsule→stages→verifier flow is not exercised by every run). A
per-box wiring badge would resolve it.

**Plate 10 — Evidence, data and RSI.** MAJOR M-6 (current-state voice). Verified
correct: gate ledger semantics ("append-only, writer-attributed verdicts; node status is
a projection; corrections supersede rather than edit history" — `gate_ledger.py:1–27`,
`append_record` at `:110` with `writer`/`author` fields and `AUTHOR_TYPES` validation,
`project_node_status` at `:212`); the five-decision separation in section B is a sound
reading of `record_status_transition`/verdict kinds plus the contract/verification gates
(`contract_gate_executor.py`, `verification_gate.py`); GEPA maturity caption ("GEPA
text-artifact path is implemented/tested but isolated") matches the source audit
(~3,540 LOC under `harness/integrations/gepa_optimizer/` with unit tests, wired to
nothing in the dispatch path). Label defects (MINOR): claim-link vocabulary
"supports · refutes · contextual" — the schema says `supports/refutes/qualifies`
(`claim_evidence.chk_relation`, `001_init.sql:113`) and `supports/refutes/neutral`
(`claims.chk_stance`); "char+byte offsets" — the schema has a single
`span_start`/`span_end` integer pair, not dual char+byte offsets; "metric protocol +
raw result" has no schema counterpart. "Capsule/operator and data/benchmark on-ramps
are partial": `CandidateType` (`gepa_optimizer/candidate_schema.py:23–30`) is
`SKILL/CAPSULE/ROUTING_POLICY/REWRITE_RULES/COST_MODEL` — CAPSULE exists as a schema
on-ramp, but there is **no** data/benchmark candidate type; "partial" is generous for
that surface (MINOR). Section C's "one event/artifact truth" needs a target badge: the
current state is at least four disjoint stores (research SQLite, gate ledger JSONL,
evidence ledger JSONL, GEPA ArtifactStore).

**diagram-review.html + README.** Sound framing; the README's "review inputs, not a
replacement for source verification" and "the YAML is a proposal, not current runtime
behavior" disclaimers are exactly right (and partially rescue M-6 at package level,
though not at plate level where readers land). Rendering: all five `<img>`s load at
natural size 1100×(1480–1780), no console errors, no horizontal overflow at 1440/390.
STYLE: the plates hard-code light-theme colors (own `COLORS` dict in
`build_design.py`), so they will not adapt if the shell ever gains the site's dark
mode; the main site's diagrams use CSS variables — acceptable divergence for a review
package, worth aligning later. STYLE: no solid/dashed legend on plates 07/09 although
dashed feedback/loop edges are used.

## 7. Capability Capsule findings

Corrected inventory (see B-1): **42 manifests · 11 universal v1 sections · 35 registry
entries · 30 stable + 5 draft · 7 unregistered · 0 ghost entries · all manifest_paths
resolve.**

On the proposed v2 template, field by field:

- `schema_version` / `capability_capsule_id` / `capsule_kind` / `version`: sound. MINOR:
  the id pattern comment `cap.<domain>-<capability>` contradicts the kind enum — the
  existing corpus uses `guard.*`/`resource.*`/`adapter.*` prefixes for non-capability
  kinds. State the prefix rule per kind. MINOR: 19 of 42 current manifests lack
  `version`; migration needs a backfill rule (registry entries do carry versions).
- `portability`: the design rule "reusable across projects, agents and teams" is the
  right target, but `scope: universal` as the only sanctioned value contradicts the
  existing corpus — the five `understand-anything-*` drafts and
  `cap.flashmlx-performance-debugger` are product- or project-specific. Either admit a
  `project` scope or the migration must reclassify/retire those capsules explicitly
  (MINOR, but it decides the fate of 6+ real manifests).
- `applicability` / `contract` / `composition`: faithful upgrades of v1. Good: schema
  refs on inputs/outputs, `requires_before/after`, explicit guard/resource capsule
  references. MAJOR M-5 applies here: no secret→guard invariant stated.
- `planning_blueprint`: the centerpiece and entirely new (no v1 counterpart; current
  expansion is taxonomy-template-based, `capability_capsules.py:813`). Internally
  coherent (steps, `depends_on`, `ordering_constraints`, `completion_checks`;
  capability-not-instance `tool_requirements`/`mcp_requirements`). MAJOR M-2: step unit
  disagrees with plate 06. MINOR: `planner_policy.may_relax_contract: false` is stated
  but no enforcement point is designated (who checks the planner's output against the
  blueprint — the capsule loader, the plan validator, or the gate?). MINOR: the section
  is meaningless for `guard`/`resource` kinds; mark kind-conditional sections.
- `effects`: good; `budget_class` + `hard_limit_ref` policy indirection is right.
- `executor_policy`: `fail_closed | require_human` matches the honest-stall behavior the
  scheduler already exhibits (`no_matching_worker`, `admission_failed:*`,
  `policy_blocked:*` — all real strings in `capability_capsules.py`). MAJOR M-3
  (deny-list dropped) and M-4 (`default_operator_profile` conflict) apply.
  `separation_of_duties.writer_may_verify: false` matches the evaluator independence
  already enforced in dispatch (builder/evaluator pane separation,
  `graph_node_dispatcher.py:7167ff`). Good field: `pin_binding_for_attempt` — pin per
  attempt, never per capsule — this is the correct resolution of the pinning tension.
- `resources`: reasonable successor to v1 `bindings`. MINOR: v1's `runtime_preferences`
  (present in 6 manifests) has no v2 destination — map into
  `executor_policy.model_requirements`/`permitted_operator_kinds` or declare it dropped.
- `verification`: keeps v1's strengths, adds `evidence_requirements` (receipt,
  execution receipt, provenance, evaluation record) — aligned with plate 09-E and the
  gate ledger's actual record kinds.
- `registry_status` / `runtime_status` / `assurance_status`: the three-axis split is the
  best idea in the template and directly repairs the current conflation (a "stable"
  registry status today means only "definition maturity" while nothing tracks runtime or
  assurance — the census confirms no runtime/assurance fields exist anywhere in v1).
  MINOR (acknowledged in the template's own comments): `runtime_status` is mutable
  operational state and does not belong in a versioned manifest file; keep the field
  *contract* here but store values in the control plane keyed by (capsule id, version).
- `lifecycle` / `history_refs` / `evolution`: target-only (no current implementation of
  the ledger URIs or promotion/rollback policies for capsules); consistent with the GEPA
  Promoter design (`gepa_optimizer` Promoter with sha256 sidecars and rollback);
  `promotion_requires_human: true` matches plate 10-D. Fine as proposal; label as such.

On the "agents are bindings, not the capability" claim (plate 06 §3, HTML §4): correct
and consistent with both v1 (`operator_compatibility` + registry
`default_operator_profile` as the only executor coupling) and the resolver, which
returns operator *constraints* rather than an operator identity. The claim survives
adversarial reading with the M-3/M-4 caveats above.

## 8. OpenJiuwen component findings

Classification per the six-status vocabulary, from source and executed probes:

- **DeepAgent turn machinery** (spec/build/config, task loop + ReAct, Rails, permission
  engine, SysOperation, skills, memory, workspace): **active-wired** in the installed
  package; every plate-07 claim checked resolved to a real class/enum/call site (§6).
- **Rail hook surface**: active-wired; exactly the 11 events; no before-ReAct hook
  exists, so any AI4RnD per-iteration *pre*-checks must ride `BEFORE_MODEL_CALL`.
- **Permission engine**: implemented and wired in openjiuwen (`ToolSecurityRail`);
  **deployed-config gap** in JiuwenSwarm (zero rules load; orphaned
  `resources/builtin_rules.yaml`) — fix-before-reuse (O-2).
- **Core Workflow/Pregel**: active-wired; checkpointer snapshots verified by probe;
  zero-arg router constraint (O-4).
- **SwarmFlow**: active-wired with two sharp edges — success-despite-step-failure (O-1)
  and tool-surface resume rejection (O-6); `ConcurrencyGovernor` is a hard precondition
  (probe: engine refuses to run without it).
- **Dynamic Team/NativeHarness**: active-wired; task board with real dependency edges
  (`tools/tool_task.py`: `depends_on`, `add_blocked_by`,
  `task_manager.add_dependencies`); reliability detectors + remediation present.
- **Model pool/allocator**: active-wired with the silent-fallback defect (M-1) —
  fix-before-reuse.
- **agent_evolving**: implemented-unwired for AI4RnD purposes; `Trainer` requires
  `get_operators()`, whose sole implementor is
  `core/single_agent/agents/react_agent_evolve.py`; "Operator is NOT an executable unit"
  (`core/operator/base.py`); JiuwenSwarm imports only EvolutionStore/experience/
  tool-description parts. It does **not** replace any GEPA governance component
  (frozen-policy checking, isolated evaluation, promotion/rollback); overlap is limited
  to prompt-artifact candidate generation.

## 9. AI4RnD component findings

- **Graph scheduler + node dispatcher** (`graph_scheduler.py` 4,189 LOC;
  `graph_node_dispatcher.py` ~7,900 LOC): active-wired, including capability admission,
  `no_matching_worker` stall, quarantine, batch safety. The tmux carrier inside the
  dispatcher is active-wired and correctly marked reject-retire by plate 09-D.
- **Capsule system** (`capability_capsules.py` 1,351 LOC + registry + gates): partial —
  loader/validator/resolver implemented with real enforcement (admission, guard
  attachment, secrets rule, operator deny-list); wiring into live dispatch exists for
  capsule-backed nodes but the full capsule→stage→verifier expansion is not the default
  path of every run (`graph_scheduler.py:2151, 2253` document the seams).
- **Gate ledger** (`gate_ledger.py`, 372 LOC): active-wired; append-only,
  writer-attributed, projection-based status — exactly as plate 10-B claims. Note its
  deliberate best-effort contract ("gate evidence must never break the dispatch hot
  path" — failures return `None`): worth stating in the design, since evidence loss is
  silent by design at this layer.
- **Evidence ledger** (`evidence_ledger.py`, 117 LOC): active-wired but minimal
  (scheduler decisions; no hashes/spans/claims) — the plate-10-A chain is **target-only**
  at harness level (M-6).
- **Research pipeline store** (`research/storage.py` + `001_init.sql`): implemented;
  sources→evidence(spans, hashes)→claims→claim_evidence with CHECK constraints; the
  only current substrate matching plate 10-A; not integrated with harness ledgers.
- **GEPA** (`harness/integrations/gepa_optimizer/`, ~3,540 LOC + unit tests):
  implemented-unwired (tested in isolation; CLI dry-run default; Promoter with sha256
  sidecars and rollback; `hard_policy_checker` frozen-section diff; Budget + five
  stopper types). Plate 10-D's loop is a faithful rendering of this code plus a governed
  wrapper that does not yet exist.
- **Physical/Logical operator registries** (`physical-operators.json`,
  `logical-operators.json`, `actor_registry.py`): active-wired.
- **Coordinator roles** (PM/Planner/Builder/Evaluator): active-wired in dispatcher
  title/role classification and evaluator-independence rules.

No component in plates 06–10 is drawn as current while being absent from source; the
two currency problems found are voice/badging (M-6) and the partial capsule wiring
nuance (plate 09-C), not phantom components.

## 10. Compatibility and reuse implications

Reconciled with the 142-row ownership matrix (BUILD 50 / ADAPT 35 / REUSE 23 / PORT 20 /
EXTEND 11 / DEFER 2 / UNRESOLVED 1) — the package's implicit consequences are compatible
with the matrix; per component:

- **DeepAgent runtime, Core Workflow, Dynamic Team**: reuse-unchanged behind the
  compilation boundary; plate 08's design rule (persist node/attempt ↔ native-run-id
  mapping) is the right adapter obligation.
- **SwarmFlow**: compose-adapter **with a result-validation wrapper** that converts
  `None` step results into failed attempts before any receipt is issued (O-1). Reuse
  without this wrapper would violate the five-decision separation the package itself
  mandates on plate 10-B.
- **Model allocator**: fix-before-reuse (M-1) — either upstream a fail-closed mode or
  wrap allocation and refuse silent defaults for capsule-bound attempts.
- **Guardrails/tiered policy**: fix-before-reuse (O-2) — deployed rules path must be
  wired or AI4RnD ships its own policy loading.
- **agent_evolving**: bounded reuse (candidate-generation ideas only); GEPA remains the
  promotion/rollback/frozen-policy authority — matches the Rev-5 matrix corrections
  (FN-05/FN-11/FN-23 → ADAPT with GEPA evidence).
- **Capsule registry/resolver**: extend (v1→v2) with the four migration defects fixed
  (M-2/M-3/M-4/M-5) plus schema/validator updates
  (`schemas/draft/capability-capsule.v1.draft.json`,
  `validate_capability_capsule_semantics`).
- **tmux carrier**: reject-retire, as the package already says; the retained-semantics
  list on plate 09-D (typed work packet, capability decision, artifact expectations) is
  the correct salvage boundary.
- **Evidence foundation**: bounded derivation — promote the research pipeline's proven
  schema shape (spans, hashes, claim links) to the harness level rather than building
  the plate-10-A chain from scratch; keep the gate ledger as-is (its pattern is the
  strongest verified piece of the current evidence story).

## 11. Prioritized diagram corrections

(Not applied — per the brief, this review precedes any revision.)

1. **Plate 06 invariant strip** (`build_design.py:267`): "41 unique manifests … 34
   entries (30 stable, 4 draft)" → "42 unique manifests … 35 entries (30 stable,
   5 draft)". Same fix at `build_design.py:126` (plate 01 generator). Regenerate.
2. **Plate 06 §3 Model box**: add "current allocator falls back silently — fix before
   reuse" or restate as target requirement with a badge.
3. **Plate 06 §1 Planner blueprint**: reconcile with the YAML step schema (M-2) — pick
   operator-referenced or skill-bundle steps and make both artifacts say the same thing.
4. **Plate 08 SwarmFlow row**: add the silent-step-failure caveat to Returns; note
   tool-surface resume rejection in Durability.
5. **Plate 10-A/C**: add current/target badges; correct claim-link vocabulary to
   `supports/refutes/qualifies`; "char+byte offsets" → "span offsets"; point at
   `research/migrations/001_init.sql` as the existing substrate.
6. **Plate 07-E Permission engine**: annotate the deployed zero-rules gap; move the
   permission check visually inside the before-tool Rail phase in step 6.
7. **Plate 09-C**: add per-box wiring badges (live vs partially wired) for the capsule
   loader/stage expansion path.
8. STYLE: add solid/dashed legends to plates 07/09; consider theme-variable colors for
   consistency with the site's diagrams.

## 12. Source-verified claims

Claims from the package that this review confirmed directly against source (paths as
cited in §6–§9): the 11-event Rail envelope with after-only ReAct hook; the
`AgentRail` overridable surface; the DeepAgentSpec→BuildContext→DeepAgentConfig→DeepAgent
chain with cross-process rebuild seed; PermissionLevel ALLOW/ASK/DENY; SysOperationRail
auto-prepension; the JiuwenSwarm gateway→AgentServer→agent-manager resolution chain; all
sixteen mechanism cells on plate 08; `no_matching_worker`; the PM/Planner/Builder/
Evaluator role machine; send-keys + separate Enter; busy-marker pane classification;
mtime reconciliation; quarantine; capsule resolver admission order and honest-stall
error strings; the secrets-require-guard and operator-deny enforcement in v1; Physical
Operator registry existence and consumption; gate ledger append-only/writer-attributed/
projection semantics; GEPA CandidateType, stoppers, Promoter, frozen-policy checker;
research-store span/hash/claim schema; capsule census (42/11/35/30+5/7/0).

## 13. Execution-verified claims

Reused executed evidence from this analysis (commands run in the verify venvs, results
recorded in prior passes and re-cited here): SwarmFlow failed-step → `None` with
successful run report and journal replay semantics (probe_r2, three-run replay);
`SwarmflowTool` rejection of `resume_id`/`name` and its exact option schema (probe_r1);
unknown-option hard failure listing
`['agent_type','isolation','label','model','phase','schema','timeout']` (probe_r3);
zero-argument conditional router fan-out completing (probe_r4); guardrail loader
resolving zero rules in the JiuwenSwarm layout (builtin-rules probe); Symphony ranking
(never refusing) and `ensure_persistent_checkpointer()` sqlite default. New execution
for this review: full plate rendering with console-error capture and overflow checks
(clean), and the capsule/registry census scripts (`capsule_census2.py`,
`reg_census.py`) whose outputs ground B-1.

## 14. Inferences

Stated as inferences, not verified facts: (a) the plate's 41/34/4 miscounts stem from
missing one `understand-anything` draft capsule — pattern-consistent but unproven;
(b) plate 09-C's stage expansion order reflects the resolver's attachment order —
the resolver provably attaches guards before resources and verifier hooks last, but no
code emits graph *stages* in that order today; (c) "data/benchmark on-ramp partial" on
plate 10 refers to benchmark tooling (`agent_arena_benchmark.py`,
`capability_fusion_benchmark.py`) rather than a GEPA candidate type; (d) the intended
enforcement point for `planner_policy` is the plan validator
(`harness/lib/plan_validator.py`) — plausible, undesignated.

## 15. Unknowns and required spikes

1. **Capsule→TaskGraph expansion spike**: implement one v2 `planning_blueprint` end to
   end (one capsule, two steps, one guard) through plan validation and dispatch, to
   settle M-2's step-unit question with running code rather than schema argument.
2. **Allocator fail-closed spike**: measure what actually happens today when a
   capsule-bound team member's pool group is missing (which model runs, what is logged),
   then decide wrapper vs upstream fix (M-1).
3. **Guardrail wiring spike**: confirm whether pointing the tiered-policy loader at
   JiuwenSwarm's `resources/builtin_rules.yaml` is a config change or a code change
   (O-2).
4. **Evidence-store convergence spike**: attempt one projection (plate 10-C's trace
   graph) over the existing four stores to test the one-store-with-projections claim
   before committing to it.
5. **Unregistered-manifest disposition**: decide register/retire for the 7 unregistered
   manifests (three are `adapter.*` — a kind that neither v1 registry groups nor the v2
   `capsule_kind` enum names; the v2 enum must either add `adapter` or those capsules
   must be reclassified).
6. **Dark-mode intent for the review shell**: unknown whether `diagram-review.html` is
   meant to join the themed site; decides whether plates need variable colors (STYLE).

## 16. Presentation-readiness verdict

**Not ready as committed; ready after small, well-bounded fixes.** Gate: correct the
inventory line everywhere it appears and regenerate (B-1/B-2) — until then the package
contains a false "Current source" statement. Strongly recommended before circulating:
the two one-line badge/caption fixes that close M-1 and M-6, and the plate-08 SwarmFlow
caveat (O-1), since each prevents a reader from designing against a guarantee the
runtime does not provide. The v2 template should be circulated as a proposal with
M-2–M-5 attached as open migration issues rather than silently merged. Everything else
in this review is refinement: the package's core content — the turn anatomy, the
four-mechanism decomposition, the carrier-rejection boundary, the five-decision
evaluation split, and the three-axis capsule status model — is verified sound and is a
genuine advance over the prior high-level plates.

---

## 17. Design response after the audit

This section records the bounded revision made in response to the review. It does not
retroactively change the evidence classes above and does not claim that a runtime bridge was
implemented.

### Applied

- Corrected both generated Capsule census claims to **42 manifests, 35 registered, 30 stable,
  5 draft and 7 unregistered**.
- Made exact model/executor binding a visibly **target, fail-closed obligation** and carried the
  current silent-fallback defect as fix/fence-before-reuse.
- Reconciled the target blueprint around one `logical_operator_ref` per step; skills, tools and
  MCP remain replaceable requirements or bindings beneath that logical action.
- Restored an explicit Physical Operator id deny-list, independently of kind-level deny rules.
- Defined v1 `default_operator_profile` migration as a capability-scoped preference that is
  requalified and pinned per attempt, never copied into Capsule identity.
- Restated the secret-reference-requires-guard invariant and assigned enforcement at semantic
  validation and runtime admission.
- Corrected evidence vocabulary and currency: the current hash/span/claim substrate is the
  research SQLite store; harness-wide integration and typed graph projections remain target.
- Added the verified SwarmFlow empty-success, engine-only resume, silent model fallback and
  zero-loaded-rules hazards to the system plates and contract obligations.
- Added current/target/partial wording where Capsule stage expansion, evidence integration and
  GEPA/data paths were previously too broad.
- Added a contract-level plate and normative design document defining `PlanSlice`,
  `BindingDecision`, `ExecutionSpec`, `AttemptReceipt` and `EvaluationGateRecord`, including
  idempotency conflicts, attempt fencing, cancellation acknowledgement, stale-result
  quarantine, restart reconciliation and fail-closed gate persistence.

### Still open by design

- No v2 Capsule has been expanded through a running Planner, binder and OpenJiuwen mechanism.
- No credentialed live-team probe has demonstrated exact model binding or the current fallback.
- The guardrail loader is still a product defect; this package specifies the non-empty,
  digest-pinned target contract but does not modify product code.
- The five boundary objects are normative proposals, not implemented schemas or services.
- Evidence-store convergence, authoritative gate persistence and mechanism-specific receipt
  adapters still require the spikes in §15 and the contract document.

### Readiness after the response

The revised package is suitable for **contract-design stakeholder review** once its generated
artifacts and browser rendering pass. It remains unfit for implementation sign-off until the
required execution spikes validate the contract against real OpenJiuwen mechanisms.
