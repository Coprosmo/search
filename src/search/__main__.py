# imports:
import configparser
import importlib
from utils.helpers import parse

# command line args, etc
config_file = 'configs/example.conf'

# load and unpack config file
config = parse(config_file)
domain_name = config['domain']
search_name = config['search_alg']
# domain_name = 'pancake'
# search_name = 'astar'
print(config)

# load domain, problem, determine search alg
domain = importlib.import_module('domains.' + domain_name)
search = importlib.import_module('searches.' + search_name)
print('Domain: ', domain.__name__)
print('Search algorithm: ', search.__name__)

# log initial configuration

# run search
#search(problem, domain)

# log results


