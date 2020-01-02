"""Simple parser to extend functionality of configparser module.

Accepts standard format INI files as in configparser module. Returns a dictionary containing all keys, values from the
config file.

    Typical usage example:

    config = parse(example_config.conf)
"""

import configparser

__all__ = ['parse']

required_fields = ['search_alg',
                   'domain',
                   'initial']

defaults = {'cost': 'unit',
            'fw_heuristic': 'None',
            'bw_heuristic': 'None',}


def parse(config_file):
    """Parses an INI config file.

    Allows for certain defaults, and has required fields.

    Args:
        config_file: path to desired config file.

    Returns:
        A dict containing all key-value pairs from config file.

    Raises:
        Exception if any required fields are missing.
    """

    config = configparser.ConfigParser()
    config.read(config_file)

    sections = [config[section] for section in config.sections()]
    all_pairs = {k: v for section in sections for k,v in section.items()}

    if any(field not in all_pairs.keys() for field in required_fields):
        not_specified = [field for field in required_fields in field not in all_pairs.keys()]
        raise Exception(f'One or more required config fields not specified: {not_specified}')

    for field, default in defaults.items():
        if field not in all_pairs.keys():
            all_pairs[field] = default

    return all_pairs
