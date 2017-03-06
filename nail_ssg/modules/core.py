from .basemodule import BaseModule


class Core(BaseModule):
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

    @classmethod
    def get_default_config(cls):
        return super().get_default_config()

    def build(self):
        super().build()

    def process_file(self):
        super().process_file()

    def __init__(self):
        super().__init__()


def create():
    return Core()
