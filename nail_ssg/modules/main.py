from .baseplugin import BasePlugin
from nail_ssg.check_rules import check_rule


class NailMain(BasePlugin):
    _default_config = {
        'main': {
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
    _config_comments = {}
    name = 'main'

    def modify_data(self):
        super().modify_data()

    def build(self):
        super().build()

    def process_file(self, fileinfo, rules, data, global_data):
        super().process_file(fileinfo, rules, data, global_data)
        # todo: определить к какому правилу относится файл
        # print('*'*20)
        for file_type in self.types:
            for rule in file_type['rules']:
                validation = check_rule(rule, fileinfo['name'])
                if validation:
                    # print(validation, fileinfo['name'])
                    if file_type['type'] not in rules:
                        rules[file_type['type']] = []
                    rules[file_type['type']] += [rule]
        print(rules)


    def __init__(self, config):
        super().__init__(config)
        if not config:
            return
        print(config)

    def init(self):
        self.types = self.config('main.scan.types', [])


def create(config):
    return NailMain(config)
