from .baseplugin import BasePlugin


class Mixin(BasePlugin):
    pass


def create(config):
    return Mixin(config)
