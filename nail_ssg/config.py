import os
from .common import dict_concat
import yaml


class Config(object):

    """docstring for Config"""
    _config = {}
    _config_filename = ''

    def __init__(self, filename='.config.yml'):
        self._config_filename = filename
        self._config = self.loadConfig()

    def loadConfig(self):
        filename = self._config_filename
        self._config = {}
        if not os.path.exists(filename):
            self._config = {}
        else:
            with open(filename, 'r') as f:
                dict_concat(self._config, yaml.load(f))
        return self._config

    def config(self, option: str, default_value=None) -> object:
        section = self._config
        section_names = option.split('.')
        name = section_names[-1]
        for section_name in section_names[:-1]:
            if section_name not in section:
                section[section_name] = {}
            section = section[section_name]
        if name not in section:
            section[name] = default_value
        return section[name]

    def save(self):
        with open(self._config_filename, 'w') as f:
            yaml.dump(self._config, f, default_flow_style=False)
