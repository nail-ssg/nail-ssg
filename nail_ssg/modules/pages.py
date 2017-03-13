from .baseplugin import BasePlugin
import os
from nail_config.common import dict_enrich, dict_concat2 as dict_concat


class Pages(BasePlugin):

    """docstring for Pages"""
    _default_config = {
        'core': {
            'modules': {
                'pages': {
                    'folder': 'pages'
                }
            }
        },
        'main': {
            'scan': {
                'types': [{
                    'type': 'page',
                    'rules': [
                            'fileMask = *.html',
                            'regexp = \.page\.',
                    ]
                }]
            }},
        'scan': {'order': ['pages']},
        'modify': {'order': ['pages']}
    }
    _config_comments = {}

    def __init__(self, config):
        super(Pages, self).__init__(config)

    def init(self):
        self.folder = os.path.join(self.config.full_src_path, self.config('scan.pages.folder'))
        self.config.data['pages'] = []

    def modify_data(self):
        super().modify_data()

    def process_file(self, fileinfo, rules, data):
        data = super().process_file(fileinfo, rules, data)
        if 'page' in rules:
            rel_path = os.path.relpath(fileinfo['full_path'], self.folder)
            data.update(dict_enrich(data, {'$global': {'url': rel_path.replace(os.sep, '/')}}))
            self.config.data['pages'] += [data]
        return data

    def build(self):
        super().build()


def create(config):
    return Pages(config)
