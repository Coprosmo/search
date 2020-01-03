# imports:
import configparser
import importlib
import sys

from utils.helpers import parse_config
from utils.datastructures import Config

# command line args, etc
config_file = 'experiments/example.conf'

# load and unpack config file
config = parse_config(config_file)
print(config)
domain_name = config.domain
search_alg_names = config.algs
print(search_alg_names)

# load domain, problem, determine search alg
domain = importlib.import_module('domains.' + domain_name)
search_algs = [importlib.import_module('.searches.' + alg_name, package='src') for alg_name in search_alg_names]
print('Domain: ', domain.__name__, end='\n\n')
problems = [(1, 2, 3, 5, 4)]

# log initial configuration

# run search
for i, problem in enumerate(problems):
    for alg in search_algs:
        label = f'{config.domain}_{alg.__name__}_{i}'
        original_stdout = sys.stdout
        sys.stdout = open(f'experiments/runs/{label}', 'w')

        print('**************************************************')
        print(f'Running search: {alg.__name__}')
        print('-----------------')
        print(f'Label: {label}')
        print('-----------------\n\n')

        sys.stdout = original_stdout

#search(**search_args)

# log results


