# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The system over-prioritizes genre because the genre weight (2.0) is the single largest component of the total score. A song that perfectly matches a user's mood, energy, and acoustic preferences but belongs to the wrong genre will almost always rank below a genre-matched song with poor fit on every other dimension. This creates a filter bubble: once you tell the system you like "pop," it struggles to recommend anything outside that label even if the musical qualities are nearly identical (e.g., "indie pop" is treated as completely unrelated to "pop").

The dataset is also heavily skewed. Of the 18 songs, pop and lofi each have 2–3 entries while genres like classical, metal, reggae, and hip-hop have exactly one song each. This means users who prefer those minority genres will always get the same single song at the top, and the remaining recommendations are essentially random noise from unrelated genres. The system cannot distinguish between "I like hip-hop" and "I like this one specific hip-hop song."

Additionally, mood matching uses exact string equality, so "chill" and "relaxed" are treated as completely different moods even though a real listener would consider them similar. A user asking for "chill" music will never be offered the jazz song tagged "relaxed" as a mood match, losing 1.5 points of potential score. The system has no concept of semantic similarity between mood labels.

Finally, when a user specifies conflicting preferences (e.g., high energy + melancholic mood), the system does not flag the conflict, it simply scores each dimension independently. The result is that genre and energy dominate the ranking while the melancholic mood match barely contributes, since only one song in the catalog carries that label.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

We tested six user profiles covering a range of tastes and edge cases:

1. **Intense Rock Fan** (rock, intense, energy 0.9, non-acoustic) — Storm Runner ranked #1 at 5.23 with full genre + mood match. This felt exactly right.
2. **Chill Lofi Studier** (lofi, chill, energy 0.35, acoustic) — Library Rain edged out Midnight Coding (5.30 vs 5.21) thanks to a perfect energy match. Both are lofi/chill, so the tiny energy difference decided the ranking.
3. **Upbeat Pop Listener** (pop, happy, energy 0.8, non-acoustic) — Sunrise City ranked #1 at 5.40. Gym Hero ranked #2 despite being pop because its mood is "intense," not "happy," costing it 1.5 points.
4. **Conflicted — High Energy + Melancholic** (pop, melancholic, energy 0.9, non-acoustic) — This was the most surprising profile. Gym Hero (pop/intense, energy 0.93) ranked #1 at 3.85 even though the user wanted melancholic music. The only truly melancholic song (Frostbite Dawn) ranked #3 because it's electronic, not pop — genre dominance overruled mood intent. This profile exposed the filter-bubble problem most clearly.
5. **Genre Mismatch — "kpop"** (kpop, happy, energy 0.7, non-acoustic) — Since no song in the catalog is labeled "kpop," genre match never fires. Rankings fell back on mood + energy + valence, producing a reasonable happy-music list (Rooftop Lights, Sunrise City, Backroad Anthem) but with low scores (~3.3). The system degrades gracefully rather than erroring.
6. **All-Acoustic Extreme** (classical, peaceful, energy 0.1, acoustic) — Quiet Pages was the only classical song and ranked #1 at 5.25, with a 3.6-point gap over #2. This highlighted small-catalog bias: the system cannot differentiate "likes classical" from "likes this one classical song."

**Experiment 1 — Weight Shift (energy ×2, genre ×0.5):** Mood-matched songs from non-matching genres climbed significantly. For the rock fan, Gym Hero jumped from 3.35 to 4.33 and Street Poet from 3.16 to 4.06. For the pop listener, Rooftop Lights (indie pop/happy) leapfrogged Gym Hero (pop/intense). The change made recommendations feel more musically diverse but sometimes less "on-brand."

**Experiment 2 — Mood Removal:** Without mood scoring, the lofi profile's #2 and #3 swapped — Focus Flow (lofi/focused) rose above Midnight Coding (lofi/chill) because Focus Flow's energy is slightly closer. The ambient song Spacewalk Thoughts dropped from #4 to #5 since it lost its mood bonus. This confirmed that mood acts as an important secondary differentiator within the same genre.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
