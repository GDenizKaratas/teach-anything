---
name: new-track
description: Design a new learning track (any topic) to the repo's quality standard. Covers goal interview, prerequisite check, research, unconditional truths, dependency map, misconception inventory, task ladder, validation, and the learner's go-ahead. Use when the learner wants to learn something new ("X öğrenmek istiyorum", "yeni konu") or when a planned next track (e.g. after python-basics) is about to start.
---

# New track

A track is one coherent learning path toward one concrete capability. Every track, whatever the topic, is built to the same standard (`standard.md` in this folder), and `tools/learn validate` checks the mechanical parts.

## 0. Create the folder first

```bash
tools/learn new-track <kebab-name> --title "<Human title>"
```

## 1. Goal (confirm, don't re-interview)

If `learner/profile.md` or `intake.md` already state the goal, confirm and sharpen it in one question. Otherwise ask (AskUserQuestion, no grading):

- What do they want to be able to **do**? Push until it's concrete and observable. "Lineer cebir öğrenmek" is not a goal. "Bir matrisin neden ve ne zaman tersinir olduğunu açıklayıp hesaplayabilmek" is. "Bir kütüphaneyi öğrenmek" is not a goal. "O kütüphaneyle kendi verimi açıp tek bir analizi baştan sona yapabilmek" is.
- Why? What real situation will they use it in? This decides the scope and keeps the motivation visible.
- Time budget and deadline, if any.

Write the answers into the track's `README.md` (goal in their words + a concrete success criterion).

## 2. Prerequisites and order

- What does this goal depend on? Compare against existing tracks (`tools/learn progress`).
- If a prerequisite is missing, propose doing it first as its own track, or as a short opening section, and **scope the prerequisite to the goal**. Example: Python as a prerequisite for a data-analysis library needs variables, types, lists, dicts, loops, functions, imports, files/paths, arrays and reading errors. It doesn't need classes, decorators or web frameworks.
- **Scope by how the skill will really be used.** Ask yourself what the learner will do with their own judgment in the real setting, and what tools (including AI assistants) will produce for them. Teach the first deeply: reading, understanding, running, verifying, debugging, interpreting results, and knowing when output is wrong. Teach the second only as far as they need to check it. Rote production of things a tool reliably produces is low value. Understanding what the tool produced is high value.
- **Touch the goal early.** Long prerequisite chains kill motivation. Order tracks so the learner reaches a first real step toward the goal as soon as the foundations allow. Before that, show now and then where the current node will be used in the goal (`teach/engagement.md`).
- Big goals split into a chain of tracks of roughly 8–15 nodes each.

## 3. Research (researcher subagent, always)

Launch the `researcher` agent **in the background** with a precise brief, and keep talking with the learner meanwhile:

- the field's real first principles and standard teaching order;
- **common beginner misconceptions** (education research, official tutorials' FAQ, forums);
- for libraries: the **current stable API and version** from the official docs (the `stable` docs, not a blog), plus what changed recently, deprecated functions to avoid, and the datasets available for practice;
- canonical beginner pitfalls and error messages.

Don't plan from memory. Cite sources in `README.md` under "Sources".

## 4. Build the track, incrementally

Build the **outline** now and the **details** just in time. The learner shouldn't wait 20 minutes on day 1.

- **`map.md`, now:** all nodes as a mermaid DAG plus a node table (one-line statement, dependencies, how mastery will be evidenced). Unconditional truths are the roots and the goal is the sink. Stress-test every root: is it truly unconditional for this learner?
- **Details for the first 2–3 nodes only:** their misconceptions in `misconceptions.md` (belief / why tempting / correction / `seen: anticipated`) and their first task idea. Add the next nodes' details as teaching reaches them, usually at the end of a session for the next one.
- **Task ladder** in `README.md`: a short list of planned tasks per node. Create task folders only when you reach them.
- **Probe:** only if the learner has some experience. Write probe cards one at a time as you ask them. Unasked cards are never scheduled, and a complete beginner gets no probe.

Run `tools/learn validate --track <name>` until there are no errors. Treat warnings as defects to fix.

## 5. Check against `standard.md`, then present

Go through the checklist in `standard.md` honestly. Then present the plan to the learner in their language: what we'll learn, in what order, why that order, and what they'll be able to do at the end. Keep it simple for a beginner. **Wait for their go-ahead**, then hand over to `teach`.

Write `handoff.md` → "Next step".
