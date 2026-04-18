# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This project simulates a content-based music recommender. It scores a catalog of 18 songs against a user's taste profile using weighted feature matching (genre, mood, energy, valence, acousticness) and returns the top-k recommendations with explanations for each pick.

---

## How The System Works

### How Real-World Recommendations Work

Major streaming platforms like Spotify use two core approaches to predict what users will love next:

- **Collaborative filtering** relies on the behavior of many users; likes, skips, playlist additions, listening duration, and session context (time of day, device). It finds "users like you" and recommends what similar listeners enjoyed. The key insight is that you never need to analyze the music itself; patterns in collective behavior are enough.
- **Content-based filtering** relies on song attributes; genre, tempo, energy, mood, valence, danceability, acousticness. It builds a profile of what a user likes and finds songs with similar characteristics. The key insight is that songs sharing musical DNA tend to appeal to the same person.

Spotify combines both approaches (a hybrid system) and layers on reinforcement learning to optimize for long-term satisfaction, not just immediate clicks. The main data types flowing through these systems include: **user signals** (likes, skips, saves, playlist adds, listening time) and **audio features** (tempo, energy, valence, danceability, acousticness, key, loudness).

### What Our Version Prioritizes

Our simulator implements a **content-based filtering** approach. Since we have no multi-user behavior data, we focus entirely on matching song attributes to a single user's taste profile. The scoring system uses a proximity-based rule: for numerical features like energy, a song is scored higher the *closer* it is to the user's target value (using `1 - |preference - value|`), rather than simply rewarding higher or lower values. Categorical features (genre, mood) use exact-match bonuses with configurable weights.

We need two distinct rules to make this work:
1. **Scoring Rule** (per song): Evaluates one song against the user profile and produces a numeric score with an explanation.
2. **Ranking Rule** (for the catalog): Sorts all scored songs in descending order and returns the top-k results as the final recommendation list.

### Algorithm Recipe

The scoring function computes a total score for each song as follows:

| Feature         | Rule                                           | Weight |
|-----------------|------------------------------------------------|--------|
| **Genre**       | +2.0 if song genre == user's favorite genre    | 2.0    |
| **Mood**        | +1.5 if song mood == user's favorite mood      | 1.5    |
| **Energy**      | `1.0 × (1 - |target_energy - song.energy|)`    | 1.0    |
| **Valence**     | `0.5 × song.valence` (mild bonus for positive) | 0.5    |
| **Acousticness**| +0.5 if `likes_acoustic` and acousticness > 0.6, or if `!likes_acoustic` and acousticness < 0.4 | 0.5 |

**Total score** = genre_points + mood_points + energy_proximity + valence_bonus + acoustic_bonus

Genre matching is weighted most heavily (2.0) because it defines the broadest musical category. Mood is next (1.5) because two songs in the same genre can feel completely different. Energy proximity (1.0) fine-tunes intensity. Valence and acousticness are lighter signals (0.5 each) that nudge the ranking without dominating it.

**Ranking Rule**: After scoring every song, sort descending by total score. Return the top-k songs along with their scores and a human-readable explanation of why each was picked.

### Data Flow Diagram

```mermaid
flowchart TD
    A[User Profile\ngenre, mood, energy, likes_acoustic] --> B[Load Song Catalog\nsongs.csv, 18 songs]
    B --> C{For each song in catalog}
    C --> D[Score: Genre Match?\n+2.0 if match]
    D --> E[Score: Mood Match?\n+1.5 if match]
    E --> F[Score: Energy Proximity\n+1.0 × 1 minus abs diff]
    F --> G[Score: Valence Bonus\n+0.5 × valence]
    G --> H[Score: Acoustic Fit?\n+0.5 if preference aligns]
    H --> I[Total Score for this song]
    I --> C
    C -->|All songs scored| J[Sort songs by score descending]
    J --> K[Return Top-K Recommendations\nwith scores and explanations]
```

### Sample User Profiles

To verify the system can differentiate between different tastes, we define three test profiles:

- **Intense Rock Fan**: `{genre: "rock", mood: "intense", energy: 0.9, likes_acoustic: False}`; it should rank "Storm Runner" and "Shattered Glass" highest
- **Chill Lofi Studier**: `{genre: "lofi", mood: "chill", energy: 0.35, likes_acoustic: True}`; it should rank "Library Rain" and "Midnight Coding" highest
- **Upbeat Pop Listener**: `{genre: "pop", mood: "happy", energy: 0.8, likes_acoustic: False}`; it should rank "Sunrise City" and "Gym Hero" highest

### Potential Biases

- **Genre over-prioritization**: At weight 2.0, genre dominates the score. A song that perfectly matches mood, energy, and acousticness but is in the wrong genre will score lower than a genre-match with poor fit elsewhere. This mirrors a real filter bubble problem.
- **Categorical rigidity**: An "indie pop" song won't match a "pop" preference despite being closely related. The system has no concept of genre similarity.
- **Small catalog bias**: With only 18 songs, some genres have a single representative. The system can't distinguish between liking "hip-hop" as a genre and liking the one hip-hop song's specific attributes.
- **No temporal or contextual awareness**: The system ignores time of day, recent listening history, or sequential flow; all things real recommenders account for.

### Features Used

**`Song` attributes** (from `songs.csv`, 18-song catalog):
- `genre`: categorical (pop, lofi, rock, ambient, jazz, synthwave, indie pop, electronic, r&b, country, metal, classical, hip-hop, reggae)
- `mood`: categorical (happy, chill, intense, relaxed, moody, focused, energetic, romantic, aggressive, peaceful, melancholic)
- `energy`: float [0–1], intensity/excitement level
- `valence`: float [0–1], musical positivity
- `danceability`: float [0–1], rhythmic suitability for dancing
- `acousticness`: float [0–1], acoustic vs. electronic character
- `tempo_bpm`: integer, beats per minute

**`UserProfile` attributes**:
- `favorite_genre`: preferred genre (exact-match scoring)
- `favorite_mood`: preferred mood (exact-match scoring)
- `target_energy`: preferred energy level (proximity scoring)
- `likes_acoustic`: boolean preference for acoustic sound (bonus/penalty on acousticness)

### Terminal Output

<a href="terminal-output.png" target="_blank"><img src='terminal-output.png' title='Terminal Output' width='' alt='Terminal Output' class='center-block' /></a>

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

### Experiment 1: Weight Shift (energy ×2, genre ×0.5)

We doubled the energy weight from 1.0 to 2.0 and halved genre from 2.0 to 1.0. Key observations:

- **Rock Fan:** Gym Hero jumped from score 3.35 to 4.33 and Street Poet from 3.16 to 4.06; mood-matched songs from non-matching genres gained the most.
- **Pop Listener:** Rooftop Lights (indie pop/happy) leapfrogged Gym Hero (pop/intense) because energy proximity now outweighed genre loyalty.
- **Lofi Studier:** Spacewalk Thoughts (ambient/chill) climbed from #4 to #3, pushing into the top 3 because its energy was close to the target.
- Overall the change made recommendations more musically diverse but less "on-brand" for users with strong genre preferences.

### Experiment 2: Mood Removal

We commented out the mood matching check (+1.5 bonus). Key observations:

- **Lofi Studier:** Focus Flow (lofi/focused) rose above Midnight Coding (lofi/chill) since they share a genre but Focus Flow's energy is slightly closer. Without mood, the tie-breaker shifted to energy.
- **Rock Fan:** Gym Hero and Sunrise City became nearly tied (1.85 vs 1.84) since both lost their mood bonus and were differentiated only by energy/valence.
- **Conflicted profile (D):** Frostbite Dawn dropped from #3 to completely off the top 5, since mood was the only reason it appeared.
- Conclusion: mood is an important secondary differentiator, especially within the same genre. Without it, the system becomes blander.

---

## Limitations and Risks

- **Genre over-prioritization:** At weight 2.0, genre dominates scoring. A perfect mood/energy/acoustic match in the wrong genre will always lose to a mediocre same-genre match. This creates a filter bubble.
- **Tiny catalog (18 songs):** Genres like classical, metal, reggae, and hip-hop have exactly one representative. The system can't distinguish "I like classical music" from "I like Quiet Pages specifically."
- **No semantic similarity for categories:** "indie pop" ≠ "pop" and "chill" ≠ "relaxed" in the scoring logic, even though real listeners treat them as nearly interchangeable.
- **Conflicting preferences are silently ignored:** A user asking for high-energy melancholic pop gets served upbeat pop because the system adds dimensions independently without detecting contradictions.
- **No lyrics, language, or temporal context:** The system knows nothing about song content beyond numeric features and categorical labels.

See [model_card.md](model_card.md) for a deeper analysis.

---

## Reflection

Read the full evaluation details:

- [**Model Card**](model_card.md)
- [**Detailed Reflection & Profile Comparisons**](reflection.md)

The biggest lesson from this project is that weighted scoring systems are only as good as their weights and their data. Genre at 2.0 creates a strong filter bubble, it's the single most powerful signal, and if it fires, it almost guarantees a top-3 placement regardless of other dimensions. Reducing genre weight and increasing energy weight made the system more exploratory but less precise for users with strong genre loyalty.

Bias shows up in subtle ways. The dataset is 18 songs, and genres like classical, metal, and hip-hop have exactly one entry each, so the system can't distinguish between "liking a genre" and "liking one specific song." Mood matching uses exact strings, so "chill" and "relaxed" are treated as unrelated. And conflicting preferences (high energy + sad mood) are never flagged; the system just adds up scores, producing results that look reasonable on paper but feel wrong to a human listener. These are the same kinds of issues that real recommender systems face at scale, just easier to see in a small simulation.

### Personal Reflection

**Biggest learning moment:** Watching the conflicting-preferences profile (high energy + melancholic) get served upbeat pop songs taught me that scoring systems optimize numbers, not experiences. The system had no way to know that "melancholic" and "high energy pop" are emotionally contradictory; it just added the points up. That single test case changed how I think about what "personalization" really means in AI systems.

**How AI tools helped (and where I double-checked):** AI tools were great for scaffolding, generating the dataclass structure, writing CSV loading code, and brainstorming adversarial test profiles I wouldn't have thought of on my own. But I had to double-check the scoring logic manually. On more than one occasion, AI-suggested weight values produced rankings that looked correct in isolation but fell apart when I ran all six profiles side by side. The takeaway: AI accelerates the drafting phase, but you still need to run the code and inspect the output yourself.

**What surprised me about simple algorithms:** Even with just five rules and 18 songs, the recommendations genuinely felt personalized. A rock fan gets rock, a lofi listener gets lofi, and the score explanations make each pick feel intentional. It's easy to see how users could develop trust in a system like this, even though it understands nothing about music; it just matches labels and numbers. That's both powerful and a little unsettling.

**What I'd try next:** I would build a small web interface (Flask or Streamlit) so users can adjust preferences with sliders and see recommendations update in real time. I'd also experiment with fuzzy matching for genres and moods (so "indie pop" partially matches "pop") and explore using embedding-based similarity from a real audio API instead of hand-assigned categorical labels.


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

