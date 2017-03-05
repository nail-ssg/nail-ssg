from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='nail-ssg',
    version='0.2',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    entry_points={
        'console_scripts':
            ['nail-ssg = nail_ssg.commands:run']
    },
    install_requires=[
        'pystache==0.5.4',
        'click==6.7',
        'ruamel.yaml==0.13.14'
    ])
