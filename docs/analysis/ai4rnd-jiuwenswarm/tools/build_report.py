#!/usr/bin/env python3
# coding: utf-8
"""Assemble REPORT.md from the template plus generated SVG diagrams."""
import pathlib, re, subprocess, sys, os
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import gen_report_svgs as G

def gen(name):
    if name == "journey":
        return subprocess.run([sys.executable, str(HERE / "gen_journey_svg.py")],
                              capture_output=True, text=True).stdout.strip()
    return G.DIAGRAMS[name]()

t = (HERE / "REPORT.template.md").read_text(encoding="utf-8")
def sub(m):
    return "```svg\n" + gen(m.group(1)) + "\n```"
t2, n = re.subn(r"%%SVG:([a-z0-9_]+)%%", sub, t)
(ROOT / "REPORT.md").write_text(t2, encoding="utf-8")
print(f"REPORT.md written, {n} diagrams embedded, {len(t2)//1024} KB")
