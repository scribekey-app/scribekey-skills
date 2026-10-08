---
name: agent-prompt
description: >-
  Goal, context, constraints, done when. Turns a spoken request into instructions for a coding or chat agent; use in an AI assistant app.
license: MIT
metadata:
  version: "1.0.0"
  author: scribekey
  scribekey-title: Prompt for an agent
  scribekey-apps: >-
    com.openai.chatgpt
    com.anthropic.claude
    com.google.android.apps.bard
    ai.perplexity.app.android
---

Turn the text into instructions for a coding or chat agent, written to the agent as "you". Use these parts in order, each starting with its label and a colon on its own line: Goal (one sentence on what to do), Context (bullets with the background, files, names and facts that were said), Constraints (bullets with what the agent must or must not do), Done when (bullets saying how the agent knows it has finished). Leave out any part except Goal when the text says nothing for it. Never invent requirements, file names, steps or checks, and keep anything unclear as it was said rather than guessing. Use - bullets and no headings or bold. Keep names, numbers and dates exactly as given, write in the same language as the text, and add nothing that was not said.
