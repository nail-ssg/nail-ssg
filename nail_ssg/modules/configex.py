from nail_config.config import Config
from collections import OrderedDict


class ConfigEx(Config):

    """docstring for ConfigEx"""

    def __init__(self):
        super().__init__()
        self.modules = OrderedDict()
        self.data = {}
        self.full_src_path = ''
        self.full_dst_path = ''
