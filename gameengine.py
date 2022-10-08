import tkinter as tk
from menu.controlleur import MenuController


class Root(tk.Tk):
    def __init__(self):
        """Initialisation de la fenêtre principale -> Le menu"""
        super().__init__()
        self.title("Jeu du carré rouge")

        self.menu_frame = tk.Frame(self)
        self.menu_frame.pack()

        self.game_frame = tk.Frame(self)
        self.game_frame.pack()

        game = None  # TODO : game_controller(self.game_frame, None)
        self.menu = MenuController(self, game)


if __name__ == "__main__":
    root = Root()

    root.menu.start()
    root.mainloop()
