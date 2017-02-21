import pytest
import sys
sys.path += ['../..']
from nail_ssg import config


@pytest.fixture(scope="function")
def conf(request):
    cfg = config.Config()
    yield cfg
    cfg = None


def test_create(conf):
    assert conf.config() == {}


def test_one_default(conf):
    d = {'a': {'b': 'c'}, 'e': ['f', 'g'], 'i': 'j'}
    conf.defaultConfig(d)
    assert conf.config() == d


def test_more_default(conf):
    d1 = {'a': {'b': 'c'}, 'e': ['f', 'g'], 'i': 'j'}
    d2 = {'a': {'b': 'aa', 'c': 'aaa'}, 'e': ['f', 'ee'], 'i': 'ii'}
    result = {'a': {'b': 'c', 'c': 'aaa'}, 'e': ['f', 'g', 'ee'], 'i': 'j'}
    conf.defaultConfig(d1)
    conf.defaultConfig(d2)
    assert conf.config() == result
