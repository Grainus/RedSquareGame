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
from view import MenuView, GameView

if TYPE_CHECKING:
    from game_engine import Root

from model import Player, Enemy, collider


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
        self.view = MenuView(root, self.new_game, self.on_quit,
                             self.on_options, self.on_highscores)
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
    
    def new_game(self) -> None:
        """Fonction appelée lors de l'appui sur le bouton Nouvelle Partie
        afin de démarrer une nouvelle partie
        """
        self.root.menu_frame.destroy()
        self.game_controller.start()


class GameController(Controller):
    # todo : the whole thing here ! :)
    def __init__(self, root: Root):
        """Initialisation du controlleur du jeu"""
        super().__init__(root)
        self.view = GameView(root)

    def start(self) -> None:
        """Fonction appelée pour démarrer une nouvelle partie"""
        width = height = 450
        border = 50
        playersize = 50
        canvas = tk.Canvas(
            self.root,
            width=width,
            height=height,
        )
        canvas.pack()
        self.root.update()
        # player = Player(
        #     canvas,
        #     border,
        #     (width - playersize) / 2, (height - playersize) / 2,
        #     (width + playersize) / 2, (height + playersize) / 2,
        #     "red"
        # )
        # ############################## TESTING ###############################
        import c31Geometry.c31Geometry2 as Geo  # type: ignore                 #
        enemy = Enemy(                                                        #
            canvas, Geo.Point(100, 100), 75, 150, "blue", Geo.Vecteur(1, 1)   #
        )                                                                     #
        player = Player(canvas, border, playersize, playersize, "red", enemy)  #
        # ############################## TESTING ###############################
        self.view.draw()
