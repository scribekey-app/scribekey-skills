# Contributing

New skills and improvements are welcome. One skill per pull request.

## Add a skill

1. Create `skills/<name>/SKILL.md`. `<name>` is lowercase letters, digits and hyphens, and is the
   same as the `name` field. Copy an existing skill as a starting point.
2. Set `license: MIT` and `metadata.version: "1.0.0"`.
3. Add `metadata.scribekey-apps` only for apps the skill is clearly written for. Use the package
   name from the app's Play Store link (`id=` in the URL). When the skill suits every app of a
   kind, add `metadata.scribekey-categories: email` or `messaging` as well.
4. Run `node scripts/skills.mjs build` (Node 18 or later, nothing to install), then commit
   `index.json` with your skill.
5. Open a pull request with one real dictated example and what the skill returned.

## Change a skill

Edit its files, bump `metadata.version` (patch for wording, minor for new behaviour, major when
the output changes shape), and run `node scripts/skills.mjs build`. People who installed it are
offered **Update** in ScribeKey after it merges. Their own edits and settings are kept until they
choose Update.

## What CI checks

`node scripts/skills.mjs check` runs on every pull request. It fails when:

- the frontmatter is not the plain form shown in the README, or a required field is missing;
- `name` breaks the Agent Skills rules or does not match its folder;
- the description is over 1,024 characters or the instructions over 20,000;
- `metadata.version` is not `MAJOR.MINOR.PATCH`, or a changed skill kept its old version;
- an entry in `scribekey-apps` is not an Android package name, or one in `scribekey-categories` is
  not `email` or `messaging`;
- the folder has `scripts/` or anything other than text under `references/` and `assets/`;
- `index.json` is out of date.

Run it yourself before pushing: `node scripts/skills.mjs check --base origin/main`.

## The review bar

Dictation goes straight into someone's email or chat, often without a second look. A skill is
merged when it:

- does one job, named in the first sentence of its description;
- keeps every name, number, date and fact as given, in the language of the text;
- writes plain text unless the destination renders markdown;
- handles its edge cases in the instructions (a very short input, nothing to act on);
- passes the writing rules below.

## Writing a skill

A skill is read by a model, once per dictation, with the transcript beside it. These rules come
from Matt Pocock's [writing-for-agents](https://github.com/mattpocock/skills) skill; the skills
here follow them.

1. **Open with the job and the reader.** One sentence: what to produce and who it is for. "Write a
   team chat message a colleague can act on at a glance."
2. **Number the steps** when the output has a shape (greeting, body, sign-off). A flat paragraph
   of rules suits a style skill such as Professional.
3. **End on a check.** A `Check:` line the model can test its draft against, as exhaustive as the
   job allows: "every task in the text is one item, and every item is one task" beats "make a
   good list".
4. **Say what to do.** "Keep the hashtags the speaker said, and only those" lands better than
   "never add hashtags": naming a banned thing makes it more likely. Keep a prohibition only when
   it has no positive form, and pair it with the target.
5. **Use a strong word once** in place of a sentence that circles it: tight, faithful, scannable.
6. **Leave out what ScribeKey already does.** Before your skill runs, ScribeKey tells the model to
   return only the finished text, to write down a dictated question rather than answer it, to
   drop hesitation sounds and corrected false starts, and to write numbers as numerals. Repeating
   those spends tokens on every run and can argue with the app's own rules.
7. **Show, briefly, when the shape is unusual.** One short example (To-do list has one) fixes a
   format better than a paragraph describing it.
8. **Put long reference in `references/`** and name the file in the instructions, as Unslop does
   with `references/slop.md`. ScribeKey only sends the files the instructions name.

Every skill here ends with the same fidelity sentence: "Every name, number, date and fact comes
from the text exactly as given, in the language of the text." Keep it.

## Testing a skill

`evals/cases.json` holds three sample dictations per skill: a typical one and two edge cases.

```sh
python3 evals/build.py <scribekey checkout> . out/prompts   # the exact messages ScribeKey sends
OPENAI_API_KEY=... python3 evals/run.py out/prompts out/results.json 3
python3 evals/grade.py out/results.json
```

`run.py` defaults to ScribeKey's default cloud model, gpt-5-nano with minimal reasoning. Set
`MODEL` (and `BASE_URL` for another OpenAI-compatible host) to try others. `grade.py` scores each
case with a string check; read the outputs as well. Add cases and checks for a new skill.

Small models follow the first rules they read over a skill's later ones, so a skill that changes
the length or shape of the text has to say so plainly: name what to cut ("filler words, even
though plain clean-up keeps them"), and show the shape in one short example. Wording that works
on a small model works everywhere.

## Licence

By contributing you agree your contribution is released under the MIT licence in `LICENSE`.
