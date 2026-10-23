#!/usr/bin/env python3
"""Bundle the phase documents of one run into a single HTML file.

    python3 scripts/build_html.py output/<slug> [review.html]

Every .md the run has produced so far goes in, in phase order, with the PNGs
embedded, so the file opens in any browser on any OS with nothing installed.
Run it after each phase to refresh the review copy; at the end it is the
HTML output next to the PPTX and PDF carousels.
"""
import base64
import html
import re
import sys
from pathlib import Path

ORDER = [
    "gap_analysis.md", "open_questions.md", "explore_notes.md",
    "high_level_design.md", "component_arrangement.md",
    "system_description.md", "gate_checklist.md",
]

try:
    import markdown
    def to_html(text):
        return markdown.markdown(text, extensions=["tables", "fenced_code", "toc"])
except ImportError:  # ponytail: raw text fallback; `pip install markdown` for rendered headings/tables
    def to_html(text):
        return "<pre>" + html.escape(text) + "</pre>"

STYLE = """
body{font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem;color:#1a1a2e}
nav{position:sticky;top:0;background:#fff;border-bottom:1px solid #ddd;padding:.5rem 0;font-size:.9rem}
nav a{margin-right:1rem}
section{border-top:3px solid #e8e8ee;margin-top:3rem;padding-top:1rem}
table{border-collapse:collapse;margin:1rem 0;font-size:.92rem}
td,th{border:1px solid #ccc;padding:.3rem .6rem;vertical-align:top}
th{background:#f3f3f7}
img{max-width:100%}
pre{background:#f3f3f7;padding:.8rem;overflow:auto;white-space:pre-wrap}
code{background:#f3f3f7;padding:0 .2em}
@media print{nav{display:none}section{page-break-before:always}}
"""


def embed_images(text, folder):
    def sub(m):
        p = folder / m.group(2)
        if p.suffix.lower() == ".png" and p.exists():
            data = base64.b64encode(p.read_bytes()).decode()
            return f"![{m.group(1)}](data:image/png;base64,{data})"
        return m.group(0)
    return re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", sub, text)


def build(folder, out):
    files = [folder / n for n in ORDER if (folder / n).exists()]
    if not files:
        sys.exit(f"no phase files in {folder}")
    title = folder.name.replace("-", " ").replace("_", " ").title()
    nav, body = [], []
    for f in files:
        sid = f.stem
        label = sid.replace("_", " ").title()
        nav.append(f'<a href="#{sid}">{label}</a>')
        body.append(f'<section id="{sid}"><h1>{label}</h1>'
                    f'{to_html(embed_images(f.read_text(encoding="utf-8"), folder))}</section>')
    out.write_text(
        f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{html.escape(title)}</title><style>{STYLE}</style></head>'
        f'<body><nav>{"".join(nav)}</nav>{"".join(body)}</body></html>',
        encoding="utf-8")
    print(f"{out} ({len(files)} documents, {out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    folder = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else folder / "review.html"
    build(folder, out)
