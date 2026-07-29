#!/usr/bin/env python3
# coding: utf-8
"""Generate the end-to-end functional workflow diagram as deterministic SVG.

The layout algorithm in the offline Mermaid renderer cannot produce readable
swimlanes for this shape (seven lanes, cyclic control + evidence flows), so the
central diagram is authored directly. Colours come from the site's CSS custom
properties, so the SVG follows light/dark themes automatically.

Usage: python3 tools/gen_e2e_svg.py > /tmp/e2e.svg   (then embedded in 04-*.md)
"""

W, H = 1190, 918
parts = []
A = parts.append

A(f'<svg viewBox="0 0 {W} {H}" width="{W}" xmlns="http://www.w3.org/2000/svg" '
  'font-family="inherit" role="img" aria-label="End-to-end functional workflow">')
A('<defs>'
  '<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
  '<path d="M0 0L10 5L0 10z" fill="var(--subtle)"/></marker>'
  '</defs>')

# ------------------------------------------------------------------ lane bands
LANES = [
    ("1", "User and channels",                     8,   76),
    ("2", "JiuwenSwarm application",               92,  76),
    ("3", "AI4RnD product core",                   176, 236),
    ("4", "AI4RnD–Jiuwen integration bridge",      420, 168),
    ("5", "OpenJiuwen execution runtime",          596, 84),
    ("7", "External models, tools, sources",       688, 74),
    ("6", "Data, evidence and project state",      770, 124),
]
GX, GW_ = 8, 112          # label gutter
BX, BW = 126, 1056        # band area
for num, name, y, h in LANES:
    A(f'<rect x="{BX}" y="{y}" width="{BW}" height="{h}" rx="8" '
      'fill="var(--canvas)" stroke="var(--line)"/>')
    A(f'<rect x="{GX}" y="{y}" width="{GW_}" height="{h}" rx="8" '
      'fill="var(--surface-quiet)" stroke="var(--line)"/>')
    A(f'<text x="{GX+12}" y="{y+20}" font-size="15" font-weight="700" '
      'fill="var(--primary-ink)">' + num + '</text>')
    # wrapped lane name
    words, lines, cur = name.split(), [], ""
    for w_ in words:
        if len(cur) + len(w_) + 1 <= 14: cur = (cur + " " + w_).strip()
        else: lines.append(cur); cur = w_
    lines.append(cur)
    for i, ln in enumerate(lines):
        A(f'<text x="{GX+12}" y="{y+38+i*14}" font-size="10.5" '
          'fill="var(--subtle)">' + ln + '</text>')

# ----------------------------------------------------------------------- nodes
def node(x, y, w, h, lines, bold_first=False, kind="box"):
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" '
      'fill="var(--surface)" stroke="var(--line-strong)"/>')
    n = len(lines)
    for i, ln in enumerate(lines):
        fw = ' font-weight="640"' if (bold_first and i == 0) else ""
        fs = 12.5 if (bold_first and i == 0) else 11.5
        fill = "var(--ink)" if (i == 0 or not bold_first) else "var(--muted)"
        yy = y + h/2 + (i - (n-1)/2) * 14 + 4
        A(f'<text x="{x+w/2}" y="{yy:.0f}" font-size="{fs}" text-anchor="middle"'
          f'{fw} fill="{fill}">' + ln + '</text>')

def store(x, y, w, h, lines):
    A(f'<path d="M{x} {y+8} a {w/2} 8 0 0 1 {w} 0 v {h-16} a {w/2} 8 0 0 1 -{w} 0 z" '
      'fill="var(--surface)" stroke="var(--line-strong)"/>')
    A(f'<path d="M{x} {y+8} a {w/2} 8 0 0 0 {w} 0" fill="none" stroke="var(--line-strong)"/>')
    n = len(lines)
    for i, ln in enumerate(lines):
        yy = y + 10 + h/2 + (i-(n-1)/2)*13
        A(f'<text x="{x+w/2}" y="{yy:.0f}" font-size="11" text-anchor="middle" '
          'fill="var(--ink)">' + ln + '</text>')

# L1
node(226, 26, 110, 40, ["User"], True)
node(392, 26, 210, 40, ["Channel · Web UI · CLI"], True)
# L2
node(392, 112, 210, 44, ["Gateway · session"], True)
node(880, 112, 270, 44, ["Project view", "progress · approvals · deliverables"], True)
# L3
node(226, 196, 170, 48, ["Intention Compiler"], True)
node(462, 196, 120, 48, ["Planner"], True)
node(648, 196, 210, 48, ["Semantic readiness ·", "run-state authority"], True)
node(690, 308, 150, 52, ["Gate decision"], True)
node(462, 308, 140, 52, ["Repair ·", "replanning"], True)
node(900, 308, 150, 52, ["Deliverable"], True)
# L4
node(226, 440, 250, 56, ["Capability &amp; model binding", "stalls honestly — never substitutes"], True)
node(546, 440, 220, 56, ["Compiler", "progressively compiles ready sub-plans"], True)
node(836, 440, 180, 56, ["Dispatch ·", "resume · cancel"], True)
node(560, 520, 250, 50, ["Fact converter", "a None result is a failure"], True)
# L5
node(226, 612, 800, 52, ["Core Workflow · SwarmFlow · DeepAgent · Dynamic Team · code mode / worktrees"], True)
# L7
node(226, 700, 800, 44, ["Model providers · tools · literature &amp; data sources"], True)
# L6
store(236, 806, 150, 52, ["Project store", "Contract · plan · runs"])
store(416, 806, 150, 52, ["Gate ledger", "append-only"])
store(596, 806, 170, 52, ["Evidence ledger", "citation spans"])
node(806, 806, 160, 52, ["Improvement", "Proposal"], True)
store(996, 806, 150, 52, ["Typed knowledge", "graphs"])

# ----------------------------------------------------------------------- edges
def path(d, dashed=False, both=False, cls=""):
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    m = ' marker-end="url(#ah)"' + (' marker-start="url(#ah)"' if both else "")
    A(f'<path d="{d}" fill="none" stroke="var(--subtle)" stroke-width="1.5"{dash}{m}/>')

def label(x, y, text, bold=False, anchor="middle", rotate=None, fill="var(--muted)"):
    tr = f' transform="rotate({rotate} {x} {y})"' if rotate is not None else ""
    fw = ' font-weight="640"' if bold else ""
    A(f'<text x="{x}" y="{y}" font-size="11" text-anchor="{anchor}"{fw} '
      f'fill="{fill}"{tr}>' + text + '</text>')

# L1/L2
path("M336 46 L392 46")
path("M497 66 L497 112");             label(505, 94, "request", anchor="start")
path("M420 156 L280 196");            label(300, 172, "Qualified Intake", True, "start")
path("M380 196 L560 156", both=True); label(612, 150, "ambiguity Q&amp;A · confirm Contract", anchor="start")
# L3 forward
path("M396 220 L462 220");            label(429, 212, "Research", True); label(429, 236, "Contract", True)
path("M582 220 L648 220");            label(615, 190, "semantic TaskGraph", True); label(615, 258, "what must happen", fill="var(--subtle)")
path("M760 244 L760 308");            label(768, 280, "gated step done", anchor="start")
path("M690 334 L602 334");            label(646, 326, "fail")
path("M528 308 L528 244");            label(536, 280, "revised sub-plan", anchor="start")
path("M840 334 L900 334");            label(870, 326, "pass")
path("M975 308 L975 156");            label(983, 234, "Deliverable", True, "start")
path("M824 308 L940 156", both=True); label(890, 262, "human approval", anchor="start")
# L3 -> L4
path("M660 244 L660 398 L360 398 L360 440")
label(510, 380, "Logical Operator Request +", True); label(510, 394, "Capability Requirement", True)
# L4 forward
path("M476 468 L546 468");            label(511, 510, "bound capsule + executor")
path("M766 468 L836 468");            label(801, 432, "Execution Specification", True)
label(801, 508, "how ready work runs", fill="var(--subtle)")
path("M926 496 L926 612");            label(934, 560, "run", anchor="start")
# L5/L7
path("M626 664 L626 700");            label(634, 686, "model &amp; tool calls", anchor="start")
path("M685 612 L685 570");            label(693, 596, "Node Execution Receipt", True, "start")
# verified state return (right margin)
path("M810 545 L1060 545 L1060 264 L838 264 L838 244")
label(1068, 420, "verified step state", True, "start", rotate=90)
# state / evidence (dashed)
path("M800 360 L800 384 L1136 384 L1136 778 L491 778 L491 806", dashed=True)
label(955, 376, "Gate Verdict — recorded append-only", True)
path("M560 532 L178 532 L178 788 L681 788 L681 806", dashed=True)
label(360, 524, "Evidence Record", True)
path("M226 220 L205 220 L205 798 L300 798 L300 806", dashed=True)
label(198, 520, "Contract · plan · run state", rotate=-90)
path("M766 832 L806 832", dashed=True); label(786, 876, "performance history")
# progress + RSI feedback
path("M1026 638 L1108 638 L1108 156", dashed=True)
label(1120, 430, "Progress Event", True, rotate=90)
path("M886 806 L886 782 L1164 782 L1164 416 L340 416 L340 440", dashed=True)
label(1176, 600, "governed RSI loop (§5) — promoted versions govern future bindings", rotate=90)
# legend
A('<g font-size="11" fill="var(--muted)">'
  f'<line x1="{BX+8}" y1="908" x2="{BX+48}" y2="908" stroke="var(--subtle)" stroke-width="1.5" marker-end="url(#ah)"/>'
  f'<text x="{BX+56}" y="912">control / execution</text>'
  f'<line x1="{BX+196}" y1="908" x2="{BX+236}" y2="908" stroke="var(--subtle)" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#ah)"/>'
  f'<text x="{BX+244}" y="912">evidence / state</text>'
  f'<text x="{BX+400}" y="912" font-weight="640" fill="var(--muted)">bold labels</text>'
  f'<text x="{BX+478}" y="912">= the twelve hand-off objects</text>'
  '</g>')
A('</svg>')
print("\n".join(parts))
