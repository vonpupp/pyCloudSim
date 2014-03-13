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
Simulation Manager
"""
__version__ = "0.1"
__author__  = "Albert De La Fuente"


import datetime
import time
import csv
import pickle
import os
from manager import Manager


class Simulator:
    def __init__(self):
        self.results = []
        self.writer = None
    
    def csv_write_simulation(self, fout):
        self.out_file = open(fout, 'wb')
        #out_file = open(fout, 'a+')
        
        self.writer = csv.writer(self.out_file, delimiter='\t')
        header = ['#PM', '#VM',
                  '#PM-U', '#PM-S', '#PM-I',
                  '#VM-P', 'VM-U',
                  'KW',
                  'strategy',
                  #'ST', 'ET',
                  'T']
        self.writer.writerow(header)
        
    def csv_append_scenario(self, scenario):
        #for r in self.results:
        r = self.results[scenario]
        self.writer.writerow([r['physical_mahines_count'], r['virtual_mahines_count'],
              r['physical_machines_used'],
              r['physical_machines_suspended'],
              r['physical_machines_idle'],
              r['virtual_machines_placed'], r['virtual_machines_unplaced'],
              r['energy_consumed'],
              r['strategy'].__class__.__name__,
              #r['start_time'], r['end_time'],
              r['elapsed_time']])
        
    def csv_close_simulation(self):
        self.out_file.close()
        
    def pickle_writer(self, fout):
        try:
            out_file = open(fout, 'wb')
            pickle.dump(self.results, out_file)
        except:
            pass
        
    def simulate_scenario(self, strategy, trace_file, pms, vms):
        result = {}
        result['start_time'] = time.time()
        result['manager'] = m = Manager()
        result['physical_mahines_count'] = pms
        m.set_pm_count(pms)
        result['virtual_mahines_count'] = vms
        m.set_vm_count(trace_file, vms)
        result['strategy'] = strategy
        m.set_strategy(strategy)
        m.solve_hosts()
        result['placement'] = m.pmm
        result['energy_consumed'] = m.calculate_power_consumed()
        result['physical_machines_used'] = m.calculate_physical_hosts_used()
        result['physical_machines_idle'] = m.calculate_physical_hosts_idle()
        result['physical_machines_suspended'] = m.calculate_physical_hosts_suspended()
        result['virtual_machines_placed'] = m.placed_vms()
        result['virtual_machines_unplaced'] = m.unplaced_vms()
        result['end_time'] = time.time()
        result['elapsed_time'] = result['end_time'] - result['start_time']
        self.results.append(result)
        return len(self.results)-1

    def simulate_strategy(self, strategy, trace_file, pms_scenarios, vms_scenarios):
        stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d-%H%M%S')
        #strategy = EnergyUnawareStrategyPlacement()
        trace_filename = os.path.basename(trace_file)
        for pms in pms_scenarios:
            self.csv_write_simulation('results/simulation-{}-{}-{}-{}.csv'.format(trace_filename, strategy.__class__.__name__, str(pms).zfill(3), stamp))
            for vms in vms_scenarios:
                scenario = self.simulate_scenario(strategy, trace_file, pms, vms)
                self.csv_append_scenario(scenario)
            self.csv_close_simulation()
        self.pickle_writer('results/pickle-{}.pkl'.format(stamp))
