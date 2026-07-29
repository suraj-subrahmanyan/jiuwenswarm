# Diagram Index

All diagrams are Mermaid, rendered inline by GitHub/GitCode. Each is reproduced here as a
standalone reference; several also appear in context in the analysis documents.

| # | Diagram | Also in |
|---|---|---|
| 1 | [JiuwenSwarm high-level architecture](#1-jiuwenswarm-high-level-architecture) | [01](../01-jiuwenswarm-architecture.md) §2 |
| 2 | [AI4RnD high-level architecture](#2-ai4rnd-high-level-architecture) | [02](../02-ai4rnd-architecture.md) §2 |
| 3 | [JiuwenSwarm execution workflow](#3-jiuwenswarm-execution-workflow) | [03](../03-workflow-traces.md) §1, §4 |
| 4 | [AI4RnD execution workflow](#4-ai4rnd-execution-workflow) | [03](../03-workflow-traces.md) §1, §4 |
| 5 | [JiuwenSwarm swarm assembly](#5-jiuwenswarm-swarm-assembly-pipeline) | [01](../01-jiuwenswarm-architecture.md) §3.4 |
| 6 | [AI4RnD sprint state machine](#6-ai4rnd-sprint-state-machine) | [02](../02-ai4rnd-architecture.md) §4.1 |
| 7 | [AI4RnD capability routing](#7-ai4rnd-capability-routing-decision-tree) | [03](../03-workflow-traces.md) §3 |
| 8 | [AI4RnD research pipeline](#8-ai4rnd-research-pipeline) | [02](../02-ai4rnd-architecture.md) §8.1 |
| 9 | [Component mapping](#9-component-mapping) | [04](../04-component-comparison.md) |
| 10 | [Current integration boundary](#10-current-integration-boundary) | — |
| 11 | [Recommended target architecture](#11-recommended-target-architecture) | [08](../08-recommended-architecture.md) §1 |
| 12 | [Proposed end-to-end functional workflow](#12-proposed-end-to-end-functional-workflow) | — |
| 13 | [Verification comparison](#13-verification-model-comparison) | [03](../03-workflow-traces.md) §6 |
| 14 | [Extension surface map](#14-jiuwenswarm-extension-surface-map) | [06](../06-integration-challenges.md) §1 |

---

## 1. JiuwenSwarm high-level architecture

```mermaid
flowchart TB
    subgraph Clients
        WEB["Web UI :5173"]
        TUI["jiuwenswarm-tui"]
        DESK["Desktop (pywebview)"]
        IM["9 IM platforms"]
        ACP["ACP / A2A peers"]
    end
    subgraph GWP["Gateway process"]
        CM["ChannelManager"]
        IMP["im_pipeline"]
        MH["MessageHandler"]
        CRON["Cron scheduler"]
    end
    subgraph ASP["AgentServer process"]
        WS["agent_ws_server (WS RPC)"]
        AM["AgentManager"]
        ADPT["agent_adapter"]
        TM["TeamManager"]
        SM["SkillManager"]
        SESS["Session store"]
        SYM["Symphony"]
        AH["Auto Harness"]
        EXT["Extension registry"]
    end
    subgraph OJ["openjiuwen (external package)"]
        DA["DeepAgent · ReAct + task loop"]
        RAILS["Rail lifecycle"]
        PERM["Permission engine"]
        TOOLS["Built-in tools"]
        SUBA["Sub-agents"]
    end
    subgraph BOX["jiuwenbox sandbox"]
        SBX["bwrap · cgroup · network policy"]
    end
    WEB & TUI & DESK & IM & ACP --> CM --> IMP --> MH
    CRON --> MH
    MH -->|"E2A over WS"| WS
    WS --> AM --> ADPT --> DA
    ADPT --> TM & SM
    WS --> SESS & SYM & AH & EXT
    DA --> RAILS & PERM & TOOLS & SUBA
    ADPT -.->|"/sandbox enable"| SBX
```

## 2. AI4RnD high-level architecture

```mermaid
flowchart TB
    subgraph HUMAN["Human surfaces"]
        CLI["solar-harness.sh"]
        TMUX["tmux cockpit"]
        ST["status-server + React"]
    end
    subgraph CTRL["Control plane"]
        CO["coordinator.sh (polling)"]
        SMJ["coordinator-state-machine.json"]
        GS["graph_scheduler.py"]
        GND["graph_node_dispatcher.py"]
    end
    subgraph ROUTE["Capability routing"]
        LO["logical-operators.json"]
        PO["physical-operators.json"]
        CC["capability capsules"]
    end
    subgraph W["Physical operators (tmux panes)"]
        PM["PM"]
        PL["Planner"]
        BU["Builder"]
        EV["Evaluator"]
        CX["codex-bridge (inbox/outbox)"]
    end
    subgraph FS["File-backed state"]
        SP["sprints/*.status.json · task_graph.json"]
        GL["gate-ledger.jsonl"]
        EVJ["events.jsonl"]
        DB["run/state.db"]
    end
    subgraph RES["Research pipeline"]
        RC["research/cli.py"]
        EL["evidence ledger · claims · citations"]
        RE["evaluator + gates"]
        SU["survey pipeline"]
    end
    CLI --> CO --> SMJ
    CO --> GS --> GND
    GS --> LO & PO & CC
    GND -->|"tmux send-keys"| PM & PL & BU & EV
    GND --> CX
    PM & PL & BU & EV --> SP
    CO -->|"poll max mtime"| SP
    SP --> GL & EVJ & DB
    ST --> SP & DB
    TMUX --- PM & PL & BU & EV
    CLI --> RC --> EL --> RE --> SU
```

## 3. JiuwenSwarm execution workflow

```mermaid
sequenceDiagram
    participant U as User
    participant GW as Gateway
    participant WS as AgentServer
    participant DA as DeepAgent
    participant R as Rails
    participant P as Permission engine
    participant T as Tool
    participant SB as jiuwenbox

    U->>GW: message
    GW->>WS: E2A envelope (chat.send)
    WS->>DA: invoke (agent from cache)
    loop task loop round
        DA->>R: before_task_iteration
        loop ReAct
            DA->>R: before_model_call
            DA->>DA: model call
            DA->>R: before_tool_call
            R->>P: evaluate_tiered_policy
            alt deny
                P-->>DA: rejected
            else ask
                P->>U: approval prompt
                U-->>P: decision
            end
            P->>T: execute
            opt sandbox enabled
                T->>SB: run in bwrap/cgroup
            end
            T-->>DA: observation
            DA->>R: after_tool_call
        end
        DA->>R: after_task_iteration
        DA->>DA: stop evaluators (OR semantics)
    end
    DA-->>WS: final
    WS-->>GW: chat.final
    GW-->>U: reply
```

## 4. AI4RnD execution workflow

```mermaid
sequenceDiagram
    participant U as User
    participant CLI as solar-harness
    participant FS as filesystem
    participant CO as coordinator.sh
    participant GS as graph_scheduler
    participant PN as tmux pane (agent CLI)
    participant GL as gate ledger

    U->>CLI: intake "..."
    CLI->>FS: write status.json + scaffold
    loop poll (~1s)
        CO->>FS: max mtime over sprint-*.status.json
    end
    CO->>GS: ready nodes?
    GS->>GS: capability match (hard gate)
    alt no capable worker
        GS->>FS: queue node · reason=no_matching_worker
        Note over GS,FS: run stalls honestly
    else assigned
        GS-->>CO: node → pane
        CO->>PN: capture-pane, check busy markers
        loop up to 12 × 10s
            CO->>PN: still busy? wait
        end
        alt still busy
            CO->>FS: DISPATCH_DEFERRED
        else
            CO->>PN: send-keys "<cmd>"
            CO->>CO: sleep 0.8
            CO->>PN: send-keys Enter
        end
        PN->>FS: write handoff.md / eval.md
        PN->>CLI: handoff-submit (atomic)
        CLI->>GL: append status_transition (+writer)
        CO->>FS: detect change → next transition
    end
```

## 5. JiuwenSwarm swarm assembly pipeline

```mermaid
flowchart TB
    REQ["request<br/>mode · role · channel · session · project_dir · config.yaml"]
    ENRICH["enrich_team_spec_for_swarm()"]
    REG["register_swarm_providers()<br/>@harness_element catalog → openjiuwen registries"]
    CTX["SwarmBuildContext<br/>(per-request environment)"]
    CFGS["config_specs<br/>bake config attributes into RailSpec.params"]
    SPEC["TeamAgentSpec<br/>leader · teammate"]
    DAS["DeepAgentSpec<br/>rails · tools · subagents"]
    BUILD["spec.build(context)"]
    FACT["provider factory<br/>inp = XxxInput.resolve(params, ctx)"]
    OBJ["Rail · Tool · SubAgentConfig"]
    SEED["build_context_seed<br/>(cross-process rebuild)"]

    REQ --> ENRICH --> REG
    ENRICH --> CTX
    ENRICH --> CFGS --> SPEC --> DAS --> BUILD --> FACT --> OBJ
    CTX --> BUILD
    CTX --> SEED
```

## 6. AI4RnD sprint state machine

```mermaid
stateDiagram-v2
    [*] --> intake
    intake --> prd_ready: prd_artifact_present<br/>→ planner
    prd_ready --> planning_complete: design + plan + task_graph<br/>→ builder_main
    planning_complete --> build_complete: handoff_present<br/>→ evaluator
    build_complete --> done: eval_verdict PASS
    build_complete --> blocked: eval_verdict FAIL<br/>→ builder_main
    blocked --> build_complete: handoff_newer_than_eval
    intake --> quarantined: corrupt artifacts
    intake --> corrupt
    planning_complete --> failed: retries exhausted
    done --> [*]
```

## 7. AI4RnD capability routing decision tree

```mermaid
flowchart TB
    N["ready node"] --> W["for each worker"]
    W --> R{"role compatible?"}
    R -->|no| S1["skip"]
    R -->|yes| C{"capabilities ⊇ required?<br/><b>HARD GATE — never relaxed</b>"}
    C -->|no| S2["skip · record missing_capabilities"]
    C -->|yes| Q{"quota exhausted?"}
    Q -->|yes| S3["skip"]
    Q -->|no| M{"strict model match required and unmet?"}
    M -->|yes| S4["skip"]
    M -->|no| RT{"runtime available?"}
    RT -->|no| S5["blocked_by_runtime"]
    RT -->|yes| B{"pane free and not busy?"}
    B -->|no| S6["blocked_by_capacity"]
    B -->|yes| SK{"skills match?"}
    SK -->|yes| ST["strict candidates"]
    SK -->|no| RX["relaxed candidates"]
    ST --> SORT["sort by role_penalty, −cap_score,<br/>−skill_count, model_penalty, load, pane"]
    RX -.->|"only if strict empty"| SORT
    SORT --> A["assign"]
    S2 & S3 & S4 & S5 & S6 --> E{"any candidate?"}
    E -->|no| STALL["queue with reason:<br/>no_matching_worker |<br/>worker_capacity_exhausted |<br/>worker_runtime_unavailable"]
```

## 8. AI4RnD research pipeline

```mermaid
flowchart TB
    T["user topic"] --> RI["run initialization"]
    RI --> RC["research contract"]
    RC --> DC["domain / research-type classification"]
    DC --> QG["question graph"]
    QG --> LP["logical research plan"]
    LP --> OPT["Optimizer<br/>(specified; not implemented)"]
    OPT --> PP["physical operator plan"]
    PP --> SRC["source retrieval + ingestion"]
    SRC --> SPAN["span extraction (char + byte offsets)"]
    SPAN --> EL["evidence ledger"]
    EL --> CG["claim graph"]
    CG --> BP["report blueprint + section packets"]
    BP --> CR["citation rendering (from stored spans only)"]
    CR --> QT["quality gates<br/>grounding · authority · diversity ·<br/>coverage · plausibility · novelty"]
    QT -->|repairable_fail| RP["repair DAG"]
    RP --> SRC
    QT -->|pass| FC["FinalCloseoutGate"]
    FC --> BUN["research bundle"]
```

## 9. Component mapping

```mermaid
flowchart LR
    subgraph A["AI4RnD"]
        direction TB
        a1["solar-harness CLI"]
        a2["coordinator.sh"]
        a3["graph_scheduler"]
        a4["capability routing"]
        a5["tmux dispatch"]
        a6["codex bridge"]
        a7["sprint artifacts"]
        a8["gate ledger"]
        a9["verification gate"]
        a10["evidence ledger"]
        a11["claim graph"]
        a12["research evaluator"]
        a13["repair DAG"]
        a14["skills (SKILL.md)"]
        a15["status server"]
        a16["wiki schema"]
    end
    subgraph J["JiuwenSwarm"]
        direction TB
        b1["channels + gateway"]
        b2["DeepAgent task loop"]
        b3["— none —"]
        b4["— none —"]
        b5["in-process invocation"]
        b6["sub-agents · MCP · ACP"]
        b7["session store"]
        b8["— none —"]
        b9["— none —"]
        b10["— none —"]
        b11["— none —"]
        b12["Auto Harness (different purpose)"]
        b13["— none —"]
        b14["skills (SKILL.md)"]
        b15["web UI"]
        b16["memory index"]
    end
    a1 -->|reuse JW| b1
    a2 -->|reuse JW| b2
    a3 -->|port| b3
    a4 -->|port| b4
    a5 -->|drop| b5
    a6 -->|adapt| b6
    a7 -->|port to service| b7
    a8 -->|port| b8
    a9 -->|port| b9
    a10 -->|port| b10
    a11 -->|port| b11
    a12 -->|port| b12
    a13 -->|port+build| b13
    a14 -->|reuse JW| b14
    a15 -->|rewrite| b15
    a16 -->|keep both| b16
```

## 10. Current integration boundary

Today there is none. The two systems share no code, no protocol, no data format — with one
exception.

```mermaid
flowchart LR
    subgraph J["JiuwenSwarm"]
        JS["skills/&lt;n&gt;/SKILL.md<br/>YAML: name, description"]
        JR["Rail plugin dir<br/>&lt;workspace&gt;/extensions/"]
        JM["MCP client"]
        JA["ACP / A2A server"]
    end
    subgraph A["AI4RnD"]
        AS["skills/&lt;n&gt;/SKILL.md<br/>YAML: name, description,<br/>user-invocable, argument-hint"]
        AH["harness/lib/*"]
        AC["harness/config/*"]
    end
    JS <-.->|"compatible frontmatter —<br/>the ONLY shared format today"| AS
    JR -.->|"unused seam"| AH
    JM -.->|"unused seam"| AH
    JA -.->|"unused seam"| AH
    AH x--x JM
```

The dotted lines are *potential* seams, none currently used. The only real overlap is the
`SKILL.md` frontmatter convention, which both inherit from the Anthropic skill format.

## 11. Recommended target architecture

```mermaid
flowchart TB
    subgraph USERS["Users"]
        U["Web · TUI · Desktop · IM · Cron"]
    end
    subgraph JW["JiuwenSwarm — owns execution"]
        GW["Gateway · channels · E2A"]
        AS["AgentServer · session · skills · memory"]
        DA["DeepAgent · swarm members · sub-agents"]
        PERM["Permission engine"]
        SBX["jiuwenbox"]
    end
    subgraph GLUE["Integration layer"]
        RAIL["ResearchToolkitRail<br/><b>out-of-tree plugin</b>"]
        EXT["research extension<br/><b>in-tree · ~10 lines core patch</b>"]
    end
    subgraph SVC["Research service — owns truth"]
        API["HTTP API (loopback + token)"]
        RUN["Run orchestrator"]
        ROUTER["Capability router"]
        DAG["DAG scheduler"]
        OPS["Research operators"]
        GATES["Gate registry + repair"]
        GL[("Gate ledger")]
        EL[("Evidence · claims · citations")]
    end
    U --> GW --> AS --> DA
    DA -.mounts.-> RAIL
    DA --> PERM --> SBX
    RAIL -->|"start · status · evidence · report"| API
    API --> RUN --> DAG --> ROUTER
    ROUTER -->|"bounded work packet"| EXT
    EXT -->|"dispatch to capability-matched member"| DA
    DA -->|"artifacts + provenance"| API
    RUN --> OPS --> EL
    RUN --> GATES --> GL
    GATES -->|fail| DAG
```

## 12. Proposed end-to-end functional workflow

```mermaid
sequenceDiagram
    autonumber
    participant U as User (Feishu)
    participant GW as Gateway
    participant DA as DeepAgent
    participant RL as ResearchToolkitRail
    participant SV as Research service
    participant RT as Capability router
    participant EX as research extension
    participant WK as Swarm member (capability-matched)
    participant PE as Permission engine
    participant GL as Gate ledger

    U->>GW: "Research the state of skills governance"
    GW->>DA: E2A chat.send
    DA->>RL: research_start(topic, depth=standard)
    RL->>SV: POST /runs
    SV-->>RL: run_id
    RL-->>DA: run_id
    DA-->>U: "Started run <id>. I'll report as gates complete."

    SV->>SV: contract → domain → question graph → plan
    loop each ready DAG node
        SV->>RT: assign(node)
        alt no capability match
            RT-->>SV: no_matching_worker + missing_capabilities
            SV->>GL: append gate_check (stalled)
            SV-->>RL: status: stalled (honest)
            RL-->>U: "Stalled: no worker provides <capability>"
        else assigned
            RT->>EX: execute_node(bounded packet, budget, idempotency key)
            EX->>WK: dispatch
            WK->>PE: tool calls (fetch, parse, extract)
            PE-->>WK: allow / ask / deny
            WK-->>EX: artifacts + provenance
            EX-->>SV: node result
            SV->>GL: append route_record + status_transition (writer attributed)
        end
    end

    SV->>SV: span extraction → evidence ledger → claim graph
    SV->>SV: run quality gates
    alt gate fails
        SV->>SV: repair DAG (targeted search → extract → verify → rewrite)
        SV->>GL: repair_start
        Note over SV: bounded; on exhaustion → needs_human_review
    end
    SV->>SV: FinalCloseoutGate
    SV->>GL: eval_verdict (evaluator ≠ writer, enforced by routing)

    DA->>RL: research_status(run_id)
    RL->>SV: GET /runs/{id}
    SV-->>RL: done · gate summary · claim counts
    DA->>RL: research_report(run_id, "md")
    RL->>SV: GET /runs/{id}/report
    SV-->>RL: file path
    DA->>GW: swarm.send_file
    GW-->>U: report + gate dossier
    U->>DA: "Where does claim C014 come from?"
    DA->>RL: research_evidence(run_id, claim="C014")
    RL->>SV: GET /runs/{id}/evidence?claim=C014
    SV-->>DA: evidence ids + verified spans
    DA-->>U: source, span offsets, authority score
```

## 13. Verification model comparison

```mermaid
flowchart TB
    subgraph JV["JiuwenSwarm — verifies execution"]
        J1["stop evaluators<br/>rounds · timeout · token budget"]
        J2["permission engine<br/>allow / ask / deny"]
        J3["LSP diagnostics (code mode)"]
        J4["Auto Harness CI<br/>(verifies harness changes)"]
        J5["skilldev evaluate_stage<br/>(verifies skill quality)"]
        JX["❌ nothing verifies<br/>whether the output is TRUE"]
    end
    subgraph AV["AI4RnD — verifies correctness"]
        A1["verification_gate<br/>patch + tests + <b>writer ≠ verifier</b>"]
        A2["scheduler guards<br/>no self-graded pass"]
        A3["citation grounding"]
        A4["source authority · diversity ·<br/>type plausibility"]
        A5["section coverage · novelty · figures"]
        A6["per-profile thresholds"]
        A7["gate ledger → status projection"]
        AX["⚠️ grounding uses token overlap<br/>(_jaccard), not entailment"]
    end
    J1 & J2 & J3 & J4 & J5 --> JX
    A1 & A2 --> A7
    A3 & A4 & A5 --> A6 --> A7
    A3 -.-> AX
```

## 14. JiuwenSwarm extension surface map

```mermaid
flowchart TB
    subgraph GREEN["✅ Out-of-tree — no core change"]
        R["Rail plugin (rail.py)<br/>hooks + <b>add_ability → tools</b>"]
        S["Skill (SKILL.md)"]
        M["MCP server"]
        H["User hooks (config.hooks)"]
        C["Config (models, permissions, channels)"]
    end
    subgraph AMBER["⚠️ In-tree module with a manifest"]
        E["Extension package<br/>RPC handlers + 6 hook events"]
    end
    subgraph RED["❌ Core-tree change required"]
        EN["ReqMethod enum<br/>common/schema/message.py"]
        FS["_SYMPHONY_METHODS frozenset<br/>agent_adapter/interface.py:437"]
        CS["config_specs.py element name lists"]
    end
    subgraph GREY["🔒 Upstream openjiuwen"]
        L["config-driven harness loader<br/>(DESIGN.md §15 — future work)"]
    end

    R -->|"used by the recommendation"| TARGET["ResearchToolkitRail"]
    E -->|"in-process callable ✅"| INP["tools can dispatch by string"]
    E -.->|"externally callable ❌"| EN --> FS
    CS -.->|"gates inclusion of"| HE["@harness_element registrations"]
    L -.->|"would remove"| CS
```
