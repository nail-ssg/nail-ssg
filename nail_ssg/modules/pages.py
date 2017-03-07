from .baseplugin import BasePlugin


class Pages(BasePlugin):
    """docstring for Pages"""
    _default_config = {}
    _config_comments = {}

    def __init__(self, config):
        super(Pages, self).__init__(config)

    def modify_data(self):
        super().modify_data()

    def process_file(self, fileinfo, data, global_data):
        return super().process_file(fileinfo, data, global_data)

    def build(self):
        super().build()


def create(config):
    return Pages(config)
