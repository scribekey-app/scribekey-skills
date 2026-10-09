"""Scores run.py results with one mechanical check per case in cases.json, keyed by case id.

Usage: python3 evals/grade.py <results.json>
Each check tests the case's "what" and its skill's Check line as far as a string test can: a
pass is a strong signal, a fail is worth reading. Read the outputs too before changing a skill.
"""
import collections
import json
import re
import sys

def has(o, *xs): return all(x.lower() in o.lower() for x in xs)
def no(o, *xs): return not any(x.lower() in o.lower() for x in xs)
def lines(o): return [l for l in o.splitlines() if l.strip()]
C = {
 "clean-up-1": lambda o: has(o, "10:15") and no(o, "10:30"),
 "clean-up-2": lambda o: "\n\n" in o.strip() and has(o, "landlord"),
 "clean-up-3": lambda o: no(o, "canberra"),
 "summary-1": lambda o: len(o) < 470 and has(o, "friday") and has(o, "21"),
 "summary-2": lambda o: o.strip().count(".") <= 1 and "\n" not in o.strip(),
 "summary-3": lambda o: len(o) < 140,
 "email-1": lambda o: o.startswith(("Hi Sam", "Hey Sam")) and has(o, "$850", "resend"),
 "email-2": lambda o: o.startswith("Hi,") and no(o, "nguyen", "[", "]"),
 "email-3": lambda o: o.startswith(("Dear Dr Nguyen", "Dear Doctor Nguyen", "Dear Dr. Nguyen")) and has(o, "44729"),
 "notes-1": lambda o: len([l for l in lines(o) if l.startswith("#")]) >= 2 and has(o, "beaumont"),
 "notes-2": lambda o: len(lines(o)) == 1 and "#" not in o and has(o, "bluegum"),
 "notes-3": lambda o: any("hail mary" in l.lower() and "overstory" not in l.lower() for l in lines(o)) and sum(l.lstrip().startswith("-") for l in lines(o)) >= 3 and no(o, "not specified"),
 "meeting-notes-1": lambda o: has(o, "### decisions", "### actions") and any("- [ ]" in l and "maria" in l.lower() for l in lines(o)),
 "meeting-notes-2": lambda o: no(o, "### decisions"),
 "meeting-notes-3": lambda o: has(o, "### decisions") and no(o, "### actions"),
 "todo-list-1": lambda o: o.count("- [ ]") == 4 and not any("- [ ]" in l and "job" in l.lower() for l in lines(o)),
 "todo-list-2": lambda o: "- [ ]" not in o,
 "todo-list-3": lambda o: has(o, "(jamie)", "(priya)") and o.count("- [ ]") == 3,
 "agent-prompt-1": lambda o: o.startswith("Goal:") and has(o, "constraints:", "done when:", "src/settings.tsx") and no(o, "localstorage", "n/a"),
 "agent-prompt-2": lambda o: o.startswith("Goal:") and no(o, "n/a"),
 "agent-prompt-3": lambda o: o.startswith("Goal:") and has(o, "steps:", "payments") and re.search(r"^\s*1\.", o, re.M) is not None,
 "friendly-message-1": lambda o: no(o, "dear") and (has(o, "11") or has(o, "eleven")),
 "friendly-message-2": lambda o: len(o) < 60,
 "friendly-message-3": lambda o: no(o, "wanted to i just", "for for"),
 "work-chat-1": lambda o: "@maya" in o.lower() and has(o, "checkout_service.log"),
 "work-chat-2": lambda o: sum(l.lstrip().startswith("- ") for l in lines(o)) >= 3 and not o.startswith("Hi"),
 "work-chat-3": lambda o: o.startswith(("Ben", "Hi Ben")) and "?" in o,
 "social-post-1": lambda o: "#" in o and no(o, "hashtag"),
 "social-post-2": lambda o: "#" not in o,
 "social-post-3": lambda o: "#" not in o,
 "professional-1": lambda o: no(o, "gonna", "a mess", "yeah"),
 "professional-2": lambda o: has(o, "50", "30", "friday") and no(o, "remaining 20", "the other 20"),
 "professional-3": lambda o: has(o, "signed contract"),
 "concise-1": lambda o: len(o) < 150,
 "concise-2": lambda o: has(o, "3 pm", "4b") and len(o) < 50,
 "concise-3": lambda o: has(o, "6:40", "qf409", "4:40", "mike") and len(o) < 200,
 "unslop-1": lambda o: no(o, "seamless", "robust", "empower", "unlock", "foster", "—", "hope this helps", "let me know", "cutting-edge", "not just"),
 "unslop-2": lambda o: no(o, "hope this message", "reach out", "worth noting", "due to the fact", "commence", "hesitate", "circle back"),
 "unslop-3": lambda o: has(o, "typo", "after lunch"),
}
res = json.load(open(sys.argv[1]))
by = collections.defaultdict(list)
for r in res:
    o = (r.get("output") or "").strip()
    by[r["id"]].append(C[r["id"]](o) if "error" not in r else False)
tot = sum(sum(v) for v in by.values()); n = sum(len(v) for v in by.values())
skills = collections.defaultdict(lambda: [0, 0])
for k, v in by.items():
    s = k.rsplit("-", 1)[0]; skills[s][0] += sum(v); skills[s][1] += len(v)
print(f"TOTAL {tot}/{n}")
print("  ".join(f"{s} {a}/{b}" for s, (a, b) in sorted(skills.items())))
print("fails:", " ".join(f"{k}:{len(v)-sum(v)}" for k, v in sorted(by.items()) if sum(v) < len(v)))
