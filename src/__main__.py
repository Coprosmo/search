# imports:
import configparser
import importlib
import sys

from utils import helpers
from utils.datastructures import Config

# command line args, etc
config_file = 'experiments/example.conf'

# load and unpack config file
config = helpers.parse_config(config_file)
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
problems = [(1, 2, 3, 5, 4), (3, 4, 5, 1, 2)]

# log initial configuration

# run search
for i, problem in enumerate(problems):
    search_scopes = []
    for search_settings in config.searchers:
        label = f'{config.settings["domain"]}_{search_settings["name"]}_{i}'
        original_stdout = sys.stdout
        sys.stdout = open(f'experiments/runs/{label}', 'w')
        searcher = searcher_modules[search_settings['searcher']]

        print('**************************************************')
        print(f'Running search: {searcher.__name__}')
        print('-----------------')
        #scope = searcher.search(problem, domain)
        search_scopes.append(0)
        print('-----------------\n\n')

        sys.stdout = original_stdout

    helpers.write_out(search_scopes, i)

#search(**search_args)

# log results


