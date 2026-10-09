---
name: meeting-notes
description: >-
  Decisions, each person's actions and open questions. Turns a meeting transcript with speakers, or a spoken recap, into notes; use after a meeting, call or class.
license: MIT
metadata:
  version: "2.0.0"
  author: scribekey
---

Turn a meeting into notes the people in it can act on.

The text is either a transcript in turns, each paragraph starting with the speaker's name in bold (`**Maria:** words`), or one person's spoken recap with no names, where the speaker is the note-taker.

1. Start with a ## title of up to six words, in sentence case, naming the meeting's topic.
2. ### Summary, then one to three sentences on what was covered and where it landed.
3. ### Decisions, then one - bullet per decision. A decision is anything said as settled: "we decided", "we agreed", "let's", "then we", "we'll go with", and a proposal the others say yes to. A topic left undecided or put off is an open question, not a decision.
4. ### Actions, grouped by owner. An action is a promise or an assignment: "I'll", "I can", "X will", "X is going to". A #### heading with the owner's name, then one - [ ] item per task, with the due date when it was said. A task someone asked for that nobody took on goes under #### Unassigned.
5. ### Open questions, then one - bullet per question raised and left unanswered.

Find every decision and action first, then write. Leave out a section only when the text has nothing for it, heading included; never write "None" or an empty item. These are not actions: waiting for something, such as paperwork arriving; a topic coming up again; a decision said again as a task.

In a transcript, "I" and "I'll" in a turn mean that turn's speaker: "**Speaker 3:** I'll update the notes" makes Speaker 3 the owner. Someone only mentioned is not an owner. Keep each speaker's name exactly as written, "Speaker 2" included.

Example of the shape:
## Android release timing
### Summary
The team moved the release back a week to fix a crash on Samsung phones.
### Decisions
- Delay the Android release by one week
### Actions
#### Maria
- [ ] Fix the Samsung crash and have it in review by Wednesday
#### Speaker 3
- [ ] Update the release notes and tell support by Friday
### Open questions
- Whether pricing changes ship with this release

A meeting where nothing was settled and nobody took anything on keeps only what it has. For "we went over the logo, half of us like the blue one, we'll look again next week, the printer quote arrives Friday" there is no Decisions or Actions section:
## Logo choice
### Summary
The group compared logo options without settling on one and will look again next week.
### Open questions
- Whether to use the blue logo

Check: every decision, action and open question in the text appears exactly once, each action sits under the person who took it on, and nothing appears that nobody said.

Every name, number, date and fact comes from the text exactly as given, in the language of the text.
