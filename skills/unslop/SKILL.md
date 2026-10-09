---
name: unslop
description: >-
  Plain, human wording without AI or corporate filler. Removes clichés, buzzwords, hedging and stock phrases; use when text sounds generated or padded.
license: MIT
metadata:
  version: "1.1.1"
  author: scribekey
  scribekey-title: Unslop
---

Edit the text so it reads as plain writing by a person. references/slop.md lists the patterns, each with its fix.

The commonest, which the text must not keep:
- "not just X, it's Y" and "it's not X, it's Y": say Y.
- Em dashes: use a full stop or a comma.
- Stock openers and closers: "I hope this finds you well", "I wanted to reach out", "circle back", "Hope this helps", "Let me know if you have any questions", "Don't hesitate to reach out". Cut them.
- Inflated and AI words: leverage, utilise, commence, seamless, robust, cutting-edge, empower, unlock, foster, drive innovation. Name the concrete thing or cut the phrase; a synonym is still slop.
- Filler phrases: "in today's fast-paced world", "it's worth noting that", "due to the fact that".

1. Scan the text for those and every other pattern in references/slop.md.
2. Rewrite each hit with its fix, keeping the meaning, the facts and the speaker's voice.
3. Give it a voice. Vary sentence length, and keep the speaker's own phrasing and first person where they used it.
4. Scan the result again and fix anything left.

When the text is already plain, return it unchanged. When stripping the patterns leaves little, return the little that is left.

Check: no pattern from the list above or references/slop.md remains, and every fact is still there.

Write plain text: sentences and line breaks only. Every name, number, date and fact comes from the text exactly as given, in the language of the text.
