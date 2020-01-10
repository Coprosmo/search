# imports:

import importlib
import sys

from utils import helpers


def set_heuristics(domain, search_conf):
    heuristics = domain.heuristics[search_conf['heuristic']]
    domain.heuristic, domain.heuristic_fw, domain.heuristic_bw = heuristics[0], heuristics[0], heuristics[1]


def get_heuristics(domain, search_conf):
    heuristics = domain.heuristics[search_conf['heuristic']]
    return heuristics[0], heuristics[0], heuristics[1]


def set_config():
    # TODO: replace this with command line arg
    config_file = 'experiments/example2.conf'
    return helpers.parse_config(config_file)


def set_domain(config):
    domain_name = config.settings['domain']
    domain = importlib.import_module('domains.' + domain_name)
    print('Domain: ', domain.__name__, end='\n\n')
    return domain


def load_searchers(config):
    return {searcher['searcher']: importlib.import_module('.searchers.' + searcher['searcher'], package='src')
            for searcher in config.searchers}


def get_searchers(config):
    searchers = {}
    for search_config in config.searchers:
        name = search_config["name"]
        searchers[name] = search_config
        search_module = importlib.import_module('.searchers.' + search_config['searcher'], package='src')
        for k in search_module.__dict__.keys():
            if k.endswith('Search'):
                print(k)
                searchers[name]["searcher"] = search_module.__dict__[k]
                break
    return searchers


def generate_searchers(problems, searchers, domain, config):
    for search_name, search_conf in searchers.items():
        heuristics = get_heuristics(domain, search_conf)
        if isinstance(search_conf['degradation'], int):
            search_conf['degradation'] = [search_conf['degradation']]

        for degradation in search_conf["degradation"]:
            searcher = search_conf["searcher"]
            label = f'{domain.__name__}_{search_name}_h{degradation}'
            yield searcher(domain, heuristics, degradation, search_conf), label


if __name__ == "__main__":
    config = set_config()
    domain = set_domain(config)
    problems = domain.generate_problems(config)
    searchers = get_searchers(config)
    print(searchers)

    for i, problem in enumerate(problems):
        for searcher, label in generate_searchers(problems, searchers, domain, config):
            label = label + f'p{i}'
            searcher(problem)

"""
    for search_name, search_conf in searchers.items():
        #set_heuristics(domain, config)

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
"""