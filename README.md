# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

## Chunking Strategy

**Chunk size:** One `##` section per chunk, with no fixed character count. On
this corpus that gives 94 chunks of 182 to 757 characters, 318 on average.

**Overlap:** None.

Every guide is divided into labelled sections, and each section covers one
topic, like a town's "Getting there" or "Where to stay". So I cut at the
headings. The starter's 800-character windows ignored them: they cut through
the middle of sections and left scraps as short as 24 characters.

Each chunk starts with the guide's title and the section name, for example
`Brightwater: Getting there`. Most town sections never say which town they are
about, and nine "Practical notes" sections are word-for-word the same. Without
the header, those chunks can't be told apart.

There is no overlap because a section is already a whole topic. Overlap would
only pull in the end of the section before it, which is about something else.

The paragraph before a guide's first heading has no heading of its own, so it
becomes an "Overview" chunk. That keeps facts like Halden Bay being "a working
fishing port of 8,000".

**Where this doesn't meet criterion 4.** Criterion 4 says every chunk starts at
a `##` heading and none is under 200 characters.

- The 10 Overview chunks don't start at a `##` heading, because the intro
  doesn't have one.
- 3 chunks are under 200 characters: Givens Mill and Thornby Wells "Where to
  stay" (187 and 188) and the accessibility guide's Overview (182). The two
  "Where to stay" sections are complete, just short. I set the floor thinking
  every real section was longer than 200, and that was wrong.

I've left criterion 4 as I wrote it and will come back to it in unit 2.

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

Printed with `python app.py chunks --indices 1,4,29,6,90`. Each one holds the
answer to one of my five test questions.

**Chunk 1** — source: `guide_accessibility.md#1` — produced by: `chunker.py::split_documents`

Answers: *What is the easiest town in the region?*

```
Getting around the region with limited mobility: Straightforward

**Thornby Wells** is the easiest town in the region. It is flat, compact, and
everything is within three minutes of everything else. Parking is free for two
hours anywhere in town and the station is central. The pump room and gardens
are level throughout.

**Marchwood** has a modern tram network with level boarding on all four lines,
running every 8 minutes on weekdays. The city museum and covered market are both
step-free. The distances between districts are the main consideration.

**Brightwater** is level along the river and through the centre. The mill museum
is step-free. The station is a 15-minute walk from campus on flat ground, or the
shuttle meets the four busiest arrivals.
```

**Chunk 2** — source: `guide_accessibility.md#4` — produced by: `chunker.py::split_documents`

Answers: *Where is the nearest full hospital?*

```
Getting around the region with limited mobility: Practical

The nearest full hospital is in Marchwood. Brightwater has a hospital;
Kestrelford, Halden Bay, Corry Vale, Givens Mill and Elder Ness have minor
injuries units with limited hours or nothing at all.

Mobile coverage is good in the town centres and patchy on the outskirts, and
genuinely absent in parts of Corry Vale.
```

**Chunk 3** — source: `guide_elder_ness.md#3` — produced by: `chunker.py::split_documents`

Answers: *How many shops does Elder Ness have?*

```
Elder Ness: Eat and drink

One pub, serving food 12 to 2 and 6 to 8, closed Mondays. A shop that sells basics and closes at 5pm and all day Sunday. That is the complete list. Visitors staying more than a night bring food with them.
```

**Chunk 4** — source: `guide_brightwater.md#1` — produced by: `chunker.py::split_documents`

Answers: *How many services does the railway have on Sundays?*

```
Brightwater: Getting there

The train runs to the regional hub eleven times a day on weekdays and six times on Sundays, taking 50 minutes. The station is a 15-minute walk from campus, or the shuttle meets the four busiest arrivals. Long-distance coaches stop on Verrill Street rather than at the station, which catches people out. There is no airport; the nearest is 90 minutes by road.
```

**Chunk 5** — source: `guide_walking.md#0` — produced by: `chunker.py::split_documents`

Answers: *What is the most walked route in the region?*

```
Walking in the region: Easy, on good surfaces

The **Brightwater river path** runs four miles upstream from the town to a weir,
on a made surface, flat throughout. It is the most-walked route in the region
and deservedly so. Continuing downstream from Givens Mill reaches Brightwater in
about three hours.

The **Kestrelford trackbed** follows the railway line closed in 1963 for six
miles to the next village. Easy gradient, good surface, and the best walking in
the region for the effort involved.

**Thornby Wells** has flat, formal gardens and level streets — the region's
most accessible town on foot.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** Where is the nearest full hospital?

**Answer:**

```
  (best distance 0.334, cutoff 0.67)

According to `guide_accessibility.md`, the nearest full hospital is in Marchwood. However, `guide_givens_mill.md`, `guide_halden_bay.md`, `guide_kestrelford.md`, and `guide_marchwood.md` state that the nearest full hospital is in Brightwater.

Sources retrieved: guide_accessibility.md, guide_givens_mill.md, guide_halden_bay.md, guide_kestrelford.md, guide_marchwood.md
```

The documents disagree here: one guide says Marchwood and four town guides say
Brightwater. The answer reports both and names each file instead of picking
one.

**My relevance cutoff:** 0.67

My five test questions all scored between 0.334 and 0.536. The five
out-of-scope questions scored between 0.810 and 0.967. That leaves a gap from
0.536 to 0.810, and I put the cutoff in the middle of it, so there is about
0.13 of room on each side. The starter's 0.6 was also in the gap, but only
0.064 above my weakest question, so a slightly reworded version of it could
have been refused.

The closest out-of-scope question was the capital of Mongolia, as I predicted
in criterion 3: it is a geography question put to a geography corpus.

I kept top-k at 5. That brings back a chunk with the answer for 4 of my 5
questions. The railway answer is at rank 9, and I've left that miss for unit 2.

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---|
| What is the easiest town in the region? | Yes | 0.536 |
| Where is the nearest full hospital? | Yes | 0.334 |
| How many shops does Elder Ness have? | Yes | 0.343 |
| How many services does the railway have on Sundays? | Yes | 0.468 |
| What is the most walked route in the region? | Yes | 0.452 |
| What is the capital of Mongolia? | No | 0.810 |
| How do I change the oil in a diesel engine? | No | 0.883 |
| Who won the 1994 World Cup? | No | 0.967 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.834 |
| How do I write a for loop in Rust? | No | 0.847 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**

**2.**

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
