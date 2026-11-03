#!/usr/bin/env python3
"""Build the role reader: the run's documents arranged by role, in one HTML page.

    python3 scripts/build_role_reader.py output/<slug>          # writes role_reader.html
    python3 scripts/build_role_reader.py output/<slug> --keys   # lists the section keys roles.json may use

Everyone reads the executive summary and the high-level design first; each role
then gets its Must / Skim / Lookup path, its BOM lines, schedule tasks and the
decisions that bind it, and every decision traces back to the rows behind it.

The text comes from the same .md files review.html bundles, so the two cannot
differ in content. `roles.json` (written by the skill from team.md and the
documents) only says who reads what; it adds no facts. Every reference in it is
checked against the documents and the build fails on a dangling one.
"""
import datetime
import hashlib
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_html import ORDER, embed_images, product_name, to_html  # noqa: E402

TEMPLATE = Path(__file__).parent.parent / "templates" / "role_reader.html"
SPLIT = {"4", "9"}
TITLES = {"high_level_design": "High-level system design", "explore_notes": "Exploration notes"}  # §4 (one subsection per lead) and §9 (constraints) split by ###


def sections(folder):
    """[(key, title, markdown)] in bundle order. Documents are one section each;
    the system description is one per ## heading, §4 and §9 one per ### heading."""
    out = []
    for name in ORDER:
        p = folder / name
        if not p.exists():
            continue
        text = embed_images(p.read_text(encoding="utf-8"), folder)
        text = re.sub(r"\A\s*#{1,3} [^\n]*\n", "", text)  # the document's own title line
        if name != "system_description.md":
            out.append((p.stem, TITLES.get(p.stem, p.stem.replace("_", " ").capitalize()), text))
            continue
        pre, *h2s = re.split(r"^(?=## )", text, flags=re.M)
        for i, chunk in enumerate(h2s):
            head, body = chunk.split("\n", 1)
            m = re.match(r"##\s*(\d+)\.?\s*(.*)", head)
            n, title = (m.group(1), m.group(2).strip()) if m else (None, head[2:].strip())
            body = (pre if i == 0 else "") + body
            subs = re.split(r"^(?=### )", body, flags=re.M)
            if n not in SPLIT or len(subs) < 2:
                out.append((f"§{n}" if n else title, title, body))
                continue
            for j, sub in enumerate(subs[1:]):
                shead, sbody = sub.split("\n", 1)
                st = re.sub(r"\*\(.*?\)\*", "", shead[3:]).strip()
                sm = re.match(rf"({n}\.\d+)\s+(.*)", st)
                key, st = (f"§{sm.group(1)}", sm.group(2)) if sm else (f"§{n} {st}", st)
                out.append((key, st, (subs[0] if j == 0 else "") + sbody))
    return out


def check(cfg, secs):
    """Every key, role and id in roles.json must resolve; ids must appear in the text they point at."""
    errs, roles = [], cfg.get("roles") or {}
    text = {k: re.sub(r"<[^>]+>", " ", html.unescape(v["html"])) for k, v in secs.items()}

    def sec(k, where):
        if k not in secs:
            errs.append(f"{where}: no section '{k}'")

    def role(r, where):
        if r not in roles:
            errs.append(f"{where}: no role '{r}'")

    if not roles:
        errs.append("roles: empty")
    for r, v in roles.items():
        for tier in ("owns", "must", "skim"):
            for k in v.get(tier, []):
                sec(k, f"roles.{r}.{tier}")
    for f in cfg.get("figures", []):
        if f.get("section"):
            sec(f["section"], f"figures '{f.get('label')}'")
    for i, p in enumerate(cfg.get("problems", []), 1):
        role(p.get("owner"), f"problems #{i}")
        for r in p.get("support", []):
            role(r, f"problems #{i}")
    for part in ("bom", "tasks"):
        if part in cfg:
            if cfg[part].get("section"):
                sec(cfg[part]["section"], f"{part}.section")
            for i, row in enumerate(cfg[part]["rows"], 1):
                for r in row.get("roles", []):
                    role(r, f"{part} row {i}")
    for t in cfg.get("tasks", {}).get("rows", []):
        if t.get("path", "") not in ("", "critical", "near"):
            errs.append(f"tasks '{t.get('task')}': path must be critical, near or empty")
    nodes = cfg.get("nodes", {})
    for kind, items in (("decisions", cfg.get("decisions", {})), ("nodes", nodes)):
        for i, v in items.items():
            v.setdefault("find", i)
            if v.get("home") not in secs:
                errs.append(f"{kind}.{i}: home '{v.get('home')}' is not a section")
            elif v["find"] not in text[v["home"]]:
                errs.append(f"{kind}.{i}: '{v['find']}' not found in {v['home']}")
            for r in v.get("roles", []):
                role(r, f"{kind}.{i}")
            for k in v.get("sections", []):
                sec(k, f"{kind}.{i}.sections")
            for n in v.get("chain", []):
                if n not in nodes:
                    errs.append(f"{kind}.{i}: chain node '{n}' not in nodes")
    bom = cfg.get("bom")
    if bom and bom.get("total"):
        s = sum(float(r.get("cost") or 0) for r in bom["rows"])
        if abs(s - bom["total"]) > 0.01 * bom["total"]:
            print(f"warning: BOM rows sum to {s:g}, total says {bom['total']:g}")
    return errs


def build(folder, keys_only=False):
    parts = sections(folder)
    if keys_only:
        for k, t, _ in parts:
            print(f"{k:28} {t}")
        return
    imgs, secs = {}, {}

    def stash(m):
        k = hashlib.md5(m.group(1).encode()).hexdigest()[:8]
        imgs[k] = m.group(1)
        return f'data-img="{k}"'

    for i, (key, title, md) in enumerate(parts):
        rendered, _ = to_html(md, f"s{i}")
        secs[key] = {"title": title, "html": re.sub(r'src="(data:image/[^"]+)"', stash, rendered)}
    cfg_path = folder / "roles.json"
    if not cfg_path.exists():
        sys.exit(f"no {cfg_path}; write it first (see the skill's role reader step), "
                 f"or run with --keys to list the section keys")
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    errs = check(cfg, secs)
    if errs:
        sys.exit("roles.json does not match the documents:\n  " + "\n  ".join(errs))
    anchors = {a: k for k, s in secs.items() for a in re.findall(r'id="([^"]+)"', s["html"])}
    data = {"product": product_name(folder), "date": datetime.date.today().isoformat(),
            "order": list(secs), "sections": secs, "imgs": imgs, "anchors": anchors, "cfg": cfg}
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    page = TEMPLATE.read_text(encoding="utf-8").replace("__PRD_DATA__", blob)
    page = page.replace("__TITLE__", html.escape(data["product"]))
    out = folder / "role_reader.html"
    out.write_text(page, encoding="utf-8")
    print(f"{out} ({len(secs)} sections, {len(cfg['roles'])} roles, {out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    build(Path(args[0]), "--keys" in sys.argv)
