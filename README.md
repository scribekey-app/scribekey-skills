# ScribeKey skills

Curated [Agent Skills](https://agentskills.io) for [ScribeKey](https://scribekey.app), the Android
voice-to-text app. Each one turns dictation into something ready to send: an email, a to-do list,
a prompt for an agent. Apache 2.0 licensed.

ScribeKey lists this repository as its default skill marketplace. Open **Settings → Skills →
Marketplaces** to install one; it shows **Update** when a new version lands here.

The skills are ordinary `SKILL.md` files, so any client that reads Agent Skills can use them.

## Skills

| Skill | What it does | Suggested apps |
| --- | --- | --- |
| [Prompt for an agent](skills/agent-prompt/SKILL.md) | Goal, context, constraints, done when | com.openai.chatgpt, com.anthropic.claude, com.google.android.apps.bard, ai.mistral.chat, com.deepseek.chat, ai.x.grok |
| [Clean up](skills/clean-up/SKILL.md) | Punctuation, fillers and false starts | – |
| [Concise](skills/concise/SKILL.md) | Same message, fewer words | – |
| [Email](skills/email/SKILL.md) | Greeting, clear paragraphs, sign-off | com.google.android.gm, com.microsoft.office.outlook, com.samsung.android.email.provider, ch.protonmail.android, com.fastmail.app, com.readdle.spark |
| [Friendly message](skills/friendly-message/SKILL.md) | Warm and conversational | com.whatsapp, com.google.android.apps.messaging, com.samsung.android.messaging, org.thoughtcrime.securesms, org.telegram.messenger, com.facebook.orca, com.whatsapp.w4b, com.viber.voip, jp.naver.line.android, com.discord |
| [Interview Q&A](skills/interview-qa/SKILL.md) | Each question paired with its answer | – |
| [Lecture notes](skills/lecture-notes/SKILL.md) | Study notes by topic, with questions from the room | – |
| [Meeting notes](skills/meeting-notes/SKILL.md) | Summary, decisions and actions | – |
| [Notes](skills/notes/SKILL.md) | Bullet points by topic | com.google.android.keep, com.samsung.android.app.notes, md.obsidian, notion.id, com.microsoft.office.onenote, com.automattic.simplenote |
| [1:1 notes](skills/one-on-one/SKILL.md) | Updates, blockers and actions for each person | – |
| [Professional](skills/professional/SKILL.md) | Polished and businesslike | – |
| [Search query](skills/search-query/SKILL.md) | One concise query for an ordinary web or search field | – |
| [Social post](skills/social-post/SKILL.md) | One clear post in your voice | com.twitter.android, com.linkedin.android, xyz.blueskyweb.app, com.instagram.barcelona, org.joinmastodon.android |
| [Summary](skills/summary/SKILL.md) | The key points, shorter | – |
| [Taobao search](skills/taobao-search/SKILL.md) | One Simplified Chinese product query | com.taobao.taobao |
| [To-do list](skills/todo-list/SKILL.md) | One task per line, for a to-do app | com.todoist, com.ticktick.task, com.google.android.apps.tasks, com.microsoft.todos, com.anydo |
| [Work chat](skills/work-chat/SKILL.md) | Short, clear and friendly for a team channel | com.Slack, com.microsoft.teams, com.google.android.apps.dynamite, com.mattermost.rn, im.vector.app |

Suggest an app only when the skill's output fits the box you dictate into there. A to-do app's box holds one task, so To-do list writes one plain line per task rather than a `- [ ]` checklist.

**Suggested apps** are an offer, never a switch. After you add a skill, its page in ScribeKey
lists the ones you have installed under **Apply automatically**, each with its own switch.

## Format

A skill is a folder with a `SKILL.md`: YAML frontmatter, then the instructions. ScribeKey's
additions live under `metadata`, which the Agent Skills spec defines as string keys to string
values, so other clients ignore them.

```yaml
---
name: email                     # required. Lowercase, digits, hyphens. Matches the folder.
description: >-                 # required. What it does, then when to use it. ≤ 1,024 characters.
  Greeting, clear paragraphs, sign-off. Turns dictation into an email body ready to paste.
license: Apache-2.0             # required here
metadata:
  version: "1.0.0"              # required here. Bump it on every change.
  author: your-github-name      # optional
  scribekey-title: Email        # optional. Display name; default is the name humanised.
  scribekey-apps: >-            # optional. Android package names, space-separated.
    com.google.android.gm
    com.microsoft.office.outlook
  scribekey-categories: email   # optional. email, messaging, or both.
  scribekey-discovery-categories: writing  # optional. writing, search, productivity, developer-ai, languages.
  scribekey-suggested-fields: search  # optional. Suggestion order for matching field kinds; never runs a skill.
  scribekey-actions: rewrite,make  # rewrite (in place), make (Studio result), or both.
  scribekey-presentation: text     # how Studio shows a Make result: text, diagram, page, slides, image or audio.
  scribekey-icon: mail             # optional. Bundled Material Symbol: auto_awesome, article, checklist, mail, chat or code.
---

Rewrite the text as the body of an email…
```

| Key | Meaning in ScribeKey |
| --- | --- |
| `name` | The skill's identity. Installing the same name again updates it |
| `description` | The first sentence is the line under the skill's name |
| `metadata.version` | What **Update** compares |
| `metadata.scribekey-title` | The title shown in lists |
| `metadata.scribekey-apps` | Apps the skill offers to apply automatically in |
| `metadata.scribekey-categories` | Kinds of app it also offers itself in: `email` (apps that open `mailto:` links) or `messaging` (apps that open `smsto:` links). Each app still has its own switch |
| `metadata.scribekey-discovery-categories` | Optional catalogue topics, space- or comma-separated: `writing`, `search`, `productivity`, `developer-ai`, `languages`. This is separate from app kinds in `scribekey-categories` |
| `metadata.scribekey-suggested-fields` | Optional field kinds for suggestion ordering, currently `search`. This only influences recommendations; it never runs a Skill or grants a permission |
| `metadata.scribekey-actions` | `rewrite` (changes text in place: bubble, Improve), `make` (adds a Studio result), or `rewrite,make`. The marketplace groups on this; omitting it lists the skill as Make only |
| `metadata.scribekey-presentation` | How Studio shows a Make result: `text`, `diagram`, `page`, `slides`, `image` or `audio`. Default `text` |
| `metadata.scribekey-icon` | Marketplace and tile glyph. One of `auto_awesome`, `article`, `checklist`, `mail`, `chat`, `code`. Related skills share a glyph; omitting it uses auto_awesome |

A skill may add text files under `references/` or `assets/`; the instructions name them by path
and ScribeKey sends the ones named. `scripts/` is not allowed: ScribeKey never runs code.

`index.json` is generated from the skills by `node scripts/skills.mjs build`. Don't edit it by
hand.

## Schema

There is no official Agent Skills JSON Schema: the spec is YAML frontmatter, and `metadata`
must stay string keys to string values. This catalog keeps that shape and adds:

- [`schema/skill-frontmatter.schema.json`](schema/skill-frontmatter.schema.json) — the `SKILL.md`
  frontmatter this repo accepts, including the `scribekey-*` keys
- [`schema/index.schema.json`](schema/index.schema.json) — the generated `index.json`

With the [YAML](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml) extension,
workspace settings map those schemas onto `skills/**/SKILL.md` and `index.json` so editors
autocomplete and flag a YAML list in `scribekey-actions` (it has to stay a string). CI still
runs `node scripts/skills.mjs check`: a schema cannot see that `name` matches the folder, that
a changed skill bumped `metadata.version`, or that `index.json` is fresh.

A `# yaml-language-server: $schema=…` comment in the frontmatter is allowed; existing skills
leave it out so installing them does not offer a no-op Update.

In `index.json`, these optional values appear as `discoveryCategories` and `suggestedFields`
arrays. Missing values stay omitted, so existing entries remain uncategorised and neutral.

## Credits

The way these skills are written follows Matt Pocock's [writing-for-agents](https://github.com/mattpocock/skills) skill.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
