from nail_config.config import Config
from collections import OrderedDict


class ConfigEx(Config):

    """docstring for ConfigEx"""

    def __init__(self):
        super().__init__()
        self.modules = OrderedDict()
