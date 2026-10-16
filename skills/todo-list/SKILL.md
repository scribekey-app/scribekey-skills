---
name: todo-list
description: >-
  One task per line, ready for a to-do app. Turns spoken errands and commitments into task titles; use in Todoist, TickTick, Google Tasks or Microsoft To Do.
license: Apache-2.0
metadata:
  version: "2.0.0"
  author: scribekey
  scribekey-title: To-do list
  scribekey-apps: >-
    com.todoist
    com.ticktick.task
    com.google.android.apps.tasks
    com.microsoft.todos
    com.anydo
---

Write the text as task titles for a to-do app, where each line becomes one task.

1. One line per task, errand or commitment. Start each line with its verb and end it without a full stop.
2. Keep each date, time and repeat with its own task, in the speaker's words, at the end of the line: "Call Mum on Sunday", "Water the plants every Monday". To-do apps read those words as the due date.
3. When someone else owns a task, put their name in brackets after it: Book the venue (Jamie).
4. Keep only the tasks. Feelings, asides and background stay out, because every line becomes a task.

A single task is a single line, which is the usual case. When the text holds no task at all, return it unchanged.

Example. "need to call mum on sunday, Sam's picking up the cake, oh and the car's due for a service next month, I'm so tired" becomes:
Call Mum on Sunday
Pick up the cake (Sam)
Get the car serviced next month

Check: every task in the text is one line, every line is one task, and each line starts with a verb.

Every name, number, date and fact comes from the text exactly as given, in the language of the text.
