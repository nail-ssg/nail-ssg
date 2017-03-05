class BaseModule(object):
    _default_config = None   # dict
    _config_comments = None  # dict
    __version__ = None       # string
    name = ''
    types = {}

    def __init__(self):
        pass

    def folders(self):
        pass

    def process_file(self):
        pass

    def modify_data(self):
        pass

    def build(self):
        pass

    def render(self, text, data):
        pass

    @classmethod
    def get_default_config(cls):
        return cls._default_config, cls._config_comments
