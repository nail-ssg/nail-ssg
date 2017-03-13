from .baseplugin import BasePlugin


class Pages(BasePlugin):

    """docstring for Pages"""
    _default_config = {
        'main': {
            'scan': {
                'types': [{
                    'type': 'page',
                    'rules': [
                        'fileMask = *.html',
                        'fileMask = *.part',
                        'fileMask = *.tpl',
                        'regexp = \.page\.',
                    ]
                }]
            }}
    }
    _config_comments = {}

    def __init__(self, config):
        super(Pages, self).__init__(config)

    def init(self):
        pass

    def modify_data(self):
        super().modify_data()

    def process_file(self, fileinfo, rules, data, global_data):
        return super().process_file(fileinfo, rules, data, global_data)

    def build(self):
        super().build()


def create(config):
    return Pages(config)
