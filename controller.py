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
"""TODO: DOCSTRING"""

# Type hinting
from __future__ import annotations
from typing import TYPE_CHECKING

# Modules standards
from abc import ABC  # Abstract Base Class
import tkinter as tk

# Modules du projet
from view import MenuView, GameView, HighscoreView
import c31Geometry.c31Geometry2 as geo
from config import Config

if TYPE_CHECKING:
    from game_engine import Root

from model import Player, Enemy, collider

from model import int_to_time
from view import create_timer_widget


class Controller(ABC):
    def __init__(self, root: Root):
        """Initialisation du controlleur"""
        self.root = root

    def on_quit(self) -> None:
        """Fonction appelée lors de l'appui sur le bouton Quitter
        afin de quitter le jeu
        """
        self.root.destroy()


class MenuController(Controller):
    def __init__(self, root: Root, game_controller: GameController):
        """Initialisation du controlleur du menu"""
        super().__init__(root)
        self.view = MenuView(
                root, self.new_game, self.on_quit,
                self.on_options, self.on_highscores
        )
        self.game_controller = game_controller

    def start(self) -> None:
        """Fonction appelée pour démarrer le menu"""
        self.view.draw()

    def on_options(self) -> None:
        pass

    def on_highscores(self) -> None:
        """Fonction appelée lors de l'appui sur le bouton Highscores
        afin d'afficher le tableau des highscores
        """
        self.root.menu_frame.destroy()
        highscore_controller = HighscoreController(self.root)
        highscore_controller.start()

    def new_game(self) -> None:
        """Fonction appelée lors de l'appui sur le bouton Nouvelle Partie
        afin de démarrer une nouvelle partie
        """
        self.root.menu_frame.destroy()
        self.game_controller.start()


class GameController(Controller):
    def __init__(self, root: Root):
        """Initialisation du controlleur du jeu"""
        super().__init__(root)
        self.view = GameView(root)

    def start(self) -> None:
        """Fonction appelée pour démarrer une nouvelle partie"""
        config = Config.get_instance()

        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.game_frame.place(anchor=tk.CENTER)
        self.view.draw()
        canvas = tk.Canvas(
            self.root.game_frame,
            width=width,
            height=height,
            background=config["Game"]["Color"]["Fill"],
        )
        timer_widget = create_timer_widget(canvas)

        canvas.pack()
        self.root.game_frame.update()
        ############################### TESTING ###############################
        firstEnemy = config["Enemies"][0]
        pos = firstEnemy["Position"]
        speed = firstEnemy["Speed"]
        size = firstEnemy["Size"]

        enemy = Enemy(
            canvas,
            pos=geo.Point(pos["X"], pos["Y"]),
            width=size["Width"], height=size["Height"],
            speed=geo.Vecteur(speed["X"], speed["Y"]),
        )
        ############################### TESTING ###############################
        player = Player(
                canvas,
                enemy=enemy,
                start_timer=start_timer,
                timer_widget=timer_widget
        )
        self.view.draw()
        print("Game started")

    def on_game_end(self) -> None:
        self.root.game_frame.destroy()
        self.root.score_controller.start()


class HighscoreController(Controller):
    def __init__(self, root: Root):
        """Initialisation du controlleur du tableau des highscores"""
        super().__init__(root)
        self.view = HighscoreView(root, self.on_quit)

    def start(self) -> None:
        """Fonction appelée pour démarrer le tableau des highscores"""
        self.view.draw()


def start_timer(label: tk.Label, time : int) -> None:
    """ Debute la boucle du timer qui sera par la suite gérée par update_timer """
    # Start at 1 second to avoid a 1 second delay before the timer starts
    label.after(1000, update_timer, label, time)
    # 1000ms = 1s


def update_timer(time_label: tk.Label, time: int):
    """ Met a jour le label du timer et relance la fonction après 1s """
    time += 1
    time_label.config(text=int_to_time(time))
    time_label.after(1000, update_timer, time_label, time)
