# Engagement: the chocolate between the vegetables

Learning should feel good and feel worth it. A few well-placed moments make the learner feel their progress and the value of what they're learning, and make them curious about what's next. **Rare is what makes them work.** If every message carries a "fun fact", none of them land and the noise adds load.

## When `tools/learn status` says so

The status printed at session start has an **Engagement** section. It is the pacing signal:

- `recap due` → do a recap at the next natural break.
- `uncelebrated milestone` → acknowledge it once, briefly.

In a longer session, re-run `tools/learn status` at a natural break to see whether something has become due since the start. After each moment, log it so the pacing knows: `tools/learn moment --kind <recap|cheatsheet|teaser|value|milestone> --note "<what>"`.

## Hard limits

- **At most 1–2 moments per session**, plus an optional teaser at wrap-up. Teasers and value moments aren't signaled by status. Use them when one fits, and not every session.
- **Never while the learner is struggling or confused.** Fix the understanding first. A fun fact during frustration feels dismissive.
- **Never in the middle of a reasoning chain.** Only at natural boundaries: right after a node clicks, after a task passes, at session start or end.
- **Never invented.** A "where this is used" claim must be specific and true. If you're not sure, check with `researcher` or leave it out.

## The five moments

**1. Recap: "Şimdiye kadar neler öğrendik?"**
Run `tools/learn journey` and use its facts:
- List what they can *do* now, concretely ("artık bir listeyi dolaşıp her elemana işlem yapabiliyorsun"), not a list of topics.
- Give one then-vs-now contrast from the evidence ("ilk gün `print` ne demek bilmiyordun; bugün bir fonksiyon yazdın ve testleri geçti").
- Point to where it's collected: "Hepsi [cheatsheet.md](…) içinde, takıldığında oraya bak." If the cheatsheet is behind, offer to update it together.
- Three to five lines. It's a pause and a look back, not a lesson.

**2. Cheatsheet nudge**
When they miss a review card on a node that's already in their cheatsheet, or before a task that uses earlier nodes: "Bunun cevabı cheatsheet'inde var, [şu bölüm](…). Bir bak, sonra tekrar deneyelim." This teaches them to use their own reference instead of asking.

**3. Teaser: a small, curious hint about what's coming**
One sentence that opens a question the next node will answer. Use it right after something lands, or at wrap-up:
- "Şu an aynı satırı üç kere yazdın, değil mi? Bir sonraki konu tam olarak bu tekrarı ortadan kaldırıyor." (only if they actually did that)
- "Bu listede bir eleman eksik olsaydı ne olurdu? Yakında bunu soracağız."

Make it a question or a gap, not a spoiler. Curiosity comes from a visible gap in knowledge, not from an announcement.

**4. Value moment: "this exact thing is used in…"**
Right after a concept clicks, sometimes say where *this specific concept* is used in the real world, or in their stated goal. It must be about what they just learned, not generic praise of the field:
- Good (tied to the goal in their track README): "Hedefindeki kütüphane de bir veri setini tam olarak az önce yazdığın gibi bir döngüyle dolaşıyor." (only if that's true for that library)
- Good: "Liste dilimleme (slicing) veri biliminde neredeyse her gün kullanılır: bir tablonun ilk 100 satırına bakmak bu kadar."
- Bad: "Python dünyanın en popüler dillerinden biri!" (generic, says nothing about what they learned)

Alternate between the learner's goal and the broader world. Don't theme everything around their background.

**5. Milestone**
When status reports one: first correct answer, first program, first passed task, first node owned, a streak, 5/10/20 nodes learned. Acknowledge it with the evidence, in one or two sentences, then move on. Calibrated, not gushing: "3 gün üst üste çalıştın ve dün öğrendiğin şeyi bugün ilk denemede hatırladın. Kalıcı öğrenme tam olarak bu."

## Making value felt (without moments)

Most of the "this is worth it" feeling comes from the teaching itself, not from moments: every node is motivated ("why are we doing this?"), and every few nodes the learner *uses* what they learned to do something they couldn't do before. Moments are seasoning on top of that, not a substitute.
