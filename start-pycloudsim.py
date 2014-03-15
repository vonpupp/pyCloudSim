#!/usr/bin/python
# vim:ts=4:sts=4:sw=4:et:wrap:ai:fileencoding=utf-8:
#
# Copyright 2014 Albert P. M. De La Fuente Vigliotti
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
pyCloudSim :: A Simple Enery Aware Cloud Simulator framework
"""
__version__ = "0.2"
__author__ = "Albert De La Fuente"


#import argparse
from pycloudsim.globals.manager import Manager
from pycloudsim.classes.repeatedtimer import RepeatedTimer
import logging
log = logging.getLogger(__name__)


def host_factory(hostname_list):
    result = []
    for host in hostname_list:
        result += ['host {}'.format(host)]
        print('Creating host {}'.format(host))
#    h = Host()
#    h.name = ''
#    h.cpu =
#    h.
    return result

def callback(arg):
    print(arg)


def run():

#    rt = RepeatedTimer(1, callback, "hello")
    m = Manager()
    factory = host_factory
    m.add_physical_hosts_factory = factory
    m.add_physical_hosts_args = ['a', 'b', 'c', 'd']
#    m.add_physical_hosts(16)
    m.add_physical_hosts()
#    m.add_virtual_machines(16)
    m.start()

if __name__ == "__main__":
    run()
#    parser = argparse.ArgumentParser(description='A VM distribution/placement simulator.')
#    parser.add_argument('-pm', '--pmcount', help='Number of physical machines (def: 64)', required=False)
#    parser.add_argument('-vm', '--vmcount', help='Number of VMs (def: 64)', required=False)
#    parser.add_argument('-cl', '--clock', help='', required=False)
#    parser.add_argument('-pa', '--pack', help='', required=False)
#    parser.add_argument('-clcb', '--clockcallback', help='', required=False)
#    #clock_callback = distsim.x.y.z.callback
#    #pack_callback = distsim.x.y.z.callback
