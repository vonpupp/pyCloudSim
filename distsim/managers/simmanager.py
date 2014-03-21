import datetime
import time
import csv
import pickle
import os
from manager import Manager
from distsim.analysis.louvain import *


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

    def csv_generate_graph(self, scenario, vmscount, fout):
        fh = open(fout, 'wb')
        writer = csv.writer(fh, delimiter='\t')
        hosts = self.results[scenario]['manager'].pmm.items


        n = Network()
        #for v1, v2 in [(1,2),(1,3),(1,10),(2,3),(4,5),(4,6),(4,10),(5,6),(7,8),(7,9),(7,10),(8,9)]:
        #for v1, v2 in [(1,5), (2,3), (2,4), (2,5), (3,5)]:
#        for v1, v2 in [(0,2),(0,3),(0,4),(0,5),(1,2),(1,4),(1,7),(2,4),(2,5),(2,6),(3,7),(4,10),(5,7),(5,11),(6,7),(6,11),
#                    (8,9),(8,10),(8,11),(8,14),(8,15),(9,12),(9,14),(10,11),(10,12),(10,13),(10,14),(11,13)]:
#            n.add_edge(v1, v2, 1)

        matrix = []
#        matrix = [[0]*vmscount]*vmscount
        for r in range(0, vmscount):
            matrix.append([0 for c in range(0, vmscount)])

        for host in hosts:
            for vm1 in host.vms:
                vm1id = int(vm1.id)
                for vm2 in host.vms:
                    vm2id = int(vm2.id)
                    if vm1id is not vm2id:
                        matrix[vm1id][vm2id] = matrix[vm1id][vm2id] + 1
                        matrix[vm2id][vm1id] = matrix[vm2id][vm1id] + 1
                        n.add_edge(vm1id, vm2id, 1)
            #result += row

#        print n
#        print n.size("edge"), 'edges'
#        print n.size("vertex"), 'vertices'

#        t = louvainmethod(n, True)
#        import ipdb; ipdb.set_trace() # BREAKPOINT

        header = [None] + [str(vm).zfill(2) for vm in range(0, vmscount)]
        writer.writerow(header)
        for vm, row in enumerate(matrix):
            writer.writerow([str(vm).zfill(2)] + row)
        fh.close()

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
                self.csv_generate_graph(scenario, vms, 'results/graph-{}-{}-{}-{}-{}.csv'.format(trace_filename, strategy.__class__.__name__, str(pms).zfill(3), str(vms).zfill(3), stamp))
                self.csv_append_scenario(scenario)
            self.csv_close_simulation()
        self.pickle_writer('results/pickle-{}.pkl'.format(stamp))
