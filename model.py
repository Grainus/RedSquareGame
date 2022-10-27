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


class Difficulty(Enum):
    """Enumération des difficultés de jeu"""
    EASY = 1
    MEDIUM = 2  # -> Default for production
    HARD = 3


"""window.update() time.sleep(0.01) dans loop jeu pour animation ennemi"""


class Enemy:
    """"Initalise la classe ennemi"""
    def __init__(self, canvas, x1, y1, x2, y2, color, speed_x, speed_y) -> None:
        """Initialise les variables de la classe."""
        # Canvas du jeu (peut-être root).
        self.canvas = canvas

        # Crée l'image de l'enemy.
        self.enemy = canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        # La vitesse et direction de l'animation (ex: -2, 2).
        self.speed_x = speed_x
        self.speed_y = speed_y

        # Calcule le milieu d'un segment/vecteur.
        self.pos_middle_x = int((x1 + x2) / 2)
        self.pos_middle_y = int((y1 + y2) / 2)

        # Pour collider().
        self.heigth = abs(y1 - y2)
        self.width = abs(x1 - x2)



    def animate_enemy_bounce(self) -> None:
        """La logique du déplacement des ennemis, peut en faire plusieurs."""
        # Dimensions du canvas.
        height = (self.canvas.winfo_height())
        width = (self.canvas.winfo_width())

        # Bouge le rectangle dans la direction indiquée.
        self.canvas.move(self.enemy, self.speed_x, self.speed_y)

        # Pour avoir les (x,y) des coins du rectangle.
        carre_pos = self.canvas.coords(self.enemy)
        x1, y1, x2, y2 = carre_pos

        # Met à jour pos_milieu_xy.
        self.pos_middle_x = int((x1 + x2) / 2)
        self.pos_middle_y = int((y1 + y2) / 2)
        self.height = abs(x1 - x2)
        self.width = abs(y1 - y2)

        # Si l'objet touche à un mur il change de direction.
        if y1 < abs(self.speed_y) or y2 > height - abs(self.speed_y):
            self.speed_y = - self.speed_y
        if x1 < abs(self.speed_x) or x2 > width - abs(self.speed_x):
            self.speed_x = - self.speed_x


class Player:
    """"Initalise la classe joueur"""
    def __init__(self, canvas: tk.Canvas, border, x1, y1, x2, y2, color) -> None:
        """Initialise les variables de la classe."""
        # Canvas du jeu (celui que le joueur ne peut pas dépasser).
        self.canvas = canvas
        
        # Affichage de la bordure
        self.canvas.create_rectangle(
            0, 0,
            canvas.winfo_width(), canvas.winfo_height(),
            outline="black",
            width=border*2,
        )

        # Crée le rectangle du Joueur.
        self.player = canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        # Pour wall_collision().
        self.border = border

        # Calcule le milieu d'un segment/vecteur.
        self.pos_middle_x = int((x1 + x2) / 2)
        self.pos_middle_y = int((y1 + y2) / 2)

        # Pour collider().
        self.heigth = abs(y1 - y2)
        self.width = abs(x1 - x2)

        # Pour la vérification du clique.
        self.x_start = self.pos_middle_x - abs(x1 - x2)
        self.x_stop = self.pos_middle_x + abs(x1 - x2) + 1
        self.y_start = self.pos_middle_y - abs(y1 - y2)
        self.y_stop = self.pos_middle_y + abs(y1 - y2) + 1

        # Lorsque le joueur clique sur le carre rouge fonction move().
        canvas.tag_bind(self.player, "<B1-Motion>", self._move)



    def wall_collision(self):
        """Détecte une collision avec les murs."""
        collision = False
        
        # Position du joueur
        x1, y1, x2, y2 = self.canvas.coords(self.player)
        self.pos_middle_x = int((x1 + x2) / 2)
        self.pos_middle_y = int((y1 + y2) / 2)
        # Dimensions du canvas.
        height = (self.canvas.winfo_height() - self.border)
        width = (self.canvas.winfo_width() - self.border)

        # Coins supérieurs
        cs_y = (self.pos_middle_y) - self.heigth/2
        cs_x = (self.pos_middle_x) - self.width/2

        # Coins inférieurs
        ci_y = (self.pos_middle_y) + self.heigth/2
        ci_x = (self.pos_middle_x) + self.width/2

        # Détecte la collision.
        if ci_y > height or cs_y < 0 + self.border:
            collision = True
        elif ci_x > width or cs_x < 0 + self.border:
            collision = True

        return collision

    def _move(self, event) -> None:
        # Arrète le joueur si il touche aux murs.
        if not self.wall_collision():
            self.canvas.moveto(
                self.player,
                event.x - self.width/2,
                event.y - self.heigth/2
            )
            
        else:
            # Game Over.





def collider(object1, object2):
    """Vérifie un collision entre deux objets."""
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

    # Distance minimum entre les deux objets.
    x_diff_min = (object1.width/2) + (object2.width/2)
    y_diff_min = (object1.heigth/2) + (object2.heigth/2)

    # Distance entre les deux côtés.
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

    #Return le coin de collision de l'objet1
    return collision
