"""Scores run.py results with one mechanical check per case in cases.json, keyed by case id.

Usage: python3 evals/grade.py <results.json>, or import passed() to score one output
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
}
CHECKS = C


def passed(case_id, output):
    """True when one output passes its case's check. Other repos import this to score a run."""
    return C[case_id]((output or "").strip())


def main(path):
    res = json.load(open(path))
    by = collections.defaultdict(list)
    for r in res:
        by[r["id"]].append(passed(r["id"], r.get("output")) if "error" not in r else False)
    tot = sum(sum(v) for v in by.values()); n = sum(len(v) for v in by.values())
    skills = collections.defaultdict(lambda: [0, 0])
    for k, v in by.items():
        s = k.rsplit("-", 1)[0]; skills[s][0] += sum(v); skills[s][1] += len(v)
    print(f"TOTAL {tot}/{n}")
    print("  ".join(f"{s} {a}/{b}" for s, (a, b) in sorted(skills.items())))
    print("fails:", " ".join(f"{k}:{len(v)-sum(v)}" for k, v in sorted(by.items()) if sum(v) < len(v)))


if __name__ == "__main__":
    main(sys.argv[1])
