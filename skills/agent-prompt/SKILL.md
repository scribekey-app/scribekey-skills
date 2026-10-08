---
name: agent-prompt
description: >-
  Goal, context, constraints, done when. Turns a spoken request into instructions for a coding or chat agent; use in an AI assistant app.
license: MIT
metadata:
  version: "1.1.1"
  author: scribekey
  scribekey-title: Prompt for an agent
  scribekey-apps: >-
    com.openai.chatgpt
    com.anthropic.claude
    com.google.android.apps.bard
    ai.perplexity.app.android
---

Turn the spoken request into a prompt an AI agent can carry out without coming back with questions. Write to the agent as "you", in whole sentences.

Always start with "Goal:", even for a one-line request. Then add the other parts in this order, only when the text gives content for them. Start each part on a new line with its label and a colon.

Goal: one sentence naming the outcome, starting with a verb.
Context: - bullets with the background, files, names, links and facts the speaker gave.
Steps: numbered steps, only when the speaker gave an order to follow.
Constraints: - bullets, each phrased as what to keep or use ("use only the existing dependencies", "keep the public API as it is").
Done when: - bullets with conditions the agent can check ("the tests pass", "the page loads in under a second").

Carry anything uncertain across as the speaker said it, marked as their guess ("I think it's in utils").

Check: the agent could start now, and every requirement in the prompt came from the text.

Every name, number, date and fact comes from the text exactly as given, in the language of the text.
