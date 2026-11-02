"""Scores run.py results with one mechanical check per case in cases.json, keyed by case id.

Usage: python3 evals/grade.py <results.json>, or import passed() to score one output
Each check tests the case's "what" and its skill's Check line as far as a string test can: a
pass is a strong signal, a fail is worth reading. Read the outputs too before changing a skill.
"""
import collections
import json
import re
import sys
from pathlib import Path

def has(o, *xs): return all(x.lower() in o.lower() for x in xs)
def no(o, *xs): return not any(x.lower() in o.lower() for x in xs)
def lines(o): return [l for l in o.splitlines() if l.strip()]
# Tells the app's writing floor forbids; the slop cases fail when any appears.
TELLS = ("—", "hope this", "reach out", "feel free", "let me know if", "don't hesitate", "great question",
         "certainly", "leverage", "utilise", "utilize", "seamless", "robust", "delve", "crucial", "pivotal",
         "foster", "unlock", "empower", "showcase", "elevate", "journey", "game-changer", "excited to",
         "serves as", "boasts", "not just", "worth noting", "in order to", "landscape", "testament")
def clean(o): return no(o, *TELLS)
C = {
 "search-query-1": lambda o: len(lines(o)) == 1 and has(o, "sourdough", "rye") and no(o, "starter is", "you can"),
 "search-query-2": lambda o: len(lines(o)) == 1 and has(o, "sony", "wh-1000xm5", "300") and no(o, "reviews are", "best headphones"),
 "search-query-3": lambda o: len(lines(o)) == 1 and has(o, "artículos", "energía solar", "chile", "2024"),
 "clean-up-1": lambda o: has(o, "10:15") and no(o, "10:30"),
 "clean-up-2": lambda o: "\n\n" in o.strip() and has(o, "landlord"),
 "clean-up-3": lambda o: no(o, "canberra"),
 "summary-1": lambda o: len(o) < 470 and has(o, "friday") and has(o, "21"),
 "summary-2": lambda o: o.strip().count(".") <= 1 and "\n" not in o.strip(),
 "summary-3": lambda o: len(o) < 140,
 "email-1": lambda o: o.startswith(("Hi Sam", "Hey Sam")) and has(o, "$850", "resend"),
 "email-2": lambda o: o.startswith("Hi,") and no(o, "nguyen", "[", "]"),
 "email-3": lambda o: o.startswith(("Dear Dr Nguyen", "Dear Doctor Nguyen", "Dear Dr. Nguyen")) and has(o, "44729"),
 "notes-1": lambda o: "#" not in o and sum(l.rstrip().endswith(":") for l in lines(o)) >= 2 and has(o, "beaumont"),
 "notes-2": lambda o: len(lines(o)) == 1 and "#" not in o and has(o, "bluegum"),
 "notes-3": lambda o: any("hail mary" in l.lower() and "overstory" not in l.lower() for l in lines(o)) and sum(l.lstrip().startswith("-") for l in lines(o)) >= 3 and no(o, "not specified"),
 "meeting-notes-1": lambda o: has(o, "### decisions", "#### maria", "#### ken"),
 "meeting-notes-2": lambda o: no(o, "### decisions"),
 "meeting-notes-3": lambda o: has(o, "### decisions") and no(o, "### actions"),
 "meeting-notes-4": lambda o: has(o, "#### maria", "#### speaker 3", "### decisions", "### open questions") and no(o, "#### ana"),
 "meeting-notes-5": lambda o: no(o, "#### priya", "#### ken") and has(o, "#### ana"),
 "interview-qa-1": lambda o: o.count("**Q (") == 2 and has(o, "shipped", "six weeks"),
 "interview-qa-2": lambda o: o.count("**Q (") == 2 and has(o, "no answer", "twelve"),
 "interview-qa-3": lambda o: has(o, "**Q (Speaker 1)", "**A (Speaker 2)", "one"),
 "one-on-one-1": lambda o: has(o, "### ken", "export", "empty state", "### feedback", "- [ ] ana") ,
 "one-on-one-2": lambda o: has(o, "late", "held up") and has(o, "- [ ] jo"),
 "one-on-one-3": lambda o: no(o, "blockers") and has(o, "onboarding"),
 "lecture-notes-1": lambda o: o.count("\n### ") >= 2 and has(o, "**equilibrium price**", "### questions from the room", "rent control"),
 "lecture-notes-2": lambda o: has(o, "f = ma") or has(o, "f = m", "6 n") or has(o, "6 newtons"),
 "lecture-notes-3": lambda o: no(o, "questions from the room") and has(o, "1789", "14 july", "1793"),
 "todo-list-1": lambda o: 4 <= len(lines(o)) <= 5 and no(o, "job", "- [") and not any(l.endswith(".") for l in lines(o)),
 "todo-list-2": lambda o: "- [" not in o and has(o, "park"),
 "todo-list-3": lambda o: has(o, "(jamie)", "(priya)") and len(lines(o)) == 3 and no(o, "- ["),
 "todo-list-4": lambda o: len(lines(o)) == 1 and has(o, "dentist", "tomorrow") and not o.endswith(".") and no(o, "- [", "* "),
 "todo-list-5": lambda o: len(lines(o)) == 2 and no(o, "week", "ugh") and has(o, "thursday"),
 "todo-list-6": lambda o: len(lines(o)) == 3 and not any(l.lstrip()[:1] in "-*•[" for l in lines(o)),
 "professional-4": lambda o: clean(o) and has(o, "two weeks", "supplier"),
 "email-4": lambda o: clean(o) and has(o, "thursday"),
 "social-post-5": lambda o: clean(o) and has(o, "ten years") and "?" not in o,
 "friendly-message-5": lambda o: clean(o) and len(o) < 140,
 "agent-prompt-1": lambda o: o.startswith("Goal:") and has(o, "constraints:", "done when:", "src/settings.tsx") and no(o, "localstorage", "n/a"),
 "agent-prompt-2": lambda o: o.startswith("Goal:") and no(o, "n/a"),
 "agent-prompt-3": lambda o: o.startswith("Goal:") and has(o, "steps:", "payments") and re.search(r"^\s*1\.", o, re.M) is not None,
 "friendly-message-1": lambda o: no(o, "dear") and (has(o, "11") or has(o, "eleven")),
 "friendly-message-2": lambda o: len(o) < 60,
 "friendly-message-3": lambda o: no(o, "wanted to i just", "for for"),
 "work-chat-1": lambda o: "@maya" in o.lower() and has(o, "checkout_service.log"),
 "work-chat-2": lambda o: sum(l.lstrip().startswith("- ") for l in lines(o)) >= 3 and not o.startswith("Hi"),
 "work-chat-3": lambda o: o.startswith(("Ben", "Hi Ben", "@Ben", "@ben")) and "?" in o,
 "social-post-1": lambda o: "#" in o and no(o, "hashtag"),
 "social-post-2": lambda o: "#" not in o,
 "social-post-3": lambda o: "#" not in o,
 "professional-1": lambda o: no(o, "gonna", "a mess", "yeah"),
 "professional-2": lambda o: has(o, "50", "30", "friday") and no(o, "remaining 20", "the other 20"),
 "professional-3": lambda o: has(o, "signed contract"),
 "concise-1": lambda o: len(o) < 150,
 "concise-2": lambda o: has(o, "3 pm", "4b") and len(o) < 50,
 "concise-3": lambda o: has(o, "6:40", "qf409", "4:40", "mike") and len(o) < 200,
 "notes-4": lambda o: "#" not in o and sum(l.rstrip().endswith(":") for l in lines(o)) >= 2,
 "agent-prompt-4": lambda o: o.startswith("Goal:") and has(o, "--dry-run", "scripts/migrate.py"),
 "agent-prompt-5": lambda o: o.startswith("Goal:") and has(o, "react", "tailwind") and len(o) < 600,
 "work-chat-4": lambda o: has(o, "@sam", "readme.md"),
 "clean-up-4": lambda o: has(o, "fucking"),
 "clean-up-5": lambda o: has(o, "4") and no(o, "not 3", "not three", " 3 ", "three"),
 "clean-up-6": lambda o: has(o, "actually"),
 "friendly-message-4": lambda o: has(o, "shit", "sick"),
 "concise-4": lambda o: has(o, "think") or has(o, "might") or has(o, "may") or has(o, "probably"),
 "summary-4": lambda o: has(o, "viernes") and no(o, " the ", " and "),
 "meeting-notes-6": lambda o: no(o, "### decisions", "### actions", "### summary") and has(o, "marie"),
 "social-post-4": lambda o: has(o, "@maya") and len(o) < 90,
 "taobao-search-1": lambda o: len(lines(o)) == 1 and has(o, "衣柜", "灯", "人体感应", "磁吸", "免打孔") and no(o, "充电", "usb", "尺寸", "厘米"),
 "taobao-search-2": lambda o: len(lines(o)) == 1 and has(o, "34", "带鱼屏", "usb-c") and no(o, "4k", "曲面"),
 "taobao-search-3": lambda o: len(lines(o)) == 1 and has(o, "戴森", "v11", "充电器") and no(o, "电压", "伏", "吸尘器"),
 "taobao-search-4": lambda o: len(lines(o)) == 1 and has(o, "浴室", "置物架", "免打孔", "不锈钢") and no(o, "吸盘", "胶", "免钉胶"),
 "taobao-search-5": lambda o: len(lines(o)) == 1 and has(o, "奶", "泡", "咖啡") and no(o, "可以", "当然", "推荐", "吗？", "吗?"),
 "taobao-search-6": lambda o: len(lines(o)) == 1 and has(o, "推拉门") and no(o, "液压", "静音", "不锈钢"),
 "taobao-search-7": lambda o: len(lines(o)) == 1 and has(o, "usb-c", "macbook air m3", "hdmi"),
 "taobao-search-8": lambda o: len(lines(o)) == 1 and has(o, "衣柜", "人体感应灯", "磁吸") and no(o, "wardrobe", "english"),
}
CHECKS = C

# Diagram skills are scored from each case's "expect" in cases.json, one named check each:
#   format     Mermaid source alone: the skill's header first, no fence, no %% (init, comments),
#              no click/href/style/class lines, every label in double quotes, spaces not tabs.
#   size       node count (timeline: events) within expect "nodes" [min, max], default [1, 25].
#   coverage   every "must" term is in some label (a list is alternatives).
#   absent     no "must_not" term as a whole word in any label, and no filler node ("Start",
#              "End", "Done"...) unless the speaker said that word: the speaker's first step is
#              the start, so a bare Start box only spends a row of a phone screen.
#   order      flowchart: each "order" term's node reaches the next one along the arrows;
#              timeline: each term's line comes no later than the next one's.
#   decisions  flowchart: at least expect "decisions" diamonds, each with two or more exits, all
#              labelled with the answer.
#   shapes     flowchart: the first node is a stadium (or a diamond, when the process opens with a
#              question) and so is every final outcome, a node no arrow leaves; a diamond holds at
#              most 5 words and any other node at most 6, so the drawing stays small on a phone.
#   hierarchy  mind map: one centre, at most three levels below it, and each ["child", "parent"]
#              in "under" has the child's node somewhere beneath the parent's.
#   colons     timeline: no time like 9:30 left in, which Pele splits into another event.
DIAGRAMS = {"flowchart": "flowchart TD", "mind-map": "mindmap", "timeline": "timeline"}
EXPECT, SAID = {}, {}
for c in json.load(open(Path(__file__).parent / "cases.json")):
    if c["skill"] in DIAGRAMS:
        cid = f'{c["skill"]}-{sum(k.startswith(c["skill"] + "-") for k in EXPECT) + 1}'
        EXPECT[cid], SAID[cid] = c.get("expect", {}), c["transcript"]
FILLER = {"start", "end", "begin", "finish", "done", "stop", "the end"}
NODE = re.compile(r'(\w+)\s*(\(\(|\[\[|\[\(|\(\[|\{\{|[\[\(\{>])"([^"]*)"')
EDGE = re.compile(r'(\w+)(?:\s*[\[\(\{>]+"[^"]*"[\]\)\}]+)?\s*'
                  r'(?:--\s*"([^"]*)"\s*-->|(?:-->|==>|-\.->|---)\s*(?:\|"?([^|"]*)"?\|)?)\s*(?=(\w+))')


def flowchart(o):
    """Nodes {id: (label, opening bracket)} and edges [(from, to, label)]."""
    nodes = {}
    for m in NODE.finditer(o):
        nodes.setdefault(m[1], (m[3], m[2]))
    edges = [(m[1], m[4], (m[2] or m[3] or "").strip()) for m in EDGE.finditer(o)]
    for a, b, _ in edges:
        nodes.setdefault(a, (a, "")); nodes.setdefault(b, (b, ""))
    return nodes, edges


def mindmap(o):
    """Rows (indent, label) in order, and each row's parent row index (None for a centre)."""
    rows = [(len(l) - len(l.lstrip(" ")), (re.search(r'"([^"]*)"', l) or [None, l.strip()])[1])
            for l in lines(o)[1:]]
    parents, stack = [], []
    for i, (ind, _) in enumerate(rows):
        while stack and stack[-1][0] >= ind:
            stack.pop()
        parents.append(stack[-1][1] if stack else None)
        stack.append((ind, i))
    return rows, parents


def timeline(o):
    """Title and one list per time line: [time, event, ...]."""
    body = [l.strip() for l in lines(o)[1:]]
    title = next((l[6:] for l in body if l.startswith("title ")), "")
    return title, [[p.strip() for p in l.split(":")] for l in body if not l.startswith(("title ", "section "))]


def diagram_checks(case_id, output):
    """{check: passed} for one diagram output; see the table above."""
    skill = case_id.rsplit("-", 1)[0]
    o, e, said = (output or "").strip(), EXPECT.get(case_id, {}), SAID.get(case_id, "")
    fmt = (o.startswith(DIAGRAMS[skill]) and no(o, "```", "%%", "href", ":::", "\t")
           and not re.search(r"^\s*(click|style|classDef|class|linkStyle)\s", o, re.M))
    r = {}
    if skill == "flowchart":
        nodes, edges = flowchart(o)
        labels = [l for l, _ in nodes.values()]
        bare = re.sub(r'"[^"]*"', '""', o)
        fmt = fmt and not re.search(r'\w[\[\(\{>]+(?![\[\(\{>"])', bare) and not re.search(r'-->\|(?!")', bare)
        count = len(nodes)
        diamonds = [i for i, (_, shape) in nodes.items() if shape == "{"]
        exits = {d: [lbl for a, _, lbl in edges if a == d] for d in diamonds}
        r["decisions"] = len(diamonds) >= e.get("decisions", 0) and all(len(x) >= 2 and all(x) for x in exits.values())
        first = next(iter(nodes), None)
        ends = [i for i, (_, shape) in nodes.items() if shape != "{" and not any(a == i for a, _, _ in edges)]
        r["shapes"] = ((first is None or nodes[first][1] in ("([", "{")) and all(nodes[i][1] == "([" for i in ends)
                       and all(len(l.replace("#quot;", "").split()) <= (5 if shape == "{" else 6) for l, shape in nodes.values()))
        if "order" in e:
            find = lambda t: [i for i, (l, _) in nodes.items() if term_in(t, l)]  # noqa: E731
            r["order"] = all(any(b in reachable(a, edges) for a in find(s) for b in find(t)) for s, t in zip(e["order"], e["order"][1:]))
    elif skill == "mind-map":
        rows, parents = mindmap(o)
        labels = [l for _, l in rows]
        fmt = fmt and all('"' in l for l in lines(o)[1:]) and "((" in (lines(o) + ["", ""])[1]
        count = len(rows)
        depth = lambda i: 0 if parents[i] is None else 1 + depth(parents[i])  # noqa: E731
        above = lambda i: [] if parents[i] is None else [parents[i]] + above(parents[i])  # noqa: E731
        r["hierarchy"] = (parents.count(None) == 1 and all(depth(i) <= 3 for i in range(len(rows)))
                          and all(any(term_in(p, rows[a][1]) for i, (_, l) in enumerate(rows) if term_in(c, l) for a in above(i))
                                  for c, p in e.get("under", [])))
    else:
        title, periods = timeline(o)
        labels = [title] + [p for row in periods for p in row]
        fmt = fmt and bool(title) and len(title.split()) <= 6
        count = sum(max(1, len(row) - 1) for row in periods)
        r["colons"] = not re.search(r"\d:\d", o)
        if "order" in e:
            at = lambda t: min((i for i, row in enumerate(periods) if any(term_in(t, p) for p in row)), default=None)  # noqa: E731
            pos = [at(t) for t in e["order"]]
            r["order"] = None not in pos and pos == sorted(pos)
    labels = [re.sub(r"#(\d+);", lambda m: chr(int(m[1])), l.replace("#quot;", '"')) for l in labels]
    lo, hi = e.get("nodes", [1, 25])
    text = " | ".join(labels)
    r["format"] = fmt
    r["size"] = lo <= count <= hi
    r["coverage"] = all(term_in(t, text) for t in e.get("must", []))
    r["absent"] = (not any(re.search(rf"(?<!\w){re.escape(t)}(?!\w)", text, re.I) for t in e.get("must_not", []))
                   and not any(l.strip(" .!").lower() in FILLER and l.strip(" .!").lower() not in said.lower() for l in labels))
    return r


def reachable(start, edges):
    seen, todo = {start}, [start]
    while todo:
        a = todo.pop()
        for x, y, _ in edges:
            if x == a and y not in seen:
                seen.add(y); todo.append(y)
    return seen


def term_in(term, text):
    return any(t.lower() in text.lower() for t in ([term] if isinstance(term, str) else term))


def passed(case_id, output):
    """True when one output passes its case's check. Other repos import this to score a run."""
    if case_id.rsplit("-", 1)[0] in DIAGRAMS:
        return all(diagram_checks(case_id, output).values())
    return C[case_id]((output or "").strip())


def main(path):
    res = json.load(open(path))
    by = collections.defaultdict(list)
    asked, ok_by = collections.defaultdict(collections.Counter), collections.defaultdict(collections.Counter)
    wrong = []
    for r in res:
        ok = passed(r["id"], r.get("output")) if "error" not in r else False
        by[r["id"]].append(ok)
        s = r["id"].rsplit("-", 1)[0]
        if s in DIAGRAMS and "error" not in r:
            got = diagram_checks(r["id"], r.get("output"))
            asked[s].update(got.keys()); ok_by[s].update(k for k, v in got.items() if v)
        if "should" in r and ok != (r["should"] == "pass"):
            wrong.append(f'{r["id"]}-{r["rep"]}')
    tot = sum(sum(v) for v in by.values()); n = sum(len(v) for v in by.values())
    skills = collections.defaultdict(lambda: [0, 0])
    for k, v in by.items():
        s = k.rsplit("-", 1)[0]; skills[s][0] += sum(v); skills[s][1] += len(v)
    print(f"TOTAL {tot}/{n}")
    print("  ".join(f"{s} {a}/{b}" for s, (a, b) in sorted(skills.items())))
    for s, c in sorted(asked.items()):
        print(f"  {s}:", "  ".join(f"{k} {ok_by[s][k]}/{n}" for k, n in sorted(c.items())))
    print("fails:", " ".join(f"{k}:{len(v)-sum(v)}" for k, v in sorted(by.items()) if sum(v) < len(v)))
    if wrong:
        print("MISMATCH against fixture 'should':", " ".join(wrong))
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1])
