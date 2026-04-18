# Reflection: Music Recommender Evaluation

## Profile-Pair Comparisons

### Rock Fan (A) vs. Chill Lofi Studier (B)

These two profiles sit at opposite ends of the energy spectrum (0.9 vs. 0.35) and prefer completely different genres and moods. The rock fan's top 5 is dominated by high-energy, non-acoustic tracks; Storm Runner, Gym Hero, Street Poet; while the lofi studier gets Library Rain, Midnight Coding, and Spacewalk Thoughts. There is zero overlap between the two lists. This makes sense because genre (2.0) and mood (1.5) together account for up to 3.5 points, and the two profiles share neither genre nor mood. The energy gap between the profiles (0.55) also pushes songs in opposite directions. The system correctly separates these two very different listeners.

### Upbeat Pop Listener (C) vs. Conflicted High-Energy Melancholic (D)

Both profiles prefer pop and high energy, but C wants "happy" while D wants "melancholic." Despite this mood difference, their top two songs are the same; Sunrise City and Gym Hero; just in different order. This happens because the genre match (+2.0) and energy proximity (~0.9) are so dominant that mood only reshuffles things slightly. Frostbite Dawn (the only melancholic song) appears at #3 for D but not at all for C, which is the only visible effect of the mood difference. This reveals a weakness: a user who explicitly asked for sad, high-energy pop music still gets served happy pop because the system weights genre more than mood. In plain language, if you told the system "I want to feel melancholic" but you also like pop, it hands you the same upbeat pop songs anyway, the "melancholic" part of your request barely matters.

### Genre Mismatch "kpop" (E) vs. Upbeat Pop Listener (C)

Profile E asks for "kpop," which doesn't exist in the catalog, while C asks for "pop." The pop listener gets Sunrise City at #1 with a score of 5.40; the kpop listener gets Rooftop Lights at #1 with only 3.34. Without genre match ever firing, the kpop user's rankings are driven entirely by mood ("happy") and energy proximity. Interestingly, Rooftop Lights (indie pop/happy) beats Sunrise City (pop/happy) for the kpop user because its energy (0.76) is closer to the target (0.7). This shows the system degrades gracefully (it doesn't crash or return garbage) but the recommendations feel generic. A real system would benefit from fuzzy genre matching so that "kpop" could partially match "pop" or "indie pop."

### All-Acoustic Extreme (F) vs. Chill Lofi Studier (B)

Both profiles prefer low energy and acoustic sounds, but F targets classical/peaceful while B targets lofi/chill. Their top-1 songs are completely different (Quiet Pages vs. Library Rain), but positions #4–5 overlap (Library Rain and Focus Flow appear in both lists). The overlap makes sense because lofi and classical share acoustic qualities and low energy. The divergence at the top is entirely driven by the genre match bonus. Profile F's #1 (Quiet Pages, score 5.25) has a 3.6-point gap over its #2, exposing the small-catalog problem: there's only one classical song, so the system can't offer variety within that genre.

### Rock Fan (A) vs. Conflicted High-Energy Melancholic (D)

Both profiles want high energy (0.9) and are non-acoustic, but A wants rock/intense while D wants pop/melancholic. Storm Runner ranks #1 for A but doesn't appear in D's top 5 at all, because it's in the rock genre and D prefers pop. Meanwhile, Gym Hero (pop/intense, energy 0.93) appears in both lists — #2 for A (via mood match) and #1 for D (via genre match). This shows that the same song can appear for very different reasons depending on which dimension it matches. It also illustrates why "Gym Hero" keeps showing up: it's high energy, high valence, non-acoustic, and pop; it accumulates points from many dimensions even when it doesn't perfectly match what the user asked for. If you're a non-programmer wondering why "Gym Hero" keeps appearing for people who just want "Happy Pop," it's because the song checks so many boxes (pop genre, high energy, high danceability score, low acousticness) that it earns enough partial-match points to sneak into nearly any high-energy, non-acoustic list.

## What I Learned

The biggest takeaway is that weighted scoring systems are only as good as their weights and their data. Genre at 2.0 creates a strong filter bubble, it's the single most powerful signal, and if it fires, it almost guarantees a top-3 placement regardless of other dimensions. Reducing genre weight and increasing energy weight in our experiment made the system feel more exploratory and diverse, but also less precise for users with strong genre loyalty.

Mood matching had a subtler-than-expected impact. Removing it entirely only shuffled a few positions within the top 5 for most profiles, because genre and energy already did most of the differentiation. This suggests that in our small 18-song catalog, mood is a "tie-breaker" rather than a primary signal.

The adversarial profiles were most revealing. The conflicting-preferences profile (high energy + melancholic) showed that the system doesn't understand emotional coherence, it just adds up numbers. And the non-existent genre profile showed that graceful degradation works but produces bland results. Real recommender systems would need fallback logic (fuzzy matching, collaborative signals) to handle these cases well.
