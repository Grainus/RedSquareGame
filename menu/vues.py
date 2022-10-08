import tkinter as tk


class MenuView:
    def __init__(self, root, on_new_game, on_quit):
        self.root = root
        self.on_new_game = on_new_game
        self.on_quit = on_quit
        self.btn_new_game = tk.Button(self.root, text='New game',
                                      command=self.on_new_game,
                                      width=20, height=5,
                                      font=('Helvetica', 20),
                                      bg='green', fg='white')

        self.btn_quit = tk.Button(self.root, text='Quit',
                                  command=self.on_quit,
                                  width=20, height=5,
                                  font=('Helvetica', 20),
                                  bg='red', fg='white'
                                  )

    def draw(self) -> None:
        """Fonction appelée pour dessiner le menu"""

        self.root.title("Jeu du carré rouge - Menu")
        self.root.geometry("900x600")

        self.btn_new_game.pack()
        self.btn_quit.pack()
