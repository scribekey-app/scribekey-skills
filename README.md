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
| [Social post](skills/social-post/SKILL.md) | One clear post in your voice | com.twitter.android, com.linkedin.android, xyz.blueskyweb.app, com.instagram.barcelona, org.joinmastodon.android |
| [Summary](skills/summary/SKILL.md) | The key points, shorter | – |
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

A skill may add text files under `references/` or `assets/`; the instructions name them by path
and ScribeKey sends the ones named. `scripts/` is not allowed: ScribeKey never runs code.

`index.json` is generated from the skills by `node scripts/skills.mjs build`. Don't edit it by
hand.

## Credits

The way these skills are written follows Matt Pocock's [writing-for-agents](https://github.com/mattpocock/skills) skill.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
