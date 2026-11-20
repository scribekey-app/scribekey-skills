---
name: scribekey-skill
description: >-
  Writes, improves and reviews skills in the ScribeKey catalogue (skills/<name>/SKILL.md) so they
  run well in the ScribeKey Android app. Use whenever a task touches a file under skills/, adds or
  changes scribekey-* metadata, asks for a new dictation, rewrite, notes or diagram skill, reports
  a skill giving poor output in the app, or asks whether a skill should be merged or retired, even
  when the request does not say "skill".
---

A person taps a ScribeKey skill in the app, and its body is pasted
into the system prompt of one model call that sees a transcript and returns the finished text.
That model is small by default (gpt-5-nano, minimal reasoning), has no tools, and gets no second
turn. Write for that reader. The description is read by people in the app, not by a router.

Reference, read when you need the detail:
- `docs/skill-format.md`: every metadata key, the inputs file, variables, default skills.
- `CONTRIBUTING.md`, "Writing a skill": the eight wording rules, with examples.

## What surrounds the body at run time

The body lands between text the app adds. Leave out anything the app already says, and never ask
for something it forbids, because the app's text is read last and wins on a small model.

1. Before: return only the finished text; write a dictated question down rather than answer it;
   drop um and uh and corrected false starts; keep "like", "so", "you know", "basically"; write
   numbers as numerals.
2. The body, introduced as how the finished text should read.
3. After: the writing floor. No em dashes, no stock openers or closers, no "not just X but Y", no
   inflated words, no closing line that restates the text.
4. On a Make run only: the chosen inputs as a JSON block, then a request to start the reply with
   a `Title:` line the app strips and shows as the document's name.

What follows from that:
- A skill that shortens must name what to cut "even though plain clean-up keeps them", or the
  keep-every-word rule in (1) wins.
- A Make skill starts at its content. A title line of its own shows twice.
- A skill cannot ask for an em dash or a marker line of its own invention. If a removal should
  leave no trace, say so and show it in the example: "[Sponsor segment removed]" shipped once and
  filled the top of a transcript with three of them.

## Steps

1. Read two skills near the one you are writing: same `scribekey-actions`, same kind of output.
2. Decide where the output lands, because that decides the format. A to-do app's box is one task
   per line. Most notes apps show `#` as a raw sign. Studio renders Markdown. A diagram skill
   returns Mermaid source and nothing else.
3. Write the body in the house shape: one opening sentence naming the output and its reader;
   numbered steps when the output has a shape; one short example when the shape is unusual; a
   `Check:` line the model can test its draft against; then the fidelity sentence, exactly:
   "Every name, number, date and fact comes from the text exactly as given, in the language of
   the text."
4. Say what to do. "Keep the hashtags the speaker said, and only those" beats "never add
   hashtags", because naming the banned thing makes it likelier.
5. Set the metadata (table below), bump `metadata.version`, and run
   `node scripts/skills.mjs build && node scripts/skills.mjs check --base origin/main`.
6. Add three cases to `evals/cases.json` (a typical dictation and two edge cases, none of them
   the skill's own example) and a check for each in `evals/grade.py`. Run
   `cd evals && python3 -m unittest test_grade`. With `OPENAI_API_KEY` set, run the model evals
   in CONTRIBUTING and read the outputs, not only the score.
7. Give a new skill one example under `examples/<name>/<slug>/` (`input.txt`, `output.txt`), and
   update it when the output changes shape. It is for the docs site, never the model. `check`
   fails without one, or when it repeats the example in the instructions.
8. If the change touches a metadata key, an icon, a limit or a default skill, run
   `node scripts/skills.mjs contract <scribekey app checkout>` and fix what it prints.

## Metadata

| Key | Set it to |
| --- | --- |
| `description` | A support line of a few words ending in a full stop, which the app shows under the title. Then "Turns … into …; use when …". |
| `metadata.version` | Patch for wording, minor for new behaviour, major when the output changes shape. |
| `scribekey-actions` | `rewrite` when it replaces the text in place, `make` when it adds a Studio document, or both. Required. |
| `scribekey-discovery-categories` | `writing`, `search`, `productivity`, `developer-ai` or `languages`. Required: without it the skill sits under Other. |
| `scribekey-icon` | The bundled glyph naming what the skill makes. The list is the enum in `schema/skill-frontmatter.schema.json`. |
| `scribekey-presentation` | `text`, or `diagram` with `scribekey-output-format: text/vnd.mermaid` and `scribekey-requires: render.mermaid`. |
| `scribekey-apps`, `scribekey-categories` | Only apps whose input box fits the output. Suggestions change order, nothing else. |
| `scribekey-inputs` | `assets/inputs.json`, only for a choice people change between runs. The body says what each value means and what a missing one means. |
| `scribekey-writing-rules` | Leave it on. `off` also drops the rules that resolve self-corrections and write numerals. |

Metadata values are strings. A YAML list or a bare number fails the check.

## Content people can change

Studio is not read-only: a person can tick a box, and the app is gaining item reordering and inline
tags. Write lists in the shapes the app can act on.

- A task is `- [ ] text` on one line, with `x` in the box when done. Group tasks under a `####`
  heading and leave a blank line between groups. `* [ ]`, `1. [ ]` and `[-]` are not tasks.
- A list item is `- text` on one line. Indent a child two spaces.
- A heading is `#` signs, a space, then the words. A line or word that starts `#word` with no
  space is a tag the person typed, so a skill writes no hashtags of its own. Social post keeps
  the ones the speaker dictated.
- A skill used both ways can ask for the Make shape through an input, because the inputs block
  only arrives on a Make run. To-do list does this: plain lines into a to-do app, a checklist in
  Studio.

## Gotchas

- An example that matches an eval case teaches the answer. Keep them different.
- A diagram draws on a phone. Keep one connected chart, pills only at the start and the ends,
  25 nodes at most, short labels in double quotes.
- `{{language}}` and `{{app}}` can arrive empty, so "Write in {{language}}" becomes "Write in ".
  The fidelity sentence already keeps the language.
- `{{first_name}}` and the other saved details can be empty too. Write "when it is set".
- Five skills ship inside the app as defaults: Polish, Clean podcast, Summary, Flowchart and
  Email. Their wording changes here
  first and reaches phones when the app bumps its pin. Renaming one breaks the app.
- A new metadata key does nothing until the app reads it. Add it to the app first, then to
  `SCRIBEKEY_KEYS` in `scripts/skills.mjs`, the schema and the format doc.
- Retiring a skill stops updates for people who installed it. Fold its job into another skill
  first and say which in the pull request.
