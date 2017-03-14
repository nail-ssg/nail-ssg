from .basemodule import BaseModule


class BaseRender(BaseModule):

    """docstring for BaseRender"""
    module_type = 'render'

    def __init__(self, config):
        super().__init__(config)
        self._config = config
        self._plugin = None

    def render(self, text: str, model: dict, render_options: dict) -> str:
        return text
