from __future__ import annotations
from typing import Any

from configparser import ConfigParser, RawConfigParser, SectionProxy
import os


class Multiton(type):
    """Permet d'initialiser l'objet une seule fois par nom"""
    _instances = {}

    def __call__(cls, name: str, *args, **kwargs):
        if name not in Multiton._instances:
            Multiton._instances[name] = (
                    super().__call__(name, *args, **kwargs)
            )
        return Multiton._instances[name]


class Config(metaclass=Multiton):
    """Interface de configuration du programme. Permet d'accéder à la
    configuration en « dot notation ».

    La méthode `get_instance` est utilisée pour obtenir un objet.
    """
    def __init__(self, name):
        super().__init__()
        currentdir = os.path.dirname(__file__)
        configdir = os.path.join(currentdir, "Data")
        self.configfile = os.path.join(configdir, name + '.ini')

        self.config = ConfigParser()

        # Lecture du fichier
        if not self.config.read(self.configfile):
            if not os.path.exists(configdir):
                os.mkdir(configdir)
            open(self.configfile, 'a').close() # Crée le fichier
            if not self.config.read(self.configfile):
                raise OSError("Could not read config file.")
        
        # Remplacement des proxy
        for section in self.config._proxies.keys():
            self.config._proxies[section] = (
                    ConfigSection(self.config, section)
            )
            

    @classmethod
    def get_instance(cls, name: str = "settings"):
        return cls(name)

    def __getattribute__(self, __name: str) -> Any | ConfigSection:
        config: ConfigParser = super().__getattribute__('config')
        if not config.has_section(__name):
            return super().__getattribute__(__name)
        else:
            return config[__name]
    
    def __getitem__(self, __name: str) -> ConfigSection:
        config: ConfigParser = super().__getattribute__('config')
        return config[__name]

    def save(self):
        self.config.write(self.configfile)

class ConfigSection(SectionProxy):
    """Ajoute l'accès en « dot notation » comme alternative au
    « bracket notation ».
    """
    def __init__(self, parser: RawConfigParser, name: str):
        object.__setattr__(self, 'initialized', False)
        super().__init__(parser, name)
        object.__setattr__(self, 'attributes', self.__dict__.keys())
        object.__setattr__(self, 'initialized', True)

    def _use_attr(self, __name) -> bool:
        initialized = object.__getattribute__(self, 'initialized')
        if initialized:
            attributes = object.__getattribute__(self, 'attributes')
            return __name in attributes
        else:
            return True

    def __getattribute__(self, __name: str) -> Any | str:
        _use_attr = object.__getattribute__(self, '_use_attr')
        if _use_attr(__name):
            return super().__getattribute__(__name)
        else:
            return super().__getitem__(__name)
        
    def __setattr__(self, __name: str, __value: Any) -> None:
        _use_attr = object.__getattribute__(self, '_use_attr')
        if _use_attr(__name):
            return super().__setattr__(__name, __value)
        else:
            return super().__setitem__(__name, __value)


def test_access():
    config = Config.get_instance()
    a = config["Game"]["Difficulty"]
    b = config["Game"].Difficulty
    c = config.Game["Difficulty"]
    d = config.Game.Difficulty
    e = config.config["Game"].Difficulty
    f = config.config["Game"]["Difficulty"]
    print(a, a is b is c is d is e is f)

if __name__ == "__main__":
    test_access()
