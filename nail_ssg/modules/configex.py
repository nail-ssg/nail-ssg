import importlib
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

    def add_module(self, module_name):
        if module_name not in self.modules:
            try:
                module = importlib.import_module('nail_ssg.modules.' + module_name)
            except Exception as e:
                raise e
            self.modules[module_name] = module.create(self)
            modules = self('core.modules')
            if modules:
                for name in modules:
                    if modules[name]:
                        self.add_module(name)
        return self._get_module(module_name)

    def _get_module(self, module_name):
        return self.modules[module_name] if module_name in self.modules else None

    def get_module(self, module_name):
        module = self._get_module(module_name)
        return self.add_module(module_name) if module is None else module
