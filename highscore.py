"""Permet d'enregistrer des scores à un fichier."""
# Documentation
from typing import Callable
from functools import partial

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
        """Alias sémantique de create_db"""
        return HighScore.create_db()

    @staticmethod
    def create_db() -> sql.Connection:
        """Crée la base de donnée si elle n'est pas présente."""
        con = sql.connect(HighScore.database)

        con.execute(f"""
            CREATE TABLE IF NOT EXISTS HighScores (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserName TEXT,
                Score INTEGER,
                Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )"""
        )
        con.commit()

        return con

    @staticmethod
    def save_score(name: str, score: int) -> None:
        con = HighScore.connect()
        con.cursor().execute(f"""
            INSERT INTO HighScores (UserName, Score)
                VALUES (?, ?) 
            """, (name, score)
        )

        con.commit()
        con.close()


    @staticmethod
    def get_scores(
            order: str = "Score"
    ) -> list[tuple[tuple[str, int], Callable[[], None]]]:
        """Retourne une liste de tuples contenant les scores (nom et
        temps) ainsi qu'une fonction qui supprime le score.

        Args:
            order: Colonne à utiliser pour l'ordre des scores. Par
              défaut, les scores les plus hauts sont en premier.
        """
        con = HighScore.connect()
        cur = con.cursor()

        exc = cur.execute(f"""
                SELECT* FROM HighScores
                ORDER BY {order} DESC
                """
        )

        result = exc.fetchall()
        # TODO: fancy zip() or itertools
        return [
            (
                tuple(res[1:3]),
                partial(HighScore.delete_score, res[0])
            )  # type: ignore  # Je sais ce que je fais
            for res in result
        ]

    @staticmethod
    def delete_score(id) -> None:
        con = HighScore.connect()
        con.cursor().execute(
                "DELETE FROM HighScores WHERE ID = ?", (id,)
        )

        con.commit()
        con.close()
