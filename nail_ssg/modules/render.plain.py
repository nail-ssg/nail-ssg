from nail_ssg.modules.baseplugin import BasePlugin


class Plain(BaseRender):

    """docstring for Plain"""

    def __init__(self, config, plugin):
        super().__init__(config, plugin)

    def render(self, text, data):
        pass


def create(config, plugin):
    return Plain(config, plugin)
