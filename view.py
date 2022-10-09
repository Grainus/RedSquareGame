from abc import ABC # Abstract Base Class
from typing import Callable

import tkinter as tk



class View(ABC):
    def __init__(self, root):
        self.root = root

    def set_listen(self, eventname: str, command: Callable):
        """" Fonction permettant de lier un événement à une fonction """
        self.root.bind(eventname, command)


class MenuView(View):
    def __init__(self, root, on_new_game: Callable,
                 on_quit: Callable):
        """" Initialisation de la vue du menu """
        # Initialise la classe parente (View) pour les éléments communs
        super().__init__(root)

        # Storage des fonctions creer nouvelle partie et quitter le jeu
        self.on_new_game = on_new_game
        self.on_quit = on_quit

        # Création des boutons et des informations de la fenetre
        self.root.title("Jeu du carré rouge - Menu")
        self.root.geometry("900x600")
        self.btn_new_game = tk.Button(self.root.menu_frame, text='New game',
                                      command=self.on_new_game,
                                      width=20, height=5,
                                      font=('Helvetica', 20),
                                      bg='green', fg='white')

        self.btn_quit = tk.Button(self.root.menu_frame, text='Quit',
                                  command=self.on_quit,
                                  width=20, height=5,
                                  font=('Helvetica', 20),
                                  bg='red', fg='white'
                                  )

    def destroy(self):
        """" Fonction appelée pour détruire le menu """
        self.root.menu_frame.destroy()

    def draw(self) -> None:
        """Fonction appelée pour dessiner le menu"""
        self.btn_new_game.pack()
        self.btn_quit.pack()


class GameView(View):
    # todo : the whole thing here ! :)
    def draw(self):
        """" Fonction appelée pour dessiner le jeu """
        self.root.game_frame.pack()

    def destroy(self):
        """" Fonction appelée pour détruire le jeu """
        self.root.game_frame.destroy()
