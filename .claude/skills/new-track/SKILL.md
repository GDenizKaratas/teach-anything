---
name: new-track
description: Design a new learning track (any topic) to the repo's quality standard. Covers goal interview, prerequisite check, research, unconditional truths, dependency map, misconception inventory, task ladder, validation, and the learner's go-ahead. Use when the learner wants to learn something new ("X öğrenmek istiyorum", "yeni konu") or when a planned next track (e.g. after python-basics) is about to start.
---

# New track

A track is one coherent learning path toward one concrete capability. Every track, whatever the topic, is built to the same standard (`standard.md` in this folder), and `tools/learn validate` checks the mechanical parts.

## 1. Goal interview (AskUserQuestion, no grading)

- What do they want to be able to **do**? Push until it's concrete and observable. "Lineer cebir öğrenmek" is not a goal. "Bir matrisin neden ve ne zaman tersinir olduğunu açıklayıp hesaplayabilmek" is. "Bir kütüphaneyi öğrenmek" is not a goal. "O kütüphaneyle kendi verimi açıp tek bir analizi baştan sona yapabilmek" is.
- Why? What real situation will they use it in? This decides the scope and keeps the motivation visible.
- Time budget and deadline, if any.

Write the answers into the track's `README.md` (goal in their words + a concrete success criterion).

## 2. Prerequisites and order

- What does this goal depend on? Compare against existing tracks (`tools/learn progress`).
- If a prerequisite is missing, propose doing it first as its own track, or as a short opening section, and **scope the prerequisite to the goal**. Example: Python as a prerequisite for a data-analysis library needs variables, types, lists, dicts, loops, functions, imports, files/paths, arrays and reading errors. It doesn't need classes, decorators or web frameworks.
- Big goals split into a chain of tracks of roughly 8–15 nodes each.

## 3. Research (researcher subagent, always)

Launch the `researcher` agent with a precise brief:

- the field's real first principles and standard teaching order;
- **common beginner misconceptions** (education research, official tutorials' FAQ, forums);
- for libraries: the **current stable API and version** from the official docs (the `stable` docs, not a blog), plus what changed recently, deprecated functions to avoid, and the datasets available for practice;
- canonical beginner pitfalls and error messages.

Don't plan from memory. Cite sources in `README.md` under "Sources".

## 4. Build the track

```bash
tools/learn new-track <kebab-name> --title "<Human title>"
```

Then fill in:

- **`map.md`**: unconditional truths as roots, derived nodes, and the goal as the sink. Each node gets a one-line statement, its dependencies, and *how mastery will be evidenced* (which question type, which task). Stress-test every root: is it truly unconditional for this learner?
- **`misconceptions.md`**: at least 2 anticipated misconceptions for every node with a real risk, from the research and your knowledge of the learner. Each has belief / why tempting / correction / `seen: anticipated`.
- **Task ladder** in `README.md`: a list of planned tasks (PRIMM order) per node. Create the actual task folders only when you reach them.
- **First probe cards**: write 4–8 diagnostic cards with `add-card` for phase 1a, so the probe is stored too.

Run `tools/learn validate --track <name>` until there are no errors. Treat warnings as defects to fix.

## 5. Check against `standard.md`, then present

Go through the checklist in `standard.md` honestly. Then present the plan to the learner in their language: what we'll learn, in what order, why that order, and what they'll be able to do at the end. Keep it simple for a beginner. **Wait for their go-ahead**, then hand over to `teach`.

Write `handoff.md` → "Next step".
