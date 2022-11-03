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
from view import MenuView, GameView, HighscoreView, OptionsView, GameOverView
import c31Geometry.c31Geometry2 as geo
from config import Config
from model import Player, Enemy, Difficulty
from view import create_timer_widget

if TYPE_CHECKING:
    from game_engine import Root

__docformat__ = "google"

from view import create_timer_widget

class Controller(ABC):
    def __init__(self, root: Root, frame: tk.Frame):
        """Initialisation du controlleur"""
        self.root = root
        self.frame = frame

    def on_quit(self) -> None:
        """Fonction appelée lors de l'appui sur le bouton Quitter
        afin de quitter le jeu
        """
        self.root.destroy()



class MenuController(Controller):
    def __init__(self, root: Root):
        """Initialisation du controlleur du menu"""
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
        """Fonction appelée pour démarrer le menu"""
        self.view.draw()

    def on_options(self) -> None:
        """Fonction appelée pour démarrer le menu d'options"""
        self.root.menu_frame.pack_forget()
        options_controller = OptionsController(self.root)
        options_controller.start()

    def on_highscores(self) -> None:
        """Fonction appelée lors de l'appui sur le bouton Highscores
        afin d'afficher le tableau des highscores
        """
        self.frame.pack_forget()
        frame = tk.Frame(self.root)
        highscore_controller = HighscoreController(self.root, frame)
        highscore_controller.start()

    def new_game(self) -> None:
        """Fonction appelée lors de l'appui sur le bouton Nouvelle Partie
        afin de démarrer une nouvelle partie
        """
        self.frame.destroy()
        frame = tk.Frame(self.root)
        game_controller = GameController(self.root, frame)
        game_controller.initialize()


class GameController(Controller):
    def __init__(self, root: Root, frame: tk.Frame):
        """Initialisation du controlleur du jeu"""
        super().__init__(root, frame)
        self.view = GameView(root, frame)

    def initialize(self) -> None:
        """Fonction appelée pour démarrer une nouvelle partie"""
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
        """Commence le mouvement des éléments du jeu."""
        self.player.canvas.tag_unbind(self.player.sprite, "<Button-1>")
        self.player.score.start()
        
        for enemy in self.enemies:
            enemy.start_move()
        

    def on_game_end(self) -> None:
        self.frame.destroy()
        print("You died")
        print(f"Your score: {self.player.score.value}")
        #self.root.score_controller.start()


class HighscoreController(Controller):
    def __init__(self, root: Root, frame: tk.Frame):
        """Initialisation du controlleur du tableau des highscores"""
        super().__init__(root, frame)
        self.view = HighscoreView(
            root, frame,
            self.on_quit, self.on_menu
        )

    def start(self) -> None:
        """Fonction appelée pour démarrer le tableau des highscores"""
        self.view.draw()

    def on_menu(self) -> None:
        self.root.highscore_frame.pack_forget()
        self.root.menu_frame.pack()

class OptionsController(Controller):
    def __init__(self, root: Root):
        """Initialisation du controlleur des options"""
        super().__init__(root)
        self.view = OptionsView(root, self.on_quit,self.on_menu)

    def start(self) -> None:
        self.view.draw()

    def on_menu(self) -> None:
        self.root.options_frame.pack_forget()
        self.root.menu_frame.pack()

class GameOverController(Controller):
    def __init__(self, root: Root):
        """Initialisation du controlleur du menu game over"""
        super().__init__(root)
        self.view = GameOverView(root, self.on_quit,self.on_menu)

    def start(self) -> None:
        self.view.draw()

    def on_menu(self) -> None:
        self.root.options_frame.pack_forget()
        self.root.menu_frame.pack()
