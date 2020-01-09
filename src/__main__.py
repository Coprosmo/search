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


def load_searchers(config):
    return {searcher['searcher']: importlib.import_module('.searches.' + searcher['searcher'], package='src')
            for searcher in config.searchers}


def get_searchers(config):
    searchers = {}
    for search_config in config.searchers:
        name = search_config["name"]
        searchers[name] = search_config
        search_alg = importlib.import_module('.searches.' + search_config['searcher'], package='src')
        searchers[name]["searcher"] = search_alg
    return searchers


if __name__ == "__main__":
    config = set_config()
    domain = set_domain(config)
    problems = domain.generate_problems(config)
    searchers = get_searchers(config)
    print(searchers)

    for search_name, search_conf in searchers.items():
        set_heuristics(domain, config)

        for i, problem in enumerate(problems):
            if isinstance(search_conf["degradation"], int):
                search_conf["degradation"] = [search_conf["degradation"]]
            for degradation in search_conf["degradation"]:
                label = f'{domain.__name__}_{search_name}_h{degradation}_p{i}'
                domain.heuristic.degradation = degradation
                searcher = search_conf["searcher"]

                original_stdout = sys.stdout
                sys.stdout = open(f'experiments/runs/{label}', 'w')
                output = searcher.search(problem, domain, search_conf)
                sys.stdout = original_stdout
