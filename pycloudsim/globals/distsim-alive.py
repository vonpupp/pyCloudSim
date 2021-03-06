#!/usr/bin/python
# vim:ts=4:sts=4:sw=4:et:wrap:ai:fileencoding=utf-8:
#
# Copyright 2014 Albert De La Fuente
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
Distsim :: A VM distribution/placement simulator
"""
__version__ = "0.1"
__author__  = "Albert De La Fuente"


from distsim.managers.simmanager import Simulator
import argparse
from distsim.config import *
import distsim.common as common
from distsim.model.repeatedtimer import RepeatedTimer
import logging
log = logging.getLogger(__name__)

#PROF_DATA = {}
#
#def profile(fn):
#    @wraps(fn)
#    def with_profiling(*args, **kwargs):
#        start_time = time.time()
#
#        ret = fn(*args, **kwargs)
#
#        elapsed_time = time.time() - start_time
#
#        if fn.__name__ not in PROF_DATA:
#            PROF_DATA[fn.__name__] = [0, []]
#        PROF_DATA[fn.__name__][0] += 1
#        PROF_DATA[fn.__name__][1].append(elapsed_time)
#
#        return ret
#
#    return with_profiling
#
#def print_prof_data():
#    for fname, data in PROF_DATA.items():
#        max_time = max(data[1])
#        avg_time = sum(data[1]) / len(data[1])
#        print "Function %s called %d times. " % (fname, data[0]),
#        print 'Execution time max: %.3f, average: %.3f' % (max_time, avg_time)
#
#def clear_prof_data():
#    global PROF_DATA
#    PROF_DATA = {}


def get_default_arg(default_value, arg):
    if arg is None:
        return default_value
    else:
        return arg

if __name__ == "__main__":
    # ./ distsim.py -h 72 -vma 16 -vmo 304 -vme 16
    #   -t planetlab-workload-traces/merkur_planetlab_haw-hamburg_de_ yale_p4p
    #   -o results/72-bla
    # ./ simuplot.py
#    parser = argparse.ArgumentParser(description='A VM distribution/placement simulator.')
#    parser.add_argument('-pm', '--pmcount', help='Number of physical machines (def: 64)', required=False)
#    parser.add_argument('-vm', '--vmcount', help='Number of VMs (def: 64)', required=False)
#    parser.add_argument('-cl', '--clock', help='', required=False)
#    parser.add_argument('-pa', '--pack', help='', required=False)
#    parser.add_argument('-clcb', '--clockcallback', help='', required=False)
#    #clock_callback = distsim.x.y.z.callback
#    #pack_callback = distsim.x.y.z.callback
#
#    parser.add_argument('-o', '--output', help='Output path', required=True)
#    parser.add_argument('-seu', '--simeu', help='Simulate Energy Unaware', required=False)
#    parser.add_argument('-sksp', '--simksp', help='Simulate Iterated-KSP', required=False)
#    parser.add_argument('-sec', '--simec', help='Simulate Iterated-EC', required=False)
#    args = parser.parse_args()
#
#    pmcount = int(get_default_arg(64, args.pmcount))
#    vmcount = int(get_default_arg(64, args.vmcount))
#    trace_file = get_default_arg('planetlab-workload-traces/merkur_planetlab_haw-hamburg_de_yale_p4p', args.vmtrace)
#    output_path = get_default_arg('results/path', args.output)
#    simulate_eu = bool(get_default_arg(0, args.simeu))
#    simulate_ksp = bool(get_default_arg(0, args.simksp))
#    simulate_ec = bool(get_default_arg(0, args.simec))

    start()
    s = Simulator()

#    if simulate_eu:
#        from distsim.strategies.energyunaware import EnergyUnawareStrategyPlacement
#        strategy = EnergyUnawareStrategyPlacement()
#        s.simulate_strategy(strategy, trace_file, pms_scenarios, vms_scenarios)
#
#    if simulate_ksp:
#        from distsim.strategies.iteratedksp import OpenOptStrategyPlacement
#        strategy = OpenOptStrategyPlacement()
#        s.simulate_strategy(strategy, trace_file, pms_scenarios, vms_scenarios)
#
#    if simulate_ec:
#        from distsim.strategies.iteratedec import EvolutionaryComputationStrategyPlacement
#        strategy = EvolutionaryComputationStrategyPlacement()
#        s.simulate_strategy(strategy, trace_file, pms_scenarios, vms_scenarios)

    print('done')
