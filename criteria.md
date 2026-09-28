# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->

---

## 4. Chunks follow section boundaries

Every chunk begins at a `##` section heading and contains that section's text
and nothing from any other section. No chunk is shorter than 200 characters.

**Why this target:**

Nine of the fourteen guides in `city_guides` use the same seven headings —
Getting there, Getting around, Eat and drink, What to see, Where to stay, When
to go, Practical notes — and each section is one self-contained topic of
roughly 150 to 350 characters. The answer to a question about a town's shops is
the whole of that town's "Eat and drink" section and none of its neighbours.

The starter's 800-character splitter ignores all of that. It cuts mid-sentence
and mid-section, and it leaves tails of 24 characters on `guide_eating.md` and
41 on `guide_elder_ness.md` — half a sentence with nothing around it, which can
still be retrieved and can never answer anything. That's where the 200
character floor comes from: it is below every real section in this corpus and
above every fragment the blind splitter produces.

This one is all-or-nothing rather than "4 of 5" because it is a mechanical
property of my chunker, not a judgement about an answer. I can check it over
every chunk, so there's no reason to accept exceptions. It predicts a count too:
around 100 chunks instead of the 51 I have now, which also makes `TOP_K` of 5 a
more selective slice than the tenth of the corpus it is today.

I picked this over "4 of 5 sampled chunks read as a complete thought" because I
couldn't trust myself to score that the same way twice. Starting at a heading is
something I can count.

---

## 5. Answers name the document the answer actually came from

For at least 4 of my 5 test questions, the answer names the document that
actually contains the answer — not merely some document.

**Why this target:**

Criterion 2 only asks that an answer names *a* source, and this corpus makes
that trivially passable while being wrong. Nine of the guides carry a
byte-identical "Practical notes" paragraph, including the sentence "The nearest
full hospital is in Brightwater" — `guide_marchwood.md` says it about itself,
while `guide_accessibility.md` says the nearest full hospital is in Marchwood.
So an answer can cite a real filename, read fluently, and still be about the
wrong town. Naming a source and naming the right source are different
properties and only the second one is worth anything to someone reading the
answer.

I expect this to be the hardest of my five, because those nine near-identical
paragraphs are exactly what embedding-based retrieval clusters on. 4 of 5 rather
than 5 of 5 is my allowance for the hospital question specifically — I have one
document giving the regional answer against nine repeating the local one, and I
would rather write down now that I expect it to fail than discover it later.

It costs nothing to measure: `run_eval.py` already writes a "Sources retrieved"
line for every question on every run, three runs per question.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
