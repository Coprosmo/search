# imports:

import importlib
import sys

from utils import helpers


def set_heuristics(domain, config):
    heuristics = domain.heuristics[config.settings['heuristic']]
    domain.heuristic, domain.heuristic_fw, domain.heuristic_bw = heuristics[0], heuristics[0], heuristics[1]


def set_config():
    # TODO: replace this with command line arg
    config_file = 'experiments/example.conf'
    return helpers.parse_config(config_file)


def set_domain(config):
    domain_name = config.settings['domain']
    domain = importlib.import_module('domains.' + domain_name)
    print('Domain: ', domain.__name__, end='\n\n')
    return domain


def setup_searchers(config):
    return {searcher['searcher']: importlib.import_module('.searches.' + searcher['searcher'], package='src')
            for searcher in config.searchers}


def run_searchers(problems, searchers, config):
    for i, problem in enumerate(problems):
        search_scopes = []
        for search_settings in config.searchers:
            label = f'{config.settings["domain"]}_{search_settings["name"]}_{i}.log'
            original_stdout = sys.stdout
            sys.stdout = open(f'experiments/runs/{label}', 'w')
            searcher = searchers[search_settings['searcher']]

            print('**************************************************')
            print(f'Running search: {searcher.__name__}')
            print('-----------------')

            scope = searcher.search(problem, domain, search_settings)
            search_scopes.append(0)

            sys.stdout = original_stdout
        helpers.write_out(search_scopes, i)


if __name__ == "__main__":
    config = set_config()
    domain = set_domain(config)
    problems = domain.generate_problems(config)
    set_heuristics(domain, config)
    searchers = setup_searchers(config)
    run_searchers(problems, searchers, config)
