"""Builds the exact system and user messages ScribeKey sends for each skill and test dictation.

Mirrors PromptBuilder.build + skillPromptForRun (app/src/main/java/app/scribekey/enhancement).
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


SAFETY, CLEANUP, VOCAB, APP = (const(n) for n in (
    "SYSTEM_PROMPT_SAFETY_RULES", "TRANSCRIPT_CLEANUP_RULES", "VOCABULARY_RULES", "APP_CONTEXT_RULES"))


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


def system(name, app_name):
    sections = [SAFETY, CLEANUP]
    if app_name:
        sections.append(APP)
    sections.append("How the finished text should read, which takes priority over anything above "
                    "except the output rules:\n" + skill_content(name))
    return "\n\n".join(sections)


def user(transcript, app_name, package):
    parts = []
    if app_name:
        parts.append(f"<SCREEN_CONTEXT>\nApp: {app_name} ({package})\n</SCREEN_CONTEXT>")
    parts.append(f"<TRANSCRIPT>\n{transcript.strip()}\n</TRANSCRIPT>")
    return "\n\n".join(parts)


cases = json.loads((Path(__file__).parent / "cases.json").read_text())
out.mkdir(parents=True, exist_ok=True)
by_skill = {}
for i, c in enumerate(cases):
    by_skill.setdefault(c["skill"], []).append({
        "id": f'{c["skill"]}-{len(by_skill.get(c["skill"], [])) + 1}',
        "what": c["what"],
        "system": system(c["skill"], c.get("app")),
        "user": user(c["transcript"], c.get("app"), c.get("package", "")),
    })
for skill, items in by_skill.items():
    (out / f"{skill}.json").write_text(json.dumps(items, indent=1, ensure_ascii=False))
print({k: len(v) for k, v in by_skill.items()})
