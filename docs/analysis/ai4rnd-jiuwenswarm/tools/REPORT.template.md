# AI4RnD on JiuwenSwarm — The Architecture Report

**Recommendation: build the complete intended AI4RnD product as a first-class, persistent
subsystem on JiuwenSwarm, with AI4RnD permanently owning product semantics, OpenJiuwen supplying
execution, and a thin integration bridge compiling ready work onto the runtime progressively —
each delegation gated by a passing compatibility test. All 142 workbook outcomes are preserved;
none is dropped, weakened or renamed into something less capable.**

This report is self-contained: a technically informed reader needs no other document to
understand the product, the current systems, the recommended architecture, its end-to-end
behaviour, ownership and state boundaries, component sourcing, implementation direction,
evidence, risks and open decisions. The row-level matrices, probe transcripts and the full
analysis history remain available as supporting material and are linked where relevant, but
nothing below depends on them.

**How to read the evidence labels.** Every load-bearing claim carries one of: **EXEC** —
executed in this analysis environment; **SRC** — verified by direct source reading of the pinned
dependencies (JiuwenSwarm `0.2.3.beta1`, OpenJiuwen `0.1.15.post3`, AI4Research `d35c511`);
**DOC** — documented only; **INF** — inferred; **UNKNOWN** — explicitly not determinable here.
29 experiments were executed in total.

---

## 1. What AI4RnD is intended to become

**AI4RnD is an evidence-governed autonomous R&D system.** It discovers needs and opportunities,
researches and ideates, forms explicit technical claims and falsifiable hypotheses, builds
proof-of-concept software, runs experiments and benchmarks, evaluates results against declared
acceptance criteria, and delivers defended conclusions — while retaining what it learned as
organizational knowledge and improving its own capabilities under governance.

Its verification spine is **claims refinement**: nothing the system asserts reaches a user
without resolving to evidence, and nothing is built before its hypothesis can state what would
refute it. An earlier revision of this analysis used that spine as the whole identity
("a claims refinery"). That framing was too narrow — it made the product sound like a
literature-review engine. The refinery is the spine; the product is the whole R&D body around
it: opportunity discovery, POC construction, benchmarking, datasets, capability development,
delivery and self-improvement are first-class outcomes, not accessories to citation checking.

The product is defined by a 142-feature workbook, read directly in this analysis (**EXEC**) and
reconciling exactly:

| Sheet | Plane | Groups | Features |
|---|---|---:|---:|
| Workflow Features | what a research run does — nine lanes from ingestion to delivery | 9 | 54 |
| Foundation Features | the machinery underneath — capsules, operators, evaluators, models, RSI, data, harness, compilers, planner, builder | 10 | 65 |
| Vertical Features | the product around both — visibility, installers, UI, accounts, channels, configuration | 6 | 23 |
| **Total** | | **25** | **142** |

This definition is held constant everywhere below. **Current code is evidence of maturity and a
source of reusable assets; it is never the boundary of the target product.** Every sourcing
decision in §7 is an implementation strategy and redefines nothing.

### 1.1 The intended architecture, independent of any foundation

Before choosing an implementation substrate, this is the shape the workbook demands — five
responsibilities and the relationships between them:

%%SVG:intended%%

Three structural commitments in this picture matter more than any component name:

- **One authority for meaning.** A single project-control layer decides what a request means,
  what work exists, what may start, what truly succeeded, and when the Contract is satisfied.
- **Capabilities are governed objects, not prompt files.** The capability layer owns identity,
  contracts, effects, compatibility and certification — and is itself the main subject of
  improvement.
- **Execution is an abstraction.** Plan nodes invoke Logical Operators; *which* physical
  executor serves an invocation is a binding decision under declared rules. The product never
  hard-couples to one engine — which is precisely what makes the JiuwenSwarm question answerable
  on evidence rather than on faith.

### 1.2 The user journey

%%SVG:journey%%

The journey begins when a need exists — a question, a qualified signal, or imported material —
and ends twice: for the requester, with an authorized, evidence-linked deliverable; for the
organization, with frozen evidence and retained knowledge. One loop deliberately outlives every
journey: governed improvement. The nine workbook lanes live inside these phases as individually
addressable capabilities — a literature-only project never builds a POC; a refuted claim
re-enters framing; lanes can run in parallel or recursively. A refuted hypothesis is a *success*
of the verification machinery, never a failure of the run.

### 1.3 Capability Capsules, precisely

The workbook's central capability idea is a five-level separation that survives every
architecture decision in this report:

| Level | What it is | Lifetime |
|---|---|---|
| **Capability Capsule** | governed, versioned, reusable capability identity | independent of any request |
| **Contract** | the promise for *this* request: scope, constraints, acceptance | one request |
| **TaskGraph** | the project-specific plan | one project |
| **Logical Operator** | a stable callable action a plan node invokes directly | independent |
| **Physical Operator** | the concrete executor | one binding |

%%SVG:capsule%%

All 42 capsule manifests in the current repository already carry every governed section
(**EXEC** — parsed in this analysis; registry: 35 entries, 30 stable). What the schema does not
yet carry — versions, evaluation history, RSI targets — is named work in §8, not a redefinition.
Skills, tools, agents, workflows, models and APIs are **bindings beneath a Capsule**; replacing
a binding never changes the Capsule's identity or governance.

---

## 2. What exists today

Two honest as-is pictures, kept deliberately separate from the target. Nothing in this section
is design; every status is verified.

### 2.1 Current AI4RnD

%%SVG:cur_a4%%

The reading: AI4RnD's *governance assets are real* — the evidence ledger, gate ledger, capsule
registry and GEPA optimizer all exist and mostly run (**EXEC/SRC**) — while its *carrier* is a
tmux cockpit driven by a polling shell script, its scheduler fuses plan semantics with 4,189
lines of physical scheduling, its central grounding check measured **0.25 precision** on a
labelled set (**EXEC**), and the knowledge layer, Idea Card, falsifiability stage, accounts and
RSI governance are absent (**EXEC** — exhaustive searches). GEPA deserves emphasis because
earlier revisions under-weighted it: it is 3,540 lines with unit tests, a typed candidate
envelope covering skills, capsules, routing policies, rewrite rules and cost models, budget
stoppers, a frozen-policy checker, and a checksummed, atomic, rollback-capable promoter whose
CLI defaults to dry-run (**SRC**).

### 2.2 Current JiuwenSwarm and OpenJiuwen

%%SVG:foundation%%

The foundation is substantial and much of it is verified by execution: durable staged graphs
with runtime-computed fan-out (**EXEC**), a scripted pipeline engine whose journal replays
interrupted runs re-executing only the failed step (**EXEC**), admission control that refuses
rather than queues silently (**EXEC**), a persistent sqlite checkpointer in a stock install
(**SRC**), a team task board with real dependency edges, reliability anomaly detectors and
remediation, shared team memory, sandboxing, nine channels and a web UI (**SRC**).

Four verified gaps shape the integration, and one pattern explains why reading source is not
enough here: **this codebase fails loudly on typos and silently on unimplemented features.**

| # | Verified gap | Class |
|---|---|---|
| 1 | An unknown model name silently resolves to the default worker model — no error, no warning | SRC |
| 2 | The agent-facing pipeline tool advertises `resume_id` and rejects it: "not supported yet"; resume exists only as an internal control-plane call | EXEC |
| 3 | A step that fails all its retries returns an empty result and the run reports success | EXEC |
| 4 | The executor-typing option is validated and forwarded, but no backend reads it | EXEC |
| 5 | The built-in shell-guardrail tier loads zero rules; the rules file the installer writes is read by nothing | EXEC |
| 6 | The evolution trainer accepts exactly one subject class in the entire runtime; the application imports only its archive and tool-description parts | EXEC |

---

## 3. The recommended integration, and why

Five coherent complete-product options were evaluated. Execution mechanisms — DeepAgent,
SwarmFlow, Core Workflow, Dynamic Team — are not among them: each implements 0 of the 142
outcomes alone and appears *inside* every option as machinery.

| Option | In one line | Verdict |
|---|---|---|
| **A** — AI4RnD-led control plane | keep AI4RnD's scheduler; Jiuwen replaces only physical executors | complete, but pays a permanent duplicate-scheduler tax against engines verified to work |
| **B** — Jiuwen-native lifecycle | delegate sequencing, checkpoints and human turns to the runtime now | right destination, wrong commitment schedule — deletes fallbacks on the strength of *reading* |
| **C** — progressive compilation ★ | B's destination, reached one capability at a time, each retirement gated by a passing test | **recommended** |
| **D** — full delegation now | remove AI4RnD's execution machinery immediately | **fails the preservation gate today** — silent model substitution would drop Model Routing & Selection with no layer left to catch it |
| **E** — standalone / defer | keep the tmux-carried system as is | preserves the most, gains nothing, leaves ~50 never-built outcomes unbuilt |

The preservation gate evaluates all 142 outcomes under every option
([full row-level CSV](traceability/142-feature-preservation-gate.csv)):

| Verdict | A | B | C ★ | D | E |
|---|---:|---:|---:|---:|---:|
| PRESERVED | 71 | 78 | 78 | 59 | 84 |
| PRESERVED WITH ADAPTATION | 13 | 6 | 6 | 24 | 0 |
| NEW BUILD REQUIRED | 56 | 56 | 56 | 55 | 56 |
| UNRESOLVED | 2 | 2 | 2 | 3 | 2 |
| **DROPPED** | **0** | **0** | **0** | **1** | **0** |

Two facts decide it. First, the big number barely moves: ~56 outcomes need new construction
under *every* option, because they exist in neither system — no architecture choice avoids
them. Second, only D drops an outcome today. **That failure is evidence against immediate full
delegation, not proof that full delegation can never become safe**: every blocking gap in §2.2
is small and fixable, and when they close upstream, C's mature form *is* D. C differs from B
only in *when* each fallback dies — after a named, falsifiable test rather than on a schedule.
Given that this analysis's execution probes repeatedly caught source-reading overstating what is
reachable, that difference is worth having.

**Progressive compilation remains the recommendation.**

### 3.1 The target architecture

%%SVG:target%%

The bridge is the only bilingual component: plan nodes, capability requirements and gate policy
on one side; engine specifications, agent calls and worktrees on the other. It is forbidden to
make semantic decisions — it translates them. Each box carries its sourcing decision from the
component audit (§7).

---

## 4. How the complete product works, end to end

The one picture to hold. Solid arrows are control and execution; dashed arrows are state,
evidence and improvement. The semantic TaskGraph defines *what must happen*; engine
specifications define *how ready work runs*.

%%SVG:master%%

Walking it once: a need arrives on any channel and **creates or retrieves a project**. The
Intention Compiler resolves ambiguity with the requester and mints **Contract v1**, confirmed by
a human before any work starts. The Planner derives **TaskGraph vN** — claims, dependencies,
acceptance. As steps become *semantically* ready (dependencies, inputs, budget, scope), the
bridge **binds** each to a qualified Capsule, permitted executor and available model — or stalls
with the missing capability named; it never substitutes. The compiler emits an engine
specification and dispatch runs it on whichever OpenJiuwen mechanism fits the sub-plan's shape —
a choice users never see. Engines return receipts and artifacts; the **receipt builder** turns
them into typed receipts with provenance, recording every attempt — and treating an empty result
as a failed attempt. Evaluators (never the writer) turn artifacts into **evidence**; gates issue
**verdicts** per claim; failures route to repair or to a **plan revision vN+1**; policy-flagged
decisions go to a human. When every claim is decided and the Contract is satisfied, the project
**closes**: evidence freezes, distribution is authorized, the deliverable returns through the
originating channel, and knowledge persists as typed projections. Performance history feeds
**GEPA**, whose approved candidates become new capsule, prompt, routing and evaluator versions —
governing *future* bindings only, because in-flight projects pin their versions.

### 4.1 State: precise invariants, not slogans

An earlier revision asserted "the TaskGraph is the only mutable object" and "runtime state is
never product state." Both were too absolute, and this report replaces them with the actual
invariant classes:

| Class | Members | Rule |
|---|---|---|
| **Immutable once written** | a confirmed Contract *version*; each evidence record; each verdict; each typed receipt; each promotion record | never edited — superseded by a new record |
| **Versioned** | Contract (scope change ⇒ new version + re-confirmation), TaskGraph (every replan ⇒ vN+1), Capsules, Operator profiles, evaluator policies, benchmark protocols, datasets | full history retained; heads move only forward |
| **Append-only streams** | evidence ledger, gate ledger, **execution-attempt lineage** (dispatches, receipts, cancellations, reconciliations), improvement history | ordered, attributed, replayable |
| **Mutable operational state** | per-step run status, consumed budget, stall queue, approval queue | reconstructible from the streams after any crash |
| **Reproducible projections** | the seven knowledge graphs, project status, the deliverable itself | derived from ledgers; rebuildable at any time; never hand-edited |

And the runtime-state correction: **engine journals and checkpoints are the runtime's property**
— reconstruction aids, session-scoped, free to be garbage-collected (**SRC**: the pipeline
journal is keyed by session and a new session replays nothing). But **the facts of execution are
project history**: every attempt, receipt, cancellation and reconciliation is captured into the
attempt lineage *by the bridge* at the moment it happens. On restart or resume, the bridge
re-derives a specification from the plan, lets the engine replay what its journal still holds
(**EXEC** — verified to re-execute only unfinished work), and reconciles the attempt lineage
against what actually ran. Project truth never depends on a journal surviving.

### 4.2 Execution success versus semantic acceptance

Seven distinct questions, each with one owner. Today's fail-closed posture exists because of
verified defects; the target does not enshrine those defects as permanent principles:

| # | Question | Target owner | Today (fail-closed) |
|---|---|---|---|
| 1 | did execution complete? | OpenJiuwen runtime | runtime — reliable (EXEC) |
| 2 | did execution technically succeed? | OpenJiuwen runtime, propagating failure | **bridge compensates**: empty result ⇒ failed attempt, because the engine reports success around failed steps (EXEC) |
| 3 | is there a valid typed receipt? | integration bridge | bridge (build) |
| 4 | does the artifact satisfy the node contract? | AI4RnD evaluators (conformance family) | same |
| 5 | does the evidence support the claim? | AI4RnD evidence authority + entailment | same — after the 0.25-precision check is replaced and re-measured |
| 6 | may work proceed? | AI4RnD gates (+ human where policy says) | same |
| 7 | is the project Contract satisfied? | AI4RnD project control | same |
| — | runtime supervision: retries, hangs, anomaly detection, remediation | **OpenJiuwen** — its reliability subsystem (detectors + remediation) is real (SRC) and AI4RnD must **not** rebuild it | reused as-is |

When gaps 1–2 close upstream (loud failure propagation, honest model binding, reachable
resume), rungs 1–3 belong wholly to the runtime and bridge verification thins to
schema-checking receipts. That is the mature form of Option C — and the compatibility tests in
§8 are exactly the conditions for it.

---

## 5. GEPA and governed self-improvement

The improvement **engine** is GEPA — AI4RnD's own, existing, tested machinery. The **substrate
that tests its candidates** is the same execution machinery that runs real work, reached through
the same bridge. OpenJiuwen's evolution framework contributes evaluation-and-training plumbing
through its Operator protocol; nothing in OpenJiuwen replaces GEPA's candidate generation or
governance. (One narrow overlap exists: the runtime's tool-description optimizer covers a slice
of GEPA's text-artifact surface; it is a binding-level alternative, not a replacement — **SRC**.)

%%SVG:gepa%%

What already exists in GEPA (**SRC**, unit-tested): the typed candidate envelope — skill,
capsule, routing policy, rewrite rules, cost model — which *is* the candidate-scope definition;
budget stoppers (spend, evaluations, wall-time, plateau, stop-file) with dry-run as the CLI
default; the frozen-policy checker that reports exact violating paths; the artifact store of
runs and candidates; and the promoter with sha256 sidecars, tmp-versus-production path guards,
atomic writes and rollback. What is missing is not machinery but **wiring and product surface**:
connection to real run history, the Improvements inbox for human approval, capsule-registry
integration, monitoring, and version pinning for in-flight projects. All eight workbook RSI
surfaces route through this one loop; model-weight evolution (surface 7) is deferred on cost —
the RL substrate exists but is unreachable from the application today (**SRC**).

Evaluation-data selection and isolated replay reuse OpenJiuwen: candidates are evaluated on
held-out case sets via the Trainer's validation-selection loop, executed through the bridge in
isolated worktrees/sandboxes — never in place.

---

## 6. Ownership at a glance

| Concern | Owner |
|---|---|
| Meaning: Contract, claims, plan, completion | **AI4RnD** |
| Capability governance: Capsules, Logical Operators, effects, certification | **AI4RnD** |
| Verification: evidence, evaluators, gates; writer ≠ verifier | **AI4RnD** |
| Improvement: GEPA candidates, budgets, frozen policy, approval, promotion | **AI4RnD** |
| Durable product state: projects, ledgers, attempt lineage, knowledge, versions | **AI4RnD** |
| Binding, compilation, dispatch/resume/cancel, typed receipts | **integration bridge** (semantic decisions forbidden) |
| Physical execution, scheduling within a spec, runtime supervision, sandbox | **OpenJiuwen** |
| Identity, sessions, channels, UI shell, configuration, packaging | **JiuwenSwarm** |
| Contract confirmation, gated approvals, improvement approvals, stall resolution | **humans** — the three-plus-one deliberate touchpoints |

Across the 142 outcomes: AI4RnD semantically owns 118; runtime implementation splits 53
AI4RnD / 32 bridge / 27 JiuwenSwarm / 25 OpenJiuwen / 4 new / 1 unresolved. That divergence —
own the meaning of far more than you run — is the architecture.

---

## 7. Component sourcing: reuse, adapt, derive or build

A systematic harvest of the foundation, with one of six verdicts per component:
**REUSE** unchanged · **COMPOSE** through an adapter · **EXTEND** via a supported interface ·
**DERIVE** a bounded fork · **BUILD** in AI4RnD · **REJECT**. Bounded derivation was neither
assumed nor excluded; it won exactly one candidate.

| Component | Verdict | Basis (evidence) | Condition / spike |
|---|---|---|---|
| Channels, Gateway, AgentServer, sessions, workspace | REUSE | the application shell the verticals require (SRC) | — |
| UI shell, configuration, model management, packaging | REUSE + EXTEND | research views and settings added on top | — |
| Core Workflow / Pregel | REUSE | runtime-computed fan-out executed (EXEC); durable supersteps | F4 covers lifecycle fit |
| SwarmFlow **engine** | REUSE via its backend seam | this analysis ran it end-to-end against a custom backend — the seam is the product's entry point (EXEC) | F4: three real plans compile & run |
| SwarmFlow **leader tool** | REJECT | advertises resume and rejects it; leader-chat coupling (EXEC) | replaced by bridge dispatch |
| DeepAgent, sub-agents, code mode/worktrees | REUSE | bounded agent work and POC construction (SRC) | — |
| Dynamic Team | REUSE | open-ended excursions | roles/permissions unverified live — U3 |
| Team task board (dependency edges) | COMPOSE | real add-dependencies/blocked-by manager (SRC) | projection of the TaskGraph for visibility, never the plan authority |
| Reliability detectors + remediation | REUSE | model/tool-error, loop, repeat detectors with remediation policy (SRC) | signals feed receipts; AI4RnD must not rebuild supervision |
| Team/shared memory, retrieval | EXTEND | substrate exists (SRC) | research-grade retrieval measured in P5 |
| Graph memory module | EXTEND (conditional) | exists, referenced nowhere by the app (EXEC) | spike: fit for typed projections, else BUILD |
| Model pool + allocator | COMPOSE (loud-failure adapter) | silent fallback by documented design (SRC) | retire adapter if upstream fails loudly |
| Guardrail rules tier | DERIVE (bounded) or upstream EXTEND | loader ignores the installed file (EXEC); single-file boundary, upstream tests retained, delta = search path + non-empty assertion | reconcile on upstream fix |
| Permissions engine + jiuwenbox sandbox | REUSE | tiered policy executed in analysis (EXEC); enforcement itself untested here (U2) | adversarial test before trust |
| Observability, progress events, background tasks | REUSE | spans and async controller (SRC) | — |
| agent_evolving: Trainer, Updater, Operator protocol, metrics, EvolutionStore | EXTEND | real loop; one wired subject today (EXEC) | Q27-class spike: register a capsule as a subject |
| agent_rl (PPO/verl) | DEFER | unreachable from the app (SRC); cost | with RSI surface 7 |
| Tool-description optimizer | COMPOSE (narrow) | overlaps one GEPA text slice (SRC) | binding-level only |
| Symphony skill retrieval | COMPOSE | ranks but never refuses (SRC) | candidate *suggestion* under the capsule gate — never the gate |
| AI4RnD evidence + gate ledgers | PORT | run standalone (EXEC) | project-scoped storage |
| AI4RnD capsule registry + manifests | PORT + EXTEND | 42 complete manifests (EXEC) | schema gains versions/history/RSI targets |
| AI4RnD GEPA | PORT (survives whole) | §5 (SRC, tested) | wire to inbox + registry |
| AI4RnD graph_scheduler + actor family | REJECT | duplicates verified engines; semantic readiness/binding logic relocates to project control and bridge | — |
| tmux cockpit + polling coordinator | REJECT | cannot meet multi-user/channel verticals | retained in history as rejected design |
| Grounding check | REJECT & REBUILD | 0.25 precision (EXEC) | bar published before build, measured after |

Matrix impact: this audit changed three rows of the 142-row ownership matrix (capsule
version-promotion, evaluator-driven operator evolution, capsules-as-evolution-subjects) from
BUILD to ADAPT, because GEPA's promoter, budget/frozen-policy machinery and typed capsule
candidates already exist. New decision totals: **BUILD 50 · ADAPT 35 · REUSE 23 · PORT 20 ·
EXTEND 11 · DEFER 2 · UNRESOLVED 1**
([full matrix](traceability/142-feature-implementation-ownership.csv)).

---

## 8. Implementation direction

Dependency-driven, no calendar estimates — earlier LOC/month figures were withdrawn when
execution probes showed what reading had missed. Sequence is knowable; duration is staffing.

| Phase | Objective | Exit evidence |
|---|---|---|
| **P1 — project & Contract foundation** | durable projects behind the existing channels/UI; Intention Compiler; users choose objective and depth only | a project survives restart; an unconfirmed Contract blocks work |
| **P2 — spikes, then the bridge** | prove compilation; build binding, dispatch/resume/cancel, receipt builder; fix the guardrail file | interrupted run resumes re-executing only unfinished work; empty result blocks its gate; guardrails load non-empty |
| **P3 — trustworthy evidence & capability registry** | ledgers project-scoped; **entailment rebuilt with the bar published first**; honest binding with effects enforcement and writer≠verifier | claims resolve to spans; measured precision materially above 0.25; unsatisfiable requirements stall |
| **P4 — the R&D lanes & Builder** | Idea Card, falsifiability gate, POC on worktrees, benchmarking, the 14 Builder outcomes | a run reaches a decision with card, falsifiability verdict, baseline benchmark, dossier |
| **P5 — data foundations & delivery** | one authoritative store, seven typed projections, TaskGraph lifecycle, closure | any claim resolves to its concepts/datasets/code/runs in one query |
| **P6 — GEPA wiring, RSI governance, accounts, hardening** | inbox, pinning, monitoring/rollback drills; the account subsystem; platform packaging | frozen-policy candidate rejected pre-evaluation; rollback drill leaves in-flight runs untouched |

**Spikes that gate the plan** (choices conditional on them):

- **F4 — compile three representative plans** — (1) source-heavy research, (2) POC construction
  plus benchmarking, (3) failed verification followed by repair and replanning — to the pipeline
  engine and/or staged workflows, and run the deterministic parts. *Both targets failing reverts
  the architecture to Option A.* Two related spikes already passed during analysis: runtime-
  computed fan-out (EXEC) and stock-install persistence (SRC).
- **Capsule-as-subject** — register one capsule as an evolution-framework subject through the
  Operator protocol. Failure grows P6 and keeps the affected RSI surfaces manual longer.
- **Graph-memory fit** — decides EXTEND versus BUILD for the typed-projection layer.
- **Sandbox adversarial test** — before any security reliance on jiuwenbox.
- **Team roles/permissions live probe** — before routing open-ended excursions to Dynamic Team.

---

## 9. Verified limitations, risks and open decisions

**Execution-verified limitations** (each shaped the design; none was silently accepted): silent
model substitution; unreachable resume; false-success on failed steps; unread executor typing;
zero-rule guardrail tier; one-subject evolution wiring; 0.25 grounding precision.

**Not verifiable here** (recorded, not assumed): platform installers (6 matrix rows carry
UNVERIFIED); sandbox enforcement under attack; live Team role limits; end-to-end model-fallback
behaviour with real credentials; achievable entailment ceiling.

**Principal risks.**
1. *Entailment quality* — if a rebuilt check cannot materially beat 0.25 on research citations,
   the product's central promise fails regardless of architecture. Mitigation: P3 publishes the
   bar before building; stop-widening decision point if unmet.
2. *Compilation coverage* — the mechanism mix is design intent until F4 runs.
3. *Upstream drift* — adapters and the one bounded derivative must be reconciled against pinned
   dependency updates; each carries retained upstream tests as its tripwire.
4. *Approval throughput* — three-plus-one human touchpoints could bottleneck at volume; P1 exit
   review watches it.

**Open product decisions** (need an owner, not more analysis): what "Cluster setting" owns
(the one UNRESOLVED row); whether tmux is a supported *channel* of the product or retired
tooling; the definition of the externally-referenced "V-05" intake qualification tier; who owns
strategic screening criteria; whether one-shot runs without a durable project are a product
mode.

---

## 10. Conclusion

The complete intended AI4RnD product — all 142 outcomes, with Capsules, Contracts, Operators,
semantic TaskGraphs, evaluators, evidence, knowledge, GEPA and governed RSI first-class — can be
built on JiuwenSwarm and OpenJiuwen. The foundation contributes exactly what the product should
not build: channels, sessions, UI, sandboxing, durable graph execution, replayable pipelines,
teams, supervision and training plumbing. AI4RnD contributes exactly what no runtime can:
meaning, capability governance, verification and governed self-improvement. The bridge between
them stays thin, honest and fail-closed until each compatibility test proves the runtime can be
trusted with more — and the target explicitly hands runtime supervision back to the runtime as
those tests pass.

~56 of the 142 outcomes require new construction under every option; the architecture decision
was never about avoiding that work, only about never doing it twice and never dropping an
outcome to make a diagram simpler.

### What changed from commit `69ebc372`, and what held

**Held:** the recommendation (progressive compilation, Option C); zero dropped outcomes; all
seven negative findings; the decision-ownership principle; the journey's shape; the preservation
gate's logic; every executed probe result.

**Changed, with reasons:**
1. *Framing* — "claims refinery" narrowed the product; now the identity is an evidence-governed
   R&D system with claims refinement as its verification spine (§1).
2. *State model* — two absolutes replaced by invariant classes plus execution-attempt lineage as
   first-class project history (§4.1).
3. *Execution ownership* — the fail-closed bridge posture is dated to today's defects, with an
   explicit target that returns rungs 1–3 and supervision to the runtime (§4.2).
4. *GEPA* — surfaced from an unexplained "governed RSI" box into the named improvement engine,
   with its existing budgets, frozen-policy and promote/rollback machinery credited (§5); three
   matrix rows corrected BUILD → ADAPT accordingly (§7).
5. *Component audit* — extended beyond engines to the task board, reliability, memory,
   Symphony-as-suggester and a single bounded derivative (§7).
6. *Document set* — this report replaces the multi-document presentation as the primary
   deliverable; the eight analyses and the full history are supporting material; the stale
   "seven documents" language is corrected.
7. *Diagrams* — one authoritative end-to-end functional architecture restored at full product
   scope (§4); current-state and intended-state views separated and status-labelled (§1–2); the
   hard-to-read five-actor sequence demoted to the supporting engineering appendix.

### Assumptions this report rests on

1. The 142-feature workbook is the complete product definition.
2. Phases group by the durable object each mints; the workbook names no macro-phases.
3. A confirmed Contract is immutable per version; the workbook requires confirmation but not
   mutability rules — chosen for auditability.
4. Seven knowledge graphs are typed projections over one authoritative store; physical storage
   is unprescribed.
5. Human touchpoints are the four named; the workbook implies review without enumerating.
6. The pinned OpenJiuwen (`0.1.15.post3`) is representative of the integration target; upstream
   fixes shift adapter work but not ownership.

*Supporting material: the [eight detailed analyses](html/index.html), the
[142-row ownership matrix](traceability/142-feature-implementation-ownership.csv), the
[preservation gate](traceability/142-feature-preservation-gate.csv), and the
[full four-revision history with probe transcripts](source-material/README.md).*
