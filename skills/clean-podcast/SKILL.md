---
name: clean-podcast
description: >-
  Ads out, laid out by speaker and topic. Turns the transcript of a podcast or recording into a clean read with every word of the conversation kept; use on a session imported from a link or a file.
license: Apache-2.0
metadata:
  version: "1.1.0"
  author: scribekey
  scribekey-title: Clean podcast
  scribekey-discovery-categories: productivity
  scribekey-actions: rewrite
  scribekey-presentation: text
  scribekey-icon: forum
---

Turn a podcast transcript into a clean, readable transcript with the ads taken out. You are an editor, not a summariser: everything the hosts and guests said about the show's subject stays, in their words and order.

1. Take out advertising: sponsor reads ("brought to you by", "support comes from", "use code", "go to example.com/show", "first month free", "terms apply"), inserted ads in another voice, trailers for other shows, and pitches to rate, review, subscribe, join a Patreon or buy merch. Take out the hand-off into a break ("after a quick word from our sponsor") and the return from it ("anyway, back to it") as well. An ad leaves no trace: the conversation carries on from the last thing said before it, with no line, bracket or note where it stood. A transcript that opens with ads opens with the first words of the show.
2. Keep talk about a product, company or website that belongs to the conversation: an episode about a company, a tool a guest uses, a guest's book discussed as part of an answer. It is an ad only when it asks the listener to buy, visit, sign up or use a code.
3. Write each turn as a paragraph starting with the speaker's name in bold: `**Sam:** words`. Keep every speaker label and timestamp exactly as written, "Speaker 2" included, even when the talk reveals a name. When there are no names, write paragraphs without them and add none.
4. Delete hesitation sounds (um, uh), stutters ("we, we, we can't"), false starts the speaker corrected, and "you know", "like" or "I mean" where they are only filler, even though plain clean-up keeps them. Keep repetition said for emphasis ("no, no, no") and words that steer the argument ("well", "actually"). Fix punctuation, capitals and words the transcription clearly misheard. End a turn another speaker cut off with three dots.
5. Split a long turn into paragraphs of three to five sentences. Before each new topic, add a `## Heading` of up to six words naming it, in sentence case. Start with the conversation itself, not a heading.

When unsure whether a passage is an ad, keep it.

Example. "Speaker 1: so um the the study had 400 people. Speaker 2: and this episode is brought to you by Acme, go to acme.com slash pod for 20 percent off. anyway back to it. Speaker 1: yeah so 400 people over two years" becomes:
**Speaker 1:** So the study had 400 people.

**Speaker 1:** Yeah, so 400 people over two years.

Check: nothing left asks the listener to buy, visit or subscribe, nothing marks where an ad was, and every sentence that remains is something a speaker said, apart from those repairs.

Every name, number, date and fact comes from the text exactly as given, in the language of the text.
