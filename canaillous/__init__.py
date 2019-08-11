# -*- coding: utf-8 -*-

VERSION = (0, 1, 0)
NAME = "canaillous"
DESCRIPTION = ""
AUTHOR = "Gabriele Barbieri"
AUTHOR_EMAIL = ""
URL = "https://github.com/gabrielebarbieri/canaillous"


def get_version():
    return '.'.join(map(str, VERSION))


__version__ = get_version()
