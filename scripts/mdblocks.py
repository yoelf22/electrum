"""Markdown blocks shared by the Word builders: parse() a file into blocks, runs() inline marks."""
import re

def parse(text):
    """Markdown -> list of blocks: (kind, level, payload)."""
    lines, out, i = text.split("\n"), [], 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("```"):
            lang, body = l[3:].strip(), []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                body.append(lines[i]); i += 1
            out.append(("code", 0, (lang, body)))
        elif l.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                if not re.match(r"^\|[\s:|-]+\|?\s*$", lines[i]):
                    rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            out.append(("table", 0, rows)); continue
        elif m := re.match(r"^(#{1,4})\s+(.*)$", l):
            out.append(("h", len(m[1]), m[2].strip()))
        elif m := re.match(r"^>\s?-?\s*(.*)$", l):
            if m[1].strip(): out.append(("prompt", 0, m[1]))
        elif m := re.match(r"^!\[[^\]]*\]\(([^)]+)\)", l):
            out.append(("img", 0, m[1]))
        elif m := re.match(r"^(\s*)- \[[ xX]\]\s+(.*)$", l):
            out.append(("check", 0, m[2]))
        elif m := re.match(r"^(\s*)[-*]\s+(.*)$", l):
            out.append(("bullet", len(m[1]) // 2, m[2]))
        elif m := re.match(r"^\s*(\d+)\.\s+(.*)$", l):
            out.append(("num", 0, f"{m[1]}. {m[2]}"))
        elif re.match(r"^---+\s*$", l):
            pass
        elif m := re.match(r"^\*([^*].*)\*$", l.strip()):
            out.append(("prompt", 0, m[1]))
        elif l.strip():
            out.append(("p", 0, l.strip()))
        i += 1
    return out

def runs(par, text, placeholder=False, **base):
    """Add **bold**, *italic*, `code` runs to a paragraph."""
    for tok in re.split(r"(\*\*[^*]+\*\*|`[^`]+`|(?<![\w*])\*[^*\s][^*]*\*(?!\w)|(?<!\w)_[^_]+_(?!\w))", text):
        if not tok: continue
        fmt = dict(base)
        if tok.startswith("**"): tok, fmt["bold"] = tok[2:-2], True
        elif tok.startswith("`"): tok, fmt["font"] = tok[1:-1], "Consolas"
        elif tok[0] in "*_" and tok[-1] == tok[0] and len(tok) > 2: tok, fmt["italic"] = tok[1:-1], True
        r = par.add_run(tok)
        if placeholder: r.style = "Placeholder Text"
        if fmt.get("bold"): r.bold = True
        if fmt.get("italic"): r.italic = True
        if fmt.get("font"): r.font.name = fmt["font"]
        if fmt.get("color"): r.font.color.rgb = fmt["color"]
        if fmt.get("size"): r.font.size = fmt["size"]
    return par
