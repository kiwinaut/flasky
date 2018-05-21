import argparse
import os
# from constants import Mime

HOME = os.environ['HOME']
DIRPATH = os.path.dirname(os.path.realpath(__file__))
MOUNT = '/media/soni/1001'

class ConfigManager(object):
    "Config manager"

    def __init__(self):
        self.defaults = {
            '1001.path': '%s/persistent/1001/1001_v2.db' % MOUNT,
            'mount': MOUNT,
        }
        self.config = {}
        self.options = {}
        # self.arguments = []

    def parse(self):
        parser = argparse.ArgumentParser(description='flasky all in one', prog='flasky')
        parser.add_argument('-d', '--debug', action="store_true", help="Debug")
        args = parser.parse_args()
        self.options['debug'] = args.debug

    # def parse(self):
    #     parser = argparse.ArgumentParser(description='vip server', prog='vip')
    #     parser.add_argument('--test', action="store_true", help="Use Test Files")
    #     parser.add_argument('-p', '--port', type=int, metavar='8000', help="Port")

    #     args = parser.parse_args()
    #     self.options['test'] = args.test
    #     if args.test:
    #         self.options['database.path'] = ':memory:'



    def __setitem__(self, key, value, config=True):
        self.options[key] = value
        if config:
            self.config[key] = value

    def __getitem__(self, key):
        return self.options.get(key, self.config.get(key,
            self.defaults.get(key)))


CONFIG = ConfigManager()
