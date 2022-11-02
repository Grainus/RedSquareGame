# Copyright (c) 2022 Grainus
#
# All rights reserved.
"""Module de configuration optimisé.

Ce module permet de lire et de sauvegarder une configuration en format
JSON. Il nécessite un fichier représentant les valeurs par défaut nommé
`defaults.json`. Le fichier de sauvegarde (par défaut `settings.json`)
est optimisé pour n'inclure que les valeurs qui diffèrent de celles par
défaut. Plusieurs méthodes permettant de manipuler des dictionnaires
imbriqués sont aussi présentes.

Example:

  config = Config.get_instance()
  config["Game"]["Difficulty"] = "HARD"
  config.save(indent=4)
"""

from __future__ import annotations
from typing import Sequence, Self, TextIO, Any

from functools import reduce
import json
import os

__docformat__ = "google"


class Multiton(type):
    """Permet d'initialiser l'objet une seule fois par nom.

    Une fois un objet initialisé, une référence est créée avec le nom
    donné. Si on essaie d'initialiser un objet de la même classe avec le
    même nom, la référence est retournée et aucun nouveau objet n'est
    créé. Un même nom peut être utilisé par plusieurs classes
    différentes sans problème.

    Demander un objet déja créé a une complexité de O(1).
    """
    _instances: dict[tuple[type, str], Any] = {}

    def __call__(cls, name: str, *args, **kwargs):
        key = (cls, name)
        if key not in Multiton._instances:
            Multiton._instances[key] = (
                    super().__call__(name, *args, **kwargs)
            )
        return Multiton._instances[key]


class Config(metaclass=Multiton):
    """Classe permettant d'accéder aux configurations JSON.

    La configuration gardée en memoire représente la configuration
    complète des valeurs par défaut et des modifications. Pour accéder
    aux valeurs, l'utilisation de crochets `[]` est la méthode préférée.

    Note:
        Pour obtenir un objet Config, la méthode `Config.get_instance`
        doit être utilisée à la place de la méthode d'initialisation.
    """
    def __init__(self, name):
        """Méthode interne. Voir `Config.get_instance`."""
        currentdir = os.path.dirname(__file__)
        configdir = os.path.join(currentdir, "Data")
        self.filepath = os.path.join(configdir, name + '.json')

        # Charge les valeurs par défaut d'abord
        self.config: dict[str, Any] = {}
        if name != "defaults":
            defaults = Config.get_instance("defaults").filepath
            with open(defaults) as file:
                self.config = json.load(file)
        try:
            with open(self.filepath) as file:
                deep_update(self.config, json.load(file))
        except (OSError, json.JSONDecodeError):
            with open(self.filepath, 'a') as file:
                file.write('{}')

    @classmethod
    def get_instance(cls, name: str = "settings") -> Self:
        """Retourne une instance de Config pour le fichier spécifié.

        Args:
            name: Le nom du fichier de configuration à ouvrir.
              Defaults to "settings".

        Returns:
            Si le fichier spécifié n'a pas encore été ouvert, une
            nouvelle instance de Config. Sinon, une référence à l'objet
            existant.
        """
        return cls(name)

    def __getitem__(self, __key: str) -> Any | dict[str, Any]:
        """Accès directe au dictionnaire des configurations."""
        return self.config[__key]

    def save(self, file: TextIO | str | None = None, **kwargs) -> None:
        """Sauvegarde la configuration optimisée pour la taille dans un
        fichier.

        Args:
            file: Le fichier à utiliser pour la sauvegarde. Peut être un
              file-like ou un chemin. Si la valeur n'est pas donnée, le
              fichier utilisé lors de l'initialisation est pris.
            **kwargs: Arguments passés à `json.dump`.
        """
        defaults = Config.get_instance('defaults').config
        diffs = deep_compare(defaults, self.config)
        file = file if file is not None else self.filepath
        if not isinstance(file, str):
            json.dump(diffs, file, **kwargs)
        else:
            with open(file, 'w') as out:
                json.dump(diffs, out, **kwargs)


def deep_get(dct: dict, keys, *_keys: Any) -> Any | None:
    """
    Retourne un élément dans un dictionnaire imbriqué avec un nombre
    variable de clés. Si la clé est inexistante, retourne None.

    Args:
        dct: Le dictionnaire à chercher.
        keys: Une séquence de clés, ou une clé unique.
        _keys: Un nombre variable de clés.

    Example:
        mydict = {"People": {"John": {"Age": 30}, "Marie": {"Age": 20}}}

        deep_get(mydict, "People", "John", "Age")  # 30
        deep_get(mydict, ("People", "John", "Age"))  # 30

        marie = ("People", "Marie")
        deep_get(mydict, marie, "Age")  # 20
    """
    if isinstance(keys, Sequence) and not isinstance(keys, str):
        keys = (*keys, *_keys)
    else:
        keys = (keys, *_keys)
    # Retourne None si valeur non trouvée pour émuler dict.get
    return reduce(
        lambda d, key: d.get(key) if d else None, keys, dct  # type: ignore
    )


def deep_set(dct: dict, keys: Sequence, value: Any) -> None:
    """Modifie la valeur d'un dictionnaire imbriqué à une clé donnée.

    Si une clé est manquante, un nouveau dictionnaire est créé à chaque
    niveau pour insérer la valeur.

    Args:
        dct: Le dictionnaire à modifier.
        keys: Une séquence de clés jusqu'à la valeur.
        value: La valeur à mettre dans le dictionnaire.
    """
    _dict = dct
    for key in keys[:-1]:
        if key not in _dict:
            _dict[key] = {}
        _dict = _dict[key]
    _dict[keys[-1]] = value


def deep_update(dct: dict, new: dict) -> None:
    """Implémentation de `dict.update` qui fonctionne sur les
    dictionnaires imbriqués.

    Modifie le `dct` de manière à ce que tous les éléments de `new` y
    soient présents. Si une clé est présente dans les deux
    dictionnaires avec des valeurs différentes, la valeur dans `new` est
    utilisée. Si `dct` n'a aucun élément inexistants dans `new`, les
    deux dictionnaires seront identiques.

    Args:
        dct: Le dictionnaire à modifier.
        new: Le dictionnaire possédant les clés à ajouter ou modifier.
    """
    # Afin d'éviter une solution récursive
    dict.update
    _stack: list[tuple[tuple[Any, ...], dict[Any, Any]]] = [((), new)]
    while _stack:
        keystack, subdict = _stack.pop(0)
        for key, val in subdict.items():
            _keys = (*keystack, key)
            if isinstance(val, dict):
                _stack.append((_keys, val))
            else:
                deep_set(dct, _keys, val)


def deep_compare(dct: dict, defaults: dict) -> dict:
    """Calcule la différence entre deux dictionaires.

    Returns:
        Un nouveau dictionaire D tel que `deep_update(dct, D)`
          produise un dictionaire identique à `dct` si `defaults` ne
          possède aucune clé inexistante dans `dct`.
    """
    # Afin d'éviter une solution récursive
    _stack: list[tuple[tuple[Any, ...], dict[Any, Any]]] = [((), dct)]
    _diffs: dict[Any, Any] = {}
    while _stack:
        keystack, subdict = _stack.pop(0)
        for key, val in subdict.items():
            _keys = (*keystack, key)
            if isinstance(val, dict):
                _stack.append((_keys, val))
            elif val != deep_get(defaults, _keys):
                deep_set(_diffs, _keys, val)
    return _diffs


def test_diff_save():
    config = Config.get_instance()
    default = Config.get_instance('defaults')
    cfgcolor = config["Game"]["Color"]
    defcolor = default["Game"]["Color"]

    cfgcolor["Outline"] = defcolor["Outline"] + "_"  # Force valeur custom
    config.save()
    size1 = os.stat(config.filepath).st_size

    cfgcolor["Outline"] = defcolor["Outline"]  # Remet le defaut
    config.save()
    size2 = os.stat(config.filepath).st_size

    # Le fichier ne sauvegarde que les différences. Les valeurs par
    # défaut créent donc un plus petit fichier.
    assert size2 < size1


if __name__ == "__main__":
    test_diff_save()
    print("All test passed")
