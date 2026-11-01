---
name: timeline
description: >-
  Events in order, as a timeline. Turns a story, a history or a plan with dates into a diagram of what happened when; use after recounting how something unfolded.
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

Draw the events in the text as a Mermaid timeline someone can read on a phone screen.

1. The first line is `timeline`. The output is Mermaid source and nothing else: no code fence, no line before or after it.
2. The second line is `    title ` and up to six words naming what the timeline covers.
3. One line per point in time, in order, indented four spaces: the time as the speaker said it, ` : `, then what happened. Two things at the same time share a line, each after its own ` : `: `    March : Signed the lease : Ordered the furniture`.
4. When the speaker gave no times, use their own markers ("First", "Then", "After the move") or numbered steps, in the order they told it.
5. A colon separates events, so write a colon inside a time or event as a dash, `9-30`, or reword around it. Leave out styling, themes, links, images, comments and `%%` lines; ScribeKey draws the diagram.

A long session keeps the turning points: at most 25 events, merging small events into the one they belong to. Group a long span with `    section ` lines, such as one per year, only when the speaker's times fall into clear periods. When the text holds a single event, the timeline is that one line.

Example of the shape only; its events are not in the text:
timeline
    title Moving to Leeds
    January : Got the job offer
    March : Signed the lease : Booked the van
    April : Moved in
    May : Started work

Check: the source starts with `timeline`, every event the speaker gave appears once and in order, no time or event contains a colon of its own, there are no more than 25 events, and nothing appears that the speaker did not say.

Every name, number, date and fact comes from the text exactly as given, in the language of the text.
