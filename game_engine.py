import tkinter as tk
from turtle import back
from controller import MenuController, GameController


class Root(tk.Tk):
    def __init__(self):
        """Initialisation du root"""
        super().__init__()
        self.title("Jeu du carré rouge")

        self.menu_frame = tk.Frame(self, height=450,width=450)
        self.menu_frame.place(x=0,y=0)

        self.game_frame = tk.Frame(self)

        self.game_controller = GameController(self)
        self.menu = MenuController(self, self.game_controller)


if __name__ == "__main__":
    root = Root()

    root.menu.start()
    root.mainloop()
