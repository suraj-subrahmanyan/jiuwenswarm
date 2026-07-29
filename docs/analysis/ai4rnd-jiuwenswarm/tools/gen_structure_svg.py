#!/usr/bin/env python3
# coding: utf-8
"""Generate the four-layer integration-structure diagram as deterministic SVG.

Same rationale and conventions as gen_e2e_svg.py: the offline Mermaid layout
cannot hold horizontal layers steady once cross-layer edges are added, so this
diagram is authored directly, themed via the site's CSS custom properties.
"""

parts = []
A = parts.append
A('<svg viewBox="0 0 1190 448" width="1190" xmlns="http://www.w3.org/2000/svg" '
  'font-family="inherit" role="img" aria-label="Recommended integration structure">')
A('<defs><marker id="ah2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
  'markerHeight="7" orient="auto-start-reverse">'
  '<path d="M0 0L10 5L0 10z" fill="var(--subtle)"/></marker></defs>')

BANDS = [
    ("JiuwenSwarm — application foundation",      8,   96),
    ("AI4RnD — product core (permanent)",         112, 104),
    ("AI4RnD–Jiuwen integration bridge",          224, 104),
    ("OpenJiuwen — execution mechanisms",         336, 96),
]
for name, y, h in BANDS:
    A(f'<rect x="8" y="{y}" width="1174" height="{h}" rx="8" '
      'fill="var(--canvas)" stroke="var(--line)"/>')
    A(f'<text x="24" y="{y+24}" font-size="12.5" font-weight="640" '
      'fill="var(--primary-ink)">' + name + '</text>')

def node(x, y, w, h, lines):
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" '
      'fill="var(--surface)" stroke="var(--line-strong)"/>')
    n = len(lines)
    for i, ln in enumerate(lines):
        fw = ' font-weight="640"' if i == 0 else ""
        fill = "var(--ink)" if i == 0 else "var(--muted)"
        fs = 12.5 if i == 0 else 11.5
        yy = y + h/2 + (i - (n-1)/2) * 14 + 4
        A(f'<text x="{x+w/2}" y="{yy:.0f}" font-size="{fs}" text-anchor="middle"'
          f'{fw} fill="{fill}">' + ln + '</text>')

def path(d, dashed=False):
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    A(f'<path d="{d}" fill="none" stroke="var(--subtle)" stroke-width="1.5"'
      f'{dash} marker-end="url(#ah2)"/>')

def label(x, y, text):
    A(f'<text x="{x}" y="{y}" font-size="11" text-anchor="start" '
      'fill="var(--muted)">' + text + '</text>')

# layer 1
node(240, 42, 200, 44, ["Channels · Gateway"])
node(480, 42, 200, 44, ["Sessions · workspace"])
node(720, 42, 430, 44, ["UI shell · accounts · providers · config · packaging"])
# layer 2
node(40, 146, 240, 52, ["Project subsystem", "record · Contract · budget · status"])
node(320, 146, 250, 52, ["Intention Compiler · Planner", "→ semantic TaskGraph"])
node(610, 146, 230, 52, ["Capability Capsules ·", "Logical Operators"])
node(880, 146, 270, 52, ["Evidence · gates · evaluators", "data foundations · governed RSI"])
# layer 3
node(320, 258, 250, 52, ["Compiler", "ready sub-plan → execution spec"])
node(610, 258, 230, 52, ["Capability & model binding", "honest stall · no substitution"])
node(880, 258, 270, 52, ["Fact converter", "receipts → evidence & state"])
# layer 4
node(40, 370, 800, 44, ["Core Workflow · SwarmFlow · DeepAgent · Dynamic Team · code mode / worktrees"])

path("M520 86 L200 146");   label(300, 124, "requests · sessions")
path("M445 198 L445 258");  label(453, 232, "ready sub-plans")
path("M725 198 L725 258");  label(733, 232, "qualified capsules")
path("M1015 258 L1015 198", dashed=True); label(1023, 232, "evidence · verified state")
path("M445 310 L445 370");  label(453, 344, "stages · scripts")
path("M725 310 L725 370");  label(733, 344, "bound agent calls")
path("M840 392 L1015 392 L1015 310", dashed=True); label(860, 384, "execution facts")
A('</svg>')
print("\n".join(parts))
