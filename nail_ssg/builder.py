from .print import *
from nail_config.config import Config
from .dir_runner import DirRunner
from collections import OrderedDict
import importlib
import os


class Builder(object):
    config = None

    def _load_config(self, filename):
        self.config = Config()
        if not self.config.load(filename):
            raise Exception('OMG')
        config_comments = {
            'core.modules': 'list of modules and they states',
            'core.dist': 'distination directory for ready site',
            'core.src': 'source of templates, site files and raw page data',
            'core.currentNamespace': 'current namespace of aliases',
        }
        self.config.add_default_config(
            {'core': {'main': 'main', 'dist': 'site', 'src': 'src', 'currentNamespace': 'default'}},
            config_comments
        )

    def _init_modules(self):
        for module_name in self._modules:
            module = self._modules[module_name]
            module.init()

    def __init__(self, filename):
        # if not os.path.exists(filename):
        #     self.set_default_config()
        self._modules = OrderedDict()
        self._load_config(filename)
        self.src = self.config('core.src', 'src')
        main_module = self.config('core.main', 'main')
        self.add_module(main_module)
        self._init_modules()
        # print(self._modules)
        # print(self.config.as_yamlstr())
        # print(self.config)

    def build(self):
        self.global_data = {}
        dr = DirRunner(self.config('core.src', 'src'), self._file_handler)
        dr.run()

    def _file_handler(self, dr: DirRunner, full_path: str, is_dir: bool) -> bool:
        data = {}
        rules = {}
        for module_name in self._modules:
            module = self._modules[module_name]
            folder, name = full_path.rsplit(os.sep, 1)
            fileinfo = {
                'folder': folder,
                'name': name,
                'is_dir': is_dir,
                'full_path': full_path
            }
            module.process_file(fileinfo, rules, data, self.global_data)
        return True

    def add_module(self, module_name):
        if module_name not in self._modules:
            try:
                module = importlib.import_module('nail_ssg.modules.' + module_name)
            except Exception as e:
                raise e
            self._modules[module_name] = module.create(self.config)
            modules = self.config('core.modules')
            if modules:
                for module_name in modules:
                    if modules[module_name]['state'] or 'state' not in modules[module_name]:
                        self.add_module(module_name)

    def set_default_configs(self):
        for key in self._modules:
            module = self._modules[key]
            default_core_config, core_comments = module.get_default_config()
            self.set_default_config(default_core_config, core_comments)

    def set_default_config(self, dconf, comments=None):
        self.config.add_default_config(dconf, comments)
