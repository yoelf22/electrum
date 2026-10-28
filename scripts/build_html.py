#!/usr/bin/env python3
"""Bundle the phase documents of one run into a single HTML file.

    python3 scripts/build_html.py output/<slug> [review.html]

Every .md the run has produced so far goes in, in phase order, with the PNGs
embedded, so the file opens in any browser on any OS with nothing installed.
The page opens with the product name, an intro paragraph and a table of
contents whose entries link to each document and its sections. Run it after
each phase to refresh the review copy; build_docx.py makes the Word copy.
"""
import base64
import datetime
import html
import re
import sys
from pathlib import Path

ORDER = [
    "executive_summary.md", "gap_analysis.md", "open_questions.md", "explore_notes.md",
    "team.md", "high_level_design.md", "component_arrangement.md",
    "system_description.md", "gate_checklist.md",
]

try:
    import markdown
    from markdown.extensions.toc import slugify

    def to_html(text, prefix):
        """Render one document; heading ids are prefixed so documents never collide.
        Returns (html, level-2 headings as (id, name))."""
        md = markdown.Markdown(extensions=["tables", "fenced_code", "toc"], extension_configs={
            "toc": {"slugify": lambda v, sep: f"{prefix}-{slugify(v, sep)}"}})
        out = md.convert(text)
        heads, stack = [], list(md.toc_tokens)
        while stack:
            t = stack.pop(0)
            if t["level"] == 2:
                heads.append((t["id"], t["name"]))
            stack = t["children"] + stack
        return out, heads
except ImportError:  # ponytail: raw text fallback; `pip install markdown` for rendered headings/tables
    def to_html(text, prefix):
        return "<pre>" + html.escape(text) + "</pre>", []

STYLE = """
body{font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem;color:#1a1a2e}
nav{position:sticky;top:0;background:#fff;border-bottom:1px solid #ddd;padding:.5rem 0;font-size:.9rem}
nav a{margin-right:1rem}
header h1{margin:1.5rem 0 .2rem}
header .sub{color:#6b7479;margin:0 0 1rem}
.toc{background:#f3f3f7;padding:1rem 1.5rem;border-radius:6px}
.toc ol{margin:.2rem 0;padding-left:1.4rem}
.toc>ol>li{margin:.4rem 0;font-weight:600}
.toc ol ol{font-weight:400;font-size:.92rem;columns:2}
section{border-top:3px solid #e8e8ee;margin-top:3rem;padding-top:1rem}
table{border-collapse:collapse;margin:1rem 0;font-size:.92rem}
td,th{border:1px solid #ccc;padding:.3rem .6rem;vertical-align:top}
th{background:#f3f3f7}
img{max-width:100%}
pre{background:#f3f3f7;padding:.8rem;overflow:auto;white-space:pre-wrap}
code{background:#f3f3f7;padding:0 .2em}
@media print{nav{display:none}section{page-break-before:always}.toc ol ol{columns:1}}
"""


def embed_images(text, folder):
    def sub(m):
        p = folder / m.group(2)
        if p.suffix.lower() == ".png" and p.exists():
            data = base64.b64encode(p.read_bytes()).decode()
            return f"![{m.group(1)}](data:image/png;base64,{data})"
        return m.group(0)
    return re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", sub, text)


def product_name(folder):
    """The product's name from the first phase file that carries it, else the folder name."""
    for n, pat in (("executive_summary.md", r"#\s*Executive Summary:\s*(.+)"),
                   ("system_description.md", r"#\s*System Description:\s*(.+)"),
                   ("explore_notes.md", r"#\s*Exploration Notes\s*[—:-]\s*(.+)")):
        p = folder / n
        if p.exists() and (m := re.search(pat, p.read_text(encoding="utf-8"))):
            return m.group(1).strip()
    return folder.name.replace("-", " ").replace("_", " ").title()


def intro(folder):
    """The Solution section of the executive summary, else the Product Summary of the
    exploration notes: the first plain paragraph under that heading."""
    for n, head in (("executive_summary.md", r"^##\s*(?:\d+\.\s*)?The Solution"),
                    ("explore_notes.md", r"^##\s*Product Summary")):
        p = folder / n
        if not p.exists():
            continue
        m = re.search(head + r".*?\n(.*?)(?=^##\s|\Z)", p.read_text(encoding="utf-8"), re.M | re.S)
        if not m:
            continue
        for para in re.split(r"\n\s*\n", m.group(1)):
            s = para.strip()
            if s and s[0] not in "#|>!-`":
                return re.sub(r"\*\*|`", "", s)
    return ""


def build(folder, out):
    files = [folder / n for n in ORDER if (folder / n).exists()]
    if not files:
        sys.exit(f"no phase files in {folder}")
    title = product_name(folder)
    nav, toc, body = [], [], []
    for f in files:
        sid = f.stem
        label = sid.replace("_", " ").title()
        rendered, heads = to_html(embed_images(f.read_text(encoding="utf-8"), folder), sid)
        nav.append(f'<a href="#{sid}">{label}</a>')
        subs = "".join(f'<li><a href="#{i}">{html.escape(n)}</a></li>' for i, n in heads)
        toc.append(f'<li><a href="#{sid}">{label}</a>{f"<ol>{subs}</ol>" if subs else ""}</li>')
        body.append(f'<section id="{sid}"><h1>{label}</h1>{rendered}</section>')
    lead = intro(folder)
    head = (f'<header><h1>{html.escape(title)}</h1>'
            f'<p class="sub">Product definition · Electrum · {datetime.date.today().isoformat()}</p>'
            f'{f"<p>{html.escape(lead)}</p>" if lead else ""}'
            f'<div class="toc"><strong>Contents</strong><ol>{"".join(toc)}</ol></div></header>')
    out.write_text(
        f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{html.escape(title)}</title><style>{STYLE}</style></head>'
        f'<body><nav>{"".join(nav)}</nav>{head}{"".join(body)}</body></html>',
        encoding="utf-8")
    print(f"{out} ({len(files)} documents, {out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    folder = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else folder / "review.html"
    build(folder, out)
