from fnmatch import fnmatch
import re

def check_rule(rule, filename):
    rule_type, pattern = (s.strip() for s in rule.split('='))
    # print('> '*4, rule_type, pattern, filename)
    if rule_type.lower() == 'filemask':
        return _check_rule_mask(pattern, filename)
    if rule_type.lower() == 'regexp':
        return _check_rule_regexp(pattern, filename)
    return False


def _check_rule_mask(pattern, filename):
    return fnmatch(filename, pattern)


def _check_rule_regexp(pattern, filename):
    return not not re.findall(pattern, filename)
