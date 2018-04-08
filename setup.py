#!/usr/bin/env python3
from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), 'r') as f:
    long_description = f.read()

setup(
    name='dl-fish-completions',
    version='1.0',

    description='Download latest completion files from the fish-shell master branch.',
    long_description=long_description,
    url='https://github.com/rickh94/download-fish-completions',

    author='Rick Henry',
    author_email='fredericmhenry@gmail.com',

    license='MIT',
    python_requires='>=3.6',
    install_requires=['click',
                      'requests',
                      'aiohttp',
                      'bs4'],

    py_modules=['dl_fish_completions'],
    entry_points={
        'console_scripts': [
            'dl-fish-completions=dl_fish_completions:cli',
            ],
        },
    )
