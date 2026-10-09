---
name: interview-qa
description: >-
  Each question paired with its answer. Turns an interview transcript with speakers into questions and answers; use after an interview, podcast or Q&A.
license: MIT
metadata:
  version: "1.0.0"
  author: scribekey
---

Turn an interview into questions and answers a reader can scan.

The text is a transcript in turns, each paragraph starting with the speaker's name in bold (`**Sam:** words`). It can also be one person's recap with no names.

1. Start with a ## title of up to six words, in sentence case, naming the interview's subject.
2. For each question, a line `**Q (Name):** the question`, then on the next line `**A (Name):** the answer`, then a blank line.
3. Write each answer in the answerer's own words, tightened: keep their claims, numbers and examples, drop repeats.
4. When the person asked declines ("let's skip that", "no comment", "pass") or nobody answers, the answer line is `**A (Name):** No answer`, never their words. The answerer is never the person who asked.

A follow-up that asks the same thing again joins its question. An answer spread over several turns of the same person is one answer. Keep each speaker's name exactly as written, "Speaker 2" included.

Example of the shape:
## Hiring the first designer
**Q (Ana):** What did you look for first?
**A (Sam):** A portfolio with shipped work, not concepts.

**Q (Ana):** How long did it take?
**A (Sam):** Six weeks from posting to offer.

Check: every question asked appears once, each with the answer it got, and every answer is something the answerer said.

Every name, number, date and fact comes from the text exactly as given, in the language of the text.
