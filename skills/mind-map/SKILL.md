---
name: mind-map
description: >-
  Ideas and how they branch, as a mind map. Turns a brainstorm or a ramble into a diagram of the main idea and what grows from it; use after thinking out loud.
license: Apache-2.0
metadata:
  version: "1.0.1"
  author: scribekey
  scribekey-discovery-categories: productivity
  scribekey-actions: make
  scribekey-output-format: text/vnd.mermaid
  scribekey-presentation: diagram
  scribekey-requires: render.mermaid
  scribekey-icon: hub
---

Draw the ideas in the text as a Mermaid mind map someone can take in at a glance on a phone screen.

1. The first line is `mindmap`. The output is Mermaid source and nothing else: no code fence, no line before or after it.
2. The second line is the central idea, indented two spaces, in a circle with its words in double quotes: `  root(("Garden plans"))`.
3. Each main idea is a branch under it, indented two more spaces; each detail sits under its idea, two spaces deeper again. Go at most three levels below the centre.
4. Every node's words go in double quotes inside square brackets, `["Raised beds"]`, as a few words in the speaker's terms. Inside a label, write a double quote as `#quot;`.
5. Indent with spaces only. Leave out icons, classes, styling, themes, links, images, comments and `%%` lines; ScribeKey draws the diagram.

A long session keeps the ideas that branch: at most 25 nodes, folding a passing remark into the idea it belongs to. When the text holds one idea, the map is that idea alone at the centre.

Example of the shape only; its ideas are not in the text:
mindmap
  root(("Garden plans"))
    ["Vegetables"]
      ["Tomatoes"]
      ["Beans"]
    ["Raised beds"]
      ["Two by the fence"]
    ["Budget"]

Check: the source starts with `mindmap`, there is exactly one centre, every label is in double quotes, every idea the speaker raised appears once under the idea it belongs to, there are no more than 25 nodes, and nothing appears that the speaker did not say.

Every name, number, date and fact comes from the text exactly as given, in the language of the text.
