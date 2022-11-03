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
"""Module contenant les classes de gestion des sprites.

Classes:
    - RectSprite: Classe de base des sprites rectangulaires.
    - Player: Classe du joueur.
    - Enemy: Classe des ennemis.
    - Score: Classe du score.

Fonction:
    - collider: Vérifie une collision entre deux objets.
"""
# Documentation
from __future__ import annotations
from typing import Callable

# Modules standards
from functools import partial
from enum import Enum
import tkinter as tk

# Modules de projet
import c31Geometry.c31Geometry2 as geo  # type: ignore
from config import Config

__docformat__ = "google"


class Difficulty(Enum):
    """#Enumération des difficultés de jeu"""
    EASY = 1
    MEDIUM = 2  # -> Default for production
    HARD = 3


class RectSprite:
    """#Classe de base pour les entités rectangulaires dans le canvas.

    Attributs:
        - canvas: Canvas où est dessiné l'objet.
        - pos_middle: Position du centre de l'objet.
        - height: Hauteur.
        - width: Largeur.
        - p1: Coin supérieur gauche ↖ du rectangle.
        - p2: Coin inférieur droit ↘ du rectangle.
        - sprite: Rectangle de l'entité.

    Notes:
        - Les attributs `p1` et `p2` sont des points, et non des vecteurs.
        """

    def __init__(
            self, canvas: tk.Canvas,
            pos: geo.Point,
            width: float,
            height: float,
            color: str,
    ):
        """"""
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
        """##Met à jour les attributs de position de l'objet.

        Notes:
            - Cette méthode est appelée à chaque fois que l'objet est déplacé.
            - Les attributs `p1` et `p2` sont des points, et non des vecteurs.
            - Ne deplace pas l'objet sur le canvas, que les points.
        """
        coords = self.canvas.coords(self.sprite)
        self.p1, self.p2 = geo.Point(*coords[:2]), geo.Point(*coords[2:])
        # Centre: Coin ↖ plus la moitié du vecteur entre les deux coins
        self.pos_middle = self.p1 + (self.p2 - self.p1) / 2


class Enemy(RectSprite):
    """#Classe pour les ennemis.

    Attributs:
        - canvas: Canvas où est dessiné l'objet.
        - pos : Position du  de l'objet.
        - width: Largeur.
        - height: Hauteur.
        - speed: Vecteur de vitesse.
        - color: Couleur.
        - player: Référence vers le joueur.

    Note:
        - Les attributs `p1` et `p2` sont des points, et non des vecteurs.
        """

    def __init__(
            self, canvas: tk.Canvas,
            pos: geo.Point,
            width: float,
            height: float,
            speed: geo.Vecteur,
            *, # Prochains sont keyword-only
            color: str | None = None,
            player: Player,
    ):
        """"""
        colordefault = Config.get_instance()["Enemy"]["Color"]["Fill"]
        _color = color if color is not None else colordefault

        super().__init__(canvas, pos, width, height, _color)
        self.speed = speed
        self.player = player

    def start_move(self) -> None:
        """##La logique du déplacement des ennemis.

        Note:
            - Collider sert à détecter les collisions avec le joueur.
            """
        # Bouge le rectangle dans la direction indiquée.
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

        self.canvas.after(20, self.start_move)
        collider(self.player, self)


class Player(RectSprite):
    """#Classe pour le joueur.

    Attributs:
        - canvas: Canvas où est dessiné l'objet.
        - bounds: Limites du canvas.
        - width: Largeur.
        - height: Hauteur.
        - color: Couleur.
        - timer_widget: Widget du timer.
        - endgame : Fonction à appeler à la fin de la partie.
        - score: Score du joueur.
        """
    def __init__(
            self, canvas: tk.Canvas,
            border: float | None = None,
            width: float | None = None,
            height: float | None = None,
            color: str | None = None,
            *,  # Prochains sont keyword-only
            timer_widget : tk.Label,
            endgame: Callable
        ):
        """"""
        config = Config.get_instance()
        def if_given(value, default):
            return value if value is not None else default

        _border = if_given(border, config["Game"]["Size"]["Border"])
        _width = if_given(width, config["Player"]["Size"]["Width"])
        _height = if_given(height, config["Player"]["Size"]["Height"])
        _color = if_given(color, config["Player"]["Color"]["Fill"])
        
        self.endgame = endgame
        cwidth, cheight = canvas.winfo_width(), canvas.winfo_height()
        pos = geo.Point(cwidth / 2, cheight / 2)

        # Les arguments sont optionels, mais des valeurs sont ajoutées
        super().__init__(canvas, pos, _width, _height, _color)
        self.border = _border
        self.score = Score(canvas, timer_widget)

        # Affichage de la bordure
        rect = self.canvas.create_rectangle(
            0, 0,
            canvas.winfo_width(), canvas.winfo_height(),
            outline=config["Game"]["Color"]["Outline"],
            width=_border * 2,
        )
        self.canvas.lower(rect)

        #  Lorsque le joueur clique sur le carre rouge fonction move().
        canvas.tag_bind(self.sprite, "<B1-Motion>", self._move)

    def wall_collision(self, bordersize: float = None) -> bool:
        """##Détecte une collision avec les murs.

        Args:
            - bordersize: Taille de la bordure.

        Returns:
            - True si il y a collision, False sinon.
            """
        if bordersize is None:
            bordersize = self.border

        self.update_pos()

        #  Dimensions du canvas.
        cheight = self.canvas.winfo_height() - bordersize
        cwidth = self.canvas.winfo_width() - bordersize

        # Détecte la collision.
        return (not bordersize < self.p1.y < self.p2.y < cheight
                or not bordersize < self.p1.x < self.p2.x < cwidth)

    def _move(self, event: tk.Event) -> None:
        """##Permet au joueur de se déplacer

        Args:
            - event: Événement de déplacement.
        """
        #  Arrête le déplacement si le joueur touche un mur.
        if not self.wall_collision():
            self.canvas.moveto(
                self.sprite,
                event.x - self.width/2,
                event.y - self.height/2
            )
        else:
            self.endgame()


def collider(object1: RectSprite | Player, object2: RectSprite) -> bool:
    """##Vérifie une collision entre deux objets.

    Args:
        - object1: Premier objet.
        - object2: Deuxième objet.

    Note:
        - Si un des objets est le joueur, il doit être le premier argument.

    Returns:
        - True si il y a collision, False sinon.
    """
    overlaps = object1.canvas.find_overlapping(*object1.p1, *object1.p2)
    ret =  object2.sprite in overlaps
    if ret and isinstance(object1, Player):
        object1.endgame()
    return ret


class Score:
    """#Contrôle l'état du score

    Attributs:
        canvas: Canvas où est dessiné l'objet.
        label: Label du score.
        value: Valeur du score.
        started : Booléen indiquant si le timer est lancé.
        loop : Boucle du timer.
        """
    def __init__(self, canvas: tk.Canvas, label: tk.Label):
        """"""
        self.value = 0
        self.started = False
        self.canvas = canvas
        self.label = label

    def start(self):
        """##Démarre le timer."""
        if not self.started:
            def update(self: Score):
                self.value += 1
                self.label.config(text=self)
            self.loop = geo.LoopEvent(
                self.canvas, partial(update, self),
                1000,
            )
            self.loop.start()
        else:
            raise RuntimeError("Started score twice")
    
    @staticmethod
    def to_readable(value: int) -> str:
        """##Convertit un nombre de secondes en une chaîne de caractères lisible.

        Args:
            - value: Nombre de secondes.

        Returns:
            - Chaîne de caractères lisible.
        """
        minutes, seconds = divmod(value, 60)
        return f"{minutes:02d}:{seconds:02d}"
        return f'{int(value / 60):02}:{int(value % 60):02}'

    def __str__(self) -> str:
        return Score.to_readable(self.value)
