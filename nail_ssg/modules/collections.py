from .baseplugin import BasePlugin


class Collections(BasePlugin):
    pass


def create(config):
    return Collections(config)
