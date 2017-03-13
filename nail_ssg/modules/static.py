from .baseplugin import BasePlugin


class Static(BasePlugin):
    pass


def create(config):
    return Static(config)
