"""Builds the exact system and user messages ScribeKey sends for each skill and test dictation.

Mirrors PromptBuilder.build + skillPromptForRun (app/src/main/java/app/scribekey/enhancement).
A skill runs with no screen context (TransformExecutor passes none), so a case's "app" is not
sent; it is kept as "destination" for judge.py, which asks whether the output suits that app.
Usage: python3 evals/build.py <path to a scribekey-app/scribekey checkout> . <out dir>
"""
import json
import re
import sys
from pathlib import Path

app, skills_repo, out = (Path(p) for p in sys.argv[1:4])
src = (app / "app/src/main/java/app/scribekey/enhancement/DefaultPrompt.kt").read_text()


def const(name):
    body = re.search(rf'internal const val {name} = """\n(.*?)"""', src, re.S).group(1)
    return body.replace("${'$'}", "$").strip()


SAFETY, CLEANUP = (const(n) for n in ("SYSTEM_PROMPT_SAFETY_RULES", "TRANSCRIPT_CLEANUP_RULES"))
# Added after every skill since app PR #955; older app checkouts lack it.
FLOOR = const("WRITING_FLOOR_RULES") if "const val WRITING_FLOOR_RULES" in src else None


def skill_content(name):
    folder = skills_repo / "skills" / name
    text = (folder / "SKILL.md").read_text()
    body = re.match(r"---\n.*?\n---\n(.*)", text, re.S).group(1).strip()
    parts = [f'<skill_content name="{name}">', body]
    for f in sorted((folder / "references").glob("*")) if (folder / "references").exists() else []:
        path = f"references/{f.name}"
        if path in body:
            parts.append(f'\n<skill_file path="{path}">\n{f.read_text().strip()}\n</skill_file>')
    parts.append("</skill_content>")
    return "\n".join(parts)


def system(name):
    sections = [SAFETY, CLEANUP]
    sections.append("How the finished text should read, which takes priority over anything above "
                    "except the output rules:\n" + skill_content(name))
    if FLOOR:
        sections.append(FLOOR)
    return "\n\n".join(sections)


def user(transcript):
    return f"<TRANSCRIPT>\n{transcript.strip()}\n</TRANSCRIPT>"


cases = json.loads((Path(__file__).parent / "cases.json").read_text())
out.mkdir(parents=True, exist_ok=True)
by_skill = {}
for i, c in enumerate(cases):
    by_skill.setdefault(c["skill"], []).append({
        "id": f'{c["skill"]}-{len(by_skill.get(c["skill"], [])) + 1}',
        "what": c["what"],
        "system": system(c["skill"]),
        "user": user(c["transcript"]),
        "destination": c.get("app") and f'{c["app"]} ({c["package"]})',
    })
for skill, items in by_skill.items():
    (out / f"{skill}.json").write_text(json.dumps(items, indent=1, ensure_ascii=False))
print({k: len(v) for k, v in by_skill.items()})
