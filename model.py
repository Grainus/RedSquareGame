from enum import Enum
from tkinter import Canvas


class Difficulty(Enum):
    """Enumération des difficultés de jeu"""
    EASY = 1
    MEDIUM = 2  # -> Default for production
    HARD = 3


"""window.update() time.sleep(0.01) dans loop jeu pour animation ennemi"""


class Enemy:

    def __init__(self, canvas, x1, y1, x2, y2, color, speed_x, speed_y) -> None:
        """Canvas du jeu (peut-être root)."""
        self.canvas = canvas

        """Crée l'image de l'enemy"""
        self.enemy = canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        """La vitesse et direction de l'animation (ex: -2, 2)."""
        self.speed_x = speed_x
        self.speed_y = speed_y

        """Calcule le milieu d'un segment/vecteur."""
        self.pos_middle_x = int((x1 + x2) / 2)
        self.pos_middle_y = int((y1 + y2) / 2)

        """Pour collider()."""
        self.heigth = abs(y1 - y2)
        self.width = abs(x1 - x2)

    """La logique du déplacement des ennemis, peut en faire plusieurs."""

    def animate_enemy_bounce(self) -> None:
        """Dimensions du canvas."""
        height = (self.canvas.winfo_height())
        width = (self.canvas.winfo_width())

        """Bouge le rectangle dans la direction indiquée."""
        self.canvas.move(self.enemy, self.speed_x, self.speed_y)

        """Pour avoir les (x,y) des coins du rectangle."""
        carre_pos = self.canvas.coords(self.enemy)
        x1, y1, x2, y2 = carre_pos

        """Met à jour pos_milieu_xy."""
        self.pos_middle_x = int((x1 + x2) / 2)
        self.pos_middle_y = int((y1 + y2) / 2)
        self.height = abs(x1 - x2)
        self.width = abs(y1 - y2)

        """Si l'objet touche à un mur il change de direction."""
        if y1 < abs(self.speed_y) or y2 > height - abs(self.speed_y):
            self.speed_y = - self.speed_y
        if x1 < abs(self.speed_x) or x2 > width - abs(self.speed_x):
            self.speed_x = - self.speed_x


class Player:

    def __init__(self, canvas, border, x1, y1, x2, y2, color) -> None:
        """Canvas du jeu (celui que le joueur ne peut pas dépasser)."""
        self.canvas = canvas

        """Crée le rectangle du Joueur."""
        self.player = canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        """Pour wall_collision()."""
        self.border = border

        """Calcule le milieu d'un segment/vecteur."""
        self.pos_middle_x = int((x1 + x2) / 2)
        self.pos_middle_y = int((y1 + y2) / 2)

        """Pour collider()."""
        self.heigth = abs(y1 - y2)
        self.width = abs(x1 - x2)

        """Pour la vérification du clique."""
        self.x_start = self.pos_middle_x - abs(x1 - x2)
        self.x_stop = self.pos_middle_x + abs(x1 - x2) + 1
        self.y_start = self.pos_middle_y - abs(y1 - y2)
        self.y_stop = self.pos_middle_y + abs(y1 - y2) + 1

        """Lorsque le joueur clique sur le carre rouge fonction move()."""
        canvas.bind("<B1-Motion>", self.move)

    """Détecte une collision avec les murs."""

    def wall_collision(self):

        collision = False

        """Dimensions du canvas."""
        height = (self.canvas.winfo_height() - self.border)
        width = (self.canvas.winfo_width() - self.border)

        """Coins supérieurs"""
        cs_y = (self.pos_middle_y) - self.heigth/2
        cs_x = (self.pos_middle_x) - self.width/2

        """Coins inférieurs"""
        ci_y = (self.pos_middle_y) + self.heigth/2
        ci_x = (self.pos_middle_x) + self.width/2

        """Détecte la collision."""
        if ci_y > height or cs_y < 0 + self.border:
            collision = True
        elif ci_x > width or cs_x < 0 + self.border:
            collision = True

        return collision

    def move(self, event) -> None:
        """Vérifie si on clique bien sur le joueur."""
        if int(event.x) in range(int(self.x_start), int(self.x_stop)):
            if int(event.y) in range(int(self.y_start), int(self.y_stop)):
                """Arrète le joueur si il touche aux murs."""
                if (self.wall_collision() == False):

                    """Global pour avoir l'info joueur.pos_milieu_xy dans la boucle."""
                    global player

                    """Pour avoir les (x,y) des coins du rectangle."""
                    player_pos = self.canvas.coords(self.player)
                    x1, y1, x2, y2 = player_pos

                    """Enlève l'ancien rectangle du canvas de jeu."""
                    self.canvas.delete(self.player)

                    """Creer un nouveau joueur."""
                    player = Player(self.canvas, self.border,
                                    x1/2 + event.x - x2/2,
                                    y1/2 + event.y - y2/2,
                                    x2/2 + event.x - x1/2,
                                    y2/2 + event.y - y1/2, color="#f00")
                else:
                    """Game Over."""


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
