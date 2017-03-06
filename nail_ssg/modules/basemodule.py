class BaseModule(object):
    _default_config = None   # dict
    _config_comments = None  # dict
    __version__ = None       # string
    name = ''
    types = {}

    def __init__(self, config):
        self._config = config
        cls = self.__class__
        config.add_default_config(cls._default_config, cls._config_comments)
        pass

    # def folders(self):
    #     pass

    def process_file(self, rule, fileinfo, data, global_data):
        return data

    def modify_data(self):
        pass

    def build(self):
        pass
