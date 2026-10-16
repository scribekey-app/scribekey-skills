---
name: clean-up
description: >-
  Punctuation, fillers and false starts. Fixes dictated text without changing what was said; use when the words are right and only the transcription is rough.
license: Apache-2.0
metadata:
  version: "1.2.0"
  author: scribekey
---

Make the transcript read correctly while staying word-for-word faithful to what was said.

1. Fix punctuation, capitals, and words the transcription clearly misheard.
2. Delete hesitation sounds (um, uh), stutters, repeated words, and false starts the speaker corrected, keeping only the corrected version.
3. Break the text into sentences. Start a new paragraph where the speaker changes topic ("anyway, different thing").

Everything else stays as spoken: the speaker's words, word order, tone, swearing and length.

Example. "um so the the standup is at ten thirty actually no make that ten fifteen anyway different thing did you see the email" becomes:
So the standup is at 10:15.

Anyway, different thing. Did you see the email?

Check: each sentence matches what was said, apart from those repairs.

Write plain text: sentences and line breaks only. Every name, number, date and fact comes from the text exactly as given, in the language of the text.
