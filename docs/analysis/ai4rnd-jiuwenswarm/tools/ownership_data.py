# coding: utf-8
"""Per-row implementation-ownership decisions for the 142 workbook L2 features.

Row identity, L1/L2 wording and descriptions come from the workbook itself
(`workbook142.json`), never from this file. This file carries only the analytic
columns: who owns the meaning, who runs it, who stores it, who validates it,
where the user sees it, and what has to be built.

Column vocabularies are fixed by the brief:

  owner      AI4RnD Core | AI4RnD-Jiuwen Integration | JiuwenSwarm Application
             | OpenJiuwen Runtime | External / New Product Work | Unresolved
  decision   REUSE | CONFIGURE | ADAPT | PORT | EXTEND | BUILD | DEFER | UNRESOLVED
  evidence   EXEC (executed here) | SRC (source-read) | DOC (documented) | INF (inferred)

`GROUP` gives per-L1-group defaults; `ROW` overrides individual features.
Anything a row does not override is inherited from its group.
"""

# --------------------------------------------------------------- group defaults
# keys: sem (semantic owner), run (runtime implementer), mech (Jiuwen execution
# mechanism), persist (authoritative store), verify (verification authority),
# surface (user-facing product surface), subsystem, phase, pclass (preservation
# class, see PRESERVE_RULES)
GROUP = {
 # ---- Workflow plane -------------------------------------------------------
 ("Workflow", "Ingestion"): dict(
    sem="AI4RnD Core", run="JiuwenSwarm Application", mech="DeepAgent (session turn)",
    persist="JiuwenSwarm session store + AI4RnD intake ledger",
    verify="AI4RnD intake qualification rules", surface="Chat / channel + project intake view",
    subsystem="Intake plane", phase="P1", pclass="app_sem"),
 ("Workflow", "Requirement compilation"): dict(
    sem="AI4RnD Core", run="AI4RnD Core", mech="DeepAgent (bounded agent work)",
    persist="AI4RnD project Contract record", verify="AI4RnD Contract acceptance check",
    surface="Project view - Contract panel", subsystem="Intention Compiler",
    phase="P1", pclass="sem"),
 ("Workflow", "Search & ideation"): dict(
    sem="AI4RnD Core", run="AI4RnD-Jiuwen Integration", mech="SwarmFlow (deterministic fan-out)",
    persist="AI4RnD evidence ledger", verify="AI4RnD evidence + source qualification evaluators",
    surface="Project view - evidence browser", subsystem="Discovery lane",
    phase="P2", pclass="sem"),
 ("Workflow", "Idea identification / screening / opportunity selection"): dict(
    sem="AI4RnD Core", run="AI4RnD Core", mech="SwarmFlow (panel) + DeepAgent",
    persist="AI4RnD opportunity store", verify="AI4RnD screening evaluators + gate ledger",
    surface="Project view - opportunity portfolio", subsystem="Opportunity lane",
    phase="P4", pclass="sem"),
 ("Workflow", "Generate technical claims & hypothesis"): dict(
    sem="AI4RnD Core", run="AI4RnD Core", mech="SwarmFlow (panel)",
    persist="AI4RnD claim graph", verify="AI4RnD falsifiability + scientific-validity evaluators",
    surface="Project view - claims panel", subsystem="Claims lane",
    phase="P4", pclass="sem"),
 ("Workflow", "POC implementation"): dict(
    sem="AI4RnD Core", run="OpenJiuwen Runtime", mech="Code mode / worktree + jiuwenbox sandbox",
    persist="Jiuwen worktree + AI4RnD build evidence", verify="AI4RnD engineering-correctness evaluator",
    surface="Project view - build panel", subsystem="Builder",
    phase="P4", pclass="sem_exec"),
 ("Workflow", "Benchmarking"): dict(
    sem="AI4RnD Core", run="AI4RnD-Jiuwen Integration", mech="Deterministic tools + SwarmFlow",
    persist="AI4RnD benchmark store", verify="AI4RnD performance/cost/benchmark evaluator",
    surface="Project view - benchmark panel", subsystem="Benchmarking lane",
    phase="P4", pclass="sem"),
 ("Workflow", "Evaluation"): dict(
    sem="AI4RnD Core", run="AI4RnD Core", mech="SwarmFlow (panel) + deterministic checks",
    persist="AI4RnD evidence ledger + gate ledger",
    verify="AI4RnD evaluator families (writer != verifier)",
    surface="Project view - evaluation dossier", subsystem="Evaluation lane",
    phase="P3", pclass="sem"),
 ("Workflow", "Delivery"): dict(
    sem="AI4RnD Core", run="AI4RnD-Jiuwen Integration", mech="DeepAgent + deterministic packaging",
    persist="AI4RnD deliverable store", verify="AI4RnD lifecycle/parity/human-review evaluator",
    surface="Project view - deliverables + channels", subsystem="Delivery lane",
    phase="P5", pclass="sem"),
 # ---- Foundation plane -----------------------------------------------------
 ("Foundation", "Capability capsule"): dict(
    sem="AI4RnD Core", run="AI4RnD Core", mech="n/a - capsules constrain execution, do not perform it",
    persist="AI4RnD capsule registry (workspace-scoped)",
    verify="Capsule certification + conformance evaluator",
    surface="Capability registry view", subsystem="Capability Capsules",
    phase="P3", pclass="sem"),
 ("Foundation", "Operators"): dict(
    sem="AI4RnD Core", run="AI4RnD-Jiuwen Integration",
    mech="binding target: DeepAgent / SwarmFlow worker / tool / Team member",
    persist="AI4RnD operator registry", verify="Operator admission + runtime profiling",
    surface="Capability registry view - operators", subsystem="Operators",
    phase="P3", pclass="sem_exec"),
 ("Foundation", "Evaluator"): dict(
    sem="AI4RnD Core", run="AI4RnD Core", mech="Deterministic tools + DeepAgent judges",
    persist="AI4RnD evidence ledger", verify="Evaluator self-calibration + human review",
    surface="Project view - evaluation dossier", subsystem="Evaluators",
    phase="P3", pclass="sem"),
 ("Foundation", "Foundational models"): dict(
    sem="JiuwenSwarm Application", run="JiuwenSwarm Application", mech="Jiuwen model pool / allocator",
    persist="JiuwenSwarm model pool config", verify="JiuwenSwarm config validation",
    surface="Settings - models", subsystem="Model plane", phase="P1", pclass="app"),
 ("Foundation", "RSI"): dict(
    sem="AI4RnD Core", run="AI4RnD-Jiuwen Integration", mech="openjiuwen agent_evolving (Trainer/Updater/Operator)",
    persist="AI4RnD improvement store + openjiuwen EvolutionStore",
    verify="Governed promotion gate (approval + frozen-policy check)",
    surface="Improvements inbox", subsystem="Governed RSI", phase="P6", pclass="rsi"),
 ("Foundation", "Data foundations"): dict(
    sem="AI4RnD Core", run="AI4RnD Core", mech="Jiuwen retrieval / store where projections are served",
    persist="AI4RnD typed graph projections over one authoritative store",
    verify="Schema + provenance conformance evaluator",
    surface="Project view - knowledge browser", subsystem="Data foundations",
    phase="P5", pclass="data"),
 ("Foundation", "Harness Core"): dict(
    sem="AI4RnD Core", run="OpenJiuwen Runtime",
    mech="Pregel / Core Workflow / SwarmFlow journal / ConcurrencyGovernor",
    persist="Jiuwen checkpointer + SwarmFlow journal",
    verify="Runtime invariants + AI4RnD run-state assertions",
    surface="Project view - run status (read-only)", subsystem="Harness Core",
    phase="P2", pclass="sched"),
 ("Foundation", "Intention compilers"): dict(
    sem="AI4RnD Core", run="AI4RnD Core", mech="DeepAgent (bounded)",
    persist="AI4RnD Contract record", verify="Contract completeness + acceptance compilation checks",
    surface="Project view - Contract panel", subsystem="Intention Compiler",
    phase="P1", pclass="sem"),
 ("Foundation", "Planner"): dict(
    sem="AI4RnD Core", run="AI4RnD Core", mech="n/a - planning emits a logical plan, execution is separate",
    persist="AI4RnD TaskGraph store", verify="TaskGraph validation + feasibility analysis",
    surface="Project view - plan inspector", subsystem="Planner", phase="P2", pclass="sem"),
 ("Foundation", "Builder"): dict(
    sem="AI4RnD Core", run="OpenJiuwen Runtime", mech="Code mode / worktree + DeepAgent + deterministic tools",
    persist="Jiuwen worktree + AI4RnD artifact store",
    verify="AI4RnD engineering + conformance evaluators",
    surface="Project view - build panel", subsystem="Builder", phase="P4", pclass="sem_exec"),
 # ---- Vertical plane -------------------------------------------------------
 ("Vertical", "Visibility / Statistics"): dict(
    sem="JiuwenSwarm Application", run="JiuwenSwarm Application", mech="Jiuwen observability / telemetry",
    persist="JiuwenSwarm telemetry store", verify="JiuwenSwarm platform tests",
    surface="Web UI - status and statistics", subsystem="Visibility", phase="P2", pclass="app"),
 ("Vertical", "Installer & CLI & Webapp"): dict(
    sem="JiuwenSwarm Application", run="JiuwenSwarm Application", mech="n/a - packaging and distribution",
    persist="Installed workspace on disk", verify="JiuwenSwarm packaging tests",
    surface="Installer / CLI / web app", subsystem="Distribution", phase="P1", pclass="app"),
 ("Vertical", "UI"): dict(
    sem="JiuwenSwarm Application", run="JiuwenSwarm Application", mech="n/a - presentation",
    persist="JiuwenSwarm UI state", verify="JiuwenSwarm UI tests",
    surface="CLI / GUI / TUI", subsystem="UI shell", phase="P1", pclass="app"),
 ("Vertical", "Account management"): dict(
    sem="External / New Product Work", run="External / New Product Work",
    mech="n/a - identity service", persist="Account/identity store (absent today)",
    verify="Security review + authentication tests", surface="Account settings",
    subsystem="Accounts", phase="P6", pclass="absent"),
 ("Vertical", "Message Channels"): dict(
    sem="JiuwenSwarm Application", run="JiuwenSwarm Application", mech="Jiuwen channel adapters",
    persist="JiuwenSwarm channel config + session link",
    verify="JiuwenSwarm channel integration tests", surface="Channel settings",
    subsystem="Channels", phase="P1", pclass="app"),
 ("Vertical", "System Configurations"): dict(
    sem="JiuwenSwarm Application", run="JiuwenSwarm Application", mech="n/a - configuration",
    persist="JiuwenSwarm config store", verify="Config schema validation",
    surface="Settings", subsystem="Configuration", phase="P1", pclass="app"),
}

# ------------------------------------------------------------------ row detail
# id -> dict of overrides. Required per row: dec (decision), a4 (existing AI4RnD
# implementation), jw (existing Jiuwen/OpenJiuwen implementation), ev (reusable
# code/spec evidence), miss (missing work), ec (evidence class), conf
# (confidence). Optional: sem/run/mech/persist/verify/surface/phase/pclass
# override the group default; graph (affected data/knowledge graph); acc
# (acceptance evidence or test); note (assumptions / open questions);
# slices (named cross-layer implementation slices).
ROW = {}

def R(fid, **kw):
    ROW[fid] = kw

# ---------------------------------------------------------------- WORKFLOW (54)
R("WF-01", dec="EXTEND", conf="HIGH", ec="SRC",
  a4="Intake handled by coordinator.sh polling loop + tmux panes",
  jw="Gateway + 9 IM channels + session creation carry request capture",
  ev="jw-src/jiuwenswarm/gateway/, agents/harness/common/session_ops_service.py",
  miss="Bind a captured request to an AI4RnD project record and Contract draft",
  acc="A message on any channel creates a project record with the raw request preserved",
  graph="Trace graph")
R("WF-02", dec="BUILD", conf="MEDIUM", ec="INF",
  a4="Channel signal intake exists for social/GitHub sources, not V-05-qualified Slack",
  jw="Slack channel adapter exists; no qualification tier",
  ev="jw-src/jiuwenswarm/gateway/channel_manager/",
  miss="V-05 qualification tier and clue schema",
  acc="An unqualified clue is rejected with a stated reason",
  note="Workbook references a 'V-05' qualification level defined outside the workbook; definition unresolved")
R("WF-03", dec="REUSE", conf="HIGH", ec="SRC",
  a4="File ingest via harness tools",
  jw="Parser registry loads xlsx/csv/pdf/docx/md/html/json/images at import time",
  ev="openjiuwen parser registration (observed on every process start)",
  miss="Attach imported material to the project record as first-class evidence",
  acc="An uploaded PDF appears in the evidence ledger with a content hash")
R("WF-04", dec="ADAPT", conf="HIGH", ec="SRC",
  a4="Session/pane binding via coordinator state machine",
  jw="Session, workspace and user binding in the gateway; team workspace layout",
  ev="jw-src/jiuwenswarm/agents/harness/common/session_ops_service.py",
  miss="project_id in session metadata; project<->session link that survives restart",
  acc="A restarted agent server still resolves the session to its project")
R("WF-05", dec="PORT", conf="MEDIUM", ec="SRC",
  a4="Deduplication in the ingestion tools",
  jw="No intake-level dedup", ev="AI4Research harness ingest tooling",
  miss="Canonicalisation rules for research intake", acc="Two identical clues yield one candidate")
R("WF-06", dec="PORT", conf="HIGH", ec="EXEC",
  a4="Evidence ledger records provenance with citation spans (117 LOC lib/evidence_ledger.py)",
  jw="No provenance concept at intake",
  ev="AI4Research harness/lib/evidence_ledger.py; executed standalone in V-10",
  miss="Bind intake provenance to the ledger at capture time",
  acc="Every intake candidate resolves to a source with a byte offset", graph="Trace graph")
R("WF-07", dec="ADAPT", conf="MEDIUM", ec="SRC",
  a4="Gate ledger provides append-only, writer-attributed qualification decisions",
  jw="No qualification stage", ev="AI4Research harness/lib/gate_ledger.py (372 LOC)",
  miss="Intake qualification rule set and its gate", acc="A disqualified intake never reaches compilation")

R("WF-08", dec="ADAPT", conf="HIGH", ec="SRC",
  a4="Requirement compiler present (lib/research/deepdive_requirement_compiler.py)",
  jw="WorkflowController.intent_detection classifies intent for routing, not for R&D meaning",
  ev="AI4Research lib/research/deepdive_requirement_compiler.py; openjiuwen workflow_controller.py",
  miss="Map compiled intent onto the Contract schema",
  acc="An ambiguous request produces an explicit interpretation the user can correct")
R("WF-09", dec="ADAPT", conf="MEDIUM", ec="SRC", a4="Context scoping in the requirement compiler",
  jw="Session context + workspace scoping", ev="AI4Research requirement compiler; Jiuwen session scope",
  miss="Scope as a Contract field with an explicit boundary", acc="Out-of-scope work is refused with a reason")
R("WF-10", dec="ADAPT", conf="MEDIUM", ec="SRC", a4="Ambiguity handling in the compiler",
  jw="Human-interaction interrupt exists in Core Workflow and SwarmFlow human_session",
  ev="openjiuwen workflow_config.handle_type='interrupt'; swarmflow human_session primitive",
  miss="Ambiguity questions raised as a first-class blocking state", acc="An ambiguous Contract cannot be confirmed")
R("WF-11", dec="ADAPT", conf="MEDIUM", ec="SRC", a4="Constraint capture in the compiler",
  jw="Permission engine and jiuwenbox express runtime constraints, not research constraints",
  ev="openjiuwen harness/security/tiered_policy.py", miss="Research constraint vocabulary (budget, time, data, IP)",
  acc="A constraint that cannot be satisfied blocks planning")
R("WF-12", dec="BUILD", conf="MEDIUM", ec="INF", a4="No explicit prioritisation stage",
  jw="None", ev="-", miss="Requirement prioritisation model", acc="Requirements carry a stated priority order")
R("WF-13", dec="ADAPT", conf="HIGH", ec="SRC", a4="Acceptance criteria in capsule contract postconditions",
  jw="None", ev="42 capsule manifests all carry contract.postconditions and contract.invariants",
  miss="Project-level acceptance definition distinct from capsule-level",
  acc="Every Contract has machine-checkable acceptance criteria")
R("WF-14", dec="BUILD", conf="MEDIUM", ec="INF", a4="No explicit user confirmation step",
  jw="Human interrupt mechanism available", ev="openjiuwen interrupt handling",
  miss="Contract confirmation gate with a durable record",
  acc="Work cannot start before the Contract is confirmed", graph="Policy graph")

R("WF-15", dec="PORT", conf="HIGH", ec="SRC", a4="Search strategy formation in the survey planner",
  jw="Symphony skill retrieval is capability search, not literature search",
  ev="AI4Research lib/research/survey/planner.py", miss="Strategy as a reviewable plan artifact",
  acc="The search strategy is inspectable before execution")
R("WF-16", dec="PORT", conf="HIGH", ec="SRC", a4="Multi-source discovery implemented (arXiv, HF, GitHub, YouTube sources)",
  jw="No literature sources", ev="AI4Research lib/research/sources/",
  miss="Compile discovery fan-out to SwarmFlow", acc="A discovery run returns sources from more than one modality")
R("WF-17", dec="PORT", conf="HIGH", ec="EXEC", a4="Source qualification in the research evaluator",
  jw="None", ev="AI4Research tools/research/evaluator.py", miss="Qualification thresholds as policy, not code constants",
  acc="An unqualified source is excluded with a recorded reason")
R("WF-18", dec="PORT", conf="MEDIUM", ec="SRC", a4="Technical signal extraction (extractors/)",
  jw="None", ev="AI4Research lib/research/extractors/", miss="Typed signal schema", acc="Extracted signals validate against a schema")
R("WF-19", dec="PORT", conf="MEDIUM", ec="SRC", a4="Signal organisation in survey tooling",
  jw="None", ev="AI4Research lib/research/survey/", miss="Projection into the concept graph",
  acc="Signals are grouped and the grouping is reproducible", graph="Concept graph")
R("WF-20", dec="PORT", conf="MEDIUM", ec="SRC", a4="Trend and gap analysis in survey tooling",
  jw="None", ev="AI4Research lib/research/survey/", miss="Gap statements bound to evidence", acc="Each claimed gap cites the sources that establish it")
R("WF-21", dec="PORT", conf="MEDIUM", ec="SRC", a4="Idea generation capsule (cap.research-idea-generate)",
  jw="None", ev="AI4Research capability-capsules/cap.research-idea-generate.yaml",
  miss="Wire the capsule to a runner", acc="Generated ideas trace to the signals that motivated them")
R("WF-22", dec="BUILD", conf="MEDIUM", ec="INF", a4="No explicit coverage review",
  jw="None", ev="-", miss="Coverage metric and stopping rule", acc="A search stops on a stated coverage criterion, not a fixed count")

R("WF-23", dec="BUILD", conf="MEDIUM", ec="INF", a4="Partial - candidate handling inside ideation",
  jw="None", ev="-", miss="Consolidation stage across discovery runs", acc="Duplicate candidates across runs merge deterministically")
R("WF-24", dec="ADAPT", conf="MEDIUM", ec="SRC", a4="Idea evaluate capsule (cap.research-idea-evaluate)",
  jw="None", ev="AI4Research capability-capsules/cap.research-idea-evaluate.yaml",
  miss="Identification distinct from evaluation", acc="Identified ideas carry a stable id reused downstream")
R("WF-25", dec="BUILD", conf="HIGH", ec="EXEC", a4="Absent - no idea_card symbol anywhere in the repository",
  jw="None", ev="grep for idea_card across AI4Research lib/ and tools/ returns 0 files",
  miss="Idea Card schema and its editor", acc="Every opportunity has an Idea Card that validates against the schema",
  note="Confirmed absent in this revision by direct search, matching the prior finding")
R("WF-26", dec="BUILD", conf="MEDIUM", ec="INF", a4="No explicit opportunity object", jw="None", ev="-",
  miss="Opportunity record distinct from idea", acc="An opportunity references its ideas and its screening verdicts")
R("WF-27", dec="ADAPT", conf="MEDIUM", ec="SRC", a4="Technical screening inside idea evaluation",
  jw="None", ev="AI4Research capsule verification sections", miss="Screening as a gate with a recorded verdict",
  acc="A technically infeasible opportunity is blocked before claims are formed")
R("WF-28", dec="BUILD", conf="LOW", ec="INF", a4="No strategic screening", jw="None", ev="-",
  miss="Strategic criteria and their owner", acc="Strategic rejection is recorded with its criterion",
  note="Strategic criteria are organisation-specific; the workbook does not define them")
R("WF-29", dec="BUILD", conf="MEDIUM", ec="INF", a4="No portfolio view", jw="None", ev="-",
  miss="Portfolio prioritisation across projects", acc="Opportunities rank against each other, not only within a project")

R("WF-30", dec="PORT", conf="HIGH", ec="SRC", a4="Claim compiler + claim-extract capsule",
  jw="None", ev="AI4Research lib/research/claim_compiler.py; cap.research-claim-extract.yaml",
  miss="Research question as a distinct object from the claim", acc="Each claim states what would refute it",
  graph="Concept graph")
R("WF-31", dec="PORT", conf="HIGH", ec="EXEC", a4="Claim/evidence modelling with citation spans",
  jw="None", ev="AI4Research tests/research/unit/test_claim_evidence.py, test_evidence_span.py",
  miss="Data and method as first-class model elements", acc="A claim resolves to evidence at char and byte offsets",
  graph="Concept graph")
R("WF-32", dec="BUILD", conf="MEDIUM", ec="INF", a4="Hypotheses implicit in claims", jw="None", ev="-",
  miss="Hypothesis pool and mechanism model", acc="Competing hypotheses are held simultaneously")
R("WF-33", dec="BUILD", conf="HIGH", ec="EXEC", a4="Two files mention falsifiability; no screening stage",
  jw="None", ev="grep falsifiab across AI4Research lib/ and tools/ matches 2 files",
  miss="Falsifiability screening and hypothesis contracting - the scientific core",
  acc="A non-falsifiable hypothesis is blocked before POC construction")
R("WF-34", dec="ADAPT", conf="MEDIUM", ec="SRC", a4="Experiment design capsule (cap.research-experiment-design)",
  jw="None", ev="AI4Research capability-capsules/cap.research-experiment-design.yaml",
  miss="Design tied to the falsifiability verdict", acc="A POC design states which hypothesis it can refute")

R("WF-35", dec="REUSE", conf="HIGH", ec="SRC", a4="Environment preparation scripts",
  jw="Worktree manager + jiuwenbox sandbox (bwrap/cgroup) provide isolated build environments",
  ev="openjiuwen agent_teams/worktree.py; jiuwenbox policies",
  miss="Bind environment to the capsule effects declaration", acc="A capsule declaring network:none cannot get a networked environment")
R("WF-36", dec="REUSE", conf="HIGH", ec="SRC", a4="Build agents in the harness",
  jw="Code mode with worktree isolation is the intended construction mechanism",
  ev="openjiuwen agent_teams/worktree.py; agent(options={'isolation':'worktree'})",
  miss="Construction driven by a Build Contract rather than a free-form prompt", acc="A build runs in its own worktree and leaves the main tree untouched")
R("WF-37", dec="ADAPT", conf="MEDIUM", ec="SRC", a4="Integration handled ad hoc", jw="Worktree + tool execution",
  ev="openjiuwen worktree manager", miss="Component integration as a declared step with its own acceptance",
  acc="Integration failures are attributed to a component")
R("WF-38", dec="BUILD", conf="MEDIUM", ec="INF", a4="No explicit readiness validation", jw="None",
  ev="-", miss="Functional readiness checks before benchmark handoff", acc="An unready POC cannot enter benchmarking")
R("WF-39", dec="BUILD", conf="MEDIUM", ec="INF", a4="No consolidation/handoff artifact", jw="None", ev="-",
  miss="Testable artifact manifest and handoff contract", acc="Benchmarking receives a manifest, not a directory")

R("WF-40", dec="ADAPT", conf="MEDIUM", ec="SRC", a4="Benchmark framing inside benchmark tooling",
  jw="None", ev="AI4Research lib/heavy_proof_benchmark.py, lib/platform_workflow_benchmark.py",
  miss="Framing tied to the claim under test", acc="A benchmark states which claim it can disconfirm")
R("WF-41", dec="PORT", conf="MEDIUM", ec="SRC", a4="Benchmark asset preparation present but unwired",
  jw="None", ev="AI4Research lib/capability_fusion_benchmark.py", miss="Protocol as a versioned artifact",
  acc="A benchmark protocol is reproducible from its record", graph="Dataset graph")
R("WF-42", dec="REUSE", conf="HIGH", ec="EXEC", a4="Benchmark runners exist",
  jw="SwarmFlow executes deterministic fan-out with a replayable journal",
  ev="probe_r2.py: run 3 replayed both steps with zero live calls",
  miss="Benchmark runs registered as AI4RnD evidence", acc="A benchmark re-run reproduces from the journal")
R("WF-43", dec="PORT", conf="MEDIUM", ec="SRC", a4="Metrics collection in report_metrics.py",
  jw="Observability rail collects agent spans", ev="AI4Research tools/research/report_metrics.py",
  miss="Run evidence bound to the claim graph", acc="Every metric traces to the run that produced it", graph="Trace graph")
R("WF-44", dec="BUILD", conf="MEDIUM", ec="INF", a4="Partial comparison tooling", jw="None", ev="-",
  miss="Comparative analysis with baselines and packaging", acc="Results are stated against a named baseline")

R("WF-45", dec="ADAPT", conf="HIGH", ec="EXEC", a4="Evidence assembly in the evidence ledger",
  jw="None", ev="AI4Research lib/evidence_ledger.py executed standalone",
  miss="Scope declaration for an evaluation round", acc="An evaluation states exactly which evidence it considered")
R("WF-46", dec="ADAPT", conf="HIGH", ec="EXEC", a4="Provenance review present; grounding check measured at precision 0.25",
  jw="llm_as_judge metric and judge calibration exist in agent_evolving",
  ev="V-12 measured grounding precision 0.25 on a hand-labelled 9-case set; openjiuwen agent_evolving/evaluator/metrics",
  miss="Replace the grounding check with calibrated entailment; publish a measured bar",
  acc="Entailment precision measured on a labelled set and materially above 0.25",
  note="This is the single largest correctness risk in the product; the current check does not hold")
R("WF-47", dec="BUILD", conf="MEDIUM", ec="INF", a4="Partial - artifact review capsule exists",
  jw="None", ev="AI4Research cap.research-artifact-review.yaml",
  miss="Experimental, reasoning and external validity as separate reviews", acc="Each validity dimension has its own verdict")
R("WF-48", dec="ADAPT", conf="MEDIUM", ec="SRC", a4="Claim verify capsule compares claims to evidence",
  jw="None", ev="AI4Research cap.research-claim-verify.yaml contract",
  miss="Comparison against the project Contract acceptance criteria", acc="Acceptance is decided against the Contract, not restated")
R("WF-49", dec="PORT", conf="HIGH", ec="EXEC", a4="Gate ledger records verdicts append-only with writer attribution",
  jw="None", ev="AI4Research lib/gate_ledger.py (372 LOC); exercised in this analysis",
  miss="Residual-risk classification vocabulary", acc="A verdict cannot be edited, only superseded", graph="Policy graph")
R("WF-50", dec="BUILD", conf="MEDIUM", ec="INF", a4="No structured follow-up record", jw="None", ev="-",
  miss="Refinement and follow-up as tracked items", acc="Every blocker produces a follow-up with an owner")

R("WF-51", dec="BUILD", conf="MEDIUM", ec="INF", a4="No delivery planning stage", jw="Channel delivery exists",
  ev="jw-src/jiuwenswarm/gateway/channel_manager/", miss="Delivery plan and evidence handoff",
  acc="A deliverable ships with the evidence that supports it")
R("WF-52", dec="PORT", conf="MEDIUM", ec="SRC", a4="Report drafting capsules (report-plan, report-draft, publication-produce)",
  jw="None", ev="AI4Research cap.research-report-plan.yaml, cap.research-report-draft.yaml",
  miss="Deliverable templates bound to audience", acc="A generated report cites only evidence in the ledger")
R("WF-53", dec="BUILD", conf="MEDIUM", ec="INF", a4="Partial packaging", jw="Skill packaging exists in JiuwenSwarm",
  ev="jw-src/jiuwenswarm/server/runtime/skill/skill_manager.py",
  miss="Reusable asset extraction and knowledge packaging", acc="A completed project yields at least one reusable capsule candidate")
R("WF-54", dec="ADAPT", conf="MEDIUM", ec="SRC", a4="No lifecycle closure", jw="Channels can distribute; no authorization tier",
  ev="jw-src/jiuwenswarm/gateway/", miss="Authorized distribution and project closure semantics",
  acc="Closing a project freezes its evidence and records who authorized distribution", graph="Policy graph")

# -------------------------------------------------------------- FOUNDATION (65)
R("FN-01", dec="REUSE", conf="HIGH", ec="EXEC",
  a4="42 capsule manifests share one 10-section schema: applicability, contract, composition, effects, bindings, verification, operator_compatibility, provenance",
  jw="Skills carry name/description/prompt only - no contract, effects or verification sections",
  ev="Parsed all 42 manifests in harness/capability-capsules and config/capability-capsules",
  miss="Assembly UI and schema versioning", acc="A new capsule validates against the schema before registration",
  note="This is the evidence that Capsules are already a governed capability identity, not a workflow template")
R("FN-02", dec="EXTEND", conf="HIGH", ec="EXEC",
  a4="Registry holds 35 capsules (32 capability, 1 guard, 2 resource); 30 stable, 5 draft",
  jw="Skill registry has no certification or suspension states",
  ev="config/capability-capsules.registry.yaml parsed: statuses {stable:30, draft:5}",
  miss="Certification workflow, suspend/deprecate transitions, promotion history",
  acc="A capsule cannot move to stable without a recorded certification", graph="Policy graph")
R("FN-03", dec="ADAPT", conf="HIGH", ec="EXEC",
  a4="applicability.task_types / positive_signals / negative_signals on all 42 manifests",
  jw="Symphony skill retrieval scores skills by embedding similarity",
  ev="All 42 manifests carry the applicability triple; jw-src/jiuwenswarm/symphony/retrieval/",
  miss="Hard capability gate with discriminated stall reasons - Symphony ranks but never refuses",
  acc="A step needing an unavailable capability stalls with no_matching_worker and the missing list",
  note="Ranking without refusal is the central mismatch: research must stall honestly, not pick the nearest skill")
R("FN-04", dec="EXTEND", conf="MEDIUM", ec="SRC",
  a4="composition.consumes/produces/compatible_with/incompatible_with/requires_after on all 42",
  jw="No composition model between skills", ev="Parsed composition section on all 42 manifests",
  miss="Composition planner that uses the declared compatibility", acc="Incompatible capsules never appear in one plan")
R("FN-05", dec="ADAPT", conf="HIGH", ec="SRC",
  a4="GEPA Promoter implements promote/rollback with sha256 sidecars, tmp-vs-production path guards and atomic writes; the manifest schema itself carries no versions/history/RSI-target keys",
  jw="agent_evolving has Trainer/Updater but only ReactAgentEvolve implements get_operators()",
  ev="AI4Research integrations/gepa_optimizer/promote.py (Promoter.promote/rollback, 354 LOC, unit-tested); manifest key census: no benchmarks/performance_history/rsi_targets keys",
  miss="Wire Promoter to the capsule registry; extend the manifest schema with versions, history and RSI targets",
  acc="A promoted capsule version can be rolled back and in-flight runs keep their pinned version",
  note="Rev 5 correction: promotion/rollback machinery already exists in GEPA and was previously overlooked - this row was BUILD, now ADAPT",
  phase="P6")

R("FN-06", dec="PORT", conf="MEDIUM", ec="SRC", a4="Operator definitions in the capsule operator bindings checker",
  jw="openjiuwen Operator is a tunable-parameter handle and is explicitly NOT an executable unit",
  ev="openjiuwen/core/operator/base.py line 10: 'Operator is NOT an executable unit'",
  miss="A distinct name for AI4RnD's executable unit to avoid the collision; registration API",
  acc="Logical Operators register and resolve by capability, not by name",
  note="Naming collision confirmed again this revision; AI4RnD's executable unit must not be called Operator inside Jiuwen")
R("FN-07", dec="BUILD", conf="MEDIUM", ec="SRC", a4="check_capsule_operator_bindings.py validates bindings",
  jw="No operator admission concept", ev="AI4Research tools/check_capsule_operator_bindings.py",
  miss="Admission, certification and governance lifecycle for operators", acc="An uncertified operator cannot be bound")
R("FN-08", dec="BUILD", conf="HIGH", ec="EXEC",
  a4="operator_compatibility.preferred/forbidden declared on all 42 manifests",
  jw="agent_type is accepted by the SwarmFlow option whitelist but no backend reads it",
  ev="probe_r3: backend received {'agent_type':'researcher'}; grep agent_type in workflow/backends/ returns nothing",
  miss="Binding layer that turns a logical requirement into a concrete executor and fails when none matches",
  acc="A forbidden operator can never be bound; an unsatisfiable requirement stalls rather than defaulting",
  note="This is the sharpest verified gap: the knob exists, is validated, and is then ignored")
R("FN-09", dec="ADAPT", conf="MEDIUM", ec="SRC", a4="Physical operator profiles in config/agent-actors.json",
  jw="Team member roster, worker backend and model pool constitute the execution fleet",
  ev="AI4Research config/agent-actors.json; openjiuwen agent_teams/models/allocator.py",
  miss="Fleet management driven by capsule bindings", acc="Fleet membership is derived, not hand-maintained")
R("FN-10", dec="BUILD", conf="MEDIUM", ec="INF", a4="No runtime capability profiling", jw="Observability spans exist",
  ev="openjiuwen observability rail", miss="Per-operator capability profile built from run evidence",
  acc="Operator selection uses measured performance, not declared performance", graph="Trace graph")
R("FN-11", dec="ADAPT", conf="MEDIUM", ec="SRC", a4="GEPA supplies candidate generation, Budget stoppers (spend/evals/walltime/plateau/stop-file), frozen-policy checking and Promoter rollback; CLI defaults to dry-run",
  jw="agent_evolving Trainer performs candidate selection on a validation set",
  ev="AI4Research integrations/gepa_optimizer/ (budgets.py, hard_policy_checker.py, promote.py, unit tests); openjiuwen agent_evolving/trainer/trainer.py",
  miss="Wire GEPA's loop to operator profiles and to the approval inbox",
  acc="An operator change is promoted only after measured improvement and approval",
  note="Rev 5 correction: was BUILD - the governance machinery exists in GEPA; the missing work is wiring, not construction", phase="P6")

R("FN-12", dec="ADAPT", conf="HIGH", ec="EXEC", a4="contract.postconditions and invariants on all 42 manifests",
  jw="Schema validation exists for tool inputs and outputs",
  ev="Parsed contract section on 42/42 manifests", miss="Conformance evaluator that runs the declared checks",
  acc="A postcondition failure blocks acceptance")
R("FN-13", dec="BUILD", conf="MEDIUM", ec="INF", a4="Partial engineering checks", jw="Code mode with test execution",
  ev="openjiuwen worktree + tool execution", miss="Engineering correctness and code quality evaluator family",
  acc="A POC failing its own tests cannot pass evaluation")
R("FN-14", dec="ADAPT", conf="MEDIUM", ec="SRC", a4="Benchmark tooling present", jw="Token accounting via budget in SwarmFlow",
  ev="openjiuwen workflow engine budget_total parameter", miss="Performance, cost and benchmark evaluator family",
  acc="Cost is evaluated against the Contract budget")
R("FN-15", dec="BUILD", conf="HIGH", ec="EXEC",
  a4="effects.read/write/execute/network/cost/risk declared on all 42 manifests",
  jw="Built-in shell guardrail tier loads zero rules: the package resources directory does not exist, and the copy JiuwenSwarm installs is never read back",
  ev="get_builtin_security_rules() returned 0; grep builtin_rules across jw-src finds only the two files that write the copy",
  miss="Security, privacy, compliance and IP evaluator; and a guardrail tier that actually loads",
  acc="A capsule declaring network:none cannot bind to a network-capable runner; guardrail rule count asserted non-zero at startup",
  note="Corrects the earlier claim that this was purely an openjiuwen packaging gap - the installed rules file is orphaned")
R("FN-16", dec="BUILD", conf="HIGH", ec="EXEC", a4="Grounding check measured at precision 0.25",
  jw="llm_as_judge and judge calibration exist inside agent_evolving but are not reachable from the application",
  ev="V-12 measurement; grep shows jiuwenswarm imports only the experience/archive and tool-description optimizer parts of agent_evolving",
  miss="Calibrated entailment evaluator - the scientific core of the product",
  acc="Measured entailment precision published against a labelled set", phase="P3")
R("FN-17", dec="BUILD", conf="MEDIUM", ec="INF", a4="verification.self_check/external_verifier/pass_conditions declared on all 42",
  jw="Human interrupt available", ev="Parsed verification section on 42/42 manifests",
  miss="Lifecycle, parity and human review evaluator", acc="Human review is recorded as evidence, not as chat")

R("FN-18", dec="EXTEND", conf="HIGH", ec="SRC", a4="model_registry.py in the harness",
  jw="Model pool with named groups and positional entries; provider configuration in the app",
  ev="openjiuwen agent_teams/models/allocator.py resolve_member_model",
  miss="Capability profile per model (context, tools, structured output, cost tier)",
  acc="A model without structured-output support is never selected for a schema-bearing step")
R("FN-19", dec="BUILD", conf="HIGH", ec="SRC",
  a4="Routing by capability in graph_scheduler",
  jw="resolve_member_model returns None for an unknown model name, and the caller then falls back to the worker base spec's model - silently",
  ev="openjiuwen agent_teams/models/allocator.py lines 417-423; team_worker_backend._resolve_model",
  miss="Routing that fails loudly when the required model is unavailable",
  acc="A step requiring an unavailable model stalls; it does not run on a substitute",
  note="Silent fallback is the reason AI4RnD cannot delegate model routing to Jiuwen as-is",
  run="AI4RnD-Jiuwen Integration", sem="AI4RnD Core", pclass="route",
  slices=["Model pool and provider configuration - JiuwenSwarm Application, REUSE",
          "Capability requirement to model constraint - AI4RnD Core, BUILD",
          "Loud-failure binding adapter over resolve_member_model - AI4RnD-Jiuwen Integration, BUILD"])
R("FN-20", dec="EXTEND", conf="MEDIUM", ec="SRC", a4="Usage accounting in harness tooling",
  jw="Observability rail and token budget accounting", ev="openjiuwen workflow engine budget; observability rail",
  miss="Audit attributable to project, claim and capsule", acc="Model spend is attributable to a project",
  graph="Trace graph", slices=["Raw usage capture - JiuwenSwarm Application, REUSE",
                               "Attribution to project and claim - AI4RnD Core, BUILD"])

R("FN-21", dec="ADAPT", conf="HIGH", ec="SRC", a4="GEPA optimizer for prompt and text artifacts",
  jw="agent_evolving tool-description optimizer family is imported by JiuwenSwarm (ToolDescriptionMethod, BeamSearch, SimpleEval)",
  ev="grep of jiuwenswarm imports from openjiuwen.agent_evolving lists the tool-description optimizer symbols",
  miss="Governed promotion for text artifacts", acc="A prompt change is versioned, measured and reversible",
  note="This is the one RSI surface with real wiring on both sides")
R("FN-22", dec="BUILD", conf="MEDIUM", ec="SRC", a4="Routing strategies in graph_scheduler",
  jw="Bandit or cost-aware routing is not present", ev="No routing optimizer found in either tree",
  miss="Runtime and resource routing optimisation", acc="Routing policy improves against a measured objective")
R("FN-23", dec="ADAPT", conf="HIGH", ec="SRC", a4="GEPA's typed candidate envelope already declares CAPSULE, SKILL, ROUTING_POLICY, REWRITE_RULES and COST_MODEL as its mutable families; capsule manifests carry no RSI-target keys yet",
  jw="Trainer.train requires an agent implementing get_operators(); only ReactAgentEvolve does",
  ev="AI4Research integrations/gepa_optimizer/candidate_schema.py CandidateType enum; grep 'def get_operators' across openjiuwen returns exactly one implementor",
  miss="Operator-protocol adapters exposing capsule tunables to Trainer/Updater; wire GEPA candidates to the registry",
  acc="A capsule can be registered as an evolution subject and improved under governance",
  note="Rev 5 correction: was BUILD - GEPA already types capsules as candidates and openjiuwen's Operator protocol is the adapter seam, so this is adaptation on both sides, not new construction")
R("FN-24", dec="BUILD", conf="MEDIUM", ec="SRC", a4="No DAG or organisation search", jw="No AFlow/ADAS equivalent",
  ev="No graph-structure optimizer found in either tree", miss="DAG and agent organisation evolution",
  acc="A plan template improves measurably across runs")
R("FN-25", dec="ADAPT", conf="MEDIUM", ec="SRC", a4="Hard policy checker in gepa_optimizer",
  jw="agent_evolving evaluator/metrics provides exact_match and llm_as_judge",
  ev="AI4Research integrations/gepa_optimizer/hard_policy_checker.py; openjiuwen agent_evolving/evaluator/metrics",
  miss="Evaluator, reward and contract evolution under a frozen-policy guard",
  acc="A candidate that relaxes a frozen policy is rejected before evaluation")
R("FN-26", dec="BUILD", conf="MEDIUM", ec="SRC", a4="Evidence ledger exists; no retrieval learning",
  jw="GraphMemory exists in openjiuwen core but is not referenced anywhere in JiuwenSwarm",
  ev="grep GraphMemory across jw-src/jiuwenswarm returns zero hits",
  miss="Memory, retrieval and evidence evolution", acc="Retrieval quality improves against a held-out set",
  graph="Memory graph")
R("FN-27", dec="DEFER", conf="MEDIUM", ec="SRC", a4="No weight training",
  jw="agent_rl provides PPO/verl-based training but is not reachable from the application",
  ev="openjiuwen agent_evolving/agent_rl present; no jiuwenswarm import of it",
  miss="Model policy and weight evolution", acc="Deferred until an owned model and a training budget exist",
  note="Deferred on cost and infrastructure grounds, not because the substrate is missing")
R("FN-28", dec="BUILD", conf="MEDIUM", ec="INF", a4="Benchmarks exist but are not curriculum-managed",
  jw="No curriculum or hard-case mining", ev="-", miss="Data, benchmark and curriculum evolution with observability",
  acc="Hard cases mined from failures enter the benchmark set", graph="Dataset graph")

R("FN-29", dec="EXTEND", conf="MEDIUM", ec="SRC", a4="Evidence and memory tooling; mempalace",
  jw="Persistent checkpointer is configured in a normal install (sqlite); context processor rail exists",
  ev="jw-src/.../interface_deep.py ensure_persistent_checkpointer creates a sqlite PersistenceCheckpointer and sets it as process default",
  miss="Research-grade retrieval over project memory", acc="Context survives a session restart and a compaction",
  note="Corrects the earlier open question about whether a persistent checkpointer exists in a stock install - it does",
  graph="Memory graph")
R("FN-30", dec="BUILD", conf="HIGH", ec="EXEC", a4="Absent", jw="GraphMemory exists in openjiuwen, unwired in JiuwenSwarm",
  ev="grep concept_graph across AI4Research lib/ and tools/ returns 0 files; grep GraphMemory across jw-src returns 0",
  miss="Concept graph as a typed projection", acc="Concepts resolve to the evidence that introduced them", graph="Concept graph")
R("FN-31", dec="BUILD", conf="HIGH", ec="EXEC", a4="Absent", jw="No dataset graph",
  ev="grep dataset_graph returns 0 files", miss="Dataset graph", acc="A dataset resolves to the experiments that used it", graph="Dataset graph")
R("FN-32", dec="BUILD", conf="HIGH", ec="EXEC", a4="Absent", jw="Code indexing exists in the coding harness, not as a graph",
  ev="grep code_graph returns 0 files", miss="Code graph", acc="Code artifacts resolve to the claims they support", graph="Code graph")
R("FN-33", dec="BUILD", conf="HIGH", ec="EXEC", a4="Absent as a graph; gate ledger holds policy decisions",
  jw="Permission engine holds runtime policy", ev="grep policy_graph returns 0 files",
  miss="Policy graph", acc="A policy decision resolves to the rule and the approver", graph="Policy graph")
R("FN-34", dec="BUILD", conf="HIGH", ec="EXEC", a4="Absent", jw="Workflow definitions exist but are not graph-indexed",
  ev="grep workflow_graph returns 0 files", miss="Workflow graph", acc="A plan resolves to the plans it was derived from", graph="Workflow graph")
R("FN-35", dec="BUILD", conf="HIGH", ec="EXEC", a4="Absent as a graph; traces exist in run logs",
  jw="Observability spans exist", ev="grep trace_graph returns 0 files", miss="Trace graph",
  acc="A result resolves to the exact execution that produced it", graph="Trace graph")
R("FN-36", dec="BUILD", conf="HIGH", ec="EXEC", a4="Absent", jw="GraphMemory exists in openjiuwen, unwired",
  ev="grep memory_graph returns 0 files in AI4RnD; 0 GraphMemory references in JiuwenSwarm",
  miss="Memory graph", acc="Memory entries carry provenance and can be revoked", graph="Memory graph")
R("FN-37", dec="ADAPT", conf="HIGH", ec="SRC", a4="task_graph_io.py and task_graph_state_io.py persist TaskGraphs",
  jw="Checkpointer persists session and graph state; SwarmFlow journal persists call results",
  ev="AI4Research lib/task_graph_io.py, lib/task_graph_state_io.py; openjiuwen checkpointer",
  miss="TaskGraph lifecycle that spans sessions - the SwarmFlow journal is keyed by session id",
  acc="A TaskGraph survives a session change without losing completed work",
  note="Journal path is {team}/sessions/{session_id}/workflows/{name}; a new session gets a new journal and replays nothing",
  graph="Workflow graph")

R("FN-38", dec="REUSE", conf="HIGH", ec="EXEC", a4="coordinator.sh polling state machine",
  jw="NativeHarness run lifecycle: start, pause, abort, subscribe, outputs",
  ev="openjiuwen agent_teams/harness/; SwarmFlow background task controller",
  miss="Project-level run lifecycle above the session", acc="A project run survives an agent-server restart")
R("FN-39", dec="REUSE", conf="HIGH", ec="SRC", a4="File-based message passing between panes",
  jw="Messager, topics and durable background task controller",
  ev="openjiuwen agent_teams/messager/", miss="Nothing at this layer", acc="Messages are not lost across a restart")
R("FN-40", dec="ADAPT", conf="HIGH", ec="EXEC", a4="graph_scheduler.py (4,189 LOC) performs readiness, ordering and binding",
  jw="Pregel supersteps compute ready nodes; Core Workflow validates connections; conditional routers accept a runtime-computed target list",
  ev="probe_r4: add_conditional_connection accepted a router returning a computed list and the run completed",
  miss="Capability binding at node level - the part Pregel does not do",
  acc="A plan compiles to a runnable graph and unbound nodes stall rather than defaulting",
  note="Router is invoked with no arguments, so fan-out width must be computed from a closure or channel read, not from a router parameter",
  slices=["Readiness, ordering, batching - OpenJiuwen Runtime, REUSE",
          "Capability binding per node - AI4RnD Core, BUILD",
          "Plan to graph compilation - AI4RnD-Jiuwen Integration, BUILD"])
R("FN-41", dec="REUSE", conf="HIGH", ec="EXEC", a4="Concurrency policy JSON",
  jw="ConcurrencyGovernor admits workflows and caps agents per run; admission refusal is explicit",
  ev="probe_r1: invoke returned 'Swarmflow concurrency governor is not configured' - admission is a hard precondition",
  miss="Nothing at this layer", acc="Exceeding the concurrency limit refuses with a stated limit, not a queue stall")
R("FN-42", dec="REUSE", conf="HIGH", ec="SRC", a4="Main loop in coordinator.sh",
  jw="Pregel superstep dispatch and the harness main loop", ev="openjiuwen core/graph/pregel/",
  miss="Nothing at this layer", acc="Supervision restarts a failed node without restarting the run")
R("FN-43", dec="ADAPT", conf="HIGH", ec="EXEC",
  a4="Retry and resume in graph_scheduler",
  jw="Journal replay works: an interrupted run resumed with only the failed step re-executed, and a third run replayed with zero live calls",
  ev="probe_r2 run2 executed only step-B; run3 executed nothing",
  miss="Reachable resume - the leader-facing swarmflow tool advertises resume_id and then rejects it, and a failed step returns None instead of failing the run",
  acc="A resumed run re-executes only unfinished work, and a failed step blocks its gate rather than yielding None",
  note="Two verified defects: resume_id is schema-advertised but unimplemented, and agent failure degrades to None after retries",
  pclass="sched_risk",
  slices=["Journal replay - OpenJiuwen Runtime, REUSE",
          "Resume trigger reachable from the control plane - AI4RnD-Jiuwen Integration, BUILD",
          "Failed-step detection and gate blocking - AI4RnD Core, BUILD"])

R("FN-44", dec="ADAPT", conf="MEDIUM", ec="SRC", a4="Intent classification in the harness intent engine",
  jw="WorkflowController.intent_detection routes between execution strategies",
  ev="AI4Research lib/intent_engine_adapter.py; openjiuwen workflow_controller.py",
  miss="Compilation variant selection distinct from routing", acc="The chosen compilation variant is recorded and inspectable")
R("FN-45", dec="ADAPT", conf="MEDIUM", ec="SRC", a4="Goal and scope handling in the requirement compiler",
  jw="Session context provides scope", ev="AI4Research lib/research/deepdive_requirement_compiler.py",
  miss="Normalisation to a canonical Contract shape", acc="Two phrasings of one goal normalise identically")
R("FN-46", dec="ADAPT", conf="MEDIUM", ec="SRC", a4="Ambiguity handling present", jw="Interrupt mechanism available",
  ev="openjiuwen workflow_config handle_type='interrupt'", miss="Readiness as a checkable state",
  acc="A Contract reports ready or not-ready with reasons")
R("FN-47", dec="BUILD", conf="MEDIUM", ec="INF", a4="Constraints captured informally", jw="None at the research layer",
  ev="-", miss="Constraint compilation into executable checks", acc="Every constraint compiles to a check or is rejected")
R("FN-48", dec="ADAPT", conf="HIGH", ec="EXEC", a4="Capsule contracts show the shape; project Contract absent",
  jw="None", ev="42/42 manifests carry contract.inputs/outputs/pre/post/invariants",
  miss="Project-level Task Contract with acceptance compilation", acc="Acceptance criteria are machine-checkable before work starts")

R("FN-49", dec="ADAPT", conf="MEDIUM", ec="SRC", a4="Decomposition inside graph_scheduler and survey planner",
  jw="None at the research layer", ev="AI4Research lib/research/survey/planner.py",
  miss="Decomposition driven by the Contract", acc="Every task traces to a Contract clause")
R("FN-50", dec="ADAPT", conf="HIGH", ec="SRC", a4="TaskGraph construction in graph_scheduler (4,189 LOC)",
  jw="Core Workflow and Pregel construct executable graphs",
  ev="AI4Research lib/graph_scheduler.py; openjiuwen core/graph/",
  miss="Separation of the logical plan from the runtime graph", acc="A plan is inspectable before any execution begins",
  graph="Workflow graph")
R("FN-51", dec="ADAPT", conf="HIGH", ec="EXEC", a4="Validation in graph_scheduler (cycles, missing deps, duplicates)",
  jw="Pregel validates node ids and forward reachability; Core Workflow validates connections",
  ev="probe_r4 built and ran a conditional fan-out graph; openjiuwen graph validation",
  miss="Feasibility analysis against available capabilities", acc="A plan requiring an unavailable capability fails validation")

R("FN-52", dec="BUILD", conf="MEDIUM", ec="INF", a4="Build contracts implicit", jw="None", ev="-",
  miss="Build Contract interpretation", acc="A build states its acceptance before it starts")
R("FN-53", dec="REUSE", conf="HIGH", ec="SRC", a4="Environment scripts", jw="Worktree manager + jiuwenbox",
  ev="openjiuwen agent_teams/worktree.py", miss="Preparation driven by declared effects", acc="Build environments match the declared effects")
R("FN-54", dec="REUSE", conf="HIGH", ec="SRC", a4="Code agents", jw="Code mode with worktree isolation",
  ev="agent(options={'isolation':'worktree'}) accepted by the engine option whitelist",
  miss="Construction bound to a Build Contract", acc="Concurrent builds never share a worktree", graph="Code graph")
R("FN-55", dec="DEFER", conf="LOW", ec="INF", a4="No model construction", jw="agent_rl exists but is unreachable from the app",
  ev="openjiuwen agent_evolving/agent_rl present, no application import",
  miss="Model construction pipeline", acc="Deferred with RSI-7", phase="P6")
R("FN-56", dec="BUILD", conf="MEDIUM", ec="INF", a4="Experiment assets built ad hoc", jw="None", ev="-",
  miss="Experimental asset construction as a declared step", acc="Experiment assets are reproducible from their record", graph="Dataset graph")
R("FN-57", dec="PORT", conf="MEDIUM", ec="SRC", a4="Benchmark asset tooling present but unwired",
  jw="None", ev="AI4Research lib/capability_fusion_benchmark.py", miss="Wire to the benchmark lane",
  acc="Benchmark assets version with the benchmark protocol", graph="Dataset graph")
R("FN-58", dec="BUILD", conf="MEDIUM", ec="INF", a4="Verification assets implicit", jw="None", ev="-",
  miss="Verification asset construction", acc="Every claim has a verification asset")
R("FN-59", dec="BUILD", conf="MEDIUM", ec="INF", a4="Decision artifacts produced as prose", jw="None", ev="-",
  miss="Decision artifact schema", acc="A decision artifact states the evidence and the alternative rejected")
R("FN-60", dec="BUILD", conf="MEDIUM", ec="INF", a4="Prototype assembly ad hoc", jw="Worktree + code mode",
  ev="openjiuwen worktree manager", miss="Assembly as a declared step with acceptance", acc="An assembled prototype passes readiness validation")
R("FN-61", dec="BUILD", conf="LOW", ec="INF", a4="No product integration stage", jw="None", ev="-",
  miss="Product integration", acc="Integration into a target product is recorded and reversible")
R("FN-62", dec="REUSE", conf="MEDIUM", ec="SRC", a4="Defect repair via coding agents", jw="Code mode with tests",
  ev="openjiuwen code mode + worktree", miss="Repair bound to a recorded defect", acc="A repair references the defect it closes")
R("FN-63", dec="PORT", conf="HIGH", ec="EXEC", a4="Build evidence generation in the evidence ledger",
  jw="Observability spans", ev="AI4Research lib/evidence_ledger.py executed standalone",
  miss="Build evidence linked to the Build Contract", acc="Every build produces evidence sufficient to re-run it", graph="Trace graph")
R("FN-64", dec="PORT", conf="MEDIUM", ec="SRC", a4="Report and publication capsules exist",
  jw="None", ev="AI4Research cap.research-report-draft.yaml, cap.research-publication-produce.yaml",
  miss="Deliverable construction bound to the evidence ledger", acc="A report cites only ledger evidence")
R("FN-65", dec="BUILD", conf="LOW", ec="INF", a4="No runtime deliverable construction", jw="Skill packaging exists",
  ev="jw-src/jiuwenswarm/server/runtime/skill/skill_manager.py", miss="Runtime deliverable packaging",
  acc="A runtime deliverable installs and runs from its package")

# ---------------------------------------------------------------- VERTICAL (23)
R("VT-01", dec="EXTEND", conf="MEDIUM", ec="SRC", a4="Status server and dashboards",
  jw="Web UI shows session and task status", ev="jw-src/jiuwenswarm/gateway/channel_manager/web/",
  miss="Research-specific progress: gates, budgets, blockers", acc="A user sees which gate a project is blocked on",
  sem="AI4RnD Core", slices=["Platform status - JiuwenSwarm Application, REUSE",
                             "Gate, budget and blocker view - AI4RnD Core, BUILD"])
R("VT-02", dec="EXTEND", conf="MEDIUM", ec="SRC", a4="Trace inspection in the harness",
  jw="Observability rail emits spans; web UI shows tool calls",
  ev="openjiuwen observability rail", miss="Search across time-ordered transitions bound to claims",
  acc="A user can find the run that produced a given claim", graph="Trace graph")
R("VT-03", dec="BUILD", conf="MEDIUM", ec="INF", a4="Runtime stats in the status server",
  jw="No CPU/GPU statistics surface", ev="-", miss="Host resource statistics", acc="CPU and GPU utilisation are visible per run")
R("VT-04", dec="EXTEND", conf="MEDIUM", ec="SRC", a4="Cost tracking in harness tooling",
  jw="Token budget accounting in the workflow engine", ev="openjiuwen workflow engine budget_total",
  miss="Cost and capacity against a project budget", acc="A project halts when its budget is exhausted")
R("VT-05", dec="REUSE", conf="MEDIUM", ec="DOC", a4="Windows support not claimed",
  jw="Packaging and installer exist", ev="jw-src/deploy/, install scripts",
  miss="Research mode included in the package", acc="A clean Windows install launches into research mode")
R("VT-06", dec="REUSE", conf="MEDIUM", ec="DOC", a4="macOS install scripts present (install.sh, get-solar.sh)",
  jw="Packaging exists", ev="AI4Research install.sh; jw-src/deploy/", miss="Single installer for the combined product",
  acc="A clean macOS install launches into research mode")
R("VT-07", dec="REUSE", conf="MEDIUM", ec="DOC", a4="CLI present (bin/)", jw="jiuwenswarm CLI exists",
  ev="jw-src/jiuwenswarm/ CLI entry points", miss="Research commands in the CLI", acc="A project can be started and inspected from the CLI")
R("VT-08", dec="REUSE", conf="MEDIUM", ec="DOC", a4="Linux CLI present", jw="jiuwenswarm CLI exists",
  ev="jw-src CLI entry points", miss="Research commands in the CLI", acc="Same as VT-07 on Linux")
R("VT-09", dec="REUSE", conf="HIGH", ec="SRC", a4="Status server present",
  jw="Web application and gateway are the product's primary surface",
  ev="jw-src/jiuwenswarm/gateway/channel_manager/web/", miss="Project routes", acc="The project view is reachable from the web app")
R("VT-10", dec="REUSE", conf="MEDIUM", ec="DOC", a4="CLI present", jw="CLI present", ev="jw-src CLI",
  miss="Nothing beyond VT-07", acc="Covered by VT-07")
R("VT-11", dec="EXTEND", conf="HIGH", ec="SRC", a4="Web UI prototype in the AI4Research repository",
  jw="Web UI with session, skills and settings", ev="jw-src/jiuwenswarm/gateway/channel_manager/web/",
  miss="Project view, plan inspector, evidence browser, improvements inbox",
  acc="A user can run a project end to end without the CLI")
R("VT-12", dec="REUSE", conf="MEDIUM", ec="DOC", a4="tmux cockpit is the current TUI",
  jw="jiuwenswarm-tui package exists", ev="jw-src/packages/jiuwenswarm-tui/",
  miss="Research views in the TUI", acc="Project status is visible in the TUI")
R("VT-13", dec="BUILD", conf="HIGH", ec="EXEC", a4="Absent - no account registration in the repository",
  jw="No account registration; sessions are not user accounts",
  ev="grep account_registration across AI4Research returns 0 files",
  miss="The whole account subsystem", acc="A user can register and the account owns their projects")
R("VT-14", dec="BUILD", conf="HIGH", ec="EXEC", a4="Absent", jw="No authentication tier for end users",
  ev="No authentication module found in either tree at the product layer",
  miss="Authentication and session security", acc="Sessions cannot be assumed by another user",
  note="Explicitly out of scope for verification here - the safeguards forbid touching authentication")
R("VT-15", dec="BUILD", conf="HIGH", ec="INF", a4="Absent", jw="Absent", ev="-",
  miss="User profile management", acc="A profile persists across installs")
R("VT-16", dec="BUILD", conf="HIGH", ec="INF", a4="Absent", jw="Absent", ev="-",
  miss="Privacy and personal data controls", acc="A user can export and delete their data")
R("VT-17", dec="REUSE", conf="HIGH", ec="SRC", a4="Not present", jw="WeChat is one of the nine supported channels",
  ev="jw-src/jiuwenswarm/gateway/channel_manager/", miss="Project notifications on the channel",
  acc="A gate decision can be approved from WeChat")
R("VT-18", dec="REUSE", conf="HIGH", ec="SRC", a4="Not present", jw="Discord is a supported channel",
  ev="jw-src/jiuwenswarm/gateway/channel_manager/", miss="Project notifications", acc="Same as VT-17 on Discord")
R("VT-19", dec="PORT", conf="HIGH", ec="SRC", a4="tmux is the current AI4RnD carrier",
  jw="No tmux channel", ev="AI4Research harness tmux cockpit and coordinator.sh",
  miss="Decide whether tmux remains a channel or is retired with the cockpit",
  acc="Either tmux is a registered channel or its retirement is recorded",
  note="Open question: the workbook lists TMUX as a message channel, but the recommended architecture retires the tmux carrier",
  pclass="unresolved")
R("VT-20", dec="REUSE", conf="HIGH", ec="SRC", a4="Model config in harness config",
  jw="Model pool and provider configuration in settings", ev="openjiuwen agent_teams/models/allocator.py",
  miss="Research-specific model policy", acc="Model configuration is a single surface")
R("VT-21", dec="REUSE", conf="MEDIUM", ec="SRC", a4="Settings in config/", jw="User settings in the web UI",
  ev="jw-src/jiuwenswarm/resources/config.yaml", miss="Research preferences", acc="Settings persist across restarts")
R("VT-22", dec="EXTEND", conf="MEDIUM", ec="SRC", a4="Budget policy in concurrency-policy.json",
  jw="Token budget accounting exists; no user-facing budget settings",
  ev="openjiuwen workflow engine budget_total", miss="Budget settings surface and enforcement per project",
  acc="A project cannot exceed its configured budget")
R("VT-23", dec="UNRESOLVED", conf="LOW", ec="INF", a4="actor-hosts.json describes a host fleet",
  jw="Distributed team configuration exists (config.team.distributed.*.yaml)",
  ev="jw-src/jiuwenswarm/resources/config.team.distributed.leader.yaml",
  miss="Cluster semantics for the combined product are undefined",
  acc="Unresolved - the workbook does not state what a cluster owns",
  note="Genuinely unresolved: 'Cluster setting' is one line in the workbook with no description of scope",
  sem="Unresolved", run="Unresolved", pclass="unresolved")


# ------------------------------------------------------- preservation-gate rules
# For each preservation class, the verdict under each complete-product option.
# P = PRESERVED, A = PRESERVED WITH ADAPTATION, N = NEW BUILD REQUIRED,
# U = UNRESOLVED, D = DROPPED.
PRESERVE_RULES = {
  #                       A    B    C    D    E
  "app":        dict(A="P", B="P", C="P", D="P", E="P"),
  "app_sem":    dict(A="P", B="P", C="P", D="A", E="P"),
  "sem":        dict(A="P", B="P", C="P", D="P", E="P"),
  "sem_exec":   dict(A="A", B="P", C="P", D="A", E="P"),
  "sched":      dict(A="P", B="A", C="A", D="A", E="P"),
  "sched_risk": dict(A="P", B="A", C="A", D="U", E="P"),
  "route":      dict(A="P", B="A", C="A", D="D", E="P"),
  "rsi":        dict(A="N", B="N", C="N", D="N", E="N"),
  "data":       dict(A="N", B="N", C="N", D="N", E="N"),
  "absent":     dict(A="N", B="N", C="N", D="N", E="N"),
  "unresolved": dict(A="U", B="U", C="U", D="U", E="U"),
}

# Rows whose decision is BUILD always require new build work regardless of class,
# because nothing exists to preserve. Applied after the class rule.
BUILD_FORCES_NEW = True

OPTIONS = {
 "A": ("AI4RnD-led control plane on Jiuwen execution",
       "AI4RnD keeps its TaskGraph, scheduler, Contracts, Capsules, evidence and gates; "
       "Jiuwen adapters replace physical execution only."),
 "B": ("Jiuwen-native lifecycle with AI4RnD semantic control",
       "Core Workflow provides the persistent outer R&D lifecycle; AI4RnD keeps project TaskGraphs, "
       "Capsules, Contracts, evidence and RSI; Jiuwen mechanisms execute stages."),
 "C": ("Progressive TaskGraph compilation into Jiuwen",
       "AI4RnD keeps semantic planning and governance; low-level scheduling migrates into "
       "SwarmFlow and Core Workflow only as compatibility evidence accumulates."),
 "D": ("Full compilation into Jiuwen execution",
       "AI4RnD keeps product semantics and removes most of its execution scheduler."),
 "E": ("Standalone AI4RnD baseline or defer",
       "Keep the current implementation where Jiuwen integration does not yet add value or safety."),
}
