from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='awesomeengine',
    version='0.0.1',

    description='A Pythonic 2D game engine.',
    long_description=long_description,

    url='https://github.com/TeamAwesomeTOJam/awesomeengine',
    author='Team Awesome',
    author_email='jonathan@jdoda.ca',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    packages=['awesomeengine'],
    test_suite='tests',

    install_requires=[
        'sdl2hl>=0.3.2',
    ],
)
