# Type hinting
from __future__ import annotations
from typing import TYPE_CHECKING, Callable

# Modules standards
from abc import ABC # Abstract Base Class

import tkinter as tk
from tkinter import PhotoImage,TOP

if TYPE_CHECKING:
    from game_engine import Root


class View(ABC):
    def __init__(self, root: Root):
        self.root = root

    def set_listen(self, eventname: str, command: Callable) -> None:
        """" Fonction permettant de lier un événement à une fonction """
        self.root.bind(eventname, command)


class MenuView(View):
    def __init__(self, root: Root, on_new_game: Callable,
                 on_quit: Callable,on_options : Callable,on_highscores:Callable):
        """" Initialisation de la vue du menu """
        # Initialise la classe parente (View) pour les éléments communs
        super().__init__(root)

        # Storage des fonctions creer nouvelle partie et quitter le jeu
        self.on_new_game = on_new_game
        self.on_quit = on_quit
        self.on_options= on_options
        self.on_highscores = on_highscores
        
        # Dimensions des widgets
        self.btn_height = 100
        self.btn_width = 200
        self.logo_width = 300
        self.logo_height = 130
        # Création des boutons et des informations de la fenetre
        self.root.title("Jeu du carré rouge - Menu")
        self.root.geometry("450x450")
        self.title_photo = PhotoImage(file = r"Graphics\logo.png")
        self.play_photo = PhotoImage(file = r"Graphics\Buttons\playButton.png")
        self.play_pressed_photo = PhotoImage(file = r"Graphics\Buttons\playButtonPressed.png")
        self.quit_photo = PhotoImage(file = r"Graphics\Buttons\quitButton.png")
        self.quit_pressed_photo = PhotoImage(file = r"Graphics\Buttons\quitButtonPressed.png")
        self.options_photo = PhotoImage(file = r"Graphics\Buttons\optionsButton.png")
        self.options_photo = PhotoImage(file = r"Graphics\Buttons\optionsButton.png")
        self.highscores_photo = PhotoImage(file = r"Graphics\Buttons\highscoresButton.png")
        self.title_logo = tk.Label(self.root.menu_frame,image=self.title_photo)
        self.btn_new_game = tk.Button(
            self.root.menu_frame,
            image=self.play_photo,
            width=self.btn_width,height=self.btn_height,
            borderwidth=0,
            command=self.on_new_game
        )
        self.btn_quit = tk.Button(
            self.root.menu_frame,
            image = self.quit_photo,
            width=self.btn_width, height=self.btn_height,
            borderwidth=0,
            command=self.on_quit
        )
        self.btn_options = tk.Button(
            self.root.menu_frame,
            image = self.options_photo,
            width=self.btn_width, height=self.btn_height,
            borderwidth=0,
            command=self.on_options
        )
        self.btn_highscores = tk.Button(
            self.root.menu_frame,
            image = self.highscores_photo,
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
        self.btn_quit.place(x=(450-self.btn_width)/2, y=self.logo_height+(self.btn_height*2))
        self.btn_options.place(x=(450-(self.btn_width*2))/2, y=self.logo_height+self.btn_height)
        self.btn_highscores.place(x=(450-(self.btn_width*2))/2+self.btn_width, y=self.logo_height+self.btn_height)
        
        


class GameView(View):
    # todo : the whole thing here ! :)
    def draw(self):
        """" Fonction appelée pour dessiner le jeu """
        self.root.game_frame.pack()

    def destroy(self):
        """" Fonction appelée pour détruire le jeu """
        self.root.game_frame.destroy()
