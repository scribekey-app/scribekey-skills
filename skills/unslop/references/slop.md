# Slop patterns

Each pattern names a tell of generated or padded writing and the plain version that replaces it.
A pattern is a signal: keep a flagged word when it is the precise one for what was meant. Pattern
numbers are stable ids, so a removed pattern leaves a gap rather than renumbering the rest.

Adapted from the unslop skill in Cursor's pstack plugin (https://github.com/cursor/plugins,
pstack/skills/unslop), MIT licence, Copyright (c) 2026 Lauren Tan.

## Words

1. **Inflated words.** Utilise and leverage become use. Facilitate becomes help. Commence becomes
   start. Numerous, a myriad of and a plethora of become many. Endeavour becomes try.
2. **AI vocabulary.** Delve, crucial, pivotal, intricate, interplay, tapestry, landscape, realm,
   testament, underscore, showcase, foster, garner, vibrant, enduring, robust, seamless. Use the
   plain word, or name the actual thing.
3. **Fancy ways to say "is".** Serves as, stands as, acts as, boasts and features become is or has.
4. **Abstract metaphor nouns.** North star, flywheel, paradigm, bedrock, vector, wedge, endgame,
   unlock, empower. Name the concrete thing or action.
5. **Adverbs propping up a weak verb.** "Significantly improves" becomes the amount it improved.
   "Runs really quickly" becomes "is fast", or the number.

## Phrases

6. **Stock openers and closers.** "I hope this message finds you well", "I wanted to reach out",
   "Just circling back", "Feel free to", "Don't hesitate to", "Let me know if you have any
   questions", "Hope this helps". Start with the point and end on the last real sentence.
7. **Chatbot and sycophantic phrases.** "Great question", "Absolutely", "Certainly", "Of course",
   "You're absolutely right". State the point directly.
8. **Filler phrases.** "In order to" becomes to. "Due to the fact that" becomes because. "It's
   worth noting that", "It's important to note that" and "At the end of the day" are cut.
9. **Stacked hedges.** "Could potentially perhaps" becomes may. Keep one hedge where the speaker
   was genuinely unsure.
10. **Vague attributions.** "Experts say", "Studies show", "Many people believe". Name the source
    the speaker gave, or state the claim as the speaker's own.
11. **Superficial -ing tails.** A clause like "highlighting the importance of..." or "ensuring a
    smooth experience" tacked onto a sentence. Cut it, or make it a sentence with a real subject.

## Shapes

12. **"Not just X, but Y."** And "It's not X, it's Y". State Y directly.
13. **Forced threes.** Three adjectives or three examples where the speaker had one or two. Use
    the number the content has.
14. **Synonym cycling.** Calling one thing the project, the initiative and the effort in one
    paragraph. Pick one name and repeat it.
15. **False ranges.** "From startups to global enterprises" where the two ends are not a real
    scale. List what is actually meant.
16. **Generic conclusions.** "The future looks bright", "Overall, it was a great success", a last
    line that restates the paragraph. End on the last specific fact or ask.
17. **Announcing instead of saying.** "I want to talk about...", "Here's the thing:". Say the thing.
18. **Rhetorical questions** the speaker did not ask. Turn each into the statement it implies.

## Punctuation and format

19. **Em dashes.** Use a full stop or a comma. When the thought needs separating, end the sentence.
20. **Colons as connectors.** A colon belongs before a list or an example. Mid-sentence, rewrite
    so the point stands on its own.
21. **Bold, headings and emoji** in a message or a paragraph of prose. Write plain sentences.
22. **Inline-header lists.** "Performance: performance improved..." becomes a plain sentence.
23. **Title Case headings.** Use sentence case.

## Plain speech

24. **Say what it does, not how it feels.** "A seamless experience" names a feeling; "it saves your
    draft every 10 seconds" names the mechanism. A sentence that could appear unchanged in anyone
    else's message says nothing; cut it.
25. **Passive voice that hides the actor.** "The issue was resolved" becomes "Sam fixed the issue"
    when the speaker said who. Keep passive only when the actor is unknown.
26. **Dense sentences.** If the reader has to go back to parse it, split it in two. One idea per
    sentence.
27. **Mannered prose.** Aphorisms, figurative verbs and flourishes ("it rides on", "a dial worth
    turning") become the literal phrase.
28. **Over-compression.** Dropped articles, arrows and abbreviations ("bug fixed → deploy tmrw")
    become whole sentences ("The bug is fixed, so we can deploy tomorrow").
