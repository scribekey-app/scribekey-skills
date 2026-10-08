---
name: unslop
description: >-
  Plain, human wording without AI or corporate filler. Removes clichés, buzzwords, hedging and stock phrases; use when text sounds generated or padded.
license: MIT
metadata:
  version: "1.1.0"
  author: scribekey
  scribekey-title: Unslop
---

Edit the text so it reads as plain writing by a person. references/slop.md lists the patterns, each with its fix.

1. Scan the text for every pattern in references/slop.md.
2. Rewrite each hit with its fix, keeping the meaning, the facts and the speaker's voice.
3. Give it a voice. Vary sentence length, and keep the speaker's own phrasing and first person where they used it. Text with the patterns stripped but no voice left reads as generated too.
4. Scan the result again and fix anything left.

When the text is already plain, return it with only those fixes.

Check: no pattern from references/slop.md remains, and every fact is still there.

Write plain text: sentences and line breaks only. Every name, number, date and fact comes from the text exactly as given, in the language of the text.
