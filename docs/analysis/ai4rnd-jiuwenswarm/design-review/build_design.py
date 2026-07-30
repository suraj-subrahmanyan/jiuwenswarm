#!/usr/bin/env python3
"""Generate the architecture plates from a deliberately small SVG vocabulary."""
from __future__ import annotations

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
W = 1100

COLORS = {
    "ink": "#1e293b", "muted": "#64748b", "line": "#475569", "canvas": "#ffffff",
    "blue": "#e8eef7", "blue_s": "#7d97b8", "green": "#e9f2ec", "green_s": "#84a98c",
    "sand": "#f3eee4", "sand_s": "#b3a689", "purple": "#f3edf8", "purple_s": "#9873bb",
    "yellow": "#fff8e7", "yellow_s": "#c3a158", "cyan": "#eef6f8", "cyan_s": "#73a0aa",
    "red": "#fff0ee", "red_s": "#d16d62", "gray": "#f8fafc", "gray_s": "#94a3b8",
}


class SVG:
    def __init__(self, height: int, title: str, desc: str):
        self.height = height
        self.parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" font-family="Helvetica,Arial,'Segoe UI',sans-serif" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="#475569"/></marker></defs>
<style>.title{{font-size:24px;font-weight:700;fill:#0f172a}}.h{{font-size:15px;font-weight:700;fill:#1e293b}}.n{{font-size:12.5px;font-weight:700;fill:#1e293b}}.s{{font-size:10.5px;fill:#475569}}.m{{font-size:11px;fill:#64748b}}.tiny{{font-size:9.5px;fill:#64748b}}.tag{{font-size:10px;font-weight:700;fill:#475569;letter-spacing:.04em}}.flow{{stroke:#475569;stroke-width:1.7;fill:none;marker-end:url(#arr)}}.flow2{{stroke:#475569;stroke-width:1.7;fill:none;marker-start:url(#arr);marker-end:url(#arr)}}.dash{{stroke:#64748b;stroke-width:1.3;stroke-dasharray:5 4;fill:none;marker-end:url(#arr)}}.box{{fill:#fff;stroke:#64748b;stroke-width:1;rx:7}}</style><rect width="{W}" height="{height}" fill="#fff"/>''']
        self.text(24, 38, title, "title")
        self.text(24, 62, desc, "m")

    def text(self, x, y, value, cls="s", anchor=None):
        a = f' text-anchor="{anchor}"' if anchor else ""
        self.parts.append(f'<text x="{x}" y="{y}" class="{cls}"{a}>{escape(value)}</text>')

    def lines(self, x, y, values, cls="s", gap=17):
        for i, value in enumerate(values): self.text(x, y + i * gap, value, cls)

    def rect(self, x, y, w, h, fill="gray", radius=10, stroke=None, dashed=False, sw=1.2):
        st = stroke or COLORS.get(fill + "_s", COLORS["gray_s"])
        dash = ' stroke-dasharray="5 4"' if dashed else ""
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{COLORS.get(fill, fill)}" stroke="{st}" stroke-width="{sw}"{dash}/>')

    def panel(self, x, y, w, h, title, subtitle="", fill="gray", dashed=False):
        self.rect(x, y, w, h, fill, dashed=dashed)
        self.text(x + 14, y + 24, title, "h")
        if subtitle: self.text(x + 14, y + 43, subtitle, "m")

    def node(self, x, y, w, h, title, lines=(), fill="#fff", dashed=False):
        self.rect(x, y, w, h, fill, stroke=COLORS["gray_s"] if dashed else COLORS["line"], dashed=dashed, sw=1)
        self.text(x + 11, y + 22, title, "n")
        self.lines(x + 11, y + 40, lines, "s", 16)

    def arrow(self, d, cls="flow"):
        self.parts.append(f'<path d="{d}" class="{cls}"/>')

    def label(self, x, y, value): self.text(x, y, value, "tag")

    def badge(self, x, y, value, fill="gray", width=None):
        width = width or max(72, 16 + len(value) * 6)
        self.rect(x, y, width, 24, fill, radius=12, sw=1)
        self.text(x + width / 2, y + 16, value, "tag", anchor="middle")

    def finish(self, name):
        (ROOT / name).write_text("\n".join(self.parts) + "\n</svg>\n", encoding="utf-8")


def openjiuwen():
    s = SVG(1520, "OpenJiuwen — Current System Design", "How a serializable agent definition becomes durable, governed execution")
    # Host/application boundary
    s.panel(30, 90, 1040, 150, "JiuwenSwarm application host", "Channels and UI are outside the OpenJiuwen package; AgentServer is its main assembly/invocation client", "blue")
    for x, title, body in [(50,"Gateway & channels",("web · TUI · desktop · IM", "E2A normalization + routing")),(310,"AgentServer",("session + agent/team cache", "build / invoke / interrupt")),(570,"Application services",("configuration · providers · cron", "history · UI state")),(830,"Request context",("session · mode · language", "workspace · permissions"))]:
        s.node(x,145,220,70,title,body)

    # OpenJiuwen package boundary
    s.rect(30, 275, 1040, 1160, "gray", radius=14, stroke=COLORS["ink"], sw=2.2)
    s.text(46, 299, "OPENJIUWEN PACKAGE", "tag")

    # Construction
    s.panel(50, 320, 1000, 175, "1. Definition & runtime construction", "Serializable intent is resolved through explicit provider registries", "green")
    s.node(70,375,210,88,"Agent specifications",("DeepAgentSpec / TeamAgentSpec", "JSON-round-trippable"))
    s.node(300,375,210,88,"Leaf contracts",("model · tools · MCP · Rails", "skills · workspace · sub-agents"))
    s.node(530,375,210,88,"Build context",("provider registries", "parameter + context resolution"))
    s.node(760,375,270,88,"Live runtime graph",("DeepAgentConfig + resources", "process-local handles and callbacks"))
    s.arrow("M280 419 H295"); s.arrow("M510 419 H525"); s.arrow("M740 419 H755")

    # Runtime kernels
    s.panel(50, 525, 660, 330, "2. Execution kernels", "The agent loop and graph engine are different kernels with different control models", "sand")
    s.node(70,580,290,112,"DeepAgent task kernel",("outer task loop: follow-up · completion", "inner ReAct: model ↔ tool observation", "session-bound, cancellable"))
    s.node(380,580,310,112,"Workflow / Pregel graph kernel",("components + typed channels", "barrier supersteps · conditional routing", "interrupt + checkpoint + restore"))
    s.node(70,715,290,112,"Model-call boundary",("prompt/context assembly", "model allocation + client/request config", "response or typed exception"))
    s.node(380,715,310,112,"Ability-call boundary",("Tool/MCP/Agent/Workflow card", "argument parse → permission decision", "runner resource → ToolMessage"))
    s.arrow("M215 692 V710"); s.arrow("M535 692 V710")

    # Rails cross-cutting
    s.panel(735, 525, 315, 330, "3. Rail lifecycle envelope", "Ordered middleware around the execution kernels", "purple")
    s.lines(755,590,["Invoke: before · after","Task iteration: before · after","ReAct iteration: after","Model: before · after · exception","Tool: before · after · exception"],"n",31)
    s.lines(755,762,["May add abilities or context","May ask/interrupt/retry/finish","May record trajectory/evolution"],"s",20)
    s.arrow("M735 690 H715", "flow2")

    # Orchestration
    s.panel(50, 885, 1000, 190, "4. Orchestration mechanisms", "Each mechanism composes kernels; none defines AI4RnD product semantics", "blue")
    for x,title,body in [(70,"Direct DeepAgent",("one adaptive agent turn", "task loop owns continuation")),(310,"Core Workflow",("known component topology", "checkpoint + interrupt")),(550,"SwarmFlow",("Python orchestration primitives", "journal · admission · abort")),(790,"Dynamic Team / NativeHarness",("leader · members · review", "persistent dependency tasks"))]:
        s.node(x,940,220,102,title,body)

    # Resource services
    s.panel(50, 1105, 1000, 190, "5. Resource and capability services", "The kernels consume these services through cards, registries, and scoped operations", "yellow")
    for x,title,body in [(70,"Models",("pool entries · allocator", "client + request config")),(265,"Tools & MCP",("cards separate from resources", "typed calls + permissions")),(460,"Skills",("SKILL.md registry", "prompt or on-demand discovery")),(655,"Workspace / sandbox",("private · team · worktree", "local or sandbox SysOperation")),(850,"Sub-agents",("nested specs · fallback model", "sync or session-spawn"))]:
        s.node(x,1160,180,102,title,body)

    # State
    s.panel(50, 1325, 1000, 86, "6. Durability is distributed by execution model", "session history · workflow checkpoints · SwarmFlow WAL · team task DB · long-term/coding/team memory", "cyan")
    s.text(70,1394,"These stores preserve runtime progress. They do not provide Contracts, evidence ledgers, scientific gates, or Capsule certification.","tiny")

    # Layer flow
    s.arrow("M550 240 V320"); s.arrow("M550 495 V520"); s.arrow("M550 855 V880"); s.arrow("M550 1075 V1100"); s.arrow("M550 1295 V1320")
    s.rect(50, 1450, 1000, 46, "red", radius=8)
    s.text(64,1472,"Verified gaps", "n"); s.text(155,1472,"silent model fallback · resume not agent-reachable · failed step may return empty success · agent_type unused", "s")
    s.text(64,1490,"Integration must fence these behaviors with typed receipts and fail-closed compatibility tests.","tiny")
    s.finish("01-openjiuwen-as-is.svg")


def ai4rnd():
    s = SVG(1600, "AI4RnD — Current System Design", "Implemented, unwired, partial, and absent product machinery shown as distinct architectural blocks")
    s.panel(30,90,1040,120,"Current product surface & carrier","The product is reached through a CLI/status UI and coordinated through files and tmux", "blue")
    for x,t,b in [(50,"solar-harness CLI",("intake · commands · status",)),(310,"tmux cockpit",("PM · Planner · Builder · Evaluator",)),(570,"Status server / React",("reads artifacts for visibility",)),(830,"Polling coordinator",("mtime + state transitions",))]: s.node(x,140,220,55,t,b)

    s.panel(30,245,1040,240,"1. Run control and planning","Current execution control is real but coupled to sprint files and the tmux carrier", "gray")
    for x,t,b in [(50,"Sprint state machine",("12 lifecycle states", "timeouts · retries · artifacts")),(300,"TaskGraph scheduler",("DAG validation · topo layers", "readiness · batching · write scope")),(550,"APO plan compiler",("logical workflow expansion", "Capsule/skill/MCP stages")),(800,"Capability router",("hard capability gate", "role · quota · health · capacity"))]: s.node(x,310,230,122,t,b)
    s.arrow("M280 371 H295"); s.arrow("M530 371 H545"); s.arrow("M780 371 H795")

    s.panel(30,515,1040,230,"2. Governed capability and operator model","Reusable product semantics are separate from the workers that happen to execute them", "purple")
    s.node(50,575,240,130,"Capability Capsules",("42 manifests; 35 registered", "applicability · contract · effects", "composition · verification · provenance"))
    s.node(310,575,230,130,"Logical Operators",("stable DAG-callable actions", "required capabilities · evidence", "completion and write scope"))
    s.node(560,575,230,130,"Physical Operators",("worker profiles · quota · cost", "health · model · runtime", "hard admission, then binding"))
    s.node(810,575,240,130,"Runtime gate",("inputs · preconditions · resources", "sensitive effects · idempotency", "cooldown · verifier attachment"))
    s.arrow("M290 640 H305"); s.arrow("M540 640 H555"); s.arrow("M790 640 H805")

    s.panel(30,775,330,300,"3. Physical execution carrier","This substrate is the principal part to retire", "red")
    s.lines(50,830,["tmux pane workers","send-keys dispatch","pane busy-marker polling","Codex inbox/outbox bridge","artifact handoff files"],"n",38)
    s.lines(50,1033,["Known failure family:","focus · split command/Enter · stale pane", "polling delay · unsafe permissions"],"tiny",16)

    s.panel(390,775,680,300,"4. R&D workflow capabilities","Real modules exist across the workflow, but the complete intended product is not one wired path", "green")
    lanes=[("Discover","search · rank · qualify"),("Ingest","documents · spans · provenance"),("Structure","claims · evidence links"),("Build / test","code · POC · benchmark"),("Evaluate","gates · repair · verifier"),("Deliver","report · evidence bundle")]
    for i,(t,b) in enumerate(lanes):
        x=410+(i%3)*215; y=835+(i//3)*100; s.node(x,y,195,76,t,(b,))
    s.text(410,1030,"Current correctness blocker: grounding is token overlap; prior measured precision 0.25.","tiny")

    s.panel(30,1105,510,250,"5. Evidence, verification and authoritative state","This is the strongest portable AI4RnD asset", "yellow")
    s.node(50,1160,145,150,"Run truth",("status.json", "task_graph.json", "handoff/eval artifacts"))
    s.node(213,1160,145,150,"Evidence truth",("sources + hashes", "spans + claims", "claim/evidence links"))
    s.node(376,1160,145,150,"Gate truth",("append-only ledger", "writer attribution", "verdict + repair"))

    s.panel(560,1105,510,250,"6. Data foundations","Current stores exist; the intended typed graph plane does not", "cyan")
    s.node(580,1160,145,150,"Operational",("events.jsonl", "run/state.db", "traces + artifacts"))
    s.node(743,1160,145,150,"Knowledge",("wiki schemas", "memory / context", "partial typed entities"))
    s.node(906,1160,145,150,"To build",("concept · dataset", "code · policy · workflow", "trace · memory projections"), dashed=True)

    s.panel(30,1385,1040,150,"7. Governed self-improvement — current maturity","Eight intended improvement surfaces do not yet form one operational loop", "red")
    s.node(50,1435,290,75,"Implemented but isolated",("GEPA: propose → evaluate → promote/rollback", "dry-run default + budget + frozen policy"), fill=COLORS["green"])
    s.node(360,1435,280,75,"Partial on-ramps",("Capsule compiler · operator profiles", "failure mining · benchmark fragments"), fill=COLORS["yellow"])
    s.node(660,1435,390,75,"Not wired end to end",("routing · DAG · evaluators · retrieval", "model weights · data/benchmark curriculum"), dashed=True)
    s.arrow("M550 210 V240"); s.arrow("M550 485 V510"); s.arrow("M550 745 V770"); s.arrow("M550 1075 V1100"); s.arrow("M550 1355 V1380")
    s.finish("02-ai4rnd-as-is.svg")


def compatibility():
    s = SVG(1510, "AI4RnD × OpenJiuwen — Component Compatibility", "Architecture decisions are based on semantic fit, not name similarity")
    s.text(42,102,"AI4RnD product block","h"); s.text(424,102,"Decision","h"); s.text(582,102,"OpenJiuwen / JiuwenSwarm foundation","h")
    rows = [
      ("Channels, UI, sessions, packaging","REUSE + EXTEND","Gateway, channels, UI, session and packaging are strong; add project linkage."),
      ("Intention Compiler + Contract","ADAPT / BUILD","Ask-user and session context help, but no research Contract authority exists."),
      ("Planner + semantic TaskGraph","ADAPT + DERIVE","Team planning/task DAG is useful plumbing; AI4RnD meaning, evidence and gates must be added."),
      ("Capability Capsules","PORT + EXTEND","Skills/tools/agents are bindings beneath Capsules; no OpenJiuwen equivalent governs contract/effects/certification."),
      ("Logical/Physical Operators","ADAPT","Reuse agent/tool/workflow construction; add capability admission, exact binding and operator profiling."),
      ("Harness Core","REUSE + FENCE","Reuse DeepAgent, Pregel, Workflow, SwarmFlow, Team, checkpoints and concurrency; fence verified false-success gaps."),
      ("POC / code / benchmark execution","REUSE + ADAPT","Code mode, worktrees, tools and sandbox execute work; AI4RnD supplies build/benchmark contracts and receipts."),
      ("Evidence, claims, evaluators, gates","PORT + BUILD","No equivalent foundation semantics; port ledgers and complete entailment, evaluator families and repair."),
      ("Typed data foundations","BUILD + COMPOSE","Use Jiuwen stores/retrieval as infrastructure; AI4RnD owns schemas, provenance and typed projections."),
      ("GEPA and governed RSI","PORT + COMPOSE","Keep GEPA search/governance; reuse Trainer/Updater as machinery only after compatibility tests."),
      ("Permissions and sandbox","REUSE + FIX","Strong substrate, but builtin guardrail loading is currently miswired and must be proven non-empty."),
      ("Accounts / multi-user governance","BUILD","Neither local-first system supplies the complete account/privacy lifecycle."),
    ]
    y=125
    decision_fill={"REUSE":"green","ADAPT":"yellow","PORT":"purple","BUILD":"red"}
    for i,(left,decision,right) in enumerate(rows):
        h=102; fill="gray" if i%2==0 else "#ffffff"; s.rect(30,y,1040,h,fill,radius=0,stroke="#cbd5e1",sw=1)
        s.text(46,y+28,left,"n")
        key=next((k for k in decision_fill if k in decision),"ADAPT"); s.rect(405,y+18,150,34,decision_fill[key],radius=17)
        s.text(480,y+40,decision,"tag",anchor="middle")
        # manual two-line wrap
        split=right.rfind(" ",0,73); split=split if split>45 else len(right)
        s.text(580,y+28,right[:split],"s");
        if split<len(right): s.text(580,y+48,right[split+1:],"s")
        y+=h
    s.rect(30,1365,1040,110,"blue",radius=10)
    s.text(46,1392,"Compatibility verdict","h")
    s.lines(46,1417,["OpenJiuwen is a credible execution and application foundation, not the AI4RnD product core.","The integration succeeds only if AI4RnD retains Contracts, Capsules, TaskGraph semantics, evidence/gates, typed data and governed RSI.","The bridge must compile bounded work into Jiuwen execution and return typed receipts—never transfer semantic completion authority."],"s",19)
    s.finish("03-component-compatibility.svg")


def target():
    s = SVG(1450, "Recommended Target Design", "AI4RnD owns product truth; JiuwenSwarm hosts the product; OpenJiuwen executes bounded work")
    s.panel(30,90,1040,150,"JiuwenSwarm product shell","Reusable application foundation", "blue")
    for x,t,b in [(50,"Channels & UI",("web · desktop · TUI · IM",)),(300,"Gateway & sessions",("E2A · identity · project link",)),(550,"Configuration",("models · permissions · credentials",)),(800,"Operations",("cron · packaging · platform status",))]: s.node(x,145,230,70,t,b)

    s.panel(30,285,1040,365,"AI4RnD project and semantic control plane","Authoritative meaning, readiness and completion", "purple")
    for x,y,t,b in [(50,345,"Project / Contract",("objective · scope · budgets · acceptance",)),(300,345,"Intention Compiler",("interpret · clarify · confirm",)),(550,345,"Planner / TaskGraph",("dependencies · evidence owed · write scope",)),(800,345,"Capsule registry",("contract · effects · composition · certification",)),(50,465,"Logical Operators",("stable callable actions",)),(300,465,"Capability binding policy",("hard admission · model/operator constraints",)),(550,465,"Evidence & gate authority",("claims · evaluators · verdicts · repair",)),(800,465,"Data & improvement authority",("typed graphs · GEPA · promotion/rollback",))]: s.node(x,y,230,90,t,b)

    s.panel(180,690,740,210,"Integration compiler and execution bridge","The only layer allowed to translate between product semantics and runtime mechanisms", "yellow")
    s.node(200,750,215,110,"Compile ready slice",("Contract/Capsule constraints", "→ agent/workflow/team spec", "idempotency + budget + effects"))
    s.node(442,750,215,110,"Bind exact executor",("agent/tool/model/workflow", "stall when no qualified target", "no silent fallback"))
    s.node(684,750,215,110,"Reconcile receipt",("attempt lineage + artifacts", "technical success/failure", "never a semantic verdict"))
    s.arrow("M415 805 H437"); s.arrow("M657 805 H679")

    s.panel(30,940,1040,225,"OpenJiuwen execution foundation","Mechanism selection is internal and replaceable", "sand")
    for x,t,b in [(50,"DeepAgent",("adaptive bounded work", "ReAct + task loop")),(250,"Core Workflow / Pregel",("known graphs", "checkpoint + interrupt")),(450,"SwarmFlow",("parallel/pipeline/map", "journal + admission")),(650,"Dynamic Team",("leader/members/review", "persistent task DAG")),(850,"Code + tools",("worktrees · LSP · MCP", "jiuwenbox sandbox"))]: s.node(x,1000,180,122,t,b)

    s.panel(30,1205,1040,175,"Authoritative state boundaries","A session is not a project; a runtime checkpoint is not evidence", "cyan")
    s.node(50,1260,310,86,"Jiuwen runtime state",("session · checkpoint · WAL · team task DB", "operational and replayable"))
    s.node(395,1260,310,86,"AI4RnD product state",("Contract · TaskGraph · Capsule versions", "claims · evidence · gates · improvements"))
    s.node(740,1260,310,86,"Cross-system lineage",("project_id · attempt_id · runtime run_id", "typed request/receipt + reconciliation"))
    s.arrow("M550 240 V280"); s.arrow("M550 650 V685"); s.arrow("M550 900 V935"); s.arrow("M550 1165 V1200")
    s.finish("04-target-architecture.svg")


def lifecycle():
    s = SVG(1540, "End-to-End Integrated Lifecycle", "From an R&D objective to evidence-backed delivery and governed improvement")
    stages=[
      ("1. Capture objective","JiuwenSwarm","channel/session creates or opens an AI4RnD project","raw request + provenance"),
      ("2. Compile Contract","AI4RnD","interpret intent, clarify consequential ambiguity, confirm scope/budget/acceptance","versioned Contract"),
      ("3. Plan the work","AI4RnD","decompose into a validated TaskGraph with dependencies, evidence owed and write scope","semantic TaskGraph"),
      ("4. Select Capsules","AI4RnD","expand reusable skill-centered partial plans; enforce effects, composition and verification","qualified Logical Operators"),
      ("5. Bind and compile","Bridge","choose exact model/operator and compile ready slices into agent/workflow/team specifications","ExecutionRequest"),
      ("6. Execute bounded work","OpenJiuwen","run DeepAgent, Workflow, SwarmFlow, Team, code or deterministic tools under permissions/sandbox","events · artifacts · ExecutionReceipt"),
      ("7. Reconcile technical result","Bridge","validate identity, lineage, terminal state, artifacts and declared effects; fail closed on ambiguity","accepted/rejected attempt"),
      ("8. Evaluate meaning","AI4RnD","independent evaluators check Contract conformance, evidence, science, engineering, security and cost","evidence records + gate verdict"),
      ("9. Repair, replan or progress","AI4RnD","repair artifact; revise TaskGraph; or release dependent nodes—never retry past a refuted claim","new attempt or plan revision"),
      ("10. Deliver and retain","AI4RnD + JiuwenSwarm","freeze evidence-linked deliverable, distribute through channels, update typed knowledge projections","deliverable + retained knowledge"),
      ("11. Govern improvement","AI4RnD GEPA + Jiuwen machinery","mine trajectories, propose candidates, run isolated evaluation, frozen-policy check, approve, promote, monitor, rollback","new version for future projects"),
    ]
    y=90
    fills=["blue","purple","purple","purple","yellow","sand","yellow","green","red","blue","red"]
    for i,(title,owner,action,out) in enumerate(stages):
        s.rect(120,y,860,105,fills[i],radius=10)
        s.text(140,y+27,title,"h"); s.text(780,y+27,owner,"tag")
        s.text(140,y+52,action,"s"); s.text(140,y+77,"Produces: "+out,"tiny")
        if i<len(stages)-1: s.arrow(f"M550 {y+105} V{y+125}")
        y+=130
    s.arrow("M980 1185 H1040 V835 H985","dash"); s.text(992,1015,"repair / replan","m")
    s.arrow("M980 1445 H1060 V245 H985","dash"); s.text(992,575,"future runs use", "m"); s.text(992,591,"approved versions", "m")
    s.finish("05-end-to-end-lifecycle.svg")


def capsule_design():
    s = SVG(1480, "Capability Capsule — Detailed Design", "A universal governed capability definition that contributes a partial plan and binds replaceable execution resources")

    s.panel(30, 90, 1040, 390, "1. Capsule definition — stable product identity", "Created before a project; reusable across agents, teams and execution engines", "purple")
    blocks = [
        (50, 150, "Applicability", ("task types · positive/negative signals", "selection and exclusion rules")),
        (300, 150, "Typed contract", ("inputs · outputs · pre/postconditions", "invariants · acceptance evidence")),
        (550, 150, "Declared effects", ("read · write · execute · network", "cost · risk · approval class")),
        (800, 150, "Composition", ("consumes · produces · ordering", "compatible · incompatible Capsules")),
        (50, 285, "Planner blueprint [TARGET]", ("each step names one Logical Operator", "dependencies · binding needs · evidence owed")),
        (300, 285, "Executor compatibility", ("required capabilities", "kind allow/deny + operator deny-list")),
        (550, 285, "Verification", ("self-check · independent verifier", "pass conditions · separation of duties")),
        (800, 285, "Provenance & lifecycle", ("owner · origin · certification", "version · history · rollback")),
    ]
    for x, y, title, body in blocks:
        s.node(x, y, 230, 100, title, body)
    s.rect(50, 405, 980, 48, "yellow", radius=8)
    s.text(64, 427, "Invariant", "n")
    s.text(132, 427, "A Capsule may constrain or expand the plan; it may not hide Logical Operators, embed credentials, or pin one agent instance.", "s")
    s.text(64, 444, "Current source: 42 unique manifests; all carry 11 v1 sections. Registry: 35 entries (30 stable, 5 draft), with 7 manifests unregistered.", "tiny")

    s.panel(30, 520, 1040, 250, "2. Planning contribution — the house-plan model", "The Planner selects reusable partial plans, then composes them into the project TaskGraph", "green")
    s.node(50, 585, 200, 120, "Project Contract", ("goal · constraints · budgets", "acceptance · required evidence"))
    s.node(285, 585, 220, 120, "Capsule selection", ("match applicability", "check composition", "pin version"))
    s.node(540, 585, 230, 120, "Partial plan expansion", ("wall before window", "typed data/evidence edges", "required verifier steps"))
    s.node(805, 585, 225, 120, "Validated TaskGraph", ("project-specific nodes", "dependencies + write scope", "Capsule/Operator references"))
    s.arrow("M250 645 H280"); s.arrow("M505 645 H535"); s.arrow("M770 645 H800")
    s.text(50, 742, "The Capsule is analogous to a reusable building-system specification: it contributes mandatory order and checks, while the Planner still owns the complete house plan.", "tiny")

    s.panel(30, 810, 1040, 300, "3. Replaceable execution bindings — implementation beneath the Capsule", "Binding happens after semantic readiness; failure to find an exact qualified executor produces an honest stall", "sand")
    s.node(50, 875, 230, 150, "Logical Operator", ("stable callable action", "typed request/receipt", "write scope · evidence owed", "referenced by TaskGraph"))
    binding_nodes = [
        (315, 865, "Skill", ("prompt package", "portable guidance")),
        (500, 865, "Tool / MCP", ("typed callable", "resource capability")),
        (685, 865, "Agent / Team", ("adaptive executor", "DeepAgent / Dynamic Team")),
        (870, 865, "Workflow", ("Core Workflow", "SwarmFlow / code")),
        (407, 985, "Model [TARGET]", ("exact qualified binding", "fix/fence silent fallback")),
        (592, 985, "Data / secret", ("versioned references", "never inline")),
        (777, 985, "External operator", ("browser · API · host", "health/quota/cost")),
    ]
    for x, y, title, body in binding_nodes:
        s.node(x, y, 165, 88, title, body)
    s.arrow("M280 950 H305");
    s.text(50, 1084, "A skill, agent, model, tool or workflow can implement part of a Capsule. None is its identity. Secret refs require a guard Capsule.", "tiny")

    s.panel(30, 1150, 1040, 260, "4. Assurance, operation and evolution — three status axes", "Do not compress definition maturity, runtime health and certification into one 'stable' flag", "cyan")
    s.node(50, 1210, 285, 130, "Definition lifecycle", ("manifest-present → registered", "draft → stable → deprecated", "schema and composition validation"))
    s.node(375, 1210, 285, 130, "Runtime readiness", ("unbound → bound → runnable", "integrated · degraded · unavailable", "exact executor + resource health"))
    s.node(700, 1210, 330, 130, "Assurance lifecycle", ("unassessed → tested → verified", "certified → revoked", "independent evidence + approval"))
    s.arrow("M335 1275 H370"); s.arrow("M660 1275 H695")
    s.text(50, 1372, "GEPA / governed RSI may propose a new version from execution and evaluation history. Promotion requires frozen-policy checks, isolated evaluation, approval, monitoring and rollback.", "s")
    s.text(50, 1392, "In-flight projects pin the selected Capsule version; improvement changes future runs only unless an explicit migration is approved.", "tiny")
    s.finish("06-capability-capsule-design.svg")


def openjiuwen_turn_design():
    s = SVG(1780, "OpenJiuwen — DeepAgent Turn Design", "White-box request, construction, model, tool, Rail, permission, workspace and state interactions")

    s.panel(30, 90, 1040, 175, "A. Request resolution in JiuwenSwarm", "The application resolves identity and a session-bound runtime before OpenJiuwen begins agent execution", "blue")
    request = [
        (50, 150, "Channel / client", ("message · command · ACP/A2A", "user + channel identity")),
        (260, 150, "Gateway routing", ("normalize E2A envelope", "resolve route + session")),
        (470, 150, "AgentServer", ("select configured agent/team", "cache · invoke · interrupt")),
        (680, 150, "Agent manager", ("load or rebuild runtime", "bind session context")),
        (880, 150, "Invocation context", ("request · mode · language", "workspace · permissions")),
    ]
    for x, y, title, body in request: s.node(x, y, 180 if x == 880 else 190, 90, title, body)
    for x in (240, 450, 660, 870): s.arrow(f"M{x} 195 H{x+15}")

    s.panel(30, 300, 1040, 235, "B. Serializable specification becomes a live agent", "Construction is explicit; definitions and process-local resources remain separate", "green")
    construction = [
        (50, 365, "DeepAgentSpec", ("model · prompt · tools · MCP", "Rails · skills · sub-agents", "task loop · workspace · policy")),
        (270, 365, "BuildContext", ("provider registries", "parameter/context resolution", "cross-process rebuild seed")),
        (490, 350, "Resolved components", ("model pool + allocator [GAP]", "Ability cards + resources", "Rail instances + callbacks", "Skill/workspace managers")),
        (730, 365, "DeepAgentConfig", ("live model/runner references", "loop and context policies", "session-capable config")),
        (930, 365, "DeepAgent", ("outer task coordinator", "inner ReAct agent", "interrupt/cancel surface")),
    ]
    widths = [190, 190, 210, 170, 130]
    for (x, y, title, body), w in zip(construction, widths): s.node(x, y, w, 130, title, body)
    s.arrow("M240 430 H265"); s.arrow("M460 430 H485"); s.arrow("M700 430 H725"); s.arrow("M900 430 H925")

    s.panel(30, 575, 760, 870, "C. One invocation — two nested loops", "The outer task loop owns continuation; the inner ReAct loop owns model/tool interaction", "sand")
    steps = [
        (70, 640, 680, 72, "1 · Invoke", ("InvocationContext enters DeepAgent; before-invoke Rails may add context or reject",)),
        (70, 742, 680, 72, "2 · Start task iteration", ("Task-loop budget, cancellation, follow-up and prior session state are checked",)),
        (70, 844, 680, 72, "3 · Assemble model context", ("system prompt + history + skill guidance + memory + available ability cards",)),
        (70, 946, 680, 72, "4 · Allocate and call model", ("before-model Rails → allocator [GAP: missing request may silently fall back] → provider client → response/exception Rails",)),
        (70, 1048, 680, 72, "5 · Parse response", ("text may finish the ReAct turn; tool requests enter the ability path",)),
        (70, 1150, 680, 96, "6 · Authorize and execute each ability", ("before-tool Rail enforces permission → validate arguments → ALLOW/ASK/DENY → runner", "Tool/MCP/sub-agent/workflow/SysOperation returns ToolMessage or typed exception")),
        (70, 1276, 680, 72, "7 · Consume observation", ("after-tool Rails → model observation → after-ReAct-iteration Rails",)),
        (70, 1378, 680, 42, "8 · Decide", ("continue ReAct · finish task iteration · interrupt · fail",)),
    ]
    for x, y, w, h, title, body in steps: s.node(x, y, w, h, title, body)
    for y1, y2 in [(712, 737), (814, 839), (916, 941), (1018, 1043), (1120, 1145), (1246, 1271), (1348, 1373)]: s.arrow(f"M410 {y1} V{y2}")
    s.arrow("M750 1399 H775 V780 H755", "dash"); s.text(680, 771, "next outer task iteration", "tiny")
    s.arrow("M750 1312 H770 V1084 H755", "dash"); s.text(657, 1077, "next ReAct turn", "tiny")

    s.panel(820, 575, 250, 430, "D. Rail callback envelope", "Hooks surrounding both loops", "purple")
    s.lines(840, 640, ["Invocation", "before · after", "", "Task iteration", "before · after", "", "ReAct iteration", "after", "", "Model call", "before · after · exception", "", "Tool call", "before · after · exception"], "n", 22)
    s.lines(840, 930, ["Possible actions:", "context/ability injection", "approval · interrupt · retry", "force-complete · telemetry", "ReAct after-hook: success-only"], "tiny", 14)

    s.panel(820, 1045, 250, 400, "E. Services used by a turn", "Shared contracts used by the loop", "yellow")
    services = [
        (840, 1100, "Model allocator [GAP]", ("missing requested model may use default",)),
        (840, 1170, "AbilityManager + runner", ("metadata cards · executable resources",)),
        (840, 1240, "Permission engine [GAP]", ("ALLOW/ASK/DENY · 0 builtin rules load",)),
        (840, 1310, "Workspace / SysOperation", ("private · team · worktree · sandbox",)),
        (840, 1380, "Skill + memory managers", ("prompt guidance · retrieved context",)),
    ]
    for x, y, title, body in services: s.node(x, y, 210, 56, title, body)

    s.panel(30, 1485, 1040, 230, "F. State written during and after the turn", "Operational state is deliberately split; no store is automatically AI4RnD evidence", "cyan")
    state = [
        (50, 1545, "Session state", ("messages · interrupts", "task-loop continuation")),
        (250, 1545, "Workspace state", ("files · worktree", "team/shared artifacts")),
        (450, 1545, "Execution state", ("tool/model events", "allocation + cost facts")),
        (650, 1545, "Engine checkpoint", ("graph/workflow snapshot", "SwarmFlow journal if used")),
        (850, 1545, "Memory state", ("long-term · coding · team", "retrieval indices")),
    ]
    for x, y, title, body in state: s.node(x, y, 180, 100, title, body)
    s.text(50, 1684, "AI4RnD integration requirement: convert validated runtime facts into a typed attempt receipt; never treat a final message or checkpoint as a scientific verdict.", "s")
    s.finish("07-openjiuwen-deepagent-turn-design.svg")


def openjiuwen_orchestration_design():
    s = SVG(1540, "OpenJiuwen — Orchestration and State Design", "Four orchestration mechanisms compose common execution resources but use different schedulers and durability models")

    s.panel(30, 90, 1040, 150, "Execution request before mechanism choice", "A caller supplies a bounded objective or topology; OpenJiuwen does not infer AI4RnD evidence obligations", "blue")
    for x, title, body in [
        (50, "Objective / inputs", ("messages · typed args · files",)),
        (300, "Execution policy", ("budget · timeout · isolation",)),
        (550, "Available resources", ("models · tools · members",)),
        (800, "Mechanism selector", ("agent · workflow · flow · team",)),
    ]: s.node(x, 145, 230, 70, title, body)
    s.arrow("M280 180 H295"); s.arrow("M530 180 H545"); s.arrow("M780 180 H795")

    mechanisms = [
        (30, 285, "1. Direct DeepAgent", "Adaptive task when topology is unknown locally", ("Task-loop coordinator",), ("model ↔ ability ReAct iterations",), ("session history + interrupts",), ("final message · tool artifacts",)),
        (30, 555, "2. Core Workflow / Pregel", "Known component topology and deterministic/conditional routing", ("Pregel superstep scheduler",), ("components read/write typed channels",), ("checkpointer snapshots",), ("graph outputs · interrupt state", "router receives no state argument")),
        (30, 825, "3. SwarmFlow [FENCE]", "Script-defined parallel, pipeline, map and nested phases", ("Python flow interpreter + admission",), ("agent sessions / backend calls",), ("journal/WAL + progress events", "resume is engine-API-only"), ("script return · phase/run events", "failed step may yield empty success")),
        (30, 1095, "4. Dynamic Team / NativeHarness", "Open-ended coordination with delegation and independent review", ("Leader + persistent task scheduler",), ("members · assignees · reviewers", "human/bridge roles available"), ("team task DB + member/worktree state",), ("task results · review · team stream",)),
    ]
    colors = ["sand", "green", "blue", "purple"]
    for i, (x, y, title, purpose, scheduler, workers, state, output) in enumerate(mechanisms):
        s.panel(x, y, 1040, 225, title, purpose, colors[i])
        cells = [
            (50, "Control", scheduler),
            (300, "Work unit", workers),
            (550, "Durability", state),
            (800, "Returns", output),
        ]
        for cx, ct, cb in cells: s.node(cx, y + 75, 230, 100, ct, cb)
        for cx in (280, 530, 780): s.arrow(f"M{cx} {y+125} H{cx+15}")

    s.panel(30, 1380, 1040, 105, "Common lower-level resources", "All four ultimately consume model pools, AbilityManager/runners, Rails, skills, workspace/SysOperation, permissions and memory", "yellow")
    s.text(50, 1450, "Design rule for AI4RnD: compile a ready semantic slice into one mechanism; persist the mapping between project node/attempt and the mechanism's native run/checkpoint identifiers.", "s")
    s.finish("08-openjiuwen-orchestration-state-design.svg")


def ai4rnd_control_design():
    s = SVG(1750, "AI4RnD — Planning, Binding and Execution Design", "White-box current control flow with retained product semantics and the tmux carrier marked for replacement")

    s.panel(30, 90, 1040, 170, "A. Intake and run authority", "Files currently hold the run contract and lifecycle; product meaning is independent of the worker carrier", "blue")
    intake_nodes = [
        (50, 180, "Run intake", ("objective · repo/workspace", "budget · mode hints")),
        (250, 180, "Run scaffold", ("sprint status · task graph", "artifact directories")),
        (450, 230, "Coordinator state machine", ("PM → Planner → Builder → Evaluator", "retry · timeout · quarantine")),
        (700, 170, "Artifact predicates", ("PRD · design · handoff · eval", "mtime + schema checks")),
        (890, 160, "Run projection", ("state · owner · blockers", "next action")),
    ]
    for x, w, title, body in intake_nodes: s.node(x, 150, w, 86, title, body)
    s.arrow("M230 193 H245"); s.arrow("M430 193 H445"); s.arrow("M680 193 H695"); s.arrow("M870 193 H885")

    s.panel(30, 300, 1040, 300, "B. Planning and semantic readiness", "The plan expresses meaning, dependencies, capabilities, write safety and evidence—not panes", "green")
    planning = [
        (50, 365, "Requirement / intent", ("normalized objective", "constraints + acceptance")),
        (260, 365, "Planner / compiler", ("decompose logical work", "select Capsule patterns")),
        (470, 350, "TaskGraph", ("nodes + dependencies", "Logical Operators", "required capabilities", "write scope + evidence owed")),
        (700, 365, "Graph validation", ("schema · cycles · endpoints", "topological layers")),
        (890, 365, "Readiness", ("deps + external waits", "gates + retry policy")),
    ]
    widths = [180, 180, 200, 170, 160]
    for (x, y, title, body), w in zip(planning, widths): s.node(x, y, w, 130, title, body)
    s.arrow("M230 430 H255"); s.arrow("M440 430 H465"); s.arrow("M670 430 H695"); s.arrow("M870 430 H885")
    s.node(260, 515, 600, 56, "Batch safety", ("ready nodes may run together only when dependencies, write scopes, effects and resource constraints are compatible",), fill=COLORS["yellow"])

    s.panel(30, 640, 1040, 315, "C. Capsule, Operator and worker binding", "Capability admission is a hard gate; scoring happens only after qualification", "purple")
    binding = [
        (50, 705, "Capsule loader [PARTIAL]", ("applicability · contract", "effects · composition", "verification · compatibility")),
        (260, 705, "Stage expansion [PARTIAL]", ("guard → resource", "capability → verifier", "skill/MCP plan")),
        (470, 705, "Logical Operator", ("typed action identity", "inputs/outputs", "completion + evidence")),
        (680, 705, "Candidate enumeration", ("Physical Operator registry", "role/model/runtime profiles")),
        (890, 705, "Hard admission", ("capabilities · quota", "health · capacity", "security + resources")),
    ]
    for x, y, title, body in binding: s.node(x, y, 180, 140, title, body)
    for x in (230, 440, 650, 860): s.arrow(f"M{x} 775 H{x+25}")
    s.node(260, 865, 600, 58, "Selection after admission", ("rank qualified candidates by role/model fit, skill overlap, cost/latency and current load; otherwise record no_matching_worker",), fill=COLORS["yellow"])

    s.panel(30, 995, 1040, 260, "D. Current physical carrier — rejected for the target", "The worker transport is coupled to terminal UI state and filesystem polling", "red")
    carrier = [
        (50, "Graph-node dispatcher", ("node → role/pane command",)),
        (260, "Pane readiness probe", ("capture-pane · busy markers",)),
        (470, "tmux send-keys", ("command then delayed Enter",)),
        (680, "CLI worker", ("Codex/Claude process", "writes artifact handoff")),
        (890, "Polling reconciliation", ("max mtime · status file", "infer next transition")),
    ]
    for x, title, body in carrier: s.node(x, 1060, 180, 110, title, body)
    for x in (230, 440, 650, 860): s.arrow(f"M{x} 1115 H{x+25}")
    s.text(50, 1205, "Retain the typed work packet, capability decision and artifact expectations. Replace pane focus, split send-keys/Enter, busy-marker polling and unsafe permission assumptions.", "s")

    s.panel(30, 1295, 1040, 375, "E. Return path and semantic state transition", "Artifacts do not advance the run until independent evidence and gates accept them", "yellow")
    return_path = [
        (50, 1360, "Worker handoff", ("artifacts · tests · metrics", "claimed completion")),
        (260, 1360, "Receipt / provenance", ("writer identity · hashes", "attempt + timestamps")),
        (470, 1360, "Independent evaluator", ("contract · engineering", "evidence/science · security", "cost/performance")),
        (680, 1360, "Gate ledger", ("append-only verdict", "writer attribution", "approval/repair data")),
        (890, 1360, "State transition", ("progress · repair", "replan/reframe", "blocked · done")),
    ]
    for x, y, title, body in return_path: s.node(x, y, 180, 140, title, body)
    for x in (230, 440, 650, 860): s.arrow(f"M{x} 1430 H{x+25}")
    s.arrow("M980 1500 V1605 H20 V505 H545 V480", "dash")
    s.text(350, 1595, "failed verdict produces a new attempt or versioned plan revision", "tiny")
    s.finish("09-ai4rnd-planning-execution-design.svg")


def ai4rnd_evidence_rsi_design():
    s = SVG(1640, "AI4RnD — Evidence, Data and Governed RSI Design", "How execution facts become claims and verdicts, then controlled improvement candidates")

    s.panel(30, 90, 1040, 220, "A. Evidence lineage [CURRENT RESEARCH STORE → TARGET INTEGRATION]", "The research SQLite schema supplies hashes, spans and claim links; harness-wide integration is not current", "green")
    evidence = [
        (50, "Source", ("URI/repository/dataset/run", "authority + retrieval facts")),
        (260, "Document/artifact", ("content hash", "version + parser facts")),
        (470, "Span / measurement", ("span_start · span_end", "content + content hash")),
        (680, "Evidence item", ("typed payload", "provenance + confidence")),
        (890, "Claim link", ("supports · refutes · qualifies", "link strength")),
    ]
    for x, title, body in evidence: s.node(x, 155, 180, 110, title, body)
    for x in (230, 440, 650, 860): s.arrow(f"M{x} 210 H{x+25}")

    s.panel(30, 350, 1040, 300, "B. Evaluation and gate authority", "Technical execution success, typed receipt validity, Contract satisfaction, evidence support and gate permission are five separate decisions", "yellow")
    evals = [
        (50, 415, "Receipt conformance", ("terminal state · identity", "effects · artifacts")),
        (260, 415, "Contract conformance", ("typed outputs", "pre/postconditions")),
        (470, 415, "Engineering/performance", ("tests · code quality", "benchmark · cost")),
        (680, 415, "Evidence/scientific", ("grounding · authority", "diversity · falsifiability")),
        (890, 415, "Security/lifecycle", ("policy · privacy · IP", "human review")),
    ]
    for x, y, title, body in evals: s.node(x, y, 180, 118, title, body)
    s.node(260, 560, 600, 58, "Gate ledger", ("append-only, writer-attributed verdicts; node status is a projection; corrections supersede rather than edit history",), fill=COLORS["purple"])
    for x in (140, 350, 560, 770, 980): s.arrow(f"M{x} 533 V555")

    s.panel(30, 690, 1040, 300, "C. Data foundation [TARGET]", "Today four stores are separate; target records support typed projections with distinct lifecycle rules", "cyan")
    s.node(50, 755, 250, 145, "Authoritative records", ("Contracts · TaskGraph versions", "attempts · receipts · artifacts", "claims · evidence · verdicts", "Capsule/operator versions"))
    graph_nodes = [
        (335, 745, "Concept graph", ("ideas · claims · relations",)),
        (510, 745, "Dataset graph", ("datasets · lineage · splits",)),
        (685, 745, "Code graph", ("repos · commits · artifacts",)),
        (860, 745, "Policy graph", ("rules · effects · approvals",)),
        (422, 865, "Workflow graph", ("plans · attempts · patterns",)),
        (597, 865, "Trace graph", ("events · calls · provenance",)),
        (772, 865, "Memory graph", ("retrieval units · summaries",)),
    ]
    for x, y, title, body in graph_nodes: s.node(x, y, 155, 82, title, body)
    s.arrow("M300 827 H330");
    s.text(50, 974, "Jiuwen memory/retrieval may index these projections. It must not rewrite source evidence or become the only copy of project knowledge.", "tiny")

    s.panel(30, 1030, 1040, 535, "D. Governed improvement loop", "GEPA proposes; evaluation and policy decide; promotion is versioned and reversible", "red")
    improve = [
        (50, 1095, "Trajectory + failure mining", ("receipts · gates · cost", "hard cases · regressions")),
        (260, 1095, "GEPA candidate search", ("propose versioned change", "respect eval/spend/wall limits")),
        (470, 1095, "Frozen-policy check", ("cannot relax secrets", "git push · destructive shell", "payments/external writes")),
        (680, 1095, "Isolated evaluation", ("sandbox · holdout · replay", "golden set · A/B")),
        (890, 1095, "Approval", ("evaluator verdict", "human for governed risk")),
    ]
    for x, y, title, body in improve: s.node(x, y, 180, 135, title, body)
    for x in (230, 440, 650, 860): s.arrow(f"M{x} 1162 H{x+25}")
    s.node(210, 1280, 240, 112, "Promotion", ("new version + registry update", "future runs use it", "in-flight runs stay pinned")),
    s.node(500, 1280, 240, 112, "Post-promotion monitoring", ("quality/cost drift", "policy and regression alarms")),
    s.node(790, 1280, 240, 112, "Rollback / rejection", ("restore prior version", "record reason and evidence"))
    s.arrow("M980 1230 V1275 H915"); s.arrow("M450 1336 H495"); s.arrow("M740 1336 H785")
    s.text(50, 1435, "Improvement subjects", "h")
    subjects = ["prompt/text", "routing/model policy", "Capsule/operator", "TaskGraph pattern", "evaluator/reward", "memory/retrieval", "model weights", "data/benchmark"]
    for i, subject in enumerate(subjects):
        x = 50 + (i % 4) * 250; y = 1460 + (i // 4) * 48
        s.rect(x, y, 230, 34, "gray", radius=6); s.text(x + 12, y + 22, subject, "s")
    s.text(50, 1554, "Current maturity: GEPA text-artifact path is isolated; Capsule on-ramp is partial; no data/benchmark candidate type; the eight-surface loop is not wired.", "tiny")
    s.finish("10-ai4rnd-evidence-data-rsi-design.svg")


def integration_contract_design():
    s = SVG(
        1900,
        "AI4RnD × OpenJiuwen — Integration Contract Design",
        "Five normative boundary objects preserve AI4RnD meaning while OpenJiuwen executes bounded attempts",
    )
    s.badge(30, 78, "TARGET CONTRACT", "purple", 130)
    s.badge(175, 78, "REUSE WITH FENCE", "sand", 145)
    s.badge(335, 78, "CURRENT GAP", "red", 112)
    s.text(470, 94, "Solid arrows: control and execution · dashed arrows: facts, evidence and reconciliation", "tiny")

    s.panel(
        30, 120, 1040, 245,
        "1. AI4RnD semantic authority",
        "Only verified semantic readiness can mint a PlanSlice; runtime availability never defines product meaning",
        "purple",
    )
    semantic = [
        (50, "Contract version", ("objective · scope · budget", "acceptance · evidence owed")),
        (255, "TaskGraph version", ("ready nodes · dependencies", "write scope · repair lineage")),
        (460, "Capsule + action", ("Capsule version · effects", "Logical Operator identity")),
        (665, "Readiness validator", ("inputs · gates · budget", "schema · capability feasibility")),
        (870, "PlanSlice", ("slice_id · plan_version · digest", "operator nodes · dep/order edges")),
    ]
    for x, title, body in semantic: s.node(x, 190, 180, 110, title, body)
    for x in (230, 435, 640, 845): s.arrow(f"M{x} 245 H{x+20}")
    s.text(50, 335, "Invariant: the same idempotency key with a different content digest is a hard conflict; a replan creates a new plan/slice version.", "s")

    s.panel(
        30, 405, 1040, 335,
        "2. Integration bridge — admission, binding and compilation",
        "The bridge translates and validates; it may not invent meaning, relax policy, or substitute an unqualified executor",
        "yellow",
    )
    bridge = [
        (50, "Resolve Capsule", ("pin version + guards", "enforce effects + secrets rule")),
        (255, "Enumerate candidates", ("operators · models · tools", "resources · skills · health")),
        (460, "BindingDecision", ("qualified resource selection", "exact bindings or STALL · no mechanism")),
        (665, "Compile mechanism", ("agent · graph · flow · team", "emit normalized common spec")),
        (870, "ExecutionSpec", ("attempt · epoch · mechanism", "policy/guard digest · typed I/O")),
    ]
    for x, title, body in bridge: s.node(x, 480, 180, 118, title, body)
    for x in (230, 435, 640, 845): s.arrow(f"M{x} 539 H{x+20}")
    s.rect(50, 630, 980, 76, "cyan", radius=8)
    s.text(64, 653, "Bridge mapping — authoritative cross-system lineage", "n")
    s.text(64, 673, "project · slice · binding · execution · attempt ↔ native run/checkpoint · idempotency key · attempt lease epoch", "s")
    s.text(64, 691, "Every contract: same explicit key + digest deduplicates; same key + different digest hard-conflicts.", "tiny")
    s.arrow("M960 300 V400", "dash")

    s.panel(
        30, 780, 1040, 305,
        "3. OpenJiuwen native attempt",
        "OpenJiuwen owns bounded physical execution and operational recovery—not Contract satisfaction, evidence truth or gate permission",
        "sand",
    )
    s.node(50, 850, 150, 105, "Attempt admission", ("idempotency · lease epoch", "budget · timeout · cancel"))
    s.node(230, 850, 150, 105, "Mechanism dispatch", ("read spec discriminator", "invoke exactly one option"))
    alternatives = [
        (410, "DeepAgent", ("adaptive bounded turn", "ReAct + task loop")),
        (565, "Workflow / Pregel", ("known topology", "checkpoint + interrupt")),
        (720, "SwarmFlow [FENCE]", ("parallel / pipeline / map", "empty-success gap")),
        (875, "Dynamic Team", ("delegation · tasks", "review + remediation")),
    ]
    for x, title, body in alternatives: s.node(x, 850, 140, 105, title, body)
    s.arrow("M200 902 H225")
    s.parts.append('<path d="M380 902 H395 V830 H945" stroke="#475569" stroke-width="1.7" fill="none"/>')
    for x in (480, 635, 790, 945): s.arrow(f"M{x} 830 V845")
    s.text(712, 817, "SELECT EXACTLY ONE MECHANISM", "tag", anchor="middle")
    s.rect(50, 985, 980, 70, "blue", radius=8)
    s.text(64, 1004, "Shared resources and derived attempt state", "n")
    s.text(64, 1026, "code/tools · worktree · MCP · sandbox · native run/checkpoint · progress · cancel acknowledgement · retry counter", "s")
    s.text(64, 1044, "Resume keeps the attempt only with checkpoint continuity; otherwise mint a new attempt. Runtime completion cannot release dependencies.", "tiny")
    s.arrow("M960 706 V775", "flow")

    s.panel(
        30, 1125, 1040, 325,
        "4. Typed return and independent assurance",
        "Execution facts become product truth only after receipt validation, independent evaluation and an authoritative gate record",
        "green",
    )
    assurance = [
        (50, "AttemptReceipt", ("attempt + epoch + native run", "runtime_outcome enum or absent", "receipt_disposition separate")),
        (300, "Receipt validator", ("identity · digest · lineage", "VALID · INVALID · QUARANTINED", "RECONCILING · CONFLICT")),
        (550, "Independent evaluators", ("Contract · engineering · cost", "evidence/science · security", "writer ≠ verifier")),
        (800, "EvaluationGateRecord", ("evaluation findings + gate disposition", "one immutable envelope", "duplicate delivery: no transition")),
    ]
    for x, title, body in assurance: s.node(x, 1200, 230, 145, title, body)
    for x in (280, 530, 780): s.arrow(f"M{x} 1272 H{x+15}")
    s.rect(50, 1375, 980, 42, "red", radius=8)
    s.text(64, 1401, "One terminal receipt per attempt+epoch; identical redelivery deduplicates; contradiction quarantines/reconciles and never overwrites.", "s")
    s.arrow("M970 1051 V1120", "dash")

    s.panel(
        30, 1490, 1040, 340,
        "5. Product outcomes and recovery",
        "Only the gate/reconciliation authority selects an outcome; every transition is durable, attributable and versioned",
        "cyan",
    )
    outcomes = [
        (50, 1555, "Release", ("gate permits progress", "release dependants"), "green"),
        (250, 1555, "Repair", ("same plan node", "new attempt + lineage"), "yellow"),
        (450, 1555, "Replan", ("new TaskGraph version", "new PlanSlice digest"), "purple"),
        (650, 1555, "Stall / stop / quarantine", ("named reason · never progress", "human may resolve or close"), "red"),
        (850, 1555, "Human gate", ("approval dossier", "record decision"), "blue"),
    ]
    for x, y, title, body, fill in outcomes: s.node(x, y, 180, 92, title, body, fill=COLORS[fill])
    recovery = [
        (50, "Cancel", ("persist intent → runtime ack", "quarantine late result")),
        (300, "Resume", ("same attempt only if", "checkpoint continuity holds")),
        (550, "Restart", ("UNKNOWN → RECONCILING", "until native state matches")),
        (800, "Fence stale work", ("lease epoch rejects old result", "new attempt supersedes")),
    ]
    for x, title, body in recovery: s.node(x, 1690, 230, 92, title, body)
    s.text(50, 1812, "Five distinct decisions: runtime outcome ≠ receipt disposition ≠ Contract satisfaction ≠ evidence support ≠ gate permission.", "n")

    s.finish("11-integration-contracts-design.svg")


if __name__ == "__main__":
    capsule_design(); openjiuwen_turn_design(); openjiuwen_orchestration_design()
    ai4rnd_control_design(); ai4rnd_evidence_rsi_design(); integration_contract_design()
