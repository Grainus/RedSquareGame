# Copyright (c) 2022 Grainus, WyllasSidjeno, AsadPug, Phil-DB
# Licence Libre MIT

# L’autorisation est accordée, gracieusement, à toute personne acquérant une copie
# de ce logiciel et des fichiers de documentation associés (le « logiciel »), de commercialiser
# le logiciel sans restriction, notamment les droits d’utiliser, de copier, de modifier,
# de fusionner, de publier, de distribuer, de sous-licencier et / ou de vendre des copies du logiciel,
# ainsi que d’autoriser les personnes auxquelles la logiciel est fournie à le faire,
# sous réserve des conditions suivantes :
# 
# La déclaration de copyright ci-dessus et la présente autorisation doivent être incluses dans
# toutes copies ou parties substantielles du logiciel.
# 
# LE LOGICIEL EST FOURNI « TEL QUEL », SANS GARANTIE D’AUCUNE SORTE, EXPLICITE OU IMPLICITE,
# NOTAMMENT SANS GARANTIE DE QUALITÉ MARCHANDE, D’ADÉQUATION À UN USAGE PARTICULIER ET D’ABSENCE
# DE CONTREFAÇON. EN AUCUN CAS, LES AUTEURS OU TITULAIRES DU DROIT D’AUTEUR NE SERONT RESPONSABLES
# DE TOUT DOMMAGE, RÉCLAMATION OU AUTRE RESPONSABILITÉ, QUE CE SOIT DANS LE CADRE D’UN CONTRAT,
# D’UN DÉLIT OU AUTRE, EN PROVENANCE DE, CONSÉCUTIF À OU EN RELATION AVEC LE LOGICIEL OU SON UTILISATION,
# OU AVEC D’AUTRES ÉLÉMENTS DU LOGICIEL.
"""Permet d'enregistrer des scores à un fichier."""

# Documentation
from typing import Callable
from functools import partial

# Modules standard
import sqlite3 as sql
import os.path


class HighScore:
    """Interface permettant d'enregistrer et de retourner des scores
    dans un fichier de base de donnée.
    
    Ne possède que des méthodes statiques. Essayer de l'instancier
    causera une erreur.

    Méthodes:
        `HighScore.save_score`: Sauvegarde un score dans le fichier.
        `HighScore.get_scores`: Retourne une liste des scores
          enregistrés.

    Note:
        Les autres méthodes sont à usage interne. Il n'est pas
        recommandé de les utiliser.
    """
    database = os.path.join(
        os.path.dirname(__file__),
        "Data", "highscores.db",
    )

    def __init__(self):
        """Méthode explicitement interdite."""
        raise RuntimeError("This class cannot be instantiated.")

    @staticmethod
    def connect() -> sql.Connection:
        """Alias sémantique de create_db. Utiliser cette méthode est
        préférable puisque son effet voulu est plus clair.
        
        Returns:
            Une connection à la base de donnée qui peut être utilisée
              pour y exécuter des commandes.
        """
        return HighScore.create_db()

    @staticmethod
    def create_db() -> sql.Connection:
        """Crée le schema si il n'est pas présent dans le fichier.
        
        Returns:
            Une connection à la base de donnée qui peut être utilisée
              pour y exécuter des commandes.
        """
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
        """Enregistre un score dans la base de donnée.

        Args:
            name: Le nom du joueur à utiliser pour la ligne.
            score: Le nombre de secondes que le joueur a survécu.
        """
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

        exc = cur.execute(
            f"SELECT * FROM HighScores ORDER BY {order} DESC"
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
        """Supprime une ligne dans la base de donnée.
        
        Args:
            id: L'identifiant principal (PRIMARY KEY) à utiliser pour
              déterminer quelle ligne supprimer.
        """
        con = HighScore.connect()
        con.cursor().execute(
                "DELETE FROM HighScores WHERE ID = ?", (id,)
        )

        con.commit()
        con.close()
