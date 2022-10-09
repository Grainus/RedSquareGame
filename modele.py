from enum import Enum


class Difficulty(Enum):
    """" Enumération des difficultés de jeu """
    EASY = 1
    MEDIUM = 2  # -> Default for production
    HARD = 3
    