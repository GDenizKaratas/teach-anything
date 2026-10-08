#!/usr/bin/env python3
"""learn.py — the deterministic half of the learning system.

The LLM teaches; this script owns everything that must be exact:
scheduling (spaced repetition), grading multiple-choice answers,
recording every attempt, and validating tracks against the standard.

Stdlib only. Run through the `tools/learn` wrapper.

Data layout (per track, under tracks/<track>/):
  cards.jsonl     one card per line (content + srs state)
  attempts.jsonl  append-only log of every answer
  misconceptions.md  inventory; ids look like `m-some-slug`
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACKS = ROOT / "tracks"
LEARNER = ROOT / "learner"
STATE = LEARNER / "state.json"
TEMPLATE = ROOT / "tools" / "track-template"

CARD_TYPES = {"mcq", "predict-output", "recall", "explain", "spot-the-bug"}
GRADED_BY_SCRIPT = {"mcq", "predict-output", "spot-the-bug"}  # have options
LETTERS = "ABCD"
MISC_RE = re.compile(r"\bm-[a-z0-9][a-z0-9-]*\b")
DEFAULT_EASE = 2.5
MIN_EASE = 1.3


# ── helpers ────────────────────────────────────────────────────────────────

def today() -> dt.date:
    return dt.date.today()


def die(msg: str, code: int = 1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def out(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=1))


def track_dir(track: str) -> Path:
    d = TRACKS / track
    if not d.is_dir():
        die(f"track '{track}' not found under tracks/ (create it with: new-track {track})")
    return d


def all_tracks() -> list[str]:
    if not TRACKS.is_dir():
        return []
    return sorted(p.name for p in TRACKS.iterdir() if p.is_dir() and (p / "cards.jsonl").exists())


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as e:
            die(f"{path.relative_to(ROOT)} line {i}: invalid JSON ({e})")
    return rows


def write_jsonl(path: Path, rows: list[dict]):
    tmp = path.with_suffix(".tmp")
    tmp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    tmp.replace(path)


def append_jsonl(path: Path, row: dict):
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {}


def save_state(state: dict):
    LEARNER.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def known_misconceptions(track: str) -> set[str]:
    f = TRACKS / track / "misconceptions.md"
    return set(MISC_RE.findall(f.read_text(encoding="utf-8"))) if f.exists() else set()


def find_card(card_id: str) -> tuple[str, list[dict], int]:
    for t in all_tracks():
        cards = read_jsonl(TRACKS / t / "cards.jsonl")
        for i, c in enumerate(cards):
            if c.get("id") == card_id:
                return t, cards, i
    die(f"card '{card_id}' not found")


def public_view(card: dict) -> dict:
    """What gets shown while asking: no correctness, no explanation."""
    v = {k: card[k] for k in ("id", "track", "node", "type", "prompt") if k in card}
    if card.get("code"):
        v["code"] = card["code"]
    if card.get("options"):
        v["options"] = {LETTERS[i]: o["text"] for i, o in enumerate(card["options"])}
    v["due"] = card["srs"]["due"]
    v["reviews"] = card["srs"]["reps"]
    return v


# ── validation (the "same standard" for every track) ──────────────────────

def check_card(card: dict, track: str, miscs: set[str]) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    cid = card.get("id", "?")
    for field in ("node", "type", "prompt", "explanation"):
        if not str(card.get(field, "")).strip():
            errors.append(f"{cid}: missing '{field}'")
    ctype = card.get("type")
    if ctype and ctype not in CARD_TYPES:
        errors.append(f"{cid}: type '{ctype}' not in {sorted(CARD_TYPES)}")
    opts = card.get("options") or []
    if ctype in GRADED_BY_SCRIPT:
        if not 2 <= len(opts) <= 4:
            errors.append(f"{cid}: needs 2-4 options (has {len(opts)}); the UI adds its own 'Other'")
        correct = [o for o in opts if o.get("correct")]
        if len(correct) != 1:
            errors.append(f"{cid}: exactly one option must have correct=true (has {len(correct)})")
        for o in opts:
            if not str(o.get("text", "")).strip():
                errors.append(f"{cid}: option with empty text")
            if o.get("correct"):
                continue
            m = o.get("misconception")
            if not m:
                errors.append(f"{cid}: distractor '{o.get('text', '')[:40]}' has no misconception id")
            elif miscs and m not in miscs:
                errors.append(f"{cid}: misconception '{m}' is not defined in misconceptions.md")
        # tells: the correct option should not stand out
        if correct and len(opts) >= 2:
            c_len = len(correct[0].get("text", ""))
            others = [len(o.get("text", "")) for o in opts if not o.get("correct")]
            avg = sum(others) / len(others) if others else c_len
            if avg and c_len > 1.5 * avg and c_len - avg > 15:
                warnings.append(f"{cid}: correct option is much longer than distractors (length tell)")
        for o in opts:
            if re.search(r"\b(because|since|çünkü|zira|bu yüzden)\b", o.get("text", ""), re.I):
                warnings.append(f"{cid}: option contains justification ('{o['text'][:40]}…'); move reasoning to explanation")
            if "**" in o.get("text", ""):
                warnings.append(f"{cid}: bold inside an option (asymmetric highlighting tell)")
    elif ctype in ("recall", "explain"):
        if not str(card.get("answer", "")).strip():
            errors.append(f"{cid}: recall/explain cards need a reference 'answer'")
    return errors, warnings


REQUIRED_TRACK_FILES = ["README.md", "map.md", "misconceptions.md", "cards.jsonl",
                        "attempts.jsonl", "handoff.md", "cheatsheet.md"]


def validate_track(track: str) -> tuple[list[str], list[str]]:
    d = track_dir(track)
    errors, warnings = [], []
    for f in REQUIRED_TRACK_FILES:
        if not (d / f).exists():
            errors.append(f"{track}: missing {f}")
    if (d / "map.md").exists():
        m = (d / "map.md").read_text(encoding="utf-8")
        if "```mermaid" not in m:
            errors.append(f"{track}: map.md has no mermaid dependency graph")
    for f in ("README.md", "map.md"):
        if (d / f).exists() and "TODO" in (d / f).read_text(encoding="utf-8"):
            warnings.append(f"{track}: {f} still contains TODO")
    miscs = known_misconceptions(track)
    if not miscs:
        warnings.append(f"{track}: misconceptions.md defines no m-… ids yet")
    ids = set()
    for c in read_jsonl(d / "cards.jsonl"):
        if c.get("id") in ids:
            errors.append(f"{c.get('id')}: duplicate id")
        ids.add(c.get("id"))
        e, w = check_card(c, track, miscs)
        errors += e
        warnings += w
    tasks = d / "tasks"
    if tasks.is_dir():
        for t in sorted(p for p in tasks.iterdir() if p.is_dir()):
            if not (t / "TASK.md").exists():
                errors.append(f"{track}/tasks/{t.name}: missing TASK.md")
            if not list(t.glob("test_*.py")) and not (t / "CHECK.md").exists():
                errors.append(f"{track}/tasks/{t.name}: needs test_*.py (code) or CHECK.md (non-code rubric)")
    return errors, warnings


# ── scheduling (SM-2 variant, confidence-aware) ───────────────────────────
# quality: 1 = wrong, 3 = right but guessed, 4 = right but unsure, 5 = right and sure

def quality(correct: str, confidence: int) -> int:
    if correct == "no":
        return 1
    if correct == "partial":
        return 3
    return {1: 3, 2: 4, 3: 5}[confidence]


def schedule(srs: dict, q: int) -> dict:
    srs = dict(srs)
    ease = srs.get("ease", DEFAULT_EASE)
    if q < 3:
        srs["reps"] = 0
        srs["lapses"] = srs.get("lapses", 0) + 1
        srs["interval"] = 1
    else:
        reps = srs.get("reps", 0)
        if reps == 0:
            interval = 1
        elif reps == 1:
            interval = 3
        else:
            interval = round(srs.get("interval", 1) * ease)
        if q == 3:  # a guess is not evidence of memory: grow slowly
            interval = max(1, min(interval, srs.get("interval", 1) + 1))
        srs["interval"] = interval
        srs["reps"] = reps + 1
    srs["ease"] = round(max(MIN_EASE, ease + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))), 2)
    srs["due"] = (today() + dt.timedelta(days=srs["interval"])).isoformat()
    srs["last"] = today().isoformat()
    return srs


# ── commands ───────────────────────────────────────────────────────────────

def cmd_new_track(a):
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", a.track):
        die("track name must be kebab-case, e.g. python-basics")
    d = TRACKS / a.track
    if d.exists():
        die(f"tracks/{a.track} already exists")
    d.mkdir(parents=True)
    (d / "tasks").mkdir()
    for src in TEMPLATE.iterdir():
        text = src.read_text(encoding="utf-8").replace("{{TRACK}}", a.track) \
            .replace("{{TITLE}}", a.title or a.track).replace("{{DATE}}", today().isoformat())
        (d / src.name).write_text(text, encoding="utf-8")
    state = load_state()
    state["active_track"] = a.track
    save_state(state)
    out({"created": f"tracks/{a.track}", "active_track": a.track,
         "next": "fill README.md, map.md, misconceptions.md per the new-track skill, then run validate"})


def cmd_use(a):
    track_dir(a.track)
    state = load_state()
    state["active_track"] = a.track
    save_state(state)
    out({"active_track": a.track})


def cmd_add_card(a):
    track_dir(a.track)
    raw = sys.stdin.read().strip()
    if not raw:
        die("pass card JSON (object or array) on stdin")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        die(f"invalid JSON on stdin: {e}")
    items = data if isinstance(data, list) else [data]
    path = TRACKS / a.track / "cards.jsonl"
    cards = read_jsonl(path)
    existing = {c["id"] for c in cards}
    miscs = known_misconceptions(a.track)
    prefix = "".join(w[0] for w in a.track.split("-"))[:4]
    n = len(cards)
    added, all_warnings = [], []
    for item in items:
        item = dict(item)
        item["track"] = a.track
        if not item.get("id"):
            n += 1
            while f"{prefix}-{n:03d}" in existing:
                n += 1
            item["id"] = f"{prefix}-{n:03d}"
        if item["id"] in existing:
            die(f"id '{item['id']}' already exists")
        if item.get("options"):
            random.shuffle(item["options"])  # position of the correct answer is never chosen by the LLM
        errors, warnings = check_card(item, a.track, miscs)
        if errors:
            die("card rejected:\n  " + "\n  ".join(errors))
        all_warnings += warnings
        item["created"] = today().isoformat()
        item["srs"] = {"due": today().isoformat(), "interval": 0, "ease": DEFAULT_EASE, "reps": 0, "lapses": 0}
        cards.append(item)
        existing.add(item["id"])
        added.append(public_view(item))
    write_jsonl(path, cards)
    res = {"added": added, "warnings": all_warnings}
    if any("options" in c for c in added):
        res["note"] = "present options in exactly this order with these letters; grade only via `record`"
    out(res)


def cmd_due(a):
    tracks = [a.track] if a.track else all_tracks()
    horizon = (today() + dt.timedelta(days=a.ahead)).isoformat()
    rows = []
    for t in tracks:
        for c in read_jsonl(TRACKS / t / "cards.jsonl"):
            if c.get("retired"):
                continue
            if c["srs"]["due"] <= horizon and (a.ahead or c["srs"].get("last") != today().isoformat()):
                rows.append(c)
    # most overdue first, then interleave tracks/nodes so similar items are not blocked together
    rows.sort(key=lambda c: (c["srs"]["due"], -c["srs"].get("lapses", 0)))
    picked, seen_nodes = [], []
    pool = rows[:]
    while pool and len(picked) < a.limit:
        idx = next((i for i, c in enumerate(pool) if c["node"] not in seen_nodes[-2:]), 0)
        c = pool.pop(idx)
        picked.append(public_view(c))
        seen_nodes.append(c["node"])
    out({"due_total": len(rows), "showing": len(picked), "cards": picked})


def cmd_record(a):
    track, cards, i = find_card(a.card)
    card = cards[i]
    result = {"card": card["id"], "node": card["node"]}
    misconception = a.misconception
    if card.get("options"):
        if not a.choice:
            die("this card has options: pass --choice A/B/C/D (or --choice X for 'I don't know')")
        letter = a.choice.upper()
        if letter == "X":
            correct = "no"
            result["chosen"] = "dont-know"
        else:
            idx = LETTERS.find(letter)
            if idx < 0 or idx >= len(card["options"]):
                die(f"choice must be one of {LETTERS[:len(card['options'])]} or X")
            chosen = card["options"][idx]
            correct = "yes" if chosen.get("correct") else "no"
            result["chosen"] = f"{letter}) {chosen['text']}"
            misconception = misconception or chosen.get("misconception")
        right = next(j for j, o in enumerate(card["options"]) if o.get("correct"))
        result["correct_option"] = f"{LETTERS[right]}) {card['options'][right]['text']}"
    else:
        if not a.correct:
            die("open-answer card: pass --correct yes|partial|no (your judgement against the reference answer)")
        correct = a.correct
        result["reference_answer"] = card.get("answer")
    q = quality(correct, a.confidence)
    old_srs = card["srs"]
    card["srs"] = schedule(old_srs, q)
    cards[i] = card
    write_jsonl(TRACKS / track / "cards.jsonl", cards)
    delayed = old_srs.get("last") is not None and old_srs.get("last") != today().isoformat()
    attempt = {"ts": dt.datetime.now().isoformat(timespec="seconds"), "kind": "card", "card": card["id"],
               "node": card["node"], "type": card["type"], "correct": correct, "confidence": a.confidence,
               "misconception": misconception if correct != "yes" else None,
               "delayed": delayed, "session": a.session}
    if a.answer_text:
        attempt["answer_text"] = a.answer_text
    if a.choice:
        attempt["choice"] = a.choice.upper()
    append_jsonl(TRACKS / track / "attempts.jsonl", attempt)
    result.update({"correct": correct, "confidence": a.confidence, "misconception": attempt["misconception"],
                   "explanation": card.get("explanation"), "next_due": card["srs"]["due"]})
    if correct == "no" and a.confidence == 3:
        result["flag"] = "high-confidence error: dig into the belief behind it before moving on (hypercorrection moment)"
    elif correct == "yes" and a.confidence == 1:
        result["flag"] = "correct but guessed: not evidence of knowledge; re-check this node soon with a different question"
    out(result)


def cmd_retire(a):
    track, cards, i = find_card(a.card)
    cards[i]["retired"] = {"on": today().isoformat(), "reason": a.reason}
    write_jsonl(TRACKS / track / "cards.jsonl", cards)
    out({"retired": a.card, "reason": a.reason})


def cmd_task(a):
    track_dir(a.track)
    if a.status not in {"started", "passed", "failed", "explained"}:
        die("status must be started|passed|failed|explained")
    row = {"ts": dt.datetime.now().isoformat(timespec="seconds"), "kind": "task", "task": a.task,
           "node": a.node, "status": a.status, "hints_used": a.hints, "note": a.note}
    append_jsonl(TRACKS / a.track / "attempts.jsonl", row)
    out({"recorded": row})


def node_progress(track: str) -> dict:
    cards = read_jsonl(TRACKS / track / "cards.jsonl")
    attempts = read_jsonl(TRACKS / track / "attempts.jsonl")
    nodes: dict[str, dict] = {}
    for c in cards:
        n = nodes.setdefault(c["node"], {"cards": 0, "attempts": 0, "correct": 0, "delayed_correct": 0,
                                         "lapses": 0, "tasks_passed": 0, "explained": 0})
        n["cards"] += 1
        n["lapses"] += c["srs"].get("lapses", 0)
    for at in attempts:
        n = nodes.setdefault(at.get("node") or "?", {"cards": 0, "attempts": 0, "correct": 0, "delayed_correct": 0,
                                                     "lapses": 0, "tasks_passed": 0, "explained": 0})
        if at["kind"] == "card":
            n["attempts"] += 1
            if at["correct"] == "yes":
                n["correct"] += 1
                if at.get("delayed"):
                    n["delayed_correct"] += 1
        elif at["kind"] == "task":
            if at["status"] == "passed":
                n["tasks_passed"] += 1
            if at["status"] == "explained":
                n["explained"] += 1
    for n in nodes.values():
        # mastery ladder: seen → checked (right in-session) → retained (right after a delay) → owned (retained + did a task)
        if n["attempts"] == 0 and n["tasks_passed"] == 0:
            n["level"] = "new"
        elif n["delayed_correct"] and n["tasks_passed"]:
            n["level"] = "owned"
        elif n["delayed_correct"]:
            n["level"] = "retained"
        elif n["correct"]:
            n["level"] = "checked"
        else:
            n["level"] = "struggling"
    return nodes


def cmd_progress(a):
    tracks = [a.track] if a.track else all_tracks()
    report = {}
    for t in tracks:
        attempts = read_jsonl(TRACKS / t / "attempts.jsonl")
        misc_counts: dict[str, int] = {}
        for at in attempts:
            if at.get("misconception"):
                misc_counts[at["misconception"]] = misc_counts.get(at["misconception"], 0) + 1
        report[t] = {"nodes": node_progress(t),
                     "recurring_misconceptions": dict(sorted(misc_counts.items(), key=lambda x: -x[1])[:8])}
    out(report)


def cmd_signals(a):
    """How this learner learns, computed from their answers across all tracks."""
    cards_att, tasks = [], []
    for t in all_tracks():
        for at in read_jsonl(TRACKS / t / "attempts.jsonl"):
            (cards_att if at["kind"] == "card" else tasks).append(at)
    if not cards_att:
        out({"note": "no answers recorded yet"})
        return

    def acc(rows):
        return {"n": len(rows), "correct_rate": round(sum(r["correct"] == "yes" for r in rows) / len(rows), 2)} if rows else {"n": 0}

    names = {1: "guessed", 2: "unsure", 3: "sure"}
    calib = {names[c]: acc([r for r in cards_att if r.get("confidence") == c]) for c in (1, 2, 3)}
    sure, unsure = calib["sure"], calib["unsure"]
    if sure.get("n", 0) >= 5 and sure["correct_rate"] < 0.7:
        reading = "overconfident: 'sure' answers are often wrong → ask why they are sure, more explain cards, slow down"
    elif unsure.get("n", 0) >= 5 and unsure["correct_rate"] > 0.8:
        reading = "underconfident: 'unsure' answers are mostly right → point out the evidence, fade support faster"
    else:
        reading = "roughly calibrated (or too little data)"
    by_type = {}
    for r in cards_att:
        by_type.setdefault(r["type"], []).append(r)
    recent, earlier = cards_att[-20:], cards_att[-40:-20]
    passed = [t for t in tasks if t["status"] in ("passed", "explained")]
    out({
        "answers": len(cards_att),
        "calibration": calib, "calibration_reading": reading,
        "high_confidence_errors": sum(r["correct"] == "no" and r.get("confidence") == 3 for r in cards_att),
        "dont_know_rate": round(sum(r.get("choice") == "X" for r in cards_att) / len(cards_att), 2),
        "by_question_type": {k: acc(v) for k, v in by_type.items()},
        "delayed_recall": acc([r for r in cards_att if r.get("delayed")]),
        "trend": {"last_20": acc(recent), "previous_20": acc(earlier)},
        "tasks": {"events": len(tasks), "passed": len(passed),
                  "avg_hints_when_passed": round(sum(t.get("hints_used", 0) for t in passed) / len(passed), 1) if passed else None},
        "use": "update the Observed sections of learner/profile.md only with patterns that hold across sessions; cite the evidence",
    })


# ── engagement pacing ("chocolate"): when to recap, tease, celebrate ─────────
# The LLM decides what to say; this decides *when*, so it is neither every message nor never.

MOMENTS = LEARNER / "moments.jsonl"
MOMENT_KINDS = {"recap", "cheatsheet", "teaser", "value", "milestone"}
RECAP_EVERY_NODES = 4      # newly checked nodes since the last recap
VALUE_EVERY_DAYS = 3       # at most one "where this is used" moment per ~3 study days
TEASER_EVERY_DAYS = 2


def all_attempts() -> list[dict]:
    rows = []
    for t in all_tracks():
        for at in read_jsonl(TRACKS / t / "attempts.jsonl"):
            at["track"] = t
            rows.append(at)
    return sorted(rows, key=lambda r: r["ts"])


def checked_nodes() -> int:
    return sum(1 for t in all_tracks() for n in node_progress(t).values()
               if n["level"] in ("checked", "retained", "owned"))


def study_days(attempts: list[dict]) -> list[str]:
    return sorted({r["ts"][:10] for r in attempts})


def streak(days: list[str]) -> int:
    if not days:
        return 0
    d = dt.date.fromisoformat(days[-1])
    if (today() - d).days > 1:
        return 0
    have, n = set(days), 0
    while d.isoformat() in have:
        n += 1
        d -= dt.timedelta(days=1)
    return n


def achieved_milestones(attempts: list[dict]) -> list[str]:
    m = []
    cards = [r for r in attempts if r["kind"] == "card"]
    tasks = [r for r in attempts if r["kind"] == "task"]
    if any(r["correct"] == "yes" for r in cards):
        m.append("first-correct-answer")
    if any(r["correct"] == "yes" and r.get("delayed") for r in cards):
        m.append("first-remembered-after-a-delay")
    if any(t["status"] in ("passed", "explained") for t in tasks):
        m.append("first-task-passed")
    if any(n["level"] == "owned" for t in all_tracks() for n in node_progress(t).values()):
        m.append("first-node-owned")
    c = checked_nodes()
    m += [f"{k}-nodes-learned" for k in (5, 10, 20, 40) if c >= k]
    s = streak(study_days(attempts))
    m += [f"{k}-day-streak" for k in (3, 7, 14, 30) if s >= k]
    for t in all_tracks():
        nodes = node_progress(t)
        if len(nodes) >= 5 and all(n["level"] in ("retained", "owned") for n in nodes.values()):
            m.append(f"track-{t}-retained")
    return m


def engagement_hints() -> list[str]:
    moments = read_jsonl(MOMENTS)
    attempts = all_attempts()
    days = study_days(attempts)
    hints = []

    def last(kind):
        return next((r for r in reversed(moments) if r["kind"] == kind), None)

    def days_since(row):
        if not row:
            return None
        return sum(1 for d in days if d > row["ts"][:10])  # study days, not calendar days

    r = last("recap")
    new_nodes = checked_nodes() - (r.get("checked_nodes", 0) if r else 0)
    if new_nodes >= RECAP_EVERY_NODES:
        hints.append(f"recap due: {new_nodes} nodes newly learned since the last recap → at a natural break, "
                     "'şimdiye kadar neler öğrendik' + link to cheatsheet (then: tools/learn moment --kind recap)")
    for kind, every in (("teaser", TEASER_EVERY_DAYS), ("value", VALUE_EVERY_DAYS)):
        ds = days_since(last(kind))
        if days and (ds is None or ds >= every):
            hints.append(f"{kind} allowed today (one, only if it fits naturally)")
    celebrated = {r.get("note") for r in moments if r["kind"] == "milestone"}
    fresh = [m for m in achieved_milestones(attempts) if m not in celebrated]
    if fresh:
        hints.append(f"uncelebrated milestone: {fresh[0]} → acknowledge it with evidence, briefly "
                     f"(then: tools/learn moment --kind milestone --note {fresh[0]})")
    return hints


def cmd_moment(a):
    if a.kind not in MOMENT_KINDS:
        die(f"kind must be one of {sorted(MOMENT_KINDS)}")
    LEARNER.mkdir(exist_ok=True)
    row = {"ts": dt.datetime.now().isoformat(timespec="seconds"), "kind": a.kind, "note": a.note,
           "checked_nodes": checked_nodes()}
    append_jsonl(MOMENTS, row)
    out({"recorded": row})


def cmd_journey(a):
    """Then-vs-now facts for a recap: concrete evidence of growth."""
    attempts = all_attempts()
    if not attempts:
        out({"note": "nothing recorded yet"})
        return
    days = study_days(attempts)
    cards = [r for r in attempts if r["kind"] == "card"]
    first10, last10 = cards[:10], cards[-10:]

    def rate(rows):
        return round(sum(r["correct"] == "yes" for r in rows) / len(rows), 2) if rows else None

    per_track = {}
    for t in all_tracks():
        nodes = node_progress(t)
        per_track[t] = {"learned": sorted(k for k, n in nodes.items() if n["level"] in ("checked", "retained", "owned")),
                        "owned": sorted(k for k, n in nodes.items() if n["level"] == "owned"),
                        "struggling": sorted(k for k, n in nodes.items() if n["level"] == "struggling")}
    out({"started": days[0], "study_days": len(days), "current_streak": streak(days),
         "answers": len(cards), "accuracy_first_10": rate(first10), "accuracy_last_10": rate(last10),
         "tasks_passed": sum(1 for r in attempts if r["kind"] == "task" and r["status"] in ("passed", "explained")),
         "tracks": per_track})


def handoff_next(track: str) -> str:
    f = TRACKS / track / "handoff.md"
    if not f.exists():
        return ""
    text = f.read_text(encoding="utf-8")
    m = re.search(r"##\s*Next step\s*\n(.*?)(\n##|\Z)", text, re.S | re.I)
    return (m.group(1) if m else text).strip()[:600]


def cmd_status(a):
    """Short, human-readable; printed into Claude's context at session start."""
    lines = ["# Learning system status", f"date: {today().isoformat()}"]
    profile = LEARNER / "profile.md"
    if not profile.exists():
        lines += ["learner: NO PROFILE YET → run the onboarding skill first (greet, explain how this works, build learner/profile.md)."]
        if (LEARNER / "intake.md").exists():
            lines.append("mentor notes: learner/intake.md exists → read it and confirm with the learner instead of re-asking.")
        print("\n".join(lines))
        return
    state = load_state()
    active = state.get("active_track")
    tracks = all_tracks()
    if not tracks:
        lines.append("tracks: none yet → use the new-track skill once the learner's goal is clear.")
    for t in tracks:
        cards = read_jsonl(TRACKS / t / "cards.jsonl")
        due = sum(1 for c in cards if not c.get("retired") and c["srs"]["due"] <= today().isoformat()
                  and c["srs"].get("last") != today().isoformat())
        mark = " (ACTIVE)" if t == active else ""
        levels: dict[str, int] = {}
        for n in node_progress(t).values():
            levels[n["level"]] = levels.get(n["level"], 0) + 1
        lines.append(f"- track {t}{mark}: {len(cards)} cards, {due} due for review today, nodes {levels or '{}'}")
    if active:
        nxt = handoff_next(active)
        if nxt:
            lines += ["", f"## Resume point ({active}/handoff.md)", nxt]
    hints = engagement_hints()
    if hints:
        lines += ["", "## Engagement (see teach/engagement.md; never during struggle)"] + [f"- {h}" for h in hints]
    print("\n".join(lines))


def cmd_validate(a):
    tracks = [a.track] if a.track else all_tracks()
    report, failed = {}, False
    for t in tracks:
        e, w = validate_track(t)
        report[t] = {"errors": e, "warnings": w, "ok": not e}
        failed |= bool(e)
    out(report)
    sys.exit(1 if failed else 0)


def main():
    # Windows consoles default to a legacy code page; Turkish text and symbols need UTF-8.
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(prog="learn", description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status", help="summary for session start")
    s.set_defaults(fn=cmd_status)

    s = sub.add_parser("new-track", help="scaffold tracks/<track> from the template")
    s.add_argument("track")
    s.add_argument("--title")
    s.set_defaults(fn=cmd_new_track)

    s = sub.add_parser("use", help="set the active track")
    s.add_argument("track")
    s.set_defaults(fn=cmd_use)

    s = sub.add_parser("add-card", help="validate + shuffle + store card(s) from stdin JSON")
    s.add_argument("--track", required=True)
    s.set_defaults(fn=cmd_add_card)

    s = sub.add_parser("due", help="cards due for review (interleaved)")
    s.add_argument("--track")
    s.add_argument("--limit", type=int, default=8)
    s.add_argument("--ahead", type=int, default=0, help="look N days ahead (e.g. 1 = what tomorrow brings)")
    s.set_defaults(fn=cmd_due)

    s = sub.add_parser("record", help="record an answer; grades option cards itself")
    s.add_argument("--card", required=True)
    s.add_argument("--choice", help="A-D, or X for 'I don't know'")
    s.add_argument("--correct", choices=["yes", "partial", "no"], help="for open-answer cards")
    s.add_argument("--confidence", type=int, choices=[1, 2, 3], default=2, help="1 guess, 2 unsure, 3 sure")
    s.add_argument("--misconception", help="m-… id you diagnosed (open answers)")
    s.add_argument("--answer-text", help="learner's own words, for open answers")
    s.add_argument("--session", help="free label, e.g. 2026-10-08-a")
    s.set_defaults(fn=cmd_record)

    s = sub.add_parser("retire", help="stop reviewing a card (memorized wording, replaced by a transfer card, flawed)")
    s.add_argument("--card", required=True)
    s.add_argument("--reason", required=True)
    s.set_defaults(fn=cmd_retire)

    s = sub.add_parser("task", help="record a task event")
    s.add_argument("--track", required=True)
    s.add_argument("--task", required=True)
    s.add_argument("--node", required=True)
    s.add_argument("--status", required=True)
    s.add_argument("--hints", type=int, default=0)
    s.add_argument("--note", default="")
    s.set_defaults(fn=cmd_task)

    s = sub.add_parser("progress", help="per-node mastery levels + recurring misconceptions")
    s.add_argument("--track")
    s.set_defaults(fn=cmd_progress)

    s = sub.add_parser("moment", help="log an engagement moment so pacing knows about it")
    s.add_argument("--kind", required=True, help="recap|cheatsheet|teaser|value|milestone")
    s.add_argument("--note", default="")
    s.set_defaults(fn=cmd_moment)

    s = sub.add_parser("journey", help="then-vs-now evidence for recaps and milestones")
    s.set_defaults(fn=cmd_journey)

    s = sub.add_parser("signals", help="how this learner learns: calibration, question types, trend, hints")
    s.set_defaults(fn=cmd_signals)

    s = sub.add_parser("validate", help="check tracks against the standard")
    s.add_argument("--track")
    s.set_defaults(fn=cmd_validate)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
