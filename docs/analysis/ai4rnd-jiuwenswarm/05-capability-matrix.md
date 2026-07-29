# Capability and Compatibility Matrix

Every AI4RnD requirement classified against what JiuwenSwarm provides.

> **Revision 2 note.** This matrix was built against AI4RnD *as it exists*. The controlling
> matrix is now [`traceability/142-feature-matrix.md`](traceability/142-feature-matrix.md),
> which covers all 142 intended Level-2 features. This document is retained because its
> per-capability reasoning remains valid, with four corrections from execution:
>
> | Row | Was | Now |
> |---|---|---|
> | 4.2 tool registration out-of-tree | `X` extensible, inferred | `X` **verified by execution** [V-2] |
> | 8.2 built-in high-risk denials | `P` provided | **`~P`** — loads 0 rules in a stock install [V-4] |
> | 6.14 writer ≠ verifier | `M` port to JiuwenSwarm | **`M`** — must live in AI4RnD's router; JiuwenSwarm has 2 roles + global policy [V-6] |
> | 6.11 entailment "partial in AI4RnD" | partial | **absent** — measured precision 0.25, no NLI anywhere [V-12] |

## Legend

| Symbol | Meaning |
|---|---|
| **P** | **Provided** — JiuwenSwarm already does this at production quality |
| **~P** | **Partial** — exists but with material gaps for AI4RnD's purposes |
| **X** | **Extensible** — addable through existing out-of-tree extension points (Rail plugin, extension package, skill, MCP, config) |
| **I** | **Internals** — requires changes to JiuwenSwarm core-tree files |
| **U** | **Upstream** — requires changes to the `openjiuwen` package (outside JiuwenSwarm's control) |
| **S** | **Service** — best supplied by an external service AI4RnD already has |
| **M** | **Missing from both** — neither system provides it; must be built |

---

## 1. Execution substrate

| # | Requirement | JiuwenSwarm | Class | Notes |
|---|---|---|---|---|
| 1.1 | Run an agent loop with tool calling | `DeepAgent` ReAct + dual-layer task loop | **P** | mature |
| 1.2 | Long-running multi-round tasks | outer task loop, stop evaluators | **P** | |
| 1.3 | Runtime steering / follow-up / abort | `steer` / `follow_up` / `abort` | **P** | documented; in `openjiuwen` |
| 1.4 | Delegate to sub-agents with isolated context | `explore` / `plan` / `browser` / `code` sub-agents | **P** | |
| 1.5 | Multi-agent team with specialised roles | swarm mode leader/teammate | **P** | roles, not capabilities |
| 1.6 | Distributed workers across machines | `remote_member_bootstrap.py`, build-context seed | **P** | |
| 1.7 | Parallel execution of independent work | teammates; performance mode | **~P** | no dependency graph, no batching |
| 1.8 | Bounded delegation to an external expensive runtime | MCP, ACP, `agent_client` extension | **~P** | no token budget / circuit breaker like the Codex bridge |
| 1.9 | Per-worker concurrency limits | `max_concurrency` not modelled | **M** | AI4RnD has it declaratively |

## 2. Planning and orchestration

| # | Requirement | JiuwenSwarm | Class | Notes |
|---|---|---|---|---|
| 2.1 | Decompose a goal into steps | `TaskPlanningRail`, plan mode | **P** | in-session, not artifact |
| 2.2 | Explicit DAG with typed dependencies | — | **M** | port `graph_scheduler` |
| 2.3 | DAG validation (cycles, missing deps, duplicates) | — | **M** | |
| 2.4 | Topological layering, critical path, parallelism metrics | — | **M** | |
| 2.5 | Write-scope conflict avoidance in batching | — | **M** | correctness property for parallel agents |
| 2.6 | Declarative state machine with guards and timeouts | — | **M** | AI4RnD's frozen transition table |
| 2.7 | Plan validated before dispatch ("compiles ⇒ dispatchable") | — | **M** | |
| 2.8 | Human approval gate between phases | permission `ask`; `structured_ask_user` rail | **~P** | tool-call granularity, not phase granularity |
| 2.9 | Skill-chain orchestration by I/O compatibility | Symphony score + orchestration | **P** | JiuwenSwarm is *ahead* here |

## 3. Worker selection and routing

| # | Requirement | JiuwenSwarm | Class | Notes |
|---|---|---|---|---|
| 3.1 | Declare a worker's capabilities | — | **M** | |
| 3.2 | Declare a task's required capabilities | — | **M** | |
| 3.3 | Hard capability gate (never relaxed) | — | **M** | AI4RnD's central mechanism |
| 3.4 | Skills as soft preference with liveness net | — | **M** | |
| 3.5 | Discriminated stall reasons | — | **M** | `no_matching_worker` vs capacity vs runtime |
| 3.6 | Honest stall (never force-assign) | — | **M** | |
| 3.7 | Model preference with fallback | model config per role (`models show`) | **~P** | no per-node preferred model with fallback flag |
| 3.8 | Quota / rate-limit awareness in routing | — | **M** | AI4RnD tracks `flow_control` per operator |
| 3.9 | Cost / latency / context tiers in selection | — | **M** | |

## 4. Tools, skills, capabilities

| # | Requirement | JiuwenSwarm | Class | Notes |
|---|---|---|---|---|
| 4.1 | Register tools on an agent | ability manager | **P** | |
| 4.2 | Register tools from an out-of-tree plugin | Rail plugin + `add_ability` | **X** | **the key seam** [E-J09],[E-J10] |
| 4.3 | Skills as `SKILL.md` capability packages | skill system, 5 registries | **P** | format-compatible with AI4RnD |
| 4.4 | Hot install / uninstall skills | web UI + `SkillManager` | **P** | |
| 4.5 | Skill retrieval at scale | Symphony tree index | **P** | JiuwenSwarm ahead |
| 4.6 | Skill self-improvement from usage signals | evolution rails, `evolutions.json` | **P** | JiuwenSwarm ahead |
| 4.7 | MCP tool servers | `mcp_config.py` | **P** | |
| 4.8 | Register a new harness element type out-of-tree | `@harness_element` + global registries | **I** | registration works; inclusion needs `config_specs.py` change [E-J05] |
| 4.9 | Config-driven harness assembly from a file | — | **U** | `DESIGN.md` §15 lists as future work |
| 4.10 | Versioned capability manifests | Symphony score is versioned; capsules are not modelled | **~P** | |

## 5. State and artifacts

| # | Requirement | JiuwenSwarm | Class | Notes |
|---|---|---|---|---|
| 5.1 | Conversation persistence | session store | **P** | |
| 5.2 | Session rewind / undo | 3 rewind variants + context rewind | **P** | JiuwenSwarm ahead |
| 5.3 | Context compaction | `/compact`, context engine | **P** | JiuwenSwarm ahead |
| 5.4 | Long-term memory with hybrid retrieval | SQLite + vector, file-watched | **P** | JiuwenSwarm ahead |
| 5.5 | Typed intermediate artifacts per run | — | **S** | research service owns this |
| 5.6 | Run directory with schema-validated sub-trees | — | **S** | |
| 5.7 | Append-only event stream | logs + OTel | **~P** | not a queryable domain event log |
| 5.8 | Content-addressed artifacts (SHA-256) | — | **S** | |
| 5.9 | Deterministic ids | — | **S** | |
| 5.10 | Typed knowledge graph with enforced back-links | memory index (untyped) | **~P** | AI4RnD's `xref.yaml` contract |
| 5.11 | Artifact ownership contracts (user-owned / tools-only / append-only) | file whitelists, `/add-dir` | **~P** | different granularity |

## 6. Verification and evaluation — the decisive section

| # | Requirement | JiuwenSwarm | Class | Notes |
|---|---|---|---|---|
| 6.1 | Evidence ledger (source → document → span → evidence) | — | **M/S** | **port from AI4RnD** |
| 6.2 | Claim graph with typed relations | — | **M/S** | |
| 6.3 | Citation spans verified at char + byte offsets | — | **M/S** | |
| 6.4 | Citation grounding metrics | — | **M/S** | |
| 6.5 | Source authority scoring | — | **M/S** | |
| 6.6 | Source diversity gate | — | **M/S** | |
| 6.7 | Source-type plausibility validation | — | **M/S** | |
| 6.8 | Freshness gate | — | **M/S** | specified in SDD |
| 6.9 | Question-coverage gate | — | **M/S** | |
| 6.10 | Contradiction search / coverage | — | **M** | **specified but not implemented in AI4RnD either** |
| 6.11 | Entailment checking claim ← evidence | — | **M** | **partial in AI4RnD** (token-overlap heuristics, `_jaccard`) |
| 6.12 | Pluggable gate registry | — | **M/S** | AI4RnD's `@register_gate` |
| 6.13 | Per-profile gate thresholds | — | **M/S** | `profiles/*.yaml` |
| 6.14 | Writer ≠ verifier enforcement | — | **M** | port; needs swarm-level expression |
| 6.15 | Guard against self-graded passes | — | **M** | |
| 6.16 | Append-only gate ledger, status as projection | — | **M** | port |
| 6.17 | Writer attribution on state transitions | — | **M** | |
| 6.18 | Bounded repair loop on gate failure | `on_*_exception` rails repair context only | **~P** | different layer |
| 6.19 | Repair-exhausted → human review | — | **M** | |
| 6.20 | Evaluation-driven harness optimisation | Auto Harness | **P** | JiuwenSwarm ahead — but optimises capability, not correctness |
| 6.21 | Benchmark generation for self-evaluation | Auto Harness "agents generate their own benchmarks" | **P** | documented |

## 7. Research-specific

| # | Requirement | JiuwenSwarm | Class | Notes |
|---|---|---|---|---|
| 7.1 | Research contract from an ambiguous topic | — | **S** | |
| 7.2 | Domain / research-type classification | — | **S** | |
| 7.3 | Question graph | — | **S** | |
| 7.4 | Source connector abstraction | `core.web_search`, `web_fetch`, `web_paid_search`, MCP | **~P** | tools exist; no `SourceConnector` contract with retrieval metadata |
| 7.5 | Source deduplication and ranking | — | **S** | |
| 7.6 | Document ingestion / normalisation | vision, audio, OCR, `financial-document-parser` skill | **~P** | no span model |
| 7.7 | Span extraction with offsets | — | **S** | |
| 7.8 | Report AST / blueprint / section contracts | — | **S** | |
| 7.9 | Citation rendering from stored spans | — | **S** | |
| 7.10 | Bibliography management | — | **S** | |
| 7.11 | Depth tiers (quick / standard / deep) | — | **S** | |
| 7.12 | Human-in-the-loop source import | — | **S** | `handoff-search` / `import-search` |
| 7.13 | Deep research end-to-end | `openJiuwen-DeepSearch` skill | **~P** | a *black-box* skill: runs a subprocess, produces a report, no evidence ledger, no gates [E-J16] |
| 7.14 | Lightweight research ontology | — | **M** | specified in SDD; not implemented in AI4RnD |
| 7.15 | Living / incrementally updated reports | — | **S** | `LivingReport` schema exists |

**Row 7.13 deserves emphasis.** JiuwenSwarm *does* ship deep research — as a skill that
shells out to a script and returns a Markdown/Doc/HTML report after ~15 minutes. It has no
evidence ledger, no claim graph, no citation verification and no gates. It is exactly the
"single essay-writing prompt" that AI4RnD's architecture document defines itself against.
The two are not competitors at the same layer; AI4RnD would *replace* it.

## 8. Security and operations

| # | Requirement | JiuwenSwarm | Class | Notes |
|---|---|---|---|---|
| 8.1 | Per-tool-call permission decisions | tiered policy engine | **P** | JiuwenSwarm far ahead |
| 8.2 | Built-in high-risk command denial (non-overridable) | `builtin_rules.yaml` | **P** | |
| 8.3 | User approval prompts | `ask` action, web/CLI prompt | **P** | |
| 8.4 | Filesystem / OS isolation | jiuwenbox (bwrap, cgroup) | **P** | AI4RnD has none |
| 8.5 | Network policy for sandboxed execution | jiuwenbox `network.py` | **P** | |
| 8.6 | Workspace-external path control | `ExternalDirectoryChecker`, `/add-dir` | **P** | |
| 8.7 | Token / cost budget with circuit breaker | `TokenBudgetEvaluator` (per-loop) | **~P** | no daily cross-run budget like AI4RnD's Codex bridge |
| 8.8 | Plugin code isolation | **none** — `rail.py` runs with full privileges after a syntax check | **M** | risk for both |
| 8.9 | Audit trail of state mutations | logs, OTel | **~P** | no writer-attributed ledger |
| 8.10 | Secret handling | crypto provider abstraction, `.env` | **P** | AI4RnD uses `key_ref` indirection + gitleaks |
| 8.11 | Provenance of a result (who/what/when produced it) | — | **M** | AI4RnD's route records |

## 9. Interfaces and delivery

| # | Requirement | JiuwenSwarm | Class | Notes |
|---|---|---|---|---|
| 9.1 | Multi-channel chat delivery | 9 IM + web + TUI + desktop | **P** | JiuwenSwarm far ahead |
| 9.2 | Scheduled/recurring runs | cron scheduler | **P** | |
| 9.3 | File delivery to the user | `swarm.send_file` | **P** | |
| 9.4 | Agent-to-agent protocols | ACP, A2A | **P** | |
| 9.5 | Web dashboard for run state | web UI | **~P** | no DAG/gate view |
| 9.6 | Honest-state UI rules | — | **M** | AI4RnD's design contract |
| 9.7 | Programmatic API for external orchestration | WS RPC (closed enum), extension RPC (in-process only) | **I** | see [06-integration-challenges.md](06-integration-challenges.md) §2 |

---

## Roll-up

| Class | Count | Interpretation |
|---|---|---|
| **P** Provided | 30 | JiuwenSwarm's execution, channel, skill, memory and security layers are ready to use as-is |
| **~P** Partial | 14 | usable with adaptation; mostly granularity mismatches |
| **X** Extensible out-of-tree | 1 | tool registration via Rail plugin — small in count, decisive in effect |
| **I** Internals required | 3 | RPC exposure, harness element inclusion, external API |
| **U** Upstream required | 1 | config-driven harness loader (`openjiuwen`) |
| **S** Service-supplied | 17 | the research core — keep in AI4RnD's codebase |
| **M** Missing from both | 23 | of which ~15 are "missing from JiuwenSwarm, present in AI4RnD" and ~8 are genuinely absent from both |

### Genuinely missing from both systems

These need building regardless of which architecture is chosen:

1. **Contradiction search and contradiction-coverage gating** — specified in AI4RnD's SDD,
   not implemented.
2. **Real entailment checking.** AI4RnD's grounding uses token-overlap heuristics
   (`_jaccard`, `_tokens`). A claim can pass by lexical overlap without being entailed.
   This is the weakest link in the evidence chain and the most valuable thing to fix.
3. **The research ontology** — entity/claim type vocabulary with synonym and alias
   resolution. Specified, not built.
4. **The optimizer** — compiling a logical research plan into a physical operator plan.
   Specified in detail; the implementation is CLI-subcommand-shaped instead.
5. **Plugin code isolation.** Both systems execute third-party plugin code with full
   privileges after only a syntax check.
6. **Cross-run cost budgeting.** JiuwenSwarm budgets a loop; AI4RnD budgets Codex calls
   only. Neither budgets a research programme.
7. **Result provenance as a first-class query.** AI4RnD records route metadata in the gate
   ledger but exposes no "why does this sentence exist" query path.
8. **Multi-tenant isolation of research state.** Both are single-user in practice
   (`tenant_agent_pool.py` exists in JiuwenSwarm but the research artifact model has no
   tenancy concept at all).

Items 2 and 5 are the two that should worry a reviewer most: the first because it
undermines the correctness guarantee AI4RnD is built to provide, the second because it
undermines the security guarantee JiuwenSwarm is built to provide.
