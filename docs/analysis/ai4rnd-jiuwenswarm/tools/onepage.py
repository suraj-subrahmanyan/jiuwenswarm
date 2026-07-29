#!/usr/bin/env python3
"""Single-file edition: every document on one page, same design tokens."""
import sys, os, re, html, pathlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mdsite as M

ROOT = pathlib.Path(sys.argv[1]).resolve()
parts, nav = [], []
for sec in M.SECTIONS:
    nav.append(f'<div class="navsec">{sec}</div>')
    for src, title, s in M.DOCS:
        if s != sec: continue
        p = ROOT / src
        if not p.exists(): continue
        did = "d-" + M.SLUG[src].replace(".html", "")
        nav.append(f'<a href="#{did}">{html.escape(title)}</a>')
        M.CUR_DIR = os.path.dirname(src)
        setattr(M, "CUR_DIR", os.path.dirname(src))
        body, _ = M.render(p.read_text(encoding="utf-8"))
        # rewrite cross-doc links to in-page anchors
        for s2 in M.SLUG:
            body = body.replace(f'href="{M.SLUG[s2]}"', f'href="#d-{M.SLUG[s2].replace(".html","")}"')
            body = body.replace(f'href="{M.SLUG[s2]}#', f'href="#')
        body = body.replace('href="../', 'href="')
        parts.append(f'<section id="{did}"><div class="crumb">{sec} / {html.escape(src)}</div>{body}</section>')

CSS = M.CSS + """
section{padding-bottom:64px;margin-bottom:48px;border-bottom:1px solid var(--line)}
section:last-child{border-bottom:0}
section h1{padding-top:8px}
"""
doc = f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI4RnD &times; JiuwenSwarm &mdash; Architecture Review (Revision 3)</title>
<style>{CSS}</style></head><body>
<div class="layout">
<aside><div class="brand">{M.MARK}<h1>AI4RnD &times; JiuwenSwarm</h1></div>
<p class="rev">Architecture review &middot; Rev 4</p>
{"".join(nav)}
<div class="side-foot">Single-page edition<br>jiuwenswarm @ a98d7ad<br>openjiuwen 0.1.15.post3<br>
AI4Research @ d35c511</div></aside>
<main>{"".join(parts)}</main></div>
<button class="tt" id="tt" aria-label="Toggle colour theme">&#9689;</button>
<script src="html/vendor/mermaid.min.js"></script>
<script>
(function(){{{M.THEME_JS}{M.MERMAID_JS}}})();
</script></body></html>"""
out = ROOT / "ai4rnd-architecture-review.html"
out.write_text(doc, encoding="utf-8")
ndia = doc.count('class="mermaid"')
print("  single-page: %d KB, %d documents, %d diagrams" % (len(doc)//1024, len(parts), ndia))
