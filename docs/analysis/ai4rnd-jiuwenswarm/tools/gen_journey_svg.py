#!/usr/bin/env python3
# coding: utf-8
"""Generate the user-journey diagram (doc 07 §1) as deterministic SVG.

An eight-node left-to-right Mermaid chain exceeds the content column and forces
horizontal scrolling, so the journey is authored directly as a two-row snake,
themed via the site's CSS custom properties.
"""

parts = []
A = parts.append
A('<svg viewBox="0 0 1190 314" width="1190" xmlns="http://www.w3.org/2000/svg" '
  'font-family="inherit" role="img" aria-label="The user journey">')
A('<defs><marker id="ahj" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
  'markerHeight="7" orient="auto-start-reverse">'
  '<path d="M0 0L10 5L0 10z" fill="var(--subtle)"/></marker></defs>')

def node(x, y, w, lines, h=60):
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" '
      'fill="var(--surface)" stroke="var(--line-strong)"/>')
    n = len(lines)
    for i, ln in enumerate(lines):
        fw = ' font-weight="640"' if i == 0 else ""
        fill = "var(--ink)" if i == 0 else "var(--muted)"
        fs = 12.5 if i == 0 else 11
        yy = y + h/2 + (i - (n-1)/2) * 14 + 4
        A(f'<text x="{x+w/2}" y="{yy:.0f}" font-size="{fs}" text-anchor="middle"'
          f'{fw} fill="{fill}">' + ln + '</text>')

def path(d, dashed=False):
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    A(f'<path d="{d}" fill="none" stroke="var(--subtle)" stroke-width="1.5"'
      f'{dash} marker-end="url(#ahj)"/>')

def label(x, y, text, anchor="middle"):
    A(f'<text x="{x}" y="{y}" font-size="11" text-anchor="{anchor}" '
      'fill="var(--muted)">' + text + '</text>')

# row 1 — from need to verdicts
node(40,  56, 190, ["A need", "question · clue · material"])
node(290, 56, 220, ["Understand", "mint the Research Contract"])
node(570, 56, 220, ["Frame", "mint falsifiable claims", "and the plan"])
node(850, 56, 250, ["Establish", "build · benchmark · evaluate", "mint verdicts"])
path("M230 86 L290 86")
path("M510 86 L570 86")
path("M790 86 L850 86")
path("M975 56 L975 28 L680 28 L680 56")
label(827, 22, "claim refuted — reframe honestly")

# row 2 — delivery, closure, standing improvement
node(290, 216, 220, ["Deliver", "the evidence-backed", "deliverable"])
node(570, 216, 220, ["Close & retain", "freeze evidence ·", "keep the knowledge"])
node(850, 216, 250, ["Improve — governed", "better capsules · prompts ·", "routing · evaluators"])
path("M940 116 L940 186 L400 186 L400 216")
label(668, 178, "Contract satisfied — deliver")
path("M510 246 L570 246")
path("M790 246 L850 246", dashed=True)
label(820, 240, "run history", anchor="middle")
path("M1010 216 L1010 146 L400 146 L400 116", dashed=True)
label(668, 140, "next runs start stronger — the loop outlives every journey")
A('</svg>')
print("\n".join(parts))
