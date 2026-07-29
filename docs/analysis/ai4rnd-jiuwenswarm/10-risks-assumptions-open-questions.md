# Risks, Assumptions, Conflicting Evidence, and Open Questions

Everything this analysis could not settle, with its effect on the conclusions.

---

## L — Limitations of this analysis

### L1 — Nothing was executed ⚠️ **highest-impact limitation**

Neither system was installed or run. No test suite was executed. The container had neither
system's dependencies, and `openjiuwen` — the package holding `DeepAgent`, the ReAct loop,
the Rail base classes, the task-loop controller, the permission engine implementation, the
harness manifest framework and ~12 built-in elements — is a separate PyPI dependency
**not vendored into the JiuwenSwarm repository**. A direct import check confirmed its
absence from the analysis environment.

**Affects:** every statement about `DeepAgent` behaviour, rail lifecycle semantics, stop
evaluators, the permission engine's runtime behaviour, and the exact `ability_manager` API.
These are marked **documented** rather than **verified** throughout.

**Mitigation:** Stage 0 of the implementation plan exists primarily to close this gap.
Spike E2 is explicitly about reading the real `openjiuwen` API surface.

**If wrong:** if `DeepAgentRail` or `ability_manager` differ materially from what the
in-tree rails suggest, the `ResearchToolkitRail` design needs revision. The *architecture*
(hybrid, service-owned evidence) survives; the *integration mechanism* may not.

### L2 — AI4RnD's repository is very large and was sampled, not read exhaustively

~534k LOC Python across 5,778 files, with `harness/lib/` holding 300+ modules. Reading was
targeted at the components the architecture depends on. Modules not examined may contain
capabilities this analysis reports as missing.

**Specifically unexamined:** most of `lib/` outside research/scheduler/gate/operator paths;
`autopilot/`; `brain/`; `x_api/`; `youtube/`; `influence/`; `vendor/autoresearch/` (4,411
LOC of shell); the `desktop/`, `app/` and `components.d/` trees; the majority of
`harness/tests/`.

### L3 — The `AI4RnD` name was resolved by inference

No repository, package, module or config key uses the string "AI4RnD". The mapping to
`Stellven/AI4Research*` rests on: name similarity, the repositories being the only research
systems in the user's accessible set, and `AI4Research`'s content matching the task's
description ("research workflow, verification model, orchestration, state, specialized
capabilities"). Confidence: high, but not certain. See §A1.

### L4 — Cross-tier repository attachment was unavailable

`add_repo` refused the `Stellven/*` repositories ("cross-tier adds are not supported in v1"
— the session already held `suraj-subrahmanyan` sources). They were read by cloning over
HTTPS instead, which succeeded because they are public. Consequently:

- Only the default branch of each was read. Other branches, open PRs, and issues were not
  examined.
- Git history was shallow-cloned (depth 50), so long-range history was unavailable.

**Affects:** any claim that a capability "does not exist" in AI4RnD — it may exist on an
unmerged branch.

### L5 — JiuwenSwarm's upstream history was not examined

Analysis used the fork `suraj-subrahmanyan/jiuwenswarm` at `a98d7ad`. The canonical
repository is on GitCode (`gitcode.com/openJiuwen/jiuwenswarm`), not GitHub. Upstream
issues, PRs and roadmap discussions were not read. The fork may lag upstream.

**Affects:** the upstream-risk assessment in
[06-integration-challenges.md](06-integration-challenges.md) §7, and any claim about what
upstream is likely to accept.

### L6 — Documentation was used as evidence where source was unavailable

`docs/en/Harness.md`, `AutoHarness.md`, `Symphony.md`, `ToolPermissionsSecurity.md` and
`E2A-protocol.md` describe behaviour in `openjiuwen` or in code not read. These are the
project's own documentation, so they are credible, but they are claims about the system
rather than observations of it. The E2A doc itself warns that on conflict, `models.py` is
authoritative over the prose — implying the docs can drift.

---

## A — Assumptions

| # | Assumption | Basis | If wrong |
|---|---|---|---|
| **A1** | AI4RnD = `Stellven/AI4Research*` | name similarity; content match; no other candidate | The entire AI4RnD analysis is about the wrong system. **This is the single largest binary risk in the document set.** Verify before acting. |
| **A2** | `AI4Research` at `openJiuwen-Solar` is the current implementation | most recently pushed branch; contains the research pipeline | may be a stale or experimental branch |
| **A3** | AI4Research-A's SDD reflects intended architecture | it is the only architecture spec present; the implementation partially matches | the SDD may be aspirational and abandoned |
| **A4** | Rails can register tools via `ability_manager.add_ability` in *any* rail, not only in-tree ones | `MemberSkillToolkitRail` does it; the API is on the agent object, not gated | Stage 1 fails; Option D collapses. **Spike E1 tests this first for exactly this reason.** |
| **A5** | Research artifacts are large enough that keeping them out of session context matters | evidence ledgers with spans and hashes; deep tier = 50+ sources | over-engineering; could simplify by inlining |
| **A6** | The research core has no hidden Solar coupling beyond path resolution | `README.research.md` says "no pip install needed, `PYTHONPATH=lib`"; imports are stdlib + sqlite3 | port cost rises; spike E3 tests it |
| **A7** | JiuwenSwarm's team members can be given distinct capability declarations | swarm assembly is config-driven and per-role | capability routing needs a different worker abstraction |
| **A8** | Two processes are operationally acceptable | JiuwenSwarm already runs gateway + agentserver + web, and spawns jiuwenbox | if not, Option B returns to consideration |
| **A9** | The `_SYMPHONY_METHODS` pattern is the *only* external RPC gate | grep found one dispatch site and one frozenset | there may be other closed paths not found |
| **A10** | `openjiuwen`'s provider registries are process-global mutable dicts | `DESIGN.md` §2.2 states `dict[str, Callable]` with `register_*` functions | out-of-tree harness element registration is impossible; only affects a non-recommended path |

---

## C — Conflicting evidence

### C1 — AI4RnD's README contradicts its architecture documents

The README states plainly: *"Solar is not a finished autonomous cloud service and not a
TypeScript orchestrator product… Some code in `core/` is roadmap scaffolding or
compatibility glue. It is kept in the repository, but the README and CLI surfaces should
not treat it as a fully working autonomous orchestrator."* [E-A01]

The Pipeline A SDD describes a complete operator-based research compiler with an optimizer,
ontology, claim compiler and repair DAGs.

**Resolution used:** the README is treated as authoritative about maturity; the SDD as
authoritative about intent. Where a component appears in the SDD but not in code, it is
labelled **specified, not built** — see
[02-ai4rnd-architecture.md](02-ai4rnd-architecture.md) §8.2. This distinction is honoured
throughout, and it materially changes the port estimates.

### C2 — "Capability-routed DAG" versus a fixed four-role state machine

The GUI design contract insists the orchestration is a capability-routed DAG and *not* a
linear PM → Planner → Builder → Evaluator pipeline [E-A02]. But
`coordinator-state-machine.json` is exactly a linear role sequence with
`requested_role: planner | builder_main | evaluator` [E-A03].

**Resolution:** both are true at different layers. The *sprint* lifecycle is a linear role
handoff; the *task graph within* a sprint is a capability-routed DAG scheduled by
`graph_scheduler`. The design contract describes the DAG layer; the state machine describes
the sprint layer. This was not stated anywhere in AI4RnD's documentation and is an
inference — moderate confidence.

### C3 — Extension SDK described as a plugin system, but half-closed

`BaseExtension` and `ExtensionRegistry` present as a plugin API with metadata, versioning,
`min_jiuwenswarm_version` and dependency declaration. But only two extensions exist, both
in-tree, and the RPC path requires core-tree enum edits to be externally reachable
[E-J07],[E-J08].

**Resolution:** treated as an in-tree modularisation mechanism, not a third-party plugin
API. This is a judgement, and a JiuwenSwarm maintainer might disagree — it is possible the
generic passthrough exists somewhere not found. Worth confirming with upstream before
Stage 4.

### C4 — Three unrelated meanings of "operator" in AI4RnD, plus a fourth in JiuwenSwarm

`logical_operator_registry` (types), `physical_operator_catalog` (workers),
`operator_router` (scheduled scripts in the AI-influence subsystem), and JiuwenSwarm's
harness elements. Documented in
[06-integration-challenges.md](06-integration-challenges.md) §6. Creates a real risk of
porting the wrong module — `operator_router.py` looks central and is not.

### C5 — JiuwenSwarm already ships deep research

`openJiuwen-DeepSearch` is a built-in skill described as "knowledge-enhanced deep retrieval
and deep research, supporting query planning, information gathering, understanding and
reflection, research report generation with multi-agent collaboration", producing Markdown,
Doc and HTML reports in ~15 minutes [E-J16].

This is superficially the same product as AI4RnD. It is architecturally the opposite: a
subprocess-launching skill with no evidence ledger, no claim graph, no citation verification
and no gates — precisely the "single essay-writing prompt" AI4RnD's architecture document
defines itself against.

**But the analysis did not run either.** If `openJiuwen-DeepSearch` produces comparably
useful reports, the commercial case for a 9-month integration weakens considerably, however
strong the architectural case. **This is spike E7 and it is the most important open
question in the document set.**

---

## Q — Open questions

### For the AI4RnD owners

| # | Question | Why it matters |
|---|---|---|
| Q1 | Is AI4RnD really `Stellven/AI4Research`? | assumption A1 — invalidates everything if wrong |
| Q2 | Is the Pipeline A SDD current intent, or superseded? | determines how much of Stage 5 is needed |
| Q3 | Is the operator/optimizer/ontology layer planned, or abandoned? | ~3 of Stage 5's 7 items |
| Q4 | Must the tmux cockpit survive? Is it a UX requirement or an implementation detail? | if it is a requirement, the recommendation changes materially |
| Q5 | Who is the user — the AI4RnD team, or external researchers? | determines whether multi-channel delivery is valuable |
| Q6 | Is `--dangerously-skip-permissions` deliberate, and is it acceptable going forward? | if acceptable, JiuwenSwarm's main security advantage is not valued |
| Q7 | What is the scale target — one user, a team, or a service? | single-user makes the whole integration less compelling |
| Q8 | Has `_jaccard` grounding precision ever been measured? | AI4RnD's central claim rests on it |
| Q9 | Is there an unmerged branch with the operator layer built? | limitation L4 |

### For the JiuwenSwarm maintainers

| # | Question | Why it matters |
|---|---|---|
| Q10 | Is a generic extension-RPC passthrough acceptable upstream? | removes the only core patch in Stage 4 |
| Q11 | When will the config-driven harness loader (`DESIGN.md` §15) land? | would make first-class element registration out-of-tree |
| Q12 | Is `RailManager` a supported extension API or an internal mechanism? | Stage 1 depends on it entirely |
| Q13 | What is `openjiuwen`'s API-stability policy at 0.1.x? | upstream break risk for the Rail plugin |
| Q14 | Would capability-based routing be welcome upstream? | if yes, contribute rather than build in the service |
| Q15 | Is `openJiuwen-DeepSearch` a strategic direction or a demonstration? | determines whether AI4RnD complements or competes |

### Technical, resolvable by spike

| # | Question | Spike |
|---|---|---|
| Q16 | Exact `DeepAgentRail` lifecycle signatures in the installed `openjiuwen` | E2 |
| Q17 | Does a Rail plugin survive agent-cache invalidation and restart? | E1 |
| Q18 | Can a Rail be scoped to specific team members, or is it agent-global? | affects writer ≠ verifier enforcement |
| Q19 | What fraction of `graph_scheduler.py` is Solar-coupled? | E6 |
| Q20 | Does `TokenBudgetEvaluator` compose with an external service's budget? | cross-run cost control |
| Q21 | Can `permissions.rules` deny a tool for one member but not another? | E5, non-re-entrancy |
| Q22 | Does jiuwenbox's network policy allow the research service's outbound fetches? | sandboxed source retrieval |
| Q23 | How does session sharing across channels interact with a single run? | multi-observer runs |

---

## R — Risks to the recommendation

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | A1 is wrong — AI4RnD is a different system | Low | **Fatal** | confirm before Stage 0 |
| R2 | The Rail seam does not work as inferred | Low–Med | High | spike E1 first, week 1 |
| R3 | `openjiuwen` breaks the Rail API in a minor release | Medium | Medium | pin; wrap behind one adapter file |
| R4 | `graph_scheduler.py` is too coupled to port | Medium | Medium | E6 decides port vs rewrite; same exit gate |
| R5 | `openJiuwen-DeepSearch` is good enough that integration is not worth 9 months | **Medium** | **High** | E7 in Stage 0 — treat as a go/no-go |
| R6 | Two processes prove operationally unacceptable | Low | Medium | Stage 2 exit gate tests it |
| R7 | The core patch is rejected upstream and must be carried | Medium | Low–Med | prefer the generic form; Stages 1–3 need no patch |
| R8 | Entailment precision is poor, so "verified" is overclaimed | **Medium–High** | **High** | E8 in Stage 0; promote entailment work to Stage 1 if needed |
| R9 | Research skills do not migrate cleanly (slash-command assumptions) | High | Low | expect rewrite, not port; scoped to 3–5 skills in Stage 1 |
| R10 | Unsandboxed Rail plugin becomes a security incident | Low | High | first-party plugin only; do not market a third-party plugin story |
| R11 | Both upstreams are pre-1.0 and churn faster than integration lands | Medium | Medium | minimal in-tree footprint is the entire defence |
| R12 | Prompt injection via fetched research sources | **High** | Medium–High | run source-fetching operators inside jiuwenbox with network policy; never let fetched content reach a tool-calling context unfiltered |

**R5 and R8 are the two that should be resolved before any engineering commitment.** R5 asks
whether the integration is worth doing; R8 asks whether the thing being integrated does what
it claims. Both are cheap to test and both can invalidate the plan.

---

## Statement of confidence

| Conclusion | Confidence | Basis |
|---|---|---|
| JiuwenSwarm has no evidence/claim/citation model | **High** | repository-wide search; no such identifier exists |
| AI4RnD's research core is the valuable asset | **High** | read directly in source |
| The Rail plugin seam can register tools | **Medium-High** | pattern read in in-tree source; not executed |
| Extension RPC is closed externally | **High** | read the frozenset, the enum, and the single dispatch site |
| `config_specs.py` gates element inclusion | **High** | read in source and confirmed by `DESIGN.md` §15 |
| tmux dispatch should not be ported | **High** | `DISPATCH-PROTOCOL.md`'s own post-mortems |
| Hybrid is the right architecture | **Medium-High** | follows from the above; sensitive to R5 |
| Effort estimates | **Low-Medium** | derived from module sizes and coupling, not measured velocity |
| AI4RnD = AI4Research | **Medium-High** | inference; see A1 |
