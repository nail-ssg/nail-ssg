import pytest
from os.path import abspath
import sys
from  nail_ssg import builder

# Создать объект builder
@pytest.fixture()
def empty_builder():
	filename = abspath('../tests/data/config1.yml')
	print(filename)
	return builder.Builder(filename)

def test_builder(empty_builder):
	empty_builder.open_plugin('pages')
