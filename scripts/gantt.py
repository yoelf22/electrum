"""Draw the §9 Schedule table of a system description as a Gantt chart, critical path highlighted.

    python scripts/gantt.py SYSTEM_DESCRIPTION.md OUT.png

Reads the table under "### Schedule" with columns # | Task | Start (week) | Duration (weeks) |
Depends on | Owner. A task with dependencies starts when the last one ends; otherwise at its Start
week. A range like "6–8" counts as its high end.
"""
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK, MUTED, CRIT, BAR = "#1B2328", "#6B7479", "#8A6D1F", "#B9C2C7"


def weeks(s):
    nums = re.findall(r"\d+(?:\.\d+)?", s)
    return float(nums[-1]) if nums else 0.0


def read_tasks(md):
    sec = re.search(r"^### Schedule\s*$(.*?)(?=^#{1,3} |\Z)", md, re.M | re.S)
    if not sec: sys.exit("no '### Schedule' section")
    rows = [[c.strip() for c in l.strip().strip("|").split("|")]
            for l in sec[1].splitlines() if l.startswith("|") and not re.match(r"^\|[\s:|-]+\|?\s*$", l)]
    head, body = rows[0], rows[1:]
    col = {h.split(" (")[0].lower(): i for i, h in enumerate(head)}
    tasks = {}
    for r in body:
        tasks[r[col["#"]]] = dict(name=re.sub(r"\*", "", r[col["task"]]), start=weeks(r[col["start"]]),
                                  dur=weeks(r[col["duration"]]),
                                  deps=re.findall(r"\d+", r[col["depends on"]]), owner=r[col["owner"]])
    return tasks


def schedule(tasks):
    """Earliest start from dependencies; returns the set of task ids on the critical path."""
    def end(i):
        t = tasks[i]
        if "end" not in t:
            t["start"] = max((end(d) for d in t["deps"]), default=t["start"])
            t["end"] = t["start"] + t["dur"]
        return t["end"]
    last = max(tasks, key=end)
    crit, cur = {last}, last
    while tasks[cur]["deps"]:  # walk back through the dependency that sets each start
        cur = max(tasks[cur]["deps"], key=end)
        crit.add(cur)
    return crit


def draw(tasks, crit, out):
    ids = list(tasks)
    fig, ax = plt.subplots(figsize=(11, 0.42 * len(ids) + 1.4))
    for y, i in enumerate(ids):
        t = tasks[i]
        c = CRIT if i in crit else BAR
        ax.barh(y, t["dur"], left=t["start"], color=c, height=0.6)
        ax.text(t["end"] + 0.3, y, f"{t['dur']:g} wk · {t['owner']}", va="center", fontsize=8, color=MUTED)
    ax.set_yticks(range(len(ids)), [f"{i}. {tasks[i]['name']}" for i in ids], fontsize=9, color=INK)
    ax.invert_yaxis()
    total = max(t["end"] for t in tasks.values())
    ax.set_xlim(0, total * 1.18)
    ax.set_xlabel("Week", color=MUTED)
    ax.grid(axis="x", color="#E3E6E1"); ax.set_axisbelow(True)
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
    ax.set_title(f"Schedule — {total:g} weeks; critical path in gold", loc="left", fontsize=11, color=INK)
    fig.tight_layout()
    fig.savefig(out, dpi=160)


def demo():
    t = {"1": dict(name="a", start=0, dur=4, deps=[], owner=""), "2": dict(name="b", start=0, dur=9, deps=[], owner=""),
         "3": dict(name="c", start=0, dur=2, deps=["1"], owner=""), "4": dict(name="d", start=0, dur=1, deps=["2", "3"], owner="")}
    assert schedule(t) == {"2", "4"} and t["4"]["start"] == 9 and t["3"]["start"] == 4
    print("ok")


if __name__ == "__main__":
    if len(sys.argv) < 3: demo(); sys.exit()
    tasks = read_tasks(open(sys.argv[1]).read())
    crit = schedule(tasks)
    draw(tasks, crit, sys.argv[2])
    print(sys.argv[2], "critical path:", " → ".join(sorted(crit, key=lambda i: tasks[i]["start"])))
