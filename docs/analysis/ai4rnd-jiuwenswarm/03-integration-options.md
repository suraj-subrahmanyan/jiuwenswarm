# Integration Options

**Purpose of this document: compare the five coherent ways to put AI4RnD on the JiuwenSwarm
foundation, and show why progressive compilation (Option C) wins.**

One rule governs the comparison: **an option is a complete architecture only if it preserves all
142 workbook outcomes.** Every outcome was evaluated under every option
([preservation-gate CSV](traceability/142-feature-preservation-gate.csv)). Execution mechanisms —
DeepAgent, SwarmFlow, Core Workflow, Dynamic Team — are *not* options: each implements 0 of the
142 outcomes alone. They appear inside every option as the machinery ready work runs on.

---

## 1. The five options

**A — AI4RnD-led control plane on Jiuwen execution.**
AI4RnD keeps its own scheduler, contracts, capsules, evidence and gates unchanged. Jiuwen replaces
only the physical executors (agents instead of tmux panes). Maximum preservation of working AI4RnD
code; forfeits the verified Jiuwen engines (durable graphs, journal replay, admission control) and
maintains a parallel scheduler forever.

**B — Jiuwen-native lifecycle with AI4RnD semantic control.**
Core Workflow runs the outer research lifecycle as durable stages with checkpoints and human
turns. AI4RnD keeps the project TaskGraph, capsules, contracts, evidence and RSI, and Jiuwen
mechanisms execute the stages. Commits to the delegation immediately.

**C — Progressive compilation (recommended).**
Same target picture as B, plus a migration discipline: AI4RnD-side scheduling and safety logic is
retired **per capability, only after a compatibility test passes** — never on a schedule. Starts
with the outer lifecycle on Core Workflow, deterministic sub-plans on SwarmFlow, and AI4RnD
retaining capability binding, model routing, failure detection, gate evaluation and run-state
authority. Each verified gap that closes upstream retires the corresponding AI4RnD fallback.

**D — Full delegation now.**
AI4RnD keeps semantics but removes its execution-side machinery immediately, trusting Jiuwen for
persistence, gates-relevant completion signals, cancellation, recovery and routing.

**E — Standalone baseline / defer.**
Keep AI4RnD as it is (tmux carrier, own scheduler) and postpone integration. Changes nothing,
gains nothing: no channels, no sandbox, no UI, no packaging — and the ~50 never-built outcomes
stay unbuilt.

## 2. Preservation-gate results

| Verdict | A | B | C ★ | D | E |
|---|---:|---:|---:|---:|---:|
| PRESERVED | 71 | 78 | 78 | 59 | 84 |
| PRESERVED WITH ADAPTATION | 13 | 6 | 6 | 24 | 0 |
| NEW BUILD REQUIRED | 56 | 56 | 56 | 55 | 56 |
| UNRESOLVED | 2 | 2 | 2 | 3 | 2 |
| **DROPPED** | **0** | **0** | **0** | **1** | **0** |

Two facts stand out.

**First: the big number never moves.** 55–56 outcomes require new construction under *every*
option, because they exist in neither system (all seven typed graphs, the Idea Card, account
management, most evaluators, most RSI surfaces…). Any comparison that makes one option look
dramatically cheaper is comparing execution plumbing, not the product.

**Second: only D drops an outcome.** Model Routing & Selection is lost under D because OpenJiuwen
silently substitutes the default model when a requested one is missing, and under D no AI4RnD
layer remains to catch it. D also leaves failure recovery unresolved: resume is not reachable
from the agent surface, and a failed step returns `None` while the run reports success.

**This is evidence against *immediate* full delegation — not proof that full delegation can never
be safe.** All three blocking gaps are small and fixable. If they close upstream, D stops
dropping outcomes, and C's mature form *is* D. The gate measures the systems as they are today.

## 3. Why C over A and B

| Consideration | A | B | C ★ |
|---|---|---|---|
| Preserves all 142 outcomes | yes | yes | yes |
| Uses the verified Jiuwen engines (durable graphs, replay, admission) | no | yes | yes |
| Maintains a duplicate scheduler indefinitely | yes | no | shrinking |
| Survives the known runtime gaps without new risk | yes | only if bridged correctly on day one | yes — fallbacks stay until tests pass |
| Migration reversible if a gap proves worse than measured | n/a | partly | yes, by construction |

A pays a permanent tax (two schedulers, ~4,700 lines of duplicated readiness/queue/lease logic)
to avoid a risk that can be managed more cheaply. B is the right destination but the wrong
commitment schedule: it deletes fallbacks on the strength of reading the engine, and this
analysis's execution testing showed exactly where reading overstates reachability. C differs from
B only in *when* each fallback dies — and ties each retirement to a named, falsifiable test:

- silent model substitution fixed → retire AI4RnD-side model routing;
- resume exposed through a supported surface → retire AI4RnD-side re-drive logic;
- failed steps propagate as failures → slim the run-state authority;
- typed executor binding honored end to end → retire bridge-side type enforcement.

## 4. What is permanently AI4RnD's, under every option

Regardless of how far delegation eventually goes, the product keeps final authority over:
**semantic readiness** (is this step *meaningfully* ready, not just dependency-ready), **evidence
sufficiency**, **gate decisions**, **repair and replanning**, and **project completion**. These
are product semantics, not scheduling — no execution engine can decide them, and no option
proposes that one should.
