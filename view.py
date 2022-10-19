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

from abc import ABC # Abstract Base Class
from typing import Callable

import tkinter as tk

from game_engine import Root


class View(ABC):
    def __init__(self, root: Root):
        self.root = root

    def set_listen(self, eventname: str, command: Callable):
        """" Fonction permettant de lier un événement à une fonction """
        self.root.bind(eventname, command)


class MenuView(View):
    def __init__(self, root: Root, on_new_game: Callable,
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
    def draw(self):
        """" Fonction appelée pour dessiner le jeu """
        self.root.game_frame.pack()

    def destroy(self):
        """" Fonction appelée pour détruire le jeu """
        self.root.game_frame.destroy()
