import io
import os
import re
import inspect


def _default_handler(self, full_path, is_dir):
    print(is_dir, full_path)
    return True


class DirRunner(object):
    """docstring for DirRunner"""
    EXCLUDE = 0
    INCLUDE = 1
    default_action = INCLUDE
    include_rules = []
    exclude_rules = []

    def __init__(self, path, handler=None):
        super(DirRunner, self).__init__()
        self.path = path
        self.handler = handler if handler else _default_handler

    def _in_rules(self, abs_path: str, is_dir: bool, rules: list) -> bool:
        for rule in rules:
            if inspect.isfunction(rule):
                if rule(abs_path, is_dir):
                    return True
            else:
                if len(re.findall(rule, abs_path)) != 0:
                    return True
        return False

    def _exclude(self, abs_path, is_dir):
        return self._in_rules(abs_path, is_dir, self.exclude_rules)

    def _include(self, abs_path, is_dir):
        return self._in_rules(abs_path, is_dir, self.include_rules)

    def _scan_dir(self, abs_path: str):
        dir_list = os.listdir(abs_path)
        for item in dir_list:
            full_path = os.path.abspath(os.sep.join([abs_path, item]))
            is_dir = os.path.isdir(full_path)
            if self._exclude(full_path, is_dir):
                continue
            if self.default_action == DirRunner.EXCLUDE and not self._include(full_path, is_dir):
                if is_dir:
                    self._scan_dir(full_path)
                    continue
                else:
                    continue
            if self.handler(self, full_path, is_dir) and is_dir:
                self._scan_dir(full_path)

    def run(self) -> None:
        full_path = os.path.abspath(self.path)
        self._scan_dir(full_path)


def get_file_info(abs_path):
    return {
        'path': abs_path,
        'date': str(os.path.getmtime(abs_path)),
        'size': str(os.path.getsize(abs_path))
    }
