# Contributing

New skills and improvements are welcome. One skill per pull request.

## Add a skill

1. Create `skills/<name>/SKILL.md`. `<name>` is lowercase letters, digits and hyphens, and is the
   same as the `name` field. Copy an existing skill as a starting point.
2. Set `license: MIT` and `metadata.version: "1.0.0"`.
3. Add `metadata.scribekey-apps` only for apps the skill is clearly written for. Use the package
   name from the app's Play Store link (`id=` in the URL).
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
- an entry in `scribekey-apps` is not an Android package name;
- the folder has `scripts/` or anything other than text under `references/` and `assets/`;
- `index.json` is out of date.

Run it yourself before pushing: `node scripts/skills.mjs check --base origin/main`.

## The review bar

Dictation goes straight into someone's email or chat, often without a second look. A skill is
merged when it:

- does one job, named in the first sentence of its description;
- keeps names, numbers and dates exactly as given, and adds nothing that was not said;
- writes in the language of the text;
- writes plain text unless the destination renders markdown;
- never asks the model to explain itself, greet the reader, or add a sign-off, emoji or call to
  action the speaker did not say;
- handles its edge cases in the instructions (a very short input, nothing to act on).

Most skills here end with the same fidelity sentence. Keep it.

## Licence

By contributing you agree your contribution is released under the MIT licence in `LICENSE`.
