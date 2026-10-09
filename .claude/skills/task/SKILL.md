---
name: task
description: Hands-on practice. Create a small task the learner does themselves (code with tests, or a non-code exercise with a rubric), give hints without solving it, check their work, and record the result. Use when the learner says "görev ver", "pratik", "alıştırma", "kontrol et", "ipucu", "çalışmıyor", "hata verdi", or when teach reaches a "Do" step.
---

# Tasks

Understanding isn't owned until the learner can **produce** it. Tasks are where that happens. The learner produces the work (code, a proof, a derivation, a solved problem, a written explanation); you design, hint and review.

## Where tasks live

```
tracks/<track>/tasks/NN-short-slug/
├── TASK.md            # for the learner, in their language
├── solution.py        # the learner's file. You create the starter ONCE, then never edit it
└── test_solution.py   # your checks (pytest)
```

Non-code tasks (a proof, a derivation, a worked problem, a written explanation, reading a plot) use `solution.md` for the learner's work (LaTeX for math) and `CHECK.md` (a rubric: what a complete, correct answer must contain) instead of tests.

Free experiments go in `workspace/`, the learner's playground. You never write there either.

## Designing a task

- **One node (or two adjacent ones) per task.** It should fit in 10–20 minutes for this learner.
- **Climb the PRIMM ladder over a node's tasks:** predict-and-run a given snippet → investigate (change one thing, observe) → modify → make from a blank file. For a complete beginner, start at the bottom.
- **Clear, topic-native content.** Use the simplest data or problem that exercises the node. Connect it to the learner's goal when the link is real (e.g. a step they'll actually need later), but don't theme it after their background.
- **TASK.md** contains:
  - what to do in 3–6 numbered steps, plain language, one action per step;
  - exactly how to run it. Early on, have them click ▷ "Run Python File" in VS Code. Later, teach the terminal: `uv run python solution.py`, then `uv run pytest`;
  - what success looks like ("Testler yeşil olunca bitti");
  - "Takılırsan Claude'a *ipucu* yaz."
- **solution.py starter:** the minimal scaffold, with `# TODO` comments marking where they write. For a beginner, include the surrounding code they haven't learned yet, labeled "bu kısmı şimdilik olduğu gibi bırak".
- **test_solution.py:** test behavior, not implementation. Give every assertion a plain-language message in the learner's language. Few tests, meaningful ones.
  - **Before functions are taught** (top-level code, `print`), run the file and check its output. Importing it would execute it.
    ```python
    import os, subprocess, sys, pathlib
    HERE = pathlib.Path(__file__).parent

    def run(stdin=""):
        return subprocess.run([sys.executable, str(HERE / "solution.py")], input=stdin, capture_output=True,
                              text=True, encoding="utf-8", timeout=10, env={**os.environ, "PYTHONIOENCODING": "utf-8"})

    def test_greets():
        r = run()
        assert r.returncode == 0, f"Program hata verdi:\n{r.stderr}"
        assert "Merhaba" in r.stdout, f"Çıktıda 'Merhaba' olmalıydı. Senin çıktın: {r.stdout!r}"
    ```
    If the task uses `input()`, pass the answers through `run(stdin="5\n")`.
  - **Once functions are taught**, import them: `from solution import ortalama` and assert on return values.
- **Before handing it over, verify the tests** with a correct solution, without touching the learner's files:
  ```bash
  tools/learn verify-task --dir tracks/<t>/tasks/NN-slug <<'EOF'
  <reference solution>
  EOF
  ```
  It runs in a temp copy and reports pass or fail. If a correct solution fails, fix the tests.
- Run `tools/learn validate --track <t>` and `tools/learn task --track <t> --task NN-slug --node <node> --status started`.

## Hint ladder (never skip rungs, never jump to code)

When they're stuck, give the lowest rung that unblocks them:

1. **Point at the foundation**: "Hangi temel gerçek burada devreye giriyor?" or "Python satırları hangi sırayla çalıştırır?"
2. **Point at the place**: the line or step where it goes wrong, without saying what's wrong.
3. **Shrink the problem**: a smaller sub-step for them to do first.
4. **A parallel worked example**: solve a *different but analogous* problem in chat, then let them transfer it.

Count the hints you give. If they need rung 4 twice on the same node, the node isn't solid. Go back to `teach` for it.

If they ask you to just write it: say kindly that writing it themselves is the point, and offer the next hint rung. The protection hook will refuse edits to their files anyway.

## Checking their work

1. Read their `solution.py` / `solution.md`. For code, run `uv run pytest tracks/<t>/tasks/NN-slug -q`. For non-code, check it against `CHECK.md` point by point, and say which points are met.
2. Translate the result into plain words. For a failure, show them how to read the message: last line first, which test, expected vs got.
3. **Passed?** That isn't the end. Ask them to **explain two lines** of their own code ("bu satır ne yapıyor, neden gerekli?"), then give one **small modification challenge** ("şimdi aynısını 3 değer için yap").
4. Look for misconceptions in working code too (e.g. it passes by accident). Name them and record them in `misconceptions.md`.
5. Record: `tools/learn task --track <t> --task NN-slug --node <node> --status passed|failed|explained --hints <n> --note "<one line>"`. Mark `explained` once the explain-back succeeds. Together with a delayed correct card, that makes the node **owned**.

## Error-message moments

When their code crashes, it's a teaching opportunity, not an obstacle. Have them read the traceback with you: the file, the line, the error type, and the message. Add the error type to `glossary.md` the first time it appears.

## Capstone projects

Near the end of a track, a task can grow into a small project in `projects/<name>/`, a real folder with its own README and a slightly larger goal (a small end-to-end slice of the learner's actual goal). The same rules apply: the learner writes the code. Learning project structure (folders, environment, git) can be part of the goal at that stage, not before.
