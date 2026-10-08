# teach-anything

A personal tutor that runs inside Claude Code (VS Code extension or CLI). It can teach any topic to any learner to the same standard: it starts from unconditional truths, builds by motivated discovery, uses diagnostic multiple-choice questions where every wrong option maps to a known misconception, schedules spaced repetition, assigns hands-on tasks with tests, and records everything in files so each session resumes exactly where the last one stopped.

It knows nothing about the learner up front beyond what they or a mentor tell it. It gets to know them from their answers: which wrong option they choose, how calibrated their confidence is, what kind of explanation lands, and how fast they move. That evidence shapes the teaching.

The learner-facing guide is [BASLA.md](BASLA.md) (Turkish).

## How it is built

| Part | Where | Role |
|---|---|---|
| Entry point | `CLAUDE.md` | session protocol, skill routing, hard rules, beginner communication |
| Skills | `.claude/skills/` | `onboarding`, `new-track`, `teach` (+ `questions.md`, `engagement.md`), `review`, `task`, `cheatsheet`, `wrap-up`, `setup` |
| Track standard | `.claude/skills/new-track/standard.md` | the quality checklist every track must pass |
| Researcher | `.claude/agents/researcher.md` | verifies facts and APIs before they are taught |
| Engine | `tools/learn` (stdlib Python) | spaced repetition (SM-2 variant, confidence-aware), deterministic grading, option shuffling, attempt log, mastery levels, validation |
| Hooks | `.claude/settings.json` | SessionStart injects `learn status`; PreToolUse stops Claude from editing the learner's solutions and `workspace/` |
| Learner state | `learner/`, `tracks/<track>/` | profile, map, misconceptions, cards, attempts, tasks, cheatsheet, glossary, handoff |

The split is deliberate. The LLM does what LLMs are good at: explaining, adapting, and writing questions and tasks. Code does what has to be exact: dates, intervals, grading, where the correct option sits, and whether a track meets the standard.

## Setting it up for someone

1. Copy or clone this repo for the learner. Each learner gets their own copy.
2. Optionally fill `learner/intake.md` with who they are and what they want (see the example). Onboarding will confirm it instead of interrogating them.
3. Open the folder in VS Code with the Claude Code extension installed and say "Merhaba". The `setup` skill installs Python (via uv) when the first coding task needs it.

Learner data (`learner/`, `tracks/`, `workspace/`, `projects/`) is git-ignored so the template stays clean. In a learner's private copy, remove those lines from `.gitignore` to version their progress.

`.vscode/settings.json` hides engine files (`tools/`, `.claude/`, `*.jsonl`) from the Explorer to keep a beginner's view clean and to keep answers out of sight. Remove `files.exclude` entries if you're maintaining the system.

## Engine cheat sheet

```bash
tools/learn status                       # what the session-start hook prints
tools/learn new-track python-basics --title "Python Temelleri"
tools/learn add-card --track python-basics < card.json
tools/learn due [--track t] [--limit 6] [--ahead 1]
tools/learn record --card pb-001 --choice B --confidence 3
tools/learn task --track t --task 01-x --node n --status passed --hints 1
tools/learn progress [--track t]         # new → checked → retained → owned per node
tools/learn signals                      # how this learner learns: calibration, question types, trend, hints
tools/learn journey                      # then-vs-now evidence for recaps
tools/learn moment --kind recap          # log an engagement moment (pacing: recap/teaser/value/milestone)
tools/learn validate [--track t]         # checks the mechanical parts of the standard
tools/doctor                             # learner's environment
```
