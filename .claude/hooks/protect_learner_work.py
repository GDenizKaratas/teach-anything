"""PreToolUse hook: the learner writes their own code.

Blocks Claude from editing:
  - tracks/*/tasks/*/solution*.py once it exists (Claude may create the starter once)
  - anything under workspace/ or projects/ (the learner's own space)
"""
import json
import os
import sys
from pathlib import Path

data = json.load(sys.stdin)
tool_input = data.get("tool_input", {})
raw = tool_input.get("file_path") or tool_input.get("notebook_path")
if not raw:
    sys.exit(0)

root = Path(os.environ.get("CLAUDE_PROJECT_DIR", data.get("cwd", "."))).resolve()
path = Path(raw)
path = (path if path.is_absolute() else root / path).resolve()
try:
    rel = path.relative_to(root).parts
except ValueError:
    sys.exit(0)

reason = None
if rel and rel[0] in ("workspace", "projects"):
    reason = f"{'/'.join(rel)} is in the learner's own space."
elif len(rel) >= 5 and rel[0] == "tracks" and rel[2] == "tasks" and rel[-1].startswith("solution") and path.exists():
    reason = f"{'/'.join(rel)} is the learner's solution file (the starter already exists)."

if reason:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason + " The learner writes this code themselves. Use the hint ladder from the task skill instead; show analogous examples in chat, never their solution.",
    }}))
sys.exit(0)
