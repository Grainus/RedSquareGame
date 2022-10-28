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
import c31Geometry.c31Geometry2 as geo

class Difficulty(Enum):
    """Enumération des difficultés de jeu"""
    EASY = 1
    MEDIUM = 2  # -> Default for production
    HARD = 3


"""window.update() time.sleep(0.01) dans loop jeu pour animation ennemi"""


class BaseSprite:
    def __init__(self, canvas: tk.Canvas,
            pos: geo.Point,
            width: float,
            height: float,
            color: str,
    ):
        """Initialise une entité rectangulaire dans le jeu.

        Args:
            canvas: Canvas où l'on dessine l'objet.
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
        p1 = pos - halfsize
        p2 = pos + halfsize
        
        # Crée le rectangle de l'entité.
        self.sprite = canvas.create_rectangle(*p1, *p2, fill=color)


class Enemy(BaseSprite):

    def __init__(self, canvas: tk.Canvas,
            pos: geo.Point,
            width: float,
            height: float,
            color: str,
            speed: geo.Vecteur,
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


    def animate_enemy_bounce(self) -> None:
        """La logique du déplacement des ennemis, peut en faire plusieurs."""
        # Note: confusing docstring               ^^^^^^^^^^^^^^^^^^^^^^^^ ???
        """Bouge le rectangle dans la direction indiquée."""
        self.canvas.move(self.sprite, *self.speed)

        """Pour avoir les (x,y) des coins du rectangle."""
        coords = self.canvas.coords(self.sprite)
        p1, p2 = geo.Point(*coords[:2]), geo.Point(*coords[2:])
        self.pos_middle = p1 + (p2 - p1) / 2

        # Dimensions du canvas.
        cheight = self.canvas.winfo_height()
        cwidth = self.canvas.winfo_width()

        # Si l'objet touche à un mur il change de direction.
        if not 0 < p1.y < p2.y < cheight:
            self.speed = self.speed.conjugate()
        if not 0 < p1.x < p2.x < cwidth:
            self.speed = -self.speed.conjugate()
        # if y1 < abs(self.speed_y) or y2 > height - abs(self.speed_y):
        #     self.speed_y = - self.speed_y
        # if x1 < abs(self.speed_x) or x2 > width - abs(self.speed_x):
        #     self.speed_x = - self.speed_x


class Player(BaseSprite):

    def __init__(self, canvas: tk.Canvas,
            border: float,
            width: float,
            height: float,
            color: str,
    ):  
        
        cwidth, cheight = canvas.winfo_width(), canvas.winfo_height()
        pos = geo.Point(cwidth / 2, cheight / 2)
        super().__init__(canvas, pos, width, height, color)

        self.border = border

        # Affichage de la bordure
        self.canvas.create_rectangle(
            0, 0,
            canvas.winfo_width(), canvas.winfo_height(),
            outline="black",
            width=border*2,
        )

        """Lorsque le joueur clique sur le carre rouge fonction move()."""
        canvas.tag_bind(self.sprite, "<B1-Motion>", self._move)

    """Détecte une collision avec les murs."""

    def wall_collision(self, bordersize: float = None):
        if bordersize is None:
            bordersize = self.border
        # Position du joueur
        #x1, y1, x2, y2 = self.canvas.coords(self.player)
        coords = self.canvas.coords(self.sprite)
        p1, p2 = geo.Point(*coords[:2]), geo.Point(*coords[2:])
        self.pos_middle = p1 + (p2 - p1) / 2

        """Dimensions du canvas."""
        cheight = self.canvas.winfo_height() - bordersize
        cwidth = self.canvas.winfo_width() - bordersize

        """Détecte la collision."""
        return (not bordersize < p1.y < p2.y < cheight
                or not bordersize < p1.x < p2.x < cwidth)

    def _move(self, event) -> None:
        #TODO: This doc is irrelevant to the actual effect of the method
        """Arrète le joueur si il touche aux murs."""
        if not self.wall_collision():
            self.canvas.moveto(
                self.sprite,
                event.x - self.width/2,
                event.y - self.height/2
            )
            
        else:
            print("""Game Over.""")


"""Vérifie un collision entre deux objets."""


def collider(object1, object2):

    collision = ""

    top_x_obj1 = object1.pos_middle_x
    top_y_obj1 = object1.pos_middle_y - (object1.heigth/2)

    bottom_x_obj1 = object1.pos_middle_x
    bottom_y_obj1 = object1.pos_middle_y + (object1.heigth/2)

    left_x_obj1 = object1.pos_middle_x - (object1.width/2)
    left_y_obj1 = object1.pos_middle_y

    right_x_obj1 = object1.pos_middle_x + (object1.width/2)
    right_y_obj1 = object1.pos_middle_y

    top_x_obj2 = object2.pos_middle_x
    top_y_obj2 = object2.pos_middle_y - (object2.heigth/2)

    bottom_x_obj2 = object2.pos_middle_x
    bottom_y_obj2 = object2.pos_middle_y + (object2.heigth/2)

    left_x_obj2 = object2.pos_middle_x - (object2.width/2)
    left_y_obj2 = object2.pos_middle_y

    right_x_obj2 = object2.pos_middle_x + (object2.width/2)
    right_y_obj2 = object2.pos_middle_y

    """Distance minimum entre les deux objets."""
    x_diff_min = (object1.width/2) + (object2.width/2)
    y_diff_min = (object1.heigth/2) + (object2.heigth/2)

    """Distance entre les deux côtés."""
    if (top_y_obj1 - bottom_y_obj2 == 0):
        if (abs(top_x_obj1 - bottom_x_obj2) < x_diff_min):
            collision = "top"

    elif (bottom_y_obj1 - top_y_obj2 == 0):
        if (abs(bottom_x_obj1 - top_x_obj2) < x_diff_min):

            collision = "bottom"

    elif (right_x_obj1 - left_x_obj2 == 0):
        if (abs(right_y_obj1 - left_y_obj2) < y_diff_min):
            collision = "right"

    elif (left_x_obj1 - right_x_obj2 == 0):
        if (abs(left_y_obj1 - right_y_obj2) < y_diff_min):
            collision = "left"

    """Return le coin de collision de l'objet1"""
    return collision
