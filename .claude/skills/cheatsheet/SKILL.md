---
name: cheatsheet
description: Build or update a track's cheatsheet together with the learner. It covers only what they have actually learned, and they recall it first. Use when the learner says "cheatsheet", "özet", "kopya kağıdı", "not çıkar", at the end of a track section, or when wrap-up suggests it.
---

# Cheatsheet

A cheatsheet you hand over is just reading material. One the learner reconstructs is retrieval practice, and it ends up containing *their* weak spots. So the learner goes first.

## Flow

1. Pick the nodes: those at level `checked` or higher in `tools/learn progress --track <t>` that aren't in `cheatsheet.md` yet. Never include nodes they haven't learned.
2. **Learner recalls first.** For each node, ask in chat: "Bunu kendi cümlelerinle, bir satırda yaz. Bir de küçük bir örnek." Let them type. "Bilmiyorum" is fine; note it.
3. **You correct and complete.** Keep their wording where it's right, and fix where it's wrong. If something was wrong, record it with `tools/learn record` on a matching card, or add a recall card.
4. Write the entry into `tracks/<t>/cheatsheet.md`, grouped by map node, in this shape:

```markdown
## <node title>
**Temel gerçek:** <the unconditional truth or rule, one line>
**Örnek:** <minimal example: a runnable code block if code, LaTeX if math>
**Dikkat (senin hatan):** <their own recorded misconception for this node, if any, from attempts/misconceptions>
```

5. Tell them where it is ([cheatsheet.md](…), Markdown preview: Cmd+Shift+V on Mac, Ctrl+Shift+V on Windows) and that it grows as they learn. Log it with `tools/learn moment --kind cheatsheet --note "<nodes added>"`.

Keep it short: one screen per ~5 nodes. If an entry needs a paragraph, the node is too big. Split it in `map.md`.
