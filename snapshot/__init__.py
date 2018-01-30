# -*- coding: utf-8 -*-

from pkg_resources import get_distribution

def parse_int(number):
    # type: (str) -> int
    try:
        return int(number)
    except ValueError as e:
        return 0

__version__ = get_distribution('snapshot').version
VERSION = tuple(map(parse_int, __version__.split('.')))
