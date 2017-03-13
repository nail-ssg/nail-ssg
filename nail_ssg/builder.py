from .print import *
from .modules import ConfigEx
from .dir_runner import DirRunner
from collections import OrderedDict
import importlib
import os


class Builder(object):
    config = None

    def _load_config(self, filename):
        self.config = ConfigEx()
        if not self.config.load(filename):
            raise Exception('OMG')
        default_config = {
            'core':
            {
                'src': 'src',
                'dist': 'site',
                'currentNamespace': 'default',
                'main': 'main',
            },
            'scan': {
                'order': [],
                'types': []
            },
            'modify': {
                'order': [],
                'options': []
            },
            'builders': {
                'order': []
            }
        }
        config_comments = {
            'core.modules': 'list of modules and they states',
            'core.dist': 'distination directory for ready site',
            'core.src': 'source of templates, site files and raw page data',
            'core.currentNamespace': 'current namespace of aliases',
        }
        self.config.add_default_config(
            default_config,
            config_comments
        )

    def _init_modules(self):
        for module_name in self.config.modules:
            module = self.config.modules[module_name]
            module.init()

    def __init__(self, filename):
        # if not os.path.exists(filename):
        #     self.set_default_config()
        self._load_config(filename)
        self.src = self.config('core.src')
        self.config.full_src_path = os.path.abspath(self.src)
        self.dst = self.config('core.dist',)
        self.config.full_dst_path = os.path.abspath(self.dst)
        main_module_name = self.config('core.main')
        self.main_module = self.add_module(main_module_name)
        self._init_modules()
        self.scan_order = self.config('scan.order', [])
        # print(self._modules)
        print(self.config.as_yamlstr())
        # print(self.config)

    def build(self):
        dr = DirRunner(self.src, self._file_handler)
        dr.run()
        print('='*20)
        yprint(self.config.data)

        for module_name in self.config('modify.order'):
            print(module_name)
            module = self.config.modules[module_name]
            module.modify_data()

        for module_name in self.config('builders.order'):
            print(module_name)
            module = self.config.modules[module_name]
            module.build()

    def _file_handler(self, dr: DirRunner, full_path: str, is_dir: bool) -> bool:
        if is_dir:
            return True
        data = {}
        rules = {}
        folder, name = full_path.rsplit(os.sep, 1)
        fileinfo = {
            'folder': folder,
            'name': name,
            'full_path': full_path
        }
        rel_path = os.path.relpath(full_path, self.config.full_src_path)
        self.main_module.process_file(fileinfo, rules, data)
        for module_name in self.scan_order:
            module = self.config.modules[module_name]
            module.process_file(fileinfo, rules, data)
        self.config.data[rel_path] = data
        return True

    def add_module(self, module_name):
        if module_name not in self.config.modules:
            try:
                module = importlib.import_module('nail_ssg.modules.' + module_name)
            except Exception as e:
                raise e
            self.config.modules[module_name] = module.create(self.config)
            modules = self.config('core.modules')
            if modules:
                for name in modules:
                    if modules[name]:
                        self.add_module(name)
        return self.config.modules[module_name]

    def set_default_configs(self):
        for key in self._modules:
            module = self._modules[key]
            default_core_config, core_comments = module.get_default_config()
            self.set_default_config(default_core_config, core_comments)

    def set_default_config(self, dconf, comments=None):
        self.config.add_default_config(dconf, comments)
