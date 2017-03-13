from .baseplugin import BasePlugin


class Alias(BasePlugin):
    pass


def create(config):
    return Alias(config)
