# Evidence, Assumptions and Open Questions

**Purpose of this document: separate what was verified from what was judged and what was assumed,
so a reviewer can weigh each claim correctly.** Three labels are used throughout this package:

| Label | Meaning |
|---|---|
| **Verified** | executed in this analysis environment, or confirmed by direct source reading (each entry says which) |
| **Architectural judgment** | a design decision reasoned from verified facts — could be made differently |
| **Unverified assumption** | believed but not demonstrated; each carries its reason |

Environment: JiuwenSwarm `0.2.3.beta1` (source checkout), OpenJiuwen `0.1.15.post3` (installed
package, imported and executed), AI4Research @ `d35c511`, workbook `AI4RnD Feature List.xlsx`.
29 executed experiments in total; the full probe scripts, commands and raw outputs are preserved
in [source-material/12-verification-appendix.md](source-material/12-verification-appendix.md).

---

## 1. Verified — by execution

| # | Finding | How |
|---|---|---|
| E1 | The workbook reconciles exactly: 25 groups, 142 features (54+65+23) | read directly with `openpyxl`; totals recomputed |
| E2 | SwarmFlow journal replay works: an interrupted run resumed re-executing only the failed step; a third run replayed with zero live calls | two-step probe script against the real engine |
| E3 | **A failed step returns `None` and the run reports success** after retries are exhausted | same probe; failing backend on step B |
| E4 | **The agent-facing SwarmFlow tool rejects `resume_id` and `name`** with "not supported yet", though both appear in its parameter schema | invoked the tool with each parameter combination |
| E5 | Admission control is a hard precondition: no governor → explicit refusal | same tool probe |
| E6 | **`agent_type` is validated and forwarded but consumed by no backend**; unknown option keys raise a precise error | engine probe + search of all backend implementations |
| E7 | Core Workflow accepts a router returning a runtime-computed node list; the run completes. The router is invoked with **no arguments** | built and ran a fan-out graph |
| E8 | **The built-in guardrail tier loads 0 rules** in a stock install; the loader looks only in the OpenJiuwen package, where no rules file ships | called the loader; observed the warning and empty result |
| E9 | The rules file JiuwenSwarm installs to the user config directory is **written by two files and read by none** | exhaustive search across the JiuwenSwarm tree |
| E10 | The evolution trainer requires `get_operators()`; **exactly one class in OpenJiuwen implements it**. JiuwenSwarm imports only the experience-archive and tool-description-optimizer parts | search + import census |
| E11 | All **42 capsule manifests** carry the same eight governed sections; the registry holds 35 entries (30 stable, 5 draft) | parsed every manifest and the registry |
| E12 | The seven typed graph domains, the Idea Card and account registration are **absent** from the AI4RnD tree; OpenJiuwen's graph memory is referenced zero times in JiuwenSwarm | exhaustive searches |
| E13 | AI4RnD's citation grounding check measured **0.25 precision** on a hand-labelled 9-case set | executed against the real checker (earlier revision, preserved) |
| E14 | AI4RnD's evidence ledger and gate ledger run standalone; out-of-tree Rail plugins register, resolve, invoke and uninit correctly | executed (earlier revisions, preserved) |
| E15 | The prior 142-row matrix matches the workbook row-for-row: zero wording mismatches | position-by-position comparison |

## 2. Verified — by source reading (not executed, with reasons)

| # | Finding | Why not executed |
|---|---|---|
| S1 | **Unknown model name → silent substitution**: the resolver returns `None` for a missing pool group and the worker backend falls back to its default model, by documented design | end-to-end confirmation needs a live team with a populated model pool → provider credentials, excluded by the safety rules |
| S2 | A stock install sets a sqlite persistence checkpointer as the process default at startup | restart-survival known from code path; a full restart drill was not run |
| S3 | The SwarmFlow journal path is keyed by team, **session id** and workflow name — a new session replays nothing | follows directly from the path-resolution code |
| S4 | Resume exists internally as a control-plane relaunch, deliberately not a tool | code comment states the design intent |
| S5 | OpenJiuwen's `Operator` is a tunable-parameter handle, "NOT an executable unit" (verbatim) | definitional |

## 3. Architectural judgments

These are choices, not findings. Each could be revisited without any fact above changing.

| # | Judgment | Basis |
|---|---|---|
| J1 | Progressive compilation (Option C) over immediate delegation (D) or a permanent own scheduler (A) | D fails the preservation gate today (S1, E3, E4); A pays a permanent duplication tax for engines E2/E5/E7 prove work |
| J2 | Option D's gate failure is evidence against *immediate* delegation, **not** proof it can never be safe | the blocking gaps are small and individually fixable |
| J3 | Seven typed graphs as projections over one authoritative store, not seven databases | the workbook requires typed views with provenance, not physical separation |
| J4 | The nine lanes are capabilities, not a rigid sequence | the workbook defines what lanes must do, not an ordering constraint; repair/replanning requires revisiting |
| J5 | Execution mechanism is never a user choice | exposing it couples product semantics to a user's guess about internals |
| J6 | AI4RnD's executable Operator concept must carry a different name inside integration code | E10/S5 naming collision |
| J7 | Effort expressed as work items with acceptance criteria; all earlier LOC and month figures withdrawn | the figures were extrapolated from reading, and execution (E3, E4, E6) found work they missed |
| J8 | The preservation-gate verdicts per row per option | rule-based on each row's class and decision; the rules and per-row results are in the [gate CSV](traceability/142-feature-preservation-gate.csv) |

## 4. Unverified assumptions

| # | Assumption | Risk if wrong |
|---|---|---|
| U1 | The six packaging/installer rows (Windows, macOS, CLI, TUI) work as documented — labelled UNVERIFIED in the ownership CSV; this environment cannot build platform installers | P1 platform scope grows |
| U2 | jiuwenbox sandbox enforcement holds under adversarial use — needs kernel privileges to test | security posture weaker than assumed; re-test before relying on it |
| U3 | Dynamic Team roles and permissions suffice for open-ended excursions — needs a live team runtime | open-ended steps fall back to DeepAgent or scripted panels |
| U4 | A calibrated entailment check can materially beat 0.25 precision on research citations | **the product's central claim fails**; this is why P3 publishes its bar before building |
| U5 | SwarmFlow's determinism lint will accept compiled research sub-plans (spike F4, still open) | compilation targets narrow to Core Workflow; if that also fails, revert to Option A |
| U6 | Real AI4RnD capsules can be bound as evolution subjects without framework changes | P6 grows; RSI surfaces stay manual longer |

## 5. Open product questions

Recorded, not guessed. These need a product owner's decision, not more analysis.

| # | Question | Where it bites |
|---|---|---|
| Q1 | **"Cluster setting"** (System Configurations) is a single workbook line with no description. What does a cluster own — execution hosts, model capacity, data residency? | the one UNRESOLVED row; P1 config surface |
| Q2 | **tmux** is listed as a message channel in the workbook, but the recommended architecture retires the tmux cockpit as the carrier. Is tmux a supported channel of the product, or legacy tooling? | channels scope in P1 |
| Q3 | The workbook references a **"V-05-qualified"** intake tier defined outside the workbook. What are its qualification criteria? | ingestion lane acceptance |
| Q4 | Strategic opportunity screening criteria are organization-specific and undefined in the workbook. Who owns them? | opportunity lane, P4 |
| Q5 | Is the **project** the right product unit, or do users also need one-shot runs with no durable record? | P1 exit review |

## 6. Negative findings that must not get lost

For a reviewer who reads only one section of this document: the recommendation is shaped by seven
verified negatives, and any future change to the architecture should re-check them first.

1. Silent model substitution (S1) — fails Option D today.
2. Resume advertised but rejected at the agent surface (E4).
3. Failed steps degrade to `None`; the run reports success (E3).
4. `agent_type` accepted, forwarded, read by nothing (E6).
5. Guardrail tier loads zero rules; the installed rules file is orphaned (E8, E9).
6. One of eight RSI surfaces wired end to end (E10).
7. Grounding precision 0.25 (E13) — the deepest product-correctness gap, independent of any
   integration choice.

A pattern worth remembering: **this codebase fails loudly on typos and silently on unimplemented
features.** Reading source overstates what is reachable; every reuse decision in this package is
therefore labelled by whether it was executed.

## 7. What "verified" does not mean here

HTML, link and diagram checks in this package validate the *documents*, not the product. No claim
of product-runtime correctness is based on them. Product-runtime claims come only from the
experiments in §1, and their limits are stated in §2 and §4.

---

*Provenance: the full analysis history — 21 working documents across four revisions, including
the correction log of what each revision got wrong and why — is preserved under
[source-material/](source-material/README.md). The primary documents supersede it.*
