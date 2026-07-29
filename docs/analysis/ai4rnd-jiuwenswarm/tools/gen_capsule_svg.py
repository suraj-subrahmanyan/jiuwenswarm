#!/usr/bin/env python3
# coding: utf-8
"""Generate the Capability Capsule lifecycle diagram as deterministic SVG.

Same rationale as gen_e2e_svg.py: the cycle (promotion and rollback feeding
the registry) defeats the offline Mermaid layout, so the diagram is authored
directly, themed via the site's CSS custom properties.
"""

parts = []
A = parts.append
A('<svg viewBox="0 0 1190 440" width="1190" xmlns="http://www.w3.org/2000/svg" '
  'font-family="inherit" role="img" aria-label="Capability Capsule lifecycle">')
A('<defs><marker id="ah3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
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
      f'{dash} marker-end="url(#ah3)"/>')

def label(x, y, text, anchor="start"):
    A(f'<text x="{x}" y="{y}" font-size="11" text-anchor="{anchor}" '
      'fill="var(--muted)">' + text + '</text>')

# row 1 — the capsule as a governed identity
node(40,  36, 170, ["Defined", "manifest authored"])
node(260, 36, 190, ["Certified", "schema + policy checks"])
node(500, 36, 170, ["Registered", "discoverable"])
node(720, 36, 200, ["Selected", "matches a step's requirement"])
node(970, 36, 180, ["Bound", "to a permitted executor"])
path("M210 62 L260 62")
path("M450 62 L500 62")
path("M670 62 L720 62")
path("M920 62 L970 62")

# row 2 — the capsule as a runtime constraint
node(970, 186, 180, ["Executed", "under declared effects"])
node(700, 186, 200, ["Verified", "independent verifier"])
node(420, 186, 210, ["Improvement candidate", "from performance history"])
path("M1060 88 L1060 186");  label(1052, 142, "in-flight runs pin their version", anchor="end")
path("M970 212 L900 212")
path("M700 212 L630 212", dashed=True)
label(602, 174, "performance history", anchor="middle")

# row 3 — the capsule as an evolution subject
node(420, 336, 210, ["Promoted", "new version, approved"])
node(720, 336, 200, ["Rolled back", "on regression"])
path("M525 238 L525 336");   label(535, 292, "governed approval (RSI loop)")
path("M630 362 L720 362", dashed=True)
path("M420 362 L230 362 L230 110 L560 110 L560 88")
label(240, 130, "promotion updates the registry")
path("M920 362 L1165 362 L1165 118 L610 118 L610 88")
label(700, 138, "rollback restores the prior version")
A('</svg>')
print("\n".join(parts))
