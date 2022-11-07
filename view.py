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
"""#Module de la vue
Ce module contient les classes et fonctions nécessaires à la création de la vue

Classe:
    - View : Classe abstraite de la vue
    - MenuView : Classe de la vue du menu
    - GameView : Classe de la vue du jeu
    - HighscoreView : Classe de la vue des highscores

Et des fonctions de vue

Fonctions:
    - create_timer_widget : Fonction de création du widget du timer

Notes:
    - Les classes de la vue sont des classes filles de la classe abstraite View
"""

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

from model import Score, Difficulty
from config import Config
from highscore import HighScore

__docformat__ = "google"


class View(ABC):
    """#Classe abstraite de la vue

    Cette classe est une classe abstraite qui contient les attributs et méthodes
    communes à toutes les vues du jeu.

    Attributs:
        - root (Root): Instance du root
        - frame (tk.Frame): Frame de la vue
        """
    def __init__(self, root: Root, frame: tk.Frame):
        self.root = root
        self.frame = frame

    def set_listen(self, eventname: str, command: Callable) -> None:
        """##Fonction permettant de lier un événement à une fonction

        Args:
            - eventname (str): Nom de l'événement
            - command (Callable): Fonction à appeler
            """
        self.root.bind(eventname, command)

    def destroy(self):
        """##Fonction appelée pour détruire la vue"""
        self.frame.destroy()


class MenuView(View):
    """#Classe de la vue du menu

    Cette classe est une classe fille de la classe View qui contient les attributs et méthodes
    spécifiques à la vue du menu du jeu.

    Attributs:
        - root (Root): Instance du root
        - frame (tk.Frame): Frame de la vue
        - on_new_game (Callable): Fonction à appeler lors du clic sur le bouton Nouvelle partie
        - on_quit (Callable): Fonction à appeler lors du clic sur le bouton Quitter
        - on_options (Callable): Fonction à appeler lors du clic sur le bouton Options
        - on_highscores (Callable): Fonction à appeler lors du clic sur le bouton Highscores
        - btn_width (int): Largeur des boutons
        - btn_height (int): Hauteur des boutons
        - logo_width (int): Largeur du logo
        - logo_height (int): Hauteur du logo
        - title_logo (tk.Label): Label du logo
        - label_title (tk.Label): Label du titre
        - btn_new_game (tk.Button): Bouton Nouvelle partie
        - btn_quit (tk.Button): Bouton Quitter
        - btn_options (tk.Button): Bouton Options
        - btn_highscores (tk.Button): Bouton Highscores
        """
    def __init__(
            self, root: Root, frame: tk.Frame,
            on_new_game: Callable,
            on_quit: Callable,
            on_options: Callable,
            on_highscores: Callable
    ):
        """"""
        # Initialise la classe parente (View) pour les éléments communs
        super().__init__(root, frame)

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
        # Photos des widgets
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
        
        def create_btn(image: PhotoImage, cmd: Callable) -> tk.Button:
            """##Fonction de création d'un bouton

            Args:
                - image (PhotoImage): Image du bouton
                - cmd (Callable): Fonction à appeler lors du clic sur le bouton

            Retourne:
                - tk.Button: Bouton créé
            """
            return tk.Button(
                    self.frame,
                    image=image,
                    width=self.btn_width, height=self.btn_height,
                    borderwidth=0,
                    command=cmd
            )
        
        self.title_logo = tk.Label(
            self.frame, image=self.title_photo
        )
        self.btn_new_game = create_btn(
            self.play_photo, self.on_new_game
        )
        self.btn_quit = create_btn(
            self.quit_photo, self.on_quit
        )
        self.btn_options = create_btn(
            self.options_photo, self.on_options
        )
        self.btn_highscores = create_btn(
            self.highscores_photo, self.on_highscores
        )

    def draw(self) -> None:
        """##Fonction appelée pour dessiner le menu"""
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
    """"#Classe de la vue du jeu

    Cette classe est une classe fille de la classe View. Elle contient les méthodes
    et attributs spécifiques à la vue du jeu.

    Attributs:
        - root (Root): Instance du root
        - frame (tk.Frame): Frame de la vue
        - on_quit (Callable): Fonction à appeler lors du clic sur le bouton Quitter"""
    def draw(self):
        """##Fonction appelée pour dessiner le jeu"""
        self.frame.pack()


class HighscoreView(View):
    """#Classe de la vue des highscores

    Cette classe est une classe fille de la classe View. Elle contient les méthodes
    et attributs spécifiques à la vue des highscores.

    Attributs:
        - root (Root): Instance du root
        - frame (tk.Frame): Frame de la vue
        - on_quit (Callable): Fonction à appeler lors du clic sur le bouton Quitter"""
    def __init__(
                self, root: Root,
                frame: tk.Frame,
                on_quit: Callable,
                on_menu: Callable
        ):
        """"""
        super().__init__(root, frame)
        size = Config.get_instance()["Game"]["Size"]

        self.on_quit = on_quit
        self.on_menu = on_menu
        self.highscore_canvas = tk.Canvas(
            self.frame,
            width=size["Width"], height=size["Height"]
        )
        self.highscore_canvas.pack()
        self.highscore_canvas.label = tk.Label(
            self.highscore_canvas,
            text="Highscores",
            font=("Arial", 50)
        )
        self.highscore_canvas.label.place(anchor="center", relx=0.5, rely=0.1)

        self.highscore_canvas.listBox = tk.Listbox(
            self.highscore_canvas,
            width=30, height=15, selectmode="single",
        )
        scrollbar = tk.Scrollbar(
            self.highscore_canvas.listBox,
            orient="vertical",
            command=self.highscore_canvas.listBox.yview
        )

        self.highscore_canvas.listBox.config(yscrollcommand=scrollbar.set)
        self.highscore_canvas.listBox.place(
            anchor="center", relx=0.5, rely=0.45
        )

        scrollbar.place(
            anchor="center", relx=0.9, rely=0.5, relheight=1
        )

        self.callbacks: list[Callable[[], None]] = []
        for score, callback in HighScore.get_scores():
            self.highscore_canvas.listBox.insert(
                    "end", f"{score[0]} : {Score.to_readable(score[1])}"
            )
            self.callbacks.append(callback)

        # Put a scrolling box for the score underneath the canvas's text

        # Dimensions des widgets
        self.btn_height = size["Height"] / 4,5
        self.btn_width = 2 * self.btn_height

        currentdir = os.path.dirname(__file__)
        graphics = os.path.join(currentdir, "Graphics")
        buttons = os.path.join(graphics, "Buttons")

        self.quit_photo = PhotoImage(
            file=os.path.join(buttons, "quitButton.png")
        )
        self.menu_photo = PhotoImage(
            file=os.path.join(buttons, "menuButton.png")
        )
        # Initialization des boutons
        def create_btn(image: PhotoImage, cmd: Callable) -> tk.Button:
            return tk.Button(
                    self.highscore_canvas,
                    image=image,
                    width=self.btn_width, height=self.btn_height,
                    borderwidth=0,
                    command=cmd
            )

        self.btn_menu = create_btn(self.menu_photo, self.on_menu)
        self.btn_quit = create_btn(self.quit_photo, self.on_quit)
        
        # Positionnement des widgets
        self.btn_menu.place(
            x=(size["Width"] - (self.btn_width*2)) / 2,
            y=size["Height"] - self.btn_height
        )
        self.btn_quit.place(
            x=(size["Width"] - (self.btn_width*2)) / 2 + self.btn_width,
            y=size["Height"] - self.btn_height
        )
        
        self.btn_quit.place(x=1/3, rely=8/9)
        self.initialize()

    def draw(self):
        """##Fonction appelée pour dessiner les highscores"""
        self.frame.pack()

    def initialize(self):
        """##Fonction appelée pour initialiser les highscores"""
        # Event listener for each element inside the listbox
        self.highscore_canvas.listBox.bind(
            "<<ListboxSelect>>", self.on_select
        )

    def on_select(self, event):
        """##Fonction appelée lors de la sélection d'un élément dans la liste.

        Elle doit pouvoir supprimer un element de la liste ainsi que de se supprimer
        elle meme grace a sa fonction partielle. """
        # Get the index of the selected item
        if self.highscore_canvas.listBox.curselection():
            index = self.highscore_canvas.listBox.curselection()[0]
            # Get the value of the selected item
            value = self.highscore_canvas.listBox.get(index)
            # Delete the selected item from the listbox
            self.highscore_canvas.listBox.delete(index)
            # Delete the selected item from the file
            self.callbacks[index]()

class GameEndView(View):
    """#Classe de la vue de fin de jeu

    Cette classe est une classe fille de la classe View. Elle contient les méthodes
    et attributs spécifiques à la vue de fin de jeu.

    On y créera aussi les attributs spécifiques à la vue de fin de jeu
    Bouton:
        - btn_menu (tk.Button): Bouton pour revenir au menu
        - btn_quit (tk.Button): Bouton pour quitter le jeu
    Entry:
        - entry (tk.Entry): Entry pour entrer son nom

    Attributs:
        - root (Root): Instance du root
        - frame (tk.Frame): Frame de la vue
        - on_quit (Callable): Fonction à appeler lors du clic sur le bouton Quitter
    """
    def __init__(self, root: Root, scorevalue: int):
        """"""
        super().__init__(root, tk.Frame(root))
        self.scoreValue = scorevalue
        size = Config.get_instance()["Game"]["Size"]
        self.game_over_canvas = tk.Canvas(
            self.frame,
            width=size["Width"], height=size["Height"]
        )
        self.game_over_canvas.pack()
        self.game_over_canvas.create_text(
            225, 20,
            text="Game Over - Vous avez perdu",
            font=("Arial", 20)
        )
        self.game_over_canvas.create_text(
            225, 70,
            text="Score :" + str(self.scoreValue),
            font=("Arial", 15)
        )

        self.game_over_canvas.create_text(
            225, 95,
            text= "Quel est votre nom ? (Appuyez sur entrer pour confirmer)",
            font=("Arial", 10)
        )

        self.nameEntry = tk.Entry(self.game_over_canvas)
        self.nameEntry.place(relx=1/3, rely=1/3.75)
        self.nameEntry.focus_set()

        # Dimensions des widgets
        self.btn_height = size["Height"] / 4,5
        self.btn_width = 2 * self.btn_height

        currentdir = os.path.dirname(__file__)
        graphics = os.path.join(currentdir, "Graphics")
        buttons = os.path.join(graphics, "Buttons")

        self.quit_photo = PhotoImage(
            file=os.path.join(buttons, "quitButton.png")
        )
        self.menu_photo = PhotoImage(
            file=os.path.join(buttons, "menuButton.png")
        )
        # Initialization des boutons
        def create_btn(image: PhotoImage, cmd: Callable) -> tk.Button:
            return tk.Button(
                    self.game_over_canvas,
                    image=image,
                    width=self.btn_width, height=self.btn_height,
                    borderwidth=0,
                    command=cmd
            )

        self.btn_menu = create_btn(self.menu_photo, self.on_menu)
        self.btn_quit = create_btn(self.quit_photo, self.on_quit)
        
        # Positionnement des widgets
        self.btn_menu.place(
            x=(size["Width"] - (self.btn_width*2)) / 2,
            y=size["Height"] - self.btn_height
        )
        self.btn_quit.place(
            x=(size["Width"] - (self.btn_width*2)) / 2 + self.btn_width,
            y=size["Height"] - self.btn_height
        )

    def draw(self):
        """##Fonction appelée pour dessiner la vue de fin de jeu"""
        self.frame.pack()

class OptionsView(View):
    def __init__(
                self, root: Root, frame: tk.Frame,
                on_quit: Callable,
                on_menu:Callable
        ):
        """ Initialisation de la vue des options """
        super().__init__(root, frame)
        size = Config.get_instance()["Game"]["Size"]
        self.on_quit = on_quit
        self.on_menu = on_menu
        self.options_canvas = tk.Canvas(self.frame, width=size["Width"], height=size["Height"])
        self.options_canvas.pack()
        self.options_canvas.create_text(225, 35, text="Options", font=("Arial", 50))

        # Dimensions des widgets
        self.btn_height = size["Height"] / 4.5
        self.btn_width = self.btn_height * 2
        self.diff_height = self.btn_height / 2
        self.diff_width = self.diff_height * 2


        currentdir = os.path.dirname(__file__)
        graphics = os.path.join(currentdir, "Graphics")
        buttons = os.path.join(graphics, "Buttons")

        # Photos des widgets
        self.quit_photo = PhotoImage(
            file=os.path.join(buttons, "quitButton.png")
        )
        self.menu_photo = PhotoImage(
            file=os.path.join(buttons, "menuButton.png")
        )
        self.easy_photo = PhotoImage(
            file=os.path.join(buttons, "easyButton.png")
        )
        self.medium_photo = PhotoImage(
            file=os.path.join(buttons, "mediumButton.png")
        )
        self.hard_photo = PhotoImage(
            file=os.path.join(buttons, "hardButton.png")
        )

        # Initialization des boutons
        def create_btn(image: PhotoImage, cmd: Callable) -> tk.Button:
            return tk.Button(
                    self.options_canvas,
                    image=image,
                    width=self.btn_width, height=self.btn_height,
                    borderwidth=0,
                    command=cmd
            )
            
        def diff_btn(image: PhotoImage, diff: Difficulty) -> tk.Button:
            def change_diff():
                config = Config.get_instance()
                config["Game"]["Difficulty"]["Level"] = diff.name
                config.save()
            
            return tk.Button(
                    self.options_canvas,
                    image=image,
                    width=self.diff_width, height=self.diff_height,
                    borderwidth=0,
                    command=change_diff
            )
        
        self.btn_menu = create_btn(self.menu_photo, self.on_menu)
        self.btn_quit = create_btn(self.quit_photo, self.on_quit)
        self.btn_easy = diff_btn(self.easy_photo, Difficulty.EASY)
        self.btn_medium = diff_btn(self.medium_photo, Difficulty.MEDIUM)
        self.btn_hard = diff_btn(self.hard_photo, Difficulty.HARD)
        
        # Positionnement des widgets
        self.btn_menu.place(
            x=(size["Width"] - (self.btn_width*2)) / 2,
            y=size["Height"] - self.btn_height
        )
        self.btn_quit.place(
            x=(size["Width"] - (self.btn_width*2)) / 2 + self.btn_width,
            y=size["Height"] - self.btn_height
        )
        self.btn_easy.place(
            x=(size["Width"] - self.diff_width) / 2,
            y=size["Height"]/2 - (self.diff_height*2)
        )
        self.btn_medium.place(
            x=(size["Width"] - self.diff_width) / 2,
            y=size["Height"]/2 - self.diff_height
        )
        self.btn_hard.place(
            x=(size["Width"] - self.diff_width) / 2,
            y=size["Height"]/2
        )

    def draw(self):
        self.frame.pack()


def create_timer_widget(canvas: tk.Canvas) -> tk.Label:
    """#Créé la vue du widget et retourne son label

    Args:
        - canvas (tk.Canvas): Canvas sur lequel dessiner le widget

    Retourne:
        - tk.Label: Label du widget
        """
    label = tk.Label(
        canvas, font=('Comic Sans MS', 18),
        text=Score.to_readable(0), width=5, height=1,
        border=0, relief='flat', bg='black', fg='white'
    )
    label.place(x=225, y=25, anchor="center")
    return label

class GameOverView(View):
    def __init__(
                self, root: Root, frame: tk.Frame,
                on_quit: Callable,
                on_menu:Callable,
                on_input:Callable
        ):
        super().__init__(root, frame)
        size = Config.get_instance()["Game"]["Size"]
        self.game_over_canvas = tk.Canvas(
            self.frame,
            width=size["Width"], height=size["Height"]
        )
        self.game_over_canvas.pack()
        self.game_over_canvas.create_text(
            225, 50,
            text="Game\nOver",
            font=("Arial", 50)
        )

        score = tk.StringVar()
        score_entry = tk.Entry(self.game_over_canvas)

        # Dimensions des widgets
        self.btn_height = size["Height"] / 4.5
        self.btn_width = self.btn_height * 2
        
        
        currentdir = os.path.dirname(__file__)
        graphics = os.path.join(currentdir, "Graphics")
        buttons = os.path.join(graphics, "Buttons")

        # Photos des widgets
        self.quit_photo = PhotoImage(
            file=os.path.join(buttons, "quitButton.png")
        )
        self.menu_photo = PhotoImage(
            file=os.path.join(buttons, "menuButton.png")
        )
        
        # Initialization des boutons
        
        self.btn_menu = tk.Button(
            self.game_over_canvas,
            image=self.menu_photo,
            width=self.btn_width, height=self.btn_height,
            borderwidth=0,
            command=self.on_menu
        )
        self.btn_quit = tk.Button(
            self.game_over_canvas,
            image=self.quit_photo,
            width=self.btn_width, height=self.btn_height,
            borderwidth=0,
            command=self.on_quit
        )
        
        # Positionnement des widgets
        self.btn_menu.place(
            x=(size["Width"]- (self.btn_width*2)) / 2,
            y=size["Height"]-self.btn_height
        )
        self.btn_quit.place(
            x=(size["Width"]- (self.btn_width*2)) / 2 + self.btn_width,
            y=size["Height"]-self.btn_height
        )
    
    def draw(self):
        self.pack()
