"""
recommendations.py
-------------------
Holds the curated recommendation database and the logic that picks
movies, videos, and games for a given stress level + mood preference.
"""

import random

# ---------------------------------------------------------------------------
# Recommendation database
# Each item is tagged with the stress levels it suits best, plus a "mood"
# category so users can nudge results toward what they feel like doing.
# ---------------------------------------------------------------------------

MOVIES = [
    {"title": "The Secret Life of Walter Mitty", "genre": "Adventure/Feel-good", "levels": ["Low", "Medium"], "mood": "uplifting"},
    {"title": "Paddington 2", "genre": "Comedy/Family", "levels": ["Low", "Medium", "High"], "mood": "comforting"},
    {"title": "My Neighbor Totoro", "genre": "Animation", "levels": ["Medium", "High"], "mood": "calming"},
    {"title": "Chef", "genre": "Comedy/Drama", "levels": ["Low", "Medium"], "mood": "uplifting"},
    {"title": "Julie & Julia", "genre": "Comedy/Drama", "levels": ["Low", "Medium"], "mood": "comforting"},
    {"title": "Kiki's Delivery Service", "genre": "Animation", "levels": ["Medium", "High"], "mood": "calming"},
    {"title": "The Grand Budapest Hotel", "genre": "Comedy", "levels": ["Low", "Medium"], "mood": "uplifting"},
    {"title": "Amélie", "genre": "Romance/Comedy", "levels": ["Low", "Medium"], "mood": "comforting"},
    {"title": "Spirited Away", "genre": "Animation/Fantasy", "levels": ["Medium", "High"], "mood": "calming"},
    {"title": "Soul", "genre": "Animation/Drama", "levels": ["Medium", "High"], "mood": "reflective"},
    {"title": "Inside Out", "genre": "Animation", "levels": ["Medium", "High"], "mood": "reflective"},
    {"title": "The Princess Bride", "genre": "Adventure/Comedy", "levels": ["Low", "Medium"], "mood": "uplifting"},
    {"title": "Julie's Greenroom (light background watch)", "genre": "Family", "levels": ["High"], "mood": "calming"},
    {"title": "Groundhog Day", "genre": "Comedy", "levels": ["Low", "Medium"], "mood": "uplifting"},
    {"title": "Coco", "genre": "Animation", "levels": ["Medium", "High"], "mood": "reflective"},
]

VIDEOS = [
    {"title": "10-Minute Guided Breathing Meditation", "genre": "Meditation", "levels": ["High", "Medium"], "mood": "calming"},
    {"title": "Rain Sounds on a Cabin Roof (3 Hours)", "genre": "Ambient/Nature", "levels": ["High"], "mood": "calming"},
    {"title": "Bob Ross - The Joy of Painting (Full Episode)", "genre": "Relaxing", "levels": ["Medium", "High"], "mood": "comforting"},
    {"title": "Cute Dogs Being Ridiculous - Compilation", "genre": "Comedy/Animals", "levels": ["Low", "Medium"], "mood": "uplifting"},
    {"title": "5-Minute Desk Stretch Routine", "genre": "Fitness", "levels": ["Low", "Medium"], "mood": "energizing"},
    {"title": "Yoga for Stress Relief (20 min)", "genre": "Fitness/Wellness", "levels": ["Medium", "High"], "mood": "calming"},
    {"title": "Lo-fi Beats to Relax/Study To", "genre": "Music", "levels": ["Low", "Medium", "High"], "mood": "calming"},
    {"title": "Satisfying Pottery Throwing ASMR", "genre": "ASMR", "levels": ["Medium", "High"], "mood": "calming"},
    {"title": "Stand-Up Comedy Shorts Compilation", "genre": "Comedy", "levels": ["Low", "Medium"], "mood": "uplifting"},
    {"title": "Ocean Waves at Sunset (Ambient Nature)", "genre": "Nature", "levels": ["High"], "mood": "calming"},
    {"title": "Beginner Full-Body Stretch & Breathwork", "genre": "Fitness", "levels": ["Medium", "High"], "mood": "calming"},
    {"title": "Feel-Good Travel Vlog: Coastal Villages", "genre": "Travel", "levels": ["Low", "Medium"], "mood": "uplifting"},
]

GAMES = [
    {"title": "Stardew Valley", "genre": "Farming Sim", "levels": ["Medium", "High"], "mood": "calming"},
    {"title": "Animal Crossing: New Horizons", "genre": "Life Sim", "levels": ["Medium", "High"], "mood": "calming"},
    {"title": "Journey", "genre": "Adventure", "levels": ["Medium", "High"], "mood": "reflective"},
    {"title": "Unpacking", "genre": "Puzzle/Chill", "levels": ["Medium", "High"], "mood": "calming"},
    {"title": "A Short Hike", "genre": "Exploration", "levels": ["Low", "Medium"], "mood": "uplifting"},
    {"title": "Tetris Effect: Connected", "genre": "Puzzle", "levels": ["Low", "Medium"], "mood": "energizing"},
    {"title": "Slime Rancher", "genre": "Adventure/Sim", "levels": ["Low", "Medium"], "mood": "uplifting"},
    {"title": "Flower", "genre": "Relaxation", "levels": ["High"], "mood": "calming"},
    {"title": "Spiritfarer", "genre": "Adventure/Management", "levels": ["Medium", "High"], "mood": "reflective"},
    {"title": "Kirby and the Forgotten Land", "genre": "Platformer", "levels": ["Low", "Medium"], "mood": "uplifting"},
    {"title": "Wattam", "genre": "Puzzle/Whimsical", "levels": ["Low", "Medium"], "mood": "uplifting"},
    {"title": "Abzu", "genre": "Exploration", "levels": ["Medium", "High"], "mood": "calming"},
]

_DB = {"Movies": MOVIES, "Videos": VIDEOS, "Games": GAMES}


def get_recommendations(stress_level: str, mood: str = "any", n_per_category: int = 3):
    """
    Return a dict of {category: [items]} personalized to the stress level
    and (optionally) a preferred mood tag.

    stress_level: "Low" | "Medium" | "High"
    mood: "any" or one of calming/uplifting/comforting/reflective/energizing
    """
    results = {}
    for category, items in _DB.items():
        pool = [item for item in items if stress_level in item["levels"]]
        if mood and mood != "any":
            mood_pool = [item for item in pool if item["mood"] == mood]
            # fall back to the full level-matched pool if the mood filter is too narrow
            pool = mood_pool if len(mood_pool) >= n_per_category else pool
        random.shuffle(pool)
        results[category] = pool[:n_per_category] if pool else items[:n_per_category]
    return results


AVAILABLE_MOODS = ["any", "calming", "uplifting", "comforting", "reflective", "energizing"]
