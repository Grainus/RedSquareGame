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

# Modules de projet
from model import Score, Difficulty
from config import Config

__docformat__ = "google"


class View(ABC):
    def __init__(self, root: Root, frame: tk.Frame):
        self.root = root
        self.frame = frame

    def set_listen(self, eventname: str, command: Callable) -> None:
        """Fonction permettant de lier un événement à une fonction"""
        self.root.bind(eventname, command)

    def destroy(self):
        """Fonction appelée pour détruire la vue"""
        self.frame.destroy()


class MenuView(View):
    def __init__(
            self, root: Root, frame: tk.Frame,
            on_new_game: Callable,
            on_quit: Callable,
            on_options: Callable,
            on_highscores: Callable
    ):
        """Initialisation de la vue du menu"""
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
            return  tk.Button(
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
        """Fonction appelée pour dessiner le jeu"""
        self.frame.pack()


class HighscoreView(View):
    def __init__(
                self, root: Root,
                frame: tk.Frame,
                on_quit: Callable,
                on_menu: Callable
        ):
        """Initialisation de la vue des highscores"""
        super().__init__(root, frame)
        size = Config.get_instance()["Game"]["Size"]
        
        self.on_quit = on_quit
        self.on_menu = on_menu
        self.highscore_canvas = tk.Canvas(
            self.frame,
            width=size["Width"], height=size["Height"]
        )
        self.highscore_canvas.pack()
        self.highscore_canvas.create_text(
            225, 35,
            text="Highscores",
            font=("Arial", 50)
        )

        # Dimensions des widgets
        self.btn_height = 100
        self.btn_width = 200
        self.score_width = 300

        scores = HighScore.get_scores()
        self.score_labels = []
        counter = 0
        for score, callback in scores[:10]:
            text = f"{score[0]}: {Score.to_readable(score[1])}"
            self.score_labels[counter] = tk.Button(
                self.highscore_canvas,
                text=text,
                command=callback,
                width=self.score_width)
            self.score_labels[counter].pack()
            counter+=1

        

        
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
        def create_btn(image: PhotoImage, cmd: Callable) -> tk.Button:
            return  tk.Button(
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
            x=(450 - (self.btn_width*2)) / 2,
            y=450- self.btn_height
        )
        self.btn_quit.place(
            x=(450 - (self.btn_width*2)) / 2 + self.btn_width,
            y=450- self.btn_height
        )

    def draw(self):
        """Fonction appelée pour dessiner les highscores"""
        self.frame.pack()

class OptionsView(View):
    def __init__(
                self, root: Root, frame: tk.Frame,
                on_quit: Callable,
                on_menu:Callable
        ):
        """ Initialisation de la vue des options """
        super().__init__(root, frame)
        self.on_quit = on_quit
        self.on_menu = on_menu
        self.options_canvas = tk.Canvas(self.frame, width=450, height=450)
        self.options_canvas.pack()
        self.options_canvas.create_text(225, 35, text="Options", font=("Arial", 50))

        # Dimensions des widgets
        self.btn_height = 100
        self.btn_width = 200
        self.diff_height = 50
        self.diff_width = 100


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
                config["Game"]["Difficulty"]["Level"] = str(diff)
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
            x=(450 - (self.btn_width*2)) / 2,
            y=450 - self.btn_height
        )
        self.btn_quit.place(
            x=(450 - (self.btn_width*2)) / 2 + self.btn_width,
            y=450 - self.btn_height
        )
        self.btn_easy.place(
            x=(450 - self.diff_width) / 2,
            y=450/2 - (self.diff_height*2)
        )
        self.btn_medium.place(
            x=(450 - self.diff_width) / 2,
            y=450/2 - self.diff_height
        )
        self.btn_hard.place(x=(450 - self.diff_width) / 2,y=450/2)

    def draw(self):
        self.frame.pack()


def create_timer_widget(canvas: tk.Canvas) -> tk.Label:
    """Créé la vue du widget et retourne son label"""
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
        self.btn_height = 100
        self.btn_width = 200
        
        
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
            x=(450 - (self.btn_width*2)) / 2,
            y=450-self.btn_height
        )
        self.btn_quit.place(
            x=(450 - (self.btn_width*2)) / 2 + self.btn_width,
            y=450-self.btn_height
        )
    
    def draw(self):
        self.pack()