# Architecture Options — Revision 3

**This document replaces the Revision 2 version**, which is preserved in git history at
`dc5de41`. Revision 2 evaluated options without knowing that openjiuwen contains a Pregel graph
engine, a workflow engine, SwarmFlow, admission control and a self-evolution framework. With
those on the table, three of its options collapse and two new ones appear.

Nothing is preserved by default. The previous recommendation is re-derived from evidence below,
and it changes.

---

## What the hypotheses actually are

The brief lists eight framings. Reduced against the evidence, they are not eight alternatives —
they are **choices at three independent layers**:

| Layer | Real options |
|---|---|
| **Entry** | mode · project surface · separate app · library only |
| **Control plane** | in-process subsystem · separate service · none (agent-driven) |
| **Execution** | compile to Jiuwen mechanisms · own scheduler · external workers |

Several listed "options" are points on one layer only. *"A library of registered workflows"* is
an execution choice with no control plane. *"A specialised agent/team configuration"* is an
execution choice with no project state. Treating them as whole architectures is what produced
the earlier confusion.

Options below are named by their **(entry, control plane, execution)** triple.

---

## Option 1 — Mode only *(mode, none, agent-driven)*

AI4RnD is a JiuwenSwarm mode. A research-profiled agent with research tools; no persistent
project.

| | |
|---|---|
| UX | pick "Research", chat, get a report |
| Control flow | DeepAgent task loop; tools call research helpers |
| State | session only |
| Execution | DeepAgent + tools |
| Failure / cancel | session-level; a lost session loses the run |
| Evolution | ordinary skill evolution only |
| Code boundary | out-of-tree rail + skills |
| Duplication | none |
| Upstream changes | none |
| Buildable now | **yes — weeks** |
| **Falsified by** | any run longer than a session; any evidence that must survive `/compact`; any capability shared across projects |

**Verdict: insufficient, but the right entry point.** It cannot hold a multi-day project, an
evidence ledger, or a capability registry. It becomes layer 1 of the recommendation.

---

## Option 2 — Registered workflow library *(mode, none, Core Workflow)*

AI4RnD ships research workflows registered with openjiuwen; `WorkflowController` selects them
by intent.

| | |
|---|---|
| UX | ask a question; Auto Route picks a workflow |
| Control flow | `intent_detection` → `exec_task` → interrupt/resume |
| State | workflow checkpoint + session |
| Execution | Core Workflow, reusing everything |
| Failure / cancel | `interrupt_task` / `_handle_resume` — mature |
| Evolution | prompts inside workflow components via `Operator` |
| Duplication | **none** — maximum reuse |
| Buildable now | **yes** |
| **Falsified by** | needing evidence ledgers, capability routing, gates with authorship, or cross-project capability versioning — none of which a `WorkflowCard` can carry |

**Verdict: excellent execution substrate, not an architecture.** Confirms Core Workflow is a
compilation target [17]. Cannot express research contracts or governed capabilities.

---

## Option 3 — Harness profile *(mode, none, harness elements)*

AI4RnD as a new Harness profile: research rails, tools, sub-agents assembled by `config_specs`.

| | |
|---|---|
| Duplication | none |
| Upstream changes | **`config_specs.py` edits for every element** — merge conflict on each rebase [E-J05] |
| **Falsified by** | needing per-step capability selection and independent versioning — harness elements are resolved once at agent-assembly time |

**Verdict: rejected as a primary architecture.** Elements are construction-time; capsules must
be selectable per step and versioned independently. A few AI4RnD rails will exist, but the
product is not a harness profile.

---

## Option 4 — Project subsystem, in-process *(mode + project, in-process, compile to Jiuwen)* ✅ **RECOMMENDED**

A Research mode opens a persistent project. The project owns contract, plan, evidence, gates
and artifacts, and **compiles** its plan to Core Workflow / SwarmFlow / Team. Runs on
`NativeHarness`.

| | |
|---|---|
| UX | mode → project → plan/evidence/gates/improvements ([19 §5](19-product-layers-and-ux.md)) |
| Control flow | project control plane → compiler → Jiuwen runtime → step wrapper records evidence |
| State ownership | [19 §6](19-product-layers-and-ux.md) — meaning AI4RnD, execution openjiuwen, conversation JiuwenSwarm |
| Execution | Core Workflow (static) · SwarmFlow (dynamic) · Team (open-ended) |
| Failure / cancel | inherited: journal replay, checkpoint resume, `_check_abort`, `NativeHarness.abort`. Repair DAGs are AI4RnD-side |
| Evolution | AI4RnD governance over `Trainer`/`Updater`/`Operator`/`EvolutionStore` [18] |
| Code boundary | AI4RnD package installed alongside JiuwenSwarm; rails + tools out-of-tree; ~10-line core patch only if the web UI must drive projects |
| **Duplication** | **~450 LOC of runtime code** — routing, write-scope, evidence capture [17 §7] |
| Upstream changes | none for Stages 0–3 |
| Buildable now | mode + project skeleton + SwarmFlow compilation: **~8 weeks** |
| **Falsified by** | F2 (Core Workflow cannot express runtime-determined fan-out), F4 (determinism lint blocks required patterns), or Checkpointer having no persistent backend and being invasive to add (F3) |

**Why it wins:** it is the only option that keeps all three AI4RnD-unique capabilities
(capability routing, write-scope exclusion, evidence/gates) while writing no scheduler, no
queue, no lease manager and no evolution trainer.

---

## Option 5 — Separate durable service *(app, separate service, own scheduler)* — Revision 2's answer

| | |
|---|---|
| Duplication | **~4,700 LOC** — 85% of `graph_scheduler` plus all of `actor_*` [17 §2] |
| Execution | its own workers, or a callback into JiuwenSwarm |
| Governance | rebuilds candidate selection, snapshot/rollback, freeze markers that `Trainer` already has |
| Upstream changes | a core patch to make the callback reachable |
| **Falsified by** | exactly what was found — the duplication is now measured |

**Verdict: rejected.** Its central justification was that JiuwenSwarm lacked durable
orchestration. It does not; openjiuwen has it. The isolation Revision 2 wanted is achievable
in-process, because `NativeHarness` already models a long-lived, pausable, abortable runtime.

**What was right:** ownership of meaning and verification. Option 4 keeps that.

---

## Option 6 — Fork *(any, any, fork)*

| | |
|---|---|
| **Falsified by** | V-4 — the most security-relevant defect is in **openjiuwen**, not JiuwenSwarm, so a JiuwenSwarm fork cannot fix it cleanly. And the mechanisms worth having are in openjiuwen too |

**Verdict: rejected**, more firmly than in Revision 2.

---

## Option 7 — Defer JiuwenSwarm *(app, own everything, generic infra)*

Build AI4RnD standalone on FastAPI + a queue + containers.

| | |
|---|---|
| Duplication | now includes **Pregel, Core Workflow, SwarmFlow, admission, checkpointing, `agent_evolving`** on top of channels, UI, memory and sandbox |
| **Falsified by** | the inventory [16] — the surface to rebuild roughly tripled |

**Verdict: rejected.** In Revision 2 this was the runner-up. It is now clearly the most
expensive path.

---

## Option 8 — Staged: tight first, isolate only if justified ✅ **adopted as the delivery strategy**

Not a competing architecture — the way Option 4 is built.

1. Start **in-process**: project subsystem in the AgentServer, compiling to SwarmFlow.
2. Introduce isolation **only where evidence demands it**: a separate process for the evidence
   store if contention appears; a separate service for evaluation if it needs different scaling.
3. Each isolation step must be justified by a measurement, not by anticipation.

Revision 2 started at maximum isolation and paid for it in duplication. This inverts the
default.

---

## Comparison

| Criterion | 1 Mode | 2 Workflow lib | 3 Harness | **4 Project (rec.)** | 5 Service | 6 Fork | 7 Defer JW |
|---|---|---|---|---|---|---|---|
| Persistent projects | ✗ | ✗ | ✗ | **✅** | ✅ | ✅ | ✅ |
| Evidence ledger + gates | ✗ | ✗ | ✗ | **✅** | ✅ | ✅ | ✅ |
| Capability routing | ✗ | ✗ | ✗ | **✅** | ✅ | ✅ | ✅ |
| Capsule registry + versioning | ✗ | ✗ | partial | **✅** | ✅ | ✅ | ✅ |
| Governed evolution | ✗ | partial | partial | **✅** | ✅ | ✅ | ✅ |
| Reuses Jiuwen scheduling | ✅ | ✅ | ✅ | **✅** | ✗ | ✗ | ✗ |
| Reuses `agent_evolving` | partial | partial | partial | **✅** | ✗ | ✅ | ✗ |
| Runtime code written | ~0 | ~0 | ~0 | **~450 LOC** | ~5,200 | ~5,200 | ~15,000+ |
| Upstream changes | none | none | **many** | none (Stages 0–3) | 1 patch | n/a | none |
| Reaches all 142 features | ✗ | ✗ | ✗ | **✅** | ✅ | ✅ | ✅ |
| Time to first value | 3 wks | 4 wks | 6 wks | **8 wks** | 11 wks | 8 wks | 12 wks |
| Time to complete | n/a | n/a | n/a | **12–14 mo** | 19–20 mo | 20+ mo | 18–20 mo |
| **Verdict** | layer 1 | target | ✗ | ✅ | ✗ | ✗ | ✗ |

---

## Why Option 4 over Option 5 — the re-earned argument

Revision 2 chose 5 on three grounds. All three now fail:

| Revision 2's reason | Status |
|---|---|
| "JiuwenSwarm lacks durable orchestration, so AI4RnD must own a scheduler" | **false** — Pregel checkpoints and resumes; SwarmFlow journals and replays [V-15, V-16] |
| "AI4RnD's roadmap must not be gated by JiuwenSwarm's release cadence" | **still true, and satisfied** — AI4RnD ships as its own package with its own tests; only the mode rail touches JiuwenSwarm |
| "Research execution must be governed by permissions and sandbox" | **still true, and better satisfied** — in-process compilation means every step is a normal Jiuwen tool call, with no callback contract to design |

The independence Revision 2 wanted comes from **package boundaries and state ownership**, not
from process boundaries. Option 4 keeps the boundary and drops the duplication.

---

## What would falsify Option 4

| # | Finding | Fallback |
|---|---|---|
| F2 | Core Workflow cannot express runtime-determined fan-out | rely on SwarmFlow alone; if that also fails → Option 5 |
| F3 | Checkpointer has no persistent backend in a default install and adding one is invasive | AI4RnD-side run store; partial move toward Option 5 |
| F4 | SwarmFlow's determinism lint blocks required research patterns | compile more to Core Workflow; if both fail → Option 5 |
| F5 | Write-scope exclusion cannot be solved at compile time **and** the admission protocol is insufficient | narrow scheduler for parallel groups only — not a full one |
| F6 | In-process project state contends with the AgentServer under load | apply Option 8 step 2: isolate the store, keep the architecture |

**F2 and F4 are the cheapest and most decisive** — roughly a day each, and they are the first
work in Stage 0.
