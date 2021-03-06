# imports:

import importlib
import sys
import os
import shutil

from src.search.utils import helpers

os.chdir('src/search')

def get_heuristics(domain, search_conf):
    heuristics = domain.heuristics.get(search_conf['heuristic'], domain.heuristics['zero'])
    return heuristics[0], heuristics[0], heuristics[1]


def get_config():
    # TODO: replace this with command line arg
    # config_file = 'src/search/experiments/example.conf'
    config_file = 'experiments/example.conf'
    return helpers.parse_config(config_file)


def get_domain_module(config):
    domain_name = config.settings['domain']
    domain_module = importlib.import_module('.domains.' + domain_name, package='src.search')
    print('Domain: ', domain_module.__name__, end='\n\n')
    return domain_module


def load_searching_algorithms(config):
    searchers = {}
    for search_config in config.searchers:
        name = search_config["name"]
        searchers[name] = search_config
        search_module = importlib.import_module('.searchers.' + search_config['searcher'], package='src.search')
        for k in search_module.__dict__.keys():
            if k.endswith('Search'):
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
            label = f'{domain.__name__}_{search_name}_h{degradation}_'
            yield searcher(domain, heuristics, degradation, search_conf), label


def setup_folders():
    computer_stats = 'experiments/runs/stats'
    human_readable_stats = 'experiments/runs/human_stats'
    if os.path.exists(computer_stats):
        shutil.rmtree(computer_stats)
    if os.path.exists(human_readable_stats):
        shutil.rmtree(human_readable_stats)
    os.makedirs(computer_stats)
    os.makedirs(human_readable_stats)


def main():
    setup_folders()
    config = get_config()
    domain = get_domain_module(config)
    problems = domain.generate_problems(config)
    search_algs = load_searching_algorithms(config)

    for i, problem in enumerate(problems):
        for searcher, label in generate_searchers(problems, search_algs, domain, config):
            label = label + f'p{i}'
            print(f'Starting search: {label} . . .')
            original_stdout = sys.stdout
            sys.stdout = open(f'experiments/runs/human_stats/{label}.log', 'w')
            searcher(problem, label)
            sys.stdout = original_stdout
            print(f'Finished!')
    print('All done :)')


if __name__ == "__main__":
    main()
