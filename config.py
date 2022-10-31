from __future__ import annotations
from typing import Sequence, TypeVar, Type, Self, Any

from configparser import ConfigParser, RawConfigParser, SectionProxy
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


class ConfigJson(metaclass=Multiton):
    def __init__(self, name):
        currentdir = os.path.dirname(__file__)
        configdir = os.path.join(currentdir, "Data")
        self.filepath = os.path.join(configdir, name + '.json')

        # Charge les valeurs par défaut d'abord
        self.config: dict[str, Any] = {}
        if name != "defaults":
            defaults = ConfigJson.get_instance("defaults").filepath
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
        defaults = ConfigJson.get_instance('defaults').config
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


class Config(metaclass=Multiton):
    """Interface de configuration du programme. Permet d'accéder à la
    configuration en « dot notation ».

    La méthode `get_instance` est utilisée pour obtenir un objet.
    """
    def __init__(self, name):
        super().__init__()
        currentdir = os.path.dirname(__file__)
        configdir = os.path.join(currentdir, "Data")
        configfile = os.path.join(configdir, name + '.ini')

        config = ConfigParser()
        self.config = config
        self.configfile = configfile

        # Lecture du fichier
        if not self.config.read(self.configfile):
            if not os.path.exists(configdir):
                os.mkdir(configdir)
            open(self.configfile, 'a').close() # Crée le fichier
            if not self.config.read(self.configfile):
                raise OSError("Could not read config file.")

        # Vérification de collisions
        reserved_names = ('config', 'configfile')
        for name_ in reserved_names:
            if config.has_section(name_):
                raise RuntimeError(f"Config file ({configfile}) has "
                    f"illegal section name: {name_}")
        
        # Remplacement des proxy
        for section in self.config._proxies.keys():
            self.config._proxies[section] = (
                    ConfigSection(self.config, section)
            )
        
        # Patch add_section pour utiliser ConfigSection
        def add_section(self_, section):
            ConfigParser.add_section(self_, section)
            self_._proxies[section] = ConfigSection(self_, section)
        # Bind (pour que self soit passé comme premier argument)
        self.config.add_section = add_section.__get__(self.config)
            

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
        with open(self.configfile, 'w') as file:
            self.config.write(file)

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
    assert a is b is c is d is e is f

def test_creation():
    config = Config.get_instance("settings")
    otherconfig = Config.get_instance("settings")
    lastconfig = Config.get_instance("testing")
    assert config is otherconfig and config is not lastconfig

def test_save():
    os.remove("Data/testing.ini")
    config = Config.get_instance("testing")
    config.config.add_section("Sect")
    config.config["Sect"]["Val"] = "Hello"
    config.save()
    otherconfig = Config.get_instance("testing")
    assert otherconfig.Sect.val == "Hello"
    os.remove("Data/testing.ini")

def test_diff_save():
    config = ConfigJson.get_instance()
    default = ConfigJson.get_instance('defaults')
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
    # test_access()
    # test_creation()
    # test_save()
    test_diff_save()
    print("All test passed")
    
