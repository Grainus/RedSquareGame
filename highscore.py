"""Permet d'enregistrer des scores à un fichier."""
# Documentation
from typing import Callable

# Modules standard
import sqlite3 as sql
import os.path

## TESTING
import random
names = ("Maisha", "Schneider", "Deborah"  "Burgess", "Benny", "eaver", "Kean", "Brown", "Laibah", "Rasmussen", "Jay-Jay", "Mahoney", "Lulu", "Rivers", "Kairo", "Poole", "Abdul", "Valenzuela", "Hakim", "Plant")

class HighScore:
    database = os.path.join(
        os.path.dirname(__file__),
        "Data", "highscores.db",
    )

    @staticmethod
    def connect() -> sql.Connection:
        try
            return sql.connect(HighScore.database, uri=True)
        except sql.OperationalError:
            return HighScore.create_db()

    @staticmethod
    def create_db() -> sql.Connection:
        raise NotImplementedError

    @staticmethod
    def save_score(name: str, score: int):
        con = HighScore.connect()
        cur = con.cursor()
      
        raise NotImplementedError
      
    @staticmethod
    def get_scores() -> list[tuple[tuple[str, int], Callable]:
        """Retourne une liste de tuples contenant les scores
        (nom et temps) ainsi qu'une fonction qui supprime le score
        """
        def callback():
            pass
        return [
            (
                (
                    random.choice(names),
                    random.randint(0, 100)
                ),
                callback
            )
        ]

    @staticmethod
    def delete_score(id) -> None:
        raise NotImplementedError
