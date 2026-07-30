#!/usr/bin/env python3
# coding: utf-8
"""Generate low-level-design.html — the fine-granularity design document.

Self-contained: inline CSS (light/dark via CSS variables), inline SVG diagrams,
no external assets, no JS beyond the theme toggle. Every fact drawn here was
source- or execution-verified in adversarial-review.md; line references point
at jiuwenswarm a98d7ad / openjiuwen 0.1.15.post3 / AI4Research d35c511.
"""
from __future__ import annotations

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
W = 1120


# ---------------------------------------------------------------- SVG helper
class D:
    """Theme-aware SVG: every colour is a CSS variable set by the page."""

    def __init__(self, height: int, title: str):
        self.h = height
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" '
            f'width="{W}" font-family="inherit" role="img" aria-label="{escape(title)}">',
            '<defs><marker id="lva" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
            'markerHeight="7" orient="auto-start-reverse">'
            '<path d="M0 0L10 5L0 10z" fill="var(--lv-line)"/></marker></defs>',
        ]

    def text(self, x, y, s, cls="s", anchor=None):
        a = f' text-anchor="{anchor}"' if anchor else ""
        fills = {"h": "var(--lv-ink)", "n": "var(--lv-ink)", "s": "var(--lv-sub)",
                 "m": "var(--lv-muted)", "tag": "var(--lv-muted)", "warn": "var(--lv-red-ink)",
                 "ok": "var(--lv-green-ink)"}
        sizes = {"h": 15, "n": 12.5, "s": 10.5, "m": 11, "tag": 9.5, "warn": 10.5, "ok": 10.5}
        weights = {"h": ' font-weight="700"', "n": ' font-weight="700"',
                   "tag": ' font-weight="700" letter-spacing=".05em"', "warn": ' font-weight="600"'}
        self.parts.append(
            f'<text x="{x}" y="{y}" font-size="{sizes.get(cls,10.5)}" '
            f'fill="{fills.get(cls,"var(--lv-sub)")}"{weights.get(cls,"")}{a}>{escape(s)}</text>')

    def lines(self, x, y, rows, cls="s", gap=16):
        for i, r in enumerate(rows):
            self.text(x, y + i * gap, r, cls)

    def rect(self, x, y, w, h, fill="var(--lv-surface)", stroke="var(--lv-line)",
             rx=8, dashed=False, sw=1.1):
        d = ' stroke-dasharray="5 4"' if dashed else ""
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
                          f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def panel(self, x, y, w, h, title, subtitle="", tone="gray", dashed=False):
        self.rect(x, y, w, h, f"var(--lv-{tone})", f"var(--lv-{tone}-s)", rx=12, dashed=dashed, sw=1.2)
        self.text(x + 16, y + 25, title, "h")
        if subtitle:
            self.text(x + 16, y + 44, subtitle, "m")

    def node(self, x, y, w, h, title, rows=(), tag=None, dashed=False, tone=None):
        fill = f"var(--lv-{tone})" if tone else "var(--lv-surface)"
        self.rect(x, y, w, h, fill, "var(--lv-line)", rx=7, dashed=dashed)
        self.text(x + 11, y + 21, title, "n")
        self.lines(x + 11, y + 39, rows, "s", 15.5)
        if tag:
            self.text(x + w - 9, y + 15, tag, "tag", anchor="end")

    def warn(self, x, y, w, rows, h=None):
        h = h or (16 + 16 * len(rows))
        self.rect(x, y, w, h, "var(--lv-red)", "var(--lv-red-s)", rx=7)
        self.lines(x + 12, y + 19, rows, "warn", 16)

    def note(self, x, y, w, rows, h=None, tone="yellow"):
        h = h or (16 + 16 * len(rows))
        self.rect(x, y, w, h, f"var(--lv-{tone})", f"var(--lv-{tone}-s)", rx=7)
        self.lines(x + 12, y + 19, rows, "s", 16)

    def arrow(self, d, dashed=False):
        dd = ' stroke-dasharray="5 4"' if dashed else ""
        self.parts.append(f'<path d="{d}" fill="none" stroke="var(--lv-line)" '
                          f'stroke-width="1.6"{dd} marker-end="url(#lva)"/>')

    def out(self):
        return "\n".join(self.parts) + "\n</svg>"


# ------------------------------------------------- diagram 1: OpenJiuwen runtime
def dg_openjiuwen():
    s = D(2120, "OpenJiuwen runtime, low level")

    # A — request resolution + construction
    s.panel(8, 8, W - 16, 320, "A. Request resolution and agent construction",
            "Exact classes on the path from an IM message to a live DeepAgent", "blue")
    row = [
        ("Channel adapter", ("9 IM channels", "message + identity"), "jiuwenswarm"),
        ("Gateway", ("app_gateway.py", "E2A envelope", "route + session"), "jiuwenswarm"),
        ("AgentServer", ("app_agentserver.py", "WS entrypoint", "extensions load"), "jiuwenswarm"),
        ("agent_manager", ("server/runtime/", "agent_manager.py", "load/rebuild · bind session"), "jiuwenswarm"),
        ("Invocation ctx", ("request · mode", "workspace", "permissions"), "jiuwenswarm"),
    ]
    for i, (t, b, tag) in enumerate(row):
        s.node(28 + i * 216, 62, 196, 96, t, b, tag=tag)
        if i:
            s.arrow(f"M{28 + i * 216 - 20} 110 H{28 + i * 216 - 4}")
    row2 = [
        ("DeepAgentSpec", ("deep_agent_spec.py:427", "model · prompt · tools", "Rails · skills · policy")),
        ("BuildContext", ("build_context.py:27", "derive() :51", "from_seed() :92")),
        ("resolve_parts()", ("deep_agent_spec.py:479", "registries resolved", "Rail instances")),
        ("DeepAgentConfig", ("harness/schema/", "config.py:163", "live references")),
        ("DeepAgent", ("harness/deep_agent.py", "built by .build()", "spec.build() :561")),
    ]
    for i, (t, b) in enumerate(row2):
        s.node(28 + i * 216, 186, 196, 96, t, b, tag="openjiuwen")
        if i:
            s.arrow(f"M{28 + i * 216 - 20} 234 H{28 + i * 216 - 4}")
    s.arrow("M126 158 V186")
    s.text(28, 312, "BuildContext carries the cross-process rebuild seed: definitions travel; process-local resources are re-resolved.", "m")

    # B — invocation with exact callback order
    s.panel(8, 348, 764, 866, "B. One invocation — exact callback order",
            "AgentCallbackEvent (core/single_agent/rail/base.py:214-224), fire sites in react_agent.py", "sand")
    steps = [
        ("1 · invoke()", ["ctx.lifecycle(BEFORE_INVOKE … AFTER_INVOKE)  base.py:382",
                          "lifecycle guarantees AFTER_INVOKE on every exit path"]),
        ("2 · outer task iteration", ["fires BEFORE_TASK_ITERATION",
                                      "budget, cancellation, follow-up, prior session state"]),
        ("3 · assemble model context", ["system prompt + history + skill guidance",
                                        "+ memory + ability cards"]),
        ("4 · model call", ["BEFORE_MODEL_CALL → allocator → provider client",
                            "→ AFTER_MODEL_CALL | ON_MODEL_EXCEPTION  react_agent.py:718-720"]),
        ("5 · parse response", ["plain text may finish the ReAct turn",
                                "tool requests enter the ability path (band C)"]),
        ("6 · execute abilities", ["per tool call: band C pipeline",
                                   "ToolMessage or typed exception appended"]),
        ("7 · AFTER_REACT_ITERATION", ["fired at react_agent.py:1818",
                                       "success-only: never fired on a break path  base.py:200-202"]),
        ("8 · decide", ["continue ReAct · finish task iteration (AFTER_TASK_ITERATION)",
                        "interrupt · fail → AFTER_INVOKE"]),
    ]
    y = 404
    for t, rows in steps:
        s.node(30, y, 716, 74, t, rows)
        if y > 404:
            s.arrow(f"M388 {y - 22} V{y - 4}")
        y += 96
    s.arrow("M746 918 C 778 918 778 500 746 500", dashed=True)
    s.text(780, 700, "next", "tag", anchor="end")
    s.text(780, 712, "ReAct", "tag", anchor="end")
    s.text(780, 724, "turn", "tag", anchor="end")
    s.warn(30, y - 12, 716, [
        "Verified hazard: resolve_member_model (agent_teams/models/allocator.py:387-423) returns None for a",
        "missing pool group and the caller proceeds on the default model — a silent fallback. Fix before reuse.",
    ])

    # B' — control surfaces
    s.panel(788, 348, 324, 866, "Control surfaces",
            "AgentCallbackContext base.py:231", "purple")
    s.node(806, 410, 288, 88, "Retry", (
        "request_retry(delay)  :278", "consume_retry_request  :293", "RetryRequest  :166"))
    s.node(806, 514, 288, 88, "Force finish", (
        "request_force_finish(result) :299", "consume_force_finish  :308", "ForceFinishRequest  :173"))
    s.node(806, 618, 288, 104, "Steering", (
        "bind_steering_queue  :321", "push_steering  :336", "drain_steering  :347",
        "has_pending_steering  :366"))
    s.node(806, 738, 288, 104, "Rail surface (ABC)", (
        "AgentRail  base.py:456", "10 overridables, exactly the", "callback enum minus", "AFTER_REACT_ITERATION*"))
    s.text(806, 862, "*ReAct-iteration Rails subscribe via", "m")
    s.text(806, 878, "get_callbacks() :549 — no before-", "m")
    s.text(806, 894, "ReAct hook exists; per-iteration", "m")
    s.text(806, 910, "pre-checks must ride BEFORE_MODEL_CALL.", "m")
    s.node(806, 934, 288, 104, "Run heartbeats", (
        "RunKind  base.py:43", "HeartbeatReason  :50", "InvokeInputs.is_heartbeat :88",
        "is_cron :98 · lightweight :92"))
    s.node(806, 1054, 288, 88, "Typed inputs per event", (
        "ModelCallInputs  :104", "ToolCallInputs  :120", "TaskIterationInputs  :138"))

    # C — ability pipeline
    s.panel(8, 1234, W - 16, 258, "C. Ability path — one tool call, exact order",
            "Permission enforcement is itself a before-tool Rail, not a separate engine stage", "green")
    abil = [
        ("before_tool_call Rails", ("ordered Rail list;", "SysOperationRail auto-", "prepended factory.py:119")),
        ("ToolSecurityRail", ("harness/rails/security/", "tool_security_rail.py", "argument + policy checks")),
        ("check_permission", ("harness/security/", "core.py:145", "tiered policy :508")),
        ("ALLOW | ASK | DENY", ("PermissionLevel", "models.py:26-28", "ASK routes to human")),
        ("Resource runner", ("Tool · MCP · sub-agent", "workflow · SysOperation", "core/sys_operation")),
        ("Result", ("ToolMessage or typed", "exception → after_tool_call", "| on_tool_exception")),
    ]
    for i, (t, b) in enumerate(abil):
        s.node(24 + i * 182, 1296, 168, 96, t, b)
        if i:
            s.arrow(f"M{24 + i * 182 - 14} 1344 H{24 + i * 182 - 2}")
    s.warn(24, 1408, 1072, [
        "Verified hazard: in the JiuwenSwarm layout the tiered-policy loader (harness/security/tiered_policy.py) resolves builtin rules from the",
        "package path only — resources/builtin_rules.yaml is written by common/utils.py + init_workspace.py and read by nothing: 0 rules load.",
    ])

    # D — mechanism internals
    s.panel(8, 1512, W - 16, 400, "D. Orchestration mechanisms — internals and sharp edges",
            "What each scheduler actually calls, persists and returns", "cyan")
    s.node(24, 1574, 356, 210, "Core Workflow / Pregel", (
        "core/workflow/workflow.py",
        "Workflow.invoke(inputs, session)",
        "add_conditional_connection(src, router)",
        "Router = Callable[..., Hashable|list]",
        "router is invoked with NO arguments",
        "WorkflowComponent: invoke + add_component",
        "durability: checkpointer snapshots",
        "returns: graph outputs · interrupt state"))
    s.node(396, 1574, 356, 210, "SwarmFlow", (
        "agent_teams/workflow/  engine:",
        "run_workflow(path, args, backend,",
        "  resume, journal_path, …)",
        "AgentBackend.run(prompt, opts, schema)",
        "→ AgentResult(text, structured,",
        "  tokens, skipped)",
        "journal key: {team}/sessions/{sid}/",
        "  workflows/{name} · ConcurrencyGovernor"))
    s.node(768, 1574, 328, 210, "Dynamic Team / NativeHarness", (
        "agent_teams/harness/native_harness.py",
        "TeamRole: WORKER · HUMAN_AGENT ·",
        "  BRIDGE_AGENT · …",
        "task board tools/tool_task.py:",
        "  depends_on · add_blocked_by ·",
        "  task_manager.add_dependencies",
        "reliability detectors + remediation",
        "durability: team task DB + worktrees"))
    s.warn(24, 1800, 1072, [
        "Verified hazards (executed probes): a SwarmFlow step that fails rt.retries+1 times makes agent() return None while the run reports",
        "SUCCESS, and the journal replays the None; SwarmflowTool rejects resume_id/name (\"not supported yet\") — resume is engine-API-only;",
        "unknown engine options fail loudly (allowed: agent_type · isolation · label · model · phase · schema · timeout). Typos fail loudly;",
        "unimplemented features fail silently — adapters must validate results, not trust run status.",
    ], h=84)

    # E — state
    s.panel(8, 1932, W - 16, 176, "E. State actually written",
            "Operational state is split; none of it is AI4RnD evidence by itself", "gray")
    stores = [
        ("Session", ("sqlite by default:", "ensure_persistent_", "checkpointer()", "interface_deep.py")),
        ("Engine checkpoint", ("Pregel snapshots", "SwarmFlow journal/WAL", "resume replays steps", "including None results")),
        ("Team task DB", ("assignees · reviewers", "dependencies · status", "member worktrees", "")),
        ("Workspace", ("private · team", "worktree · sandbox", "SysOperation modes", "")),
        ("Memory", ("long-term · coding", "team memory", "retrieval indices", "")),
    ]
    for i, (t, b) in enumerate(stores):
        s.node(24 + i * 220, 1994, 200, 96, t, [x for x in b if x])
    return s.out()


# ---------------------------------------------------- diagram 2: AI4RnD as-is
def dg_ai4rnd():
    s = D(2410, "AI4RnD as-is, low level")

    # A — intake / coordinator
    s.panel(8, 8, W - 16, 210, "A. Intake, coordinator and plan — as-is",
            "graph_scheduler.py (4,189 LOC) + graph_node_dispatcher.py (~7,900 LOC)", "blue")
    arow = [
        ("Run intake", ("objective · repo/workspace", "budget · mode hints", "sprint scaffold")),
        ("Coordinator roles", ("PM·产品经理 → Planner·规划者", "→ Builder·建设者 → Evaluator·审判官", "role regexes dispatcher:7104")),
        ("Lifecycle控制", ("retry · timeout", "quarantine + one-shot human", "resume  scheduler:2724")),
        ("TaskGraph", ("task_graph_io.py", "DAG · topo layers · readiness", "write scope + evidence owed")),
    ]
    for i, (t, b) in enumerate(arow):
        s.node(24 + i * 272, 66, 252, 104, t, b)
        if i:
            s.arrow(f"M{24 + i * 272 - 20} 118 H{24 + i * 272 - 2}")
    s.text(24, 198, "Batch safety: ready nodes co-run only when dependencies, write scopes, effects and resources are compatible.", "m")

    # B — capsule resolution chain
    s.panel(8, 238, W - 16, 396, "B. Capsule resolution — the seven checks, in code order",
            "resolve_capability_capsule_for_task, capability_capsules.py:1246-1338 — every failure is an honest stall with a typed reason", "purple")
    checks = [
        ("1 · candidate admission", ("rank_capsule_candidates", "empty → CapsuleResolutionError", "“admission_failed: no capability", "capsule candidate”  :1273")),
        ("2 · preconditions", ("_check_preconditions(task,", "manifest) → admission_failed:", "<failed assertions>  :1281-1283", "")),
        ("3 · operator deny-list", ("operator_compatibility.forbidden", "operator_id in forbidden →", "“operator_incompatible: <id>”", ":1286-1287")),
        ("4 · attach guard capsules", ("_attach_referenced_capsules(", "required_guard_capsules,", "kind=guard)  :1290-1294", "")),
        ("5 · attach resource capsules", ("_attach_referenced_capsules(", "required_resource_capsules,", "kind=resource)  :1295-1299", "")),
        ("6 · secrets / effects policy", ("secret_refs w/o guard →", "“policy_blocked” :1302-1303", "high-risk effects w/o guard →", "“effect_escalation_requires_human”")),
        ("7 · bindings + verifier", ("_resolve_bindings → skills, MCP", "verifier required w/o pass_conds →", "“policy_blocked: verifier required", "but no pass_conditions” :1310-1311")),
        ("Resolution record", ("selected_skills · resolved_mcp_", "bindings · attached guards/resources", "effect_summary · verification_hooks", "operator_constraints")),
    ]
    for i, (t, b) in enumerate(checks):
        x = 24 + (i % 4) * 272
        y = 296 + (i // 4) * 128
        s.node(x, y, 252, 112, t, [r for r in b if r])
        if i % 4:
            s.arrow(f"M{x - 20} {y + 56} H{x - 2}")
    s.arrow("M840 408 C 900 430 300 400 276 424", dashed=True)
    s.warn(24, 560, 1072, [
        "As-is pin: operator_constraints carries registry default_operator_profile (e.g. mini-claude-sonnet-builder-2) — an identity-pinned",
        "executor default that the to-be template forbids; migration must relocate it to the Physical Operator registry.",
    ])

    # C — worker assignment
    s.panel(8, 654, W - 16, 208, "C. Worker assignment — as-is",
            "Hard admission first; scoring only among qualified candidates", "green")
    crow = [
        ("Busy classification", ("_worker_busy :1937-1938", "status ∈ busy·leased·running", "pane markers")),
        ("Pane conflict marking", ("_workers_with_used_panes_", "marked_busy :2422-2430", "per-batch copies")),
        ("assign_workers loop", ("scheduler:2490 per node", "capabilities · role · quota ·", "health · capacity")),
        ("No qualified worker", ("reason = “no_matching_worker”", ":2386 — node strands honestly,", "run does not lie")),
    ]
    for i, (t, b) in enumerate(crow):
        s.node(24 + i * 272, 712, 252, 104, t, b)
        if i:
            s.arrow(f"M{24 + i * 272 - 20} 764 H{24 + i * 272 - 2}")
    s.text(24, 842, "Capsule-backed nodes reach this path too: enrichment seams at scheduler:2151 and :2253 exist precisely to stop them stranding.", "m")

    # D — physical carrier
    s.panel(8, 882, W - 16, 250, "D. Physical carrier — runs today, rejected for the target",
            "The exact tmux mechanics the target replaces (all in graph_node_dispatcher.py)", "red")
    drow = [
        ("Pane classification", ("role/negative regexes", ":7104 · :7108 · :7180", "PM|产品经理|Planner|…")),
        ("Readiness probe", ("capture-pane + busy markers", "“Enter to confirm” patterns", ":1455 · :1644 · :7309")),
        ("Keystroke injection", ("tmux send-keys :7580 :7605", ":7825 :7948 · separate", "“Enter” send :7958")),
        ("Confirm sequences", ("(“Enter”) · (“1”,“Enter”) ·", "(“y”,“Enter”)  :7947", "2s subprocess timeouts")),
        ("Reconciliation", ("handoff mtime :3416", "artifact mtimes ≥ handoff", ":3433 · status file")),
    ]
    for i, (t, b) in enumerate(drow):
        s.node(24 + i * 218, 940, 198, 104, t, b, dashed=True)
        if i:
            s.arrow(f"M{24 + i * 218 - 20} 992 H{24 + i * 218 - 2}")
    s.note(24, 1060, 1072, [
        "Retained across replacement: typed work packet, capability decision, artifact expectations, evaluator independence",
        "(_lab_builder_can_host_evaluator :7167 keeps writers from verifying their own work).",
    ])

    # E — return path / gate ledger
    s.panel(8, 1152, W - 16, 320, "E. Return path and the gate ledger record — as-is",
            "gate_ledger.py: append-only JSONL, writer-attributed; node status is a projection", "sand")
    s.node(24, 1210, 340, 240, "append_record — gate_ledger.py:110", (
        "record_id · sid · node_id",
        "kind ∈ RECORD_KINDS",
        "author {type ∈ AUTHOR_TYPES}",
        "writer — audit key (AC-R4.3)  :21",
        "verdict · verdict_kind ∈ VERDICT_KINDS",
        "eval_generation · repair_attempt",
        "pm_task_id · evidence_snapshot_at",
        "route (for route_record kind)",
        "BEST-EFFORT: returns None on any",
        "failure — never breaks dispatch  :127"))
    s.node(384, 1210, 340, 112, "Projection, not state", (
        "project_node_status  :212",
        "read_records (malformed lines",
        "skipped)  :182",
        "corrections supersede history"))
    s.node(384, 1338, 340, 112, "Consumability", (
        "is_gate_consumable  :285",
        "latest_consumable_verdict  :316",
        "generation-scoped: stale verdicts",
        "are not consumable"))
    s.node(744, 1210, 352, 240, "Independent evaluation — as-is", (
        "worker handoff: artifacts · tests ·",
        "  claimed completion",
        "receipt: writer identity · hashes ·",
        "  attempt + timestamps",
        "evaluator: separate pane/role by",
        "  dispatcher rule :7167",
        "verdict → append_record →",
        "  projection advances the node",
        "failed verdict → new attempt or",
        "  versioned plan revision"))

    # F — evidence stores
    s.panel(8, 1492, W - 16, 262, "F. Evidence stores — four disjoint stores today",
            "No shared keys between them; the one-store-with-projections model is target, not current", "yellow")
    frow = [
        ("research SQLite", ("research/migrations/001_init.sql", "research_sources: content_hash,", "content_span · evidence_items:", "span_start/end, content_hash", "claims: stance ∈ supports/refutes/", "neutral · claim_evidence: relation ∈", "supports/refutes/qualifies")),
        ("gate ledger JSONL", ("gate_ledger.py (372 LOC)", "verdicts · transitions · routes", "writer-attributed, append-only", "sprint-co-located", "", "", "")),
        ("evidence_ledger JSONL", ("evidence_ledger.py (117 LOC)", "scheduler run entries only", "NO content hashes", "NO spans · NO claim links", "", "", "")),
        ("GEPA ArtifactStore", ("integrations/gepa_optimizer/", "RunRecord · CandidateRecord", "sha256 sidecars", "isolated from the other three", "", "", "")),
    ]
    for i, (t, b) in enumerate(frow):
        s.node(24 + i * 272, 1550, 252, 178, t, [r for r in b if r])

    # G — RSI as-is at module granularity
    s.panel(8, 1774, W - 16, 610, "G. RSI as-is — GEPA at module granularity",
            "harness/integrations/gepa_optimizer/ (~3,540 LOC) — implemented and unit-tested, wired to nothing", "purple")
    grow = [
        ("candidate_schema.py", ("CandidateType :23-30 =", "SKILL · CAPSULE ·", "ROUTING_POLICY ·", "REWRITE_RULES · COST_MODEL")),
        ("budget + stoppers", ("Budget · SpendStopper", "EvalStopper · WalltimeStopper", "PlateauStopper · StopFileStopper", "hard ceilings, not advisory")),
        ("adapter", ("GEPAAdapter wraps", "gepa.optimize_anything", "candidate in, scored", "candidate out")),
        ("hard_policy_checker", ("check_candidate:", "frozen-section diff — cannot", "relax secrets, git push,", "destructive shell, payments")),
        ("artifact_store", ("RunRecord · CandidateRecord", "content-addressed artifacts", "sha256 sidecars", "")),
        ("promoter", ("Promoter.promote / rollback", "tmp-vs-production guards", "atomic writes", "sidecar verification")),
        ("cli", ("dry-run by default", "explicit flag to touch", "production artifacts", "")),
        ("tests", ("tests/integrations/", "gepa_optimizer/ — unit level", "no scheduler / ledger imports", "anywhere in the package")),
    ]
    for i, (t, b) in enumerate(grow):
        x = 24 + (i % 4) * 272
        y = 1834 + (i // 4) * 128
        s.node(x, y, 252, 112, t, [r for r in b if r])
    s.node(24, 2098, 528, 128, "On-ramp status per improvement surface — as-is", (
        "skill / prompt-text        schema + tests          (CandidateType.SKILL)",
        "capsule                    schema only             (CandidateType.CAPSULE)",
        "routing · rewrite · cost   schema only             (three enum members)",
        "taskgraph pattern · evaluator/reward · memory ·",
        "model weights · data/benchmark      ABSENT (no candidate type)"))
    s.node(568, 2098, 528, 128, "openjiuwen agent_evolving — overlap, not replacement", (
        "Trainer requires agent.get_operators(); sole implementor:",
        "core/single_agent/agents/react_agent_evolve.py",
        "“Operator is NOT an executable unit”  core/operator/base.py",
        "JiuwenSwarm imports only EvolutionStore / experience / tool-",
        "description parts → GEPA governance (freeze/promote/rollback) stays"))
    s.warn(24, 2244, 1072, [
        "As-is verdict: no RSI loop is executable end-to-end today. GEPA candidate→check→store→promote works in isolation (unit-tested);",
        "nothing produces trajectories for it, nothing consumes its promotions, and no scheduler or ledger references it.",
    ])
    return s.out()


# --------------------------------------------- diagram 3: capsule status model
def dg_status():
    s = D(760, "Capability Capsule status model")
    s.panel(8, 8, 348, 700, "As-is — one flag",
            "What the 42 manifests + registry express", "gray")
    s.node(28, 74, 308, 96, "registry status (only axis)", (
        "capability-capsules.registry.yaml", "status ∈ {draft, stable} observed",
        "meaning: definition maturity only"))
    s.node(28, 190, 308, 96, "No runtime axis", (
        "no field records whether a capsule", "has ever executed, is bound,",
        "or is currently executable"))
    s.node(28, 306, 308, 96, "No assurance axis", (
        "“stable” carries zero evidence:", "no probe refs, no verifier record,",
        "no approval, no revocation path"))
    s.warn(28, 424, 308, [
        "Consequence: “stable” reads as", "“works” but only means “schema",
        "settled”. 30 stable entries include", "capsules that have never executed.",
    ], h=84)
    s.node(28, 530, 308, 150, "Counts (recounted from source)", (
        "42 manifests (19 + 23 dirs)", "11 universal v1 sections",
        "35 registry entries", "30 stable · 5 draft",
        "7 unregistered (3 adapter.* +", "4 cap.*) · 0 ghost entries"))

    s.panel(372, 8, 740, 700, "To-be — three independent axes",
            "Never compress definition maturity, runtime health and certification into one flag", "cyan")
    # axis 1
    s.node(392, 74, 700, 118, "registry_status — definition lifecycle (owner: registry curator)", ())
    chain1 = ["draft", "candidate", "stable", "deprecated", "retired"]
    for i, c in enumerate(chain1):
        s.rect(410 + i * 136, 116, 116, 34, "var(--lv-surface)", "var(--lv-line)", rx=17)
        s.text(468 + i * 136, 138, c, "n", anchor="middle")
        if i:
            s.arrow(f"M{410 + i * 136 - 18} 133 H{410 + i * 136 - 2}")
    s.text(410, 174, "draft: schema-valid, not planner-selectable · candidate: complete, non-production only · stable: frozen per", "s")
    s.text(410, 188, "version, selectable · deprecated: pinned in-flight runs only · retired: never selectable, history kept", "s")

    # axis 2
    s.node(392, 210, 700, 190, "runtime_status — operational health (owner: control plane, never the manifest file)", ())
    s.text(410, 252, "binding:", "n")
    for i, c in enumerate(["unbound", "bound", "unavailable"]):
        s.rect(480 + i * 150, 236, 130, 30, "var(--lv-surface)", "var(--lv-line)", rx=15)
        s.text(545 + i * 150, 256, c, "n", anchor="middle")
        if i:
            s.arrow(f"M{480 + i * 150 - 18} 251 H{480 + i * 150 - 2}")
    s.text(410, 298, "readiness:", "n")
    for i, c in enumerate(["not_proven", "runnable", "integrated", "degraded"]):
        s.rect(490 + i * 148, 282, 128, 30, "var(--lv-surface)", "var(--lv-line)", rx=15)
        s.text(554 + i * 148, 302, c, "n", anchor="middle")
        if i:
            s.arrow(f"M{490 + i * 148 - 18} 297 H{490 + i * 148 - 2}")
    s.lines(410, 336, [
        "not_proven: never executed at this version · runnable: bindings probe-executed successfully · integrated: completed",
        "inside a real TaskGraph run with receipts · degraded: recent failures over threshold — control plane demotes",
        "automatically and re-promotes on healthy probes. Stored keyed by (capsule id, version); mirrored read-only in views.",
    ], "s", 15)

    # axis 3
    s.node(392, 418, 700, 168, "assurance_status — certification (owner: independent verifier + human approver)", ())
    for i, c in enumerate(["unassessed", "tested", "verified", "certified"]):
        s.rect(410 + i * 150, 460, 130, 32, "var(--lv-surface)", "var(--lv-line)", rx=16)
        s.text(475 + i * 150, 481, c, "n", anchor="middle")
        if i:
            s.arrow(f"M{410 + i * 150 - 18} 476 H{410 + i * 150 - 2}")
    s.rect(1010, 460, 76, 32, "var(--lv-red)", "var(--lv-red-s)", rx=16)
    s.text(1048, 481, "revoked", "warn", anchor="middle")
    s.lines(410, 516, [
        "tested: self_checks pass in isolation · verified: an independent verifier accepted a real run's evidence ·",
        "certified: human approval recorded under policy_ref · revoked: evidence invalidated or regression — any state",
        "may drop to revoked; recovery re-enters at tested. Evidence lives in evidence_refs; approval is attributable.",
    ], "s", 15)

    s.note(392, 606, 700, [
        "Axis independence (invariant): stable + unbound + unassessed is legal and common; certified requires verified",
        "history but never implies runnable-now. A UI may summarise; the stored model never collapses the axes.",
    ])
    return s.out()


# ------------------------------------------------------------------ the page
CSS = """
:root{--lv-bg:#f7f8fa;--lv-surface:#ffffff;--lv-ink:#16202e;--lv-sub:#3f4c5e;--lv-muted:#68788d;
--lv-line:#8494a8;--lv-gray:#f1f4f8;--lv-gray-s:#a8b4c4;
--lv-blue:#e9eff8;--lv-blue-s:#7d97b8;--lv-green:#eaf3ee;--lv-green-s:#84a98c;--lv-green-ink:#2f6b43;
--lv-sand:#f5f0e6;--lv-sand-s:#b3a689;--lv-purple:#f2edf8;--lv-purple-s:#9873bb;
--lv-yellow:#fdf7e6;--lv-yellow-s:#c3a158;--lv-cyan:#e9f4f6;--lv-cyan-s:#73a0aa;
--lv-red:#fdefed;--lv-red-s:#d16d62;--lv-red-ink:#a33f35;
--code:#f1f4f8;--chip:#e9eff8}
:root[data-theme=dark]{--lv-bg:#10151c;--lv-surface:#1a212b;--lv-ink:#e8edf4;--lv-sub:#c0cbd9;
--lv-muted:#8b99ac;--lv-line:#5d6c80;--lv-gray:#1e2733;--lv-gray-s:#48566a;
--lv-blue:#1c2836;--lv-blue-s:#4c6a8e;--lv-green:#1b2a22;--lv-green-s:#4f7a5c;--lv-green-ink:#8fce9f;
--lv-sand:#2a2620;--lv-sand-s:#8a7c5c;--lv-purple:#251f2e;--lv-purple-s:#7a5b99;
--lv-yellow:#2a2617;--lv-yellow-s:#9b8348;--lv-cyan:#17262a;--lv-cyan-s:#4f7d88;
--lv-red:#2e1c1a;--lv-red-s:#a35049;--lv-red-ink:#e09188;
--code:#141b24;--chip:#1c2836}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--lv-bg);color:var(--lv-sub);
font:15px/1.65 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
main{max-width:1180px;margin:0 auto;padding:44px 28px 110px}
h1{font-size:30px;line-height:1.25;color:var(--lv-ink);margin:6px 0 8px}
h2{font-size:21px;color:var(--lv-ink);margin:56px 0 8px;padding-top:18px;border-top:1px solid var(--lv-gray-s)}
h3{font-size:16px;color:var(--lv-ink);margin:30px 0 6px}
p{margin:10px 0}
.crumb{font-size:12.5px;color:var(--lv-muted);letter-spacing:.02em}
.chips{margin:14px 0 4px}
.chip{display:inline-block;background:var(--chip);border:1px solid var(--lv-blue-s);
border-radius:20px;padding:2px 12px;font-size:12px;color:var(--lv-sub);margin:0 6px 6px 0}
.toc{background:var(--lv-surface);border:1px solid var(--lv-gray-s);border-radius:12px;
padding:16px 20px;margin:26px 0;font-size:14px}
.toc a{display:block;color:var(--lv-sub);text-decoration:none;padding:3px 0}
.toc a:hover{color:var(--lv-ink)}
.toc .h{font-weight:700;color:var(--lv-ink);margin-bottom:6px}
.fig{background:var(--lv-surface);border:1px solid var(--lv-gray-s);border-radius:14px;
padding:18px;margin:18px 0;overflow-x:auto}
.fig svg{display:block;min-width:1120px}
.figcap{font-size:12.5px;color:var(--lv-muted);margin:10px 4px 0}
table{border-collapse:collapse;width:100%;margin:14px 0;font-size:13.5px;background:var(--lv-surface);display:block;overflow-x:auto}
table tbody{display:table;width:100%}
th,td{border:1px solid var(--lv-gray-s);padding:7px 11px;text-align:left;vertical-align:top}
th{background:var(--lv-gray);color:var(--lv-ink);font-size:12.5px}
code,pre{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
code{background:var(--code);border-radius:4px;padding:1px 5px;font-size:12.8px}
pre{background:var(--code);border:1px solid var(--lv-gray-s);border-radius:10px;
padding:16px;overflow-x:auto;font-size:12.3px;line-height:1.55}
pre code{background:none;padding:0}
.callout{border-left:4px solid var(--lv-blue-s);background:var(--lv-blue);
border-radius:0 10px 10px 0;padding:12px 16px;margin:16px 0;font-size:14px}
.callout.warn{border-left-color:var(--lv-red-s);background:var(--lv-red)}
.callout.ok{border-left-color:var(--lv-green-s);background:var(--lv-green)}
.tt{position:fixed;right:18px;bottom:18px;width:42px;height:42px;border-radius:50%;
border:1px solid var(--lv-gray-s);background:var(--lv-surface);color:var(--lv-ink);
font-size:18px;cursor:pointer}
.small{font-size:12.5px;color:var(--lv-muted)}
@media (prefers-color-scheme: dark){:root:not([data-theme=light]){--lv-bg:#10151c;--lv-surface:#1a212b;
--lv-ink:#e8edf4;--lv-sub:#c0cbd9;--lv-muted:#8b99ac;--lv-line:#5d6c80;--lv-gray:#1e2733;
--lv-gray-s:#48566a;--lv-blue:#1c2836;--lv-blue-s:#4c6a8e;--lv-green:#1b2a22;--lv-green-s:#4f7a5c;
--lv-green-ink:#8fce9f;--lv-sand:#2a2620;--lv-sand-s:#8a7c5c;--lv-purple:#251f2e;--lv-purple-s:#7a5b99;
--lv-yellow:#2a2617;--lv-yellow-s:#9b8348;--lv-cyan:#17262a;--lv-cyan-s:#4f7d88;--lv-red:#2e1c1a;
--lv-red-s:#a35049;--lv-red-ink:#e09188;--code:#141b24;--chip:#1c2836}}
"""

THEME_JS = """
var r=document.documentElement,k='lv-theme',s=null;try{s=localStorage.getItem(k)}catch(e){}
if(s)r.setAttribute('data-theme',s);
document.getElementById('tt').addEventListener('click',function(){
var cur=r.getAttribute('data-theme');
var next=cur==='dark'?'light':cur==='light'?'dark':
(window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches?'light':'dark');
r.setAttribute('data-theme',next);try{localStorage.setItem(k,next)}catch(e){}});
"""


def build():
    yaml_text = (ROOT / "capability-capsule.to-be.template.yaml").read_text(encoding="utf-8")

    hooks_table = """
<table>
<tr><th>Hook point</th><th>Enum value (<code>AgentCallbackEvent</code>)</th><th>Fires</th><th>Fire site / note</th></tr>
<tr><td rowspan="2">Invocation</td><td><code>BEFORE_INVOKE</code></td><td>before</td><td rowspan="2"><code>ctx.lifecycle(...)</code> — <code>react_agent.py:1670</code>; AFTER guaranteed on every exit path</td></tr>
<tr><td><code>AFTER_INVOKE</code></td><td>after</td></tr>
<tr><td rowspan="2">Task iteration (outer loop)</td><td><code>BEFORE_TASK_ITERATION</code></td><td>before</td><td rowspan="2">one outer coordinator iteration</td></tr>
<tr><td><code>AFTER_TASK_ITERATION</code></td><td>after</td></tr>
<tr><td>ReAct iteration (inner loop)</td><td><code>AFTER_REACT_ITERATION</code></td><td><strong>after only</strong></td><td><code>react_agent.py:1818</code>; success-only — never fired on a break path (<code>base.py:200-202</code>). There is no before-ReAct hook; per-iteration pre-checks must ride <code>BEFORE_MODEL_CALL</code>.</td></tr>
<tr><td rowspan="3">Model call</td><td><code>BEFORE_MODEL_CALL</code></td><td>before</td><td rowspan="3">decorated call, <code>react_agent.py:718-720</code></td></tr>
<tr><td><code>AFTER_MODEL_CALL</code></td><td>after</td></tr>
<tr><td><code>ON_MODEL_EXCEPTION</code></td><td>exception</td></tr>
<tr><td rowspan="3">Tool call</td><td><code>BEFORE_TOOL_CALL</code></td><td>before</td><td rowspan="3">per ability execution; permission enforcement lives inside this phase (<code>ToolSecurityRail</code>)</td></tr>
<tr><td><code>AFTER_TOOL_CALL</code></td><td>after</td></tr>
<tr><td><code>ON_TOOL_EXCEPTION</code></td><td>exception</td></tr>
</table>"""

    edges_table = """
<table>
<tr><th>#</th><th>Verified sharp edge</th><th>Evidence</th><th>Adapter obligation</th></tr>
<tr><td>1</td><td>SwarmFlow step failure is silent at run level: after <code>rt.retries+1</code> attempts <code>agent()</code> returns <code>None</code> and the run reports SUCCESS; the journal replays the <code>None</code> on resume.</td><td>executed probe (three-run journal replay)</td><td>validate every step result; a <code>None</code> is a failed attempt, never a receipt</td></tr>
<tr><td>2</td><td>Team model allocation falls back silently: <code>resolve_member_model</code> returns <code>None</code> for a missing pool group and the default model runs.</td><td><code>agent_teams/models/allocator.py:387-423</code> + executed audit</td><td>fail closed for capsule-bound attempts (wrapper or upstream fix)</td></tr>
<tr><td>3</td><td>Deployed guardrails load zero rules: the tiered-policy loader reads the package path only; JiuwenSwarm's <code>resources/builtin_rules.yaml</code> is written but never read.</td><td><code>harness/security/tiered_policy.py</code> + executed probe</td><td>wire the rules path or ship AI4RnD policy loading</td></tr>
<tr><td>4</td><td>Core Workflow conditional routers are invoked with <em>no arguments</em>; routing state must travel out-of-band.</td><td><code>core/workflow/workflow.py</code> (<code>Router</code> type) + executed probe</td><td>encode branch state in channels, not router params</td></tr>
<tr><td>5</td><td><code>SwarmflowTool</code> rejects <code>resume_id</code>/<code>name</code> ("not supported yet"); resume works only through <code>run_workflow(..., resume=…)</code>.</td><td>executed probe (tool schema)</td><td>drive resume through the engine API</td></tr>
<tr><td>6</td><td>Unknown SwarmFlow options fail loudly (allowed: <code>agent_type · isolation · label · model · phase · schema · timeout</code>) — the codebase fails loudly on typos and silently on unimplemented features.</td><td>executed probe (<code>WorkflowError</code>)</td><td>treat loud failures as friendly; hunt the silent ones</td></tr>
</table>"""

    gepa_table = """
<table>
<tr><th>Module</th><th>What it implements</th><th>Wiring status (as-is)</th></tr>
<tr><td><code>candidate_schema.py</code></td><td><code>CandidateType</code> = SKILL · CAPSULE · ROUTING_POLICY · REWRITE_RULES · COST_MODEL (<code>:23-30</code>)</td><td>schema only; SKILL exercised by tests</td></tr>
<tr><td>budget / stoppers</td><td><code>Budget</code> + Spend/Eval/Walltime/Plateau/StopFile stoppers — hard ceilings</td><td>unit-tested, unwired</td></tr>
<tr><td>adapter</td><td><code>GEPAAdapter</code> wrapping <code>gepa.optimize_anything</code></td><td>unit-tested, unwired</td></tr>
<tr><td><code>hard_policy_checker</code></td><td><code>check_candidate</code>: frozen-section diff — a candidate cannot relax secrets, git push, destructive shell or payment policies</td><td>unit-tested, unwired</td></tr>
<tr><td><code>artifact_store</code></td><td><code>RunRecord</code> / <code>CandidateRecord</code>, content-addressed with sha256 sidecars</td><td>unit-tested, isolated store</td></tr>
<tr><td><code>promoter</code></td><td><code>Promoter.promote/rollback</code>: tmp-vs-production guards, atomic writes, sidecar verification</td><td>unit-tested, unwired</td></tr>
<tr><td><code>cli</code></td><td>dry-run by default; explicit flag required to touch production artifacts</td><td>runnable standalone</td></tr>
</table>"""

    axes_tables = """
<h3>4.1 registry_status — definition lifecycle (owner: registry curator)</h3>
<table>
<tr><th>Value</th><th>Definition</th><th>Entry criterion</th><th>Planner visibility</th></tr>
<tr><td><code>draft</code></td><td>schema-valid definition exists; composition not guaranteed</td><td>manifest passes schema validation</td><td>not selectable</td></tr>
<tr><td><code>candidate</code></td><td>definition complete: contract, effects, composition and verification all populated and semantically valid</td><td><code>validate_capability_capsule</code> returns zero errors</td><td>selectable in non-production runs only</td></tr>
<tr><td><code>stable</code></td><td>definition frozen for this version; changes require a new version</td><td>curator review recorded</td><td>selectable</td></tr>
<tr><td><code>deprecated</code></td><td>superseded or discouraged; kept for pinned in-flight runs</td><td><code>replaced_by</code> set or curator decision</td><td>pinned runs only</td></tr>
<tr><td><code>retired</code></td><td>never selectable again; history retained</td><td>no in-flight pins remain</td><td>none</td></tr>
</table>
<h3>4.2 runtime_status — operational health (owner: control plane; never stored in the manifest file)</h3>
<table>
<tr><th>Axis</th><th>Value</th><th>Definition</th></tr>
<tr><td rowspan="3"><code>binding</code></td><td><code>unbound</code></td><td>no Physical Operator currently satisfies <code>executor_policy</code></td></tr>
<tr><td><code>bound</code></td><td>at least one qualified operator is admitted and healthy</td></tr>
<tr><td><code>unavailable</code></td><td>previously bound; all qualified operators currently failing health/quota</td></tr>
<tr><td rowspan="4"><code>readiness</code></td><td><code>not_proven</code></td><td>this capsule version has never executed</td></tr>
<tr><td><code>runnable</code></td><td>bindings executed successfully in a probe (skills load, MCP reachable, guards pass)</td></tr>
<tr><td><code>integrated</code></td><td>completed inside a real TaskGraph run with receipts and an accepted verdict</td></tr>
<tr><td><code>degraded</code></td><td>recent failure rate over threshold; control plane demotes automatically, re-promotes on healthy probes</td></tr>
</table>
<h3>4.3 assurance_status — certification (owner: independent verifier + human approver)</h3>
<table>
<tr><th>Value</th><th>Definition</th><th>Evidence required</th></tr>
<tr><td><code>unassessed</code></td><td>no assurance evidence exists</td><td>—</td></tr>
<tr><td><code>tested</code></td><td>all <code>verification.self_checks</code> pass in isolation</td><td>test run reference in <code>evidence_refs</code></td></tr>
<tr><td><code>verified</code></td><td>an independent verifier accepted a real run's evidence against the contract</td><td>verifier verdict, writer-attributed, in the gate ledger</td></tr>
<tr><td><code>certified</code></td><td>human approval recorded under <code>policy_ref</code></td><td>approval record: who, when, under which policy</td></tr>
<tr><td><code>revoked</code></td><td>evidence invalidated or regression observed; recovery re-enters at <code>tested</code></td><td>revocation reason + reference</td></tr>
</table>
<div class="callout"><strong>Axis independence (invariant).</strong> <code>stable</code> + <code>unbound</code> + <code>unassessed</code>
is a legal, common combination. <code>certified</code> requires verified history but never implies runnable-now.
A dashboard may summarise the three axes into one badge; the stored model never collapses them.</div>"""

    doc = f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI4RnD × OpenJiuwen — Low-Level Design</title>
<style>{CSS}</style></head><body><main>
<div class="crumb">Design package · low-level companion to the review plates ·
jiuwenswarm a98d7ad · openjiuwen 0.1.15.post3 · AI4Research d35c511</div>
<h1>Low-Level Design — OpenJiuwen runtime, AI4RnD as-is, and Capability Capsules</h1>
<p>The review plates (06–10) hold the design at architecture altitude. This document goes one
level down: <strong>exact classes, functions, enum values, error strings and line references</strong>,
so a design decision can be checked against the code it binds to. Every fact here is
source-verified or execution-verified; the verification record is
<code>adversarial-review.md</code> in this directory. Two things are as-is throughout —
the AI4RnD diagram and the Capsule inventory. The only to-be content is §4 (status
definitions) and §5 (the revised template), and both are labelled as proposals.</p>
<div class="chips">
<span class="chip">§1 OpenJiuwen runtime — low level</span>
<span class="chip">§2 AI4RnD as-is — low level, RSI in detail</span>
<span class="chip">§3 Capsules as-is</span>
<span class="chip">§4 Status definitions</span>
<span class="chip">§5 To-be template, draft 2</span>
</div>
<nav class="toc"><div class="h">Contents</div>
<a href="#s1">1 · OpenJiuwen runtime — low level (diagram + hook envelope + sharp edges)</a>
<a href="#s2">2 · AI4RnD as-is — low level (diagram + gate ledger anatomy + RSI module map)</a>
<a href="#s3">3 · Capability Capsules — as-is (corrected census, section anatomy, enforcement)</a>
<a href="#s4">4 · Status definitions — the three axes, precisely</a>
<a href="#s5">5 · Capability Capsule to-be template — draft 2</a>
<a href="#s6">6 · Changes applied in this revision</a>
</nav>

<h2 id="s1">1 · OpenJiuwen runtime — low level</h2>
<p>One diagram, five bands: request resolution and construction (A), the exact callback
order of one invocation (B) with its control surfaces, the ability path expanded to its
real pipeline (C), the internals of the three other orchestration mechanisms (D), and the
state actually written (E). Red strips are verified hazards, not stylistic warnings.</p>
<div class="fig">{dg_openjiuwen()}</div>
<p class="figcap">Diagram LL-1 — OpenJiuwen runtime at implementation granularity. All line references:
openjiuwen 0.1.15.post3 installed package; JiuwenSwarm paths from the a98d7ad checkout.</p>
<h3>1.1 The hook envelope, exactly</h3>
{hooks_table}
<h3>1.2 Verified sharp edges and the adapter obligations they impose</h3>
{edges_table}

<h2 id="s2">2 · AI4RnD — as-is, low level</h2>
<p>Seven bands, all current state: intake/coordinator (A), the capsule resolver's seven
checks in code order with their exact error strings (B), worker assignment (C), the
physical carrier that runs today and is rejected for the target (D), the return path with
the gate-ledger record anatomy (E), the four disjoint evidence stores (F), and RSI at
module granularity (G). Nothing in this diagram is target design.</p>
<div class="fig">{dg_ai4rnd()}</div>
<p class="figcap">Diagram LL-2 — AI4RnD current implementation. File references relative to the
AI4Research checkout at d35c511; <code>scheduler:</code> = harness/lib/graph_scheduler.py,
<code>dispatcher:</code> = harness/lib/graph_node_dispatcher.py.</p>
<h3>2.1 RSI as-is — module status</h3>
{gepa_table}
<div class="callout warn"><strong>As-is RSI verdict.</strong> The candidate→policy-check→store→promote
mechanics are implemented and unit-tested, and the governance properties (frozen sections,
dry-run default, atomic promotion, rollback) are real code — but nothing produces
trajectories for GEPA and nothing consumes its promotions. No RSI loop is executable
end-to-end today, and no diagram or document should claim otherwise.</div>

<h2 id="s3">3 · Capability Capsules — as-is</h2>
<p>Recounted from source for this document (census scripts in the verification record):</p>
<table>
<tr><th>Fact</th><th>Value</th><th>Source</th></tr>
<tr><td>Unique manifests</td><td><strong>42</strong> (19 in <code>harness/capability-capsules/</code> + 23 in <code>harness/config/capability-capsules/</code>; zero duplicate IDs)</td><td>directory census</td></tr>
<tr><td>Universal v1 sections</td><td><strong>11</strong>: <code>capability_capsule_id · capsule_kind · metadata · applicability · contract · composition · effects · bindings · verification · operator_compatibility · provenance</code></td><td>key-intersection over all 42</td></tr>
<tr><td>Optional extras</td><td><code>version</code> in 23 manifests; <code>runtime_preferences</code> in 6</td><td>key census</td></tr>
<tr><td>Registry entries</td><td><strong>35</strong> (32 capability · 1 guard · 2 resource)</td><td><code>capability-capsules.registry.yaml</code></td></tr>
<tr><td>Statuses</td><td><strong>30 stable · 5 draft</strong> (the five <code>cap.understand-anything-*</code>)</td><td>registry</td></tr>
<tr><td>Unregistered manifests</td><td><strong>7</strong>: 3 × <code>adapter.*</code> + <code>cap.chatgpt-browser-agent</code>, <code>cap.gemini-enhanced-search</code>, <code>cap.notebooklm-enrichment</code>, <code>cap.skill-execution-bridge</code></td><td>reconciliation</td></tr>
<tr><td>Ghost entries / broken paths</td><td><strong>0</strong> — every registry <code>manifest_path</code> resolves</td><td>reconciliation</td></tr>
</table>
<h3>3.1 What v1 actually enforces (as-is)</h3>
<p>The manifest is not decorative — three enforcement layers exist today, all in
<code>harness/lib/capability_capsules.py</code>:</p>
<table>
<tr><th>Layer</th><th>Checks</th><th>Failure behaviour</th></tr>
<tr><td>Schema validation</td><td>Draft 2020-12 JSON Schema (<code>schemas/draft/capability-capsule.v1.draft.json</code>)</td><td>error list from <code>validate_capability_capsule</code></td></tr>
<tr><td>Semantic validation (<code>:618-652</code>)</td><td>non-empty pre/postconditions and invariants; all four effect classes present; <strong>secret_refs ⇒ at least one guard.* reference</strong>; resource capsules may not declare <code>effects.execute</code>; guard capsules must declare pass conditions</td><td>error list; registration blocked</td></tr>
<tr><td>Resolution (<code>:1246-1338</code>)</td><td>the seven checks of diagram LL-2 band B, each with a typed <code>CapsuleResolutionError</code> string</td><td>honest stall — no silent degradation</td></tr>
</table>
<div class="callout"><strong>The as-is status problem.</strong> The registry's single
<code>status</code> field expresses definition maturity only. Nothing anywhere in the 42
manifests or 35 entries records whether a capsule has ever executed, is currently
executable, or has independently verified evidence. "Stable" therefore reads as
"works" while meaning only "schema settled" — the motivating defect for §4.</div>

<h2 id="s4">4 · Status definitions — the three axes, precisely</h2>
<p>Proposed (to-be). Three independent axes with distinct owners and transition rules.
The state diagram shows both worlds; the tables give the operative definitions the
template in §5 references.</p>
<div class="fig">{dg_status()}</div>
<p class="figcap">Diagram LL-3 — Capsule status: the as-is single flag versus the three
to-be axes with their transitions.</p>
{axes_tables}

<h2 id="s5">5 · Capability Capsule to-be template — draft 2</h2>
<p>The full revised template (<code>capability-capsule.to-be.template.yaml</code> in this
directory). Draft 2 keeps draft 1's structure — universal capsule, planner blueprint,
replaceable bindings, three status axes — and repairs the five migration defects the
adversarial review filed against draft 1:</p>
<table>
<tr><th>Review finding</th><th>Draft-2 change</th></tr>
<tr><td><strong>M-2</strong> — plate and template disagreed on the blueprint step unit</td><td>each step now carries <code>logical_operator_ref</code> as its typed action identity; skills remain the ingredients under it</td></tr>
<tr><td><strong>M-3</strong> — id-level operator deny-list dropped</td><td><code>executor_policy.forbidden_operators</code> restored (deny-by-id is a safety control, distinct from pinning; allow-lists stay kind/capability-based)</td></tr>
<tr><td><strong>M-4</strong> — registry <code>default_operator_profile</code> conflicts with <code>forbid_identity_pinning</code></td><td>explicit migration rule in the header: defaults move to the Physical Operator registry keyed by capability; the field is deleted from registry entries at migration</td></tr>
<tr><td><strong>M-5</strong> — secrets-require-guard invariant lost</td><td>schema invariants block restored in the header; <code>resources.secret_refs</code> annotated with the rule; validator + JSON schema listed as migration artifacts</td></tr>
<tr><td>Kind/prefix and corpus gaps</td><td><code>adapter</code> added to <code>capsule_kind</code>; per-kind ID prefixes stated; <code>portability.scope</code> gains <code>project</code>; <code>runtime_preferences</code> mapping and <code>version</code> backfill rules stated; kind-conditional sections marked</td></tr>
</table>
<pre><code>{escape(yaml_text)}</code></pre>

<h2 id="s6">6 · Changes applied in this revision</h2>
<table>
<tr><th>Change</th><th>Files</th></tr>
<tr><td>Corrected the capsule inventory everywhere it appears (42 manifests · 35 entries · 30 stable + 5 draft), closing review blocker B-1</td><td><code>build_design.py</code> (2 sites), regenerated <code>06-capability-capsule-design.svg</code></td></tr>
<tr><td>New low-level design document (this page) with diagrams LL-1/LL-2/LL-3 at implementation granularity, generated by <code>build_lowlevel.py</code></td><td><code>low-level-design.html</code>, <code>build_lowlevel.py</code></td></tr>
<tr><td>Capability Capsule to-be template revised to draft 2 (M-2 … M-5 + corpus fixes)</td><td><code>capability-capsule.to-be.template.yaml</code></td></tr>
<tr><td>Package index updated to point at the low-level companion</td><td><code>README.md</code>, <code>diagram-review.html</code></td></tr>
</table>
<p class="small">Generated by build_lowlevel.py — do not edit the HTML by hand.</p>
</main>
<button class="tt" id="tt" aria-label="Toggle colour theme">&#9689;</button>
<script>(function(){{{THEME_JS}}})();</script>
</body></html>"""

    out = ROOT / "low-level-design.html"
    out.write_text(doc, encoding="utf-8")
    print(f"wrote {out.name}: {len(doc)//1024} KB, {doc.count('<svg')} inline SVGs")


if __name__ == "__main__":
    build()
