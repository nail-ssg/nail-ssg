import pytest
from os.path import abspath
import sys
from nail_ssg import builder


# Создать объект builder
@pytest.fixture()
def empty_builder():
    filename = abspath('tests/data/config_minimal.yml')
    print(filename)
    return builder.Builder(filename)


def test_builder(empty_builder):
    # empty_builder.add_module('pages')
    empty_builder.build()
