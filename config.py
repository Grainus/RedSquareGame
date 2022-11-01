# Copyright (c) 2022 Grainus
# 
# All rights reserved.


from __future__ import annotations
from typing import Sequence, TypeVar, Type, Self, Any

from functools import reduce
import json
import os


class Multiton(type):
    """Permet d'initialiser l'objet une seule fois par nom."""
    T = TypeVar('T')
    _instances: dict[tuple[Type[T], str], T] = {}

    def __call__(cls, name: str, *args, **kwargs):
        key = (cls, name)
        if key not in Multiton._instances:
            Multiton._instances[key] = (
                    super().__call__(name, *args, **kwargs)
            )
        return Multiton._instances[key]


class Config(metaclass=Multiton):
    def __init__(self, name):
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
        except OSError:
            with open(self.filepath, 'a') as file:
                file.write('{}')
        
    @classmethod
    def get_instance(cls, name: str = "settings") -> Self:
        return cls(name)

    def __getitem__(self, __key: str) -> Any | dict[str, Any]:
        return self.config[__key]

    def save(self) -> None:
        defaults = Config.get_instance('defaults').config
        diffs = deep_compare(defaults, self.config)
        with open(self.filepath, 'w') as file:
            json.dump(diffs, file, indent=4)


def deep_get(dct: dict, keys, *_keys: Any):
    """
    Args:
        dct: Le dictionnaire à chercher.
        keys: Une séquence de clés, ou une clé unique.
        _keys: Un nombre variable de clés.

    Example:
        mydict = {"People": {"John": {"Age": 30}, "Marie": {"Age": 20}}}
        deep_get(mydict, "People", "John", "Age") # 30
        deep_get(mydict, ("People", "John", "Age")) # 30
        marie = ("People", "Marie")
        deep_get(mydict, marie, "Age") # 20
    """
    if isinstance(keys, Sequence) and not isinstance(keys, str):
        keys = (*keys, *_keys)
    else:
        keys = (keys, *_keys)
    return reduce(lambda d, key: d.get(key) if d else None, keys, dct)

def deep_set(dct: dict, keys, value: Any):
    _dict = dct
    for key in keys[:-1]:
        if key not in _dict:
            _dict[key] = {}
        _dict = _dict[key]
    _dict[keys[-1]] = value

def deep_update(dictionary: dict, new: dict) -> None:
    _stack = [((), new)] # Afin d'éviter une solution récursive
    while _stack:
        keystack, subdict = _stack.pop(0)
        for key, val in subdict.items():
            _keys = (*keystack, key)
            if isinstance(val, dict):
                _stack.append((_keys, val))
            else:
                deep_set(dictionary, _keys, val)

def deep_compare(defaults: dict, dictionary: dict) -> dict:
    """Calcule la différence entre deux dictionaires.
    
    Returns:
        Un nouveau dictionaire D tel que `deep_update(defaults, D)`
            produise un dictionaire identique à `dictionary`
    """
    _stack = [((), dictionary)] # Afin d'éviter une solution récursive
    _diffs = {}
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

    cfgcolor["Outline"] = defcolor["Outline"] + "_" # Force valeur custom
    config.save()
    size1 = os.stat(config.filepath).st_size

    cfgcolor["Outline"] = defcolor["Outline"] # Remet le defaut
    config.save()
    size2 = os.stat(config.filepath).st_size

    # Le fichier ne sauvegarde que les différences. Les valeurs par
    # défaut créent donc un plus petit fichier.
    assert size2 < size1


if __name__ == "__main__":
    test_diff_save()
    print("All test passed")
    
