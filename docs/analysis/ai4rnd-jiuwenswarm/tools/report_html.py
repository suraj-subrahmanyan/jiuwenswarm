#!/usr/bin/env python3
# coding: utf-8
"""Render REPORT.md as one self-contained offline HTML file.

No external assets: CSS inlined, all diagrams are inline SVG (no Mermaid, no
JavaScript beyond the theme toggle). Written to ai4rnd-architecture-report.html
at the package root, where the report's relative links resolve as-is.
"""
import sys, os, html, pathlib
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import mdsite as M

M.CUR_DIR = ""
body, toc = M.render((ROOT / "REPORT.md").read_text(encoding="utf-8"))
# pages under html/ prefix assets with ../ ; this file sits at the package root
body = body.replace('href="../', 'href="')
# doc links resolve to site pages
body = body.replace('href="report.html"', 'href="html/report.html"')
for slug in set(M.SLUG.values()):
    body = body.replace(f'href="{slug}"', f'href="html/{slug}"')

toc_html = ""
if toc:
    items = "".join(f'<a class="l{l}" href="#{s}">{t}</a>' for l, t, s in toc if l == 2)
    toc_html = f'<nav class="toc"><div class="toc-h">Contents</div>{items}</nav>'

CSS_EXTRA = """
.layout{display:block;max-width:960px;margin:0 auto}
main{padding:48px 28px 96px}
.crumb{margin-bottom:18px}
@media print{.toc{display:block}}
"""

doc = f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI4RnD on JiuwenSwarm — The Architecture Report</title>
<style>{M.CSS}{CSS_EXTRA}</style></head><body>
<div class="layout"><main>
<div class="crumb">Canonical report &middot; standalone offline edition &middot;
jiuwenswarm a98d7ad &middot; openjiuwen 0.1.15.post3 &middot; AI4Research d35c511</div>
<article>{toc_html}{body}</article>
</main></div>
<button class="tt" id="tt" aria-label="Toggle colour theme">&#9689;</button>
<script>(function(){{{M.THEME_JS}}})();</script>
</body></html>"""

out = ROOT / "ai4rnd-architecture-report.html"
out.write_text(doc, encoding="utf-8")
print(f"wrote {out.name}: {len(doc)//1024} KB, {doc.count('<svg')} inline SVGs, "
      f"{'NO external scripts' if 'src=' not in doc else 'WARNING: external refs'}")
