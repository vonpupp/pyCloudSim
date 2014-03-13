# Copyright 2013 Albert De La Fuente
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Distsim :: Config routines
"""
__version__ = "0.1"
__author__  = "Albert De La Fuente"

import os
import ConfigParser

import logging
log = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__),
                                   '..',
                                   'pyCloudSim.conf')

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
