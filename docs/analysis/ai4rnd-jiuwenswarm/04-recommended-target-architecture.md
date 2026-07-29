# Recommended Target Architecture

**AI4RnD is a first-class, persistent project subsystem on JiuwenSwarm. AI4RnD permanently owns
product semantics; JiuwenSwarm owns the application foundation; OpenJiuwen supplies execution
mechanisms; a thin bridge compiles ready sub-plans onto them progressively.**

This is Option C from [03-integration-options.md](03-integration-options.md). This document gives
the structure, the central end-to-end workflow, and the rules that keep the boundaries honest.

---

## 1. The structure

```svg
<svg viewBox="0 0 1190 448" width="1190" xmlns="http://www.w3.org/2000/svg" font-family="inherit" role="img" aria-label="Recommended integration structure">
<defs><marker id="ah2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="var(--subtle)"/></marker></defs>
<rect x="8" y="8" width="1174" height="96" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="32" font-size="12.5" font-weight="640" fill="var(--primary-ink)">JiuwenSwarm — application foundation</text>
<rect x="8" y="112" width="1174" height="104" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="136" font-size="12.5" font-weight="640" fill="var(--primary-ink)">AI4RnD — product core (permanent)</text>
<rect x="8" y="224" width="1174" height="104" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="248" font-size="12.5" font-weight="640" fill="var(--primary-ink)">AI4RnD–Jiuwen integration bridge</text>
<rect x="8" y="336" width="1174" height="96" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<text x="24" y="360" font-size="12.5" font-weight="640" fill="var(--primary-ink)">OpenJiuwen — execution mechanisms</text>
<rect x="240" y="42" width="200" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="340.0" y="68" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Channels · Gateway</text>
<rect x="480" y="42" width="200" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="580.0" y="68" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Sessions · workspace</text>
<rect x="720" y="42" width="430" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="935.0" y="68" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">UI shell · accounts · providers · config · packaging</text>
<rect x="40" y="146" width="240" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="160.0" y="169" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Project subsystem</text>
<text x="160.0" y="183" font-size="11.5" text-anchor="middle" fill="var(--muted)">record · Contract · budget · status</text>
<rect x="320" y="146" width="250" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="445.0" y="169" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Intention Compiler · Planner</text>
<text x="445.0" y="183" font-size="11.5" text-anchor="middle" fill="var(--muted)">→ semantic TaskGraph</text>
<rect x="610" y="146" width="230" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="725.0" y="169" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Capability Capsules ·</text>
<text x="725.0" y="183" font-size="11.5" text-anchor="middle" fill="var(--muted)">Logical Operators</text>
<rect x="880" y="146" width="270" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1015.0" y="169" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Evidence · gates · evaluators</text>
<text x="1015.0" y="183" font-size="11.5" text-anchor="middle" fill="var(--muted)">data foundations · governed RSI</text>
<rect x="320" y="258" width="250" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="445.0" y="281" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Compiler</text>
<text x="445.0" y="295" font-size="11.5" text-anchor="middle" fill="var(--muted)">ready sub-plan → execution spec</text>
<rect x="610" y="258" width="230" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="725.0" y="281" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Capability & model binding</text>
<text x="725.0" y="295" font-size="11.5" text-anchor="middle" fill="var(--muted)">honest stall · no substitution</text>
<rect x="880" y="258" width="270" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1015.0" y="281" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Fact converter</text>
<text x="1015.0" y="295" font-size="11.5" text-anchor="middle" fill="var(--muted)">receipts → evidence & state</text>
<rect x="40" y="370" width="800" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="440.0" y="396" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Core Workflow · SwarmFlow · DeepAgent · Dynamic Team · code mode / worktrees</text>
<path d="M520 86 L200 146" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah2)"/>
<text x="300" y="124" font-size="11" text-anchor="start" fill="var(--muted)">requests · sessions</text>
<path d="M445 198 L445 258" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah2)"/>
<text x="453" y="232" font-size="11" text-anchor="start" fill="var(--muted)">ready sub-plans</text>
<path d="M725 198 L725 258" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah2)"/>
<text x="733" y="232" font-size="11" text-anchor="start" fill="var(--muted)">qualified capsules</text>
<path d="M1015 258 L1015 198" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#ah2)"/>
<text x="1023" y="232" font-size="11" text-anchor="start" fill="var(--muted)">evidence · verified state</text>
<path d="M445 310 L445 370" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah2)"/>
<text x="453" y="344" font-size="11" text-anchor="start" fill="var(--muted)">stages · scripts</text>
<path d="M725 310 L725 370" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah2)"/>
<text x="733" y="344" font-size="11" text-anchor="start" fill="var(--muted)">bound agent calls</text>
<path d="M840 392 L1015 392 L1015 310" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#ah2)"/>
<text x="860" y="384" font-size="11" text-anchor="start" fill="var(--muted)">execution facts</text>
</svg>
```

The bridge is the only place the two vocabularies meet: on one side, plan nodes, capability
requirements and gate policy; on the other, workflow scripts, agent calls and worktrees. It never
makes semantic decisions — it translates them.

## 2. The end-to-end functional workflow

The central picture. **Solid arrows are control and execution; dashed arrows are evidence and
state.** The semantic TaskGraph defines *what must happen*; execution specifications define *how
ready work runs*.

```svg
<svg viewBox="0 0 1190 918" width="1190" xmlns="http://www.w3.org/2000/svg" font-family="inherit" role="img" aria-label="End-to-end functional workflow">
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="var(--subtle)"/></marker></defs>
<rect x="126" y="8" width="1056" height="76" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<rect x="8" y="8" width="112" height="76" rx="8" fill="var(--surface-quiet)" stroke="var(--line)"/>
<text x="20" y="28" font-size="15" font-weight="700" fill="var(--primary-ink)">1</text>
<text x="20" y="46" font-size="10.5" fill="var(--subtle)">User and</text>
<text x="20" y="60" font-size="10.5" fill="var(--subtle)">channels</text>
<rect x="126" y="92" width="1056" height="76" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<rect x="8" y="92" width="112" height="76" rx="8" fill="var(--surface-quiet)" stroke="var(--line)"/>
<text x="20" y="112" font-size="15" font-weight="700" fill="var(--primary-ink)">2</text>
<text x="20" y="130" font-size="10.5" fill="var(--subtle)">JiuwenSwarm</text>
<text x="20" y="144" font-size="10.5" fill="var(--subtle)">application</text>
<rect x="126" y="176" width="1056" height="236" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<rect x="8" y="176" width="112" height="236" rx="8" fill="var(--surface-quiet)" stroke="var(--line)"/>
<text x="20" y="196" font-size="15" font-weight="700" fill="var(--primary-ink)">3</text>
<text x="20" y="214" font-size="10.5" fill="var(--subtle)">AI4RnD product</text>
<text x="20" y="228" font-size="10.5" fill="var(--subtle)">core</text>
<rect x="126" y="420" width="1056" height="168" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<rect x="8" y="420" width="112" height="168" rx="8" fill="var(--surface-quiet)" stroke="var(--line)"/>
<text x="20" y="440" font-size="15" font-weight="700" fill="var(--primary-ink)">4</text>
<text x="20" y="458" font-size="10.5" fill="var(--subtle)">AI4RnD–Jiuwen</text>
<text x="20" y="472" font-size="10.5" fill="var(--subtle)">integration</text>
<text x="20" y="486" font-size="10.5" fill="var(--subtle)">bridge</text>
<rect x="126" y="596" width="1056" height="84" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<rect x="8" y="596" width="112" height="84" rx="8" fill="var(--surface-quiet)" stroke="var(--line)"/>
<text x="20" y="616" font-size="15" font-weight="700" fill="var(--primary-ink)">5</text>
<text x="20" y="634" font-size="10.5" fill="var(--subtle)">OpenJiuwen</text>
<text x="20" y="648" font-size="10.5" fill="var(--subtle)">execution</text>
<text x="20" y="662" font-size="10.5" fill="var(--subtle)">runtime</text>
<rect x="126" y="688" width="1056" height="74" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<rect x="8" y="688" width="112" height="74" rx="8" fill="var(--surface-quiet)" stroke="var(--line)"/>
<text x="20" y="708" font-size="15" font-weight="700" fill="var(--primary-ink)">7</text>
<text x="20" y="726" font-size="10.5" fill="var(--subtle)">External</text>
<text x="20" y="740" font-size="10.5" fill="var(--subtle)">models, tools,</text>
<text x="20" y="754" font-size="10.5" fill="var(--subtle)">sources</text>
<rect x="126" y="770" width="1056" height="124" rx="8" fill="var(--canvas)" stroke="var(--line)"/>
<rect x="8" y="770" width="112" height="124" rx="8" fill="var(--surface-quiet)" stroke="var(--line)"/>
<text x="20" y="790" font-size="15" font-weight="700" fill="var(--primary-ink)">6</text>
<text x="20" y="808" font-size="10.5" fill="var(--subtle)">Data, evidence</text>
<text x="20" y="822" font-size="10.5" fill="var(--subtle)">and project</text>
<text x="20" y="836" font-size="10.5" fill="var(--subtle)">state</text>
<rect x="226" y="26" width="110" height="40" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="281.0" y="50" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">User</text>
<rect x="392" y="26" width="210" height="40" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="497.0" y="50" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Channel · Web UI · CLI</text>
<rect x="392" y="112" width="210" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="497.0" y="138" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Gateway · session</text>
<rect x="880" y="112" width="270" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1015.0" y="131" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Project view</text>
<text x="1015.0" y="145" font-size="11.5" text-anchor="middle" fill="var(--muted)">progress · approvals · deliverables</text>
<rect x="226" y="196" width="170" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="311.0" y="224" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Intention Compiler</text>
<rect x="462" y="196" width="120" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="522.0" y="224" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Planner</text>
<rect x="648" y="196" width="210" height="48" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="753.0" y="217" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Semantic readiness ·</text>
<text x="753.0" y="231" font-size="11.5" text-anchor="middle" fill="var(--muted)">run-state authority</text>
<rect x="690" y="308" width="150" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="765.0" y="338" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Gate decision</text>
<rect x="462" y="308" width="140" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="532.0" y="331" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Repair ·</text>
<text x="532.0" y="345" font-size="11.5" text-anchor="middle" fill="var(--muted)">replanning</text>
<rect x="900" y="308" width="150" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="975.0" y="338" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Deliverable</text>
<rect x="226" y="440" width="250" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="351.0" y="465" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Capability &amp; model binding</text>
<text x="351.0" y="479" font-size="11.5" text-anchor="middle" fill="var(--muted)">stalls honestly — never substitutes</text>
<rect x="546" y="440" width="220" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="656.0" y="465" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Compiler</text>
<text x="656.0" y="479" font-size="11.5" text-anchor="middle" fill="var(--muted)">progressively compiles ready sub-plans</text>
<rect x="836" y="440" width="180" height="56" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="926.0" y="465" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Dispatch ·</text>
<text x="926.0" y="479" font-size="11.5" text-anchor="middle" fill="var(--muted)">resume · cancel</text>
<rect x="560" y="520" width="250" height="50" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="685.0" y="542" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Fact converter</text>
<text x="685.0" y="556" font-size="11.5" text-anchor="middle" fill="var(--muted)">a None result is a failure</text>
<rect x="226" y="612" width="800" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="626.0" y="642" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Core Workflow · SwarmFlow · DeepAgent · Dynamic Team · code mode / worktrees</text>
<rect x="226" y="700" width="800" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="626.0" y="726" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Model providers · tools · literature &amp; data sources</text>
<path d="M236 814 a 75.0 8 0 0 1 150 0 v 36 a 75.0 8 0 0 1 -150 0 z" fill="var(--surface)" stroke="var(--line-strong)"/>
<path d="M236 814 a 75.0 8 0 0 0 150 0" fill="none" stroke="var(--line-strong)"/>
<text x="311.0" y="836" font-size="11" text-anchor="middle" fill="var(--ink)">Project store</text>
<text x="311.0" y="848" font-size="11" text-anchor="middle" fill="var(--ink)">Contract · plan · runs</text>
<path d="M416 814 a 75.0 8 0 0 1 150 0 v 36 a 75.0 8 0 0 1 -150 0 z" fill="var(--surface)" stroke="var(--line-strong)"/>
<path d="M416 814 a 75.0 8 0 0 0 150 0" fill="none" stroke="var(--line-strong)"/>
<text x="491.0" y="836" font-size="11" text-anchor="middle" fill="var(--ink)">Gate ledger</text>
<text x="491.0" y="848" font-size="11" text-anchor="middle" fill="var(--ink)">append-only</text>
<path d="M596 814 a 85.0 8 0 0 1 170 0 v 36 a 85.0 8 0 0 1 -170 0 z" fill="var(--surface)" stroke="var(--line-strong)"/>
<path d="M596 814 a 85.0 8 0 0 0 170 0" fill="none" stroke="var(--line-strong)"/>
<text x="681.0" y="836" font-size="11" text-anchor="middle" fill="var(--ink)">Evidence ledger</text>
<text x="681.0" y="848" font-size="11" text-anchor="middle" fill="var(--ink)">citation spans</text>
<rect x="806" y="806" width="160" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="886.0" y="829" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Improvement</text>
<text x="886.0" y="843" font-size="11.5" text-anchor="middle" fill="var(--muted)">Proposal</text>
<path d="M996 814 a 75.0 8 0 0 1 150 0 v 36 a 75.0 8 0 0 1 -150 0 z" fill="var(--surface)" stroke="var(--line-strong)"/>
<path d="M996 814 a 75.0 8 0 0 0 150 0" fill="none" stroke="var(--line-strong)"/>
<text x="1071.0" y="836" font-size="11" text-anchor="middle" fill="var(--ink)">Typed knowledge</text>
<text x="1071.0" y="848" font-size="11" text-anchor="middle" fill="var(--ink)">graphs</text>
<path d="M336 46 L392 46" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah)"/>
<path d="M497 66 L497 112" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah)"/>
<text x="505" y="94" font-size="11" text-anchor="start" fill="var(--muted)">request</text>
<path d="M420 156 L280 196" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah)"/>
<text x="300" y="172" font-size="11" text-anchor="start" font-weight="640" fill="var(--muted)">Qualified Intake</text>
<path d="M380 196 L560 156" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah)" marker-start="url(#ah)"/>
<text x="612" y="150" font-size="11" text-anchor="start" fill="var(--muted)">ambiguity Q&amp;A · confirm Contract</text>
<path d="M396 220 L462 220" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah)"/>
<text x="429" y="212" font-size="11" text-anchor="middle" font-weight="640" fill="var(--muted)">Research</text>
<text x="429" y="236" font-size="11" text-anchor="middle" font-weight="640" fill="var(--muted)">Contract</text>
<path d="M582 220 L648 220" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah)"/>
<text x="615" y="190" font-size="11" text-anchor="middle" font-weight="640" fill="var(--muted)">semantic TaskGraph</text>
<text x="615" y="258" font-size="11" text-anchor="middle" fill="var(--subtle)">what must happen</text>
<path d="M760 244 L760 308" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah)"/>
<text x="768" y="280" font-size="11" text-anchor="start" fill="var(--muted)">gated step done</text>
<path d="M690 334 L602 334" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah)"/>
<text x="646" y="326" font-size="11" text-anchor="middle" fill="var(--muted)">fail</text>
<path d="M528 308 L528 244" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah)"/>
<text x="536" y="280" font-size="11" text-anchor="start" fill="var(--muted)">revised sub-plan</text>
<path d="M840 334 L900 334" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah)"/>
<text x="870" y="326" font-size="11" text-anchor="middle" fill="var(--muted)">pass</text>
<path d="M975 308 L975 156" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah)"/>
<text x="983" y="234" font-size="11" text-anchor="start" font-weight="640" fill="var(--muted)">Deliverable</text>
<path d="M824 308 L940 156" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah)" marker-start="url(#ah)"/>
<text x="890" y="262" font-size="11" text-anchor="start" fill="var(--muted)">human approval</text>
<path d="M660 244 L660 398 L360 398 L360 440" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah)"/>
<text x="510" y="380" font-size="11" text-anchor="middle" font-weight="640" fill="var(--muted)">Logical Operator Request +</text>
<text x="510" y="394" font-size="11" text-anchor="middle" font-weight="640" fill="var(--muted)">Capability Requirement</text>
<path d="M476 468 L546 468" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah)"/>
<text x="511" y="510" font-size="11" text-anchor="middle" fill="var(--muted)">bound capsule + executor</text>
<path d="M766 468 L836 468" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah)"/>
<text x="801" y="432" font-size="11" text-anchor="middle" font-weight="640" fill="var(--muted)">Execution Specification</text>
<text x="801" y="508" font-size="11" text-anchor="middle" fill="var(--subtle)">how ready work runs</text>
<path d="M926 496 L926 612" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah)"/>
<text x="934" y="560" font-size="11" text-anchor="start" fill="var(--muted)">run</text>
<path d="M626 664 L626 700" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah)"/>
<text x="634" y="686" font-size="11" text-anchor="start" fill="var(--muted)">model &amp; tool calls</text>
<path d="M685 612 L685 570" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah)"/>
<text x="693" y="596" font-size="11" text-anchor="start" font-weight="640" fill="var(--muted)">Node Execution Receipt</text>
<path d="M810 545 L1060 545 L1060 264 L838 264 L838 244" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah)"/>
<text x="1068" y="420" font-size="11" text-anchor="start" font-weight="640" fill="var(--muted)" transform="rotate(90 1068 420)">verified step state</text>
<path d="M800 360 L800 384 L1136 384 L1136 778 L491 778 L491 806" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#ah)"/>
<text x="955" y="376" font-size="11" text-anchor="middle" font-weight="640" fill="var(--muted)">Gate Verdict — recorded append-only</text>
<path d="M560 532 L178 532 L178 788 L681 788 L681 806" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#ah)"/>
<text x="360" y="524" font-size="11" text-anchor="middle" font-weight="640" fill="var(--muted)">Evidence Record</text>
<path d="M226 220 L205 220 L205 798 L300 798 L300 806" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#ah)"/>
<text x="198" y="520" font-size="11" text-anchor="middle" fill="var(--muted)" transform="rotate(-90 198 520)">Contract · plan · run state</text>
<path d="M766 832 L806 832" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#ah)"/>
<text x="786" y="876" font-size="11" text-anchor="middle" fill="var(--muted)">performance history</text>
<path d="M1026 638 L1108 638 L1108 156" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#ah)"/>
<text x="1120" y="430" font-size="11" text-anchor="middle" font-weight="640" fill="var(--muted)" transform="rotate(90 1120 430)">Progress Event</text>
<path d="M886 806 L886 782 L1164 782 L1164 416 L340 416 L340 440" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#ah)"/>
<text x="1176" y="600" font-size="11" text-anchor="middle" fill="var(--muted)" transform="rotate(90 1176 600)">governed RSI loop (§5) — promoted versions govern future bindings</text>
<g font-size="11" fill="var(--muted)"><line x1="134" y1="908" x2="174" y2="908" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah)"/><text x="182" y="912">control / execution</text><line x1="322" y1="908" x2="362" y2="908" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#ah)"/><text x="370" y="912">evidence / state</text><text x="526" y="912" font-weight="640" fill="var(--muted)">bold labels</text><text x="604" y="912">= the twelve hand-off objects</text></g>
</svg>
```

Reading it left to right and back:

1. A request arrives on any channel; the Gateway qualifies it and binds it to a project
   (**Qualified Intake**).
2. The Intention Compiler resolves ambiguity with the user and produces a confirmed **Research
   Contract**; the Planner turns it into the **semantic TaskGraph**.
3. As steps become *semantically* ready, AI4RnD issues **Logical Operator Requests** with their
   **Capability Requirements**. The bridge binds each to a qualified capsule and permitted
   executor — or stalls with a stated reason. It never substitutes.
4. The compiler emits an **Execution Specification** — a Core Workflow stage, a SwarmFlow script,
   an agent call, a team excursion or a worktree build — and dispatch hands it to the runtime.
   This is the progressive part: only *ready* sub-plans are compiled, and more compilation moves
   behind this line as compatibility tests pass.
5. The runtime streams **Progress Events** to the project view and returns **Node Execution
   Receipts**. The fact converter turns receipts into **Evidence Records** and *verified* step
   state — a step whose result is `None` is recorded as failed, whatever the engine said.
6. Evaluators read evidence; gates issue **Gate Verdicts**. Failures route to repair and
   replanning, which feed the Planner a revised sub-plan. Where policy requires, a human approves
   through the same channels.
7. Completion is decided by AI4RnD's own authority, and the **Deliverable** returns through the
   channel it came from. Run history feeds **Improvement Proposals** into the governed RSI loop.

## 3. Ownership at a glance

| Concern | Decided by | Stored by | Verified by |
|---|---|---|---|
| What the request means; when it is done | AI4RnD core | Project store | Contract acceptance criteria |
| What work exists and in what order | AI4RnD core (TaskGraph) | Project store | Plan validation & feasibility |
| Which capability serves a step | Bridge, from capsule registry | Capsule registry | Certification + effects check |
| How a ready sub-plan physically runs | Bridge compiler | Jiuwen checkpointer / journal | Compatibility tests |
| Whether a step actually succeeded | AI4RnD run-state authority | Project store | Fact converter rules |
| Whether the output is true | AI4RnD evaluators & gates | Evidence + gate ledgers | Writer ≠ verifier |
| Whether the system may change itself | Governed RSI | Improvement store | Approval + frozen-policy check |
| Who the user is; where they interact | JiuwenSwarm | Application stores | Platform |

## 4. Boundary rules

1. The product definition never moves; execution choices change ownership, never outcomes.
2. Users choose **objective and depth**. The execution mechanism is a read-only diagnostic.
3. The compiler picks mechanisms from the sub-plan's shape, not from user intent.
4. AI4RnD never trusts a completion signal it did not verify.
5. A capability, model or executor that cannot be bound **stalls with a reason** — no fallback,
   no substitution.
6. Declared capsule effects are enforced at binding time (`network: none` cannot bind to a
   networked runner).
7. The writer of an artifact never verifies it — enforced when the candidate set is built.
8. Write-scope conflicts are excluded at compile time, so conflicting steps never run in parallel.
9. The gate ledger is append-only and writer-attributed; status is a projection.
10. Evidence and project state are **project-scoped**, never session-scoped — the runtime's
    journal is keyed by session and must not carry multi-week continuity.
11. Nothing self-modifies without a proposal, risk class, frozen-policy check and approval.
12. In-flight runs pin their capsule versions; promotions never change running work.

## 5. The governed RSI loop

All eight improvement surfaces (text artifacts, routing, capsules/operators, plan structure,
evaluators/rewards, memory/retrieval, model weights, data/benchmarks) travel the same loop. Model
weights are deferred on cost, not capability.

```svg
<svg viewBox="0 0 1190 452" width="1190" xmlns="http://www.w3.org/2000/svg" font-family="inherit" role="img" aria-label="Governed RSI loop">
<defs><marker id="ah4" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="var(--subtle)"/></marker></defs>
<rect x="40" y="36" width="190" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="135.0" y="59" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Run evidence</text>
<text x="135.0" y="73" font-size="11" text-anchor="middle" fill="var(--muted)">performance history</text>
<rect x="290" y="36" width="235" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="407.5" y="59" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Improvement Proposal</text>
<text x="407.5" y="73" font-size="11" text-anchor="middle" fill="var(--muted)">subject · claim · measurement</text>
<rect x="585" y="36" width="160" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="665.0" y="59" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Risk</text>
<text x="665.0" y="73" font-size="11" text-anchor="middle" fill="var(--muted)">classification</text>
<rect x="805" y="36" width="185" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="897.5" y="59" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Frozen-policy check</text>
<text x="897.5" y="73" font-size="11" text-anchor="middle" fill="var(--muted)">rejects relaxations</text>
<path d="M230 62 L290 62" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#ah4)"/>
<path d="M525 62 L585 62" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah4)"/>
<path d="M745 62 L805 62" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah4)"/>
<rect x="585" y="186" width="220" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="695.0" y="209" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Isolated evaluation</text>
<text x="695.0" y="223" font-size="11" text-anchor="middle" fill="var(--muted)">on a held-out set</text>
<rect x="290" y="186" width="235" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="407.5" y="209" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Human approval</text>
<text x="407.5" y="223" font-size="11" text-anchor="middle" fill="var(--muted)">Improvements inbox</text>
<rect x="1010" y="186" width="140" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="1080.0" y="216" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Rejected</text>
<path d="M860 88 L695 186" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah4)"/>
<text x="742" y="132" font-size="11" text-anchor="start" fill="var(--muted)">clean</text>
<path d="M935 88 L1080 186" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah4)"/>
<text x="1010" y="132" font-size="11" text-anchor="middle" fill="var(--muted)">relaxes a</text>
<text x="1030" y="146" font-size="11" text-anchor="middle" fill="var(--muted)">frozen rule</text>
<path d="M585 212 L525 212" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah4)"/>
<path d="M407 238 L407 286 L1080 286 L1080 238" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah4)"/>
<text x="700" y="280" font-size="11" text-anchor="middle" fill="var(--muted)">declined</text>
<rect x="40" y="336" width="190" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="135.0" y="359" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Registry & config</text>
<text x="135.0" y="373" font-size="11" text-anchor="middle" fill="var(--muted)">updated, versioned</text>
<rect x="290" y="336" width="220" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="400.0" y="366" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Versioned promotion</text>
<rect x="585" y="336" width="180" height="52" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="675.0" y="366" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Monitoring</text>
<rect x="820" y="318" width="180" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="910.0" y="337" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Rolled back</text>
<text x="910.0" y="351" font-size="11" text-anchor="middle" fill="var(--muted)">on regression</text>
<rect x="820" y="380" width="160" height="44" rx="7" fill="var(--surface)" stroke="var(--line-strong)"/>
<text x="900.0" y="399" font-size="12.5" text-anchor="middle" font-weight="640" fill="var(--ink)">Kept</text>
<text x="900.0" y="413" font-size="11" text-anchor="middle" fill="var(--muted)">the new baseline</text>
<path d="M350 238 L350 336" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah4)"/>
<text x="358" y="292" font-size="11" text-anchor="start" fill="var(--muted)">approved</text>
<path d="M510 362 L585 362" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah4)"/>
<path d="M765 352 L820 336" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah4)"/>
<text x="776" y="330" font-size="11" text-anchor="start" fill="var(--muted)">regression</text>
<path d="M765 372 L820 396" fill="none" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah4)"/>
<text x="776" y="402" font-size="11" text-anchor="start" fill="var(--muted)">holds</text>
<path d="M290 362 L230 362" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#ah4)"/>
<path d="M1000 336 L1030 336 L1030 434 L135 434 L135 388" fill="none" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#ah4)"/>
<text x="600" y="428" font-size="11" text-anchor="middle" fill="var(--muted)">rollback restores the prior version</text>
</svg>
```

A reviewer must be able to answer *what changed, why, and is it better* from the Improvements
inbox alone.

## 6. What retires when, in the mature form

Option C's end state approaches full delegation. Each fallback below dies only when its named
test passes — never on a date:

| AI4RnD-side fallback | Retires when |
|---|---|
| Model routing | the runtime fails loudly on an unknown model instead of substituting |
| Resume re-drive logic | resume is reachable through a supported runtime surface |
| Failure detection in the fact converter | failed steps propagate as failures, not `None` |
| Typed-executor enforcement in the bridge | the runtime honors executor typing end to end |
| Compile-time write-scope exclusion | only if the runtime ever offers equivalent isolation guarantees |

What never retires: semantic readiness, evidence sufficiency, gate decisions, repair/replanning,
and project-completion authority. Those are the product.
