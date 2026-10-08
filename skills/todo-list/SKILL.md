---
name: todo-list
description: >-
  Tasks you can tick off. Turns spoken errands and commitments into a checklist; use in a to-do app.
license: MIT
metadata:
  version: "1.1.0"
  author: scribekey
  scribekey-title: To-do list
  scribekey-apps: >-
    com.todoist
    com.google.android.apps.tasks
    com.microsoft.todos
    com.ticktick.task
---

Turn the text into a checklist.

1. Write each task, errand or commitment as one - [ ] item that starts with a verb.
2. Keep each date, time, place or person on the item it belongs to.
3. Put anything that is not a task in one short line after the list.

Start with the first item. When the text holds no tasks, return it unchanged.

Check: every task in the text is one item, and every item is one task.

Example. "need to call mum on sunday and pick up the dry cleaning, oh and the car's due for a service next month" becomes:
- [ ] Call Mum on Sunday
- [ ] Pick up the dry cleaning
- [ ] Get the car serviced next month

Every name, number, date and fact comes from the text exactly as given, in the language of the text.
