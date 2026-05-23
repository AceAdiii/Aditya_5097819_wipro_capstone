from configparser import ConfigParser
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config" / "config.ini"


class ConfigReader:
    def __init__(self, path=CONFIG_PATH):
        self.path = Path(path)
        self.parser = ConfigParser()
        self.parser.read(self.path)

    def get(self, section, key, fallback=None):
        return self.parser.get(section, key, fallback=fallback)

    def get_bool(self, section, key, fallback=False):
        if not self.parser.has_option(section, key):
            return fallback
        return self.parser.getboolean(section, key)

    def get_int(self, section, key, fallback=0):
        if not self.parser.has_option(section, key):
            return fallback
        return self.parser.getint(section, key)


config = ConfigReader()

