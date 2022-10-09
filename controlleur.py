from abc import ABC # Abstract Base Class
import tkinter as tk

from vues import MenuView, GameView


class Controller(ABC):
    def __init__(self, root: tk.Tk):
        """Initialisation du controlleur"""
        self.root = root

    def on_quit(self) -> None:
        """Fonction appelée lors de l'appui sur le bouton Quitter
        afin de quitter le jeu
        """
        self.root.destroy()


class MenuController(Controller):
    def __init__(self, root: tk.Tk, game_controller: Controller):
        """Initialisation du controlleur du menu"""
        super().__init__(root)
        self.view = MenuView(root, self.new_game, self.on_quit)
        self.game_controller = game_controller

    def start(self) -> None:
        """Fonction appelée pour démarrer le menu"""
        self.view.draw()

    def new_game(self) -> None:
        """Fonction appelée lors de l'appui sur le bouton Nouvelle Partie
        afin de démarrer une nouvelle partie
        """
        self.root.menu_frame.destroy()
        self.game_controller.start()


class GameController(Controller):
    def __init__(self, root: tk.Tk):
        """Initialisation du controlleur du jeu"""
        super().__init__(root)
        self.view = GameView(root)

    def start(self) -> None:
        """Fonction appelée pour démarrer une nouvelle partie"""
        self.view.draw()
