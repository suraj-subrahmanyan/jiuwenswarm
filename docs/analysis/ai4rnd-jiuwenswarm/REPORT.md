# AI4RnD on JiuwenSwarm — The Architecture Report

**Recommendation: build the complete intended AI4RnD product as a first-class, persistent
subsystem on JiuwenSwarm, with AI4RnD permanently owning product semantics, OpenJiuwen supplying
execution, and a thin integration bridge compiling ready work onto the runtime progressively —
each delegation gated by a passing compatibility test. All 142 workbook outcomes are preserved;
none is dropped, weakened or renamed into something less capable.**

This report is self-contained: a technically informed reader needs no other document to
understand the product, the current systems, the recommended architecture, its end-to-end
behaviour, ownership and state boundaries, component sourcing, implementation direction,
evidence, risks and open decisions. The row-level matrices, probe transcripts and the full
analysis history remain available as supporting material and are linked where relevant, but
nothing below depends on them.

**How to read the evidence labels.** Every load-bearing claim carries one of: **EXEC** —
executed in this analysis environment; **SRC** — verified by direct source reading of the pinned
dependencies (JiuwenSwarm `0.2.3.beta1`, OpenJiuwen `0.1.15.post3`, AI4Research `d35c511`);
**DOC** — documented only; **INF** — inferred; **UNKNOWN** — explicitly not determinable here.
29 experiments were executed in total.

---

## 1. What AI4RnD is intended to become

**AI4RnD is an evidence-governed autonomous R&D system.** It discovers needs and opportunities,
researches and ideates, forms explicit technical claims and falsifiable hypotheses, builds
proof-of-concept software, runs experiments and benchmarks, evaluates results against declared
acceptance criteria, and delivers defended conclusions — while retaining what it learned as
organizational knowledge and improving its own capabilities under governance.

Its verification spine is **claims refinement**: nothing the system asserts reaches a user
without resolving to evidence, and nothing is built before its hypothesis can state what would
refute it. An earlier revision of this analysis used that spine as the whole identity
("a claims refinery"). That framing was too narrow — it made the product sound like a
literature-review engine. The refinery is the spine; the product is the whole R&D body around
it: opportunity discovery, POC construction, benchmarking, datasets, capability development,
delivery and self-improvement are first-class outcomes, not accessories to citation checking.

The product is defined by a 142-feature workbook, read directly in this analysis (**EXEC**) and
reconciling exactly:

| Sheet | Plane | Groups | Features |
|---|---|---:|---:|
| Workflow Features | what a research run does — nine lanes from ingestion to delivery | 9 | 54 |
| Foundation Features | the machinery underneath — capsules, operators, evaluators, models, RSI, data, harness, compilers, planner, builder | 10 | 65 |
| Vertical Features | the product around both — visibility, installers, UI, accounts, channels, configuration | 6 | 23 |
| **Total** | | **25** | **142** |

This definition is held constant everywhere below. **Current code is evidence of maturity and a
source of reusable assets; it is never the boundary of the target product.** Every sourcing
decision in §7 is an implementation strategy and redefines nothing.

### 1.1 The intended architecture, independent of any foundation

Before choosing an implementation substrate, this is the shape the workbook demands — five
responsibilities and the relationships between them:

```svg
<svg viewBox="0 0 1190 596" width="1190" xmlns="http://www.w3.org/2000/svg" font-family="inherit" role="img" aria-label="Intended AI4RnD product architecture">
<defs><marker id="ki" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="var(--subtle)"/></marker></defs>
<rect x="8" y="8" width="1174" height="92" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="30" font-size="12.5" font-weight="640" fill="var(--primary-ink)">Engagement — how people and signals reach the product, and how it reports back</text>
<rect x="40" y="40" width="250" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="165" y="59" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Channels · UI · CLI</text>
<text x="165" y="73" font-size="11" text-anchor="middle" fill="var(--muted)">requests · clues · material</text>
<rect x="330" y="40" width="250" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="455" y="59" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Project visibility</text>
<text x="455" y="73" font-size="11" text-anchor="middle" fill="var(--muted)">progress · gates · budgets</text>
<rect x="620" y="40" width="250" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="745" y="59" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Approvals</text>
<text x="745" y="73" font-size="11" text-anchor="middle" fill="var(--muted)">contracts · gates · improvements</text>
<rect x="910" y="40" width="240" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1030" y="59" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Accounts · configuration</text>
<text x="1030" y="73" font-size="11" text-anchor="middle" fill="var(--muted)">installers · settings</text>
<rect x="8" y="108" width="1174" height="116" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="130" font-size="12.5" font-weight="640" fill="var(--primary-ink)">Project control — one authority for meaning, readiness and completion</text>
<rect x="40" y="144" width="260" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="170" y="169" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Intention Compiler</text>
<text x="170" y="183" font-size="11" text-anchor="middle" fill="var(--muted)">need → confirmed Contract</text>
<rect x="340" y="144" width="260" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="470" y="162" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Planner</text>
<text x="470" y="176" font-size="11" text-anchor="middle" fill="var(--muted)">Contract → semantic TaskGraph</text>
<text x="470" y="190" font-size="11" text-anchor="middle" fill="var(--muted)">claims · dependencies · acceptance</text>
<rect x="640" y="144" width="240" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="760" y="162" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Readiness & run state</text>
<text x="760" y="176" font-size="11" text-anchor="middle" fill="var(--muted)">what may start · what truly</text>
<text x="760" y="190" font-size="11" text-anchor="middle" fill="var(--muted)">succeeded · repair & replan</text>
<rect x="920" y="144" width="230" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1035" y="162" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Gates & closure</text>
<text x="1035" y="176" font-size="11" text-anchor="middle" fill="var(--muted)">verdicts · delivery ·</text>
<text x="1035" y="190" font-size="11" text-anchor="middle" fill="var(--muted)">authorized distribution</text>
<rect x="8" y="232" width="1174" height="116" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="254" font-size="12.5" font-weight="640" fill="var(--primary-ink)">Capability & verification foundation — governed, versioned, improvable</text>
<rect x="40" y="268" width="300" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="190" y="286" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Capability Capsules</text>
<text x="190" y="300" font-size="11" text-anchor="middle" fill="var(--muted)">identity · contract · effects ·</text>
<text x="190" y="314" font-size="11" text-anchor="middle" fill="var(--muted)">compatibility · certification</text>
<rect x="380" y="268" width="250" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="505" y="286" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Logical Operators</text>
<text x="505" y="300" font-size="11" text-anchor="middle" fill="var(--muted)">stable callable actions</text>
<text x="505" y="314" font-size="11" text-anchor="middle" fill="var(--muted)">invoked by plan nodes</text>
<rect x="670" y="268" width="230" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="785" y="286" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Evaluator families</text>
<text x="785" y="300" font-size="11" text-anchor="middle" fill="var(--muted)">conformance · engineering · perf ·</text>
<text x="785" y="314" font-size="11" text-anchor="middle" fill="var(--muted)">security · factuality · human</text>
<rect x="940" y="268" width="210" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1045" y="286" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">GEPA + governed RSI</text>
<text x="1045" y="300" font-size="11" text-anchor="middle" fill="var(--muted)">candidates · budgets · frozen</text>
<text x="1045" y="314" font-size="11" text-anchor="middle" fill="var(--muted)">policy · approval · rollback</text>
<rect x="8" y="356" width="1174" height="104" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="378" font-size="12.5" font-weight="640" fill="var(--primary-ink)">Execution abstraction — the product never binds to one engine</text>
<rect x="40" y="388" width="540" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="310" y="413" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Logical Operator invocation → any qualified physical executor</text>
<text x="310" y="427" font-size="11" text-anchor="middle" fill="var(--muted)">agents · pipelines · staged workflows · teams · sandboxes · deterministic tools</text>
<rect x="620" y="388" width="530" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="885" y="413" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Binding rules</text>
<text x="885" y="427" font-size="11" text-anchor="middle" fill="var(--muted)">declared effects enforced · permitted/forbidden executors · honest stall</text>
<rect x="8" y="468" width="1174" height="104" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="490" font-size="12.5" font-weight="640" fill="var(--primary-ink)">Durable product state — outlives every session and run</text>
<rect x="40" y="500" width="270" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="175" y="523" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Project records</text>
<text x="175" y="537" font-size="11" text-anchor="middle" fill="var(--muted)">Contract & TaskGraph versions</text>
<rect x="350" y="500" width="270" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="485" y="523" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Evidence & verdict ledgers</text>
<text x="485" y="537" font-size="11" text-anchor="middle" fill="var(--muted)">append-only · attributed</text>
<rect x="660" y="500" width="240" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="780" y="516" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Knowledge graphs</text>
<text x="780" y="530" font-size="11" text-anchor="middle" fill="var(--muted)">concept · dataset · code · policy ·</text>
<text x="780" y="544" font-size="11" text-anchor="middle" fill="var(--muted)">workflow · trace · memory</text>
<rect x="940" y="500" width="210" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1045" y="516" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Improvement history</text>
<text x="1045" y="530" font-size="11" text-anchor="middle" fill="var(--muted)">versions · promotions ·</text>
<text x="1045" y="544" font-size="11" text-anchor="middle" fill="var(--muted)">rollbacks</text>
<path d="M165 84 L165 108" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ki)"/>
<path d="M470 84 L470 108" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ki)"/>
<path d="M760 84 L760 108" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ki)"/>
<path d="M1035 84 L1035 108" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ki)"/>
<path d="M170 200 L170 232" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ki)"/>
<path d="M470 200 L470 232" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ki)"/>
<path d="M760 200 L760 232" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ki)"/>
<path d="M1035 200 L1035 232" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ki)"/>
<path d="M310 324 L310 356" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ki)"/>
<path d="M885 324 L885 356" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ki)"/>
<path d="M310 444 L310 468" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#ki)"/>
<path d="M885 444 L885 468" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#ki)"/>
</svg>
```

Three structural commitments in this picture matter more than any component name:

- **One authority for meaning.** A single project-control layer decides what a request means,
  what work exists, what may start, what truly succeeded, and when the Contract is satisfied.
- **Capabilities are governed objects, not prompt files.** The capability layer owns identity,
  contracts, effects, compatibility and certification — and is itself the main subject of
  improvement.
- **Execution is an abstraction.** Plan nodes invoke Logical Operators; *which* physical
  executor serves an invocation is a binding decision under declared rules. The product never
  hard-couples to one engine — which is precisely what makes the JiuwenSwarm question answerable
  on evidence rather than on faith.

### 1.2 The user journey

```svg
<svg viewBox="0 0 1190 314" width="1190" xmlns="http://www.w3.org/2000/svg" font-family="inherit" role="img" aria-label="The user journey">
<defs><marker id="ahj" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="var(--subtle)"/></marker></defs>
<rect x="40" y="56" width="190" height="60" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="135.0" y="83" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">A need</text>
<text x="135.0" y="97" font-size="11" text-anchor="middle" fill="var(--muted)">question · clue · material</text>
<rect x="290" y="56" width="220" height="60" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="400.0" y="83" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Understand</text>
<text x="400.0" y="97" font-size="11" text-anchor="middle" fill="var(--muted)">mint the Research Contract</text>
<rect x="570" y="56" width="220" height="60" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="680.0" y="76" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Frame</text>
<text x="680.0" y="90" font-size="11" text-anchor="middle" fill="var(--muted)">mint falsifiable claims</text>
<text x="680.0" y="104" font-size="11" text-anchor="middle" fill="var(--muted)">and the plan</text>
<rect x="850" y="56" width="250" height="60" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="975.0" y="76" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Establish</text>
<text x="975.0" y="90" font-size="11" text-anchor="middle" fill="var(--muted)">build · benchmark · evaluate</text>
<text x="975.0" y="104" font-size="11" text-anchor="middle" fill="var(--muted)">mint verdicts</text>
<path d="M230 86 L290 86" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ahj)"/>
<path d="M510 86 L570 86" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ahj)"/>
<path d="M790 86 L850 86" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ahj)"/>
<path d="M975 56 L975 28 L680 28 L680 56" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ahj)"/>
<text x="827" y="22" font-size="11" text-anchor="middle" fill="var(--muted)">claim refuted — reframe honestly</text>
<rect x="290" y="216" width="220" height="60" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="400.0" y="236" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Deliver</text>
<text x="400.0" y="250" font-size="11" text-anchor="middle" fill="var(--muted)">the evidence-backed</text>
<text x="400.0" y="264" font-size="11" text-anchor="middle" fill="var(--muted)">deliverable</text>
<rect x="570" y="216" width="220" height="60" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="680.0" y="236" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Close & retain</text>
<text x="680.0" y="250" font-size="11" text-anchor="middle" fill="var(--muted)">freeze evidence ·</text>
<text x="680.0" y="264" font-size="11" text-anchor="middle" fill="var(--muted)">keep the knowledge</text>
<rect x="850" y="216" width="250" height="60" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="975.0" y="236" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Improve — governed</text>
<text x="975.0" y="250" font-size="11" text-anchor="middle" fill="var(--muted)">better capsules · prompts ·</text>
<text x="975.0" y="264" font-size="11" text-anchor="middle" fill="var(--muted)">routing · evaluators</text>
<path d="M940 116 L940 186 L400 186 L400 216" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ahj)"/>
<text x="668" y="178" font-size="11" text-anchor="middle" fill="var(--muted)">Contract satisfied — deliver</text>
<path d="M510 246 L570 246" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ahj)"/>
<path d="M790 246 L850 246" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#ahj)"/>
<text x="820" y="240" font-size="11" text-anchor="middle" fill="var(--muted)">run history</text>
<path d="M1010 216 L1010 146 L400 146 L400 116" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#ahj)"/>
<text x="668" y="140" font-size="11" text-anchor="middle" fill="var(--muted)">next runs start stronger — the loop outlives every journey</text>
</svg>
```

The journey begins when a need exists — a question, a qualified signal, or imported material —
and ends twice: for the requester, with an authorized, evidence-linked deliverable; for the
organization, with frozen evidence and retained knowledge. One loop deliberately outlives every
journey: governed improvement. The nine workbook lanes live inside these phases as individually
addressable capabilities — a literature-only project never builds a POC; a refuted claim
re-enters framing; lanes can run in parallel or recursively. A refuted hypothesis is a *success*
of the verification machinery, never a failure of the run.

### 1.3 Capability Capsules, precisely

The workbook's central capability idea is a five-level separation that survives every
architecture decision in this report:

| Level | What it is | Lifetime |
|---|---|---|
| **Capability Capsule** | governed, versioned, reusable capability identity | independent of any request |
| **Contract** | the promise for *this* request: scope, constraints, acceptance | one request |
| **TaskGraph** | the project-specific plan | one project |
| **Logical Operator** | a stable callable action a plan node invokes directly | independent |
| **Physical Operator** | the concrete executor | one binding |

```svg
<svg viewBox="0 0 1190 470" width="1190" xmlns="http://www.w3.org/2000/svg" font-family="inherit" role="img" aria-label="Capability Capsule anatomy">
<defs><marker id="kc" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="var(--subtle)"/></marker></defs>
<rect x="8" y="8" width="1174" height="220" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="30" font-size="12.5" font-weight="640" fill="var(--primary-ink)">One Capsule — a governed capability identity (all 42 existing manifests carry every section)</text>
<rect x="40" y="44" width="265" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="172" y="69" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Applicability</text>
<text x="172" y="83" font-size="11" text-anchor="middle" fill="var(--muted)">task types · positive and negative signals</text>
<rect x="325" y="44" width="265" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="458" y="69" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Typed contract</text>
<text x="458" y="83" font-size="11" text-anchor="middle" fill="var(--muted)">inputs · outputs · pre/postconditions · invariants</text>
<rect x="610" y="44" width="265" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="742" y="69" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Declared effects</text>
<text x="742" y="83" font-size="11" text-anchor="middle" fill="var(--muted)">read · write · execute · network · cost · risk</text>
<rect x="895" y="44" width="265" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1028" y="69" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Composition</text>
<text x="1028" y="83" font-size="11" text-anchor="middle" fill="var(--muted)">consumes · produces · compatible · incompatible · ordering</text>
<rect x="40" y="110" width="265" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="172" y="135" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Executor compatibility</text>
<text x="172" y="149" font-size="11" text-anchor="middle" fill="var(--muted)">permitted and forbidden physical operators</text>
<rect x="325" y="110" width="265" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="458" y="135" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Verification</text>
<text x="458" y="149" font-size="11" text-anchor="middle" fill="var(--muted)">self-check · external verifier · pass conditions</text>
<rect x="610" y="110" width="265" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="742" y="135" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Provenance & certification</text>
<text x="742" y="149" font-size="11" text-anchor="middle" fill="var(--muted)">owner · origin · certified status</text>
<rect x="895" y="110" width="265" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1028" y="140" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Versions & history</text>
<text x="1028" y="154" font-size="11" text-anchor="middle" fill="var(--muted)">lifecycle · evaluation & performance record</text>
<text x="1153" y="122" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--blocked)">TO ADD</text>
<text x="600" y="200" font-size="11" text-anchor="middle" fill="var(--muted)">Plan nodes call Logical Operators directly; the Capsule governs which executor may serve them, under which effects, verified by whom — it never hides the plan.</text>
<rect x="8" y="268" width="1174" height="120" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="290" font-size="12.5" font-weight="640" fill="var(--primary-ink)">Execution bindings beneath the Capsule — implementation detail, never identity</text>
<rect x="40" y="306" width="208" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="144" y="329" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Skills</text>
<text x="144" y="343" font-size="11" text-anchor="middle" fill="var(--muted)">prompt packages</text>
<rect x="268" y="306" width="208" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="372" y="329" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Tools & MCP</text>
<text x="372" y="343" font-size="11" text-anchor="middle" fill="var(--muted)">typed calls</text>
<rect x="496" y="306" width="208" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="600" y="329" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Agents & teams</text>
<text x="600" y="343" font-size="11" text-anchor="middle" fill="var(--muted)">DeepAgent · Team</text>
<rect x="724" y="306" width="208" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="828" y="329" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Models</text>
<text x="828" y="343" font-size="11" text-anchor="middle" fill="var(--muted)">pool entries</text>
<rect x="952" y="306" width="208" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1056" y="329" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Data & secrets</text>
<text x="1056" y="343" font-size="11" text-anchor="middle" fill="var(--muted)">refs, never inline</text>
<path d="M600 228 L600 268" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kc)"/>
<text x="612" y="252" font-size="11" text-anchor="start" fill="var(--muted)">binds to — replaceable without changing the Capsule</text>
<rect x="8" y="404" width="1174" height="54" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="600" y="436" font-size="11" text-anchor="middle" fill="var(--muted)">A JiuwenSwarm skill is one possible binding. It has a name, a description and a prompt — none of the eight governed sections above. The Capsule is the product object; bindings are parts.</text>
</svg>
```

All 42 capsule manifests in the current repository already carry every governed section
(**EXEC** — parsed in this analysis; registry: 35 entries, 30 stable). What the schema does not
yet carry — versions, evaluation history, RSI targets — is named work in §8, not a redefinition.
Skills, tools, agents, workflows, models and APIs are **bindings beneath a Capsule**; replacing
a binding never changes the Capsule's identity or governance.

---

## 2. What exists today

Two honest as-is pictures, kept deliberately separate from the target. Nothing in this section
is design; every status is verified.

### 2.1 Current AI4RnD

```svg
<svg viewBox="0 0 1190 560" width="1190" xmlns="http://www.w3.org/2000/svg" font-family="inherit" role="img" aria-label="Current AI4RnD implementation, as verified">
<defs><marker id="ka" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="var(--subtle)"/></marker></defs>
<rect x="8" y="8" width="1174" height="88" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="30" font-size="12.5" font-weight="640" fill="var(--primary-ink)">Carrier — how it runs today</text>
<rect x="40" y="40" width="300" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="190" y="64" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">tmux cockpit + polling coordinator</text>
<text x="190" y="78" font-size="11" text-anchor="middle" fill="var(--muted)">shell state machine drives panes</text>
<text x="333" y="52" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--blocked)">ACTIVE · REJECTED IN TARGET</text>
<rect x="380" y="40" width="360" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="560" y="64" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">graph_scheduler (4,189 lines)</text>
<text x="560" y="78" font-size="11" text-anchor="middle" fill="var(--muted)">readiness · batching · retries · binding, fused with plan semantics</text>
<text x="733" y="52" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--blocked)">ACTIVE · RETIRES</text>
<rect x="780" y="40" width="370" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="965" y="64" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">TaskGraph persistence</text>
<text x="965" y="78" font-size="11" text-anchor="middle" fill="var(--muted)">task_graph_io · state_io</text>
<text x="1143" y="52" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">ACTIVE</text>
<rect x="8" y="104" width="1174" height="88" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="126" font-size="12.5" font-weight="640" fill="var(--primary-ink)">Research pipeline</text>
<rect x="40" y="136" width="270" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="175" y="160" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Sources & extractors</text>
<text x="175" y="174" font-size="11" text-anchor="middle" fill="var(--muted)">arXiv · HF · GitHub · YouTube</text>
<text x="303" y="148" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">ACTIVE</text>
<rect x="350" y="136" width="250" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="475" y="160" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Survey & claim compiler</text>
<text x="475" y="174" font-size="11" text-anchor="middle" fill="var(--muted)">planner · sections · claims</text>
<text x="593" y="148" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">ACTIVE</text>
<rect x="640" y="136" width="250" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="765" y="160" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Grounding check</text>
<text x="765" y="174" font-size="11" text-anchor="middle" fill="var(--muted)">measured 0.25 precision</text>
<text x="883" y="148" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">BROKEN</text>
<rect x="930" y="136" width="220" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1040" y="160" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Report capsules</text>
<text x="1040" y="174" font-size="11" text-anchor="middle" fill="var(--muted)">plan · draft · publish</text>
<text x="1143" y="148" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">ACTIVE</text>
<rect x="8" y="200" width="1174" height="88" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="222" font-size="12.5" font-weight="640" fill="var(--primary-ink)">Governance assets — the parts the target keeps</text>
<rect x="40" y="232" width="250" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="165" y="256" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Evidence ledger</text>
<text x="165" y="270" font-size="11" text-anchor="middle" fill="var(--muted)">citation spans, runs standalone</text>
<text x="283" y="244" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">ACTIVE</text>
<rect x="330" y="232" width="250" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="455" y="256" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Gate ledger</text>
<text x="455" y="270" font-size="11" text-anchor="middle" fill="var(--muted)">append-only · writer-attributed</text>
<text x="573" y="244" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">ACTIVE</text>
<rect x="620" y="232" width="250" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="745" y="256" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Capsule registry</text>
<text x="745" y="270" font-size="11" text-anchor="middle" fill="var(--muted)">42 manifests · 35 registered</text>
<text x="863" y="244" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--blocked)">ACTIVE / UNWIRED</text>
<rect x="910" y="232" width="240" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1030" y="256" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">GEPA optimizer</text>
<text x="1030" y="270" font-size="11" text-anchor="middle" fill="var(--muted)">budgets · frozen policy · promote</text>
<text x="1143" y="244" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--blocked)">ACTIVE / UNWIRED</text>
<rect x="8" y="296" width="1174" height="108" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="318" font-size="12.5" font-weight="640" fill="var(--primary-ink)">Implemented but not connected</text>
<rect x="40" y="332" width="260" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="170" y="358" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Benchmark suites</text>
<text x="170" y="372" font-size="11" text-anchor="middle" fill="var(--muted)">no lane invokes them</text>
<text x="293" y="344" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--blocked)">UNWIRED</text>
<rect x="340" y="332" width="280" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="480" y="352" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Capsule → runner bindings</text>
<text x="480" y="365" font-size="11" text-anchor="middle" fill="var(--muted)">operator_compatibility declared,</text>
<text x="480" y="378" font-size="11" text-anchor="middle" fill="var(--muted)">no binder consumes it</text>
<text x="613" y="344" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--blocked)">UNWIRED</text>
<rect x="660" y="332" width="230" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="775" y="358" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Operator profiles</text>
<text x="775" y="372" font-size="11" text-anchor="middle" fill="var(--muted)">agent-actors config only</text>
<text x="883" y="344" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--blocked)">SPECIFIED</text>
<rect x="930" y="332" width="220" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1040" y="358" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Intent engine adapter</text>
<text x="1040" y="372" font-size="11" text-anchor="middle" fill="var(--muted)">routing shell hooks</text>
<text x="1143" y="344" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--blocked)">UNWIRED</text>
<rect x="8" y="412" width="1174" height="116" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="434" font-size="12.5" font-weight="640" fill="var(--primary-ink)">Absent — verified by exhaustive search</text>
<rect x="40" y="448" width="208" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)" stroke-dasharray="4 3"/>
<text x="144" y="474" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Idea Card</text>
<text x="144" y="488" font-size="11" text-anchor="middle" fill="var(--muted)">no schema anywhere</text>
<text x="241" y="460" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">ABSENT</text>
<rect x="268" y="448" width="208" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)" stroke-dasharray="4 3"/>
<text x="372" y="474" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Falsifiability stage</text>
<text x="372" y="488" font-size="11" text-anchor="middle" fill="var(--muted)">2 mentions, no gate</text>
<text x="469" y="460" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">ABSENT</text>
<rect x="496" y="448" width="208" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)" stroke-dasharray="4 3"/>
<text x="600" y="474" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Typed knowledge graphs</text>
<text x="600" y="488" font-size="11" text-anchor="middle" fill="var(--muted)">all seven missing</text>
<text x="697" y="460" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">ABSENT</text>
<rect x="724" y="448" width="208" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)" stroke-dasharray="4 3"/>
<text x="828" y="474" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Account subsystem</text>
<text x="828" y="488" font-size="11" text-anchor="middle" fill="var(--muted)">none</text>
<text x="925" y="460" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">ABSENT</text>
<rect x="952" y="448" width="208" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)" stroke-dasharray="4 3"/>
<text x="1056" y="474" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">RSI governance loop</text>
<text x="1056" y="488" font-size="11" text-anchor="middle" fill="var(--muted)">no proposals · no inbox</text>
<text x="1153" y="460" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">ABSENT</text>
</svg>
```

The reading: AI4RnD's *governance assets are real* — the evidence ledger, gate ledger, capsule
registry and GEPA optimizer all exist and mostly run (**EXEC/SRC**) — while its *carrier* is a
tmux cockpit driven by a polling shell script, its scheduler fuses plan semantics with 4,189
lines of physical scheduling, its central grounding check measured **0.25 precision** on a
labelled set (**EXEC**), and the knowledge layer, Idea Card, falsifiability stage, accounts and
RSI governance are absent (**EXEC** — exhaustive searches). GEPA deserves emphasis because
earlier revisions under-weighted it: it is 3,540 lines with unit tests, a typed candidate
envelope covering skills, capsules, routing policies, rewrite rules and cost models, budget
stoppers, a frozen-policy checker, and a checksummed, atomic, rollback-capable promoter whose
CLI defaults to dry-run (**SRC**).

### 2.2 Current JiuwenSwarm and OpenJiuwen

```svg
<svg viewBox="0 0 1190 520" width="1190" xmlns="http://www.w3.org/2000/svg" font-family="inherit" role="img" aria-label="JiuwenSwarm and OpenJiuwen, as verified">
<defs><marker id="kf" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="var(--subtle)"/></marker></defs>
<rect x="8" y="8" width="1174" height="88" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="30" font-size="12.5" font-weight="640" fill="var(--primary-ink)">Clients</text>
<rect x="40" y="40" width="250" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="165" y="66" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Web UI · TUI · CLI</text>
<rect x="330" y="40" width="300" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="480" y="59" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">9 messaging channels</text>
<text x="480" y="73" font-size="11" text-anchor="middle" fill="var(--muted)">incl. WeChat · Discord</text>
<rect x="670" y="40" width="250" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="795" y="66" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Agent-to-agent peers</text>
<rect x="8" y="104" width="1174" height="96" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="126" font-size="12.5" font-weight="640" fill="var(--primary-ink)">JiuwenSwarm — application layer</text>
<rect x="40" y="140" width="270" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="175" y="161" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Gateway</text>
<text x="175" y="175" font-size="11" text-anchor="middle" fill="var(--muted)">channel adapters · routing</text>
<rect x="350" y="140" width="270" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="485" y="161" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Agent server</text>
<text x="485" y="175" font-size="11" text-anchor="middle" fill="var(--muted)">sessions · modes · skills</text>
<rect x="660" y="140" width="230" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="775" y="166" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Skill retrieval</text>
<text x="775" y="180" font-size="11" text-anchor="middle" fill="var(--muted)">ranks — never refuses</text>
<text x="883" y="152" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--blocked)">GAP FOR RESEARCH</text>
<rect x="930" y="140" width="220" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1040" y="161" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Workspace & config</text>
<text x="1040" y="175" font-size="11" text-anchor="middle" fill="var(--muted)">templates · settings</text>
<rect x="8" y="208" width="1174" height="148" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="230" font-size="12.5" font-weight="640" fill="var(--primary-ink)">OpenJiuwen — runtime library</text>
<rect x="40" y="240" width="210" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="145" y="261" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">DeepAgent</text>
<text x="145" y="275" font-size="11" text-anchor="middle" fill="var(--muted)">single-agent turns</text>
<rect x="280" y="240" width="230" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="395" y="254" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Core Workflow</text>
<text x="395" y="268" font-size="11" text-anchor="middle" fill="var(--muted)">durable staged graphs,</text>
<text x="395" y="282" font-size="11" text-anchor="middle" fill="var(--muted)">checkpoints · interrupts</text>
<rect x="540" y="240" width="230" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="655" y="254" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">SwarmFlow</text>
<text x="655" y="268" font-size="11" text-anchor="middle" fill="var(--muted)">scripted pipelines,</text>
<text x="655" y="282" font-size="11" text-anchor="middle" fill="var(--muted)">replayable journal</text>
<rect x="800" y="240" width="170" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="885" y="261" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Dynamic Team</text>
<text x="885" y="275" font-size="11" text-anchor="middle" fill="var(--muted)">leader + roster</text>
<rect x="1000" y="240" width="150" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1075" y="261" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Code mode</text>
<text x="1075" y="275" font-size="11" text-anchor="middle" fill="var(--muted)">worktrees</text>
<rect x="40" y="300" width="280" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="180" y="314" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Team services</text>
<text x="180" y="328" font-size="11" text-anchor="middle" fill="var(--muted)">task board with dependencies ·</text>
<text x="180" y="342" font-size="11" text-anchor="middle" fill="var(--muted)">shared memory · reliability detectors</text>
<rect x="360" y="300" width="280" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="500" y="320" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">agent_evolving</text>
<text x="500" y="333" font-size="11" text-anchor="middle" fill="var(--muted)">Trainer · Updater · metrics · RL —</text>
<text x="500" y="346" font-size="11" text-anchor="middle" fill="var(--muted)">one wired subject today</text>
<text x="633" y="312" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--blocked)">NARROWLY WIRED</text>
<rect x="680" y="300" width="240" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="800" y="326" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Model pool + allocator</text>
<text x="800" y="340" font-size="11" text-anchor="middle" fill="var(--muted)">silent fallback on unknown name</text>
<text x="913" y="312" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">DEFECT</text>
<rect x="950" y="300" width="200" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1050" y="326" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Graph memory</text>
<text x="1050" y="340" font-size="11" text-anchor="middle" fill="var(--muted)">unreferenced by the app</text>
<text x="1143" y="312" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--blocked)">UNWIRED</text>
<rect x="8" y="364" width="1174" height="92" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="386" font-size="12.5" font-weight="640" fill="var(--primary-ink)">Shared infrastructure</text>
<rect x="40" y="396" width="260" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="170" y="415" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Checkpointer</text>
<text x="170" y="429" font-size="11" text-anchor="middle" fill="var(--muted)">sqlite, process default</text>
<rect x="340" y="396" width="260" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="470" y="415" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">jiuwenbox sandbox</text>
<text x="470" y="429" font-size="11" text-anchor="middle" fill="var(--muted)">bwrap / cgroups</text>
<rect x="640" y="396" width="240" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="760" y="415" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Observability</text>
<text x="760" y="429" font-size="11" text-anchor="middle" fill="var(--muted)">spans · progress events</text>
<rect x="920" y="396" width="230" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1035" y="420" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Guardrail rules tier</text>
<text x="1035" y="434" font-size="11" text-anchor="middle" fill="var(--muted)">loads 0 rules — orphaned file</text>
<text x="1143" y="408" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">DEFECT</text>
<rect x="8" y="464" width="1174" height="48" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="600" y="492" font-size="11" text-anchor="middle" fill="var(--muted)">Verified defects that shape the integration: silent model substitution · resume advertised but rejected · failed steps return empty and the run reports success · executor typing accepted but unread</text>
<path d="M165 84 L165 104" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kf)"/>
<path d="M480 84 L480 104" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kf)"/>
<path d="M795 84 L795 104" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kf)"/>
<path d="M175 188 L175 208" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kf)"/>
<path d="M485 188 L485 208" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kf)"/>
<path d="M775 188 L775 208" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kf)"/>
<path d="M1040 188 L1040 208" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kf)"/>
<path d="M170 356 L170 364" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kf)"/>
<path d="M470 356 L470 364" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kf)"/>
<path d="M760 356 L760 364" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kf)"/>
<path d="M1035 356 L1035 364" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kf)"/>
</svg>
```

The foundation is substantial and much of it is verified by execution: durable staged graphs
with runtime-computed fan-out (**EXEC**), a scripted pipeline engine whose journal replays
interrupted runs re-executing only the failed step (**EXEC**), admission control that refuses
rather than queues silently (**EXEC**), a persistent sqlite checkpointer in a stock install
(**SRC**), a team task board with real dependency edges, reliability anomaly detectors and
remediation, shared team memory, sandboxing, nine channels and a web UI (**SRC**).

Four verified gaps shape the integration, and one pattern explains why reading source is not
enough here: **this codebase fails loudly on typos and silently on unimplemented features.**

| # | Verified gap | Class |
|---|---|---|
| 1 | An unknown model name silently resolves to the default worker model — no error, no warning | SRC |
| 2 | The agent-facing pipeline tool advertises `resume_id` and rejects it: "not supported yet"; resume exists only as an internal control-plane call | EXEC |
| 3 | A step that fails all its retries returns an empty result and the run reports success | EXEC |
| 4 | The executor-typing option is validated and forwarded, but no backend reads it | EXEC |
| 5 | The built-in shell-guardrail tier loads zero rules; the rules file the installer writes is read by nothing | EXEC |
| 6 | The evolution trainer accepts exactly one subject class in the entire runtime; the application imports only its archive and tool-description parts | EXEC |

---

## 3. The recommended integration, and why

Five coherent complete-product options were evaluated. Execution mechanisms — DeepAgent,
SwarmFlow, Core Workflow, Dynamic Team — are not among them: each implements 0 of the 142
outcomes alone and appears *inside* every option as machinery.

| Option | In one line | Verdict |
|---|---|---|
| **A** — AI4RnD-led control plane | keep AI4RnD's scheduler; Jiuwen replaces only physical executors | complete, but pays a permanent duplicate-scheduler tax against engines verified to work |
| **B** — Jiuwen-native lifecycle | delegate sequencing, checkpoints and human turns to the runtime now | right destination, wrong commitment schedule — deletes fallbacks on the strength of *reading* |
| **C** — progressive compilation ★ | B's destination, reached one capability at a time, each retirement gated by a passing test | **recommended** |
| **D** — full delegation now | remove AI4RnD's execution machinery immediately | **fails the preservation gate today** — silent model substitution would drop Model Routing & Selection with no layer left to catch it |
| **E** — standalone / defer | keep the tmux-carried system as is | preserves the most, gains nothing, leaves ~50 never-built outcomes unbuilt |

The preservation gate evaluates all 142 outcomes under every option
([full row-level CSV](traceability/142-feature-preservation-gate.csv)):

| Verdict | A | B | C ★ | D | E |
|---|---:|---:|---:|---:|---:|
| PRESERVED | 71 | 78 | 78 | 59 | 84 |
| PRESERVED WITH ADAPTATION | 13 | 6 | 6 | 24 | 0 |
| NEW BUILD REQUIRED | 56 | 56 | 56 | 55 | 56 |
| UNRESOLVED | 2 | 2 | 2 | 3 | 2 |
| **DROPPED** | **0** | **0** | **0** | **1** | **0** |

Two facts decide it. First, the big number barely moves: ~56 outcomes need new construction
under *every* option, because they exist in neither system — no architecture choice avoids
them. Second, only D drops an outcome today. **That failure is evidence against immediate full
delegation, not proof that full delegation can never become safe**: every blocking gap in §2.2
is small and fixable, and when they close upstream, C's mature form *is* D. C differs from B
only in *when* each fallback dies — after a named, falsifiable test rather than on a schedule.
Given that this analysis's execution probes repeatedly caught source-reading overstating what is
reachable, that difference is worth having.

**Progressive compilation remains the recommendation.**

### 3.1 The target architecture

```svg
<svg viewBox="0 0 1190 600" width="1190" xmlns="http://www.w3.org/2000/svg" font-family="inherit" role="img" aria-label="Target integrated architecture with sourcing decisions">
<defs><marker id="kt" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="var(--subtle)"/></marker></defs>
<rect x="8" y="8" width="1174" height="96" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="30" font-size="12.5" font-weight="640" fill="var(--primary-ink)">JiuwenSwarm — application foundation</text>
<rect x="40" y="42" width="240" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="160" y="73" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Channels · Gateway</text>
<text x="273" y="54" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">REUSE</text>
<rect x="320" y="42" width="240" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="440" y="73" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Sessions · workspace</text>
<text x="553" y="54" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">REUSE</text>
<rect x="600" y="42" width="250" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="725" y="73" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">UI shell · config · packaging</text>
<text x="843" y="54" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">REUSE + EXTEND</text>
<rect x="890" y="42" width="260" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1020" y="66" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Project & registry views</text>
<text x="1020" y="80" font-size="11" text-anchor="middle" fill="var(--muted)">approvals · improvements inbox</text>
<text x="1143" y="54" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">BUILD</text>
<rect x="8" y="112" width="1174" height="116" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="134" font-size="12.5" font-weight="640" fill="var(--primary-ink)">AI4RnD — product core (permanent)</text>
<rect x="40" y="146" width="250" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="165" y="176" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Project subsystem</text>
<text x="165" y="190" font-size="11" text-anchor="middle" fill="var(--muted)">Contract & TaskGraph versions</text>
<text x="283" y="158" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">BUILD</text>
<rect x="330" y="146" width="250" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="455" y="176" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Intention Compiler · Planner</text>
<text x="455" y="190" font-size="11" text-anchor="middle" fill="var(--muted)">ported research semantics</text>
<text x="573" y="158" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">PORT + ADAPT</text>
<rect x="620" y="146" width="250" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="745" y="176" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Capsules · Logical Operators</text>
<text x="745" y="190" font-size="11" text-anchor="middle" fill="var(--muted)">registry · certification · effects</text>
<text x="863" y="158" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">PORT + EXTEND</text>
<rect x="910" y="146" width="240" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1030" y="176" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Evidence · gates · evaluators</text>
<text x="1030" y="190" font-size="11" text-anchor="middle" fill="var(--muted)">entailment rebuilt & measured</text>
<text x="1143" y="158" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">PORT + BUILD</text>
<rect x="8" y="236" width="1174" height="116" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="258" font-size="12.5" font-weight="640" fill="var(--primary-ink)">Integration bridge — the only bilingual component</text>
<rect x="40" y="270" width="260" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="170" y="294" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Binding</text>
<text x="170" y="307" font-size="11" text-anchor="middle" fill="var(--muted)">capsule + executor + model,</text>
<text x="170" y="320" font-size="11" text-anchor="middle" fill="var(--muted)">honest stall — never substitutes</text>
<text x="293" y="282" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">BUILD</text>
<rect x="340" y="270" width="250" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="465" y="294" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Compiler & dispatch</text>
<text x="465" y="307" font-size="11" text-anchor="middle" fill="var(--muted)">ready sub-plan → engine spec,</text>
<text x="465" y="320" font-size="11" text-anchor="middle" fill="var(--muted)">resume · cancel</text>
<text x="583" y="282" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">BUILD</text>
<rect x="630" y="270" width="250" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="755" y="294" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Receipt builder</text>
<text x="755" y="307" font-size="11" text-anchor="middle" fill="var(--muted)">typed receipts + provenance,</text>
<text x="755" y="320" font-size="11" text-anchor="middle" fill="var(--muted)">empty result ⇒ failed attempt</text>
<text x="873" y="282" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">BUILD</text>
<rect x="920" y="270" width="230" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1035" y="294" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Engine adapters</text>
<text x="1035" y="307" font-size="11" text-anchor="middle" fill="var(--muted)">SwarmFlow backend seam ·</text>
<text x="1035" y="320" font-size="11" text-anchor="middle" fill="var(--muted)">workflow components</text>
<text x="1143" y="282" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">COMPOSE</text>
<rect x="8" y="360" width="1174" height="108" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="382" font-size="12.5" font-weight="640" fill="var(--primary-ink)">OpenJiuwen — execution engines</text>
<rect x="40" y="392" width="250" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="165" y="427" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Core Workflow / Pregel</text>
<text x="283" y="404" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">REUSE</text>
<rect x="320" y="392" width="220" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="430" y="420" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">SwarmFlow engine</text>
<text x="430" y="434" font-size="11" text-anchor="middle" fill="var(--muted)">via its backend seam</text>
<text x="533" y="404" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">REUSE</text>
<rect x="570" y="392" width="250" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="695" y="420" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">DeepAgent · Team · worktrees</text>
<text x="695" y="434" font-size="11" text-anchor="middle" fill="var(--muted)">task board · reliability · memory</text>
<text x="813" y="404" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">REUSE</text>
<rect x="850" y="392" width="150" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="925" y="427" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Model routing</text>
<text x="993" y="404" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--blocked)">ADAPTER</text>
<rect x="1030" y="392" width="120" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1090" y="427" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Sandbox</text>
<text x="1143" y="404" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">REUSE</text>
<rect x="8" y="476" width="1174" height="112" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="498" font-size="12.5" font-weight="640" fill="var(--primary-ink)">Durable product state — AI4RnD-owned, project-scoped</text>
<path d="M40 516 a 120.0 8 0 0 1 240 0 v 36 a 120.0 8 0 0 1 -240 0 z" fill="var(--surface)" stroke="var(--line-strong)"/>
<path d="M40 516 a 120.0 8 0 0 0 240 0" fill="none" stroke="var(--line-strong)"/>
<text x="160" y="538" font-size="11" text-anchor="middle" font-weight="640" fill="var(--ink)">Project store</text>
<text x="160" y="550" font-size="11" text-anchor="middle" fill="var(--muted)">Contracts · plans · budgets</text>
<path d="M320 516 a 125.0 8 0 0 1 250 0 v 36 a 125.0 8 0 0 1 -250 0 z" fill="var(--surface)" stroke="var(--line-strong)"/>
<path d="M320 516 a 125.0 8 0 0 0 250 0" fill="none" stroke="var(--line-strong)"/>
<text x="445" y="538" font-size="11" text-anchor="middle" font-weight="640" fill="var(--ink)">Attempt lineage</text>
<text x="445" y="550" font-size="11" text-anchor="middle" fill="var(--muted)">receipts · cancels · provenance</text>
<path d="M610 516 a 120.0 8 0 0 1 240 0 v 36 a 120.0 8 0 0 1 -240 0 z" fill="var(--surface)" stroke="var(--line-strong)"/>
<path d="M610 516 a 120.0 8 0 0 0 240 0" fill="none" stroke="var(--line-strong)"/>
<text x="730" y="538" font-size="11" text-anchor="middle" font-weight="640" fill="var(--ink)">Evidence & verdicts</text>
<text x="730" y="550" font-size="11" text-anchor="middle" fill="var(--muted)">append-only</text>
<path d="M890 516 a 130.0 8 0 0 1 260 0 v 36 a 130.0 8 0 0 1 -260 0 z" fill="var(--surface)" stroke="var(--line-strong)"/>
<path d="M890 516 a 130.0 8 0 0 0 260 0" fill="none" stroke="var(--line-strong)"/>
<text x="1020" y="538" font-size="11" text-anchor="middle" font-weight="640" fill="var(--ink)">Knowledge & improvements</text>
<text x="1020" y="550" font-size="11" text-anchor="middle" fill="var(--muted)">projections · versions</text>
<path d="M165 86 L165 112" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kt)"/>
<path d="M445 86 L445 112" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kt)"/>
<path d="M745 86 L745 112" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kt)"/>
<path d="M1020 86 L1020 112" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kt)"/>
<path d="M170 202 L170 236" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kt)"/>
<path d="M455 202 L455 236" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kt)"/>
<path d="M745 202 L745 236" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kt)"/>
<path d="M1030 202 L1030 236" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kt)"/>
<path d="M170 326 L170 360" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kt)"/>
<path d="M465 326 L465 360" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kt)"/>
<path d="M755 326 L755 360" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kt)"/>
<path d="M1035 326 L1035 360" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kt)"/>
<path d="M160 444 L160 476" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#kt)"/>
<path d="M430 444 L430 476" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#kt)"/>
<path d="M700 444 L700 476" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#kt)"/>
<path d="M1020 444 L1020 476" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#kt)"/>
<g font-size="11" fill="var(--muted)"><line x1="24" y1="586" x2="62" y2="586" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kt)"/><text x="70" y="590">control</text><line x1="146" y1="586" x2="184" y2="586" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#kt)"/><text x="192" y="590">state & evidence</text><text x="322" y="590">tags: REUSE · COMPOSE (adapter) · EXTEND · PORT · ADAPT · BUILD</text></g>
</svg>
```

The bridge is the only bilingual component: plan nodes, capability requirements and gate policy
on one side; engine specifications, agent calls and worktrees on the other. It is forbidden to
make semantic decisions — it translates them. Each box carries its sourcing decision from the
component audit (§7).

---

## 4. How the complete product works, end to end

The one picture to hold. Solid arrows are control and execution; dashed arrows are state,
evidence and improvement. The semantic TaskGraph defines *what must happen*; engine
specifications define *how ready work runs*.

```svg
<svg viewBox="0 0 1190 768" width="1190" xmlns="http://www.w3.org/2000/svg" font-family="inherit" role="img" aria-label="End-to-end functional architecture">
<defs><marker id="km" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="var(--subtle)"/></marker></defs>
<rect x="126" y="8" width="1056" height="70" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<rect x="8" y="8" width="112" height="70" rx="8" fill="var(--surface-quiet)" stroke="var(--line)"/>
<text x="20" y="30" font-size="10.5" fill="var(--subtle)">People &</text>
<text x="20" y="44" font-size="10.5" fill="var(--subtle)">channels</text>
<rect x="126" y="86" width="1056" height="186" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<rect x="8" y="86" width="112" height="186" rx="8" fill="var(--surface-quiet)" stroke="var(--line)"/>
<text x="20" y="108" font-size="10.5" fill="var(--subtle)">Project control</text>
<text x="20" y="122" font-size="10.5" fill="var(--subtle)">— AI4RnD</text>
<rect x="126" y="280" width="1056" height="80" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<rect x="8" y="280" width="112" height="80" rx="8" fill="var(--surface-quiet)" stroke="var(--line)"/>
<text x="20" y="302" font-size="10.5" fill="var(--subtle)">Capability</text>
<text x="20" y="316" font-size="10.5" fill="var(--subtle)">governance</text>
<text x="20" y="330" font-size="10.5" fill="var(--subtle)">— AI4RnD</text>
<rect x="126" y="368" width="1056" height="96" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<rect x="8" y="368" width="112" height="96" rx="8" fill="var(--surface-quiet)" stroke="var(--line)"/>
<text x="20" y="390" font-size="10.5" fill="var(--subtle)">Integration</text>
<text x="20" y="404" font-size="10.5" fill="var(--subtle)">bridge</text>
<rect x="126" y="472" width="1056" height="84" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<rect x="8" y="472" width="112" height="84" rx="8" fill="var(--surface-quiet)" stroke="var(--line)"/>
<text x="20" y="494" font-size="10.5" fill="var(--subtle)">Execution</text>
<text x="20" y="508" font-size="10.5" fill="var(--subtle)">— OpenJiuwen</text>
<rect x="126" y="564" width="1056" height="168" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<rect x="8" y="564" width="112" height="168" rx="8" fill="var(--surface-quiet)" stroke="var(--line)"/>
<text x="20" y="586" font-size="10.5" fill="var(--subtle)">Durable product</text>
<text x="20" y="600" font-size="10.5" fill="var(--subtle)">state — AI4RnD</text>
<rect x="226" y="24" width="220" height="40" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="336" y="48" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Researcher · teams</text>
<rect x="486" y="24" width="230" height="40" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="601" y="48" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Channels · Web UI · CLI</text>
<rect x="900" y="24" width="250" height="40" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1025" y="48" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Approvals & stall resolution</text>
<rect x="146" y="104" width="200" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="246" y="127" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Project</text>
<text x="246" y="141" font-size="11" text-anchor="middle" fill="var(--muted)">create — or retrieve & resume</text>
<rect x="386" y="104" width="220" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="496" y="127" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Intention → Contract v1</text>
<text x="496" y="141" font-size="11" text-anchor="middle" fill="var(--muted)">ambiguity resolved · confirmed</text>
<rect x="646" y="104" width="230" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="761" y="127" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Planner → TaskGraph vN</text>
<text x="761" y="141" font-size="11" text-anchor="middle" fill="var(--muted)">claims · deps · acceptance</text>
<rect x="886" y="104" width="200" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="986" y="127" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Semantic readiness</text>
<text x="986" y="141" font-size="11" text-anchor="middle" fill="var(--muted)">deps · budget · scope</text>
<rect x="146" y="200" width="220" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="256" y="223" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Close & deliver</text>
<text x="256" y="237" font-size="11" text-anchor="middle" fill="var(--muted)">freeze · authorize</text>
<rect x="646" y="200" width="230" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="761" y="223" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Repair · replan → vN+1</text>
<text x="761" y="237" font-size="11" text-anchor="middle" fill="var(--muted)">artifact fix, or plan revision</text>
<rect x="906" y="200" width="200" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1006" y="223" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Gates</text>
<text x="1006" y="237" font-size="11" text-anchor="middle" fill="var(--muted)">verdict per claim</text>
<rect x="146" y="300" width="340" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="316" y="323" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Capability Capsules · Logical Operators</text>
<text x="316" y="337" font-size="11" text-anchor="middle" fill="var(--muted)">registry · versions · effects · compatibility</text>
<rect x="546" y="300" width="300" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="696" y="323" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Evaluator families & gate policy</text>
<text x="696" y="337" font-size="11" text-anchor="middle" fill="var(--muted)">writer ≠ verifier</text>
<rect x="146" y="392" width="250" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="271" y="410" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Binding</text>
<text x="271" y="424" font-size="11" text-anchor="middle" fill="var(--muted)">capsule + executor + model —</text>
<text x="271" y="438" font-size="11" text-anchor="middle" fill="var(--muted)">stall if nothing qualifies</text>
<rect x="446" y="392" width="220" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="556" y="417" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Compile & dispatch</text>
<text x="556" y="431" font-size="11" text-anchor="middle" fill="var(--muted)">ready sub-plan → engine spec</text>
<rect x="716" y="392" width="300" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="866" y="410" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Receipt builder</text>
<text x="866" y="424" font-size="11" text-anchor="middle" fill="var(--muted)">typed receipt + provenance —</text>
<text x="866" y="438" font-size="11" text-anchor="middle" fill="var(--muted)">an empty result is a failed attempt</text>
<rect x="146" y="492" width="600" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="446" y="518" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Core Workflow · SwarmFlow · DeepAgent · Team · worktrees</text>
<rect x="796" y="492" width="280" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="936" y="518" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">External models · tools · sources</text>
<path d="M146 604 a 105.0 8 0 0 1 210 0 v 36 a 105.0 8 0 0 1 -210 0 z" fill="var(--surface)" stroke="var(--line-strong)"/>
<path d="M146 604 a 105.0 8 0 0 0 210 0" fill="none" stroke="var(--line-strong)"/>
<text x="251" y="626" font-size="11" text-anchor="middle" font-weight="640" fill="var(--ink)">Project store</text>
<text x="251" y="638" font-size="11" text-anchor="middle" fill="var(--muted)">Contract vN · TaskGraph vN</text>
<path d="M396 604 a 105.0 8 0 0 1 210 0 v 36 a 105.0 8 0 0 1 -210 0 z" fill="var(--surface)" stroke="var(--line-strong)"/>
<path d="M396 604 a 105.0 8 0 0 0 210 0" fill="none" stroke="var(--line-strong)"/>
<text x="501" y="626" font-size="11" text-anchor="middle" font-weight="640" fill="var(--ink)">Attempt lineage</text>
<text x="501" y="638" font-size="11" text-anchor="middle" fill="var(--muted)">receipts · cancels</text>
<path d="M666 604 a 105.0 8 0 0 1 210 0 v 36 a 105.0 8 0 0 1 -210 0 z" fill="var(--surface)" stroke="var(--line-strong)"/>
<path d="M666 604 a 105.0 8 0 0 0 210 0" fill="none" stroke="var(--line-strong)"/>
<text x="771" y="626" font-size="11" text-anchor="middle" font-weight="640" fill="var(--ink)">Evidence · verdicts</text>
<text x="771" y="638" font-size="11" text-anchor="middle" fill="var(--muted)">append-only</text>
<path d="M916 604 a 115.0 8 0 0 1 230 0 v 36 a 115.0 8 0 0 1 -230 0 z" fill="var(--surface)" stroke="var(--line-strong)"/>
<path d="M916 604 a 115.0 8 0 0 0 230 0" fill="none" stroke="var(--line-strong)"/>
<text x="1031" y="626" font-size="11" text-anchor="middle" font-weight="640" fill="var(--ink)">Knowledge graphs</text>
<text x="1031" y="638" font-size="11" text-anchor="middle" fill="var(--muted)">typed projections</text>
<rect x="446" y="672" width="320" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="606" y="693" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">GEPA + governed RSI</text>
<text x="606" y="707" font-size="11" text-anchor="middle" fill="var(--muted)">candidates · budgets · frozen policy · approval</text>
<path d="M446 44 L486 44" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#km)"/>
<path d="M560 64 L560 82 L246 82 L246 104" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#km)"/>
<text x="410" y="96" font-size="11" text-anchor="middle" font-weight="640" fill="var(--muted)">a need — request · clue · material</text>
<path d="M496 104 L496 64" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#km)" marker-start="url(#km)"/>
<text x="504" y="88" font-size="11" text-anchor="start" fill="var(--muted)">confirm Contract</text>
<path d="M346 130 L386 130" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#km)"/>
<path d="M606 130 L646 130" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#km)"/>
<text x="626" y="122" font-size="11" text-anchor="middle" fill="var(--muted)"></text>
<path d="M876 130 L886 130" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#km)"/>
<path d="M966 156 L966 200" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#km)"/>
<text x="974" y="182" font-size="11" text-anchor="start" fill="var(--muted)">claim decided?</text>
<path d="M906 226 L876 226" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#km)"/>
<text x="891" y="218" font-size="11" text-anchor="middle" fill="var(--muted)">fail</text>
<path d="M761 200 L761 156" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#km)"/>
<text x="769" y="182" font-size="11" text-anchor="start" fill="var(--muted)">vN+1</text>
<path d="M930 252 L930 264 L256 264 L256 252" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#km)"/>
<text x="590" y="260" font-size="11" text-anchor="middle" font-weight="640" fill="var(--muted)">all claims decided — Contract satisfied</text>
<path d="M146 220 L138 220 L138 44 L226 44" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#km)"/>
<text x="146" y="90" font-size="11" text-anchor="start" font-weight="640" fill="var(--muted)" transform="rotate(90 146 90)">Deliverable</text>
<path d="M1106 214 L1120 214 L1120 64" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#km)"/>
<text x="1128" y="150" font-size="11" text-anchor="middle" fill="var(--muted)" transform="rotate(90 1128 150)">human approval</text>
<path d="M960 156 L960 168 L516 168 L516 380 L320 380 L320 392" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#km)"/>
<text x="700" y="162" font-size="11" text-anchor="middle" font-weight="640" fill="var(--muted)">ready step — Logical Operator request + capability requirement</text>
<path d="M280 352 L280 392" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#km)"/>
<text x="288" y="376" font-size="11" text-anchor="start" fill="var(--muted)">qualified capsule + executor</text>
<path d="M700 300 L700 276 L1006 276 L1006 252" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#km)"/>
<text x="850" y="270" font-size="11" text-anchor="middle" fill="var(--muted)">evaluation policy</text>
<path d="M396 420 L446 420" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#km)"/>
<text x="421" y="412" font-size="11" text-anchor="middle" fill="var(--muted)">spec</text>
<path d="M556 448 L556 492" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#km)"/>
<text x="564" y="474" font-size="11" text-anchor="start" fill="var(--muted)">run · resume · cancel</text>
<path d="M746 514 L796 514" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#km)"/>
<path d="M770 492 L770 470 L820 470 L820 448" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#km)"/>
<text x="830" y="474" font-size="11" text-anchor="start" fill="var(--muted)">receipts + artifacts</text>
<path d="M1016 420 L1148 420 L1148 172 L1040 172 L1040 156" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#km)"/>
<text x="1162" y="296" font-size="11" text-anchor="middle" font-weight="640" fill="var(--muted)" transform="rotate(90 1162 296)">verified step state — empty ⇒ failed</text>
<path d="M146 130 L128 130 L128 586 L210 586 L210 596" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#km)"/>
<text x="120" y="360" font-size="11" text-anchor="middle" fill="var(--muted)" transform="rotate(-90 120 360)">Contract · plan versions · budgets</text>
<path d="M866 448 L866 584 L501 584 L501 596" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#km)"/>
<path d="M866 584 L770 584 L770 596" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#km)"/>
<text x="690" y="578" font-size="11" text-anchor="middle" fill="var(--muted)">typed receipts · evidence records</text>
<path d="M1090 252 L1090 560 L830 560 L830 596" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#km)"/>
<text x="1098" y="400" font-size="11" text-anchor="middle" fill="var(--muted)" transform="rotate(90 1098 400)">Gate Verdicts</text>
<path d="M876 622 L916 622" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#km)"/>
<text x="896" y="648" font-size="10" text-anchor="middle" fill="var(--muted)">projections</text>
<path d="M501 648 L501 672" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#km)"/>
<path d="M740 648 L740 672" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#km)"/>
<path d="M766 696 L1176 696 L1176 364 L346 364 L346 352" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#km)"/>
<text x="960" y="688" font-size="11" text-anchor="middle" font-weight="640" fill="var(--muted)">governed promotion — approved versions govern future runs</text>
<g font-size="11" fill="var(--muted)"><line x1="24" y1="748" x2="62" y2="748" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#km)"/><text x="70" y="752">control / execution</text><line x1="218" y1="748" x2="256" y2="748" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#km)"/><text x="264" y="752">state · evidence · improvement</text><text x="478" y="752">bold = hand-off objects</text></g>
</svg>
```

Walking it once: a need arrives on any channel and **creates or retrieves a project**. The
Intention Compiler resolves ambiguity with the requester and mints **Contract v1**, confirmed by
a human before any work starts. The Planner derives **TaskGraph vN** — claims, dependencies,
acceptance. As steps become *semantically* ready (dependencies, inputs, budget, scope), the
bridge **binds** each to a qualified Capsule, permitted executor and available model — or stalls
with the missing capability named; it never substitutes. The compiler emits an engine
specification and dispatch runs it on whichever OpenJiuwen mechanism fits the sub-plan's shape —
a choice users never see. Engines return receipts and artifacts; the **receipt builder** turns
them into typed receipts with provenance, recording every attempt — and treating an empty result
as a failed attempt. Evaluators (never the writer) turn artifacts into **evidence**; gates issue
**verdicts** per claim; failures route to repair or to a **plan revision vN+1**; policy-flagged
decisions go to a human. When every claim is decided and the Contract is satisfied, the project
**closes**: evidence freezes, distribution is authorized, the deliverable returns through the
originating channel, and knowledge persists as typed projections. Performance history feeds
**GEPA**, whose approved candidates become new capsule, prompt, routing and evaluator versions —
governing *future* bindings only, because in-flight projects pin their versions.

### 4.1 State: precise invariants, not slogans

An earlier revision asserted "the TaskGraph is the only mutable object" and "runtime state is
never product state." Both were too absolute, and this report replaces them with the actual
invariant classes:

| Class | Members | Rule |
|---|---|---|
| **Immutable once written** | a confirmed Contract *version*; each evidence record; each verdict; each typed receipt; each promotion record | never edited — superseded by a new record |
| **Versioned** | Contract (scope change ⇒ new version + re-confirmation), TaskGraph (every replan ⇒ vN+1), Capsules, Operator profiles, evaluator policies, benchmark protocols, datasets | full history retained; heads move only forward |
| **Append-only streams** | evidence ledger, gate ledger, **execution-attempt lineage** (dispatches, receipts, cancellations, reconciliations), improvement history | ordered, attributed, replayable |
| **Mutable operational state** | per-step run status, consumed budget, stall queue, approval queue | reconstructible from the streams after any crash |
| **Reproducible projections** | the seven knowledge graphs, project status, the deliverable itself | derived from ledgers; rebuildable at any time; never hand-edited |

And the runtime-state correction: **engine journals and checkpoints are the runtime's property**
— reconstruction aids, session-scoped, free to be garbage-collected (**SRC**: the pipeline
journal is keyed by session and a new session replays nothing). But **the facts of execution are
project history**: every attempt, receipt, cancellation and reconciliation is captured into the
attempt lineage *by the bridge* at the moment it happens. On restart or resume, the bridge
re-derives a specification from the plan, lets the engine replay what its journal still holds
(**EXEC** — verified to re-execute only unfinished work), and reconciles the attempt lineage
against what actually ran. Project truth never depends on a journal surviving.

### 4.2 Execution success versus semantic acceptance

Seven distinct questions, each with one owner. Today's fail-closed posture exists because of
verified defects; the target does not enshrine those defects as permanent principles:

| # | Question | Target owner | Today (fail-closed) |
|---|---|---|---|
| 1 | did execution complete? | OpenJiuwen runtime | runtime — reliable (EXEC) |
| 2 | did execution technically succeed? | OpenJiuwen runtime, propagating failure | **bridge compensates**: empty result ⇒ failed attempt, because the engine reports success around failed steps (EXEC) |
| 3 | is there a valid typed receipt? | integration bridge | bridge (build) |
| 4 | does the artifact satisfy the node contract? | AI4RnD evaluators (conformance family) | same |
| 5 | does the evidence support the claim? | AI4RnD evidence authority + entailment | same — after the 0.25-precision check is replaced and re-measured |
| 6 | may work proceed? | AI4RnD gates (+ human where policy says) | same |
| 7 | is the project Contract satisfied? | AI4RnD project control | same |
| — | runtime supervision: retries, hangs, anomaly detection, remediation | **OpenJiuwen** — its reliability subsystem (detectors + remediation) is real (SRC) and AI4RnD must **not** rebuild it | reused as-is |

When gaps 1–2 close upstream (loud failure propagation, honest model binding, reachable
resume), rungs 1–3 belong wholly to the runtime and bridge verification thins to
schema-checking receipts. That is the mature form of Option C — and the compatibility tests in
§8 are exactly the conditions for it.

---

## 5. GEPA and governed self-improvement

The improvement **engine** is GEPA — AI4RnD's own, existing, tested machinery. The **substrate
that tests its candidates** is the same execution machinery that runs real work, reached through
the same bridge. OpenJiuwen's evolution framework contributes evaluation-and-training plumbing
through its Operator protocol; nothing in OpenJiuwen replaces GEPA's candidate generation or
governance. (One narrow overlap exists: the runtime's tool-description optimizer covers a slice
of GEPA's text-artifact surface; it is a binding-level alternative, not a replacement — **SRC**.)

```svg
<svg viewBox="0 0 1190 466" width="1190" xmlns="http://www.w3.org/2000/svg" font-family="inherit" role="img" aria-label="GEPA and the governed improvement loop">
<defs><marker id="kg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="var(--subtle)"/></marker></defs>
<rect x="40" y="36" width="230" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="155" y="59" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Performance history</text>
<text x="155" y="73" font-size="11" text-anchor="middle" fill="var(--muted)">attempts · evidence · verdicts</text>
<rect x="310" y="36" width="300" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="460" y="58" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">GEPA candidate engine</text>
<text x="460" y="71" font-size="11" text-anchor="middle" fill="var(--muted)">typed candidates: skill · capsule ·</text>
<text x="460" y="84" font-size="11" text-anchor="middle" fill="var(--muted)">routing policy · rewrite rules · cost model</text>
<text x="603" y="48" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--blocked)">EXISTS · UNWIRED</text>
<rect x="650" y="36" width="250" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="775" y="58" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Budgets & stoppers</text>
<text x="775" y="71" font-size="11" text-anchor="middle" fill="var(--muted)">spend · evals · walltime ·</text>
<text x="775" y="84" font-size="11" text-anchor="middle" fill="var(--muted)">plateau · stop-file — dry-run default</text>
<text x="893" y="48" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">EXISTS</text>
<rect x="940" y="36" width="210" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1045" y="64" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Frozen-policy check</text>
<text x="1045" y="78" font-size="11" text-anchor="middle" fill="var(--muted)">rejects any relaxation</text>
<text x="1143" y="48" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">EXISTS</text>
<path d="M270 62 L310 62" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#kg)"/>
<path d="M610 62 L650 62" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kg)"/>
<path d="M900 62 L940 62" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kg)"/>
<rect x="940" y="186" width="210" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1045" y="207" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Rejected</text>
<text x="1045" y="221" font-size="11" text-anchor="middle" fill="var(--muted)">before evaluation</text>
<rect x="600" y="186" width="300" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="750" y="202" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Isolated evaluation</text>
<text x="750" y="216" font-size="11" text-anchor="middle" fill="var(--muted)">candidates run through the same bridge</text>
<text x="750" y="230" font-size="11" text-anchor="middle" fill="var(--muted)">and engines as real work — never in place</text>
<rect x="310" y="186" width="250" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="435" y="209" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Human approval</text>
<text x="435" y="223" font-size="11" text-anchor="middle" fill="var(--muted)">Improvements inbox</text>
<path d="M1045 88 L1045 186" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kg)"/>
<text x="1053" y="142" font-size="10.5" text-anchor="start" fill="var(--muted)">relaxes a frozen rule</text>
<path d="M870 88 L790 186" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kg)"/>
<text x="806" y="142" font-size="11" text-anchor="middle" fill="var(--muted)">clean</text>
<path d="M600 212 L560 212" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kg)"/>
<path d="M400 238 L400 286 L1010 286 L1010 234" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kg)"/>
<text x="700" y="280" font-size="11" text-anchor="middle" fill="var(--muted)">declined</text>
<rect x="40" y="336" width="260" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="170" y="358" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Promoter</text>
<text x="170" y="371" font-size="11" text-anchor="middle" fill="var(--muted)">sha256-checksummed · atomic ·</text>
<text x="170" y="384" font-size="11" text-anchor="middle" fill="var(--muted)">tmp/production path guards</text>
<text x="293" y="348" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">EXISTS</text>
<rect x="340" y="336" width="230" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="455" y="352" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Registry & config</text>
<text x="455" y="366" font-size="11" text-anchor="middle" fill="var(--muted)">new capsule / prompt /</text>
<text x="455" y="380" font-size="11" text-anchor="middle" fill="var(--muted)">routing / evaluator versions</text>
<rect x="610" y="336" width="230" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="725" y="359" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Monitoring</text>
<text x="725" y="373" font-size="11" text-anchor="middle" fill="var(--muted)">regression watch</text>
<rect x="880" y="336" width="270" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1015" y="364" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Rollback</text>
<text x="1015" y="378" font-size="11" text-anchor="middle" fill="var(--muted)">restores the prior version, checksummed</text>
<text x="1143" y="348" font-size="9" font-weight="700" text-anchor="end" letter-spacing=".05em" fill="var(--primary-ink)">EXISTS</text>
<path d="M370 238 L370 310 L170 310 L170 336" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kg)"/>
<text x="272" y="304" font-size="11" text-anchor="middle" fill="var(--muted)">approved</text>
<path d="M300 362 L340 362" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kg)"/>
<path d="M570 362 L610 362" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#kg)"/>
<path d="M840 362 L880 362" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kg)"/>
<text x="860" y="354" font-size="10.5" text-anchor="middle" fill="var(--muted)">regression</text>
<path d="M1015 388 L1015 414 L455 414 L455 388" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#kg)"/>
<text x="735" y="408" font-size="11" text-anchor="middle" fill="var(--muted)">restored version re-registers</text>
<text x="595" y="436" font-size="11" text-anchor="middle" fill="var(--muted)">Evaluation/training substrate reused from OpenJiuwen (Trainer · Updater · judge metrics · RL) via Operator-protocol adapters.</text>
<text x="595" y="452" font-size="11" text-anchor="middle" fill="var(--muted)">The improvement engine is GEPA; the machinery that tests its candidates is the machinery that runs real work. In-flight projects pin versions.</text>
</svg>
```

What already exists in GEPA (**SRC**, unit-tested): the typed candidate envelope — skill,
capsule, routing policy, rewrite rules, cost model — which *is* the candidate-scope definition;
budget stoppers (spend, evaluations, wall-time, plateau, stop-file) with dry-run as the CLI
default; the frozen-policy checker that reports exact violating paths; the artifact store of
runs and candidates; and the promoter with sha256 sidecars, tmp-versus-production path guards,
atomic writes and rollback. What is missing is not machinery but **wiring and product surface**:
connection to real run history, the Improvements inbox for human approval, capsule-registry
integration, monitoring, and version pinning for in-flight projects. All eight workbook RSI
surfaces route through this one loop; model-weight evolution (surface 7) is deferred on cost —
the RL substrate exists but is unreachable from the application today (**SRC**).

Evaluation-data selection and isolated replay reuse OpenJiuwen: candidates are evaluated on
held-out case sets via the Trainer's validation-selection loop, executed through the bridge in
isolated worktrees/sandboxes — never in place.

---

## 6. Ownership at a glance

| Concern | Owner |
|---|---|
| Meaning: Contract, claims, plan, completion | **AI4RnD** |
| Capability governance: Capsules, Logical Operators, effects, certification | **AI4RnD** |
| Verification: evidence, evaluators, gates; writer ≠ verifier | **AI4RnD** |
| Improvement: GEPA candidates, budgets, frozen policy, approval, promotion | **AI4RnD** |
| Durable product state: projects, ledgers, attempt lineage, knowledge, versions | **AI4RnD** |
| Binding, compilation, dispatch/resume/cancel, typed receipts | **integration bridge** (semantic decisions forbidden) |
| Physical execution, scheduling within a spec, runtime supervision, sandbox | **OpenJiuwen** |
| Identity, sessions, channels, UI shell, configuration, packaging | **JiuwenSwarm** |
| Contract confirmation, gated approvals, improvement approvals, stall resolution | **humans** — the three-plus-one deliberate touchpoints |

Across the 142 outcomes: AI4RnD semantically owns 118; runtime implementation splits 53
AI4RnD / 32 bridge / 27 JiuwenSwarm / 25 OpenJiuwen / 4 new / 1 unresolved. That divergence —
own the meaning of far more than you run — is the architecture.

---

## 7. Component sourcing: reuse, adapt, derive or build

A systematic harvest of the foundation, with one of six verdicts per component:
**REUSE** unchanged · **COMPOSE** through an adapter · **EXTEND** via a supported interface ·
**DERIVE** a bounded fork · **BUILD** in AI4RnD · **REJECT**. Bounded derivation was neither
assumed nor excluded; it won exactly one candidate.

| Component | Verdict | Basis (evidence) | Condition / spike |
|---|---|---|---|
| Channels, Gateway, AgentServer, sessions, workspace | REUSE | the application shell the verticals require (SRC) | — |
| UI shell, configuration, model management, packaging | REUSE + EXTEND | research views and settings added on top | — |
| Core Workflow / Pregel | REUSE | runtime-computed fan-out executed (EXEC); durable supersteps | F4 covers lifecycle fit |
| SwarmFlow **engine** | REUSE via its backend seam | this analysis ran it end-to-end against a custom backend — the seam is the product's entry point (EXEC) | F4: three real plans compile & run |
| SwarmFlow **leader tool** | REJECT | advertises resume and rejects it; leader-chat coupling (EXEC) | replaced by bridge dispatch |
| DeepAgent, sub-agents, code mode/worktrees | REUSE | bounded agent work and POC construction (SRC) | — |
| Dynamic Team | REUSE | open-ended excursions | roles/permissions unverified live — U3 |
| Team task board (dependency edges) | COMPOSE | real add-dependencies/blocked-by manager (SRC) | projection of the TaskGraph for visibility, never the plan authority |
| Reliability detectors + remediation | REUSE | model/tool-error, loop, repeat detectors with remediation policy (SRC) | signals feed receipts; AI4RnD must not rebuild supervision |
| Team/shared memory, retrieval | EXTEND | substrate exists (SRC) | research-grade retrieval measured in P5 |
| Graph memory module | EXTEND (conditional) | exists, referenced nowhere by the app (EXEC) | spike: fit for typed projections, else BUILD |
| Model pool + allocator | COMPOSE (loud-failure adapter) | silent fallback by documented design (SRC) | retire adapter if upstream fails loudly |
| Guardrail rules tier | DERIVE (bounded) or upstream EXTEND | loader ignores the installed file (EXEC); single-file boundary, upstream tests retained, delta = search path + non-empty assertion | reconcile on upstream fix |
| Permissions engine + jiuwenbox sandbox | REUSE | tiered policy executed in analysis (EXEC); enforcement itself untested here (U2) | adversarial test before trust |
| Observability, progress events, background tasks | REUSE | spans and async controller (SRC) | — |
| agent_evolving: Trainer, Updater, Operator protocol, metrics, EvolutionStore | EXTEND | real loop; one wired subject today (EXEC) | Q27-class spike: register a capsule as a subject |
| agent_rl (PPO/verl) | DEFER | unreachable from the app (SRC); cost | with RSI surface 7 |
| Tool-description optimizer | COMPOSE (narrow) | overlaps one GEPA text slice (SRC) | binding-level only |
| Symphony skill retrieval | COMPOSE | ranks but never refuses (SRC) | candidate *suggestion* under the capsule gate — never the gate |
| AI4RnD evidence + gate ledgers | PORT | run standalone (EXEC) | project-scoped storage |
| AI4RnD capsule registry + manifests | PORT + EXTEND | 42 complete manifests (EXEC) | schema gains versions/history/RSI targets |
| AI4RnD GEPA | PORT (survives whole) | §5 (SRC, tested) | wire to inbox + registry |
| AI4RnD graph_scheduler + actor family | REJECT | duplicates verified engines; semantic readiness/binding logic relocates to project control and bridge | — |
| tmux cockpit + polling coordinator | REJECT | cannot meet multi-user/channel verticals | retained in history as rejected design |
| Grounding check | REJECT & REBUILD | 0.25 precision (EXEC) | bar published before build, measured after |

Matrix impact: this audit changed three rows of the 142-row ownership matrix (capsule
version-promotion, evaluator-driven operator evolution, capsules-as-evolution-subjects) from
BUILD to ADAPT, because GEPA's promoter, budget/frozen-policy machinery and typed capsule
candidates already exist. New decision totals: **BUILD 50 · ADAPT 35 · REUSE 23 · PORT 20 ·
EXTEND 11 · DEFER 2 · UNRESOLVED 1**
([full matrix](traceability/142-feature-implementation-ownership.csv)).

---

## 8. Implementation direction

Dependency-driven, no calendar estimates — earlier LOC/month figures were withdrawn when
execution probes showed what reading had missed. Sequence is knowable; duration is staffing.

| Phase | Objective | Exit evidence |
|---|---|---|
| **P1 — project & Contract foundation** | durable projects behind the existing channels/UI; Intention Compiler; users choose objective and depth only | a project survives restart; an unconfirmed Contract blocks work |
| **P2 — spikes, then the bridge** | prove compilation; build binding, dispatch/resume/cancel, receipt builder; fix the guardrail file | interrupted run resumes re-executing only unfinished work; empty result blocks its gate; guardrails load non-empty |
| **P3 — trustworthy evidence & capability registry** | ledgers project-scoped; **entailment rebuilt with the bar published first**; honest binding with effects enforcement and writer≠verifier | claims resolve to spans; measured precision materially above 0.25; unsatisfiable requirements stall |
| **P4 — the R&D lanes & Builder** | Idea Card, falsifiability gate, POC on worktrees, benchmarking, the 14 Builder outcomes | a run reaches a decision with card, falsifiability verdict, baseline benchmark, dossier |
| **P5 — data foundations & delivery** | one authoritative store, seven typed projections, TaskGraph lifecycle, closure | any claim resolves to its concepts/datasets/code/runs in one query |
| **P6 — GEPA wiring, RSI governance, accounts, hardening** | inbox, pinning, monitoring/rollback drills; the account subsystem; platform packaging | frozen-policy candidate rejected pre-evaluation; rollback drill leaves in-flight runs untouched |

**Spikes that gate the plan** (choices conditional on them):

- **F4 — compile three representative plans** — (1) source-heavy research, (2) POC construction
  plus benchmarking, (3) failed verification followed by repair and replanning — to the pipeline
  engine and/or staged workflows, and run the deterministic parts. *Both targets failing reverts
  the architecture to Option A.* Two related spikes already passed during analysis: runtime-
  computed fan-out (EXEC) and stock-install persistence (SRC).
- **Capsule-as-subject** — register one capsule as an evolution-framework subject through the
  Operator protocol. Failure grows P6 and keeps the affected RSI surfaces manual longer.
- **Graph-memory fit** — decides EXTEND versus BUILD for the typed-projection layer.
- **Sandbox adversarial test** — before any security reliance on jiuwenbox.
- **Team roles/permissions live probe** — before routing open-ended excursions to Dynamic Team.

---

## 9. Verified limitations, risks and open decisions

**Execution-verified limitations** (each shaped the design; none was silently accepted): silent
model substitution; unreachable resume; false-success on failed steps; unread executor typing;
zero-rule guardrail tier; one-subject evolution wiring; 0.25 grounding precision.

**Not verifiable here** (recorded, not assumed): platform installers (6 matrix rows carry
UNVERIFIED); sandbox enforcement under attack; live Team role limits; end-to-end model-fallback
behaviour with real credentials; achievable entailment ceiling.

**Principal risks.**
1. *Entailment quality* — if a rebuilt check cannot materially beat 0.25 on research citations,
   the product's central promise fails regardless of architecture. Mitigation: P3 publishes the
   bar before building; stop-widening decision point if unmet.
2. *Compilation coverage* — the mechanism mix is design intent until F4 runs.
3. *Upstream drift* — adapters and the one bounded derivative must be reconciled against pinned
   dependency updates; each carries retained upstream tests as its tripwire.
4. *Approval throughput* — three-plus-one human touchpoints could bottleneck at volume; P1 exit
   review watches it.

**Open product decisions** (need an owner, not more analysis): what "Cluster setting" owns
(the one UNRESOLVED row); whether tmux is a supported *channel* of the product or retired
tooling; the definition of the externally-referenced "V-05" intake qualification tier; who owns
strategic screening criteria; whether one-shot runs without a durable project are a product
mode.

---

## 10. Conclusion

The complete intended AI4RnD product — all 142 outcomes, with Capsules, Contracts, Operators,
semantic TaskGraphs, evaluators, evidence, knowledge, GEPA and governed RSI first-class — can be
built on JiuwenSwarm and OpenJiuwen. The foundation contributes exactly what the product should
not build: channels, sessions, UI, sandboxing, durable graph execution, replayable pipelines,
teams, supervision and training plumbing. AI4RnD contributes exactly what no runtime can:
meaning, capability governance, verification and governed self-improvement. The bridge between
them stays thin, honest and fail-closed until each compatibility test proves the runtime can be
trusted with more — and the target explicitly hands runtime supervision back to the runtime as
those tests pass.

~56 of the 142 outcomes require new construction under every option; the architecture decision
was never about avoiding that work, only about never doing it twice and never dropping an
outcome to make a diagram simpler.

### What changed from commit `69ebc372`, and what held

**Held:** the recommendation (progressive compilation, Option C); zero dropped outcomes; all
seven negative findings; the decision-ownership principle; the journey's shape; the preservation
gate's logic; every executed probe result.

**Changed, with reasons:**
1. *Framing* — "claims refinery" narrowed the product; now the identity is an evidence-governed
   R&D system with claims refinement as its verification spine (§1).
2. *State model* — two absolutes replaced by invariant classes plus execution-attempt lineage as
   first-class project history (§4.1).
3. *Execution ownership* — the fail-closed bridge posture is dated to today's defects, with an
   explicit target that returns rungs 1–3 and supervision to the runtime (§4.2).
4. *GEPA* — surfaced from an unexplained "governed RSI" box into the named improvement engine,
   with its existing budgets, frozen-policy and promote/rollback machinery credited (§5); three
   matrix rows corrected BUILD → ADAPT accordingly (§7).
5. *Component audit* — extended beyond engines to the task board, reliability, memory,
   Symphony-as-suggester and a single bounded derivative (§7).
6. *Document set* — this report replaces the multi-document presentation as the primary
   deliverable; the eight analyses and the full history are supporting material; the stale
   "seven documents" language is corrected.
7. *Diagrams* — one authoritative end-to-end functional architecture restored at full product
   scope (§4); current-state and intended-state views separated and status-labelled (§1–2); the
   hard-to-read five-actor sequence demoted to the supporting engineering appendix.

### Assumptions this report rests on

1. The 142-feature workbook is the complete product definition.
2. Phases group by the durable object each mints; the workbook names no macro-phases.
3. A confirmed Contract is immutable per version; the workbook requires confirmation but not
   mutability rules — chosen for auditability.
4. Seven knowledge graphs are typed projections over one authoritative store; physical storage
   is unprescribed.
5. Human touchpoints are the four named; the workbook implies review without enumerating.
6. The pinned OpenJiuwen (`0.1.15.post3`) is representative of the integration target; upstream
   fixes shift adapter work but not ownership.

*Supporting material: the [eight detailed analyses](html/index.html), the
[142-row ownership matrix](traceability/142-feature-implementation-ownership.csv), the
[preservation gate](traceability/142-feature-preservation-gate.csv), and the
[full four-revision history with probe transcripts](source-material/README.md).*
