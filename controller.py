# Type hinting
from __future__ import annotations
from typing import TYPE_CHECKING

# Modules standards
from abc import ABC # Abstract Base Class

# Modules du projet
from view import MenuView, GameView

if TYPE_CHECKING:
    from game_engine import Root


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
        self.view = MenuView(root, self.new_game, self.on_quit,self.on_options,self.on_highscores)
        self.game_controller = game_controller

    def start(self) -> None:
        """Fonction appelée pour démarrer le menu"""
        self.view.draw()

    def on_options(self)->None:
        """Fonction appelée lors de l'appui sur le bouton Options"""
        pass
    
    def on_highscores(self)->None:
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
        self.view.draw()
