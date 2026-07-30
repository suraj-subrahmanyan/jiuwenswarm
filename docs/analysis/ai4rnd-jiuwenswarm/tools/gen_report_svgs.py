#!/usr/bin/env python3
# coding: utf-8
"""Generators for the canonical report's diagram set.

Every diagram is deterministic, theme-aware SVG (see svgkit.py). The offline
Mermaid layout engine cannot hold lanes, cycles or status annotations steady
at this density, and the standalone report must carry no JavaScript, so all
report diagrams are authored here.

Usage: python3 tools/gen_report_svgs.py <name>   (or `all` to list names)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import SVG

RED = "var(--primary-ink)"
AMBER = "var(--blocked)"
MUT = "var(--subtle)"


# ---------------------------------------------------------------- D1 intended
def intended():
    s = SVG(1190, 596, "Intended AI4RnD product architecture", "ki")
    s.band(8, 92, "Engagement — how people and signals reach the product, and how it reports back")
    s.node(40, 40, 250, ["Channels · UI · CLI", "requests · clues · material"], 44)
    s.node(330, 40, 250, ["Project visibility", "progress · gates · budgets"], 44)
    s.node(620, 40, 250, ["Approvals", "contracts · gates · improvements"], 44)
    s.node(910, 40, 240, ["Accounts · configuration", "installers · settings"], 44)

    s.band(108, 116, "Project control — one authority for meaning, readiness and completion")
    s.node(40, 144, 260, ["Intention Compiler", "need → confirmed Contract"], 56)
    s.node(340, 144, 260, ["Planner", "Contract → semantic TaskGraph", "claims · dependencies · acceptance"], 56)
    s.node(640, 144, 240, ["Readiness & run state", "what may start · what truly", "succeeded · repair & replan"], 56)
    s.node(920, 144, 230, ["Gates & closure", "verdicts · delivery ·", "authorized distribution"], 56)

    s.band(232, 116, "Capability & verification foundation — governed, versioned, improvable")
    s.node(40, 268, 300, ["Capability Capsules", "identity · contract · effects ·", "compatibility · certification"], 56)
    s.node(380, 268, 250, ["Logical Operators", "stable callable actions", "invoked by plan nodes"], 56)
    s.node(670, 268, 230, ["Evaluator families", "conformance · engineering · perf ·", "security · factuality · human"], 56)
    s.node(940, 268, 210, ["GEPA + governed RSI", "candidates · budgets · frozen", "policy · approval · rollback"], 56)

    s.band(356, 104, "Execution abstraction — the product never binds to one engine")
    s.node(40, 388, 540, ["Logical Operator invocation → any qualified physical executor",
                          "agents · pipelines · staged workflows · teams · sandboxes · deterministic tools"], 56)
    s.node(620, 388, 530, ["Binding rules", "declared effects enforced · permitted/forbidden executors · honest stall"], 56)

    s.band(468, 104, "Durable product state — outlives every session and run")
    s.node(40, 500, 270, ["Project records", "Contract & TaskGraph versions"], 52)
    s.node(350, 500, 270, ["Evidence & verdict ledgers", "append-only · attributed"], 52)
    s.node(660, 500, 240, ["Knowledge graphs", "concept · dataset · code · policy ·", "workflow · trace · memory"], 52)
    s.node(940, 500, 210, ["Improvement history", "versions · promotions ·", "rollbacks"], 52)

    for x in (165, 470, 760, 1035):
        s.path(f"M{x} 84 L{x} 108")
    for x in (170, 470, 760, 1035):
        s.path(f"M{x} 200 L{x} 232")
    for x in (310, 885):
        s.path(f"M{x} 324 L{x} 356")
    for x in (310, 885):
        s.path(f"M{x} 444 L{x} 468", dashed=True)
    return s.out()


# ------------------------------------------------------------- D2 current A4
def cur_a4():
    s = SVG(1190, 560, "Current AI4RnD implementation, as verified", "ka")
    s.band(8, 88, "Carrier — how it runs today")
    s.node(40, 40, 300, ["tmux cockpit + polling coordinator", "shell state machine drives panes"], 44,
           tag="ACTIVE · REJECTED IN TARGET", tag_fill=AMBER)
    s.node(380, 40, 360, ["graph_scheduler (4,189 lines)", "readiness · batching · retries · binding, fused with plan semantics"], 44,
           tag="ACTIVE · RETIRES", tag_fill=AMBER)
    s.node(780, 40, 370, ["TaskGraph persistence", "task_graph_io · state_io"], 44, tag="ACTIVE")

    s.band(104, 88, "Research pipeline")
    s.node(40, 136, 270, ["Sources & extractors", "arXiv · HF · GitHub · YouTube"], 44, tag="ACTIVE")
    s.node(350, 136, 250, ["Survey & claim compiler", "planner · sections · claims"], 44, tag="ACTIVE")
    s.node(640, 136, 250, ["Grounding check", "measured 0.25 precision"], 44, tag="BROKEN", tag_fill=RED)
    s.node(930, 136, 220, ["Report capsules", "plan · draft · publish"], 44, tag="ACTIVE")

    s.band(200, 88, "Governance assets — the parts the target keeps")
    s.node(40, 232, 250, ["Evidence ledger", "citation spans, runs standalone"], 44, tag="ACTIVE")
    s.node(330, 232, 250, ["Gate ledger", "append-only · writer-attributed"], 44, tag="ACTIVE")
    s.node(620, 232, 250, ["Capsule registry", "42 manifests · 35 registered"], 44, tag="ACTIVE / UNWIRED", tag_fill=AMBER)
    s.node(910, 232, 240, ["GEPA optimizer", "budgets · frozen policy · promote"], 44, tag="ACTIVE / UNWIRED", tag_fill=AMBER)

    s.band(296, 108, "Implemented but not connected")
    s.node(40, 332, 260, ["Benchmark suites", "no lane invokes them"], 48, tag="UNWIRED", tag_fill=AMBER)
    s.node(340, 332, 280, ["Capsule → runner bindings", "operator_compatibility declared,", "no binder consumes it"], 48, tag="UNWIRED", tag_fill=AMBER)
    s.node(660, 332, 230, ["Operator profiles", "agent-actors config only"], 48, tag="SPECIFIED", tag_fill=AMBER)
    s.node(930, 332, 220, ["Intent engine adapter", "routing shell hooks"], 48, tag="UNWIRED", tag_fill=AMBER)

    s.band(412, 116, "Absent — verified by exhaustive search", title_fill=RED)
    for i, (t1, t2) in enumerate([
            ("Idea Card", "no schema anywhere"),
            ("Falsifiability stage", "2 mentions, no gate"),
            ("Typed knowledge graphs", "all seven missing"),
            ("Account subsystem", "none"),
            ("RSI governance loop", "no proposals · no inbox")]):
        s.node(40 + i * 228, 448, 208, [t1, t2], 48, tag="ABSENT", tag_fill=RED, dashed=True)
    return s.out()


# ------------------------------------------------------------ D3 foundation
def foundation():
    s = SVG(1190, 520, "JiuwenSwarm and OpenJiuwen, as verified", "kf")
    s.band(8, 88, "Clients")
    s.node(40, 40, 250, ["Web UI · TUI · CLI"], 44)
    s.node(330, 40, 300, ["9 messaging channels", "incl. WeChat · Discord"], 44)
    s.node(670, 40, 250, ["Agent-to-agent peers"], 44)

    s.band(104, 96, "JiuwenSwarm — application layer")
    s.node(40, 140, 270, ["Gateway", "channel adapters · routing"], 48)
    s.node(350, 140, 270, ["Agent server", "sessions · modes · skills"], 48)
    s.node(660, 140, 230, ["Skill retrieval", "ranks — never refuses"], 48, tag="GAP FOR RESEARCH", tag_fill=AMBER)
    s.node(930, 140, 220, ["Workspace & config", "templates · settings"], 48)

    s.band(208, 148, "OpenJiuwen — runtime library")
    s.node(40, 240, 210, ["DeepAgent", "single-agent turns"], 48)
    s.node(280, 240, 230, ["Core Workflow", "durable staged graphs,", "checkpoints · interrupts"], 48)
    s.node(540, 240, 230, ["SwarmFlow", "scripted pipelines,", "replayable journal"], 48)
    s.node(800, 240, 170, ["Dynamic Team", "leader + roster"], 48)
    s.node(1000, 240, 150, ["Code mode", "worktrees"], 48)
    s.node(40, 300, 280, ["Team services", "task board with dependencies ·", "shared memory · reliability detectors"], 48)
    s.node(360, 300, 280, ["agent_evolving", "Trainer · Updater · metrics · RL —", "one wired subject today"], 48, tag="NARROWLY WIRED", tag_fill=AMBER)
    s.node(680, 300, 240, ["Model pool + allocator", "silent fallback on unknown name"], 48, tag="DEFECT", tag_fill=RED)
    s.node(950, 300, 200, ["Graph memory", "unreferenced by the app"], 48, tag="UNWIRED", tag_fill=AMBER)

    s.band(364, 92, "Shared infrastructure")
    s.node(40, 396, 260, ["Checkpointer", "sqlite, process default"], 44)
    s.node(340, 396, 260, ["jiuwenbox sandbox", "bwrap / cgroups"], 44)
    s.node(640, 396, 240, ["Observability", "spans · progress events"], 44)
    s.node(920, 396, 230, ["Guardrail rules tier", "loads 0 rules — orphaned file"], 44, tag="DEFECT", tag_fill=RED)

    s.band(464, 48, "")
    s.label(600, 492, "Verified defects that shape the integration: silent model substitution · "
                      "resume advertised but rejected · failed steps return empty and the run reports success · "
                      "executor typing accepted but unread", anchor="middle", size=11)
    for x in (165, 480, 795):
        s.path(f"M{x} 84 L{x} 104")
    for x in (175, 485, 775, 1040):
        s.path(f"M{x} 188 L{x} 208")
    for x in (170, 470, 760, 1035):
        s.path(f"M{x} 356 L{x} 364")
    return s.out()


# ---------------------------------------------------------------- D4 target
def target():
    s = SVG(1190, 600, "Target integrated architecture with sourcing decisions", "kt")
    s.band(8, 96, "JiuwenSwarm — application foundation")
    s.node(40, 42, 240, ["Channels · Gateway"], 44, tag="REUSE")
    s.node(320, 42, 240, ["Sessions · workspace"], 44, tag="REUSE")
    s.node(600, 42, 250, ["UI shell · config · packaging"], 44, tag="REUSE + EXTEND")
    s.node(890, 42, 260, ["Project & registry views", "approvals · improvements inbox"], 44, tag="BUILD", tag_fill=RED)

    s.band(112, 116, "AI4RnD — product core (permanent)")
    s.node(40, 146, 250, ["Project subsystem", "Contract & TaskGraph versions"], 56, tag="BUILD", tag_fill=RED)
    s.node(330, 146, 250, ["Intention Compiler · Planner", "ported research semantics"], 56, tag="PORT + ADAPT")
    s.node(620, 146, 250, ["Capsules · Logical Operators", "registry · certification · effects"], 56, tag="PORT + EXTEND")
    s.node(910, 146, 240, ["Evidence · gates · evaluators", "entailment rebuilt & measured"], 56, tag="PORT + BUILD", tag_fill=RED)

    s.band(236, 116, "Integration bridge — the only bilingual component")
    s.node(40, 270, 260, ["Binding", "capsule + executor + model,", "honest stall — never substitutes"], 56, tag="BUILD", tag_fill=RED)
    s.node(340, 270, 250, ["Compiler & dispatch", "ready sub-plan → engine spec,", "resume · cancel"], 56, tag="BUILD", tag_fill=RED)
    s.node(630, 270, 250, ["Receipt builder", "typed receipts + provenance,", "empty result ⇒ failed attempt"], 56, tag="BUILD", tag_fill=RED)
    s.node(920, 270, 230, ["Engine adapters", "SwarmFlow backend seam ·", "workflow components"], 56, tag="COMPOSE")

    s.band(360, 108, "OpenJiuwen — execution engines")
    s.node(40, 392, 250, ["Core Workflow / Pregel"], 52, tag="REUSE")
    s.node(320, 392, 220, ["SwarmFlow engine", "via its backend seam"], 52, tag="REUSE")
    s.node(570, 392, 250, ["DeepAgent · Team · worktrees", "task board · reliability · memory"], 52, tag="REUSE")
    s.node(850, 392, 150, ["Model routing"], 52, tag="ADAPTER", tag_fill=AMBER)
    s.node(1030, 392, 120, ["Sandbox"], 52, tag="REUSE")

    s.band(476, 112, "Durable product state — AI4RnD-owned, project-scoped")
    s.store(40, 508, 240, ["Project store", "Contracts · plans · budgets"])
    s.store(320, 508, 250, ["Attempt lineage", "receipts · cancels · provenance"])
    s.store(610, 508, 240, ["Evidence & verdicts", "append-only"])
    s.store(890, 508, 260, ["Knowledge & improvements", "projections · versions"])

    for x in (165, 445, 745, 1020):
        s.path(f"M{x} 86 L{x} 112")
    for x in (170, 455, 745, 1030):
        s.path(f"M{x} 202 L{x} 236")
    for x in (170, 465, 755, 1035):
        s.path(f"M{x} 326 L{x} 360")
    for x in (160, 430, 700, 1020):
        s.path(f"M{x} 444 L{x} 476", dashed=True)
    s.legend(586, [("solid", "control"), ("dashed", "state & evidence"),
                   (None, "tags: REUSE · COMPOSE (adapter) · EXTEND · PORT · ADAPT · BUILD")])
    return s.out()


# ---------------------------------------------------------------- D5 master
def master():
    s = SVG(1190, 768, "End-to-end functional architecture", "km")
    s.gutter_band(8,  70, "", ["People &", "channels"])
    s.gutter_band(86, 186, "", ["Project control", "— AI4RnD"])
    s.gutter_band(280, 80, "", ["Capability", "governance", "— AI4RnD"])
    s.gutter_band(368, 96, "", ["Integration", "bridge"])
    s.gutter_band(472, 84, "", ["Execution", "— OpenJiuwen"])
    s.gutter_band(564, 168, "", ["Durable product", "state — AI4RnD"])

    # lane 1
    s.node(226, 24, 220, ["Researcher · teams"], 40)
    s.node(486, 24, 230, ["Channels · Web UI · CLI"], 40)
    s.node(900, 24, 250, ["Approvals & stall resolution"], 40)
    # lane 2 row A
    s.node(146, 104, 200, ["Project", "create — or retrieve & resume"], 52)
    s.node(386, 104, 220, ["Intention → Contract v1", "ambiguity resolved · confirmed"], 52)
    s.node(646, 104, 230, ["Planner → TaskGraph vN", "claims · deps · acceptance"], 52)
    s.node(886, 104, 200, ["Semantic readiness", "deps · budget · scope"], 52)
    # lane 2 row B
    s.node(146, 200, 220, ["Close & deliver", "freeze · authorize"], 52)
    s.node(646, 200, 230, ["Repair · replan → vN+1", "artifact fix, or plan revision"], 52)
    s.node(906, 200, 200, ["Gates", "verdict per claim"], 52)
    # lane 3
    s.node(146, 300, 340, ["Capability Capsules · Logical Operators", "registry · versions · effects · compatibility"], 52)
    s.node(546, 300, 300, ["Evaluator families & gate policy", "writer ≠ verifier"], 52)
    # lane 4
    s.node(146, 392, 250, ["Binding", "capsule + executor + model —", "stall if nothing qualifies"], 56)
    s.node(446, 392, 220, ["Compile & dispatch", "ready sub-plan → engine spec"], 56)
    s.node(716, 392, 300, ["Receipt builder", "typed receipt + provenance —", "an empty result is a failed attempt"], 56)
    # lane 5
    s.node(146, 492, 600, ["Core Workflow · SwarmFlow · DeepAgent · Team · worktrees"], 44)
    s.node(796, 492, 280, ["External models · tools · sources"], 44)
    # lane 6
    s.store(146, 596, 210, ["Project store", "Contract vN · TaskGraph vN"])
    s.store(396, 596, 210, ["Attempt lineage", "receipts · cancels"])
    s.store(666, 596, 210, ["Evidence · verdicts", "append-only"])
    s.store(916, 596, 230, ["Knowledge graphs", "typed projections"])
    s.node(446, 672, 320, ["GEPA + governed RSI", "candidates · budgets · frozen policy · approval"], 48)

    P, L = s.path, s.label
    # intake
    P("M446 44 L486 44")
    P("M560 64 L560 82 L246 82 L246 104");            L(410, 96, "a need — request · clue · material", bold=True)
    P("M496 104 L496 64", both=True);                  L(504, 88, "confirm Contract", anchor="start")
    # plan row
    P("M346 130 L386 130")
    P("M606 130 L646 130");                            L(626, 122, "")
    P("M876 130 L886 130")
    P("M966 156 L966 200");                            L(974, 182, "claim decided?", anchor="start")
    P("M906 226 L876 226");                            L(891, 218, "fail")
    P("M761 200 L761 156");                            L(769, 182, "vN+1", anchor="start")
    P("M930 252 L930 264 L256 264 L256 252");          L(590, 260, "all claims decided — Contract satisfied", bold=True)
    P("M146 220 L138 220 L138 44 L226 44");            L(146, 90, "Deliverable", bold=True, anchor="start", rotate=90)
    P("M1106 214 L1120 214 L1120 64", dashed=True);    L(1128, 150, "human approval", rotate=90)
    # readiness -> binding
    P("M960 156 L960 168 L516 168 L516 380 L320 380 L320 392")
    L(700, 162, "ready step — Logical Operator request + capability requirement", bold=True)
    # governance feeds
    P("M280 352 L280 392");                            L(288, 376, "qualified capsule + executor", anchor="start")
    P("M700 300 L700 276 L1006 276 L1006 252", dashed=True); L(850, 270, "evaluation policy")
    # bridge & engines
    P("M396 420 L446 420");                            L(421, 412, "spec")
    P("M556 448 L556 492");                            L(564, 474, "run · resume · cancel", anchor="start")
    P("M746 514 L796 514")
    P("M770 492 L770 470 L820 470 L820 448");          L(830, 474, "receipts + artifacts", anchor="start")
    # verified return, right margin
    P("M1016 420 L1148 420 L1148 172 L1040 172 L1040 156")
    L(1162, 296, "verified step state — empty ⇒ failed", bold=True, rotate=90)
    # state writes
    P("M146 130 L128 130 L128 586 L210 586 L210 596", dashed=True)
    L(120, 360, "Contract · plan versions · budgets", rotate=-90)
    P("M866 448 L866 584 L501 584 L501 596", dashed=True)
    P("M866 584 L770 584 L770 596", dashed=True);      L(690, 578, "typed receipts · evidence records")
    P("M1090 252 L1090 560 L830 560 L830 596", dashed=True); L(1098, 400, "Gate Verdicts", rotate=90)
    P("M876 622 L916 622", dashed=True);               L(896, 648, "projections", size=10)
    # improvement loop
    P("M501 648 L501 672", dashed=True)
    P("M740 648 L740 672", dashed=True)
    P("M766 696 L1176 696 L1176 364 L346 364 L346 352", dashed=True)
    L(960, 688, "governed promotion — approved versions govern future runs", bold=True)
    s.legend(748, [("solid", "control / execution"), ("dashed", "state · evidence · improvement"),
                   (None, "bold = hand-off objects")])
    return s.out()


# ---------------------------------------------------------------- D6 capsule
def capsule():
    s = SVG(1190, 470, "Capability Capsule anatomy", "kc")
    s.band(8, 220, "One Capsule — a governed capability identity (all 42 existing manifests carry every section)")
    rows = [
        ("Applicability", "task types · positive and negative signals"),
        ("Typed contract", "inputs · outputs · pre/postconditions · invariants"),
        ("Declared effects", "read · write · execute · network · cost · risk"),
        ("Composition", "consumes · produces · compatible · incompatible · ordering"),
        ("Executor compatibility", "permitted and forbidden physical operators"),
        ("Verification", "self-check · external verifier · pass conditions"),
        ("Provenance & certification", "owner · origin · certified status"),
        ("Versions & history", "lifecycle · evaluation & performance record"),
    ]
    for i, (a, b) in enumerate(rows):
        x = 40 + (i % 4) * 285
        y = 44 + (i // 4) * 66
        tag = "TO ADD" if a.startswith("Versions") else None
        s.node(x, y, 265, [a, b], 56, tag=tag, tag_fill=AMBER)
    s.label(600, 200, "Plan nodes call Logical Operators directly; the Capsule governs which executor may serve them, "
                      "under which effects, verified by whom — it never hides the plan.", anchor="middle")

    s.band(268, 120, "Execution bindings beneath the Capsule — implementation detail, never identity")
    for i, (a, b) in enumerate([("Skills", "prompt packages"), ("Tools & MCP", "typed calls"),
                                ("Agents & teams", "DeepAgent · Team"), ("Models", "pool entries"),
                                ("Data & secrets", "refs, never inline")]):
        s.node(40 + i * 228, 306, 208, [a, b], 52)
    s.path("M600 228 L600 268")
    s.label(612, 252, "binds to — replaceable without changing the Capsule", anchor="start")

    s.band(404, 54, "")
    s.label(600, 436, "A JiuwenSwarm skill is one possible binding. It has a name, a description and a prompt — "
                      "none of the eight governed sections above. The Capsule is the product object; bindings are parts.",
            anchor="middle")
    return s.out()


# ------------------------------------------------------------------ D7 gepa
def gepa():
    s = SVG(1190, 466, "GEPA and the governed improvement loop", "kg")
    s.node(40, 36, 230, ["Performance history", "attempts · evidence · verdicts"], 52)
    s.node(310, 36, 300, ["GEPA candidate engine", "typed candidates: skill · capsule ·", "routing policy · rewrite rules · cost model"], 52, tag="EXISTS · UNWIRED", tag_fill=AMBER)
    s.node(650, 36, 250, ["Budgets & stoppers", "spend · evals · walltime ·", "plateau · stop-file — dry-run default"], 52, tag="EXISTS")
    s.node(940, 36, 210, ["Frozen-policy check", "rejects any relaxation"], 52, tag="EXISTS")
    s.path("M270 62 L310 62", dashed=True)
    s.path("M610 62 L650 62")
    s.path("M900 62 L940 62")

    s.node(940, 186, 210, ["Rejected", "before evaluation"], 48)
    s.node(600, 186, 300, ["Isolated evaluation", "candidates run through the same bridge", "and engines as real work — never in place"], 52)
    s.node(310, 186, 250, ["Human approval", "Improvements inbox"], 52)
    s.path("M1045 88 L1045 186");   s.label(1053, 142, "relaxes a frozen rule", anchor="start", size=10.5)
    s.path("M870 88 L790 186");     s.label(806, 142, "clean")
    s.path("M600 212 L560 212")
    s.path("M400 238 L400 286 L1010 286 L1010 234");  s.label(700, 280, "declined")

    s.node(40, 336, 260, ["Promoter", "sha256-checksummed · atomic ·", "tmp/production path guards"], 52, tag="EXISTS")
    s.node(340, 336, 230, ["Registry & config", "new capsule / prompt /", "routing / evaluator versions"], 52)
    s.node(610, 336, 230, ["Monitoring", "regression watch"], 52)
    s.node(880, 336, 270, ["Rollback", "restores the prior version, checksummed"], 52, tag="EXISTS")
    s.path("M370 238 L370 310 L170 310 L170 336");    s.label(272, 304, "approved")
    s.path("M300 362 L340 362")
    s.path("M570 362 L610 362", dashed=True)
    s.path("M840 362 L880 362");                      s.label(860, 354, "regression", size=10.5)
    s.path("M1015 388 L1015 414 L455 414 L455 388");  s.label(735, 408, "restored version re-registers")
    s.label(595, 436, "Evaluation/training substrate reused from OpenJiuwen (Trainer · Updater · judge metrics · RL) via Operator-protocol adapters.",
            anchor="middle", size=11)
    s.label(595, 452, "The improvement engine is GEPA; the machinery that tests its candidates is the machinery that runs real work. In-flight projects pin versions.",
            anchor="middle", size=11)
    return s.out()


DIAGRAMS = {"intended": intended, "cur_a4": cur_a4, "foundation": foundation,
            "target": target, "master": master, "capsule": capsule, "gepa": gepa}

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "all"
    if name == "all":
        print("\n".join(DIAGRAMS))
    else:
        print(DIAGRAMS[name]())
