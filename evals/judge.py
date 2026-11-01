"""Asks TypeSafe's Jev yes/no questions about each run.py output, as a second opinion to grade.py.

Usage: python3 evals/judge.py <prompts dir from build.py> <results.json> <judged.json> [rendered.json]
Environment: TYPESAFE_API_KEY; JUDGE_MODEL (default jev-latest).
Diagram skills get DIAGRAM_QUESTIONS in place of the prose ones; pass render.mjs's rendered.json
so Jev also sees how big the drawing is and how large its text lands on a phone.
grade.py tests strings; this asks what a string test cannot: did the output answer the speaker
instead of writing their words down, invent a fact, suit the app it lands in, read clearly first
time. Each answer is a probability of yes; a run fails a question when it lands on the wrong side
of 0.5. Read the outputs behind any failure before changing a skill.
"""
import collections
import concurrent.futures
import glob
import json
import os
import re
import sys
import urllib.request

src, res_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
rendered = {(r["id"], r["rep"]): r for r in json.load(open(sys.argv[4]))} if len(sys.argv) > 4 else {}
model = os.environ.get("JUDGE_MODEL", "jev-latest")
cases = {c["id"]: c for f in glob.glob(f"{src}/*.json") for c in json.load(open(f))}

# (id, question, the answer a good output gets)
QUESTIONS = [
    ("answered", "Does `output` respond to the speaker as an assistant would: answering their "
     "question, giving advice, or adding steps, suggestions or solutions of its own? Reorganising, "
     "shortening or reformatting what the speaker said, as `skill_goal` asks, is not responding.",
     False),
    ("invented", "Does `output` state a name, number, date, time, place, owner or other fact that "
     "is not in `transcript`?", False),
    ("meta", "Does `output` contain commentary about the text itself, such as a preface like "
     "'Here is the cleaned text', a note to the reader, or a placeholder in square brackets?", False),
    ("slop", "Does `output` add wording that marks text as machine-written and that is not in "
     "`transcript`: a stock opener or closer, an assistant phrase, hype or corporate words, a "
     "'not just X but Y' contrast, a tacked-on '-ing' clause, a list of three, a rhetorical "
     "question, or a closing line that only restates?", False),
    ("case", "Does `output` do what `case_requirement` asks?", True),
    ("fits_app", "Would `output` paste cleanly into the text box of `destination_app` and read as "
     "intended there, with no formatting syntax that app shows as raw symbols and no structure "
     "that app already provides on its own?", True),
    ("clear", "Would someone reading `output` for the first time understand it in one read?", True),
]

DIAGRAMS = {"flowchart": "flowchart", "mind-map": "mind map", "timeline": "timeline"}
# What makes a diagram optimal: faithful, nothing invented, the right granularity, readable on a
# phone, the right kind of diagram. "answered" and "meta" above still apply, and "invented" with
# a note that a title naming the topic is not a new fact.
DIAGRAM_QUESTIONS = [
    ("missing", "`output` is Mermaid source for a diagram of `transcript`. Does it leave out a "
     "step, decision, idea or event the speaker settled on, change what one says, put them out of "
     "the speaker's order, or keep something the speaker took back? Folding a small detail into "
     "the node it belongs to, shortening a label, and leaving out an aside are not leaving "
     "something out.", False),
    ("added", "Does `output` contain a node, step, branch, idea or event the speaker did not say: "
     "a Start or End box, a step a reader might expect but the speaker never mentioned, or an "
     "aside or passing remark drawn as its own node?", False),
    ("granularity", "Is each node in `output` one step, idea or event a reader needs, a few words "
     "long, with small details folded into the node they belong to and nothing repeated?", True),
    ("phone", "`drawing` says how large the diagram's text lands on a phone. Can its labels be read "
     "there without zooming, each short enough to take in at a glance?", True),
    ("type", "Is a `diagram_type` the right kind of diagram for what the speaker described: a "
     "flowchart for steps and decisions, a mind map for ideas that branch from one topic, a "
     "timeline for events in time order? When the text holds none of these, one node naming "
     "its topic is right.", True),
]
DIAGRAM_KEEP = {"answered", "meta"}
DIAGRAM_INVENTED = ("invented", "Does `output` state a name, number, date, time, place, owner or "
                    "other fact that is not in `transcript`? A title or centre naming the topic "
                    "in the speaker's terms is not a new fact.", False)


def drawing(item):
    r = rendered.get((item["id"], item.get("rep")))
    if not r:
        return "not rendered"
    if not r["ok"]:
        return f"failed to render: {r['error'].splitlines()[0]}"
    return f"its text lands at {r['textSp']}sp, which {'needs zooming' if r['smallText'] else 'reads without zooming'}"


def skill_goal(system):
    m = re.search(r'<skill_content name="[^"]+">\n(.*?)\n', system)
    return m.group(1) if m else ""


def ask(item):
    case = cases[item["id"]]
    app = case.get("destination")
    state = {
        "transcript": re.search(r"<TRANSCRIPT>\n(.*)\n</TRANSCRIPT>", case["user"], re.S).group(1),
        "skill_goal": skill_goal(case["system"]),
        "case_requirement": case["what"],
        "destination_app": app or "an unknown app",
        "output": item.get("output") or "",
    }
    skill = item["id"].rsplit("-", 1)[0]
    if skill in DIAGRAMS:
        state.update(diagram_type=DIAGRAMS[skill], drawing=drawing(item))
        asked = [q for q in QUESTIONS if q[0] in DIAGRAM_KEEP] + [DIAGRAM_INVENTED] + DIAGRAM_QUESTIONS
    else:
        asked = [q for q in QUESTIONS if q[0] != "fits_app" or app]
    qs = {q: {"type": "noul", "instructions": text} for q, text, _ in asked}
    body = json.dumps({"state": state, "model": model, "questions": qs}).encode()
    request = urllib.request.Request("https://api.typesafe.ai/v1/systemone", body, {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ.get('TYPESAFE_API_KEY', '')}"})
    error = None
    for _ in range(3):
        try:
            answers = json.load(urllib.request.urlopen(request, timeout=60))["answers"]
            return {**item, "jev": {q: round(a["noul"], 3) for q, a in answers.items()}}
        except Exception as e:  # noqa: BLE001 - a failed judgment is recorded, not fatal
            error = str(e)
    return {**item, "jev_error": error}


def failures(judged):
    """Question ids the run fails: yes-probability on the wrong side of 0.5."""
    good = {q: g for q, _, g in QUESTIONS + DIAGRAM_QUESTIONS}
    return [q for q, p in judged.get("jev", {}).items() if (p > 0.5) != good[q]]


if __name__ == "__main__":
    runs = [r for r in json.load(open(res_path)) if "error" not in r and r["id"] in cases]
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        judged = list(pool.map(ask, runs))
    json.dump(judged, open(out, "w"), indent=1, ensure_ascii=False)
    per_q = collections.Counter(q for j in judged for q in failures(j))
    asked = collections.Counter(q for j in judged for q in j.get("jev", {}))
    ok = sum(not failures(j) for j in judged if "jev" in j)
    print(f"JEV {ok}/{len(judged)} runs clean, {sum('jev_error' in j for j in judged)} errors")
    print("  ".join(f"{q} {asked[q] - per_q[q]}/{asked[q]}" for q, _, _ in QUESTIONS + DIAGRAM_QUESTIONS if asked[q]))
    by_case = collections.defaultdict(list)
    for j in judged:
        by_case[f'{j["id"]}-{j["rep"]}' if "should" in j else j["id"]] += failures(j)
    print("fails:", " ".join(f"{k}:{','.join(sorted(set(v)))}" for k, v in sorted(by_case.items()) if v))
    fixtures = [j for j in judged if "should" in j and "jev" in j]
    if fixtures:  # format faults are grade.py's to catch; Jev reads for content
        good = [j for j in fixtures if j["should"] == "pass"]
        bad = [j for j in fixtures if j["should"] == "fail"]
        print(f"fixtures: good ones clean {sum(not failures(j) for j in good)}/{len(good)}, "
              f"bad ones flagged {sum(bool(failures(j)) for j in bad)}/{len(bad)}")
