---
name: review
description: Spaced-repetition review of cards that are due. Use at the start of a session when `tools/learn status` shows cards due, when the learner says "tekrar", "tekrar yapalım", "soru sor", "hatırlatma", or as interleaved retrieval in the middle of a lesson.
---

# Review

The goal is retrieval spread over time, the most reliable way to make learning last. Keep it brisk: a warm-up is 3–6 cards, about 5 minutes. Don't turn it into a lesson.

## Flow

1. `tools/learn due --limit 6`. The script orders cards by overdue-ness and interleaves nodes and tracks. Keep its order.
2. Say one line to frame it ("Önce 5 dakikalık bir ısınma: geçen günlerden 4 soru."). Nothing more.
3. Ask each card with the question protocol (`.claude/skills/teach/questions.md`, steps 2–4). The card is already stored, so skip `add-card` and go straight to asking and `record`.
4. After the batch, give one sentence: what held and what slipped. No scores and no grades.

## When a card goes wrong

- **Cheatsheet first.** If the node is already in `cheatsheet.md`, send them there ([section](…)), then let them try a variant. Log it with `tools/learn moment --kind cheatsheet`. This builds the habit of using their own reference.

- **Re-teach small, from the foundation.** Restate the unconditional truth the node rests on and re-derive the step, in 3–5 sentences. If the node needs more than that, note it in `handoff.md` under "Next step" and let `teach` handle it properly. Don't hijack the warm-up.
- **Add a fresh variant card** for the same node with `add-card`: different surface, same idea. If a misconception was recorded, target it. Ask the variant later in the session, not right now.
- If the same node has failed twice across sessions (`tools/learn progress` shows `struggling` or rising lapses), the foundation under it is probably wrong. Flag it in `handoff.md`, and next time probe the node it depends on.

## Avoiding "memorized the question"

After a card has been answered correctly 2–3 times, the learner may be recognizing the wording rather than knowing the idea. Instead of asking it again:

- write a **transfer card**: same node, new context or format (MCQ → predict-output → explain, or another context);
- `tools/learn retire --card <old> --reason "replaced by transfer card <new>"`.

Prefer open `recall`/`explain` types for nodes that are already checked.

## Mid-lesson use

`teach` asks for one old question every 2–3 new nodes. Pick a due or soon-due card from an *earlier* node (`tools/learn due --limit 3`). If nothing is due, write a fresh question on an earlier node.
