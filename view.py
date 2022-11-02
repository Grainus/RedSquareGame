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
from typing import TYPE_CHECKING, Callable

# Modules standards
from abc import ABC  # Abstract Base Class
import os.path
import tkinter as tk
from tkinter import PhotoImage

if TYPE_CHECKING:
    from game_engine import Root

from model import int_to_time


class View(ABC):
    def __init__(self, root: Root):
        self.root = root

    def set_listen(self, eventname: str, command: Callable) -> None:
        """" Fonction permettant de lier un événement à une fonction """
        self.root.bind(eventname, command)


class MenuView(View):
    def __init__(self, root: Root, on_new_game: Callable,
                 on_quit: Callable, on_options: Callable, on_highscores: Callable):
        """" Initialisation de la vue du menu """
        # Initialise la classe parente (View) pour les éléments communs
        super().__init__(root)

        # Storage des fonctions creer nouvelle partie et quitter le jeu
        self.on_new_game = on_new_game
        self.on_quit = on_quit
        self.on_options = on_options
        self.on_highscores = on_highscores
        
        # Dimensions des widgets
        self.btn_height = 100
        self.btn_width = 200
        self.logo_width = 300
        self.logo_height = 130
        # Création des boutons et des informations de la fenetre
        self.root.title("Jeu du carré rouge - Menu")
        self.root.geometry("450x450")
        
        currentdir = os.path.dirname(__file__)
        graphics = os.path.join(currentdir, "Graphics")
        buttons = os.path.join(graphics, "Buttons")
        self.title_photo = PhotoImage(
            file=os.path.join(graphics, "logo.png")
        )
        self.play_photo = PhotoImage(
            file=os.path.join(buttons, "playButton.png")
        )
        self.play_pressed_photo = PhotoImage(
            file=os.path.join(buttons, "playButtonPressed.png")
        )
        self.quit_photo = PhotoImage(
            file=os.path.join(buttons, "quitButton.png")
        )
        self.quit_pressed_photo = PhotoImage(
            file=os.path.join(buttons, "quitButtonPressed.png")
        )
        self.options_photo = PhotoImage(
            file=os.path.join(buttons, "optionsButton.png")
        )
        self.options_photo = PhotoImage(
            file=os.path.join(buttons, "optionsButton.png")
        )
        self.highscores_photo = PhotoImage(
            file=os.path.join(buttons, "highscoresButton.png")
        )
        self.title_logo = tk.Label(self.root.menu_frame, image=self.title_photo)
        self.btn_new_game = tk.Button(
            self.root.menu_frame,
            image=self.play_photo,
            width=self.btn_width, height=self.btn_height,
            borderwidth=0,
            command=self.on_new_game
        )
        self.btn_quit = tk.Button(
            self.root.menu_frame,
            image=self.quit_photo,
            width=self.btn_width, height=self.btn_height,
            borderwidth=0,
            command=self.on_quit
        )
        self.btn_options = tk.Button(
            self.root.menu_frame,
            image=self.options_photo,
            width=self.btn_width, height=self.btn_height,
            borderwidth=0,
            command=self.on_options
        )
        self.btn_highscores = tk.Button(
            self.root.menu_frame,
            image=self.highscores_photo,
            width=self.btn_width, height=self.btn_height,
            borderwidth=0,
            command=self.on_highscores
        )

    def destroy(self) -> None:
        """" Fonction appelée pour détruire le menu """
        self.root.menu_frame.destroy()

    def draw(self) -> None:
        """Fonction appelée pour dessiner le menu"""
        self.title_logo.place(x=(450-self.logo_width)/2, y=0)
        self.btn_new_game.place(x=(450-self.btn_width)/2, y=self.logo_height)
        self.btn_quit.place(
                x=(450-self.btn_width) / 2,
                y=self.logo_height + (self.btn_height*2)
        )
        self.btn_options.place(
                x=(450 - (self.btn_width*2)) / 2,
                y=self.logo_height+self.btn_height
        )
        self.btn_highscores.place(
                x=(450 - (self.btn_width*2)) / 2 + self.btn_width,
                y=self.logo_height+self.btn_height
        )
        
        
class GameView(View):
    # todo : the whole thing here ! :)
    def draw(self):
        """" Fonction appelée pour dessiner le jeu """
        self.root.game_frame.pack()

    def destroy(self):
        """" Fonction appelée pour détruire le jeu """
        self.root.game_frame.destroy()


class HighscoreView(View):
    def __init__(self, root: Root, on_quit: Callable):
        """" Initialisation de la vue des highscores """
        super().__init__(root)
        self.on_quit = on_quit
        self.highscore_canvas = tk.Canvas(self.root.highscore_frame, width=450, height=450)
        self.highscore_canvas.pack()
        self.highscore_canvas.create_text(225, 20, text="Highscores", font=("Arial", 20))

        listeScore = []  # todo : get the highscores from the database

        i = listeScore.__len__()

        if i > 15:
            i = 15
        for j in range(i):
            self.highscore_canvas.create_text(225, 50 + (j*20), text=listeScore[j], font=("Arial", 10))

        self.btn_menu = tk.Button(
            self.highscore_canvas,
            text="Menu",
            width=20, height=2,
            borderwidth=0,
            command=self.on_quit, # todo : change this to go back to the menu
            background = "blue"
        )
        self.btn_menu.place(x=150, y=350)

        self.btn_quit = tk.Button(
            self.highscore_canvas,
            text="Quitter",
            width=20, height=2,
            borderwidth=0,
            command=self.on_quit,
            background="red"
        )
        self.btn_quit.place(x=150, y=400)

    def draw(self):
        """" Fonction appelée pour dessiner les highscores """
        self.root.highscore_frame.pack()


def create_timer_widget(canvas: tk.Canvas) -> tk.Label:
    """ Créé la vue du widget et retourne son label """
    label = tk.Label(canvas, font=('Comic Sans MS', 18),
                            text=int_to_time(0), width=5, height=1,
                     border=0, relief='flat', bg='green')
    label.place(x=225, y=25, anchor="center")
    return label
