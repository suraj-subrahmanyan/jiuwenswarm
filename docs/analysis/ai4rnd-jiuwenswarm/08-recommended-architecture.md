# Recommended Target Architecture

**Option D — Hybrid.** JiuwenSwarm is the interaction and execution foundation. AI4RnD owns
the workflow, the capability model and the improvement loop.

Re-derived against the complete 142-feature product; see
[07-architecture-options.md](07-architecture-options.md) for why the six alternatives lose.

---

## 1. Target architecture

```mermaid
flowchart TB
    subgraph U["Users"]
        UI["Web · TUI · Desktop · CLI · IM channels · cron"]
    end

    subgraph JW["JiuwenSwarm — interaction + execution foundation · 23 features"]
        GW["Gateway · channels · E2A normalisation"]
        AS["AgentServer · session · skills · memory index"]
        DA["DeepAgent · team members · sub-agents"]
        PERM["Permission engine"]
        SBX["jiuwenbox · bwrap · cgroup · network policy"]
    end

    subgraph GL["Integration layer — thin, mostly out-of-tree"]
        RAIL["ResearchToolkitRail<br/><i>verified V-2</i>"]
        ADPT["Execution adapter<br/><i>~10-line core patch</i>"]
    end

    subgraph AI["AI4RnD services — 90 features"]
        direction TB
        subgraph FRONT["Compile"]
            INT["Intention compiler<br/>intent · scope · ambiguity · constraints"]
            CON["Task contract<br/>versioned + hashed"]
            PLAN["Planner<br/>decompose → TaskGraph → validate"]
        end
        subgraph EXECP["Orchestrate"]
            SCHED["DAG scheduler<br/>readiness · write-scope batching"]
            ROUTE["Capability router<br/>logical → physical binding"]
            ADMIT["Admission · durable queue · leases"]
        end
        subgraph GOV["Govern"]
            CAPS["Capsule registry<br/>contract · effects · verification ·<br/>operator_compatibility"]
            OPS["Operator registries<br/>logical + physical"]
            EVAL["Evaluator suite<br/>6 families"]
            LED["Gate ledger + evidence ledger<br/>append-only · writer-attributed"]
        end
        subgraph LEARN["Improve"]
            RSI["RSI loop"]
        end
    end

    subgraph FLEET["Physical operators — heterogeneous"]
        JWA["JiuwenSwarm agents<br/><i>governed</i>"]
        API["API models"]
        BROW["Browser operators"]
        HOST["Remote hosts"]
    end

    UI --> GW --> AS --> DA
    DA -.mounts.-> RAIL
    DA --> PERM --> SBX
    RAIL -->|"start · status · evidence · report"| INT
    INT --> CON --> PLAN --> SCHED
    CAPS --> ROUTE
    OPS --> ROUTE
    SCHED --> ROUTE --> ADMIT
    ADMIT -->|"bounded work packet"| ADPT
    ADPT --> DA
    DA --> JWA
    ADMIT --> API & BROW & HOST
    JWA & API & BROW & HOST -->|"artifacts + provenance"| LED
    LED --> EVAL --> LED
    LED --> RSI
    RSI -.->|"promote / rollback"| CAPS
    RSI -.->|"promote / rollback"| OPS
    RSI -.->|"promote / rollback"| PLAN
    RSI -.->|"promote / rollback"| EVAL
```

---

## 2. Ownership boundaries

| Concern | Owner | Why |
|---|---|---|
| Channels, intake transport, delivery | **JiuwenSwarm** | 9 IM + web/TUI/desktop/ACP/A2A already exist |
| Conversational state, session rewind, compaction | **JiuwenSwarm** | mature; and research state must *not* live here |
| Skills, agent memory index | **JiuwenSwarm** | `MemoryIndexManager` 1,224 LOC; skills are capsule *ingredients* |
| Tool execution, permissions, sandboxing | **JiuwenSwarm** | only system with a permission engine and OS isolation |
| Packaging, installers, UI shell | **JiuwenSwarm** | signed desktop apps, pip, TUI |
| **Intention compilation, task contracts** | **AI4RnD** | must be a validated artifact, not model context |
| **Planning + TaskGraph** | **AI4RnD** | must be validated before dispatch |
| **DAG scheduling, capability routing, admission, leases** | **AI4RnD** | must sit *above* agents to choose which agent runs what |
| **Capsules + operator registries** | **AI4RnD** | versioned, certified, promotable — cannot live in an upstream package |
| **Evaluators, evidence, gate ledger** | **AI4RnD** | JiuwenSwarm has no gate concept |
| **RSI** | **AI4RnD** | must own the artifact tree it mutates |
| **Per-operator permission policy** | **AI4RnD router** | V-6: JiuwenSwarm has 2 roles and global policy — cannot express it |

**One-line rule.** *JiuwenSwarm decides how a unit of work is safely executed. AI4RnD decides
what work exists, who may do it, whether the result is true, and what the system should
learn from it.*

---

## 3. Capsules, Operators and TaskGraph in the target

The abstraction stack from
[00-intended-product-model.md](00-intended-product-model.md) §2 is preserved intact, with
JiuwenSwarm appearing only at the bottom as *one kind of physical operator*.

```mermaid
flowchart LR
    CAP["<b>Capsule</b><br/>governed capability<br/>11-section contract"] -->|"contains"| CON["<b>Contract</b><br/>typed I/O · pre/postconditions ·<br/>invariants · required evidence"]
    CON -->|"realised by"| LOP["<b>Logical operator</b><br/>DAG-callable · required capabilities ·<br/>write scope · completion conditions"]
    LOP -->|"bound by router"| POP["<b>Physical operator</b>"]
    POP --> O1["JiuwenSwarm agent<br/>(permissions + sandbox apply)"]
    POP --> O2["API model"]
    POP --> O3["Browser operator"]
    POP --> O4["Remote host"]
```

**Binding rules preserved from AI4RnD** (verified working, `graph_scheduler:2290-2400`):
capability match is a hard gate that is never relaxed; skills are a preference with a
liveness net; a node with no capable operator **stalls honestly** with
`no_matching_worker` plus the missing-capability list, and is never force-assigned.

**Added by the capsule layer:** `effects` (read/write/execute/network/cost) and
`operator_compatibility` (`preferred` / `forbidden`) become router inputs, and
`required_guard_capsules` gate admission. This is the mechanism that lets a capsule declare
"this capability may never touch the network" and have it enforced at binding time rather
than trusted at runtime.

---

## 4. The RSI feedback loop

The loop the brief requires, mapped onto owned components:

```mermaid
flowchart TB
    EXEC["<b>Execution evidence</b><br/>route records · artifacts · traces<br/><i>gate ledger + evidence ledger</i>"]
    EVAL["<b>Evaluation</b><br/>6 evaluator families<br/>+ operator capability profiling"]
    CAND["<b>Improvement candidate</b><br/>versioned proposal<br/><i>GEPA propose · trajectory mining ·<br/>failure_miner clusters</i>"]
    ISO["<b>Isolated testing + benchmarking</b><br/>sandboxed run · holdout set ·<br/>golden set · replay · A/B<br/><i>budget caps enforced</i>"]
    POL["<b>Frozen-policy check</b><br/>candidate may not relax<br/>secrets · git_push · destructive_shell ·<br/>payment · external_api_write"]
    DEC{"<b>Approve?</b><br/>evaluator verdict<br/>+ HITL for high-risk"}
    PROMO["<b>Promotion</b><br/>version bump · registry update"]
    REJ["<b>Rejection</b><br/>recorded with reason"]
    TGT["<b>Updated artifact</b><br/>Capsule · Operator definition ·<br/>binding policy · TaskGraph pattern ·<br/>evaluator rubric · model policy · prompt"]
    MON["<b>Post-promotion monitoring</b><br/>regression detection"]
    RB["<b>Rollback</b>"]

    EXEC --> EVAL --> CAND --> ISO --> POL --> DEC
    DEC -->|approved| PROMO --> TGT --> MON
    DEC -->|rejected| REJ
    MON -->|regression| RB --> TGT
    MON -->|stable| EXEC
    REJ -.->|"becomes a hard case"| EXEC
    TGT -.->|"next run uses new version"| EXEC
```

**What already exists for this** (V-13): `gepa_optimizer` implements
propose→run→review→promote→rollback with dry-run default, mandatory
`--max-evals`/`--max-spend`/`--max-walltime`, promotion-target restriction, and
`hard_policy_checker` enforcing the frozen-policy box above. `evolution_engine` implements
scorecard/recommend/promote/demote. `failure_miner` clusters failures into candidates.
**None of it is wired.** Stage 4 wires it; it is not a from-scratch build.

**What must be built:** RSI surfaces 2, 4, 5, 6, 7, 8 (routing optimisation, DAG/organisation
search, judge calibration and reward modelling, memory/retrieval learning, model weights,
curriculum and credit assignment). Six of eight.

**Safety invariants for the loop** — non-negotiable:

1. RSI may propose changes to any artifact; it may **never** promote without an evaluator
   verdict plus, for high-risk classes, a human verdict recorded in the gate ledger.
2. The frozen-policy set is not RSI-modifiable. A candidate that relaxes a safety policy is
   rejected before it reaches testing.
3. Every promotion is versioned and reversible, with the pre-promotion version retained.
4. RSI runs against **isolated** copies. It never mutates a live registry in place.
5. Every promotion and rollback is a gate-ledger record with writer attribution.

---

## 5. Request and evidence flow, end to end

```mermaid
sequenceDiagram
    autonumber
    participant U as User (any channel)
    participant JW as JiuwenSwarm
    participant R as ResearchToolkitRail
    participant IC as Intention compiler
    participant PL as Planner
    participant SC as Scheduler + router
    participant AD as Execution adapter
    participant AG as JiuwenSwarm agent (operator)
    participant EV as Evaluators
    participant GL as Gate ledger
    participant RS as RSI

    U->>JW: "Is technique X worth pursuing for our product?"
    JW->>R: research_start(...)
    R->>IC: POST /runs
    IC->>IC: classify lane · scope · ambiguity · constraints
    alt ambiguous
        IC-->>R: clarification questions
        R-->>U: ask (via JiuwenSwarm UX)
    end
    IC->>PL: versioned + hashed task contract
    PL->>PL: decompose → TaskGraph → validate ("compiles implies dispatchable")
    PL->>SC: TaskGraph
    loop each ready node
        SC->>SC: readiness · write-scope batching
        SC->>SC: capability match (HARD gate) + capsule effects/compatibility
        alt no capable operator
            SC->>GL: stall record · no_matching_worker + missing capabilities
            Note over SC,GL: run stalls honestly — never force-assigned
        else bound
            SC->>AD: bounded work packet (goal, input refs, output schema, budget, idempotency key)
            AD->>AG: governed dispatch
            AG->>JW: tool calls → permission engine → sandbox
            AG-->>AD: artifacts + provenance
            AD->>GL: route record (provider, model, operator, exit code, timings)
        end
    end
    SC->>EV: node + run artifacts
    EV->>EV: conformance · engineering · perf/cost · security/IP · evidence/factuality · lifecycle
    EV->>GL: verdicts (writer ≠ verifier enforced by the router)
    alt gate fails
        EV->>SC: repair DAG
    end
    GL-->>R: run status · gate dossier · evidence index
    R-->>U: deliverable + "claim C014 rests on span [120,180) of source S3"
    GL->>RS: execution evidence
    RS->>RS: propose → isolated test → policy check → approve/reject → promote/rollback
```

---

## 6. Boundary rules — non-negotiable

### 6.1 Evidence never lives in the session
Research artifacts live in AI4RnD's store; the JiuwenSwarm session holds only `run_id`.
JiuwenSwarm compacts context and supports session rewind with file restoration; evidence must
survive both.

### 6.2 Tools return references, not bulk evidence
`research_evidence` returns ids plus one-line summaries. The model reasons over ids; the
service resolves them. Prevents compaction from silently destroying citation integrity.

### 6.3 Node status is a projection of the gate ledger
Never a directly written field. Preserve writer attribution on every transition — AI4RnD's
best state-design idea, and it costs nothing to keep.

### 6.4 Writer ≠ verifier is enforced in the AI4RnD router
**Changed from the previous revision.** V-6 established that JiuwenSwarm has only
`leader`/`teammate` with a single global permission policy, so this cannot be delegated. The
router must exclude the writing operator's actor id from the evaluation node's candidate set,
making self-grading *unroutable* rather than merely detected afterwards.

### 6.5 The LLM never owns run state
`LLM proposes. Schemas constrain. Code validates. Gates decide. Artifacts preserve.` An
operator produces artifacts; the service validates and records them. No operator marks its
own node passed.

### 6.6 Capsule effects are enforced at binding, not trusted at runtime
A capsule declaring `effects.network: none` must not be bound to an operator with network
access. This is the capsule layer earning its keep over a skill.

### 6.7 JiuwenSwarm's built-in security rules must be repaired before production
V-4: `get_builtin_security_rules()` returns **0** in a stock install, and `rm -rf /` resolves
to ALLOW under a permissive baseline. Either ship `builtin_rules.yaml` into the openjiuwen
package path, or have the integration load JiuwenSwarm's copy explicitly. **Do not assume the
guardrail layer is active.**

---

## 7. What to build first

1. **ResearchToolkitRail + evidence core** — no core changes; mechanism already verified.
2. **Real entailment for feature 70** — promoted from late hardening to Stage 1 by V-12.
3. **Extract AI4RnD services with an HTTP API** — proves the ownership boundary.
4. **Wire the unwired**: capsules, operators, actor queue/leases, TaskGraph persistence — 19
   modules, ~8k LOC, already tested.
5. **Execution adapter + callback** — the only step touching JiuwenSwarm's core tree.
6. **Wire GEPA; build the remaining RSI surfaces.**

Full staging in [09-implementation-plan.md](09-implementation-plan.md).

---

## 8. Evidence that would change the recommendation

| # | Question | Would flip to |
|---|---|---|
| G1 | Can the execution callback be made bounded, idempotent and cancellable against a real `DeepAgent`? | **Option G** (defer JiuwenSwarm) if not |
| G2 | Does an out-of-tree Rail survive agent-cache invalidation and agent-server restart? | Option G if not — V-2 verified registration, **not** lifecycle persistence |
| G3 | Does the two-role limit (V-6) block per-operator governance even with router-side enforcement? | Option E (fork) if the router cannot compensate |
| G4 | Is upstream willing to accept a generic extension-RPC passthrough? | carries a permanent patch if not — tolerable |
| G5 | Does `openjiuwen` 0.1.x churn break the Rail API within a release cycle? | Option G if the seam proves unstable |
| G6 | Is the tmux cockpit a genuine user requirement rather than an implementation artifact? | changes the physical-operator model materially |

G1 and G2 are the decisive pair and are testable in Stage 1–2 — before any core-tree change
and before the expensive ports begin.
