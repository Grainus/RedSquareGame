"""Permet d'enregistrer des scores à un fichier."""
# Documentation
from typing import Callable

# Modules standard
import sqlite3 as sql
import os.path


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
        raise NotImplementedError

    @staticmethod
    def delete_score(id) -> None:
        raise NotImplementedError
