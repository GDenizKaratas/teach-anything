---
name: setup
description: Get the learner's machine ready for hands-on work in this repo (Python via uv, VS Code Python extension, project packages such as pytest or nilearn), and diagnose environment problems. Use before the first coding task, when the learner says "kurulum", "Python yok", "çalışmıyor", "ModuleNotFoundError", or when a track needs new packages.
---

# Setup

The learner may never have used a terminal. Go one step at a time, explain what each step does in one sentence, and **ask before installing anything** on their machine.

## Check first

```bash
tools/doctor
```

It reports: uv, Python, the `.venv`, pytest, and optional packages. Fix only what's missing.

## Steps (only the missing ones)

1. **uv**: the tool that installs Python and packages for this project.
   macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`. Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`.
   Before running it, tell the learner what it is and get their OK. After installing, VS Code may need a restart for the terminal to find `uv`.
2. **Project environment**: `uv sync`. This creates `.venv/` with Python and the base packages (`pytest`).
3. **Track packages**: when a track needs more, they're declared in `pyproject.toml` as dependency groups. Example: `uv sync --group neuro` for nilearn. Install them when the track reaches them, not on day one.
4. **VS Code**: install the recommended extensions when VS Code offers them (`.vscode/extensions.json`): Python and Mermaid preview. The interpreter is already set to `.venv` in `.vscode/settings.json`. If VS Code asks which Python to use, pick the one in `.venv`.
5. **Smoke test**: have the learner create `workspace/merhaba.py` *themselves* with `print("Merhaba")` and run it with the ▷ button. That's their first program, so make it a moment.

## Adding packages for a new track

Look up the current package name and version in the official docs (with `researcher` if unsure). Add the package to a dependency group in `pyproject.toml` with `uv add --group <group> <package>`, then run `tools/doctor` again.

## When something breaks

Read the error together with the learner, last line first. Common causes: `uv` isn't on PATH yet (restart the terminal or VS Code), the wrong interpreter is selected in VS Code, or a group was never synced (`ModuleNotFoundError`).
