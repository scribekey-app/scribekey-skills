---
name: introduce-me
description: >-
  A short first-person introduction written from your saved details. Use for a meetup, a cold email, a LinkedIn note or a short bio.
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: scribekey
  scribekey-discovery-categories: writing
  scribekey-actions: rewrite,make
  scribekey-presentation: text
  scribekey-icon: chat
---

Write a short first-person introduction the speaker can paste as is.

The text says what the introduction is for, and can add facts about the speaker. Facts in the text come first; the saved details fill in the rest: {{full_name}} is the speaker's name, {{about_me}} is what they wrote about themselves, and {{website}} is their website.

1. Open with "Hi, I'm" and the name the speaker said, otherwise {{full_name}} when it is set. With no name at all, open with what they do.
2. Then what the speaker does, chosen for this audience. What the text says comes first; add from {{about_me}} only what suits this audience.
3. Mention everything the text asks to mention.
4. Add {{website}} only when the text asks for a link or a website; otherwise the introduction has no link. When it is empty, leave the website out completely: no link, and no words that point to one.
5. Keep to the length the text asks for, otherwise two or three sentences.

Example. Saved name "Alex Chen", about "Android developer in Perth", and "intro for the book club, I've just joined and I love sci-fi" becomes:
Hi, I'm Alex Chen. I've just joined the book club and I love sci-fi. By day I'm an Android developer in Perth.

Check: every fact about the speaker comes from the text or the saved details, everything the text asked for is in it, and it has a link only when the text asked for one.

Write plain text: sentences and line breaks only. Every name, number, date and fact comes from the text or the saved details exactly as given, in the language of the text.
