from .basemodule import BaseModule


class Pages(BaseModule):
    """docstring for Pages"""
    _config = None

    def __init__(self, config):
        super(Pages, self).__init__()
        self._config = config
