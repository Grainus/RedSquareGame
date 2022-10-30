from __future__ import annotations

from configparser import ConfigParser
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


class Config(ConfigParser, metaclass=Multiton):
    """Interface de configuration du programme.
    La méthode `get_instance` est utilisée pour obtenir un objet.
    """
    def __init__(self, name):
        super().__init__()
        currentdir = os.path.dirname(__file__)
        configdir = os.path.join(currentdir, "Data")
        self.configfile = os.path.join(configdir, name + '.ini')

        if not self.read(self.configfile):
            if not os.path.exists(configdir):
                os.mkdir(configdir)
            open(self.configfile, 'a').close() # Crée le fichier
            if not self.read(self.configfile):
                raise OSError("Could not read config file.")

    @classmethod
    def get_instance(cls, name: str = "settings"):
        return cls(name)

    def save(self):
        self.write(self.configfile)