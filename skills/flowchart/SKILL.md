---
name: flowchart
description: >-
  Steps and decisions as a flowchart. Turns a process or a choice someone talked through into a diagram; use after explaining how something works or what to do when.
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: scribekey
  scribekey-discovery-categories: productivity
  scribekey-actions: make
  scribekey-output-format: text/vnd.mermaid
  scribekey-presentation: diagram
  scribekey-requires: render.mermaid
  scribekey-icon: auto_awesome
---

Draw the process or decision in the text as a Mermaid flowchart someone can follow on a phone screen.

1. The first line is `flowchart TD`. The output is Mermaid source and nothing else: no code fence, no line before or after it.
2. One node per step, in the order the speaker gave them. Give each node a short id (`n1`, `n2`…) and its words in double quotes: `n1["Check the order number"]`. Keep each label to a few words, in the speaker's terms.
3. A question or choice is a diamond, `n3{"Is it under warranty?"}`, with one labelled arrow per answer: `n3 -->|"Yes"| n4`. Plain steps join with `-->`.
4. Where paths meet again, point them at the same node rather than repeating it.
5. Inside a label, write a double quote as `#quot;`. Leave out styling, colours, themes, links, click actions, images, comments and `%%` lines; ScribeKey draws the diagram.

A long session keeps the main path: at most 25 nodes, merging small steps into the one they belong to and leaving out asides. When the text describes a single step, the chart is that one node. When it describes no process at all, the chart is one node naming its topic.

Example of the shape only; its steps are not in the text:
flowchart TD
    n1["Customer reports a fault"] --> n2{"Under warranty?"}
    n2 -->|"Yes"| n3["Book a repair"]
    n2 -->|"No"| n4["Send a quote"]
    n4 --> n3
    n3 --> n5["Close the ticket"]

Check: the source starts with `flowchart TD`, every label is in double quotes, every step and decision the speaker gave appears once, there are no more than 25 nodes, and nothing appears that the speaker did not say.

Every name, number, date and fact comes from the text exactly as given, in the language of the text.
