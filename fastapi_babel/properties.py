import os
import pathlib
from dataclasses import dataclass, field


@dataclass
class RootConfigs:

    ROOT_DIR: str
    BABEL_DEFAULT_LOCALE: str
    BABEL_TRANSLATION_DIRECTORY: str
    BABEL_DOMAIN: str = "messages.pot"
    BABEL_CONFIG_FILE: str = "babel.cfg"
    BABEL_MESSAGE_POT_FILE: str = field(init=False)

    def __post_init__(self):
        self.ROOT_DIR = pathlib.Path(self.ROOT_DIR).parent
        self.BABEL_TRANSLATION_DIRECTORY = os.path.join(
            self.ROOT_DIR, self.BABEL_TRANSLATION_DIRECTORY
        )
        self.BABEL_CONFIG_FILE = os.path.join(self.ROOT_DIR, self.BABEL_CONFIG_FILE)
        self.BABEL_MESSAGE_POT_FILE = os.path.join(self.ROOT_DIR, self.BABEL_DOMAIN)
