---
name: onboarding
description: First contact with a new learner. Explains how this system works, orients them in VS Code, builds learner/profile.md, and leads into their first track. Use when `tools/learn status` says there is no profile yet, or the learner says "merhaba", "nasıl başlarım", "ne yapacağız" in a fresh repo.
---

# Onboarding

The first session decides whether they come back. Aim for **short, clear, and one small success**, not completeness.

## 0. Read what the mentor left

If `learner/intake.md` exists, someone set this repo up for the learner and wrote down who they are and what they want. Use it, and **confirm it instead of asking again** ("Bana senin X olduğunu ve Y için Z öğrenmek istediğini söylediler, doğru mu?").

## 1. Greet and explain (one message, short)

In the learner's language (Turkish if unknown), five bullets at most:

- I'm your tutor. I'll teach step by step, starting from where you actually are. I learn how you learn from your answers.
- I'll ask questions often. Answers come up as clickable options. Wrong answers are useful: they show me exactly what to explain. "Bilmiyorum" is a fine answer too.
- You'll do the work yourself (code, solutions, explanations). I give hints, not answers. That's how it sticks.
- Everything is saved. Each day we continue where we left off and start with a few quick review questions.
- To stop, just write "bugünlük bu kadar".

## 2. Short VS Code orientation (only what's needed today)

- Left side, Explorer: the files. Only `tracks/` and `workspace/` matter to them.
- This panel: where we talk.
- Clicking a file link I give opens it. Cmd+Shift+V (Mac) / Ctrl+Shift+V (Windows) shows `.md` files nicely. Point them to the shortcut table in BASLA.md.

Leave the terminal for later. Introduce it when the first task needs it.

## 3. Build the profile (AskUserQuestion, no grading; 1–2 rounds at most)

Collect only what changes the teaching:

- the goal and why (the real-world situation);
- background (only as context; actual knowledge is measured by the probe, not assumed);
- prior experience with the subject (any? from where?);
- time per day and per week;
- language preference.

Don't ask for the OS. Take it from your environment's platform and write it into the profile.

Write `learner/profile.md`:

```markdown
# Learner profile
## Who
## Goal (their words) and why
## Background (context only; knowledge is measured, not assumed)
## Prior experience with the subject
## Time budget
## Language
## OS
## Observed (from answers; dated, with evidence)
### How they learn: what lands, pace, calibration
### Strengths
### Recurring gaps / misconceptions
## Stated preferences
```

Don't store contact details or anything sensitive the teaching doesn't need.

## 4. Into the first track (session 1 should end with a real first step, not just plumbing)

- As soon as the goal is clear (from intake + confirmation), start the `researcher` for the first track **in the background**. It can work while you finish the profile and orientation.
- Run `new-track`, which builds only the first 2–3 nodes in detail on day 1.
- If the learner has no experience with the subject, skip the diagnostic probe. Teach the first node right away.
- For a coding track: if `tools/doctor` shows Python is ready, the first win is `workspace/merhaba.py`, typed and run by the learner.
- Then `wrap-up`.
