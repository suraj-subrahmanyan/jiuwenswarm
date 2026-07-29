#!/usr/bin/env python3
# coding: utf-8
"""Generate the governed RSI loop diagram as deterministic SVG.

Same rationale as gen_e2e_svg.py: the branching loop defeats the offline
Mermaid layout, so the diagram is authored directly, themed via CSS variables.
"""

parts = []
A = parts.append
A('<svg viewBox="0 0 1190 452" width="1190" xmlns="http://www.w3.org/2000/svg" '
  'font-family="inherit" role="img" aria-label="Governed RSI loop">')
A('<defs><marker id="ah4" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
  'markerHeight="7" orient="auto-start-reverse">'
  '<path d="M0 0L10 5L0 10z" fill="var(--subtle)"/></marker></defs>')

def node(x, y, w, lines, h=52):
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
      f'{dash} marker-end="url(#ah4)"/>')

def label(x, y, text, anchor="start"):
    A(f'<text x="{x}" y="{y}" font-size="11" text-anchor="{anchor}" '
      'fill="var(--muted)">' + text + '</text>')

# row 1 — from evidence to the policy gate
node(40,  36, 190, ["Run evidence", "performance history"])
node(290, 36, 235, ["Improvement Proposal", "subject · claim · measurement"])
node(585, 36, 160, ["Risk", "classification"])
node(805, 36, 185, ["Frozen-policy check", "rejects relaxations"])
path("M230 62 L290 62", dashed=True)
path("M525 62 L585 62")
path("M745 62 L805 62")

# row 2 — evaluation, approval, rejection
node(585, 186, 220, ["Isolated evaluation", "on a held-out set"])
node(290, 186, 235, ["Human approval", "Improvements inbox"])
node(1010, 186, 140, ["Rejected"])
path("M860 88 L695 186");   label(742, 132, "clean")
path("M935 88 L1080 186");  label(1010, 132, "relaxes a", anchor="middle")
label(1030, 146, "frozen rule", anchor="middle")
path("M585 212 L525 212")
path("M407 238 L407 286 L1080 286 L1080 238"); label(700, 280, "declined", anchor="middle")

# row 3 — promotion, monitoring, outcome, registry
node(40,  336, 190, ["Registry & config", "updated, versioned"])
node(290, 336, 220, ["Versioned promotion"])
node(585, 336, 180, ["Monitoring"])
node(820, 318, 180, ["Rolled back", "on regression"], h=44)
node(820, 380, 160, ["Kept", "the new baseline"], h=44)
path("M350 238 L350 336");  label(358, 292, "approved")
path("M510 362 L585 362")
path("M765 352 L820 336");  label(776, 330, "regression")
path("M765 372 L820 396");  label(776, 402, "holds")
path("M290 362 L230 362", dashed=True)
path("M1000 336 L1030 336 L1030 434 L135 434 L135 388", dashed=True)
label(600, 428, "rollback restores the prior version", anchor="middle")
A('</svg>')
print("\n".join(parts))
