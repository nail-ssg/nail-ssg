class Plugin(object):
    default_config = None
    _default_config = {
        "modify": None,
        "folders": None,
        "read_file": None,
        "build": None,
    }

    def __init__(self, arg):
        super(Plugin, self).__init__()
        self.arg = arg

    def folders(self):
        pass

    def read_file(self):
        pass

    def modify(self):
        pass

    def build(self):
        pass

    def _init_config(self):
        pass
