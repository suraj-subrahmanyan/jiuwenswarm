# coding: utf-8
"""Tiny deterministic-SVG helpers shared by the diagram generators.

All colours are CSS custom properties from the site stylesheet, so every
diagram follows the light/dark theme automatically."""


class SVG:
    def __init__(self, w, h, title, marker="ak"):
        self.w, self.h, self.m = w, h, marker
        self.parts = [
            f'<svg viewBox="0 0 {w} {h}" width="{w}" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="inherit" role="img" aria-label="{title}">',
            f'<defs><marker id="{marker}" viewBox="0 0 10 10" refX="9" refY="5" '
            'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            '<path d="M0 0L10 5L0 10z" fill="var(--subtle)"/></marker></defs>',
        ]

    def band(self, y, h, title, x=8, w=None, title_fill="var(--primary-ink)"):
        w = (self.w - 16) if w is None else w
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
                          'fill="var(--canvas)" stroke="var(--line)"/>')
        if title:
            self.parts.append(f'<text x="{x+16}" y="{y+22}" font-size="12.5" '
                              f'font-weight="640" fill="{title_fill}">{title}</text>')

    def gutter_band(self, y, h, num, name_lines):
        self.band(y, h, "", x=126, w=self.w - 134)
        self.parts.append(f'<rect x="8" y="{y}" width="112" height="{h}" rx="8" '
                          'fill="var(--surface-quiet)" stroke="var(--line)"/>')
        if num:
            self.parts.append(f'<text x="20" y="{y+20}" font-size="15" font-weight="700" '
                              f'fill="var(--primary-ink)">{num}</text>')
        for i, ln in enumerate(name_lines):
            self.parts.append(f'<text x="20" y="{y+(38 if num else 22)+i*14}" '
                              f'font-size="10.5" fill="var(--subtle)">{ln}</text>')

    def node(self, x, y, w, lines, h=52, tag=None, tag_fill="var(--primary-ink)",
             dashed=False, fill="var(--surface)"):
        d = ' stroke-dasharray="4 3"' if dashed else ""
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" '
                          f'fill="{fill}" stroke="var(--line-strong)"{d}/>')
        n = len(lines)
        shift = 5 if tag else 0
        for i, ln in enumerate(lines):
            fw = ' font-weight="640"' if i == 0 else ""
            fl = "var(--ink)" if i == 0 else "var(--muted)"
            fs = 12.5 if i == 0 else 11
            yy = y + h / 2 + (i - (n - 1) / 2) * 13.5 + 4 + shift
            self.parts.append(f'<text x="{x+w/2:.0f}" y="{yy:.0f}" font-size="{fs}" '
                              f'text-anchor="middle"{fw} fill="{fl}">{ln}</text>')
        if tag:
            self.parts.append(f'<text x="{x+w-7}" y="{y+12}" font-size="9" '
                              f'font-weight="700" text-anchor="end" letter-spacing=".05em" '
                              f'fill="{tag_fill}">{tag}</text>')

    def store(self, x, y, w, lines, h=52):
        self.parts.append(
            f'<path d="M{x} {y+8} a {w/2} 8 0 0 1 {w} 0 v {h-16} a {w/2} 8 0 0 1 -{w} 0 z" '
            'fill="var(--surface)" stroke="var(--line-strong)"/>')
        self.parts.append(f'<path d="M{x} {y+8} a {w/2} 8 0 0 0 {w} 0" fill="none" '
                          'stroke="var(--line-strong)"/>')
        n = len(lines)
        for i, ln in enumerate(lines):
            fw = ' font-weight="640"' if i == 0 else ""
            fl = "var(--ink)" if i == 0 else "var(--muted)"
            yy = y + 10 + h / 2 + (i - (n - 1) / 2) * 13
            self.parts.append(f'<text x="{x+w/2:.0f}" y="{yy:.0f}" font-size="11" '
                              f'text-anchor="middle"{fw} fill="{fl}">{ln}</text>')

    def path(self, d, dashed=False, both=False):
        dash = ' stroke-dasharray="5 4"' if dashed else ""
        m = f' marker-end="url(#{self.m})"' + (f' marker-start="url(#{self.m})"' if both else "")
        self.parts.append(f'<path d="{d}" fill="none" stroke="var(--subtle)" '
                          f'stroke-width="1.5"{dash}{m}/>')

    def label(self, x, y, text, bold=False, anchor="middle", rotate=None,
              fill="var(--muted)", size=11):
        tr = f' transform="rotate({rotate} {x} {y})"' if rotate is not None else ""
        fw = ' font-weight="640"' if bold else ""
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" '
                          f'text-anchor="{anchor}"{fw} fill="{fill}"{tr}>{text}</text>')

    def legend(self, y, items, x=24):
        g = [f'<g font-size="11" fill="var(--muted)">']
        cx = x
        for kind, text in items:
            if kind in ("solid", "dashed"):
                d = ' stroke-dasharray="5 4"' if kind == "dashed" else ""
                g.append(f'<line x1="{cx}" y1="{y}" x2="{cx+38}" y2="{y}" '
                         f'stroke="var(--subtle)" stroke-width="1.5"{d} '
                         f'marker-end="url(#{self.m})"/>')
                cx += 46
            g.append(f'<text x="{cx}" y="{y+4}">{text}</text>')
            cx += len(text) * 6 + 34
        g.append("</g>")
        self.parts.append("".join(g))

    def out(self):
        return "\n".join(self.parts + ["</svg>"])
