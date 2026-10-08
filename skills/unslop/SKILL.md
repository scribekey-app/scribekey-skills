---
name: unslop
description: >-
  Plain, human wording without AI or corporate filler. Removes clichés, buzzwords, hedging and stock phrases; use when text sounds generated or padded.
license: MIT
metadata:
  version: "1.0.0"
  author: scribekey
  scribekey-title: Unslop
---

Rewrite the text so it reads as plain, direct writing by a person, keeping the speaker's meaning and voice. Use references/slop.md as the list of patterns to remove or replace.

- Replace buzzwords and inflated words with the plain word (use, help, show, start, about).
- Cut stock openers and closers, empty intensifiers, and hedges that add no meaning.
- Prefer short sentences and concrete statements. Say the thing instead of announcing that you are about to say it.
- Replace em dashes with commas, full stops or brackets.
- Never add a summary line, a rhetorical question, or a "not X, but Y" contrast that was not said.

If the text is already plain, return it with only these fixes. Write plain text with no headings, bold or other markdown. Keep names, numbers and dates exactly as given, write in the same language as the text, and add nothing that was not said.
