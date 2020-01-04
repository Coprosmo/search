# imports:
import configparser
import importlib
import sys

from utils.helpers import parse_config
from utils.datastructures import Config

# command line args, etc
config_file = 'experiments/example2.conf'

# load and unpack config file
config = parse_config(config_file)
print(config)
domain_name = config.settings['domain']

# load domain, problem, determine search alg
domain = importlib.import_module('domains.' + domain_name)
searcher_modules = {}
for searcher in config.searchers:
    alg = searcher['searcher']
    if alg not in searcher_modules.keys():
        searcher_modules[alg] = importlib.import_module('.searches.' + searcher['searcher'], package='src')

#search_algs = [importlib.import_module('.searches.' + alg_name, package='src') for alg_name in config.searchers_alg_names]
print('Domain: ', domain.__name__, end='\n\n')
problems = [(1, 2, 3, 5, 4)]

# log initial configuration

# run search
for i, problem in enumerate(problems):
    for search_settings in config.searchers:
        label = f'{config.settings["domain"]}_{search_settings["name"]}_{i}'
        original_stdout = sys.stdout
        sys.stdout = open(f'experiments/runs/{label}', 'w')
        searcher = searcher_modules[search_settings['searcher']]

        print('**************************************************')
        print(f'Running search: {searcher.__name__}')
        print('-----------------')
        print(f'Search settings: {search_settings}')
        print('-----------------\n\n')

        sys.stdout = original_stdout

#search(**search_args)

# log results


