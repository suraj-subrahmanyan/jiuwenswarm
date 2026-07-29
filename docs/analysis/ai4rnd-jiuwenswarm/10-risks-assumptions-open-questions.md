# Risks, Assumptions, Conflicting Evidence, and Open Questions

Revision 2. Items closed by execution are marked **CLOSED** with the experiment that closed
them; new items arising from execution are marked **NEW**.

---

## L — Limitations of this analysis

### L1 — Execution coverage (was: "nothing was executed") — **substantially closed**

Revision 1's largest limitation. Now: `openjiuwen==0.1.15.post3` and `jiuwenswarm` were
installed and inspected; 14 experiments were run; 2,816 JiuwenSwarm tests and 556 AI4RnD
tests were executed. See [12-verification-appendix.md](12-verification-appendix.md).

**What remains unexecuted**, and why:

| Not executed | Reason | Consequence |
|---|---|---|
| A live JiuwenSwarm agent conversation | needs model credentials — safeguard: no paid/authenticated providers | Rail *lifecycle* across restart unverified (spike G2) |
| The execution callback against a real `DeepAgent` | same | the decisive architecture question (spike G1) |
| jiuwenbox sandbox enforcement | needs kernel privileges | sandbox strength assumed from source |
| AI4RnD tmux dispatch | needs tmux + agent CLIs + credentials | behaviour taken from `DISPATCH-PROTOCOL.md` |
| GEPA `run --execute` | would spend model budget | lifecycle verified via `--help`/`status` + source |
| Full AI4RnD suite | collection aborts (`SystemExit` at import) | subsets run instead; coverage is partial |

### L2 — AI4RnD sampled, not exhaustively read
~534k LOC / 5,778 files. 48 architecturally significant modules were probed by execution;
most of `lib/` outside research/scheduler/gate/operator/capsule/RSI paths was not read, nor
`autopilot/`, `brain/`, `x_api/`, `youtube/`, `influence/`, `vendor/autoresearch/`. A
capability reported ABSENT may exist in an unread module.

### L3 — Feature-list interpretation
The 142 rows are terse (often one sentence). Maturity and coverage judgements map a feature
*description* onto code found by targeted search. Reasonable people could classify some rows
differently — particularly the 21 `SCAFFOLD` rows, which are the least crisp category.

### L4 — Single-branch view
Only default branches were read (shallow, depth 50). A capability called ABSENT may exist on
an unmerged branch. `add_repo` refused the `Stellven/*` repositories (cross-tier), so they
were cloned over HTTPS; PRs and issues were not examined.

### L5 — Effort estimates are structural, not empirical
Derived from module sizes, coupling and test coverage. No velocity data. Treat stage
durations as relative ordering, not schedule.

---

## A — Assumptions

| # | Assumption | Basis | If wrong |
|---|---|---|---|
| **A1** | AI4RnD = `Stellven/AI4Research*` | **strengthened** — `AI4RnD Feature List.xlsx` was found inside `AI4Research/Feature list stuff/` | was the largest binary risk; now near-certain |
| A2 | `openJiuwen-Solar` branch is current | most recently pushed; contains the feature workbook | may be a working branch |
| A3 | The workbook is the authoritative product definition | user designated it "the controlling traceability set" | if superseded, scope shifts |
| A4 | Rails can register tools out-of-tree | **CLOSED by V-2** — executed | — |
| A5 | The research core has no hidden Solar coupling | **CLOSED by V-10** — ran standalone | — |
| A6 | Capsules are a distinct abstraction, not skills | **CLOSED by V-11** — 11-section schema, 30 registered | — |
| A7 | JiuwenSwarm members can carry distinct capabilities | **REFUTED by V-6** — two roles, global policy | writer≠verifier moves to AI4RnD's router (adopted) |
| A8 | Two processes are operationally acceptable | JiuwenSwarm already runs gateway + agentserver + web + jiuwenbox | Stage 2 exit gate tests it |
| A9 | The 19 unwired modules work when wired | they import and have tests; **wiring is unproven** | Stage 3 cost rises; the modules may need rework |
| A10 | `evolution_engine`'s single tracked capability reflects early adoption, not a design ceiling | source structure is general | RSI scope smaller than believed |
| A11 | The tmux carrier is an implementation artifact, not a requirement | README frames it as the current substrate | if it is a requirement, the physical-operator model changes (Q4) |

---

## C — Conflicting evidence

### C1 — README maturity vs SDD ambition (unchanged)
`AI4Research/README.md`: *"Solar is not a finished autonomous cloud service… Some code in
`core/` is roadmap scaffolding or compatibility glue."* The Pipeline A SDD describes a
complete research compiler. **Resolution:** README authoritative on maturity, SDD on intent;
the maturity map distinguishes the two.

### C2 — "Capability-routed DAG" vs a linear role state machine (unchanged)
`DESIGN.md` insists routing is a capability-routed DAG, not a PM→Planner→Builder→Evaluator
line; `coordinator-state-machine.json` is exactly that line. **Resolution (inference,
moderate confidence):** the *sprint* lifecycle is a linear role handoff; the *task graph
within* a sprint is capability-routed.

### C3 — RSI ambition vs implementation — **NEW**
The workbook specifies eight RSI surfaces with named methods. Execution found **one**
implemented (GEPA, 3,540 LOC) and unwired; MIPROv2, TextGrad, Voyager, AFlow, MCTS, CEGIS,
GRPO return zero word-boundary matches. **Resolution:** RSI is genuine in architecture and
in one instance, aspirational in the other seven. Recorded per-surface in the matrix.

### C4 — Verification claim vs verification behaviour — **NEW, most consequential**
AI4RnD's stated discipline is *"Gates decide"*, and the evidence ledger, spans and hashing
are sound. But the grounding gate passes on one shared token (measured precision 0.25). The
system's central claim — that its output is verified — **does not currently hold at the
citation layer**. **Resolution:** ledger/spans/hashing are ported; the grounding *judgement*
is replaced in Stage 1, not carried over.

### C5 — Documented permission behaviour vs actual — **NEW**
`docs/en/ToolPermissionsSecurity.md` describes built-in denials that "user rules cannot
override" and shell-operator escalation. In a stock install the built-in layer loads **0
rules**, and chaining is decomposed rather than escalated. **Resolution:** documentation
describes an older openjiuwen; the pinned version behaves differently. Treated as a live
defect, not a doc error.

### C6 — DeepSearch overlap — **CLOSED**
Revision 1 flagged this as possibly invalidating the case. `scripts/main.py` is 337 LOC with
**zero** citation/evidence/claim/provenance references. Not the same class of artifact. Risk
downgraded High → Low.

---

## Q — Open questions

### For the AI4RnD owners

| # | Question | Why it matters |
|---|---|---|
| Q1 | Is the workbook the current product definition, or still moving? | 11 rows are marked DEBATED from its own notes |
| Q2 | *"one capsule have multiple contracts inside???"* (workbook, Capsule §4) | determines the capsule↔contract cardinality and the registry model |
| Q3 | Which planning strategies exist — templates or real-time generation? (workbook, Planner §1) | changes whether planning is a library or a generator |
| Q4 | Is the tmux cockpit a user requirement or an implementation artifact? | if a requirement, the physical-operator model and the recommendation change materially |
| Q5 | Why are 19 modules implemented but unwired — deliberate staging, or abandoned? | determines whether Stage 3 is integration or rescue |
| Q6 | Has grounding precision ever been measured internally? | V-12 suggests not; affects trust in past outputs |
| Q7 | What is the intended scale — single researcher, team, or product? | accounts (132–135) are absent from both systems |
| Q8 | Is RSI-7 (model weights) in scope, or permanently aspirational? | deferred in the plan |
| Q9 | *"what other kind of contract?"* besides TaskGraph (workbook, Intention compilers §5) | the contract taxonomy is undefined |
| Q10 | Should evaluators be split into more L2 features, per the workbook's own note? | affects the 6-family structure |

### For the JiuwenSwarm maintainers

| # | Question | Why it matters |
|---|---|---|
| Q11 | Is the missing `openjiuwen/harness/resources/builtin_rules.yaml` a packaging bug? | **security-relevant**; V-4 shows the guardrail layer is empty in a stock install |
| Q12 | Is `curl … \| bash` resolving to ALLOW under subcommand decomposition intended? | V-4; download-and-execute survives the built-in rule |
| Q13 | Would a generic extension-RPC passthrough be accepted upstream? | removes the only core patch in Stage 4 |
| Q14 | Is `RailManager` a supported extension API or an internal mechanism? | Stages 1–3 depend on it |
| Q15 | Are more than two member roles planned? | V-6 blocks per-operator governance |
| Q16 | What is `openjiuwen`'s API-stability policy at 0.1.x? | the Rail seam is an openjiuwen interface |
| Q17 | Does a Rail plugin survive agent-cache invalidation and restart? | **spike G2** — decisive; not answerable without a live agent |

### Technical, resolvable by spike

| # | Question | Spike |
|---|---|---|
| Q18 | Can a bounded work packet be dispatched and cancelled against a live `DeepAgent`? | G1 |
| Q19 | What fraction of `graph_scheduler.py` is Solar-coupled? | E6 |
| Q20 | Do the 19 unwired modules work when wired together? | Stage 3 |
| Q21 | Does placing `builtin_rules.yaml` in openjiuwen's package path restore the guardrails? | N1 |
| Q22 | Can capsule `effects` be enforced at binding without a permission-engine change? | Stage 3 |
| Q23 | What entailment precision is achievable, and what bar should Stage 1 set? | Stage 1 |

---

## R — Risks

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | A1 wrong (different system) | **Very low** (was Low) | Fatal | workbook found inside the repo |
| R2 | Rail seam unusable | **Closed** | — | V-2 |
| R3 | Rail does not survive restart | Medium | High | spike G2, week 1 — flips to Option G |
| R4 | Execution callback unworkable | Medium | High | spike G1 — flips to Option G |
| R5 | DeepSearch makes the case moot | **Low** (was Medium/High) | Low | V-14 |
| R6 | Grounding cannot be made trustworthy | **Medium** | **High** | Stage 1 bar set before building; if unmet the product's core claim fails |
| R7 | 19 unwired modules need rework, not wiring | **Medium** | Medium | Stage 3 estimate assumes integration; audit early |
| R8 | `openjiuwen` 0.1.x breaks the Rail API | Medium | Medium | pin; wrap behind one adapter file |
| R9 | Two-role limit blocks per-operator governance even router-side | Low–Med | Medium | enforce in AI4RnD's router (adopted); Q15 upstream |
| R10 | Permission guardrail gap ships to production | **Medium** | **High** | Stage 1 exit gate asserts `get_builtin_security_rules() > 0` |
| R11 | RSI produces churn, not improvement | Medium | Medium | Stage 6 decision point requires measured improvement |
| R12 | Prompt injection via fetched sources | **High** | Med–High | run source-fetching operators inside jiuwenbox with network policy; never let fetched content reach a tool-calling context unfiltered |
| R13 | 27 build-new features under-scoped | Medium | Medium | they include the entire opportunity lane, falsifiability screening, accounts and 6 RSI surfaces |
| R14 | Unsandboxed Rail plugin becomes an incident | Low | High | first-party plugin only; do not market a third-party plugin story |
| R15 | Both upstreams pre-1.0 churn faster than integration lands | Medium | Medium | minimal in-tree footprint; Stages 0–3 need none |

**R6 and R10 are the two that should be resolved before any production use.** R6 is whether
the product does what it claims; R10 is whether the substrate is as safe as assumed. Both
were discovered by execution in this revision, and neither is visible from reading.

---

## Confidence

| Conclusion | Confidence | Basis |
|---|---|---|
| Capsules are a distinct governed abstraction | **High** | executed (V-11) |
| Grounding precision is inadequate | **High** | measured (V-12) |
| Built-in security rules do not load | **High** | executed (V-4) |
| Out-of-tree Rail can register + invoke tools | **High** | executed (V-2) |
| JiuwenSwarm covers ~20/142 features fully | **Medium-High** | matrix judgement over executed + source evidence |
| 19 modules are implemented-but-unwired | **High** | executed probe (V-8) |
| GEPA is real and unwired | **High** | executed (V-13) |
| Hybrid is the right architecture | **Medium-High** | follows from the above; sensitive to G1/G2 |
| Option G is the runner-up, not a distant one | **Medium** | judgement |
| Effort estimates | **Low-Medium** | structural, not empirical |
| Feature-level maturity classifications | **Medium** | 21 SCAFFOLD rows are the softest |
