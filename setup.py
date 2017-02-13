from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='nail-ssg',
    version='0.1',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    entry_points={
        'console_scripts':
            ['nail-ssg = nail_ssg.commands:run']
    },
    install_requires=[
        'PyYAML==3.12',
        'pystache==0.5.4'
    ])
