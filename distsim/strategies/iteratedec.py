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
Iterated EC Strategy Placement
"""
__version__ = "0.1"
__author__  = "Albert De La Fuente"


import inspyred
import random
import time

def my_generator(random, args):
    items = args['items']
    #print items
    return [random.choice([0]*99 + [1]) for _ in range(len(items))]

@inspyred.ec.evaluators.evaluator
def my_evaluator(candidate, args):
    items = args['items']
    totals = {}
    for metric in ['weight', 'cpu', 'mem', 'disk', 'net']:
        totals[metric] = sum([items[i][1][metric] for i, c in enumerate(candidate) if c == 1])
    constraints = [max(0, totals[c] - 99) for c in ['cpu', 'mem', 'disk', 'net']]
    fitness = totals['weight'] - sum(constraints)
    #print fitness
    return fitness

class EvolutionaryComputationStrategyPlacement:
    def __init__(self):
        self.constraints = None
        self.items = None
        self.itemstuples = None
        self.vmm = None
        self.pmm = None
        #self.gen_costraints(['cpu', 'mem', 'disk', 'net'])

    def gen_vms(self):
        self.itemstuples = [(i, {
                      'name': 'item %d' % i,
                      'weight': 1,
                      'cpu': vm.value['cpu'],
                      'mem': vm.value['mem'],
                      'disk': vm.value['disk'],
                      'net': vm.value['net'],
                      'n': 1
                 }) for i, vm in enumerate(self.items)]
        return self.itemstuples

    #def check_constraints(self, item_list):
    #    total_cpu = sum(map(operator.itemgetter('cpu'), item_list))
    #    total_mem = sum(map(operator.itemgetter('mem'), item_list))
    #    total_disk = sum(map(operator.itemgetter('disk'), item_list))
    #    total_net = sum(map(operator.itemgetter('net'), item_list))
    #    return (total_cpu < 100) and (total_mem < 100) and \
    #        (total_disk < 100) and (total_net < 100)
    #
    def get_vm_objects(self, items_list):
        result = []
        for item in items_list:
            result += [self.vmm.items[item]]#get_item_values(item)]
        return result
      
    def set_vmm(self, vmm):
        self.vmm = vmm
        self.items = self.vmm.items

    def solve_host(self):
        prng = random.Random()
        prng.seed(time.time())
        
        itemstuples = self.gen_vms()
        
        psize = 50
        tsize = 25
        evals = 2500
        
        ea = inspyred.ec.EvolutionaryComputation(prng)
        ea.selector = inspyred.ec.selectors.tournament_selection
        ea.variator = [inspyred.ec.variators.n_point_crossover, inspyred.ec.variators.bit_flip_mutation]
        ea.replacer = inspyred.ec.replacers.generational_replacement
        #ea.observer = inspyred.ec.observers.stats_observer
        ea.terminator = inspyred.ec.terminators.evaluation_termination
        final_pop = ea.evolve(my_generator, my_evaluator,
                              bounder=inspyred.ec.DiscreteBounder([0, 1]),
                              maximize=True,
                              pop_size=psize,
                              tournament_size=tsize,
                              num_selected=psize,
                              num_crossover_points=1,
                              num_elites=1,
                              max_evaluations=evals,
                              items=itemstuples
                              )
    
        best = max(final_pop)
        result = [i for i, c in enumerate(best.candidate) if c == 1]
        return result
