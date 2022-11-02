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

from enum import Enum
import tkinter as tk
import c31Geometry as geo # type: ignore
import time
from typing import Self


class Difficulty(Enum):
    """Enumération des difficultés de jeu"""
    EASY = 1
    MEDIUM = 2  # -> Default for production
    HARD = 3

class RectSprite:
    """Classe de base pour les entités rectangulaires dans le canvas."""
    def __init__(self, canvas: tk.Canvas,
            pos: geo.Point,
            width: float,
            height: float,
            color: str,
    ):
        """
        Args:
            canvas: Canvas où est dessiné l'objet.
            pos: Position du centre de l'objet.
            width: Largeur.
            height: Hauteur.
            color: Couleur de remplissage.
        """
        self.canvas = canvas
        self.pos_middle = pos
        self.height = height
        self.width = width

        halfsize = geo.Vecteur(width, height) / 2
        self.p1 = pos - halfsize
        "Coin supérieur gauche ↖ du rectangle."
        self.p2 = pos + halfsize
        "Coin inférieur droit ↘ du rectangle."

        # Crée le rectangle de l'entité.
        self.sprite = canvas.create_rectangle(*self.p1, *self.p2, fill=color)

    def update_pos(self) -> None:
        """Met à jour les attributs de position de l'objet.

        Note:
            Ne déplace pas le rectangle sur le canvas. Seules les
            variables `self.p1`, `self.p2`, et `self.pos_middle` sont
            modifiées.
        """
        coords = self.canvas.coords(self.sprite)
        self.p1, self.p2 = geo.Point(*coords[:2]), geo.Point(*coords[2:])
        # Centre: Coin ↖ plus la moitié du vecteur entre les deux coins
        self.pos_middle = self.p1 + (self.p2 - self.p1) / 2

class Player(RectSprite):

    def __init__(self, canvas: tk.Canvas,
            border: float,
            width: float,
            height: float,
            color: str,
            enemyList: list
    ):
        """Initialise le modèle du joueur.

        Args:
            canvas: Canvas où est dessiné l'objet.
            pos: Position du centre de l'objet.
            width: Largeur.
            height: Hauteur.
            color: Couleur de remplissage.
        """
        
        cwidth, cheight = canvas.winfo_width(), canvas.winfo_height()
        pos = geo.Point(225, 225) # A Debug
        super().__init__(canvas, pos, width, height, color)

        self.border = border
        self.var = tk.StringVar()
        self.enemyList = enemyList
        
        #Lorsque le joueur clique sur le carré rouge fonction move().
        canvas.tag_bind(self.sprite, "<B1-Motion>", self._move)

    def wall_collision(self, bordersize: float = None):
        """Détecte une collision avec les murs."""
        if bordersize is None:
            bordersize = self.border

        self.update_pos()

        #Dimensions du canvas.
        cheight = self.canvas.winfo_height() - bordersize
        cwidth = self.canvas.winfo_width() - bordersize

        # Détecte la collision.
        return (not bordersize < self.p1.y < self.p2.y < cheight
                or not bordersize < self.p1.x < self.p2.x < cwidth)

    def _move(self, event: tk.Event) -> None:
        """Permet au joueur de se déplacer"""
        #  Arrête le déplacement si le joueur touche un mur.
        if not self.wall_collision():
            self.canvas.moveto(
                self.sprite,
                event.x - self.width/2,
                event.y - self.height/2
            )
        else:
            pass

    def collision(self) -> bool:
        collision = False 
        for element in self.enemyList:
            if collider(self, element):
                collision = True
    
        return collision


class Enemy(RectSprite):

    def __init__(self, canvas: tk.Canvas,
            pos: geo.Point,
            width: float,
            height: float,
            color: str,
            speed: geo.Vecteur,
            #player: Player # TESTING
    ):
        """Initialise un ennemi.

        Args:
            canvas: Canvas où est dessiné l'objet.
            pos: Position du centre de l'objet.
            width: Largeur.
            height: Hauteur.
            color: Couleur de remplissage.
            speed: Déplacement effectué par l'ennemi à chaque tick.
        """
        super().__init__(canvas, pos, width, height, color)
        self.speed = speed
        #self.player = player
        
        self.animate_enemy_bounce()

    def animate_enemy_bounce(self) -> None:
        """La logique du déplacement des ennemis."""
        self.canvas.move(self.sprite, *self.speed)
        self.update_pos()

        # Dimensions du canvas.
        cheight = self.canvas.winfo_height()
        cwidth = self.canvas.winfo_width()

        # Si l'objet touche à un mur, il change de direction.
        if not 0 < self.p1.y < self.p2.y < cheight:
            self.speed = self.speed.conjugate()
        if not 0 < self.p1.x < self.p2.x < cwidth:
            self.speed = -self.speed.conjugate()

        self.canvas.after(20, self.animate_enemy_bounce)

        if(collider(self, self.player)):
            print("collider")

        

def collider(object1: RectSprite, object2: RectSprite) -> bool:
    """Vérifie une collision entre deux objets."""
    collision = False
    overlaps = object1.canvas.find_overlapping(*object1.p1, *object1.p2)
    if object2.sprite in overlaps: # TESTING
        collision = True

    return collision


def int_to_time(time: int) -> str:
    """ Converti un int, soit le score, en temps. Format : mm:ss """
    return f'{int(time / 60):02}:{int(time % 60):02}'
