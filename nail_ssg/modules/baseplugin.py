from .basemodule import BaseModule


class BasePlugin(BaseModule):
    module_type = 'plugin'
    _default_config = None   # dict
    _config_comments = None  # dict
    __version__ = None       # string
    name = ''
    types = {}

    def __init__(self, config):
        super().__init__(config)
        cls = self.__class__
        config.add_default_config(cls._default_config, cls._config_comments)

    def process_file(self, fileinfo, rules, data):
        return data

    def modify_data(self):
        pass

    def build(self):
        pass
