#!/usr/bin/env python3
# coding: utf-8
"""Render 20-feature-implementation-ownership.md from the generated CSVs."""
from __future__ import annotations
import csv, sys, pathlib, collections

OUT = pathlib.Path(sys.argv[1]).resolve()
T = OUT / "traceability"
rows = list(csv.DictReader((T / "142-feature-implementation-ownership.csv").open(encoding="utf-8")))
gate = list(csv.DictReader((T / "142-feature-preservation-gate.csv").open(encoding="utf-8")))
assert len(rows) == 142 and len(gate) == 142
G = {g["feature_id"]: g for g in gate}

def esc(s):
    return (s or "").replace("|", "\\|").replace("\n", " ").strip()

def tally(key, src=rows):
    return collections.Counter(r[key] for r in src)

def table(counter, head, total=142):
    L = [f"| {head} | Rows | Share |", "|---|---:|---:|"]
    for k, v in counter.most_common():
        L.append(f"| {k or '(unset)'} | {v} | {100*v/total:.0f}% |")
    L.append(f"| **Total** | **{sum(counter.values())}** | **100%** |")
    return "\n".join(L)

P = []
w = P.append

w("# Feature Implementation Ownership — All 142 Workbook Outcomes")
w("")
w("**Source of truth.** Every row below comes from `AI4RnD Feature List.xlsx`, read directly with")
w("`openpyxl` in this revision. Feature identity, hierarchy and wording are the workbook's; only the")
w("analytic columns are this analysis's. The workbook reconciles exactly:")
w("")
w("| Sheet | Plane | L1 groups | L2 features |")
w("|---|---|---:|---:|")
w("| Workflow Features | Workflow | 9 | 54 |")
w("| Foundation Features | Foundation | 10 | 65 |")
w("| Vertical Features | Vertical | 6 | 23 |")
w("| **Total** | | **25** | **142** |")
w("")
w("Machine-readable: [`traceability/142-feature-implementation-ownership.csv`]"
  "(traceability/142-feature-implementation-ownership.csv) ·"
  " [`traceability/142-feature-preservation-gate.csv`](traceability/142-feature-preservation-gate.csv)")
w("")
w("---")
w("")
w("## 1. What this matrix decides")
w("")
w("The brief requires five responsibilities to be named separately for every feature, and forbids")
w("answering \"shared\". Every row therefore carries:")
w("")
w("| Column | Question it answers |")
w("|---|---|")
w("| `semantic_owner` | Who defines the feature's meaning, correctness, lifecycle and completion |")
w("| `runtime_implementer` | Who performs the execution |")
w("| `persistence_authority` | Who stores the authoritative state |")
w("| `verification_authority` | Who decides the output is valid |")
w("| `product_surface` | Where the user sees or controls it |")
w("")
w("Where a feature genuinely crosses architectural boundaries it gains **named implementation")
w("slices** beneath it. Slices never change the authoritative total: there are 142 rows, and")
w("there will always be 142 rows.")
w("")
w("---")
w("")
w("## 2. Counts")
w("")
w("### 2.1 By plane and L1 group")
w("")
w("| Plane | L1 group | L2 rows |")
w("|---|---|---:|")
per = collections.OrderedDict()
for r in rows:
    per.setdefault((r["plane"], r["l1_feature"]), 0)
    per[(r["plane"], r["l1_feature"])] += 1
for (p, l1), n in per.items():
    w(f"| {p} | {esc(l1)} | {n} |")
w(f"| | **25 groups** | **142** |")
w("")
w("### 2.2 By semantic owner")
w("")
w(table(tally("semantic_owner"), "Semantic owner"))
w("")
w("The product is overwhelmingly AI4RnD's to define. That is the point of the preservation gate:")
w("changing the execution substrate must not move these rows.")
w("")
w("### 2.3 By runtime implementer")
w("")
w(table(tally("runtime_implementer"), "Runtime implementer"))
w("")
w("Semantic ownership and runtime ownership diverge sharply — 118 rows are AI4RnD's to define but")
w("only 53 are AI4RnD's to run. That gap is the integration surface.")
w("")
w("### 2.4 By implementation decision")
w("")
w(table(tally("implementation_decision"), "Decision"))
w("")
w("### 2.5 By delivery phase")
w("")
w(table(tally("delivery_phase"), "Phase"))
w("")
w("### 2.6 By confidence")
w("")
w(table(tally("confidence"), "Confidence"))
w("")
w("### 2.7 By evidence class")
w("")
w(table(tally("evidence_class"), "Evidence class"))
w("")
w("`EXEC` means a probe was executed in this environment during this revision. `SRC` means the")
w("claim rests on reading source. `DOC` means documentation only. `INF` means inference — and every")
w("`INF` row is a row where the analysis is asserting an absence or a design intent it could not")
w("execute against.")
w("")
w("---")
w("")
w("## 3. Cross-layer features requiring implementation slices")
w("")
sl = [r for r in rows if r["implementation_slices"]]
w(f"{len(sl)} of 142 features cross an architectural boundary in a way that a single owner cannot")
w("honestly represent. Each keeps one row and gains named slices.")
w("")
for r in sl:
    w(f"**{r['feature_id']} — {esc(r['l2_feature'])}** ({r['l1_feature']})")
    w("")
    w("| Slice | Owner | Decision |")
    w("|---|---|---|")
    for s in r["implementation_slices"].split(" | "):
        parts = [p.strip() for p in s.rsplit(",", 1)]
        head, dec = (parts + [""])[:2]
        name, _, owner = head.rpartition(" - ")
        w(f"| {esc(name or head)} | {esc(owner)} | {esc(dec)} |")
    w("")
w("---")
w("")
w("## 4. Product-preservation gate")
w("")
w("Every one of the 142 outcomes is evaluated against every complete-product architecture option.")
w("An option is not a complete architecture unless it preserves all 142.")
w("")
w("| Verdict | A | B | C | D | E |")
w("|---|---:|---:|---:|---:|---:|")
for v in ["PRESERVED", "PRESERVED WITH ADAPTATION", "NEW BUILD REQUIRED", "UNRESOLVED", "DROPPED"]:
    cells = "".join(f" {sum(1 for g in gate if g[f'option_{o}'] == v)} |" for o in "ABCDE")
    w(f"| {v} |{cells}")
tot = "".join(f" **{sum(1 for g in gate if g[f'option_{o}'])}** |" for o in "ABCDE")
w(f"| **Total evaluated** |{tot}")
w("")
dropped = {o: [g for g in gate if g[f"option_{o}"] == "DROPPED"] for o in "ABCDE"}
for o in "ABCDE":
    if dropped[o]:
        w(f"**Option {o} drops {len(dropped[o])} outcome(s)** and therefore fails the gate:")
        w("")
        for g in dropped[o]:
            w(f"- `{g['feature_id']}` {esc(g['l2_feature'])} — {esc(g['l1_feature'])}")
        w("")
w("Options with zero DROPPED rows: " +
  ", ".join(o for o in "ABCDE" if not dropped[o]) + ".")
w("")
w("`NEW BUILD REQUIRED` is identical or near-identical across options (57–58 rows) because those")
w("outcomes do not exist in either system today. **No architecture choice can avoid them.** Any")
w("comparison that shows one option needing dramatically less new work is comparing execution")
w("plumbing, not product.")
w("")
w("---")
w("")
w("## 5. Unresolved ownership and product-definition questions")
w("")
unres = [r for r in rows if r["implementation_decision"] == "UNRESOLVED"
         or r["semantic_owner"] == "Unresolved"
         or G[r["feature_id"]]["option_C"] == "UNRESOLVED"]
w(f"{len(unres)} rows cannot be resolved from the workbook, the repositories or execution. They are")
w("recorded rather than guessed.")
w("")
for r in unres:
    w(f"- **{r['feature_id']} — {esc(r['l2_feature'])}** ({r['l1_feature']}). "
      f"{esc(r['assumptions_open_questions']) or 'No workbook description to resolve ownership from.'}")
w("")
amb = [r for r in rows if r["assumptions_open_questions"] and r not in unres]
w("Further recorded assumptions:")
w("")
for r in amb:
    w(f"- **{r['feature_id']}** — {esc(r['assumptions_open_questions'])}")
w("")
w("---")
w("")
w("## 6. Reuse claims and their evidence")
w("")
reuse = [r for r in rows if r["implementation_decision"] in ("REUSE", "CONFIGURE")]
strong = [r for r in reuse if r["evidence_class"] in ("EXEC", "SRC")]
weak = [r for r in reuse if r["evidence_class"] in ("DOC", "INF")]
w(f"{len(reuse)} rows claim reuse. {len(strong)} rest on executed probes or source reading; "
  f"{len(weak)} rest on documentation alone and are labelled **UNVERIFIED** below.")
w("")
w("| Feature | Claim | Evidence |")
w("|---|---|---|")
for r in weak:
    w(f"| `{r['feature_id']}` {esc(r['l2_feature'])} | {esc(r['existing_jiuwen_implementation'])} | "
      f"**UNVERIFIED** ({r['evidence_class']}) |")
w("")
w("These six are all packaging and distribution rows. Verifying them requires building installers")
w("on Windows and macOS, which this environment cannot do.")
w("")
w("---")
w("")
w("## 7. The full matrix")
w("")
w("Columns are abbreviated for width; the CSV carries all 26.")
w("")
cur = None
for r in rows:
    key = (r["plane"], r["l1_feature"])
    if key != cur:
        cur = key
        w("")
        w(f"### {r['plane']} · {esc(r['l1_feature'])}")
        w("")
        w("| ID | L2 feature | Semantic owner | Runtime | Decision | Ev | Conf | Missing work |")
        w("|---|---|---|---|---|---|---|---|")
    w("| `%s` | %s | %s | %s | **%s** | %s | %s | %s |" % (
        r["feature_id"], esc(r["l2_feature"]), esc(r["semantic_owner"]),
        esc(r["runtime_implementer"]), r["implementation_decision"],
        r["evidence_class"], r["confidence"], esc(r["missing_work"]) or "—"))
w("")
w("---")
w("")
w("## 8. How to read a decision")
w("")
w("| Decision | Meaning |")
w("|---|---|")
w("| `REUSE` | Jiuwen or AI4RnD already does this; use it unchanged |")
w("| `CONFIGURE` | Exists; needs configuration only |")
w("| `ADAPT` | Exists on one side but must change shape to serve the product outcome |")
w("| `PORT` | Exists in AI4RnD; move it onto the Jiuwen foundation |")
w("| `EXTEND` | Exists in Jiuwen; add the research-specific layer above it |")
w("| `BUILD` | Does not exist in either system |")
w("| `DEFER` | Deliberately postponed with a stated reason |")
w("| `UNRESOLVED` | Cannot be decided from available evidence |")

(OUT / "20-feature-implementation-ownership.md").write_text("\n".join(P) + "\n", encoding="utf-8")
print("wrote 20-feature-implementation-ownership.md  (%d lines)" % len(P))
