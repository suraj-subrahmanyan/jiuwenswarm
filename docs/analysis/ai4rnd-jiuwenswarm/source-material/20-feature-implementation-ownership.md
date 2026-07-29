# Feature Implementation Ownership — All 142 Workbook Outcomes

**Source of truth.** Every row below comes from `AI4RnD Feature List.xlsx`, read directly with
`openpyxl` in this revision. Feature identity, hierarchy and wording are the workbook's; only the
analytic columns are this analysis's. The workbook reconciles exactly:

| Sheet | Plane | L1 groups | L2 features |
|---|---|---:|---:|
| Workflow Features | Workflow | 9 | 54 |
| Foundation Features | Foundation | 10 | 65 |
| Vertical Features | Vertical | 6 | 23 |
| **Total** | | **25** | **142** |

Machine-readable: [`traceability/142-feature-implementation-ownership.csv`](../traceability/142-feature-implementation-ownership.csv) · [`traceability/142-feature-preservation-gate.csv`](../traceability/142-feature-preservation-gate.csv)

---

## 1. What this matrix decides

The brief requires five responsibilities to be named separately for every feature, and forbids
answering "shared". Every row therefore carries:

| Column | Question it answers |
|---|---|
| `semantic_owner` | Who defines the feature's meaning, correctness, lifecycle and completion |
| `runtime_implementer` | Who performs the execution |
| `persistence_authority` | Who stores the authoritative state |
| `verification_authority` | Who decides the output is valid |
| `product_surface` | Where the user sees or controls it |

Where a feature genuinely crosses architectural boundaries it gains **named implementation
slices** beneath it. Slices never change the authoritative total: there are 142 rows, and
there will always be 142 rows.

---

## 2. Counts

### 2.1 By plane and L1 group

| Plane | L1 group | L2 rows |
|---|---|---:|
| Workflow | Ingestion | 7 |
| Workflow | Requirement compilation | 7 |
| Workflow | Search & ideation | 8 |
| Workflow | Idea identification / screening / opportunity selection | 7 |
| Workflow | Generate technical claims & hypothesis | 5 |
| Workflow | POC implementation | 5 |
| Workflow | Benchmarking | 5 |
| Workflow | Evaluation | 6 |
| Workflow | Delivery | 4 |
| Foundation | Capability capsule | 5 |
| Foundation | Operators | 6 |
| Foundation | Evaluator | 6 |
| Foundation | Foundational models | 3 |
| Foundation | RSI | 8 |
| Foundation | Data foundations | 9 |
| Foundation | Harness Core | 6 |
| Foundation | Intention compilers | 5 |
| Foundation | Planner | 3 |
| Foundation | Builder | 14 |
| Vertical | Visibility / Statistics | 4 |
| Vertical | Installer & CLI & Webapp | 5 |
| Vertical | UI | 3 |
| Vertical | Account management | 4 |
| Vertical | Message Channels | 3 |
| Vertical | System Configurations | 4 |
| | **25 groups** | **142** |

### 2.2 By semantic owner

| Semantic owner | Rows | Share |
|---|---:|---:|
| AI4RnD Core | 118 | 83% |
| JiuwenSwarm Application | 19 | 13% |
| External / New Product Work | 4 | 3% |
| Unresolved | 1 | 1% |
| **Total** | **142** | **100%** |

The product is overwhelmingly AI4RnD's to define. That is the point of the preservation gate:
changing the execution substrate must not move these rows.

### 2.3 By runtime implementer

| Runtime implementer | Rows | Share |
|---|---:|---:|
| AI4RnD Core | 53 | 37% |
| AI4RnD-Jiuwen Integration | 32 | 23% |
| JiuwenSwarm Application | 27 | 19% |
| OpenJiuwen Runtime | 25 | 18% |
| External / New Product Work | 4 | 3% |
| Unresolved | 1 | 1% |
| **Total** | **142** | **100%** |

Semantic ownership and runtime ownership diverge sharply — 118 rows are AI4RnD's to define but
only 53 are AI4RnD's to run. That gap is the integration surface.

### 2.4 By implementation decision

| Decision | Rows | Share |
|---|---:|---:|
| BUILD | 53 | 37% |
| ADAPT | 32 | 23% |
| REUSE | 23 | 16% |
| PORT | 20 | 14% |
| EXTEND | 11 | 8% |
| DEFER | 2 | 1% |
| UNRESOLVED | 1 | 1% |
| **Total** | **142** | **100%** |

### 2.5 By delivery phase

| Phase | Rows | Share |
|---|---:|---:|
| P1 | 37 | 26% |
| P4 | 35 | 25% |
| P2 | 21 | 15% |
| P3 | 21 | 15% |
| P6 | 15 | 11% |
| P5 | 13 | 9% |
| **Total** | **142** | **100%** |

### 2.6 By confidence

| Confidence | Rows | Share |
|---|---:|---:|
| MEDIUM | 76 | 54% |
| HIGH | 61 | 43% |
| LOW | 5 | 4% |
| **Total** | **142** | **100%** |

### 2.7 By evidence class

| Evidence class | Rows | Share |
|---|---:|---:|
| SRC | 69 | 49% |
| EXEC | 34 | 24% |
| INF | 33 | 23% |
| DOC | 6 | 4% |
| **Total** | **142** | **100%** |

`EXEC` means a probe was executed in this environment during this revision. `SRC` means the
claim rests on reading source. `DOC` means documentation only. `INF` means inference — and every
`INF` row is a row where the analysis is asserting an absence or a design intent it could not
execute against.

---

## 3. Cross-layer features requiring implementation slices

5 of 142 features cross an architectural boundary in a way that a single owner cannot
honestly represent. Each keeps one row and gains named slices.

**FN-19 — 2. Model Routing & Selection** (Foundational models)

| Slice | Owner | Decision |
|---|---|---|
| Model pool and provider configuration | JiuwenSwarm Application | REUSE |
| Capability requirement to model constraint | AI4RnD Core | BUILD |
| Loud-failure binding adapter over resolve_member_model | AI4RnD-Jiuwen Integration | BUILD |

**FN-20 — 3. Model Usage Auditing** (Foundational models)

| Slice | Owner | Decision |
|---|---|---|
| Raw usage capture | JiuwenSwarm Application | REUSE |
| Attribution to project and claim | AI4RnD Core | BUILD |

**FN-40 — 3. DAG Scheduler, TaskGraph Readiness & Operator Binding** (Harness Core)

| Slice | Owner | Decision |
|---|---|---|
| Readiness, ordering, batching | OpenJiuwen Runtime | REUSE |
| Capability binding per node | AI4RnD Core | BUILD |
| Plan to graph compilation | AI4RnD-Jiuwen Integration | BUILD |

**FN-43 — 6. Failure Recovery & Resumability** (Harness Core)

| Slice | Owner | Decision |
|---|---|---|
| Journal replay | OpenJiuwen Runtime | REUSE |
| Resume trigger reachable from the control plane | AI4RnD-Jiuwen Integration | BUILD |
| Failed-step detection and gate blocking | AI4RnD Core | BUILD |

**VT-01 — 1. Workflow & Platform Status Visibility** (Visibility / Statistics)

| Slice | Owner | Decision |
|---|---|---|
| Platform status | JiuwenSwarm Application | REUSE |
| Gate, budget and blocker view | AI4RnD Core | BUILD |

---

## 4. Product-preservation gate

Every one of the 142 outcomes is evaluated against every complete-product architecture option.
An option is not a complete architecture unless it preserves all 142.

| Verdict | A | B | C | D | E |
|---|---:|---:|---:|---:|---:|
| PRESERVED | 70 | 76 | 76 | 58 | 82 |
| PRESERVED WITH ADAPTATION | 12 | 6 | 6 | 23 | 0 |
| NEW BUILD REQUIRED | 58 | 58 | 58 | 57 | 58 |
| UNRESOLVED | 2 | 2 | 2 | 3 | 2 |
| DROPPED | 0 | 0 | 0 | 1 | 0 |
| **Total evaluated** | **142** | **142** | **142** | **142** | **142** |

**Option D drops 1 outcome(s)** and therefore fails the gate:

- `FN-19` 2. Model Routing & Selection — Foundational models

Options with zero DROPPED rows: A, B, C, E.

`NEW BUILD REQUIRED` is identical or near-identical across options (57–58 rows) because those
outcomes do not exist in either system today. **No architecture choice can avoid them.** Any
comparison that shows one option needing dramatically less new work is comparing execution
plumbing, not product.

---

## 5. Unresolved ownership and product-definition questions

2 rows cannot be resolved from the workbook, the repositories or execution. They are
recorded rather than guessed.

- **VT-19 — 3. TMUX** (Message Channels). Open question: the workbook lists TMUX as a message channel, but the recommended architecture retires the tmux carrier
- **VT-23 — 4. Cluster setting** (System Configurations). Genuinely unresolved: 'Cluster setting' is one line in the workbook with no description of scope

Further recorded assumptions:

- **WF-02** — Workbook references a 'V-05' qualification level defined outside the workbook; definition unresolved
- **WF-25** — Confirmed absent in this revision by direct search, matching the prior finding
- **WF-28** — Strategic criteria are organisation-specific; the workbook does not define them
- **WF-46** — This is the single largest correctness risk in the product; the current check does not hold
- **FN-01** — This is the evidence that Capsules are already a governed capability identity, not a workflow template
- **FN-03** — Ranking without refusal is the central mismatch: research must stall honestly, not pick the nearest skill
- **FN-06** — Naming collision confirmed again this revision; AI4RnD's executable unit must not be called Operator inside Jiuwen
- **FN-08** — This is the sharpest verified gap: the knob exists, is validated, and is then ignored
- **FN-15** — Corrects the earlier claim that this was purely an openjiuwen packaging gap - the installed rules file is orphaned
- **FN-19** — Silent fallback is the reason AI4RnD cannot delegate model routing to Jiuwen as-is
- **FN-21** — This is the one RSI surface with real wiring on both sides
- **FN-23** — Corrects the earlier claim that agent_evolving is broadly reusable - today its only subject is one ReAct agent class
- **FN-27** — Deferred on cost and infrastructure grounds, not because the substrate is missing
- **FN-29** — Corrects the earlier open question about whether a persistent checkpointer exists in a stock install - it does
- **FN-37** — Journal path is {team}/sessions/{session_id}/workflows/{name}; a new session gets a new journal and replays nothing
- **FN-40** — Router is invoked with no arguments, so fan-out width must be computed from a closure or channel read, not from a router parameter
- **FN-43** — Two verified defects: resume_id is schema-advertised but unimplemented, and agent failure degrades to None after retries
- **VT-14** — Explicitly out of scope for verification here - the safeguards forbid touching authentication

---

## 6. Reuse claims and their evidence

23 rows claim reuse. 17 rest on executed probes or source reading; 6 rest on documentation alone and are labelled **UNVERIFIED** below.

| Feature | Claim | Evidence |
|---|---|---|
| `VT-05` 1. Windows App | Packaging and installer exist | **UNVERIFIED** (DOC) |
| `VT-06` 2. MacOS App | Packaging exists | **UNVERIFIED** (DOC) |
| `VT-07` 3. MacOS CLI | jiuwenswarm CLI exists | **UNVERIFIED** (DOC) |
| `VT-08` 4. Linux Cli | jiuwenswarm CLI exists | **UNVERIFIED** (DOC) |
| `VT-10` 1. CLI | CLI present | **UNVERIFIED** (DOC) |
| `VT-12` 3. TUI | jiuwenswarm-tui package exists | **UNVERIFIED** (DOC) |

These six are all packaging and distribution rows. Verifying them requires building installers
on Windows and macOS, which this environment cannot do.

---

## 7. The full matrix

Columns are abbreviated for width; the CSV carries all 26.


### Workflow · Ingestion

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `WF-01` | 1. Request Capture | AI4RnD Core | JiuwenSwarm Application | **EXTEND** | SRC | HIGH | Bind a captured request to an AI4RnD project record and Contract draft |
| `WF-02` | 2. Qualified Channel Signal Intake | AI4RnD Core | JiuwenSwarm Application | **BUILD** | INF | MEDIUM | V-05 qualification tier and clue schema |
| `WF-03` | 3. User-Supplied Material Import | AI4RnD Core | JiuwenSwarm Application | **REUSE** | SRC | HIGH | Attach imported material to the project record as first-class evidence |
| `WF-04` | 4. Intake Context Binding | AI4RnD Core | JiuwenSwarm Application | **ADAPT** | SRC | HIGH | project_id in session metadata; project<->session link that survives restart |
| `WF-05` | 5. Real-Time Intake Deduplication & Cleaning | AI4RnD Core | JiuwenSwarm Application | **PORT** | SRC | MEDIUM | Canonicalisation rules for research intake |
| `WF-06` | 6. Intake Provenance Registration | AI4RnD Core | JiuwenSwarm Application | **PORT** | EXEC | HIGH | Bind intake provenance to the ledger at capture time |
| `WF-07` | 7. Intake Qualification | AI4RnD Core | JiuwenSwarm Application | **ADAPT** | SRC | MEDIUM | Intake qualification rule set and its gate |

### Workflow · Requirement compilation

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `WF-08` | 1. Intent Interpretation | AI4RnD Core | AI4RnD Core | **ADAPT** | SRC | HIGH | Map compiled intent onto the Contract schema |
| `WF-09` | 2. Context Scoping | AI4RnD Core | AI4RnD Core | **ADAPT** | SRC | MEDIUM | Scope as a Contract field with an explicit boundary |
| `WF-10` | 3. Ambiguity Resolution | AI4RnD Core | AI4RnD Core | **ADAPT** | SRC | MEDIUM | Ambiguity questions raised as a first-class blocking state |
| `WF-11` | 4. Constraint Resolution | AI4RnD Core | AI4RnD Core | **ADAPT** | SRC | MEDIUM | Research constraint vocabulary (budget, time, data, IP) |
| `WF-12` | 5. Requirement Prioritization | AI4RnD Core | AI4RnD Core | **BUILD** | INF | MEDIUM | Requirement prioritisation model |
| `WF-13` | 6. Acceptance Definition | AI4RnD Core | AI4RnD Core | **ADAPT** | SRC | HIGH | Project-level acceptance definition distinct from capsule-level |
| `WF-14` | 7. Requirement Contract Confirmation | AI4RnD Core | AI4RnD Core | **BUILD** | INF | MEDIUM | Contract confirmation gate with a durable record |

### Workflow · Search & ideation

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `WF-15` | 1. Search Strategy Formation | AI4RnD Core | AI4RnD-Jiuwen Integration | **PORT** | SRC | HIGH | Strategy as a reviewable plan artifact |
| `WF-16` | 2. Multi-Source Signal Discovery | AI4RnD Core | AI4RnD-Jiuwen Integration | **PORT** | SRC | HIGH | Compile discovery fan-out to SwarmFlow |
| `WF-17` | 3. Source Qualification | AI4RnD Core | AI4RnD-Jiuwen Integration | **PORT** | EXEC | HIGH | Qualification thresholds as policy, not code constants |
| `WF-18` | 4. Technical Signal Extraction | AI4RnD Core | AI4RnD-Jiuwen Integration | **PORT** | SRC | MEDIUM | Typed signal schema |
| `WF-19` | 5. Signal Organization | AI4RnD Core | AI4RnD-Jiuwen Integration | **PORT** | SRC | MEDIUM | Projection into the concept graph |
| `WF-20` | 6. Trend & Gap Analysis | AI4RnD Core | AI4RnD-Jiuwen Integration | **PORT** | SRC | MEDIUM | Gap statements bound to evidence |
| `WF-21` | 7. Idea Generation | AI4RnD Core | AI4RnD-Jiuwen Integration | **PORT** | SRC | MEDIUM | Wire the capsule to a runner |
| `WF-22` | 8. Search Coverage Review | AI4RnD Core | AI4RnD-Jiuwen Integration | **BUILD** | INF | MEDIUM | Coverage metric and stopping rule |

### Workflow · Idea identification / screening / opportunity selection

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `WF-23` | 1. Candidate Consolidation | AI4RnD Core | AI4RnD Core | **BUILD** | INF | MEDIUM | Consolidation stage across discovery runs |
| `WF-24` | 2. Idea Identification | AI4RnD Core | AI4RnD Core | **ADAPT** | SRC | MEDIUM | Identification distinct from evaluation |
| `WF-25` | 3. Idea Card Formation | AI4RnD Core | AI4RnD Core | **BUILD** | EXEC | HIGH | Idea Card schema and its editor |
| `WF-26` | 4. Opportunity Definition | AI4RnD Core | AI4RnD Core | **BUILD** | INF | MEDIUM | Opportunity record distinct from idea |
| `WF-27` | 5. Technical Opportunity Screening | AI4RnD Core | AI4RnD Core | **ADAPT** | SRC | MEDIUM | Screening as a gate with a recorded verdict |
| `WF-28` | 6. Strategic Opportunity Screening | AI4RnD Core | AI4RnD Core | **BUILD** | INF | LOW | Strategic criteria and their owner |
| `WF-29` | 7. Opportunity Portfolio Prioritization | AI4RnD Core | AI4RnD Core | **BUILD** | INF | MEDIUM | Portfolio prioritisation across projects |

### Workflow · Generate technical claims & hypothesis

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `WF-30` | 1. Research Question & Technical Claim Formation | AI4RnD Core | AI4RnD Core | **PORT** | SRC | HIGH | Research question as a distinct object from the claim |
| `WF-31` | 2. Claim, Evidence, Data & Method Modeling | AI4RnD Core | AI4RnD Core | **PORT** | EXEC | HIGH | Data and method as first-class model elements |
| `WF-32` | 3. Hypothesis Pool & Mechanism Formation | AI4RnD Core | AI4RnD Core | **BUILD** | INF | MEDIUM | Hypothesis pool and mechanism model |
| `WF-33` | 4. Falsifiability Screening & Hypothesis Contracting | AI4RnD Core | AI4RnD Core | **BUILD** | EXEC | HIGH | Falsifiability screening and hypothesis contracting - the scientific core |
| `WF-34` | 5. Verification-Ready POC Design | AI4RnD Core | AI4RnD Core | **ADAPT** | SRC | MEDIUM | Design tied to the falsifiability verdict |

### Workflow · POC implementation

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `WF-35` | 1. POC Implementation Environment Preparation | AI4RnD Core | OpenJiuwen Runtime | **REUSE** | SRC | HIGH | Bind environment to the capsule effects declaration |
| `WF-36` | 2. POC Construction | AI4RnD Core | OpenJiuwen Runtime | **REUSE** | SRC | HIGH | Construction driven by a Build Contract rather than a free-form prompt |
| `WF-37` | 3. POC Component Integration & Configuration | AI4RnD Core | OpenJiuwen Runtime | **ADAPT** | SRC | MEDIUM | Component integration as a declared step with its own acceptance |
| `WF-38` | 4. POC Functional Readiness Validation | AI4RnD Core | OpenJiuwen Runtime | **BUILD** | INF | MEDIUM | Functional readiness checks before benchmark handoff |
| `WF-39` | 5. Testable POC Artifact Consolidation & Benchmark Handoff | AI4RnD Core | OpenJiuwen Runtime | **BUILD** | INF | MEDIUM | Testable artifact manifest and handoff contract |

### Workflow · Benchmarking

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `WF-40` | 1. Benchmark Framing | AI4RnD Core | AI4RnD-Jiuwen Integration | **ADAPT** | SRC | MEDIUM | Framing tied to the claim under test |
| `WF-41` | 2. Benchmark Protocol & Asset Preparation | AI4RnD Core | AI4RnD-Jiuwen Integration | **PORT** | SRC | MEDIUM | Protocol as a versioned artifact |
| `WF-42` | 3. Benchmark Execution | AI4RnD Core | AI4RnD-Jiuwen Integration | **REUSE** | EXEC | HIGH | Benchmark runs registered as AI4RnD evidence |
| `WF-43` | 4. Metrics & Run Evidence Collection | AI4RnD Core | AI4RnD-Jiuwen Integration | **PORT** | SRC | MEDIUM | Run evidence bound to the claim graph |
| `WF-44` | 5. Comparative Result Analysis & Benchmark Result Packaging | AI4RnD Core | AI4RnD-Jiuwen Integration | **BUILD** | INF | MEDIUM | Comparative analysis with baselines and packaging |

### Workflow · Evaluation

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `WF-45` | 1. Evaluation Scope & Evidence Assembly | AI4RnD Core | AI4RnD Core | **ADAPT** | EXEC | HIGH | Scope declaration for an evaluation round |
| `WF-46` | 2. Evidence Completeness & Provenance Review | AI4RnD Core | AI4RnD Core | **ADAPT** | EXEC | HIGH | Replace the grounding check with calibrated entailment; publish a measured bar |
| `WF-47` | 3. Experimental, Reasoning & External Validity Review | AI4RnD Core | AI4RnD Core | **BUILD** | INF | MEDIUM | Experimental, reasoning and external validity as separate reviews |
| `WF-48` | 4. Claim & Acceptance-Criteria Comparison | AI4RnD Core | AI4RnD Core | **ADAPT** | SRC | MEDIUM | Comparison against the project Contract acceptance criteria |
| `WF-49` | 5. Verdict, Blocker & Residual-Risk Classification | AI4RnD Core | AI4RnD Core | **PORT** | EXEC | HIGH | Residual-risk classification vocabulary |
| `WF-50` | 6. Refinement & Follow-Up Recording | AI4RnD Core | AI4RnD Core | **BUILD** | INF | MEDIUM | Refinement and follow-up as tracked items |

### Workflow · Delivery

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `WF-51` | 1. Delivery Planning & Evidence Handoff | AI4RnD Core | AI4RnD-Jiuwen Integration | **BUILD** | INF | MEDIUM | Delivery plan and evidence handoff |
| `WF-52` | 2. User-Facing Deliverable Generation | AI4RnD Core | AI4RnD-Jiuwen Integration | **PORT** | SRC | MEDIUM | Deliverable templates bound to audience |
| `WF-53` | 3. Deliverable, Reusable Asset & Knowledge Packaging | AI4RnD Core | AI4RnD-Jiuwen Integration | **BUILD** | INF | MEDIUM | Reusable asset extraction and knowledge packaging |
| `WF-54` | 4. Authorized Distribution, Knowledge Transfer & Lifecycle Closure | AI4RnD Core | AI4RnD-Jiuwen Integration | **ADAPT** | SRC | MEDIUM | Authorized distribution and project closure semantics |

### Foundation · Capability capsule

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `FN-01` | 1. Capability Capsule Definition & Assembly | AI4RnD Core | AI4RnD Core | **REUSE** | EXEC | HIGH | Assembly UI and schema versioning |
| `FN-02` | 2. Capsule Governance, Certification & Registry Management | AI4RnD Core | AI4RnD Core | **EXTEND** | EXEC | HIGH | Certification workflow, suspend/deprecate transitions, promotion history |
| `FN-03` | 3. Capability Discovery, Scoring & Selection | AI4RnD Core | AI4RnD Core | **ADAPT** | EXEC | HIGH | Hard capability gate with discriminated stall reasons - Symphony ranks but never refuses |
| `FN-04` | 4. Capsule Invocation & Composition | AI4RnD Core | AI4RnD Core | **EXTEND** | SRC | MEDIUM | Composition planner that uses the declared compatibility |
| `FN-05` | 5. Capability Capsule Evolution & Version Promotion | AI4RnD Core | AI4RnD Core | **BUILD** | EXEC | HIGH | Capsule version promotion, rollback, performance history and RSI target declaration |

### Foundation · Operators

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `FN-06` | 1. 逻辑算子定义、组装与注册 — Logical Operator Definition, Assembly & Registration | AI4RnD Core | AI4RnD-Jiuwen Integration | **PORT** | SRC | MEDIUM | A distinct name for AI4RnD's executable unit to avoid the collision; registration API |
| `FN-07` | 2. 算子准入、认证与治理 — Operator Qualification, Admission & Governance | AI4RnD Core | AI4RnD-Jiuwen Integration | **BUILD** | SRC | MEDIUM | Admission, certification and governance lifecycle for operators |
| `FN-08` | 3. 逻辑—物理算子匹配、选择与绑定 — Logical-to-Physical Matching, Selection & Binding | AI4RnD Core | AI4RnD-Jiuwen Integration | **BUILD** | EXEC | HIGH | Binding layer that turns a logical requirement into a concrete executor and fails when none matches |
| `FN-09` | 4. 物理算子与执行舰队管理 — Physical Operator & Execution Fleet Management | AI4RnD Core | AI4RnD-Jiuwen Integration | **ADAPT** | SRC | MEDIUM | Fleet management driven by capsule bindings |
| `FN-10` | 5. 算子运行评估与能力画像 — Operator Runtime Evaluation & Capability Profiling | AI4RnD Core | AI4RnD-Jiuwen Integration | **BUILD** | INF | MEDIUM | Per-operator capability profile built from run evidence |
| `FN-11` | 6. 评估器驱动的算子演进 — Evaluator-Driven Operator Evolution | AI4RnD Core | AI4RnD-Jiuwen Integration | **BUILD** | SRC | MEDIUM | Evaluator-driven operator evolution wired to a governed promotion gate |

### Foundation · Evaluator

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `FN-12` | 1. Contract, Schema & Artifact Conformance Evaluator | AI4RnD Core | AI4RnD Core | **ADAPT** | EXEC | HIGH | Conformance evaluator that runs the declared checks |
| `FN-13` | 2. Engineering Correctness & Code Quality Evaluator | AI4RnD Core | AI4RnD Core | **BUILD** | INF | MEDIUM | Engineering correctness and code quality evaluator family |
| `FN-14` | 3. Performance, Cost & Benchmark Evaluator | AI4RnD Core | AI4RnD Core | **ADAPT** | SRC | MEDIUM | Performance, cost and benchmark evaluator family |
| `FN-15` | 4. Security, Privacy, Compliance & IP Evaluator | AI4RnD Core | AI4RnD Core | **BUILD** | EXEC | HIGH | Security, privacy, compliance and IP evaluator; and a guardrail tier that actually loads |
| `FN-16` | 5. Evidence, Factuality & Scientific Validity Evaluator | AI4RnD Core | AI4RnD Core | **BUILD** | EXEC | HIGH | Calibrated entailment evaluator - the scientific core of the product |
| `FN-17` | 6. Lifecycle, Parity & Human Review Evaluator | AI4RnD Core | AI4RnD Core | **BUILD** | INF | MEDIUM | Lifecycle, parity and human review evaluator |

### Foundation · Foundational models

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `FN-18` | 1. Model Capability Registry | JiuwenSwarm Application | JiuwenSwarm Application | **EXTEND** | SRC | HIGH | Capability profile per model (context, tools, structured output, cost tier) |
| `FN-19` | 2. Model Routing & Selection | AI4RnD Core | AI4RnD-Jiuwen Integration | **BUILD** | SRC | HIGH | Routing that fails loudly when the required model is unavailable |
| `FN-20` | 3. Model Usage Auditing | JiuwenSwarm Application | JiuwenSwarm Application | **EXTEND** | SRC | MEDIUM | Audit attributable to project, claim and capsule |

### Foundation · RSI

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `FN-21` | 1. Text-Based Artifacts (GEPA / MIPROv2 / TextGrad) | AI4RnD Core | AI4RnD-Jiuwen Integration | **ADAPT** | SRC | HIGH | Governed promotion for text artifacts |
| `FN-22` | 2. Runtime and Resource Routing (Bayesian Optimization / Bandits / Cost-Aware RL) | AI4RnD Core | AI4RnD-Jiuwen Integration | **BUILD** | SRC | MEDIUM | Runtime and resource routing optimisation |
| `FN-23` | 3. Capability Capsules and Physical Operators (Trajectory Mining / Code Evolution / CEGIS) | AI4RnD Core | AI4RnD-Jiuwen Integration | **BUILD** | EXEC | HIGH | Bind capsules and physical operators as evolution subjects |
| `FN-24` | 4. DAG and Agent Organization (AFlow / MCTS / ADAS) | AI4RnD Core | AI4RnD-Jiuwen Integration | **BUILD** | SRC | MEDIUM | DAG and agent organisation evolution |
| `FN-25` | 5. Evaluator, Reward, Contract, and Governance (Judge Calibration / Reward Modeling / CEGIS) | AI4RnD Core | AI4RnD-Jiuwen Integration | **ADAPT** | SRC | MEDIUM | Evaluator, reward and contract evolution under a frozen-policy guard |
| `FN-26` | 6. Memory, Retrieval, and Evidence (Memory Learning / Self-RAG / Reranker Training) | AI4RnD Core | AI4RnD-Jiuwen Integration | **BUILD** | SRC | MEDIUM | Memory, retrieval and evidence evolution |
| `FN-27` | 7. Model Policies and Weights (SFT / LoRA / DPO / GRPO / Agent RL) | AI4RnD Core | AI4RnD-Jiuwen Integration | **DEFER** | SRC | MEDIUM | Model policy and weight evolution |
| `FN-28` | 8. Data, Benchmarks, Curriculum, and Observability (Active Learning / Hard-Case Mining / Credit Assignment) | AI4RnD Core | AI4RnD-Jiuwen Integration | **BUILD** | INF | MEDIUM | Data, benchmark and curriculum evolution with observability |

### Foundation · Data foundations

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `FN-29` | 1. Persistent Memory & Context Retrieval | AI4RnD Core | AI4RnD Core | **EXTEND** | SRC | MEDIUM | Research-grade retrieval over project memory |
| `FN-30` | 2. Concept Graph Management | AI4RnD Core | AI4RnD Core | **BUILD** | EXEC | HIGH | Concept graph as a typed projection |
| `FN-31` | 3. Dataset Graph Management | AI4RnD Core | AI4RnD Core | **BUILD** | EXEC | HIGH | Dataset graph |
| `FN-32` | 4. Code Graph Management | AI4RnD Core | AI4RnD Core | **BUILD** | EXEC | HIGH | Code graph |
| `FN-33` | 5. Policy Graph Management | AI4RnD Core | AI4RnD Core | **BUILD** | EXEC | HIGH | Policy graph |
| `FN-34` | 6. Workflow Graph Management | AI4RnD Core | AI4RnD Core | **BUILD** | EXEC | HIGH | Workflow graph |
| `FN-35` | 7. Trace Graph Management | AI4RnD Core | AI4RnD Core | **BUILD** | EXEC | HIGH | Trace graph |
| `FN-36` | 8. Memory Graph Management | AI4RnD Core | AI4RnD Core | **BUILD** | EXEC | HIGH | Memory graph |
| `FN-37` | 9. TaskGraph Persistence & Lifecycle Management | AI4RnD Core | AI4RnD Core | **ADAPT** | SRC | HIGH | TaskGraph lifecycle that spans sessions - the SwarmFlow journal is keyed by session id |

### Foundation · Harness Core

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `FN-38` | 1. Runtime Control Loop & Run Lifecycle Management | AI4RnD Core | OpenJiuwen Runtime | **REUSE** | EXEC | HIGH | Project-level run lifecycle above the session |
| `FN-39` | 2. Message Bus & Durable Task Queue | AI4RnD Core | OpenJiuwen Runtime | **REUSE** | SRC | HIGH | Nothing at this layer |
| `FN-40` | 3. DAG Scheduler, TaskGraph Readiness & Operator Binding | AI4RnD Core | OpenJiuwen Runtime | **ADAPT** | EXEC | HIGH | Capability binding at node level - the part Pregel does not do |
| `FN-41` | 4. Execution Admission, Lease & Concurrency Control | AI4RnD Core | OpenJiuwen Runtime | **REUSE** | EXEC | HIGH | Nothing at this layer |
| `FN-42` | 5. Main Loop Dispatch & Runtime Supervision | AI4RnD Core | OpenJiuwen Runtime | **REUSE** | SRC | HIGH | Nothing at this layer |
| `FN-43` | 6. Failure Recovery & Resumability | AI4RnD Core | OpenJiuwen Runtime | **ADAPT** | EXEC | HIGH | Reachable resume - the leader-facing swarmflow tool advertises resume_id and then rejects it, and a failed step returns None instead of failing the run |

### Foundation · Intention compilers

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `FN-44` | 1. Intent Classification & Compilation Variant Selection | AI4RnD Core | AI4RnD Core | **ADAPT** | SRC | MEDIUM | Compilation variant selection distinct from routing |
| `FN-45` | 2. Goal, Scope and Context normalization | AI4RnD Core | AI4RnD Core | **ADAPT** | SRC | MEDIUM | Normalisation to a canonical Contract shape |
| `FN-46` | 3. Ambiguity Resolution & Readiness | AI4RnD Core | AI4RnD Core | **ADAPT** | SRC | MEDIUM | Readiness as a checkable state |
| `FN-47` | 4. Constraint Compilation | AI4RnD Core | AI4RnD Core | **BUILD** | INF | MEDIUM | Constraint compilation into executable checks |
| `FN-48` | 5. Task Contract & Acceptance Compilation | AI4RnD Core | AI4RnD Core | **ADAPT** | EXEC | HIGH | Project-level Task Contract with acceptance compilation |

### Foundation · Planner

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `FN-49` | 1. Task Contract Decomposition | AI4RnD Core | AI4RnD Core | **ADAPT** | SRC | MEDIUM | Decomposition driven by the Contract |
| `FN-50` | 2. TaskGraph Construction | AI4RnD Core | AI4RnD Core | **ADAPT** | SRC | HIGH | Separation of the logical plan from the runtime graph |
| `FN-51` | 3. TaskGraph Validation & Feasibility Analysis | AI4RnD Core | AI4RnD Core | **ADAPT** | EXEC | HIGH | Feasibility analysis against available capabilities |

### Foundation · Builder

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `FN-52` | 1. Build Contract Interpretation | AI4RnD Core | OpenJiuwen Runtime | **BUILD** | INF | MEDIUM | Build Contract interpretation |
| `FN-53` | 2. Build Preparation | AI4RnD Core | OpenJiuwen Runtime | **REUSE** | SRC | HIGH | Preparation driven by declared effects |
| `FN-54` | 3. Code Construction | AI4RnD Core | OpenJiuwen Runtime | **REUSE** | SRC | HIGH | Construction bound to a Build Contract |
| `FN-55` | 4. Model Construction | AI4RnD Core | OpenJiuwen Runtime | **DEFER** | INF | LOW | Model construction pipeline |
| `FN-56` | 5. Experimental Asset Construction | AI4RnD Core | OpenJiuwen Runtime | **BUILD** | INF | MEDIUM | Experimental asset construction as a declared step |
| `FN-57` | 6. Benchmark Asset Construction | AI4RnD Core | OpenJiuwen Runtime | **PORT** | SRC | MEDIUM | Wire to the benchmark lane |
| `FN-58` | 7. Verification Asset Construction | AI4RnD Core | OpenJiuwen Runtime | **BUILD** | INF | MEDIUM | Verification asset construction |
| `FN-59` | 8. Decision Artifact Construction | AI4RnD Core | OpenJiuwen Runtime | **BUILD** | INF | MEDIUM | Decision artifact schema |
| `FN-60` | 9. Prototype Assembly | AI4RnD Core | OpenJiuwen Runtime | **BUILD** | INF | MEDIUM | Assembly as a declared step with acceptance |
| `FN-61` | 10. Product Integration | AI4RnD Core | OpenJiuwen Runtime | **BUILD** | INF | LOW | Product integration |
| `FN-62` | 11. Defect Repair | AI4RnD Core | OpenJiuwen Runtime | **REUSE** | SRC | MEDIUM | Repair bound to a recorded defect |
| `FN-63` | 12. Build Evidence Generation | AI4RnD Core | OpenJiuwen Runtime | **PORT** | EXEC | HIGH | Build evidence linked to the Build Contract |
| `FN-64` | 13. Report/Paper/Deliverable Construction | AI4RnD Core | OpenJiuwen Runtime | **PORT** | SRC | MEDIUM | Deliverable construction bound to the evidence ledger |
| `FN-65` | 14. Runtime Deliverable Construction | AI4RnD Core | OpenJiuwen Runtime | **BUILD** | INF | LOW | Runtime deliverable packaging |

### Vertical · Visibility / Statistics

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `VT-01` | 1. Workflow & Platform Status Visibility | AI4RnD Core | JiuwenSwarm Application | **EXTEND** | SRC | MEDIUM | Research-specific progress: gates, budgets, blockers |
| `VT-02` | 2. Execution Trace Search & Inspection | JiuwenSwarm Application | JiuwenSwarm Application | **EXTEND** | SRC | MEDIUM | Search across time-ordered transitions bound to claims |
| `VT-03` | 3. Runtime status visibility | JiuwenSwarm Application | JiuwenSwarm Application | **BUILD** | INF | MEDIUM | Host resource statistics |
| `VT-04` | 4. Resource Usage, Cost & Capacity Management | JiuwenSwarm Application | JiuwenSwarm Application | **EXTEND** | SRC | MEDIUM | Cost and capacity against a project budget |

### Vertical · Installer & CLI & Webapp

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `VT-05` | 1. Windows App | JiuwenSwarm Application | JiuwenSwarm Application | **REUSE** | DOC | MEDIUM | Research mode included in the package |
| `VT-06` | 2. MacOS App | JiuwenSwarm Application | JiuwenSwarm Application | **REUSE** | DOC | MEDIUM | Single installer for the combined product |
| `VT-07` | 3. MacOS CLI | JiuwenSwarm Application | JiuwenSwarm Application | **REUSE** | DOC | MEDIUM | Research commands in the CLI |
| `VT-08` | 4. Linux Cli | JiuwenSwarm Application | JiuwenSwarm Application | **REUSE** | DOC | MEDIUM | Research commands in the CLI |
| `VT-09` | 5. Web Application & Status Service | JiuwenSwarm Application | JiuwenSwarm Application | **REUSE** | SRC | HIGH | Project routes |

### Vertical · UI

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `VT-10` | 1. CLI | JiuwenSwarm Application | JiuwenSwarm Application | **REUSE** | DOC | MEDIUM | Nothing beyond VT-07 |
| `VT-11` | 2. GUI | JiuwenSwarm Application | JiuwenSwarm Application | **EXTEND** | SRC | HIGH | Project view, plan inspector, evidence browser, improvements inbox |
| `VT-12` | 3. TUI | JiuwenSwarm Application | JiuwenSwarm Application | **REUSE** | DOC | MEDIUM | Research views in the TUI |

### Vertical · Account management

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `VT-13` | 1. Account Registration | External / New Product Work | External / New Product Work | **BUILD** | EXEC | HIGH | The whole account subsystem |
| `VT-14` | 2. Authentication & Session Security | External / New Product Work | External / New Product Work | **BUILD** | EXEC | HIGH | Authentication and session security |
| `VT-15` | 3. User Profile Management | External / New Product Work | External / New Product Work | **BUILD** | INF | HIGH | User profile management |
| `VT-16` | 4. Privacy & Personal Data Controls | External / New Product Work | External / New Product Work | **BUILD** | INF | HIGH | Privacy and personal data controls |

### Vertical · Message Channels

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `VT-17` | 1. Wechat | JiuwenSwarm Application | JiuwenSwarm Application | **REUSE** | SRC | HIGH | Project notifications on the channel |
| `VT-18` | 2. Discord | JiuwenSwarm Application | JiuwenSwarm Application | **REUSE** | SRC | HIGH | Project notifications |
| `VT-19` | 3. TMUX | JiuwenSwarm Application | JiuwenSwarm Application | **PORT** | SRC | HIGH | Decide whether tmux remains a channel or is retired with the cockpit |

### Vertical · System Configurations

| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |
|---|---|---|---|---|---|---|---|
| `VT-20` | 1. LLM Config | JiuwenSwarm Application | JiuwenSwarm Application | **REUSE** | SRC | HIGH | Research-specific model policy |
| `VT-21` | 2. User Settings | JiuwenSwarm Application | JiuwenSwarm Application | **REUSE** | SRC | MEDIUM | Research preferences |
| `VT-22` | 3. Cost/Budget Settings | JiuwenSwarm Application | JiuwenSwarm Application | **EXTEND** | SRC | MEDIUM | Budget settings surface and enforcement per project |
| `VT-23` | 4. Cluster setting | Unresolved | Unresolved | **UNRESOLVED** | INF | LOW | Cluster semantics for the combined product are undefined |

---

## 8. How to read a decision

| Decision | Meaning |
|---|---|
| `REUSE` | Jiuwen or AI4RnD already does this; use it unchanged |
| `CONFIGURE` | Exists; needs configuration only |
| `ADAPT` | Exists on one side but must change shape to serve the product outcome |
| `PORT` | Exists in AI4RnD; move it onto the Jiuwen foundation |
| `EXTEND` | Exists in Jiuwen; add the research-specific layer above it |
| `BUILD` | Does not exist in either system |
| `DEFER` | Deliberately postponed with a stated reason |
| `UNRESOLVED` | Cannot be decided from available evidence |
