---
name: wrap-up
description: Close a learning session cleanly so the next one resumes exactly where this one stopped. Use when the learner says "bugünlük bu kadar", "bitir", "yoruldum", "sonra devam", or when the session reaches the learner's time budget.
---

# Wrap-up (about 5 minutes)

1. **Exit question.** Ask one concrete open question about today's most important node ("Kendi cümlelerinle: değişken nedir?"). Record it on that node's recall card, creating one with `add-card` if none exists. Don't store meta-questions like "bugün ne öğrendin?" as cards; they mean nothing when they come back days later.
2. **Update the files.** Do this silently; don't narrate it:
   - `tracks/<t>/handoff.md`:
     - **Next step**: exactly what to do first next time (node, task, or question to revisit). Be specific enough that a fresh session can start without asking anything.
     - **Session log**: *append* one line, newest first (`- 2026-10-09 · 40 dk · nodes: … · task 02 passed · note: …`). Don't overwrite the history; it's how the next session and the mentor see the trajectory.
     - **Open questions**: doubts the learner raised that weren't resolved.
   - If the next session reaches new nodes, prepare their details now (misconceptions, a first task idea). See `new-track` §4.
   - `glossary.md`: terms that came up today.
   - `misconceptions.md`: observed / new.
   - `learner/profile.md` → Observed: run `tools/learn signals`. Add only patterns that hold across sessions (calibration, what kind of explanation landed, pace, strong and weak question types), each with a date and the evidence. Not a diary.
3. **Tell the learner** in 2–3 lines: what they can do now that they couldn't before (concrete), what comes next time, and roughly how many review questions will be waiting (`tools/learn due --ahead 1 --limit 0` → `due_total`). End warmly but without empty praise.
4. **Teaser.** If the session ended on a good note (and the last one didn't already end with a teaser), close with a one-sentence curious hint about the next node (`engagement.md` §3). Log it with `tools/learn moment --kind teaser`.
5. If 3+ new nodes reached `checked` since the last cheatsheet update, offer the `cheatsheet` skill next time (not now; the session is over).
