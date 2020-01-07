# imports:
import configparser
import importlib
import sys

from utils import helpers
from utils.datastructures import Config


def set_heuristics(domain, config):
    heuristics = domain.heuristics[config.settings['heuristic']]
    print(heuristics)
    domain.heuristic, domain.heuristic_fw, domain.heuristic_bw = heuristics[0], heuristics[0], heuristics[1]


# command line args, etc
config_file = 'experiments/example.conf'

# load and unpack config file
config = helpers.parse_config(config_file)
print(config)
domain_name = config.settings['domain']

# load domain, problem, determine search alg
domain = importlib.import_module('domains.' + domain_name)
set_heuristics(domain, config)

searcher_modules = {}
for searcher in config.searchers:
    alg = searcher['searcher']
    if alg not in searcher_modules.keys():
        searcher_modules[alg] = importlib.import_module('.searches.' + searcher['searcher'], package='src')

#search_algs = [importlib.import_module('.searches.' + alg_name, package='src') for alg_name in config.searchers_alg_names]
print('Domain: ', domain.__name__, end='\n\n')
problems = domain.generate_problems(config)
print(problems)

# log initial configuration

# run search
for i, problem in enumerate(problems):
    search_scopes = []
    for search_settings in config.searchers:
        label = f'{config.settings["domain"]}_{search_settings["name"]}_{i}.log'
        original_stdout = sys.stdout
        sys.stdout = open(f'experiments/runs/{label}', 'w')
        searcher = searcher_modules[search_settings['searcher']]

        print('**************************************************')
        print(f'Running search: {searcher.__name__}')
        print('-----------------')
        scope = searcher.search(problem, domain, search_settings)
        search_scopes.append(0)
        print('-----------------\n\n')

        sys.stdout = original_stdout

    helpers.write_out(search_scopes, i)

#search(**search_args)

# log results


