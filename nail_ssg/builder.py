from .print import *
from nail_config.config import Config
from .dir_runner import DirRunner
from .modules.core import Core
import importlib


class Builder(object):
    config = None

    def __init__(self, filename):
        # if not os.path.exists(filename):
        #     self.set_default_config()
        self._modules = {}
        self.config = Config()
        if not self.config.load(filename):
            raise Exception('OMG')
        self.add_module('core')

    def _load_modules(self):
        module_list = self.config('core.modules', {})
        for module in module_list:
            if self.config('.'.join(['core.modules', module.name]), True):
                default_config, config_comments = module.get_default_config()
                self.config.add_default_config(default_config, config_comments)

    def build(self):

        dr = DirRunner(self.config('core.src', 'src'), self._file_handler)
        dr.run()
        # yprint(self.allData)
        # for builder in _builders:
        #     builder(self)
        # if self.conf.config('core.autoUpdateConfig', True):
        #     self.conf.save()

    def _file_handler(self, dr: DirRunner, full_path: str, is_dir: bool) -> bool:
        for module_name in self._modules:
            module = self._modules[module_name]
            fileinfo = {
                'rule': None,
                'folder': full_path,
                'is_dir': is_dir,
                'full_path': full_path
            }
            data = {}
            global_data = {}
            module.process_file(fileinfo, data, global_data)
        return True

    def add_module(self, module_name):
        if module_name not in self._modules:
            try:
                module = importlib.import_module('nail_ssg.modules.' + module_name)
            except Exception as e:
                raise e
            self._modules[module_name] = module.create(self.config)

    def set_default_configs(self):
        for key in self._modules:
            module = self._modules[key]
            default_core_config, core_comments = module.get_default_config()
            self.set_default_config(default_core_config, core_comments)

    def set_default_config(self, dconf, comments=None):
        self.config.add_default_config(dconf, comments)
