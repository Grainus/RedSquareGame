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
"""
#Fichier principal des controlleurs du jeu

Ce fichier contient les controlleurs du jeu.
Controlleurs:
    - La superclasse des controlleurs
    - La classe MenuController qui gère le menu
    - GameController qui gère le jeu
    - HighscoreController qui gère la vue du highscore déjà enregistré
"""

# Type hinting
from __future__ import annotations
from typing import TYPE_CHECKING

# Modules standards
from abc import ABC  # Abstract Base Class
import tkinter as tk

# Modules du projet
from view import MenuView, GameView, HighscoreView, GameEndView
import c31Geometry.c31Geometry2 as geo
from config import Config
from highscore import HighScore

if TYPE_CHECKING:
    from game_engine import Root

from model import Player, Enemy

from view import create_timer_widget

__docformat__ = "google"


class Controller(ABC):
    """#Classe abstraite des controlleurs

    Cette classe abstraite est la superclasse des controlleurs. Elle contient les méthodes et valeurs communes à tous
    les controlleurs.

    Attributs:
        - root (Root): La fenêtre principale du jeu
        - frame (tk.Frame): Le frame dans lequel le controlleur est affiché
    """
    def __init__(self, root: Root, frame: tk.Frame):
        """"""""
        self.root = root
        self.frame = frame

    def on_quit(self) -> None:
        """##Fonction appelée lors de l'appui sur le bouton Quitter afin de quitter le jeu
        """
        self.root.destroy()


class MenuController(Controller):
    """#Controlleur du menu

    Cette classe gère le menu du jeu. Elle est une sous-classe de Controller.
    Sa responsabilité est de gérer les boutons du menu ainsi que les événements
    reliées à ceux-ci.

    Attributs:
        - view (MenuView): La vue du menu
        - root (Root): La fenêtre principale du jeu
        - frame (tk.Frame): Le frame dans lequel le controlleur est affiché
        - root (Root): La fenêtre principale du jeu
        - frame (tk.Frame): Le frame dans lequel le controlleur est affiché
            -> Qui a une taille égale à la taille de la fenêtre principale
        """
    def __init__(self, root: Root):
        """"""""
        config = Config.get_instance()
        frame = tk.Frame(
                root,
                width=config["Game"]["Size"]["Width"],
                height=config["Game"]["Size"]["Height"],
        )
        
        super().__init__(root, frame)
        self.frame.place(x=0, y=0)
        self.view = MenuView(
                root, self.frame,
                self.new_game, self.on_quit,
                self.on_options, self.on_highscores
        )

    def start(self) -> None:
        """##Fonction appelée pour démarrer le menu"""
        self.view.draw()

    def on_options(self) -> None:
        """##Fonction appelée lors de l'appui sur le bouton Options afin d'afficher la vue des options
        """
        pass

    def on_highscores(self) -> None:
        """##Fonction appelée lors de l'appui sur le bouton Highscores afin d'afficher le tableau des highscores
        """
        self.frame.destroy()
        frame = tk.Frame(self.root)
        highscore_controller = HighscoreController(self.root, frame)
        highscore_controller.start()

    def new_game(self) -> None:
        """##Fonction appelée lors de l'appui sur le bouton Nouvelle Partie afin de démarrer une nouvelle partie
        """
        self.frame.destroy()
        frame = tk.Frame(self.root)
        game_controller = GameController(self.root, frame)
        game_controller.initialize()


class GameController(Controller):
    """#Controlleur du jeu

    Cette classe gère le jeu. Elle est une sous-classe de Controller. Sa responsabilité est de gérer les événements du
    jeu ainsi que les interactions entre les différents objets du jeu.

    Attributs:
        - view (GameView): La vue du jeu
        - player (Player): Le joueur
        - enemies (list[Enemy]): La liste des ennemis
        - root (Root): La fenêtre principale du jeu
        - frame (tk.Frame): Le frame dans lequel le controlleur est affiché
    """
    def __init__(self, root: Root, frame: tk.Frame):
        """"""
        super().__init__(root, frame)
        self.view = GameView(root, frame)

    def initialize(self) -> None:
        """##Fonction appelée pour démarrer une nouvelle partie

        Cette fonction initialise les objets du jeu et les affiche
        Elle est appelée lors de l'appui sur le bouton Nouvelle Partie

        Initalise:
            - Le joueur
            - Les ennemis
            - Le timer
        """
        config = Config.get_instance()

        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.frame.place(anchor=tk.CENTER)
        self.view.draw()
        canvas = tk.Canvas(
            self.frame,
            width=width,
            height=height,
            background=config["Game"]["Color"]["Fill"],
        )
        timer_widget = create_timer_widget(canvas)

        canvas.pack()
        self.frame.update()
        
        # Crée le joueur
        self.player = Player(
                canvas,
                timer_widget=timer_widget,
                endgame=self.on_game_end
        )
        
        self.enemies: list[Enemy] = []
        for enemy in config["Enemies"]:
            
            pos = enemy["Position"]
            speed = enemy["Speed"]
            size = enemy["Size"]

            self.enemies.append(
                Enemy(
                    canvas,
                    pos=geo.Point(pos["X"], pos["Y"]),
                    width=size["Width"], height=size["Height"],
                    speed=geo.Vecteur(speed["X"], speed["Y"]),
                    player=self.player
                )
            )
        
        self.player.canvas.tag_bind(
            self.player.sprite, "<Button-1>", self.start
        )
        self.view.draw()
    
    def start(self, _) -> None:
        """##Commence le mouvement des éléments du jeu.

        Cette fonction est appelée lors du premier clic sur le joueur

        Attributs:
           - _ (tk.Event): L'événement qui a appelé la fonction
        ."""
        self.player.canvas.tag_unbind(self.player.sprite, "<Button-1>")
        self.player.score.start()
        
        for enemy in self.enemies:
            enemy.start_move()

    def on_game_end(self) -> None:
        """##Fonction appelée lorsque la partie est terminée afin d'afficher le menu de score et de sauvegarder le
        score """
        self.frame.destroy()
        self.root.controller = GameEndController(self.root, self.player.score.value)


class GameEndController(Controller):
    """#Controlleur de fin de partie
    
    Cette classe gère la fin de partie. Elle est une sous-classe de Controller. Sa responsabilité est de gérer les événements
    de fin de partie ainsi que les interactions entre les différents objets de fin de partie.
    Tel:
    - Afficher le menu de fin de partie
    - Sauvegarder le score, si le joueur entre un nom et appuie sur entrer.
        - Afficher le tableau des highscores
    - Afficher le menu principal, si le boutton est pressé.
    - Afficher le menu des options, si le boutton est pressé.

    Attributs:
        - view (GameEndView): La vue de fin de partie
        - root (Root): La fenêtre principale du jeu
        - frame (tk.Frame): Le frame dans lequel le controlleur est affiché
        - score (int): Le score du joueur
    """
    def __init__(self, root: Root, score: int):
        """"""
        super().__init__(root, tk.Frame(root))
        self.score = score
        self.view = GameEndView(root, score)
        self.root.title("Game Over")
        self.view.draw()
        self.initialize()

    def initialize(self) -> None:
        """##Fonction appelée pour initialiser le controlleur de fin de partie

        Cette fonction initialise les événements du controlleur de fin de partie
        """
        self.view.nameEntry.bind("<Return>", self.on_submit)
        self.view.nameEntry.focus_set()
        self.view.btn_menu.bind("<Button-1>", self.on_menu)

    def on_submit(self, _) -> None:
        """##Fonction appelée lorsque le joueur appuie sur Entrée pour valider son nom"""
        name = self.view.nameEntry.get()  # Prend le nom du joueur
        if name:  # Si le nom n'est pas vide
            self.view.destroy()
            HighScore.save_score(name, self.score)
            self.root.HighscoreController = HighscoreController(self.root, self.frame)
            self.root.HighscoreController.start()

    def on_menu(self, _) -> None:
        """##Fonction appelée lorsque le joueur appuie sur le bouton Menu afin de revenir au menu"""
        self.view.destroy()
        self.root.controller = MenuController(self.root)
        self.root.controller.start()


class HighscoreController(Controller):
    """#Controlleur du tableau des highscores

    Cette classe gère le tableau des highscores. Elle est une sous-classe de
    Controller. Sa responsabilité est de gérer les événements du tableau des
    highscores ainsi que les interactions entre l'utilisateur, le talbeau
    et le fichier de sauvegarde

    Attributs:
        - root (Root): La fenêtre principale du jeu
        - frame (tk.Frame): Le frame dans lequel le controlleur est affiché
            -> Qui a une taille égale à la taille de la fenêtre principale
        - view (HighscoreView): La vue du tableau des highscores
    """
    def __init__(self, root: Root, frame: tk.Frame):
        """"""
        super().__init__(root, frame)
        self.view = HighscoreView(root, frame, self.on_quit)

    def start(self) -> None:
        """##Fonction appelée pour démarrer le tableau des highscores"""
        self.view.draw()
