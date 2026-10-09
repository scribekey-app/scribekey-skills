---
name: one-on-one
description: >-
  Updates, blockers and actions for each person. Turns a 1:1 conversation into notes; use after a one-on-one, check-in or mentoring call.
license: MIT
metadata:
  version: "1.0.0"
  author: scribekey
---

Turn a one-on-one conversation into notes both people can look back on.

The text is a transcript in turns, each paragraph starting with the speaker's name in bold (`**Ana:** words`), or one person's recap with no names.

1. Start with a ## title: "1:1" and the two names, for example "## 1:1 Ana and Ken".
2. For each person with news about their own work, a ### heading with their name, then **Updates** (what they did) and **Blockers** (what stops them) as - bullets, in the third person. Write a label only when it has a bullet under it.
3. ### Feedback, then one - bullet per piece of praise or criticism of the other person's work, as "Giver to receiver: what was said". Feedback is never an update.
4. ### Actions, then one - [ ] item per promise to do something: the owner's name, a colon, the task, and the due date when it was said. A promise is never an update.

Who owns a promise: "I'll" means the person whose turn it is. In "**Ana:** I'll chase design by Thursday" the owner is Ana, so the item is "- [ ] Ana: chase design by Thursday".

Leave out any heading or label with nothing under it; never write an empty bullet or "None". Keep feedback exactly as strong or as soft as it was said. Keep each speaker's name exactly as written, "Speaker 2" included.

Example of the shape:
## 1:1 Ana and Ken
### Ken
**Updates**
- Shipped the export screen
**Blockers**
- Waiting on design for the empty state
### Feedback
- Ana to Ken: the release notes were clear and on time
### Actions
- [ ] Ana: ask design for the empty state by Thursday

Keep only the parts the text has. Criticism and a promise in reply, "**Lee:** The demo slipped and it cost us the client call. **Jo:** Sorry, I'll send a status note every Monday.", give no person headings:
## 1:1 Lee and Jo
### Feedback
- Lee to Jo: the demo slipped and it cost the client call
### Actions
- [ ] Jo: send a status note every Monday

Check: every update, blocker, piece of feedback and action appears once, under the right person, and nothing appears that neither person said.

Every name, number, date and fact comes from the text exactly as given, in the language of the text.
