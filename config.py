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


class Config(metaclass=Multiton):
    def __init__(self, name):
        self.configfile = os.path.join(
                os.path.dirname(__file__),
                "Data", name + '.ini'
        )
        self.config = ConfigParser()
        self.config.read(self.configfile)
        

    @classmethod
    def get_instance(cls, name: str = "settings"):
        return cls(name)


a = Config.get_instance("settings")
