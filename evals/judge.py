"""Asks TypeSafe's Jev yes/no questions about each run.py output, as a second opinion to grade.py.

Usage: python3 evals/judge.py <prompts dir from build.py> <results.json> <judged.json>
Environment: TYPESAFE_API_KEY; JUDGE_MODEL (default jev-latest).
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
    qs = {q: {"type": "noul", "instructions": text} for q, text, _ in QUESTIONS
          if q != "fits_app" or app}
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
    good = {q: g for q, _, g in QUESTIONS}
    return [q for q, p in judged.get("jev", {}).items() if (p > 0.5) != good[q]]


if __name__ == "__main__":
    runs = [r for r in json.load(open(res_path)) if "error" not in r]
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        judged = list(pool.map(ask, runs))
    json.dump(judged, open(out, "w"), indent=1, ensure_ascii=False)
    per_q = collections.Counter(q for j in judged for q in failures(j))
    asked = collections.Counter(q for j in judged for q in j.get("jev", {}))
    ok = sum(not failures(j) for j in judged if "jev" in j)
    print(f"JEV {ok}/{len(judged)} runs clean, {sum('jev_error' in j for j in judged)} errors")
    print("  ".join(f"{q} {asked[q] - per_q[q]}/{asked[q]}" for q, _, _ in QUESTIONS if asked[q]))
    by_case = collections.defaultdict(list)
    for j in judged:
        by_case[j["id"]] += failures(j)
    print("fails:", " ".join(f"{k}:{','.join(sorted(set(v)))}" for k, v in sorted(by_case.items()) if v))
