---
name: search-query
description: >-
  One concise search query. Turns a spoken request into the words to search for; use in a web or app search field, when the request is something to look up rather than a question for an assistant.
license: Apache-2.0
metadata:
  version: "1.1.0"
  author: scribekey
  scribekey-title: Search query
  scribekey-discovery-categories: search
  scribekey-suggested-fields: search
  scribekey-actions: rewrite
  scribekey-presentation: text
  scribekey-icon: search
---

Write the spoken request as one search query the speaker can submit as is. You are writing the search down, not answering it.

1. Keep the topic and every term that narrows the results: names, brands, model numbers, dates, places, prices and exact phrases.
2. Cut the conversational setup ("I'm trying to find", "can you look up") and anything said twice, even though plain clean-up keeps them.
3. Use only the speaker's terms, in the speaker's language. A request that is already a clear query stays as it is.

Example. "um can you look up when the last ferry to Rottnest leaves on a Sunday" becomes:
last ferry to Rottnest Sunday

Check: the output is one line, every narrowing term the speaker gave is in it, and every word in it came from the speaker.

Write plain text. Every name, number, date and fact comes from the text exactly as given, in the language of the text.
