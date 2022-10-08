from menu.vues import MenuView


class Controller:
    def __init__(self, root):
        self.root = root

    def on_quit(self) -> None:
        """Fonction appelée lors de l'appui sur le bouton Quitter
        afin de quitter le jeu"""
        self.root.destroy()


class MenuController(Controller):
    def __init__(self, root, game_controller):
        super().__init__(root)
        self.game_controller = game_controller
        self.view = MenuView(root, self.new_game, self.on_quit)

    def start(self) -> None:
        """Fonction appelée pour démarrer le menu"""
        self.view.draw()

    def new_game(self) -> None:
        """Fonction appelée lors de l'appui sur le bouton Nouvelle partie"""
        pass
        # if self.game_controller.get_new_game_request():
        # TODO
