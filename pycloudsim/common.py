# Copyright 2012 Albert De La Fuente
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

import os
import time
import json

import logging
log = logging.getLogger(__name__)


def start(init_state, execute, config, time_interval, iterations=-1):
    """ Start the processing loop.

    :param init_state: A function accepting a config and
                       returning a state dictionary.
     :type init_state: function

    :param execute: A function performing the processing at each iteration.
     :type execute: function

    :param config: A config dictionary.
     :type config: dict(str: *)

    :param time_interval: The time interval to wait between iterations.
     :type time_interval: int

    :param iterations: The number of iterations to perform, -1 for infinite.
     :type iterations: int

    :return: The final state.
     :rtype: dict(str: *)
    """
    state = init_state(config)

    if iterations == -1:
        while True:
            state = execute(config, state)
            time.sleep(time_interval)
    else:
        for _ in xrange(iterations):
            state = execute(config, state)
            time.sleep(time_interval)

    return state

def init_logging(log_directory, log_file, log_level):
    if log_level == 0:
        logging.disable(logging.CRITICAL)
        return True

    if not os.access(log_file, os.F_OK):
        if not os.access(log_directory, os.F_OK):
            os.makedirs(log_directory)
        elif not os.access(log_directory, os.W_OK):
            raise IOError(
                'Cannot write to the log directory: ' + log_directory)
    elif not os.access(log_file, os.W_OK):
        raise IOError('Cannot write to the log file: ' + log_file)

    if log_level == 3:
        level = logging.DEBUG
    elif log_level == 2:
        level = logging.INFO
    else:
        level = logging.WARNING

    logger = logging.root
    logger.handlers = []
    logger.filters = []

    logger.setLevel(level)
    handler = logging.FileHandler(
        os.path.join(log_directory, log_file))
    handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(levelname)-8s %(name)s %(message)s'))
    logger.addHandler(handler)

    return True


def call_function_by_name(name, args):
    """ Call a function specified by a fully qualified name.

    :param name: A fully qualified name of a function.
     :type name: str

    :param args: A list of positional arguments of the function.
     :type args: list

    :return: The return value of the function call.
     :rtype: *
    """
    fragments = name.split('.')
    module = '.'.join(fragments[:-1])
    fromlist = fragments[-2]
    function = fragments[-1]
    m = __import__(module, fromlist=fromlist)
    return getattr(m, function)(*args)


def parse_parameters(params):
    """ Parse algorithm parameters from the config file.

    :param params: JSON encoded parameters.
     :type params: str

    :return: A dict of parameters.
     :rtype: dict(str: *)
    """
    return dict((str(k), v)
                for k, v in json.loads(params).items())
