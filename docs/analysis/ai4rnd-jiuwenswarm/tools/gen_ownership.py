#!/usr/bin/env python3
# coding: utf-8
"""Join the workbook's 142 authoritative L2 rows with the ownership decisions.

Emits:
  traceability/142-feature-implementation-ownership.csv
  traceability/142-feature-preservation-gate.csv
and prints every count the brief asks to reconcile.

The workbook is the only source of feature identity, wording and hierarchy.
"""
from __future__ import annotations
import json, csv, sys, re, pathlib, collections

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ownership_data as D

OUT = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else pathlib.Path(".")
TRACE = OUT / "traceability"
TRACE.mkdir(parents=True, exist_ok=True)

rows = json.load(open(HERE / "workbook142.json", encoding="utf-8"))
assert len(rows) == 142, f"workbook yielded {len(rows)} L2 rows, expected 142"

PREFIX = {"Workflow": "WF", "Foundation": "FN", "Vertical": "VT"}
DEC_PHASE_HINT = {}   # decision -> nothing; phase comes from group/row

# ---------------------------------------------------------------- assemble rows
out, seen_ids, missing = [], set(), []
counter = collections.Counter()
for r in rows:
    plane = r["plane"]
    counter[plane] += 1
    fid = f"{PREFIX[plane]}-{counter[plane]:02d}"
    assert fid not in seen_ids, f"duplicate id {fid}"
    seen_ids.add(fid)

    g = D.GROUP.get((plane, r["l1"]))
    if g is None:
        raise SystemExit(f"no group defaults for {(plane, r['l1'])}")
    d = D.ROW.get(fid)
    if d is None:
        missing.append((fid, r["l1"], r["l2_raw"]))
        d = {}
    m = dict(g); m.update(d)

    # the workbook's own wording, never paraphrased
    l2_num = re.match(r'^\s*(\d+)\.\s*(.*)$', r["l2_raw"])
    l2_text = l2_num.group(2) if l2_num else r["l2_raw"]

    slices = d.get("slices") or []
    out.append(collections.OrderedDict([
        ("feature_id", fid),
        ("plane", plane),
        ("sheet", r["sheet"]),
        ("l1_feature", r["l1"]),
        ("l2_feature", r["l2_raw"]),
        ("l2_description", r["l2_desc"]),
        ("intended_user_outcome", d.get("acc", "")),
        ("semantic_owner", m.get("sem", "")),
        ("product_subsystem", m.get("subsystem", "")),
        ("runtime_implementer", m.get("run", "")),
        ("execution_mechanism", m.get("mech", "")),
        ("implementation_decision", d.get("dec", "UNRESOLVED")),
        ("existing_ai4rnd_implementation", d.get("a4", "")),
        ("existing_jiuwen_implementation", d.get("jw", "")),
        ("reusable_evidence", d.get("ev", "")),
        ("missing_work", d.get("miss", "")),
        ("persistence_authority", m.get("persist", "")),
        ("data_graph", d.get("graph", "")),
        ("verification_authority", m.get("verify", "")),
        ("acceptance_evidence_or_test", d.get("acc", "")),
        ("product_surface", m.get("surface", "")),
        ("delivery_phase", m.get("phase", "")),
        ("confidence", d.get("conf", "LOW")),
        ("evidence_class", d.get("ec", "INF")),
        ("implementation_slices", " | ".join(slices)),
        ("assumptions_open_questions", d.get("note", "")),
        ("_pclass", m.get("pclass", "sem")),
    ]))

if missing:
    print("!! rows with no decision entry: %d" % len(missing))
    for fid, l1, l2 in missing[:20]:
        print("   %s  [%s] %s" % (fid, l1, l2))
    raise SystemExit("every one of the 142 rows must carry an explicit decision")

# ---------------------------------------------------------------- quality gates
assert len(out) == 142
assert len(seen_ids) == 142, "duplicate stable ids"
assert counter["Workflow"] == 54 and counter["Foundation"] == 65 and counter["Vertical"] == 23, counter
l1s = {(o["plane"], o["l1_feature"]) for o in out}
assert len(l1s) == 25, f"{len(l1s)} L1 groups, expected 25"
wb_pairs = {(r["plane"], r["l2_raw"]) for r in rows}
csv_pairs = {(o["plane"], o["l2_feature"]) for o in out}
assert wb_pairs == csv_pairs, "row set drifted from the workbook"

# ------------------------------------------------------------ ownership CSV out
cols = [k for k in out[0] if not k.startswith("_")]
with (TRACE / "142-feature-implementation-ownership.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for o in out:
        w.writerow({k: o[k] for k in cols})

# ------------------------------------------------------- preservation-gate CSV
VERDICT = {"P": "PRESERVED", "A": "PRESERVED WITH ADAPTATION",
           "N": "NEW BUILD REQUIRED", "U": "UNRESOLVED", "D": "DROPPED"}
gate_rows = []
for o in out:
    rule = D.PRESERVE_RULES[o["_pclass"]]
    row = collections.OrderedDict([("feature_id", o["feature_id"]),
                                   ("plane", o["plane"]),
                                   ("l1_feature", o["l1_feature"]),
                                   ("l2_feature", o["l2_feature"])])
    for opt in "ABCDE":
        v = rule[opt]
        if D.BUILD_FORCES_NEW and o["implementation_decision"] == "BUILD" and v in ("P", "A"):
            v = "N"          # nothing exists to preserve
        if o["implementation_decision"] == "UNRESOLVED":
            v = "U"
        row[f"option_{opt}"] = VERDICT[v]
    gate_rows.append(row)

with (TRACE / "142-feature-preservation-gate.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(gate_rows[0]))
    w.writeheader(); w.writerows(gate_rows)

# ------------------------------------------------------------------ reconcile
def tally(key):
    return collections.Counter(o[key] for o in out)

print("=" * 74)
print("WORKBOOK RECONCILIATION")
print("  planes: Workflow %d + Foundation %d + Vertical %d = %d"
      % (counter["Workflow"], counter["Foundation"], counter["Vertical"], len(out)))
print("  L1 groups: %d   stable ids: %d   duplicates: %d"
      % (len(l1s), len(seen_ids), 142 - len(seen_ids)))

print("\nBY PLANE AND L1 GROUP")
per = collections.Counter((o["plane"], o["l1_feature"]) for o in out)
for (p, l1), n in sorted(per.items(), key=lambda x: (["Workflow","Foundation","Vertical"].index(x[0][0]),)):
    print("  %-11s %-52s %3d" % (p, l1[:52], n))

for label, key in [("SEMANTIC OWNER", "semantic_owner"),
                   ("RUNTIME IMPLEMENTER", "runtime_implementer"),
                   ("IMPLEMENTATION DECISION", "implementation_decision"),
                   ("DELIVERY PHASE", "delivery_phase"),
                   ("CONFIDENCE", "confidence"),
                   ("EVIDENCE CLASS", "evidence_class")]:
    print("\n%s" % label)
    for k, v in tally(key).most_common():
        print("  %-52s %3d" % (k or "(unset)", v))

print("\nPRESERVATION GATE - rows per verdict per option")
hdr = "  %-28s" % "verdict" + "".join("%9s" % f"opt {o}" for o in "ABCDE")
print(hdr)
for v in ["PRESERVED", "PRESERVED WITH ADAPTATION", "NEW BUILD REQUIRED", "UNRESOLVED", "DROPPED"]:
    line = "  %-28s" % v
    for opt in "ABCDE":
        line += "%9d" % sum(1 for g in gate_rows if g[f"option_{opt}"] == v)
    print(line)
for opt in "ABCDE":
    tot = sum(1 for g in gate_rows if g[f"option_{opt}"])
    assert tot == 142, f"option {opt} evaluated {tot} rows"
print("  every option evaluated all 142 rows: yes")

sl = [o for o in out if o["implementation_slices"]]
print("\nCROSS-LAYER FEATURES WITH IMPLEMENTATION SLICES: %d" % len(sl))
for o in sl:
    print("  %s %s" % (o["feature_id"], o["l2_feature"]))
    for s in o["implementation_slices"].split(" | "):
        print("      - %s" % s)

unres = [o for o in out if o["implementation_decision"] == "UNRESOLVED"
         or o["semantic_owner"] == "Unresolved"]
print("\nUNRESOLVED OWNERSHIP OR PRODUCT DEFINITION: %d" % len(unres))
for o in unres:
    print("  %s %s -- %s" % (o["feature_id"], o["l2_feature"], o["assumptions_open_questions"][:90]))

print("\nUNVERIFIED REUSE CLAIMS (decision REUSE with evidence class DOC or INF)")
uv = [o for o in out if o["implementation_decision"] == "REUSE" and o["evidence_class"] in ("DOC", "INF")]
for o in uv:
    print("  %s %-46s %s" % (o["feature_id"], o["l2_feature"][:46], o["evidence_class"]))
print("  total: %d" % len(uv))
print("=" * 74)
print("wrote %s" % (TRACE / "142-feature-implementation-ownership.csv"))
print("wrote %s" % (TRACE / "142-feature-preservation-gate.csv"))
