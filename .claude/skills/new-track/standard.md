# Track quality standard

Every track must meet this standard, whatever the topic. Items marked ⚙ are checked by `tools/learn validate`. The rest are your honest self-review before presenting the plan.

## Goal
- [ ] The goal is an observable capability ("can do X"), in the learner's words, plus a concrete success criterion.
- [ ] The track serves the learner's stated goal, and the motivation for each section points back to it.
- [ ] Examples are clear and topic-native. Analogies to prior knowledge are used only where structurally accurate, with their break point stated.
- [ ] The scope is cut to the goal. Every node is needed for the goal or for a node that is.

## Foundations
- [ ] The roots are unconditional truths **for this learner**: accepted at face value, no caveats.
- [ ] No root is a disguised theorem that derives from something simpler.
- [ ] Facts that need a caveat ("usually…") are derived nodes, not roots.
- [ ] Every derived node has a motivation: why we need it, and how someone could have discovered it.

## Map ⚙
- [ ] ⚙ `map.md` has a mermaid DAG and a node table.
- [ ] 8–15 nodes. Bigger goals are split into a chain of tracks.
- [ ] Each node names how its mastery will be evidenced (a question type and/or a task).

## Accuracy
- [ ] The field and the APIs were researched with the `researcher` agent, not from memory.
- [ ] For libraries, the version and the API match the current official docs. Sources are listed in `README.md`.

## Misconceptions ⚙
- [ ] ⚙ `misconceptions.md` defines `m-…` ids.
- [ ] Every risky node has ≥ 2 anticipated misconceptions, each with belief / why tempting / correction.

## Questions ⚙
- [ ] ⚙ Every option card has 2–4 options, exactly one correct, and a misconception id on every distractor.
- [ ] ⚙ No length tells, no justification inside options, no asymmetric bold.
- [ ] Each node gets several card types over time (MCQ → predict/spot-the-bug → recall/explain).

## Practice ⚙
- [ ] A PRIMM task ladder is planned per code node (predict → investigate → modify → make).
- [ ] ⚙ Every task folder has `TASK.md` plus `test_*.py` (code) or `CHECK.md` (non-code).
- [ ] The tests were verified against a correct solution in scratch before handing the task over.

## Learner fit
- [ ] Session-sized steps fit the time budget in `profile.md`.
- [ ] A beginner gets worked examples first and fading support.
- [ ] The plan was presented in plain language and the learner gave the go-ahead.
