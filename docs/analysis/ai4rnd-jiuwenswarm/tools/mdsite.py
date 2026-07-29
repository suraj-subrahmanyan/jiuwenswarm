#!/usr/bin/env python3
"""Render the AI4RnD x JiuwenSwarm analysis as a polished static HTML site.

Design tokens are taken from AI4Research's own DESIGN.md: Huawei black / white /
red, red rationed as a SIGNAL (<10% of any view), amber for blocked, quiet ink
for done (no green), pill controls, 4px rhythm.
"""
from __future__ import annotations
import html, os, re, pathlib, sys, json

ROOT = pathlib.Path(sys.argv[1]).resolve()
OUT = ROOT / "html"
OUT.mkdir(exist_ok=True)

# ---------------------------------------------------------------- document set
DOCS = [
    ("README.md",                         "Overview & verdict",        "Start"),
    ("15-correction-log.md",              "Correction log",            "Start"),
    ("20-feature-implementation-ownership.md", "Feature ownership matrix", "Decision"),
    ("16-jiuwen-execution-mechanisms.md", "Jiuwen execution mechanisms","Evidence"),
    ("17-taskgraph-verdict.md",           "TaskGraph verdict",         "Decision"),
    ("19-product-layers-and-ux.md",       "Product layers & UX",       "Decision"),
    ("07-architecture-options.md",        "Architecture options",      "Decision"),
    ("08-recommended-architecture.md",    "Recommended architecture",  "Decision"),
    ("18-evolution-governance.md",        "Evolution governance",      "Decision"),
    ("09-implementation-plan.md",         "Staged path",               "Decision"),
    ("00-intended-product-model.md",      "Intended product model",    "Product"),
    ("13-maturity-map.md",                "Maturity map",              "Product"),
    ("14-reuse-vs-build-map.md",          "Reuse vs build",            "Product"),
    ("traceability/142-feature-matrix.md","142-feature matrix",        "Product"),
    ("01-jiuwenswarm-architecture.md",    "JiuwenSwarm architecture",  "Systems"),
    ("02-ai4rnd-architecture.md",         "AI4RnD architecture",       "Systems"),
    ("03-workflow-traces.md",             "Workflow traces",           "Systems"),
    ("04-component-comparison.md",        "Component comparison",      "Systems"),
    ("05-capability-matrix.md",           "Capability matrix",         "Systems"),
    ("06-integration-challenges.md",      "Integration challenges",    "Systems"),
    ("12-verification-appendix.md",       "Verification appendix",     "Evidence"),
    ("11-evidence-appendix.md",           "Evidence appendix",         "Evidence"),
    ("10-risks-assumptions-open-questions.md","Risks & open questions","Evidence"),
    ("diagrams/README.md",                "Diagram index",             "Evidence"),
]
SECTIONS = ["Start", "Decision", "Product", "Systems", "Evidence"]
SLUG = {src: re.sub(r'[^a-z0-9]+', '-', src.lower().replace(".md", "")).strip('-') + ".html"
        for src, _, _ in DOCS}

# ---------------------------------------------------------------- chip styling
CHIP = {
    # evidence class
    "EXEC": "ok", "SRC": "neutral", "DOC": "warn", "INF": "warn", "UNK": "warn",
    # coverage
    "FULL": "ok", "PARTIAL": "warn", "NONE": "bad", "ADJACENT": "warn",
    # disposition
    "REUSE-JW": "ok", "PORT": "accent", "ADAPT": "warn", "BUILD": "bad",
    "DEFER": "neutral", "UPSTREAM": "neutral", "SERVICE": "neutral",
    # Revision 4 implementation decisions
    "REUSE": "ok", "CONFIGURE": "ok", "EXTEND": "accent", "UNRESOLVED": "warn",
    # Revision 4 preservation-gate verdicts
    "PRESERVED": "ok", "PRESERVED WITH ADAPTATION": "warn",
    "NEW BUILD REQUIRED": "bad", "DROPPED": "bad",
    # maturity
    "ACTIVE": "ok", "IMPL-UNWIRED": "accent", "SCAFFOLD": "warn",
    "SPEC": "warn", "ABSENT": "bad",
    # firmness
    "FIRM": "neutral", "DEBATED": "warn", "ASPIRE": "warn",
    # capability matrix codes
    "P": "ok", "~P": "warn", "X": "accent", "I": "warn", "U": "bad",
    "S": "neutral", "M": "bad",
}
CHIP_RE = re.compile(r'^(' + '|'.join(re.escape(k) for k in
                     sorted(CHIP, key=len, reverse=True)) + r')$')


def inline(t: str, depth: int = 0) -> str:
    t = html.escape(t, quote=False)
    t = re.sub(r'`([^`]+)`', lambda m: f'<code>{m.group(1)}</code>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\*\w])\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
               lambda m: f'<a href="{link(m.group(2))}">{m.group(1)}</a>', t)
    # bare evidence tags -> chips
    t = re.sub(r'(?<![\w>])\[(V-\d+|E-[JA]\d+)\](?!\()',
               r'<span class="tag">\1</span>', t)
    return t


CUR_DIR = ""   # directory of the markdown file currently being rendered


def link(href: str) -> str:
    if href.startswith(("http://", "https://", "#", "mailto:")):
        return html.escape(href, quote=True)
    frag = ""
    if "#" in href:
        href, frag = href.split("#", 1)
        frag = "#" + frag
    if not href:
        return html.escape(frag, quote=True)
    base = href.split("/")[-1]
    for src in SLUG:
        if src.split("/")[-1] == base:
            return SLUG[src] + frag
    # non-document asset: resolve against the source file's directory, then
    # re-base for pages that live in html/
    target = os.path.normpath(os.path.join(CUR_DIR, href)) if CUR_DIR else href
    return html.escape("../" + target.replace(os.sep, "/") + frag, quote=True)


def cell(c: str) -> str:
    s = c.strip()
    core = re.sub(r'^\*\*|\*\*$', '', s).strip().strip('`')
    m = CHIP_RE.match(core)
    if m and len(s) <= len(core) + 4:
        return f'<span class="chip {CHIP[core]}">{html.escape(core)}</span>'
    out = inline(s)
    out = out.replace("✅", '<span class="ic ok">✓</span>')
    out = out.replace("✗", '<span class="ic bad">✗</span>')
    out = out.replace("❌", '<span class="ic bad">✗</span>')
    out = out.replace("⚠️", '<span class="ic warn">!</span>')
    out = out.replace("⚠", '<span class="ic warn">!</span>')
    out = out.replace("⭐", '<span class="ic star">★</span>')
    return out


def slugify(text: str) -> str:
    t = re.sub(r'<[^>]+>', '', text)
    t = re.sub(r'[`*_]', '', t)
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')[:60]


def render(md: str):
    """markdown -> (html, toc)"""
    lines = md.split("\n")
    out, toc = [], []
    i = 0
    while i < len(lines):
        ln = lines[i]

        if ln.startswith("```"):
            lang = ln[3:].strip()
            body = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                body.append(lines[i]); i += 1
            i += 1
            code = "\n".join(body)
            if lang == "mermaid":
                out.append(f'<div class="fig"><pre class="mermaid">{html.escape(code)}</pre></div>')
            else:
                out.append(f'<pre><code>{html.escape(code)}</code></pre>')
            continue

        # table
        if ln.lstrip().startswith("|") and i + 1 < len(lines) and \
                re.match(r'^\s*\|[\s:\-|]+\|\s*$', lines[i + 1]):
            hdr = [c for c in ln.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append([c for c in lines[i].strip().strip("|").split("|")])
                i += 1
            th = "".join(f"<th>{inline(h.strip())}</th>" for h in hdr)
            body = ""
            for r in rows:
                body += "<tr>" + "".join(f"<td>{cell(c)}</td>" for c in r) + "</tr>"
            out.append(f'<div class="tw"><table><thead><tr>{th}</tr></thead>'
                       f'<tbody>{body}</tbody></table></div>')
            continue

        m = re.match(r'^(#{1,4})\s+(.*)$', ln)
        if m:
            lvl, raw = len(m.group(1)), m.group(2).rstrip()
            sid = slugify(raw)
            if lvl <= 3:
                toc.append((lvl, re.sub(r'<[^>]+>', '', inline(raw)), sid))
            out.append(f'<h{lvl} id="{sid}">'
                       f'<a class="anchor" href="#{sid}" aria-hidden="true">#</a>'
                       f'{inline(raw)}</h{lvl}>')
            i += 1
            continue

        if ln.lstrip().startswith(">"):
            body = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                body.append(re.sub(r'^\s*>\s?', '', lines[i])); i += 1
            sub, _ = render("\n".join(body))
            out.append(f'<blockquote>{sub}</blockquote>')
            continue

        if re.match(r'^\s*(?:[-*+]|\d+\.)\s+', ln):
            block = []
            while i < len(lines) and (re.match(r'^\s*(?:[-*+]|\d+\.)\s+', lines[i])
                                      or (lines[i].startswith(("   ", "\t")) and lines[i].strip())):
                block.append(lines[i]); i += 1
            out.append(render_list(block))
            continue

        if re.match(r'^\s*(---+|\*\*\*+)\s*$', ln):
            out.append("<hr>"); i += 1; continue

        if not ln.strip():
            i += 1; continue

        para = []
        while i < len(lines) and lines[i].strip() and \
                not re.match(r'^\s*(#{1,4}\s|\||```|>|---+\s*$)', lines[i]) and \
                not re.match(r'^\s*(?:[-*+]|\d+\.)\s+', lines[i]):
            para.append(lines[i].strip()); i += 1
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
    return "\n".join(out), toc


def render_list(block):
    items, cur, indent = [], None, None
    for ln in block:
        m = re.match(r'^(\s*)(?:[-*+]|\d+\.)\s+(.*)$', ln)
        if m:
            if cur is not None:
                items.append(cur)
            indent = len(m.group(1))
            cur = [m.group(2)]
        elif cur is not None:
            cur.append(ln.strip())
    if cur is not None:
        items.append(cur)
    ordered = bool(re.match(r'^\s*\d+\.', block[0]))
    tag = "ol" if ordered else "ul"
    li = "".join(f"<li>{inline(' '.join(x))}</li>" for x in items)
    return f"<{tag}>{li}</{tag}>"


# ---------------------------------------------------------------- stylesheet
CSS = """
/* Tokens from AI4Research DESIGN.md — Huawei black/white/red.
   Red is a SIGNAL (<10% of any view), never a field. Amber = blocked.
   Done is quiet ink + a check — no green as a brand colour. */
:root{
  --ink:#1a1b1d; --canvas:#fff; --surface:#fafafb; --surface-quiet:#f4f4f6;
  --muted:#54565c; --subtle:#6e7077; --faint:#d8d9dd;
  --line:#e6e6ea; --line-soft:#efeff1; --line-strong:#d3d4d9;
  --primary:#cf0a2c; --primary-ink:#a60822;
  --blocked:#b26a00; --blocked-fill:#fbefd0;
  --complete:#3a3b40; --ok-fill:#eef0ef;
  --mono:"Geist Mono",ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;
  --sans:"Schibsted Grotesk",-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
  --ease:cubic-bezier(.16,1,.3,1);
  --sidebar:300px;
}
@media (prefers-color-scheme:dark){
  :root{
    --ink:#e8e8ea; --canvas:#131316; --surface:#191a1d; --surface-quiet:#1f2024;
    --muted:#a4a6ac; --subtle:#8b8d94; --faint:#3a3b40;
    --line:#2a2b30; --line-soft:#232428; --line-strong:#3a3b40;
    --primary:#ff5d74; --primary-ink:#ff8397;
    --blocked:#e0a355; --blocked-fill:#3a2e18;
    --complete:#c8c9cd; --ok-fill:#22242a;
  }
}
:root[data-theme=dark]{
  --ink:#e8e8ea; --canvas:#131316; --surface:#191a1d; --surface-quiet:#1f2024;
  --muted:#a4a6ac; --subtle:#8b8d94; --faint:#3a3b40;
  --line:#2a2b30; --line-soft:#232428; --line-strong:#3a3b40;
  --primary:#ff5d74; --primary-ink:#ff8397;
  --blocked:#e0a355; --blocked-fill:#3a2e18; --complete:#c8c9cd; --ok-fill:#22242a;
}
:root[data-theme=light]{
  --ink:#1a1b1d; --canvas:#fff; --surface:#fafafb; --surface-quiet:#f4f4f6;
  --muted:#54565c; --subtle:#6e7077; --faint:#d8d9dd;
  --line:#e6e6ea; --line-soft:#efeff1; --line-strong:#d3d4d9;
  --primary:#cf0a2c; --primary-ink:#a60822;
  --blocked:#b26a00; --blocked-fill:#fbefd0; --complete:#3a3b40; --ok-fill:#eef0ef;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:24px}
body{margin:0;background:var(--canvas);color:var(--ink);font-family:var(--sans);
  font-size:16px;line-height:1.65;-webkit-font-smoothing:antialiased;
  font-variant-numeric:tabular-nums}
.layout{display:grid;grid-template-columns:var(--sidebar) minmax(0,1fr);max-width:1560px;margin:0 auto}

/* ---- sidebar ---- */
aside{position:sticky;top:0;height:100vh;overflow-y:auto;padding:32px 20px 48px;
  border-right:1px solid var(--line);background:var(--surface)}
.brand{display:flex;align-items:center;gap:10px;margin-bottom:2px}
.mark{flex:none}
.brand h1{font-size:15px;font-weight:770;letter-spacing:-.014em;margin:0;line-height:1.25}
.rev{font-size:11px;font-weight:660;color:var(--primary-ink);letter-spacing:.04em;
  text-transform:uppercase;margin:0 0 22px 30px}
.navsec{font-size:11px;font-weight:660;letter-spacing:.07em;text-transform:uppercase;
  color:var(--subtle);margin:20px 0 6px 10px}
aside a{display:block;padding:6px 10px;border-radius:6px;color:var(--muted);
  text-decoration:none;font-size:13.5px;line-height:1.4;transition:background 120ms var(--ease)}
aside a:hover{background:var(--canvas);color:var(--ink)}
aside a.on{background:var(--surface-quiet);color:var(--ink);font-weight:500;position:relative}
aside a.on::before{content:"";position:absolute;left:0;top:7px;bottom:7px;width:2px;
  border-radius:999px;background:var(--primary)}
.side-foot{margin-top:28px;padding-top:16px;border-top:1px solid var(--line);
  font-size:11.5px;color:var(--subtle);font-family:var(--mono);line-height:1.7}

/* ---- main ---- */
main{padding:40px 56px 96px;min-width:0}
.crumb{font-family:var(--mono);font-size:11.5px;color:var(--subtle);
  letter-spacing:.02em;margin-bottom:6px}
article{max-width:none}
h1,h2,h3,h4{letter-spacing:-.014em;scroll-margin-top:24px}
h1{font-size:32px;font-weight:770;line-height:1.18;margin:.1em 0 .55em}
h2{font-size:21px;font-weight:660;margin:2.1em 0 .6em;padding-top:.6em;
  border-top:1px solid var(--line-soft)}
h2:first-of-type{border-top:none;padding-top:0}
h3{font-size:16.5px;font-weight:660;margin:1.7em 0 .45em}
h4{font-size:14.5px;font-weight:660;color:var(--muted);margin:1.4em 0 .35em}
.anchor{position:absolute;margin-left:-1.05em;color:var(--faint);text-decoration:none;
  opacity:0;transition:opacity 120ms var(--ease);font-weight:400}
h1:hover .anchor,h2:hover .anchor,h3:hover .anchor,h4:hover .anchor{opacity:1}
p{margin:.75em 0;max-width:78ch}
ul,ol{padding-left:20px;max-width:78ch}
li{margin:.32em 0}
li::marker{color:var(--subtle)}
a{color:var(--primary-ink);text-decoration:none;border-bottom:1px solid var(--faint)}
a:hover{border-bottom-color:var(--primary)}
strong{font-weight:660}
hr{border:0;border-top:1px solid var(--line);margin:2.2em 0}
code{font-family:var(--mono);font-size:.855em;background:var(--surface-quiet);
  padding:.1em .38em;border-radius:4px;border:1px solid var(--line-soft)}
pre{background:var(--surface-quiet);border:1px solid var(--line);border-radius:8px;
  padding:16px 18px;overflow-x:auto;margin:1.1em 0}
pre code{background:none;border:0;padding:0;font-size:12.6px;line-height:1.62}
blockquote{margin:1.2em 0;padding:14px 18px;background:var(--surface);
  border-left:2px solid var(--primary);border-radius:0 8px 8px 0;max-width:82ch}
blockquote>:first-child{margin-top:0}blockquote>:last-child{margin-bottom:0}

/* ---- tables ---- */
.tw{overflow-x:auto;margin:1.2em 0;border:1px solid var(--line);border-radius:8px}
table{border-collapse:collapse;width:100%;font-size:13.5px}
th,td{text-align:left;padding:9px 13px;border-bottom:1px solid var(--line-soft);
  vertical-align:top}
th{background:var(--surface-quiet);font-weight:660;font-size:12.5px;
  letter-spacing:.01em;white-space:nowrap;border-bottom:1px solid var(--line)}
tbody tr:last-child td{border-bottom:none}
tbody tr:hover{background:var(--surface)}
td code{font-size:12px}

/* ---- chips ---- */
.chip{display:inline-block;padding:1px 9px;border-radius:999px;font-family:var(--mono);
  font-size:11px;font-weight:460;letter-spacing:.02em;white-space:nowrap;
  border:1px solid var(--line-strong);background:var(--surface-quiet);color:var(--muted)}
.chip.ok{background:var(--ok-fill);color:var(--complete);border-color:var(--line-strong)}
.chip.accent{background:transparent;color:var(--primary-ink);border-color:var(--primary)}
.chip.warn{background:var(--blocked-fill);color:var(--blocked);border-color:transparent}
.chip.bad{background:transparent;color:var(--primary-ink);border-color:var(--primary);
  font-weight:560}
.chip.neutral{background:var(--surface-quiet);color:var(--subtle)}
.tag{display:inline-block;font-family:var(--mono);font-size:11px;padding:0 6px;
  border-radius:4px;background:var(--surface-quiet);border:1px solid var(--line);
  color:var(--subtle)}
.ic{display:inline-block;width:16px;height:16px;line-height:16px;text-align:center;
  border-radius:999px;font-size:10.5px;font-weight:700}
.ic.ok{color:var(--complete)}
.ic.bad{color:var(--primary-ink)}
.ic.warn{color:var(--blocked)}
.ic.star{color:var(--primary)}

/* ---- figures ---- */
.fig{margin:1.4em 0;padding:20px;background:var(--surface);border:1px solid var(--line);
  border-radius:10px;overflow-x:auto}
.fig pre.mermaid{background:none;border:0;padding:0;margin:0;text-align:center}
.fig svg{max-width:none;height:auto}
.fig[data-wide]{padding-bottom:14px}
.fig pre.mermaid.raw{text-align:left;font-family:var(--mono);font-size:12px;
  white-space:pre;color:var(--muted)}
.fignote{font-size:11px;color:var(--subtle);font-family:var(--mono);margin-bottom:8px;
  letter-spacing:.02em}

/* ---- toc ---- */
.toc{margin:0 0 34px;padding:16px 18px;background:var(--surface);
  border:1px solid var(--line);border-radius:10px;max-width:78ch}
.toc-h{font-size:11px;font-weight:660;letter-spacing:.07em;text-transform:uppercase;
  color:var(--subtle);margin-bottom:8px}
.toc a{display:block;padding:2.5px 0;color:var(--muted);font-size:13.5px;border:0}
.toc a:hover{color:var(--primary-ink)}
.toc a.l3{padding-left:16px;font-size:13px;color:var(--subtle)}

/* ---- index page ---- */
.hero{padding:16px 0 32px;border-bottom:1px solid var(--line);margin-bottom:36px}
.hero h1{font-size:38px;margin-bottom:.2em}
.lede{font-size:19px;line-height:1.5;color:var(--muted);max-width:60ch;margin:0}
.lede strong{color:var(--ink);font-weight:660}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
  gap:1px;background:var(--line);border:1px solid var(--line);border-radius:10px;
  overflow:hidden;margin:30px 0 8px}
.stat{background:var(--canvas);padding:16px 18px}
.stat .n{font-size:26px;font-weight:770;letter-spacing:-.02em;line-height:1.1}
.stat .n .was{font-size:13px;font-weight:400;color:var(--subtle);
  text-decoration:line-through;margin-right:6px}
.stat .k{font-size:11.5px;color:var(--subtle);margin-top:3px;line-height:1.35}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(268px,1fr));gap:14px;
  margin:14px 0 8px}
.card{display:block;padding:16px 18px;border:1px solid var(--line);border-radius:10px;
  background:var(--canvas);text-decoration:none;color:inherit;
  transition:border-color 180ms var(--ease),transform 180ms var(--ease)}
.card:hover{border-color:var(--line-strong);transform:translateY(-1px)}
.card .ct{font-weight:660;font-size:14.5px;margin-bottom:3px;letter-spacing:-.008em}
.card .cd{font-size:12.5px;color:var(--subtle);line-height:1.5}
.card .cn{font-family:var(--mono);font-size:11px;color:var(--primary-ink);
  letter-spacing:.03em}
.sech{font-size:12px;font-weight:660;letter-spacing:.07em;text-transform:uppercase;
  color:var(--subtle);margin:34px 0 12px}

/* ---- pager ---- */
.pager{display:flex;justify-content:space-between;gap:16px;margin-top:56px;
  padding-top:22px;border-top:1px solid var(--line)}
.pager a{flex:1;padding:12px 16px;border:1px solid var(--line);border-radius:8px;
  text-decoration:none;color:inherit;transition:border-color 180ms var(--ease)}
.pager a:hover{border-color:var(--line-strong)}
.pager .d{font-size:11px;color:var(--subtle);letter-spacing:.05em;text-transform:uppercase}
.pager .t{font-weight:660;font-size:14px;margin-top:2px}
.pager .nx{text-align:right}

/* ---- theme toggle ---- */
.tt{position:fixed;right:20px;bottom:20px;width:38px;height:38px;border-radius:999px;
  border:1px solid var(--line-strong);background:var(--surface);color:var(--muted);
  cursor:pointer;font-size:15px;line-height:1;display:grid;place-items:center;z-index:20;
  transition:border-color 180ms var(--ease)}
.tt:hover{border-color:var(--primary)}
:focus-visible{outline:2px solid var(--primary);outline-offset:3px;border-radius:4px}

@media (max-width:1020px){
  .layout{grid-template-columns:1fr}
  aside{position:static;height:auto;border-right:0;border-bottom:1px solid var(--line)}
  main{padding:28px 20px 72px}
  .hero h1{font-size:29px}.lede{font-size:17px}
}
@media print{
  aside,.tt,.pager,.toc{display:none}
  .layout{display:block}main{padding:0}
  a{color:inherit;border:0}.fig,pre,.tw{break-inside:avoid}
}
"""

# Mermaid palette derived from the same DESIGN.md tokens as the CSS.
# 'base' theme + explicit variables so diagrams are monochrome ink-on-paper
# with red reserved as a signal on edges and cluster titles.
MERMAID_JS = """
  var FONT='"Schibsted Grotesk",-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif';
  var LIGHT={background:'#ffffff',mainBkg:'#fafafb',primaryColor:'#fafafb',
    primaryTextColor:'#1a1b1d',primaryBorderColor:'#d3d4d9',secondaryColor:'#f4f4f6',
    secondaryTextColor:'#1a1b1d',secondaryBorderColor:'#d3d4d9',tertiaryColor:'#ffffff',
    tertiaryTextColor:'#1a1b1d',tertiaryBorderColor:'#e6e6ea',
    nodeBorder:'#d3d4d9',clusterBkg:'#ffffff',clusterBorder:'#e6e6ea',
    lineColor:'#8b8d94',textColor:'#1a1b1d',titleColor:'#a60822',
    edgeLabelBackground:'#ffffff',labelBackground:'#ffffff',
    noteBkgColor:'#f4f4f6',noteTextColor:'#54565c',noteBorderColor:'#e6e6ea',
    actorBkg:'#fafafb',actorBorder:'#d3d4d9',actorTextColor:'#1a1b1d',
    signalColor:'#54565c',signalTextColor:'#1a1b1d',
    labelBoxBkgColor:'#f4f4f6',labelBoxBorderColor:'#d3d4d9',labelTextColor:'#1a1b1d',
    loopTextColor:'#54565c',altBackground:'#fafafb',
    sectionBkgColor:'#f4f4f6',sectionBkgColor2:'#fafafb',altSectionBkgColor:'#ffffff',
    taskBkgColor:'#f4f4f6',taskBorderColor:'#d3d4d9',taskTextColor:'#1a1b1d',
    taskTextDarkColor:'#1a1b1d',taskTextOutsideColor:'#54565c',
    activeTaskBkgColor:'#cf0a2c',activeTaskBorderColor:'#a60822',
    doneTaskBkgColor:'#e6e6ea',doneTaskBorderColor:'#d3d4d9',
    critBkgColor:'#fbefd0',critBorderColor:'#b26a00',
    gridColor:'#e6e6ea',todayLineColor:'#cf0a2c',
    transitionColor:'#8b8d94',stateBkg:'#fafafb',stateBorder:'#d3d4d9'};
  var DARK={background:'#131316',mainBkg:'#191a1d',primaryColor:'#191a1d',
    primaryTextColor:'#e8e8ea',primaryBorderColor:'#3a3b40',secondaryColor:'#1f2024',
    secondaryTextColor:'#e8e8ea',secondaryBorderColor:'#3a3b40',tertiaryColor:'#131316',
    tertiaryTextColor:'#e8e8ea',tertiaryBorderColor:'#2a2b30',
    nodeBorder:'#3a3b40',clusterBkg:'#131316',clusterBorder:'#2a2b30',
    lineColor:'#8b8d94',textColor:'#e8e8ea',titleColor:'#ff8397',
    edgeLabelBackground:'#131316',labelBackground:'#131316',
    noteBkgColor:'#1f2024',noteTextColor:'#a4a6ac',noteBorderColor:'#2a2b30',
    actorBkg:'#191a1d',actorBorder:'#3a3b40',actorTextColor:'#e8e8ea',
    signalColor:'#a4a6ac',signalTextColor:'#e8e8ea',
    labelBoxBkgColor:'#1f2024',labelBoxBorderColor:'#3a3b40',labelTextColor:'#e8e8ea',
    loopTextColor:'#a4a6ac',altBackground:'#191a1d',
    sectionBkgColor:'#1f2024',sectionBkgColor2:'#191a1d',altSectionBkgColor:'#131316',
    taskBkgColor:'#1f2024',taskBorderColor:'#3a3b40',taskTextColor:'#e8e8ea',
    taskTextDarkColor:'#e8e8ea',taskTextOutsideColor:'#a4a6ac',
    activeTaskBkgColor:'#ff5d74',activeTaskBorderColor:'#ff8397',
    doneTaskBkgColor:'#2a2b30',doneTaskBorderColor:'#3a3b40',
    critBkgColor:'#3a2e18',critBorderColor:'#e0a355',
    gridColor:'#2a2b30',todayLineColor:'#ff5d74',
    transitionColor:'#8b8d94',stateBkg:'#191a1d',stateBorder:'#3a3b40'};
  if(window.mermaid){
    var v = dark()? DARK : LIGHT; v.fontFamily = FONT; v.fontSize = '13px';
    mermaid.initialize({startOnLoad:true, securityLevel:'loose', theme:'base',
      themeVariables:v, flowchart:{curve:'basis',useMaxWidth:false,htmlLabels:true},
      sequence:{useMaxWidth:false}, gantt:{useMaxWidth:false}});
  } else {
    document.querySelectorAll('pre.mermaid').forEach(function(el){
      el.classList.add('raw');
      var n=document.createElement('div'); n.className='fignote';
      n.textContent='Diagram source (renderer unavailable offline)';
      el.parentNode.insertBefore(n, el);
    });
  }
"""

MARK = ('<svg class="mark" width="20" height="20" viewBox="0 0 20 20" fill="none" '
        'aria-hidden="true">'
        '<path d="M10 1.6c2.4 2.1 3.6 4.7 3.6 7.4 0 2.9-1.3 5.5-3.6 7.4-2.3-1.9-3.6-4.5-3.6-7.4 0-2.7 1.2-5.3 3.6-7.4z" fill="#cf0a2c"/>'
        '<path d="M10 16.4c-2.6 1.4-5 1.7-7.2 1-.5-2.2 0-4.4 1.6-6.4 2.2.3 4.1 1.5 5.6 3.5z" fill="#a60822"/>'
        '<path d="M10 16.4c2.6 1.4 5 1.7 7.2 1 .5-2.2 0-4.4-1.6-6.4-2.2.3-4.1 1.5-5.6 3.5z" fill="#7a0a1d"/>'
        '</svg>')


def sidebar(active: str) -> str:
    p = [f'<div class="brand">{MARK}<h1>AI4RnD &times; JiuwenSwarm</h1></div>',
         '<p class="rev">Architecture review &middot; Rev 4</p>']
    for sec in SECTIONS:
        p.append(f'<div class="navsec">{sec}</div>')
        for src, title, s in DOCS:
            if s != sec:
                continue
            on = " on" if SLUG[src] == active else ""
            p.append(f'<a class="doc{on}" href="{SLUG[src]}">{html.escape(title)}</a>')
    p.append('<div class="side-foot">jiuwenswarm @ a98d7ad<br>openjiuwen 0.1.15.post3<br>'
             'AI4Research @ d35c511<br>142 outcomes &middot; 29 experiments</div>')
    return "\n".join(p)


THEME_JS = """
  var KEY='ai4rnd-theme', r=document.documentElement;
  var saved=localStorage.getItem(KEY); if(saved) r.setAttribute('data-theme',saved);
  function dark(){ var a=r.getAttribute('data-theme');
    return a? a==='dark' : matchMedia('(prefers-color-scheme:dark)').matches; }
  document.getElementById('tt').onclick=function(){
    var next = dark()?'light':'dark';
    r.setAttribute('data-theme',next); localStorage.setItem(KEY,next);
    location.reload();
  };
"""


def page(title: str, active: str, body: str, crumb: str = "") -> str:
    return f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} &middot; AI4RnD &times; JiuwenSwarm</title>
<link rel="stylesheet" href="style.css">
</head><body>
<div class="layout">
<aside>{sidebar(active)}</aside>
<main>{('<div class="crumb">' + html.escape(crumb) + '</div>') if crumb else ''}{body}</main>
</div>
<button class="tt" id="tt" aria-label="Toggle colour theme">&#9689;</button>
<script src="vendor/mermaid.min.js"></script>
<script>
(function(){{{THEME_JS}{MERMAID_JS}}})();
</script></body></html>"""


# ---------------------------------------------------------------- build pages
order = [s for s, _, _ in DOCS]
built = 0
for idx, (src, title, sec) in enumerate(DOCS):
    p = ROOT / src
    if not p.exists():
        print("  MISSING", src); continue
    CUR_DIR = os.path.dirname(src)
    globals()["CUR_DIR"] = CUR_DIR
    body_html, toc = render(p.read_text(encoding="utf-8"))
    toc_html = ""
    if len(toc) > 3:
        items = "".join(
            f'<a class="l{l}" href="#{sid}">{t}</a>' for l, t, sid in toc if l in (2, 3))
        if items:
            toc_html = f'<nav class="toc"><div class="toc-h">On this page</div>{items}</nav>'
    nav = '<div class="pager">'
    if idx > 0:
        ps, pt, _ = DOCS[idx - 1]
        nav += f'<a href="{SLUG[ps]}"><div class="d">← Previous</div><div class="t">{html.escape(pt)}</div></a>'
    else:
        nav += '<a href="index.html"><div class="d">← Back</div><div class="t">Contents</div></a>'
    if idx < len(DOCS) - 1:
        ns, nt, _ = DOCS[idx + 1]
        nav += f'<a class="nx" href="{SLUG[ns]}"><div class="d">Next →</div><div class="t">{html.escape(nt)}</div></a>'
    nav += "</div>"
    (OUT / SLUG[src]).write_text(
        page(title, SLUG[src], f"<article>{toc_html}{body_html}</article>{nav}",
             crumb=f"{sec} / {src}"), encoding="utf-8")
    built += 1

# ---------------------------------------------------------------- index page
DESC = {
 "README.md":"The question, the verdict, and what executing the runtime changed in Revision 4.",
 "15-correction-log.md":"What each revision assumed too early, and why. Severity-rated.",
 "20-feature-implementation-ownership.md":"All 142 workbook outcomes: semantic owner, runtime implementer, persistence, verification, surface, decision.",
 "16-jiuwen-execution-mechanisms.md":"Bottom-up map of all five Jiuwen graph/state mechanisms.",
 "17-taskgraph-verdict.md":"Definitive answer: AI4RnD keeps a plan, not a scheduler.",
 "19-product-layers-and-ux.md":"What kind of product this is, what users select, who owns state.",
 "07-architecture-options.md":"Eight options as (entry, control plane, execution) triples.",
 "08-recommended-architecture.md":"Ten layers, ownership boundaries, the RSI loop.",
 "18-evolution-governance.md":"A governed ten-step improvement loop over agent_evolving.",
 "09-implementation-plan.md":"Seven stages, exit gates, decision points, ~14 months.",
 "00-intended-product-model.md":"The 142-feature target: workflow, foundation, vertical planes.",
 "13-maturity-map.md":"Active / unwired / scaffold / spec / absent, on both sides.",
 "14-reuse-vs-build-map.md":"Where each feature comes from: reuse, port, adapt, build.",
 "traceability/142-feature-matrix.md":"Row-by-row traceability for all 142 Level-2 features.",
 "01-jiuwenswarm-architecture.md":"Current state, corrected by execution.",
 "02-ai4rnd-architecture.md":"Current state including dormant and unwired code.",
 "03-workflow-traces.md":"Entry, planning, routing, execution, verification, recovery.",
 "04-component-comparison.md":"Component-by-component verdicts.",
 "05-capability-matrix.md":"Provided / partial / extensible / needs-internals / missing.",
 "06-integration-challenges.md":"Conflicts and blockers, ranked by constraint.",
 "12-verification-appendix.md":"Nineteen experiments with commands and results.",
 "11-evidence-appendix.md":"Source references, file and line.",
 "10-risks-assumptions-open-questions.md":"Risks, assumptions, reversals, open questions.",
 "diagrams/README.md":"All 27 diagrams in one place.",
}
NUM = {s: (s.split("/")[-1][:2] if s[:2].isdigit() or s.split("/")[-1][:2].isdigit() else "—")
       for s, _, _ in DOCS}

hero = f"""<div class="hero">
<h1>Can AI4RnD be built on JiuwenSwarm?</h1>
<p class="lede">Yes &mdash; as a <strong>mode, plus a persistent project subsystem, plus a
workspace capability registry</strong>. AI4RnD owns meaning: the research plan, capability
routing, evidence, gates, capsules and evolution governance. Jiuwen owns execution. AI4RnD
writes <strong>no scheduler</strong>.</p>
<div class="stats">
  <div class="stat"><div class="n"><span class="was">5,200</span>450</div>
    <div class="k">LOC of AI4RnD runtime code</div></div>
  <div class="stat"><div class="n"><span class="was">6</span>1</div>
    <div class="k">of 8 RSI surfaces to build</div></div>
  <div class="stat"><div class="n">23<span style="font-size:15px;color:var(--subtle)">/142</span></div>
    <div class="k">features Jiuwen covers fully</div></div>
  <div class="stat"><div class="n"><span class="was">20</span>14</div>
    <div class="k">months to complete product</div></div>
  <div class="stat"><div class="n">19</div>
    <div class="k">experiments executed</div></div>
</div>
<p style="font-size:13px;color:var(--subtle);margin-top:10px">Struck-through figures are
Revision 2&rsquo;s. See the <a href="15-correction-log.html">correction log</a>.</p>
</div>"""

cards = ""
for sec in SECTIONS:
    cards += f'<div class="sech">{sec}</div><div class="cards">'
    for src, title, s in DOCS:
        if s != sec:
            continue
        n = src.split("/")[-1][:2]
        if "/" in src:
            n = "MTX"
        elif not n.isdigit():
            n = "&mdash;"
        cards += (f'<a class="card" href="{SLUG[src]}">'
                  f'<div class="cn">{n}</div>'
                  f'<div class="ct">{html.escape(title)}</div>'
                  f'<div class="cd">{html.escape(DESC.get(src,""))}</div></a>')
    cards += "</div>"

extra = """<div class="sech">Also here</div><div class="cards">
<a class="card" href="../traceability/142-feature-matrix.csv"><div class="cn">CSV</div>
<div class="ct">Feature matrix (data)</div>
<div class="cd">All 142 rows, machine-readable.</div></a>
<a class="card" href="../ai4rnd-architecture-review.html"><div class="cn">HTML</div>
<div class="ct">Single-page edition</div>
<div class="cd">Every document on one page, for offline review or printing.</div></a>
</div>"""

(OUT / "index.html").write_text(
    page("Contents", "index.html", hero + cards + extra), encoding="utf-8")
(OUT / "style.css").write_text(CSS, encoding="utf-8")

# Vendored Mermaid renderer — the site must work with no network. Keep an
# existing copy; otherwise take one from beside this script.
vend = OUT / "vendor"
vend.mkdir(exist_ok=True)
mjs = vend / "mermaid.min.js"
if not mjs.exists():
    here = pathlib.Path(__file__).resolve().parent / "mermaid.min.js"
    if here.exists():
        mjs.write_bytes(here.read_bytes())
    else:
        print("  WARNING: html/vendor/mermaid.min.js missing — diagrams will "
              "fall back to source text. Place mermaid.min.js beside this script.")

print(f"  built {built} document pages + index + style.css -> {OUT}")
if mjs.exists():
    print(f"  vendored mermaid renderer: {mjs.stat().st_size // 1024} KB")
