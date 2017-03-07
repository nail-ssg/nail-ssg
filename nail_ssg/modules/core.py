from .baseplugin import BasePlugin


class Core(BasePlugin):
    _default_config = {
        'core:': {
            'modules': {
                "static": True,
                "collections": True,
                "alias": True,
                "pages": True,
                "mixin": True
            },
            'dist': 'site',
            'src': 'src',
            'defaultNamespace': 'default'
        },
    }
    _config_comments = {
        'core.modules': 'list of modules and they states',
        'core.dist': 'distination directory for ready site',
        'core.src': 'source of templates, site files and raw page data',
        'core.currentNamespace': 'current namespace of aliases',
    }
    name = 'core'

    def modify_data(self):
        super().modify_data()

    def build(self):
        super().build()

    def process_file(self, fileinfo, data, global_data):
        super().process_file(fileinfo, data, global_data)

    def __init__(self, config):
        super().__init__(config)


def create(config):
    return Core(config)
