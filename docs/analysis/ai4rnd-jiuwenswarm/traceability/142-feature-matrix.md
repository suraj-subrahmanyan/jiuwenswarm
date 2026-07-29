# 142-Feature Traceability Matrix

Controlling set: every Level-2 row of `AI4RnD Feature List.xlsx` (Workflow 54 + Foundation 65 + Vertical 23 = 142).

Machine-readable copy: [`142-feature-matrix.csv`](142-feature-matrix.csv).

> **Revision 3.** 16 rows were re-scored after the openjiuwen execution-mechanism inventory
> ([16](../16-jiuwen-execution-mechanisms.md)). JiuwenSwarm coverage rose from 20 to **23 FULL**,
> and NONE fell from 72 to **62**. Disposition shifted from PORT (69→61) to REUSE-JW (23→33):
> durable queueing, admission, resumability and most RSI surfaces already exist upstream.

## Legend

| Column | Values |
|---|---|
| **Firmness** | `FIRM` a stated target · `DEBATED` design still moving (per workbook notes) · `ASPIRE` directional only |
| **AI4RnD maturity** | `ACTIVE` wired into a runtime path · `IMPL-UNWIRED` implemented + tested but no live caller · `SCAFFOLD` partial/thin · `SPEC` described only · `ABSENT` not present |
| **JW coverage** | `FULL` usable as-is · `PARTIAL` exists with gaps · `NONE` — *"JW" means JiuwenSwarm **and** openjiuwen* |
| **Evidence class** | `EXEC` executed in this analysis · `SRC` source-read · `DOC` documentation only |
| **Disposition** | `REUSE-JW` · `PORT` bring AI4RnD code across · `ADAPT` rework · `BUILD` new · `DEFER` |

## Roll-up

**Firmness** — `FIRM` 128 · `DEBATED` 11 · `ASPIRE` 3

**AI4RnD maturity** — `ACTIVE` 68 · `IMPL-UNWIRED` 27 · `SCAFFOLD` 21 · `SPEC` 16 · `ABSENT` 10

**JiuwenSwarm + openjiuwen coverage** — `NONE` 62 · `PARTIAL` 57 · `FULL` 23

**Disposition** — `PORT` 61 · `REUSE-JW` 33 · `ADAPT` 25 · `BUILD` 22 · `DEFER` 1

**Evidence class** — `EXEC` 74 · `SRC` 66 · `DOC` 2


---


### Workflow › Ingestion

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 1 | 1. Request Capture | FIRM | ACTIVE | FULL | EXEC | **REUSE-JW** | JW gateway/channel_manager (9 IM+web+TUI+ACP); AI4R workflow_intake.py:1-24 | channel->run binding |
| 2 | 2. Qualified Channel Signal Intake | DEBATED | SPEC | PARTIAL | SRC | **BUILD** | JW im_pipeline/im_inbound.py; V-05 qualification not implemented either side | define V-05 qualification contract |
| 3 | 3. User-Supplied Material Import | FIRM | ACTIVE | FULL | SRC | **REUSE-JW** | JW file services per channel; AI4R source_manifest.py, knowledge_ingest_registry.py | large-file/dataset limits |
| 4 | 4. Intake Context Binding | FIRM | ACTIVE | PARTIAL | SRC | **ADAPT** | JW session/workspace binding; AI4R workspace_binding.py | project/workspace model mismatch |
| 5 | 5. Real-Time Intake Deduplication & Cleaning | FIRM | IMPL-UNWIRED | NONE | EXEC | **PORT** | AI4R lib/research/ids.py deterministic ids + content_hash; dedup in mirage_search | near-duplicate policy |
| 6 | 6. Intake Provenance Registration | FIRM | ACTIVE | NONE | EXEC | **PORT** | AI4R research SourceDocument.content_hash; evidence ledger provenance | provenance schema vs JW session |
| 7 | 7. Intake Qualification | FIRM | IMPL-UNWIRED | NONE | SRC | **PORT** | AI4R workflow_intake fail-closed (exit 3/4); quarantine in coordinator | quarantine semantics |

### Workflow › Requirement compilation

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 8 | 1. Intent Interpretation | FIRM | ACTIVE | PARTIAL | EXEC | **PORT** | AI4R intent_gateway.py(736) + intent_engine_adapter.py(851) wired | overlap with JW plan mode |
| 9 | 2. Context Scoping | FIRM | ACTIVE | PARTIAL | EXEC | **PORT** | AI4R requirement_compiler/, requirement_coverage.py(471) wired | — |
| 10 | 3. Ambiguity Resolution | FIRM | ACTIVE | PARTIAL | SRC | **ADAPT** | AI4R intent_gateway ambiguity path; JW structured_ask_user rail | who owns clarification UX |
| 11 | 4. Constraint Resolution | FIRM | IMPL-UNWIRED | PARTIAL | SRC | **PORT** | AI4R workflow_contract.py(1136); JW permissions config | constraint->permission mapping |
| 12 | 5. Requirement Prioritization | FIRM | SPEC | NONE | SRC | **BUILD** | AI4R feature-list only; no prioritisation module found | — |
| 13 | 6. Acceptance Definition | FIRM | ACTIVE | NONE | SRC | **PORT** | AI4R contract Done+verify blocks (contract-template-v2), solar-verify | — |
| 14 | 7. Requirement Contract Confirmation | FIRM | ACTIVE | NONE | EXEC | **PORT** | AI4R workflow_contract instantiate + hash/version; task_graph carries contract id | — |

### Workflow › Search & ideation

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 15 | 1. Search Strategy Formation | FIRM | ACTIVE | PARTIAL | EXEC | **PORT** | AI4R research/cli survey-plan; JW Symphony orchestration (different purpose) | — |
| 16 | 2. Multi-Source Signal Discovery | FIRM | ACTIVE | PARTIAL | EXEC | **PORT** | AI4R mirage_search.py(931), gemini_enhanced_search.py, research search | connector auth/quotas |
| 17 | 3. Source Qualification | FIRM | ACTIVE | NONE | EXEC | **PORT** | AI4R evaluator._source_authority_metrics + policies/source_authority.json | — |
| 18 | 4. Technical Signal Extraction | FIRM | ACTIVE | NONE | EXEC | **PORT** | AI4R research extract -> evidence spans [0,150) verified in run | — |
| 19 | 5. Signal Organization | FIRM | ACTIVE | NONE | EXEC | **PORT** | AI4R research mine -> 3 claims/3 links verified; signal clustering in survey | — |
| 20 | 6. Trend & Gap Analysis | FIRM | IMPL-UNWIRED | NONE | SRC | **PORT** | AI4R survey/source_gap.py, tech_hotspot_radar/ | — |
| 21 | 7. Idea Generation | DEBATED | SPEC | NONE | SRC | **BUILD** | Idea generation specified; no dedicated module found | is this LLM-only or structured? |
| 22 | 8. Search Coverage Review | FIRM | IMPL-UNWIRED | NONE | EXEC | **PORT** | AI4R evaluator._source_diversity_metrics + survey/gates/source_quality_distribution | — |

### Workflow › Idea identification / screening / opportunity selection

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 23 | 1. Candidate Consolidation | FIRM | SPEC | NONE | SRC | **BUILD** | Consolidation specified; partial in survey/chief_editor | — |
| 24 | 2. Idea Identification | DEBATED | SPEC | NONE | SRC | **BUILD** | No idea-identification module found | — |
| 25 | 3. Idea Card Formation | FIRM | SPEC | NONE | SRC | **BUILD** | Idea Card is the governing artifact; schema not found in code | Idea Card schema is a gap |
| 26 | 4. Opportunity Definition | FIRM | SPEC | NONE | SRC | **BUILD** | No opportunity-definition module | — |
| 27 | 5. Technical Opportunity Screening | FIRM | SPEC | NONE | SRC | **BUILD** | Screening specified only | — |
| 28 | 6. Strategic Opportunity Screening | DEBATED | SPEC | NONE | SRC | **BUILD** | Strategic screening; overlaps product judgement | who decides strategic fit |
| 29 | 7. Opportunity Portfolio Prioritization | FIRM | SPEC | NONE | SRC | **BUILD** | Portfolio prioritisation specified only | — |

### Workflow › Generate technical claims & hypothesis

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 30 | 1. Research Question & Technical Claim Formation | FIRM | SCAFFOLD | NONE | EXEC | **PORT** | AI4R research Claim dataclass + claim_type; formation not automated | — |
| 31 | 2. Claim, Evidence, Data & Method Modeling | FIRM | ACTIVE | NONE | EXEC | **PORT** | AI4R Claim/EvidenceItem/ClaimEvidenceLink schemas executed | — |
| 32 | 3. Hypothesis Pool & Mechanism Formation | FIRM | SPEC | NONE | SRC | **BUILD** | Hypothesis pool not implemented | — |
| 33 | 4. Falsifiability Screening & Hypothesis Contracting | FIRM | SPEC | NONE | SRC | **BUILD** | Falsifiability screening not implemented | core scientific gate is missing |
| 34 | 5. Verification-Ready POC Design | FIRM | SPEC | NONE | SRC | **BUILD** | POC design contract specified only | — |

### Workflow › POC implementation

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 35 | 1. POC Implementation Environment Preparation | FIRM | ACTIVE | PARTIAL | SRC | **REUSE-JW** | AI4R hands_runtime/worktree.sh; JW jiuwenbox sandbox + worktree rail | — |
| 36 | 2. POC Construction | FIRM | ACTIVE | FULL | SRC | **REUSE-JW** | JW code mode (interface_code, code_agent subagent); AI4R builder panes | — |
| 37 | 3. POC Component Integration & Configuration | FIRM | ACTIVE | PARTIAL | SRC | **ADAPT** | AI4R graph_node_dispatcher integration nodes | — |
| 38 | 4. POC Functional Readiness Validation | FIRM | ACTIVE | PARTIAL | SRC | **PORT** | AI4R run_preflight.py, contract_gate_executor.py | — |
| 39 | 5. Testable POC Artifact Consolidation & Benchmark Handoff | FIRM | IMPL-UNWIRED | NONE | SRC | **PORT** | AI4R artifact_manifest.py, accepted-artifact-export.py(1039) | — |

### Workflow › Benchmarking

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 40 | 1. Benchmark Framing | FIRM | IMPL-UNWIRED | NONE | SRC | **PORT** | AI4R benchmark/solar_solver.py(1144), agent_arena_benchmark.py(1135) | — |
| 41 | 2. Benchmark Protocol & Asset Preparation | FIRM | IMPL-UNWIRED | NONE | SRC | **PORT** | AI4R benchmark harness + heavy_proof_benchmark.py | — |
| 42 | 3. Benchmark Execution | FIRM | IMPL-UNWIRED | NONE | SRC | **PORT** | AI4R benchmark runners; platform_workflow_benchmark.py | — |
| 43 | 4. Metrics & Run Evidence Collection | FIRM | ACTIVE | NONE | EXEC | **PORT** | AI4R gate_ledger route_record (provider/model/exit_code/timings) | — |
| 44 | 5. Comparative Result Analysis & Benchmark Result Packaging | FIRM | IMPL-UNWIRED | NONE | SRC | **PORT** | AI4R capability_fusion_benchmark.py, github_comparison_view.py | — |

### Workflow › Evaluation

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 45 | 1. Evaluation Scope & Evidence Assembly | FIRM | ACTIVE | NONE | EXEC | **PORT** | AI4R evaluator.evaluate_artifacts; 104 evaluator tests pass | — |
| 46 | 2. Evidence Completeness & Provenance Review | FIRM | ACTIVE | NONE | EXEC | **PORT** | AI4R evaluator source-audit + provenance checks (executed) | — |
| 47 | 3. Experimental, Reasoning & External Validity Review | FIRM | SCAFFOLD | NONE | EXEC | **PORT** | AI4R _expert_novelty_metrics, external validity partially heuristic | external validity is weak |
| 48 | 4. Claim & Acceptance-Criteria Comparison | FIRM | ACTIVE | NONE | EXEC | **PORT** | AI4R _apply_profile_gate vs acceptance thresholds | — |
| 49 | 5. Verdict, Blocker & Residual-Risk Classification | FIRM | ACTIVE | NONE | EXEC | **PORT** | AI4R gate_ledger verdict kinds + needs_human_review | — |
| 50 | 6. Refinement & Follow-Up Recording | FIRM | ACTIVE | NONE | SRC | **PORT** | AI4R survey-diagnose / refinement recording | — |

### Workflow › Delivery

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 51 | 1. Delivery Planning & Evidence Handoff | FIRM | IMPL-UNWIRED | PARTIAL | SRC | **ADAPT** | AI4R accepted-artifact-export; JW send_file+channels | — |
| 52 | 2. User-Facing Deliverable Generation | FIRM | ACTIVE | PARTIAL | EXEC | **PORT** | AI4R research compile/synthesize/html_artifact; JW DeepSearch skill (no evidence) | — |
| 53 | 3. Deliverable, Reusable Asset & Knowledge Packaging | FIRM | IMPL-UNWIRED | NONE | SRC | **PORT** | AI4R artifact_manifest + bundle manifest spec | — |
| 54 | 4. Authorized Distribution, Knowledge Transfer & Lifecycle Closure | FIRM | SCAFFOLD | PARTIAL | SRC | **ADAPT** | AI4R acceptance_closeout.py; JW delivery via channels | — |

### Foundation › Capability capsule

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 55 | 1. Capability Capsule Definition & Assembly | FIRM | IMPL-UNWIRED | NONE | EXEC | **PORT** | AI4R capability_capsules.py(1351) + schema v1 (11 required sections); 30 registered, 23 manifests valid | capsule<->JW skill bridge |
| 56 | 2. Capsule Governance, Certification & Registry Management | FIRM | IMPL-UNWIRED | PARTIAL | EXEC | **PORT** | AI4R registry+validate_capability_capsule_semantics executed; capability_certification_suite.py(412) | certification authority |
| 57 | 3. Capability Discovery, Scoring & Selection | FIRM | IMPL-UNWIRED | PARTIAL | EXEC | **PORT** | AI4R classify_task_goal + applicability signals; JW Symphony retrieval (adjacent) | — |
| 58 | 4. Capsule Invocation & Composition | FIRM | IMPL-UNWIRED | PARTIAL | EXEC | **PORT** | AI4R composition consumes/produces/compatible_with; capsule_execution_gate.py(194) | composition engine unproven |
| 59 | 5. Capability Capsule Evolution & Version Promotion | FIRM | IMPL-UNWIRED | NONE | EXEC | **PORT** | AI4R skill_to_capsule_compiler.py(323) + evolution_engine promote/demote | — |

### Foundation › Operators

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 60 | 1. 逻辑算子定义、组装与注册 — Logical Operator Definition, Assembly & Registration | FIRM | IMPL-UNWIRED | NONE | EXEC | **PORT** | AI4R logical_operator_registry.py(33)+config/logical-operators.json (9 types) | registry is thin (33 LOC) |
| 61 | 2. 算子准入、认证与治理 — Operator Qualification, Admission & Governance | FIRM | SCAFFOLD | NONE | EXEC | **PORT** | AI4R physical_operator_catalog static_operator_rejection_reasons | admission policy incomplete |
| 62 | 3. 逻辑—物理算子匹配、选择与绑定 — Logical-to-Physical Matching, Selection & Binding | FIRM | ACTIVE | NONE | EXEC | **PORT** | AI4R graph_scheduler.py:2290-2400 hard capability gate + Layer-3 net | THE key asset |
| 63 | 4. 物理算子与执行舰队管理 — Physical Operator & Execution Fleet Management | FIRM | ACTIVE | PARTIAL | EXEC | **ADAPT** | AI4R config/physical-operators.json (full fleet profiles); JW distributed_runtime | tmux carrier must be dropped |
| 64 | 5. 算子运行评估与能力画像 — Operator Runtime Evaluation & Capability Profiling | FIRM | IMPL-UNWIRED | NONE | EXEC | **PORT** | AI4R operator_score.py(226), operator_flow_control.py(820), capability_registry scorecards | — |
| 65 | 6. 评估器驱动的算子演进 — Evaluator-Driven Operator Evolution | FIRM | SCAFFOLD | NONE | EXEC | **PORT** | AI4R evolution_engine promote/demote executed (1 capability tracked) | barely populated |

### Foundation › Evaluator

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 66 | 1. Contract, Schema & Artifact Conformance Evaluator | FIRM | ACTIVE | PARTIAL | EXEC | **PORT** | AI4R contract_gate_executor + verification_gate; JW A2UI validator (narrow) | — |
| 67 | 2. Engineering Correctness & Code Quality Evaluator | FIRM | ACTIVE | PARTIAL | SRC | **ADAPT** | AI4R eval_runner + CI; JW LSP rail + Auto Harness CI | — |
| 68 | 3. Performance, Cost & Benchmark Evaluator | FIRM | IMPL-UNWIRED | NONE | SRC | **PORT** | AI4R benchmark suite + resource_telemetry.py | — |
| 69 | 4. Security, Privacy, Compliance & IP Evaluator | FIRM | SCAFFOLD | PARTIAL | SRC | **ADAPT** | AI4R gitleaks.toml + data_plane_audit; JW permission engine+jiuwenbox | IP/licence checks absent both |
| 70 | 5. Evidence, Factuality & Scientific Validity Evaluator | FIRM | ACTIVE | NONE | EXEC | **PORT** | AI4R evaluator grounding/authority/diversity; MEASURED precision 0.25 | entailment must be built |
| 71 | 6. Lifecycle, Parity & Human Review Evaluator | FIRM | ACTIVE | PARTIAL | EXEC | **PORT** | AI4R verification_gate writer!=verifier + human_verdict; JW ask-permission | JW has only leader/teammate roles |

### Foundation › Foundational models

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 72 | 1. Model Capability Registry | FIRM | ACTIVE | PARTIAL | EXEC | **ADAPT** | AI4R model_registry.py(167)+config/model-registry.json; JW models config | — |
| 73 | 2. Model Routing & Selection | FIRM | ACTIVE | PARTIAL | EXEC | **ADAPT** | AI4R model-scenario-routing.json + operator_model_selection; JW per-role model | — |
| 74 | 3. Model Usage Auditing | FIRM | ACTIVE | PARTIAL | EXEC | **ADAPT** | AI4R model_call_runtime.py(290) + token-tracker.sh; JW usage_summary events | — |

### Foundation › RSI

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 75 | 1. Text-Based Artifacts (GEPA / MIPROv2 / TextGrad) | FIRM | IMPL-UNWIRED | PARTIAL | EXEC | **REUSE-JW** | openjiuwen optimizer/llm_call + TunableKind='prompt'; AI4R GEPA 3540 LOC (may duplicate) | dedupe GEPA vs openjiuwen optimizer |
| 76 | 2. Runtime and Resource Routing (Bayesian Optimization / Bandits / Cost-Aware RL) | ASPIRE | ABSENT | PARTIAL | EXEC | **REUSE-JW** | openjiuwen TunableKind tool_selector/memory_selector + optimizer/tool_call; agent_rl | bind AI4RnD routing policy as Operator |
| 77 | 3. Capability Capsules and Physical Operators (Trajectory Mining / Code Evolution / CEGIS) | DEBATED | SCAFFOLD | PARTIAL | EXEC | **ADAPT** | openjiuwen optimizer/skill_call + EvolutionStore + skill_package; AI4R skill_to_capsule_compiler | capsule as Operator subject |
| 78 | 4. DAG and Agent Organization (AFlow / MCTS / ADAS) | ASPIRE | ABSENT | NONE | EXEC | **BUILD** | RSI-4 DAG/organisation search absent from BOTH (confirmed against openjiuwen too) | the one genuinely absent surface |
| 79 | 5. Evaluator, Reward, Contract, and Governance (Judge Calibration / Reward Modeling / CEGIS) | DEBATED | SCAFFOLD | PARTIAL | EXEC | **REUSE-JW** | openjiuwen evaluator/metrics{exact_match,llm_as_judge} + agent_rl/reward.py + online/judge | AI4RnD metrics as metrics/ impls |
| 80 | 6. Memory, Retrieval, and Evidence (Memory Learning / Self-RAG / Reranker Training) | DEBATED | SCAFFOLD | PARTIAL | EXEC | **REUSE-JW** | openjiuwen core/operator/memory_call + optimizer/memory_call; JW memory index | — |
| 81 | 7. Model Policies and Weights (SFT / LoRA / DPO / GRPO / Agent RL) | ASPIRE | ABSENT | PARTIAL | EXEC | **REUSE-JW** | openjiuwen agent_rl/rl_trainer{ppo_step,verl_converter,verl_executor}, offline+online | was 'absent'; needs infra to run |
| 82 | 8. Data, Benchmarks, Curriculum, and Observability (Active Learning / Hard-Case Mining / Credit Assignment) | DEBATED | SCAFFOLD | PARTIAL | EXEC | **REUSE-JW** | openjiuwen dataset/{case,case_loader} + trajectory/{builder,extractor,aggregator,store} | AI4R failure_miner feeds hard cases |

### Foundation › Data foundations

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 83 | 1. Persistent Memory & Context Retrieval | FIRM | ACTIVE | FULL | SRC | **REUSE-JW** | JW MemoryIndexManager(1224) SQLite+vector+watcher; AI4R context_store | — |
| 84 | 2. Concept Graph Management | FIRM | SCAFFOLD | NONE | SRC | **PORT** | AI4R runtime/schema/entities.yaml typed entity contract | — |
| 85 | 3. Dataset Graph Management | FIRM | SPEC | NONE | SRC | **BUILD** | Dataset graph specified; no module | — |
| 86 | 4. Code Graph Management | FIRM | SPEC | PARTIAL | SRC | **BUILD** | JW coding memory / code graph adjacent; AI4R none | — |
| 87 | 5. Policy Graph Management | FIRM | SCAFFOLD | PARTIAL | SRC | **ADAPT** | AI4R runtime/policy/writers.yaml + capsule effects; JW permissions | — |
| 88 | 6. Workflow Graph Management | FIRM | IMPL-UNWIRED | NONE | SRC | **PORT** | AI4R workflow_contract registry + config/workflows/ | — |
| 89 | 7. Trace Graph Management | FIRM | ACTIVE | NONE | EXEC | **PORT** | AI4R gate_ledger + events.jsonl + route_proof.py (trace graph in practice) | — |
| 90 | 8. Memory Graph Management | FIRM | SCAFFOLD | NONE | SRC | **PORT** | AI4R runtime/schema/xref.yaml bidirectional link contract | — |
| 91 | 9. TaskGraph Persistence & Lifecycle Management | FIRM | ACTIVE | PARTIAL | EXEC | **ADAPT** | openjiuwen Checkpointer/Storage save-recover + SwarmFlow journal; AI4R task_graph_state_io | persistent KV backend? Q24 |

### Foundation › Harness Core

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 92 | 1. Runtime Control Loop & Run Lifecycle Management | FIRM | ACTIVE | FULL | EXEC | **REUSE-JW** | JW DeepAgent dual-layer task loop (verified 11 rail events); AI4R coordinator.sh | — |
| 93 | 2. Message Bus & Durable Task Queue | FIRM | IMPL-UNWIRED | FULL | EXEC | **REUSE-JW** | openjiuwen SwarmFlow Journal (WAL, call_signature memoisation) + BackgroundTaskController | was 'real gap in JW' - WRONG |
| 94 | 3. DAG Scheduler, TaskGraph Readiness & Operator Binding | FIRM | ACTIVE | PARTIAL | EXEC | **ADAPT** | openjiuwen Pregel get_ready_nodes/supersteps/barrier; binding+write-scope still AI4RnD | 85% of graph_scheduler duplicates |
| 95 | 4. Execution Admission, Lease & Concurrency Control | FIRM | IMPL-UNWIRED | FULL | EXEC | **REUSE-JW** | openjiuwen SemaphoreAdmission + ConcurrencyGovernor + WorkflowAdmission + RunAgentAdmission | actor_* port cancelled |
| 96 | 5. Main Loop Dispatch & Runtime Supervision | FIRM | ACTIVE | FULL | EXEC | **REUSE-JW** | JW agent dispatch in-process; AI4R graph_node_dispatcher(12948) tmux (drop) | — |
| 97 | 6. Failure Recovery & Resumability | FIRM | ACTIVE | FULL | EXEC | **REUSE-JW** | openjiuwen Pregel _is_resume + channel restore; SwarmFlow journal replay; resume_id | — |

### Foundation › Intention compilers

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 98 | 1. Intent Classification & Compilation Variant Selection | FIRM | ACTIVE | NONE | EXEC | **PORT** | AI4R intent_gateway.py(736) classification lanes | — |
| 99 | 2. Goal, Scope and Context normalization | FIRM | ACTIVE | NONE | EXEC | **PORT** | AI4R intent_engine_adapter.py(851) | — |
| 100 | 3. Ambiguity Resolution & Readiness | FIRM | ACTIVE | PARTIAL | SRC | **ADAPT** | AI4R readiness checks; JW structured_ask_user rail | — |
| 101 | 4. Constraint Compilation | FIRM | IMPL-UNWIRED | PARTIAL | SRC | **PORT** | AI4R workflow_contract constraints; JW permissions/budget | — |
| 102 | 5. Task Contract & Acceptance Compilation | FIRM | ACTIVE | NONE | EXEC | **PORT** | AI4R workflow_contract instantiate + version/hash (executed via intake) | — |

### Foundation › Planner

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 103 | 1. Task Contract Decomposition | FIRM | ACTIVE | PARTIAL | EXEC | **PORT** | AI4R epic_decomposer.py(926)+apo_plan_compiler.py(1093); JW TaskPlanningRail | — |
| 104 | 2. TaskGraph Construction | FIRM | ACTIVE | PARTIAL | EXEC | **ADAPT** | openjiuwen Workflow build API + PregelBuilder; AI4RnD keeps semantic plan only | compile, do not schedule |
| 105 | 3. TaskGraph Validation & Feasibility Analysis | FIRM | ACTIVE | PARTIAL | EXEC | **PORT** | AI4R plan_validator 1564 LOC; openjiuwen validates graph structure only | keep contract/coverage validation |

### Foundation › Builder

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 106 | 1. Build Contract Interpretation | FIRM | ACTIVE | PARTIAL | SRC | **ADAPT** | AI4R contract interpretation in dispatch prompts; JW code mode | — |
| 107 | 2. Build Preparation | FIRM | ACTIVE | FULL | SRC | **REUSE-JW** | JW workspace/worktree/deps; AI4R run_preflight | — |
| 108 | 3. Code Construction | FIRM | ACTIVE | FULL | EXEC | **REUSE-JW** | JW code agent + LSP + edit tools | — |
| 109 | 4. Model Construction | DEBATED | ABSENT | NONE | SRC | **BUILD** | Model construction (train/finetune) absent both | needs ML infra |
| 110 | 5. Experimental Asset Construction | FIRM | SCAFFOLD | PARTIAL | SRC | **ADAPT** | AI4R experiment assets in benchmark/; JW generic code tools | — |
| 111 | 6. Benchmark Asset Construction | FIRM | IMPL-UNWIRED | NONE | SRC | **PORT** | AI4R benchmark asset builders | — |
| 112 | 7. Verification Asset Construction | FIRM | ACTIVE | FULL | SRC | **REUSE-JW** | JW test tooling; AI4R solar-verify verify blocks | — |
| 113 | 8. Decision Artifact Construction | FIRM | SPEC | NONE | SRC | **BUILD** | Opportunity cards / decision records not implemented | — |
| 114 | 9. Prototype Assembly | FIRM | SCAFFOLD | PARTIAL | SRC | **ADAPT** | AI4R demo-rsi/prototypes; JW code mode | — |
| 115 | 10. Product Integration | DEBATED | SCAFFOLD | PARTIAL | SRC | **ADAPT** | Product integration; JW code mode + worktree | — |
| 116 | 11. Defect Repair | FIRM | ACTIVE | PARTIAL | SRC | **PORT** | AI4R failure_handler+repair DAG; JW on_tool_exception rails | — |
| 117 | 12. Build Evidence Generation | FIRM | ACTIVE | NONE | EXEC | **PORT** | AI4R artifact_manifest hashes/diffs + gate_ledger evidence | — |
| 118 | 13. Report/Paper/Deliverable Construction | FIRM | ACTIVE | PARTIAL | EXEC | **ADAPT** | AI4R research compile/html_artifact/render_sprint_html; JW skills(docx/pptx) | — |
| 119 | 14. Runtime Deliverable Construction | FIRM | SCAFFOLD | PARTIAL | SRC | **REUSE-JW** | AI4R release/+docker/; JW pip+desktop packaging | — |

### Vertical › Visibility / Statistics

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 120 | 1. Workflow & Platform Status Visibility | FIRM | ACTIVE | PARTIAL | SRC | **ADAPT** | AI4R status-server.py(14400)+React; JW web UI | rewrite as JW view |
| 121 | 2. Execution Trace Search & Inspection | FIRM | ACTIVE | PARTIAL | EXEC | **REUSE-JW** | openjiuwen trajectory store + WorkflowProgressEvent; AI4R events.jsonl | — |
| 122 | 3. Runtime status visibility | FIRM | IMPL-UNWIRED | PARTIAL | SRC | **ADAPT** | AI4R resource_telemetry.py; JW psutil-based status | — |
| 123 | 4. Resource Usage, Cost & Capacity Management | FIRM | SCAFFOLD | PARTIAL | EXEC | **PORT** | AI4R token-tracker.sh+codex budget circuit breaker; JW TokenBudgetEvaluator(per-loop) | cross-run budget missing both |

### Vertical › Installer & CLI & Webapp

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 124 | 1. Windows App | FIRM | SCAFFOLD | FULL | DOC | **REUSE-JW** | JW signed Windows desktop+auto-update; AI4R install.ps1 WSL2 (experimental) | — |
| 125 | 2. MacOS App | FIRM | SCAFFOLD | FULL | DOC | **REUSE-JW** | JW macOS desktop app; AI4R DMG needs release proof | — |
| 126 | 3. MacOS CLI | FIRM | ACTIVE | FULL | EXEC | **REUSE-JW** | JW pip CLI + jiuwenswarm-init/start; AI4R solar CLI | — |
| 127 | 4. Linux Cli | FIRM | ACTIVE | FULL | EXEC | **REUSE-JW** | JW pip on Linux (verified install+2816 tests); AI4R linux CLI supported | — |
| 128 | 5. Web Application & Status Service | FIRM | ACTIVE | FULL | SRC | **REUSE-JW** | JW jiuwenswarm-web + frontend dist; AI4R status-server | — |

### Vertical › UI

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 129 | 1. CLI | FIRM | ACTIVE | FULL | EXEC | **REUSE-JW** | JW cli/main.py + slash commands; AI4R solar-harness.sh | — |
| 130 | 2. GUI | FIRM | ACTIVE | FULL | SRC | **REUSE-JW** | JW web UI + desktop; AI4R React app | — |
| 131 | 3. TUI | FIRM | ACTIVE | FULL | SRC | **REUSE-JW** | JW jiuwenswarm-tui package; AI4R tmux cockpit | — |

### Vertical › Account management

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 132 | 1. Account Registration | FIRM | ABSENT | NONE | EXEC | **BUILD** | No account registration in either system (both single-user local) | multi-tenant is unbuilt |
| 133 | 2. Authentication & Session Security | FIRM | ABSENT | PARTIAL | EXEC | **BUILD** | JW ws_origin check + crypto provider; no user auth/session model | — |
| 134 | 3. User Profile Management | FIRM | ABSENT | PARTIAL | SRC | **BUILD** | JW config/user settings; no profile entity | — |
| 135 | 4. Privacy & Personal Data Controls | FIRM | ABSENT | NONE | SRC | **BUILD** | No privacy/export/delete controls either side | compliance gap |

### Vertical › Message Channels

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 136 | 1. Wechat | FIRM | ABSENT | PARTIAL | SRC | **REUSE-JW** | JW wechat_connect.py(1406) exists; AI4R none. Feature is link-import variant | — |
| 137 | 2. Discord | FIRM | ABSENT | FULL | SRC | **REUSE-JW** | JW discord.py connector shipped; AI4R none | — |
| 138 | 3. TMUX | DEBATED | ACTIVE | NONE | EXEC | **DEFER** | AI4R tmux panes as first-class surface; conflicts with JW in-process model | keep only if UX requirement |

### Vertical › System Configurations

| # | Level-2 feature | Firm | AI4RnD | JW | Ev | Disposition | Evidence | Still to verify |
|---|---|---|---|---|---|---|---|---|
| 139 | 1. LLM Config | FIRM | ACTIVE | FULL | EXEC | **REUSE-JW** | JW models config+/model command; AI4R model-config.sh | — |
| 140 | 2. User Settings | FIRM | ACTIVE | FULL | EXEC | **REUSE-JW** | JW config.yaml+.env+Configuration page; AI4R solar-user-config.json | — |
| 141 | 3. Cost/Budget Settings | FIRM | SCAFFOLD | PARTIAL | EXEC | **PORT** | AI4R codex budget hard_stop; JW per-loop token budget only | cross-run/programme budget missing |
| 142 | 4. Cluster setting | FIRM | ACTIVE | PARTIAL | SRC | **ADAPT** | AI4R config/actor-hosts.json+cluster; JW instance_manager+distributed_runtime | — |
