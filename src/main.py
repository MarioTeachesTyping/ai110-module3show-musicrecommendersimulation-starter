"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # --- Sample User Profiles ---
    # Profile A: "Intense Rock Fan" — high energy, non-acoustic
    user_rock = {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False}

    # Profile B: "Chill Lofi Studier" — low energy, acoustic-leaning
    user_lofi = {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True}

    # Profile C: "Upbeat Pop Listener" — moderate-high energy, danceable
    user_pop = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}

    # Choose which profile to run (change this to test different users)
    user_prefs = user_pop

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
