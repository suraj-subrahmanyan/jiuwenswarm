# AI4RnD on JiuwenSwarm — Architecture Evaluation (Revision 4)

**Question.** How can the complete intended AI4RnD product — all 142 outcomes in
`AI4RnD Feature List.xlsx` — be built using JiuwenSwarm and OpenJiuwen as its application and
execution foundation?

**Answer. AI4RnD is a first-class application surface on the JiuwenSwarm platform**: a persistent
project subsystem with its own semantic control plane, a workspace capability registry, and a
governed evolution loop — compiled **progressively** onto OpenJiuwen execution mechanisms.

**Architecture option C.** [Options](07-architecture-options.md) ·
[recommended target](08-recommended-architecture.md) ·
[row-by-row ownership](20-feature-implementation-ownership.md).

---

## The rule this revision enforces

**The product definition is held constant while implementation architectures are compared.**

DeepAgent, SwarmFlow, Core Workflow and Dynamic Team are **execution mechanisms inside the
product**, not competing versions of it. None of them implements the nine R&D workflow lanes,
Capability Capsules, logical and physical Operators, scientific evaluators, eight RSI surfaces,
seven typed graph domains, Harness Core, Intention Compilers, Planner, Builder, or any of the
visibility, installation, UI, account, channel and configuration outcomes. Alone, each implements
**0 of 142**.

An option is a complete architecture only if it preserves all 142 outcomes.

| Verdict | A | B | C ★ | D | E |
|---|---:|---:|---:|---:|---:|
| PRESERVED | 70 | 76 | 76 | 58 | 82 |
| PRESERVED WITH ADAPTATION | 12 | 6 | 6 | 23 | 0 |
| NEW BUILD REQUIRED | 58 | 58 | 58 | 57 | 58 |
| UNRESOLVED | 2 | 2 | 2 | 3 | 2 |
| **DROPPED** | **0** | **0** | **0** | **1** | **0** |

**Option D fails**: it drops `FN-19 Model Routing & Selection`, because an unknown model name
silently substitutes the default and D leaves no AI4RnD-side layer to catch it.

**The number that matters most barely moves.** `NEW BUILD REQUIRED` is 57–58 under every option —
58 outcomes exist in neither system. No architecture choice avoids them.

---

## What Revision 4 changed

Revision 3 read the OpenJiuwen execution stack. **Revision 4 executed it.** Four surfaces that read
as reusable are not yet reachable:

| # | Finding | Class |
|---|---|---|
| 1 | The leader-facing `swarmflow` tool advertises `resume_id` and **rejects it at invoke** — engine replay works, but no agent can trigger it | EXEC |
| 2 | A failed agent step returns **`None` after its retries and the run reports success** | EXEC |
| 3 | `agent_type` is validated, forwarded, and **read by no backend** | EXEC |
| 4 | An unknown model name **silently substitutes** the default worker model | SRC |
| 5 | JiuwenSwarm installs an 86-line `builtin_rules.yaml` that **nothing reads back**; openjiuwen's loader refuses user directories and loads **0 rules** | EXEC |
| 6 | `Trainer.train` needs `get_operators()`; **exactly one class in openjiuwen implements it**. Of eight RSI surfaces, **one is wired**, not seven | EXEC |

| | Revision 3 | Revision 4 |
|---|---|---|
| Architecture answer | "mode + project subsystem + registry" | **first-class application surface**, option **C** |
| Migration stance | retire the AI4RnD scheduler up front | retire it **per capability, against a passing test** |
| Options compared | 8 triples mixing mechanisms with architectures | **5 complete-product options**; mechanisms excluded |
| Product-preservation check | none | **142 × 5**, D fails |
| RSI surfaces absent | 1 of 8 | **1 of 8 wired** |
| Effort language | "~450 LOC", "~12–14 months" | **withdrawn** — work items with acceptance criteria |

Two Revision 3 open spikes closed favourably: Core Workflow **does** accept a runtime-computed
fan-out (F2), and a stock install **does** configure a persistent sqlite checkpointer (F3).

Full account: **[15-correction-log.md](15-correction-log.md) §9**.

---

## The workbook is the controlling source

Read directly with `openpyxl` in this revision:

| Sheet | Plane | L1 groups | L2 features |
|---|---|---:|---:|
| Workflow Features | Workflow | 9 | 54 |
| Foundation Features | Foundation | 10 | 65 |
| Vertical Features | Vertical | 6 | 23 |
| **Total** | | **25** | **142** |

Checked position-by-position against the Revision 3 CSV: **0 mismatches**. The row set was already
right. What was missing was ownership — who defines a feature's meaning, who runs it, who stores
it, who validates it, and where the user sees it.

| Ownership | Rows |
|---|---:|
| **Semantically owned by AI4RnD Core** | 118 |
| Semantically owned by JiuwenSwarm Application | 19 |
| External / New Product Work | 4 |
| Unresolved | 1 |
| | |
| **Runtime** — AI4RnD Core | 53 |
| Runtime — AI4RnD–Jiuwen Integration | 32 |
| Runtime — JiuwenSwarm Application | 27 |
| Runtime — OpenJiuwen Runtime | 25 |

**That divergence is the architecture.** 118 rows are AI4RnD's to define; only 53 are its to run.

---

## Capability Capsules are not templates

Verified: all **42** capsule manifests carry the same eight-section body — `applicability`,
`contract`, `composition`, `effects`, `bindings`, `verification`, `operator_compatibility`,
`provenance`. The registry holds 35 entries (32 capability, 1 guard, 2 resource), 30 stable, 5
draft. A JiuwenSwarm *skill* carries a name, a description and a prompt.

The five levels stay distinct: **Capsule** (governed reusable capability) → **Contract** (promise
for this request) → **TaskGraph** (project-specific plan) → **Logical Operator** (stable callable
action) → **Physical Operator** (actual executor). Capsules shape, constrain, observe and improve
executions; they never hide the concrete DAG.

---

## Start here

| Read this | For |
|---|---|
| **[20 Feature implementation ownership](20-feature-implementation-ownership.md)** | all 142 rows, decided |
| **[07 Architecture options](07-architecture-options.md)** | five complete-product options and the gate |
| **[08 Recommended architecture](08-recommended-architecture.md)** | the target, ten layers, boundary rules |
| **[15 Correction log §9](15-correction-log.md)** | what executing the runtime changed |
| **[12 Verification appendix](12-verification-appendix.md)** | every probe, command and output |

---

## Document set

| # | Document | Contents |
|---|---|---|
| 00 | [Intended product model](00-intended-product-model.md) | 142 features; Capsule→Contract→Operator stack; RSI scope |
| 01 | [JiuwenSwarm architecture](01-jiuwenswarm-architecture.md) | current state, corrected by execution |
| 02 | [AI4RnD architecture](02-ai4rnd-architecture.md) | current state incl. dormant and unwired code |
| 03 | [Workflow traces](03-workflow-traces.md) | entry → planning → routing → execution → verification |
| 04 | [Component comparison](04-component-comparison.md) | component-by-component verdicts |
| 05 | [Capability matrix](05-capability-matrix.md) | provided / partial / extensible / missing |
| 06 | [Integration challenges](06-integration-challenges.md) | conflicts and blockers |
| 07 | [Architecture options](07-architecture-options.md) | **Rev 4** — five complete-product options + preservation gate |
| 08 | [Recommended architecture](08-recommended-architecture.md) | **Rev 4** — ten layers, ownership, capsules, RSI |
| 09 | [Staged path](09-implementation-plan.md) | **Rev 4** — six phases, work items, no month estimates |
| 10 | [Risks & open questions](10-risks-assumptions-open-questions.md) | incl. withdrawn assumptions |
| 11 | [Evidence appendix](11-evidence-appendix.md) | source references |
| 12 | [Verification appendix](12-verification-appendix.md) | **29 experiments**, commands and results |
| 13 | [Maturity map](13-maturity-map.md) | active / unwired / scaffold / spec / absent |
| 14 | [Reuse-vs-build map](14-reuse-vs-build-map.md) | superseded for sourcing by doc 20 |
| 15 | [Correction log](15-correction-log.md) | **Rev 4 §9** — what execution changed |
| 16 | [Jiuwen execution mechanisms](16-jiuwen-execution-mechanisms.md) | bottom-up map of all five mechanisms |
| 17 | [TaskGraph verdict](17-taskgraph-verdict.md) | custom scheduler vs reuse |
| 18 | [Evolution governance](18-evolution-governance.md) | governed RSI over `agent_evolving` |
| 19 | [Product layers & UX](19-product-layers-and-ux.md) | product model, user controls, state ownership |
| **20** | [**Feature implementation ownership**](20-feature-implementation-ownership.md) | **all 142 rows: owner · runtime · persistence · verification · surface** |
| — | [Ownership CSV](traceability/142-feature-implementation-ownership.csv) · [Preservation gate CSV](traceability/142-feature-preservation-gate.csv) | machine-readable |
| — | [142-feature matrix](traceability/142-feature-matrix.md) · [CSV](traceability/142-feature-matrix.csv) | Revision 3 coverage view |
| — | [Diagrams](diagrams/README.md) | 27 diagrams |

### Rendered HTML

Every document above is also published as a polished, fully offline HTML site — no CDN, no
network, no build step. Open either file directly in a browser.

| Artifact | What it is |
|---|---|
| [`html/index.html`](html/index.html) | **navigable site** — sidebar, per-page contents, prev/next, light & dark |
| [`ai4rnd-architecture-review.html`](ai4rnd-architecture-review.html) | **single-file edition** — everything on one page, for archiving or printing |

All Mermaid diagrams render inline from a vendored copy of the renderer
(`html/vendor/mermaid.min.js`), themed to the same tokens as the text. Markdown and CSV remain the
source of truth; the HTML is generated from them:

```
python3 tools/gen_ownership.py .   # -> traceability/*.csv  (from the workbook)
python3 tools/gen_doc20.py .       # -> 20-feature-implementation-ownership.md
python3 tools/mdsite.py .          # -> html/
python3 tools/onepage.py .         # -> ai4rnd-architecture-review.html
```

Colours come from AI4Research's own `DESIGN.md`: Huawei black / white / red, red rationed as a
signal, amber for blocked, quiet ink for done.

---

## Reading the evidence

`V-n` refers to a verification experiment in
[12-verification-appendix.md](12-verification-appendix.md); `[E-Jxx]` / `[E-Axx]` to source
references in [11-evidence-appendix.md](11-evidence-appendix.md).

Claims are labelled **EXEC** (executed in this environment), **SRC** (source-read), **DOC**
(documented), **INF** (inferred). Across the 142-row ownership matrix: **34 EXEC · 69 SRC · 6 DOC ·
33 INF**. Every `INF` row is one where the analysis asserts an absence or a design intent it could
not execute against.

Six reuse claims are labelled **UNVERIFIED** — all Windows and macOS packaging rows, which cannot
be built in this environment.

Not executed, and why: no live model call, no live team runtime, no sandbox enforcement test, no
platform installer build. All require credentials, kernel privileges or host platforms the
safeguards exclude.
