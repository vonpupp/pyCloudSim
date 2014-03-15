import os
import ConfigParser

import logging
log = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__),
                                   '..',
                                   'pycloudsim.conf')

REQUIRED_FIELDS = [
    'log_directory',
    'log_level'
]

def read_config(paths):
    """ Reads the configuration file and returns the dictionary.
    """
    configParser = ConfigParser.ConfigParser()
    for path in paths:
        configParser.read(path)
    return dict(configParser.items("DEFAULT"))

def validate_config(config, required_fields):
    for field in required_fields:
        if not field in config:
            return False
    return True

def read_and_validate_config():
    paths = [DEFAULT_CONFIG_PATH]
    required_fields = REQUIRED_FIELDS
    config = read_config(paths)
    if not validate_config(config, required_fields):
        message = 'The config does not contain ' + \
                  'all the required fields'
        log.critical(message)
        raise KeyError(message)
    return config
