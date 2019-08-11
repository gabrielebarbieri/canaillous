import setuptools
import sys
import os
from setuptools.command.test import test as TestCommand

PACKAGE = 'canaillous'
pkg = __import__(PACKAGE)
VERSION = pkg.__version__

install_requires = ['pandas']

setuptools.setup(
    name=pkg.NAME,
    version=VERSION,
    description=pkg.DESCRIPTION,
    author=pkg.AUTHOR,
    author_email=pkg.AUTHOR_EMAIL,
    license='',
    packages=setuptools.find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'canaillous=canaillous.process:main'
        ],
    }
)