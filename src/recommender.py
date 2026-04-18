from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return top-k songs sorted by score descending for the given user."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }

        def _score(song: Song) -> float:
            song_dict = {
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "valence": song.valence,
                "acousticness": song.acousticness,
            }
            total, _ = score_song(user_prefs, song_dict)
            return total

        ranked = sorted(self.songs, key=_score, reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        song_dict = {
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "valence": song.valence,
            "acousticness": song.acousticness,
        }
        total, reasons = score_song(user_prefs, song_dict)
        return f"Score {total:.2f}: " + "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dictionaries with numeric conversions."""
    import csv
    import os
    # Resolve path relative to project root (one level up from src/)
    if not os.path.isabs(csv_path):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(base_dir, csv_path)
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["tempo_bpm"] = int(row["tempo_bpm"])
            for key in ("energy", "valence", "danceability", "acousticness"):
                row[key] = float(row[key])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences and return (score, reasons)."""
    score = 0.0
    reasons = []

    # Genre match: +2.0
    if song["genre"] == user_prefs["genre"]:
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood match: +1.5
    if song["mood"] == user_prefs["mood"]:
        score += 1.5
        reasons.append("mood match (+1.5)")

    # Energy proximity: 1.0 × (1 - |target - actual|)
    energy_proximity = 1.0 * (1 - abs(user_prefs["energy"] - song["energy"]))
    score += energy_proximity
    reasons.append(f"energy proximity (+{energy_proximity:.2f})")

    # Valence bonus: 0.5 × valence
    valence_bonus = 0.5 * song["valence"]
    score += valence_bonus
    reasons.append(f"valence bonus (+{valence_bonus:.2f})")

    # Acousticness preference: +0.5 if alignment
    if user_prefs["likes_acoustic"] and song["acousticness"] > 0.6:
        score += 0.5
        reasons.append("acoustic fit (+0.5)")
    elif not user_prefs["likes_acoustic"] and song["acousticness"] < 0.4:
        score += 0.5
        reasons.append("non-acoustic fit (+0.5)")

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank all songs by score and return the top-k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        total, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, total, explanation))

    # sorted() returns a new list, leaving the original unchanged — preferred when
    # you don't want to mutate the input. .sort() mutates in-place and returns None.
    scored = sorted(scored, key=lambda item: item[1], reverse=True)

    return scored[:k]
