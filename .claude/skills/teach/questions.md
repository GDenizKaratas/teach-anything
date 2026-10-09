# Question protocol

Used by `teach`, `review`, `task` and `new-track`. A question with a right answer is a measurement, so every graded question is stored, graded by the script and scheduled for spaced review.

## Why questions matter this much

- **Retrieval practice and spacing** are the two best-established learning effects. A question asked once and never again wastes most of its value, which is why every graded question becomes a card.
- **Which wrong option they chose is diagnostic.** Each distractor encodes one specific misconception, so a wrong choice tells you *what* they believe, not just that they're wrong.
- **Wrong options can teach the wrong thing** if no feedback follows. Always give feedback right after the answer.
- **Confidence matters.** A high-confidence error is a "hypercorrection" moment: corrected well, it sticks better than anything else. A correct guess is not evidence of knowledge.

## Card types

| type | use for | graded by |
|---|---|---|
| `mcq` | diagnosis, distinguishing near-neighbors | script |
| `predict-output` | "what does this code print?" (options are possible outputs) | script |
| `spot-the-bug` | "which line is wrong?" / "why does this fail?" | script |
| `recall` | "what is X?" in their own words (generation beats recognition) | you, against `answer` |
| `explain` | "why does…?", connect two nodes | you, against `answer` |

Mix them. Multiple-choice is efficient for locating edges. Open recall/explain locks things in harder. Once a node is checked, prefer open types in later reviews.

## Building multiple-choice options (construction procedure)

Don't audit options after the fact. **Build them so that the correct one can't stand out:**

1. **Every option is a bare claim, with no justification anywhere.** The number-one giveaway is the correct option carrying its own reasoning ("…, because…") while the distractors are bare. All reasoning goes in `explanation`, which the learner sees only after answering.
2. **Write the correct claim first, then mutate it into each distractor.** Take one specific misconception or easily confused neighbor and state what someone holding it would claim, in the *same* skeleton, length, and register. Parallelism then comes for free.
3. **Each distractor is a real error this learner might make**, so which one they pick is diagnostic. Make it tempting, not tricky. It must be unambiguously wrong on the intended reading.
4. **Each distractor carries a `misconception` id** (`m-…`) defined in the track's `misconceptions.md`. If the id doesn't exist, add it there first: belief / why tempting / correction / `seen: anticipated`.
5. **No asymmetric bolding or formatting.**
6. **2–4 options.** The UI adds its own "Other" field, which the learner can use to type "bilmiyorum" or their own answer.

If you can tell which option is right by reading the set cold without knowing the material, regenerate it. Don't patch.

## The flow (always these steps)

**1. Store the card first:**

```bash
tools/learn add-card --track <track> <<'EOF'
{"node": "<map node id>", "type": "mcq",
 "prompt": "…", "code": "optional code shown with the question",
 "options": [
   {"text": "…", "correct": true},
   {"text": "…", "misconception": "m-…"},
   {"text": "…", "misconception": "m-…"}
 ],
 "explanation": "why the right one is right, and why each tempting one is wrong, in terms of the foundations"}
EOF
```

For `recall`/`explain`: no `options`, but include `"answer": "reference answer"`.

For `predict-output` and every code-behavior claim, **run the code first** (`uv run python -c "…"`) and take the correct option from the real output. Never use memory for this.

The script validates the card, **shuffles the options** (you never choose where the correct one sits), assigns an id, and returns the public view with letters A–D. If it rejects the card, fix the card and retry. Treat warnings as tells, and regenerate.

**2. Ask with AskUserQuestion**, in the returned order:

- Question 1 is the question itself. Use the option labels `"A) <text>"` exactly as returned. If an option has code or is long, put the full question, code and options in your chat message first and use the labels `"A"`, `"B"`, … For "which code is correct" questions, use the `preview` field to show each option's code.
- Question 2 is confidence, in the same call (in `teach` checks; optional in quick `review` warm-ups, where `--confidence` defaults to 2): "Ne kadar eminsin?" with the options `Tahmin ettim` / `Emin değilim` / `Eminim`, which map to `--confidence 1/2/3`.
- **Never** add "(Recommended)" to any option, and never hint.
- For `recall`/`explain`, ask in plain chat ("Kendi cümlelerinle: …") and let them type.

**3. Grade through the script:**

```bash
tools/learn record --card <id> --choice <A-D|X> --confidence <1-3>
# open answers: --correct yes|partial|no --answer-text "<their words>" [--misconception m-…]
```

If they picked "Other" and typed "bilmiyorum", use `--choice X`. If they typed an answer, judge whether it matches an option or reasoning, and say what you decided.

**4. Feedback, immediately and briefly:**

- Correct: ✓, then one sentence connecting it to the foundation it rests on. If the `flag` says they guessed, say a guess counts as not-yet-known, and plan a different question on this node soon.
- Wrong: ✗, the correct answer, then **name the belief behind their choice** (from the misconception) and why it's tempting. Show which foundation it contradicts. If the flag is a high-confidence error, ask them first *why* they were sure, and dislodge that model before moving on.
- Then return to the node with a **different** question later in the session. Never repeat the same card in the same session.

**5. Update `misconceptions.md`.** Switch `seen: anticipated` to `observed` when a learner actually holds it. Add new ones you diagnosed from open answers.
