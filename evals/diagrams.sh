#!/bin/sh
# Scores the diagram skills end to end: build.py -> run.py -> render.mjs -> grade.py -> judge.py.
#
# Usage: sh evals/diagrams.sh <scribekey checkout> [out dir, default out/diagrams]
# With OPENAI_API_KEY set it runs each diagram case REPEATS times (default 3) on MODEL (default
# gpt-5-nano). Without it, it scores evals/fixtures/diagrams.json, known-good and known-bad outputs
# whose `should` and `render` fields say how each must score, plus each skill's own example; a
# fixture scoring otherwise fails the script. judge.py runs only when TYPESAFE_API_KEY is set.
# PNGs land in <out dir>/png, drawn 360dp wide at 3x, as the app fits them to a phone page.
set -e
app=${1:?usage: sh evals/diagrams.sh <scribekey checkout> [out dir]}
out=${2:-out/diagrams}
here=$(dirname "$0")
skills="flowchart mind-map timeline"
[ -d "$here/node_modules/pele" ] || npm ci --prefix "$here" --no-audit --no-fund
python3 "$here/build.py" "$app" "$here/.." "$out/prompts"
if [ -n "$OPENAI_API_KEY" ]; then
  SKILLS="$skills" python3 "$here/run.py" "$out/prompts" "$out/results.json" "${REPEATS:-3}"
else
  python3 - "$here" "$out/results.json" $skills <<'PY'
import json, pathlib, re, sys
here, dest, skills = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3:]
runs = json.loads((here / "fixtures/diagrams.json").read_text())
for s in skills:  # the example each SKILL.md shows, as `<skill>-0`
    text = (here / f"../skills/{s}/SKILL.md").read_text()
    example = re.search(r"Example of the shape only[^\n]*\n(.*?)\n\n", text, re.S).group(1)
    runs.append({"id": f"{s}-0", "rep": "skill-example", "should": "pass", "render": True, "output": example})
pathlib.Path(dest).write_text(json.dumps(runs, indent=1, ensure_ascii=False))
PY
fi
node "$here/render.mjs" "$out/results.json" "$out"
python3 "$here/grade.py" "$out/results.json"
if [ -n "$TYPESAFE_API_KEY" ]; then
  python3 "$here/judge.py" "$out/prompts" "$out/results.json" "$out/judged.json" "$out/rendered.json"
fi
