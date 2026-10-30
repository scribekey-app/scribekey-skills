---
name: work-chat
description: >-
  Short, clear and friendly for a team channel. Turns dictation into a work chat message; use in Slack, Teams or Google Chat.
license: Apache-2.0
metadata:
  version: "1.3.0"
  author: scribekey
  scribekey-apps: >-
    com.Slack
    com.microsoft.teams
    com.google.android.apps.dynamite
    com.mattermost.rn
    im.vector.app
  scribekey-actions: rewrite,make
  scribekey-presentation: text
---

Write a team chat message a colleague can act on at a glance.

1. First sentence: the point or the ask. A spoken "at" before a name is a mention: "at maya" is @maya.
2. Then the detail in short sentences. When the message is a list of separate updates, give every update its own - line, the first one too.
3. Open with "Hi" or the person's name only when the speaker addressed someone, and end on the last point.

Write spoken file names, code and links the way they are typed: "checkout underscore service dot log" is checkout_service.log.

Example. "at sam can you check the build log before two" becomes "@sam can you check the build log before 2 pm?" and "quick ones the demo moved to two and the slides are in the shared drive" becomes:
- The demo moved to 2 pm.
- The slides are in the shared drive.

Check: someone reading only the first line knows what is needed from them, and the message is punctuated.

Write plain text: sentences, line breaks and - items only. Every name, number, date and fact comes from the text exactly as given, in the language of the text.
