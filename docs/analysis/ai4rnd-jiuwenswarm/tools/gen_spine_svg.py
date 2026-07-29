#!/usr/bin/env python3
# coding: utf-8
"""Generate the state-spine diagram (doc 07 §3) as deterministic SVG.

Eight durable objects in a left-to-right Mermaid chain exceed the content
column, so the spine is authored directly as a two-row snake, themed via the
site's CSS custom properties.
"""

parts = []
A = parts.append
A('<svg viewBox="0 0 1190 300" width="1190" xmlns="http://www.w3.org/2000/svg" '
  'font-family="inherit" role="img" aria-label="The state spine">')
A('<defs><marker id="ahs" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
  'markerHeight="7" orient="auto-start-reverse">'
  '<path d="M0 0L10 5L0 10z" fill="var(--subtle)"/></marker></defs>')

def node(x, y, w, lines, h=66):
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" '
      'fill="var(--surface)" stroke="var(--line-strong)"/>')
    n = len(lines)
    for i, ln in enumerate(lines):
        fw = ' font-weight="640"' if i == 0 else ""
        fill = "var(--ink)" if i == 0 else "var(--muted)"
        fs = 12.5 if i == 0 else 10.5
        st = ' font-style="italic"' if i == n-1 and n > 2 else ""
        yy = y + h/2 + (i - (n-1)/2) * 13.5 + 4
        A(f'<text x="{x+w/2}" y="{yy:.0f}" font-size="{fs}" text-anchor="middle"'
          f'{fw}{st} fill="{fill}">' + ln + '</text>')

def path(d, dashed=False):
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    A(f'<path d="{d}" fill="none" stroke="var(--subtle)" stroke-width="1.5"'
      f'{dash} marker-end="url(#ahs)"/>')

def label(x, y, text, anchor="middle"):
    A(f'<text x="{x}" y="{y}" font-size="10.5" text-anchor="{anchor}" '
      'fill="var(--muted)">' + text + '</text>')

# row 1
node(40,  36, 230, ["Contract", "confirmed promise", "written once, then immutable"])
node(330, 36, 230, ["TaskGraph", "the living plan", "versioned on every replan"])
node(620, 36, 230, ["Claims", "falsifiable statements", "each knows what refutes it"])
node(910, 36, 240, ["Evidence", "citation-anchored records", "append-only"])
path("M270 69 L330 69")
path("M560 69 L620 69")
path("M850 69 L910 69")

# row 2 (right to left, continuing the chain)
node(910, 196, 240, ["Verdicts", "gate decisions", "append-only · writer-attributed"])
node(620, 196, 230, ["Deliverable", "claims + verdicts + evidence", "frozen at closure"])
node(330, 196, 230, ["Knowledge", "typed graph projections", "outlives the project"])
node(40,  196, 230, ["Improvements", "versioned promotions", "reversible"])
path("M1030 102 L1030 196")
path("M910 229 L850 229")
path("M620 229 L560 229")
path("M330 229 L270 229", dashed=True)

# loops
path("M960 196 L960 152 L470 152 L470 102")
label(715, 146, "verdict fails → a new plan revision — recorded evidence is never edited")
path("M155 196 L155 102", dashed=True)
label(165, 152, "improves future runs only —", anchor="start")
label(165, 166, "in-flight runs pin their versions", anchor="start")
A('</svg>')
print("\n".join(parts))
