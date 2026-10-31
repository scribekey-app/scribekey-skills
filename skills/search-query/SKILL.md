---
name: search-query
description: A concise search query from a spoken request. Use when dictation is meant for an ordinary web or search field, not a question for the assistant to answer.
license: Apache-2.0
metadata:
  version: "1.0.0"
  scribekey-title: Search query
  scribekey-actions: rewrite
  scribekey-icon: auto_awesome
  scribekey-discovery-categories: search
  scribekey-suggested-fields: search
---
Rewrite the spoken request as one concise search query. Keep the topic, useful constraints, names, brands, model numbers, dates and exact phrases that help find relevant results. Remove conversational setup and repeated wording, but keep the speaker's language. Do not answer the request or add search terms, claims or facts that were not said. If the request is already a clear query, keep it with only light cleanup.

Check: output one plain-text query, with the speaker's key terms intact and no added facts. Every name, number, date and fact comes from the text exactly as given, in the language of the text.
