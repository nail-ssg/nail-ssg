from .print import *
from .config import Config
from .dir_runner import DirRunner
from .modules.core import Core
import importlib


class Builder(object):
    _modules = []
    config = None

    def __init__(self, filename):
        # if not os.path.exists(filename):
        #     self.set_default_config()
        self.config = Config(filename)
        default_core_config, core_comments = Core.get_default_config()
        self.set_default_config(default_core_config, core_comments)
        self._load_modules()

    def _load_modules(self):
        module_list = self.config('core.modules', {})
        for module in module_list:
            if self.config('.'.join(['core.modules', module.name]), True):
                default_config, config_comments = module.get_default_config()
                self.config.default_config(default_config, config_comments)

    def build(self):
        dr = DirRunner(self.config.config('core.src', 'src'), self._file_handler)
        dr.run()
        # yprint(self.allData)
        # for builder in _builders:
        #     builder(self)
        # if self.conf.config('core.autoUpdateConfig', True):
        #     self.conf.save()

    def _file_handler(self, dr: DirRunner, full_path: str, is_dir: bool) -> bool:
        return True

    @classmethod
    def add_module(cls, module_class):
        if module_class not in cls._modules:
            cls._modules += [module_class]

    def set_default_config(self, dconf, comments={}):
        self.config.default_config(dconf, comments)
