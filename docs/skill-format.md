# Skill format

The full reference for a ScribeKey skill: the folder, the `SKILL.md` manifest, the inputs file,
and what ScribeKey does with each part. The [README](../README.md) has the short version.

A ScribeKey skill is an [Agent Skill](https://agentskills.io). Everything ScribeKey adds sits under
`metadata`, which the spec defines as string keys and string values, so any other client that reads
Agent Skills can still use these skills and ignores the extra keys.

## Folder

```text
skills/email/
├── SKILL.md            required: manifest and instructions
├── references/…        optional text files the instructions name
└── assets/inputs.json  optional: the values a Make run asks for
```

- The folder name is the skill's `name`.
- Only `SKILL.md`, `references/` and `assets/` are read. Files must be text.
- `scripts/` is not allowed. ScribeKey never runs code.
- A file under `references/` or `assets/` reaches the model only when the instructions name it by
  path.

## SKILL.md

YAML frontmatter, then the instructions in Markdown.

```yaml
---
name: email
description: >-
  Greeting, clear paragraphs, sign-off. Turns dictation into an email body ready to paste; use when writing an email.
license: Apache-2.0
metadata:
  version: "1.4.1"
  author: scribekey
  scribekey-title: Email
  scribekey-icon: mail
  scribekey-actions: rewrite,make
  scribekey-presentation: text
  scribekey-inputs: assets/inputs.json
  scribekey-apps: >-
    com.google.android.gm
    com.microsoft.office.outlook
  scribekey-categories: email
---

Write the body of an email the speaker can send as is.
…
```

### Spec keys

| Key | Required | Meaning |
| --- | --- | --- |
| `name` | Yes | Lowercase letters, digits and hyphens, matching the folder. It identifies the skill: installing the same name again updates it. |
| `description` | Yes | What the skill does, then when to use it, up to 1,024 characters. The first sentence is the line shown under the skill's name. |
| `license` | In this catalogue | `Apache-2.0`. |
| `metadata` | In this catalogue | String keys to string values only. A YAML list or a number fails the check, so quote versions (`"1.0.0"`). |

### Catalogue keys

| Key | Required | Meaning |
| --- | --- | --- |
| `metadata.version` | In this catalogue | `major.minor.patch`. ScribeKey offers **Update** when it changes. Bump it on every change; CI enforces this. |
| `metadata.author` | No | Your GitHub name. |

### What the skill does

| Key | Default | Values and meaning |
| --- | --- | --- |
| `scribekey-actions` | both | `rewrite` changes text in place: it is offered in Improve and the dictation bubble. `make` adds a new document to the session: it is offered in Studio and after meetings. `rewrite,make` does both. An unknown value falls back to the default and shows a diagnostic. |
| `scribekey-output-format` | `text/markdown` | What a Make run produces: `text/markdown` or `text/vnd.mermaid` today. `text/html`, `image/png` and `audio/mpeg` are reserved. |
| `scribekey-presentation` | `text` | How Studio shows a Make result: `text` or `diagram` today. `page`, `slides`, `image` and `audio` are reserved. |
| `scribekey-requires` | none | Space-separated capabilities the skill needs from the app. `render.mermaid` draws Mermaid as a diagram. A skill that needs something this build lacks installs but gets no Studio tile. |

Studio offers a tile only for a pair the app can show: Markdown shown as `text`, or Mermaid shown
as `diagram` with `scribekey-requires: render.mermaid`. Any other pair installs and still rewrites,
if it declares `rewrite`, but makes nothing.

### How it runs

| Key | Default | Meaning |
| --- | --- | --- |
| `scribekey-writing-rules` | `on` | `on` wraps the instructions in ScribeKey's writing rules: cleanup, the person's Dictionary and their style. `off` sends the instructions as written, for a skill that sets its own format completely, such as a diagram. In the app this is **Add ScribeKey's writing rules** under the editor's Advanced section. The Dictionary still runs over the result either way. |
| `scribekey-inputs` | none | Path to the inputs file, usually `assets/inputs.json`. See [Inputs](#inputs). |

### How it looks

| Key | Default | Meaning |
| --- | --- | --- |
| `scribekey-title` | `name`, humanised | The title in lists, menus and tiles. |
| `scribekey-icon` | `auto_awesome` | One of the bundled Material Symbol names listed in [`schema/skill-frontmatter.schema.json`](../schema/skill-frontmatter.schema.json). Name what the skill makes. Anything else falls back to the default. |

### Where it is suggested

Suggestions only change order. They never run a skill on their own, and never grant a permission.

| Key | Meaning |
| --- | --- |
| `scribekey-apps` | Android package names, separated by spaces or new lines. The bubble lists the skill first, marked as suggested, when you dictate in one of them. Suggest an app only when the skill's output fits the box you dictate into there. |
| `scribekey-categories` | `email` (apps that open `mailto:` links), `messaging` (apps that open `smsto:` links), or both. Like `scribekey-apps`, for apps the author cannot list one by one. |
| `scribekey-suggested-fields` | Field kinds the skill suits, currently `search`. |
| `scribekey-discovery-categories` | Topics for browsing the catalogue: `writing`, `search`, `productivity`, `developer-ai`, `languages`. Separate from `scribekey-categories`. |

## Instructions

The Markdown after the frontmatter is what the model reads. Write it as instructions to a model
that sees only the transcript. The house style follows Matt Pocock's
[writing-for-agents](https://github.com/mattpocock/skills) skill: numbered steps, one check at the
end, no meta commentary.

These variables are filled in where the skill runs:

| Variable | Becomes |
| --- | --- |
| `{{dictionary}}` | The person's Dictionary: Words, then each Replacement with what it is heard as. A skill that places it gets no second copy. |
| `{{app}}` | The app being dictated into, when known. |
| `{{language}}` | The transcript's language code, such as `en`. |

These four are the person's own details, from About you in the app:

| Variable | Becomes |
| --- | --- |
| `{{first_name}}`, `{{last_name}}` | The person's name. |
| `{{full_name}}` | First and last name together. |
| `{{about_me}}` | What the person wrote about themselves. |

Any other `{{name}}` is not a detail ScribeKey saves, so it always arrives empty. ScribeKey
sends only the details a skill names. Each placeholder becomes its name in backticks
(`` `full_name` ``) and the values follow the instructions as one fenced JSON block of data, so
a value can never act as an instruction. A detail the person has not set arrives empty, with the
rule to leave it out, so write "the name, when it is set" rather than assuming one. Installing a
skill offers to fill in the details it names that the person has not set yet.

## Inputs

`scribekey-inputs` names a JSON file that declares the values a Make run asks for before it runs,
such as a length or a tone. It is a small subset of JSON Schema:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "length": {
      "type": "string",
      "title": "Length",
      "enum": ["Short", "Standard", "Detailed"],
      "default": "Standard",
      "x-scribekey-control": "connected"
    }
  },
  "additionalProperties": false
}
```

| Part | Meaning |
| --- | --- |
| `type` | `string` or `boolean`. |
| `title`, `description` | The label, and one short support line. |
| `enum`, `default`, `maxLength` | Choices, the preselected value, and a free-text limit for a `string`. |
| `required` (on the root) | Keys Make waits for. |
| `x-scribekey-control` | `connected` (button group), `cards`, `language` (a language picker; the value `source` keeps the transcript's language) or `multiline`. |
| `x-scribekey-labels` | For an `enum`: the value sent mapped to the label shown. |

Anything else becomes a diagnostic and is left out; the skill still installs and runs. The chosen
values reach the model as a JSON block at the end of a Make run, so the instructions should say
what each value means and what to assume when it is missing. See
[`skills/email/SKILL.md`](../skills/email/SKILL.md).

## Default skills

ScribeKey ships four skills from this catalogue: Polish, Summary, Flowchart and Email. They are
ordinary catalogue skills, the way Claude Code and Codex ship bundled skills inside their binaries:

- The app carries a copy, so they work offline from the first launch. The copy is written by
  `scripts/skills/sync_default_skills.py` in the app repository from a pinned commit here.
- They show as **Default** and **Included**. They can be turned off but not deleted or uninstalled.
- An app update brings their new wording. Editing one in the app marks it **Edited** and stops
  those updates; **Reset** brings back the shipped copy, and **Restore default skills** resets all
  four and turns them on.

A change to a default lands here first, then ships in the next app build that bumps the pin.

## Updates

ScribeKey compares `metadata.version` with what it installed and offers **Update**. A marketplace
that is a plain repository without versions is compared by the content of the skill's link
instead. Updating replaces the installed copy, including any edits made in the app.

## Checking a skill

```sh
node scripts/skills.mjs check   # names, versions, metadata values, a fresh index.json
node scripts/skills.mjs build   # regenerate index.json after a change
```

CI runs `check` on every pull request. The schemas in [`schema/`](../schema) give editors
autocomplete; they cannot see that `name` matches the folder or that a changed skill bumped its
version, which is why `check` exists.
