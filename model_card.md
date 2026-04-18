# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, energy level, and acoustic preference. It is designed for classroom exploration and learning about how content-based recommender systems work. It is not intended for real production use, commercial music streaming, or making decisions about what music a real audience should hear.

**Non-intended uses:** This system should not be used to curate playlists for real users, make licensing or royalty decisions, evaluate artist quality, or replace human-curated recommendations. It has no understanding of lyrics, cultural context, or listener history.

---

## 3. How the Model Works

The system takes a user's taste profile (favorite genre, favorite mood, target energy level, and whether they like acoustic music) and compares it against every song in the catalog. Each song gets a score based on how well it matches the user's preferences across five dimensions:

1. **Genre** is the strongest signal. If a song's genre exactly matches the user's favorite, it gets a big boost (+2.0 points).
2. **Mood** is the second strongest. An exact mood match adds +1.5 points.
3. **Energy** uses a proximity rule: the closer a song's energy level is to the user's target, the more points it earns (up to +1.0). A song at energy 0.8 when the user wants 0.9 scores better than one at 0.3.
4. **Valence** gives a mild bonus based on how positive/happy a song sounds (up to +0.5).
5. **Acousticness** adds +0.5 if the song's acoustic character matches what the user wants (acoustic lovers get a bonus for highly acoustic songs; non-acoustic lovers get a bonus for electronic-leaning songs).

After scoring every song, the system sorts them from highest to lowest score and returns the top results along with a plain-English explanation of why each song was picked.

---

## 4. Data

The catalog contains **18 songs** stored in `songs.csv`. Each song has 9 attributes: title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness.

- **Genres represented (14):** pop, lofi, rock, ambient, jazz, synthwave, indie pop, electronic, r&b, country, metal, classical, hip-hop, reggae.
- **Moods represented (11):** happy, chill, intense, relaxed, moody, focused, energetic, romantic, aggressive, peaceful, melancholic.
- No songs were added or removed from the starter dataset.

**Gaps in the data:** Pop and lofi have 2–3 songs each, but most genres (classical, metal, reggae, hip-hop, jazz, etc.) have exactly one song. This means the system cannot offer variety within those genres. The dataset also skews toward English-language, Western genres. There are no songs representing K-pop, Afrobeats, Latin, Bollywood, or many other global music styles. Mood labels are subjective and were assigned by one person, so they may not reflect how most listeners would categorize those songs.

---

## 5. Strengths

- **Clear separation of opposites.** The system does a good job distinguishing users with very different tastes. An intense rock fan and a chill lofi studier get completely different top-5 lists with zero overlap.
- **Reasonable results for well-represented genres.** Pop and lofi users get sensible recommendations because the catalog has multiple songs in those genres, allowing energy and mood to act as meaningful tie-breakers.
- **Graceful degradation.** When a user requests a genre that doesn't exist in the catalog (e.g., "kpop"), the system doesn't crash. It falls back to mood, energy, and other features, producing results that are generic but not nonsensical.
- **Transparency.** Every recommendation comes with a score breakdown explaining exactly why it was picked. A user can see "genre match (+2.0); energy proximity (+0.88)" and understand what drove the suggestion. Real streaming platforms rarely offer this level of explainability.

---

## 6. Limitations and Bias

The system over-prioritizes genre because the genre weight (2.0) is the single largest component of the total score. A song that perfectly matches a user's mood, energy, and acoustic preferences but belongs to the wrong genre will almost always rank below a genre-matched song with poor fit on every other dimension. This creates a filter bubble: once you tell the system you like "pop," it struggles to recommend anything outside that label even if the musical qualities are nearly identical (e.g., "indie pop" is treated as completely unrelated to "pop").

The dataset is also heavily skewed. Of the 18 songs, pop and lofi each have 2–3 entries while genres like classical, metal, reggae, and hip-hop have exactly one song each. This means users who prefer those minority genres will always get the same single song at the top, and the remaining recommendations are essentially random noise from unrelated genres. The system cannot distinguish between "I like hip-hop" and "I like this one specific hip-hop song."

Additionally, mood matching uses exact string equality, so "chill" and "relaxed" are treated as completely different moods even though a real listener would consider them similar. A user asking for "chill" music will never be offered the jazz song tagged "relaxed" as a mood match, losing 1.5 points of potential score. The system has no concept of semantic similarity between mood labels.

Finally, when a user specifies conflicting preferences (e.g., high energy + melancholic mood), the system does not flag the conflict, it simply scores each dimension independently. The result is that genre and energy dominate the ranking while the melancholic mood match barely contributes, since only one song in the catalog carries that label.

---

## 7. Evaluation

The system was tested using six user profiles that cover a range of tastes and edge cases:

- **Three core profiles** (rock fan, lofi studier, pop listener) verified that the system produces distinct, intuitive results for common preferences.
- **Three adversarial profiles** (conflicting preferences, non-existent genre, extreme acoustic preference) probed how the system handles unusual or impossible inputs.
- **Profile-pair comparisons** examined whether two similar users get appropriately similar results and whether two different users get appropriately different results.
- **Two weight experiments** (boosting energy while reducing genre, and removing mood entirely) revealed how sensitive the rankings are to scoring parameters.
- **Automated unit tests** in `test_recommender.py` confirmed that the scoring function returns correct values and that the recommender sorts songs by score in the right order.

No numeric accuracy metric was used because there is no ground-truth "correct" recommendation. Instead, evaluation was qualitative: do the results match what a reasonable human listener would expect?

---

## 8. Future Work

1. **Fuzzy genre and mood matching.** Introduce a similarity map so that "indie pop" partially matches "pop" and "chill" partially matches "relaxed," reducing the rigidity of exact-string comparisons.
2. **Larger and more balanced catalog.** Expand to 50–100 songs with at least 3–5 per genre so the system can offer real variety within any genre preference.
3. **User feedback loop.** Let users rate recommendations (thumbs up/down) and adjust weights over time, moving toward a simple collaborative filtering hybrid.

---

## 9. Personal Reflection

My biggest learning moment was seeing how the conflicting-preferences profile (high energy + melancholic mood) exposed a fundamental limitation. The system just adds up numbers without understanding whether the combination makes emotional sense. It happily serves upbeat pop to someone who said they want to feel melancholic, because the genre and energy points outweigh mood. That made me realize that real recommender systems face the same problem at scale; they optimize a score, not an experience.

Using AI tools helped me move quickly through boilerplate (loading CSVs, structuring dataclasses, writing test scaffolding) and brainstorm edge-case profiles I might not have thought of. But I had to double-check the scoring logic carefully. The AI sometimes suggested weight values or scoring formulas that sounded reasonable but produced unintuitive rankings when I actually ran them against the catalog. The lesson: AI is great for drafting, but you still need to run the code and look at the output with your own eyes.

What surprised me most is how "real" even a simple weighted-scoring system can feel. With just five rules and 18 songs, the recommendations genuinely seemed personalized. A rock fan gets rock songs, a lofi studier gets lofi, and the explanations make each pick feel deliberate. It's easy to see how users could trust a system like this even though it knows nothing about music; it just matches labels and numbers.

If I extended this project, I would add a simple web interface where users could input their preferences and see recommendations update in real time, and I would experiment with embedding-based similarity (using song audio features from an API like Spotify's) instead of hand-picked categorical labels.


