# Correction Log — Revision 3

What earlier revisions assumed too early, and what the evidence now says. Prior documents are
preserved unchanged except for pointers; nothing has been destructively replaced.

---

## 0. A note on scope

The brief describes a prior revision that treated **AI4RnD as a mode** and exposed
**Auto Route / SwarmFlow / Dynamic Team / Core Workflow** as user-selectable execution
strategies, with a UI prototype and HTML artifacts.

**That work is not on this branch.** `git log` shows two commits — Revision 1 (`7b4d292`) and
Revision 2 (`dc5de41`) — and neither mentions modes, Auto Route, or a strategy selector, and
no `.html` file exists under `docs/analysis/`. That prototype was produced somewhere this
session cannot see.

The critique nonetheless lands, because most of it applies to **Revision 2** as written. This
log addresses Revision 2's actual errors. Where a criticism describes something Revision 2 did
not do, that is recorded too, so the record stays honest.

---

## 1. The central error: I recommended porting a scheduler without checking the host

**Revision 2 said** ([09 Stage 3](09-implementation-plan.md)):

> **DAG scheduler** (~2 wks if port, ~6 if rewrite) — validation, topo layering, critical path,
> **write-scope conflict avoidance**, pass-mark guards. 321 tests to carry over.

and ([14](14-reuse-vs-build-map.md)):

> **Durable queue + leases** (~1 wk) — `actor_registry`/`actor_lease`/`actor_mailbox`/
> `actor_runtime` (1,051 LOC). *This closes Harness Core features 2 and 4, which JiuwenSwarm
> does not provide.*

**What I never did:** open `openjiuwen/core/workflow/`, `openjiuwen/core/graph/`, or
`openjiuwen/agent_teams/workflow/`. I inspected `openjiuwen/harness/rails/` and
`harness/security/` and stopped.

**What is actually there** (all executed — [V-15](12-verification-appendix.md#v-15), [V-16](12-verification-appendix.md#v-16)):

| Requirement I said JiuwenSwarm lacked | What openjiuwen 0.1.15.post3 already has |
|---|---|
| DAG with typed dependencies | `Workflow` + `PregelGraph`: `add_node`, `add_edge`, `add_conditional_edges` |
| Barrier / wait-for-all | `add_node(..., wait_for_all=True)`, `BarrierMessage` |
| Dynamic fan-out | `add_conditional_connection(router)` where the router returns `Hashable` **or `list[Hashable]`** |
| Durable state, resume without re-running | Pregel channel `snapshot()`/`restore()`; `PregelLoop._is_resume`; `_save_state_on_error` persists `channel_snapshot`; `Checkpointer` + `Storage.save/recover` |
| Interrupt / human-in-the-loop pause | `GraphInterrupt`, `Interrupt`, `WorkflowController.interrupt_task` / `_handle_resume` |
| Idempotent replay | SwarmFlow `Journal` — WAL-backed, `call_signature()` memoisation, `get_cached(ks, sig)`, `hits()` |
| Admission / concurrency control | `SemaphoreAdmission`, `ConcurrencyGovernor`, `ConcurrencyLimits`, `WorkflowAdmission` |
| Background execution + pause/resume | `SwarmflowTool.run_background`, `BackgroundTaskController.pause/resume/is_paused` |
| Nested / recursive graphs | `workflow_comp` — a workflow is a component of another workflow |
| Progress events | `WorkflowProgressEvent`, `PhasePlan`, `ProgressKind` |
| Cancellation | `_check_abort(rt)` in SwarmFlow primitives; `NativeHarness.abort(immediate=)` |

**Verdict:** Revision 2's Stage 3 — the single largest piece of work in the plan, ~12 weeks —
was substantially aimed at rebuilding machinery that already exists one layer down. See
[17-taskgraph-verdict.md](17-taskgraph-verdict.md).

**Severity: high.** This changes the recommended architecture, not just the estimate.

---

## 2. I declared six of eight RSI surfaces "absent from both systems" — having searched only one

**Revision 2 said** ([13](13-maturity-map.md), [05](05-capability-matrix.md) §Missing):

> RSI-2 routing, RSI-4 DAG/organisation, RSI-5 evaluator/reward, RSI-6 memory/retrieval,
> RSI-7 model weights, RSI-8 data/curriculum — *"absent from both"*.

**How I got there:** a word-boundary grep for `GEPA|MIPROv2|TextGrad|Voyager|AFlow|MCTS|CEGIS|
GRPO` across **`Stellven/AI4Research` only**. I never ran it against openjiuwen. Searching for
*algorithm brand names* rather than *capabilities* compounded the error.

**What is actually there** — `openjiuwen/agent_evolving/`, executed
([V-17](12-verification-appendix.md#v-17)):

| RSI surface | openjiuwen provision | Status |
|---|---|---|
| 1 Prompts / rules | `core/operator/llm_call` + `TunableKind="prompt"`; `optimizer/llm_call` | **present** |
| 2 Runtime & resource routing | `TunableKind` includes `tool_selector`, `memory_selector`; `optimizer/tool_call` | **partial** |
| 3 Capsules & operators | `optimizer/skill_call`; `EvolutionStore`; `skill_package` pack/install | **partial** |
| 4 DAG & agent organisation | — no workflow-structure search | **absent** (correct) |
| 5 Evaluator, reward, governance | `evaluator/metrics/{exact_match,llm_as_judge}`; `agent_rl/reward.py`; `online/judge` | **partial** |
| 6 Memory, retrieval, evidence | `core/operator/memory_call`; `optimizer/memory_call` | **partial** |
| 7 Model policies & weights | `agent_rl/rl_trainer/{ppo_step,verl_converter,verl_executor}`, offline + online | **present** |
| 8 Data, benchmarks, curriculum | `dataset/{case,case_loader}`; `trajectory/{builder,extractor,aggregator,store}` | **partial** |

Plus the governance spine I claimed had to be built:
`Trainer.train` → `Updater.process/update` (single-dim **and** multi-dim credit assignment) →
`_select_best_candidate_on_val(candidates)` → `_snapshot_operators_state` /
`_restore_operators_state` → `_save_checkpoint_if_needed` / `_resume_if_needed`. Operators
carry **freeze markers** so `set_parameter` can refuse to touch protected parameters.

**Verdict:** one of eight absent, not six. Revision 2's Stage 6 ("build the four remaining
surfaces", 16 weeks) is largely a *binding* exercise, not a construction one.

**Severity: high.**

---

## 3. Naming collision I missed entirely: two incompatible meanings of "Operator"

`openjiuwen/core/operator/base.py`, verbatim:

> *"Operator is **NOT an executable unit**. Execution is handled by the consumer (Agent) using
> the parameters managed by Operator."*

An openjiuwen `Operator` is a **tunable-parameter handle** for self-evolution
(`get_tunables`, `set_parameter`, `get_state`, `load_state`, `operator_id` for trajectory
attribution). Kinds: `llm_call`, `memory_call`, `skill_call`, `tool_call`.

An AI4RnD **logical/physical operator** is precisely an executable unit — a DAG-callable work
unit and the worker that runs it.

Revision 2 flagged three colliding meanings of "operator" *inside AI4RnD*
([06 §6](06-integration-challenges.md)) and completely missed that openjiuwen adds a fourth
with the opposite meaning. Any integration that says "operator" without qualification will
cause repeated, expensive confusion.

**Resolution adopted in Revision 3:** AI4RnD's executable units are renamed **Steps**
(logical) and **Runners** (physical) in all integration-facing material; "Operator" is
reserved for openjiuwen's evolution-parameter handle.

**Severity: medium** — no wrong conclusion followed from it, but it would have produced one
during implementation.

---

## 4. I did not separate the layers, so "port the scheduler" hid three different decisions

Revision 2 discussed "AI4RnD owns TaskGraph, scheduling, routing, admission, leases" as a
single ownership block. Those are four separable questions with four different answers:

| Layer | Revision 2 | Revision 3 |
|---|---|---|
| Logical research plan (what must be true, what depends on what) | conflated with scheduling | **AI4RnD owns** — semantic model, no runtime |
| Runtime graph (what executes when) | AI4RnD owns; port `graph_scheduler` | **openjiuwen owns** — compile to Core Workflow / SwarmFlow |
| Worker selection (who runs it) | AI4RnD owns | **AI4RnD owns** — capability routing has no Jiuwen equivalent |
| Admission / concurrency / leases | AI4RnD owns; port `actor_*` | **openjiuwen owns** — `ConcurrencyGovernor`, `SemaphoreAdmission` |

The full ten-layer model is in
[19-product-layers-and-ux.md](19-product-layers-and-ux.md).

**Severity: high** — this is the structural error that made error #1 possible.

---

## 5. Criticisms that do not apply to Revision 2 (recorded for completeness)

| Criticism | Status on this branch |
|---|---|
| "Converged on AI4RnD as a mode" | Revision 2 recommended a **separate service** reached by a Rail plugin. It never proposed a mode. The mode question was simply **never asked** — which is its own gap, now addressed in [19](19-product-layers-and-ux.md) §1. |
| "Exposed Auto Route / SwarmFlow / Dynamic Team / Core Workflow as user choices" | Revision 2 never mentioned Auto Route, SwarmFlow or Dynamic Team at all — because I had not found them. The answer is now established: **none should be user-selectable**; SwarmFlow is already a config flag (`modes.team.jiuwen_team.enable_swarmflow`) whose phases are projected into the existing team UI as `team.member` / `team.task`. See [19](19-product-layers-and-ux.md) §2. |
| "UI prototype presented one hypothesis as decided" | No UI prototype exists on this branch. |

---

## 6. Conclusions from Revision 2 that survive

Re-checked against the new evidence; these stand:

| Conclusion | Still valid because |
|---|---|
| Capability Capsules are a distinct governed abstraction, not renamed skills | 11-section schema; 30 registered, 23 validated [V-11]. Reinforced: openjiuwen has no capsule equivalent — `skill_package` is a tarball, not a contract. |
| Citation grounding does not verify grounding (precision 0.25) | measured [V-12]; unchanged. openjiuwen's `llm_as_judge` metric is a *possible* remedy, which strengthens the recommendation to replace rather than port. |
| openjiuwen ships no `builtin_rules.yaml`, so guardrails load zero rules | measured [V-4]; unchanged. |
| JiuwenSwarm has two member roles with a global permission policy | [V-6]; unchanged, and now more consequential — see [19](19-product-layers-and-ux.md) §6. |
| An out-of-tree Rail can register and invoke abilities | executed [V-2]; unchanged. |
| JiuwenSwarm's test suite passes 2,816/2,816 | [V-7]; unchanged. |
| 19 AI4RnD modules are implemented-but-unwired | [V-8]; unchanged — but **fewer of them are worth wiring**, since `actor_*` and much of `graph_scheduler` now duplicate openjiuwen. |
| DeepSearch is not a competitor to the intended product | [V-14]; unchanged. |
| JiuwenSwarm covers 20/142 features fully | **revised to 23/142 FULL**, with NONE falling 72→62 — the mechanism inventory re-scored 16 features. See [traceability](traceability/142-feature-matrix.md). |

---

## 7. What changed in the recommendation

| | Revision 2 | Revision 3 |
|---|---|---|
| Shape | separate durable service + thin Rail + execution callback | **layered**: mode as entry point → persistent project subsystem → compiles to Jiuwen workflows |
| Runtime graph | AI4RnD's own scheduler (ported) | **Core Workflow / SwarmFlow**; AI4RnD keeps a *semantic* plan only |
| Durable queue, leases, admission | port `actor_*` from AI4RnD | **reuse** `ConcurrencyGovernor` + `Journal` + `Checkpointer` |
| RSI | build 6 of 8 surfaces | **bind** AI4RnD governance onto `agent_evolving`; build 1 |
| Custom code retained | ~25k LOC ported | **~9k LOC** — capsules, capability routing, evidence/claims, gates, governance |
| Time to complete product | ~19–20 months | **~12–14 months** |
| Core-tree changes | ~10–20 lines at Stage 4 | similar, but later and smaller |

The direction of travel is consistent — AI4RnD owns meaning and verification, Jiuwen owns
execution — but Revision 2 drew the line in the wrong place, giving AI4RnD a scheduler it does
not need to own.

---

## 8. Why the error happened, and the process fix

I inspected openjiuwen only where Revision 2's questions pointed — rails and permissions —
and treated "not in JiuwenSwarm's repository" as "not in the platform". openjiuwen is 4× the
size of the JiuwenSwarm package by surface area and holds the execution primitives.

**Process fix applied in Revision 3:** before declaring any capability missing, enumerate the
dependency's package tree and search by *capability* (checkpoint, resume, barrier, admission,
journal, reward, candidate) rather than by *brand name*. That is what produced
[16-jiuwen-execution-mechanisms.md](16-jiuwen-execution-mechanisms.md), and it is the document
Revision 2 should have opened with.
