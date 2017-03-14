from .baseplugin import BasePlugin
from nail_ssg.check_rules import check_rule
import ruamel.yaml as yaml


def _extract_yaml_data(filename: str):
    striped_line = ''
    with open(filename, 'r', encoding='utf-8') as f:
        yaml_lines = []
        checked_yaml = False
        for line in f.readlines():
            striped_line = line.strip()
            if not checked_yaml and (striped_line != '---'):
                break
            checked_yaml = True
            yaml_lines += [line]
            if striped_line == '...':
                break
    if striped_line != '...':
        return {}
    yaml_str = ''.join(yaml_lines)
    result = yaml.load(yaml_str, Loader=yaml.Loader)
    if not result:
        result = {}
    return result


class SsgMain(BasePlugin):
    _default_config = {
        'core': {
            'modules': {
                "static": True,
                "collections": True,
                "alias": True,
                "pages": True,
                "mixin": True,
            },
        },
    }
    _config_comments = {}
    name = 'main'

    def __init__(self, config):
        super().__init__(config)
        if not config:
            return

    def modify_data(self):
        super().modify_data()

    def build(self):
        super().build()

    def process_file(self, fileinfo, rules, data):
        super().process_file(fileinfo, rules, data)
        # todo: определить к какому правилу относится файл
        # print('*'*20)
        extract_data = False
        for file_type in self.types:
            for rule in file_type['rules']:
                validation = check_rule(rule, fileinfo['name'])
                if validation:
                    # print(validation, fileinfo['name'])
                    if file_type['type'] not in rules:
                        rules[file_type['type']] = []
                    rules[file_type['type']] += [rule]
                    extract_data = extract_data or file_type['extractData']
        if extract_data:
            filename = fileinfo['full_path']
            data.update(_extract_yaml_data(filename))

    def init(self):
        self.types = self.config('scan.types', [])


def create(config):
    return SsgMain(config)
