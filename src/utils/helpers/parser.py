"""Simple parser to extend functionality of configparser module.

Accepts standard format INI files as in configparser module. Returns a dictionary containing all keys, values from the
config file.

    Typical usage example:

    config = parse(example_config.conf)
"""

import configparser
import random
import json
from ..datastructures.config import Config

__all__ = ['parse_config']

required_fields = ['domain']

defaults = {'seed': random.random(),
            'param': None,
            'partial_expansion': False
            }


def _jsonload(parser, sect, item):
    return json.loads(parser.get(sect, item))


def _validifyfields(items):
    if any(field not in items.keys() for field in required_fields):
        not_specified = [field for field in required_fields if field not in items.keys()]
        raise Exception(f'One or more required config fields not specified: {not_specified}')


def parse_config(config_file):
    """Parses an INI style config file.

        Allows for certain defaults, and has required fields. Makes extensive use of the configparser and json
        libraries. Casts arguments to their desired types.

        Args:
            config_file: path to desired config file.

        Returns:
            A dict containing all key-value pairs from config file.

        Raises:
            Exception if any required fields are missing.
        """

    parser = configparser.ConfigParser()
    parser.read(config_file)

    sections = parser.sections()

    directory = dict()
    for section in sections:
        items = parser.items(section)
        directory[section] = [items[i][0] for i in range(len(items))]

    settings = {item: _jsonload(parser, "Settings", item) for item in directory["Settings"]}
    searchers = []

    for searcher in directory["Searchers"]:
        new_search = _jsonload(parser, "Searchers", searcher)
        new_search['name'] = searcher
        searchers.append(new_search)
    searchers = tuple(searchers)

    config = Config(settings=settings, searchers=searchers)
    _validifyfields(settings)
    
    return config

