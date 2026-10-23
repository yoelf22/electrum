#!/usr/bin/env python3
"""Print a specification document as plain text so the /electrum skill can read it.

Usage: python3 scripts/ingest_spec.py <file> [> output/<slug>/source_spec.md]
Formats: .txt .md .html .htm .docx .rtf .pdf .doc

Standard library only, with two optional helpers: pypdf or `pdftotext` for PDF,
macOS `textutil` for RTF and legacy .doc (RTF has a built-in fallback; .doc does not).
"""
import html
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import date
from pathlib import Path


def from_html(s):
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", s, flags=re.S | re.I)
    s = re.sub(r"<img[^>]*alt=\"([^\"]*)\"[^>]*>", r"[image: \1]", s, flags=re.I)
    s = re.sub(r"<img[^>]*>", "[image]", s, flags=re.I)
    s = re.sub(r"</t[dh]>", " | ", s, flags=re.I)
    s = re.sub(r"<br\s*/?>|</(p|div|h\d|li|tr|section|article|blockquote)>", "\n", s, flags=re.I)
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def from_docx(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    xml = re.sub(r"<w:tab/>", "\t", xml)
    xml = re.sub(r"</w:tc>", " | ", xml)
    xml = re.sub(r"</w:p>|<w:br[^>]*/>", "\n", xml)
    return html.unescape(re.sub(r"<[^>]+>", "", xml))


def from_rtf(s):
    # ponytail: minimal RTF stripper; covers Word/TextEdit output, not nested pictures or fields
    s = re.sub(r"\{\\(\*|fonttbl|colortbl|stylesheet|info)[^{}]*(\{[^{}]*\}[^{}]*)*\}", "", s)  # metadata groups
    s = re.sub(r"\\'([0-9a-fA-F]{2})", lambda m: bytes.fromhex(m.group(1)).decode("cp1252", "replace"), s)
    s = re.sub(r"\\u(-?\d+)\??", lambda m: chr(int(m.group(1)) % 65536), s)
    s = re.sub(r"\\par[d]?\b", "\n", s)
    s = re.sub(r"\\[a-zA-Z]+-?\d* ?", "", s)
    return s.replace("{", "").replace("}", "").replace("\\", "")


def via_textutil(path):
    if not shutil.which("textutil"):
        sys.exit(f"{path.suffix} needs macOS textutil, or convert the file to .docx/.pdf first")
    return subprocess.run(["textutil", "-convert", "txt", "-stdout", str(path)],
                          capture_output=True, text=True, check=True).stdout


def from_pdf(path):
    try:
        import pypdf
        return "\n".join(p.extract_text() or "" for p in pypdf.PdfReader(str(path)).pages)
    except ImportError:
        pass
    if shutil.which("pdftotext"):
        return subprocess.run(["pdftotext", "-layout", str(path), "-"],
                              capture_output=True, text=True, check=True).stdout
    sys.exit("PDF needs `pip install pypdf` or the pdftotext command")


def extract(path):
    ext = path.suffix.lower()
    if ext in (".txt", ".md"):
        return path.read_text(encoding="utf-8", errors="replace")
    if ext in (".html", ".htm"):
        return from_html(path.read_text(encoding="utf-8", errors="replace"))
    if ext == ".docx":
        return from_docx(path)
    if ext == ".rtf":
        raw = path.read_text(encoding="utf-8", errors="replace")
        return via_textutil(path) if shutil.which("textutil") else from_rtf(raw)
    if ext == ".doc":
        return via_textutil(path)
    if ext == ".pdf":
        return from_pdf(path)
    sys.exit(f"unsupported format {ext}; supported: txt md html htm docx rtf pdf doc")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = Path(sys.argv[1])
    text = extract(path)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    print(f"<!-- source: {path.name} · {path.suffix.lower().lstrip('.')} · {len(text)} chars · extracted {date.today()} -->\n")
    print(text)


if __name__ == "__main__":
    main()
