"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print top-k recommendations for a given user profile."""
    recommendations = recommend_songs(user_prefs, songs, k=k)
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"  Prefs: genre={user_prefs['genre']}, mood={user_prefs['mood']}, "
          f"energy={user_prefs['energy']}, acoustic={user_prefs['likes_acoustic']}")
    print(f"{'='*60}")
    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"\n  #{i}  {song['title']} by {song['artist']}")
        print(f"      Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"      Score: {score:.2f}")
        print(f"      Reasons: {explanation}")
    print(f"\n{'='*60}\n")


def main() -> None:
    songs = load_songs("data/songs.csv")

    # --- Core User Profiles ---
    profiles = {
        "Profile A: Intense Rock Fan": {
            "genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False
        },
        "Profile B: Chill Lofi Studier": {
            "genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True
        },
        "Profile C: Upbeat Pop Listener": {
            "genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False
        },

        # --- Adversarial / Edge-Case Profiles ---
        "Profile D: Conflicted — High Energy + Sad Mood": {
            "genre": "pop", "mood": "melancholic", "energy": 0.9, "likes_acoustic": False
        },
        "Profile E: Genre Mismatch — Non-existent Genre": {
            "genre": "kpop", "mood": "happy", "energy": 0.7, "likes_acoustic": False
        },
        "Profile F: All-Acoustic Extreme — Min Energy + Acoustic": {
            "genre": "classical", "mood": "peaceful", "energy": 0.1, "likes_acoustic": True
        },
    }

    for label, prefs in profiles.items():
        print_recommendations(label, prefs, songs, k=5)


if __name__ == "__main__":
    main()
