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
Distsim :: a VM distribution simulator
"""
__version__ = "0.1"
__author__  = "Albert De La Fuente"

import copy
import random
import operator


class EnergyUnawareStrategyPlacement:
    def __init__(self):
        self.constraints = None
        self.items = None
        self.vmm = None
        self.pmm = None
        self.gen_costraints(['cpu', 'mem', 'disk', 'net'])

    def gen_costraints(self, constraint_list):
        self.constraints = lambda values: (
            add_constraints(values, constraint_list)
        )
    
    def check_constraints(self, item_list):
        total_cpu = sum(map(operator.itemgetter('cpu'), item_list))
        total_mem = sum(map(operator.itemgetter('mem'), item_list))
        total_disk = sum(map(operator.itemgetter('disk'), item_list))
        total_net = sum(map(operator.itemgetter('net'), item_list))
        return (total_cpu < 100) and (total_mem < 100) and \
            (total_disk < 100) and (total_net < 100)

    def get_vm_objects(self, items_list):
        return items_list
      
    def set_vmm(self, vmm):
        self.vmm = vmm
        self.items = self.vmm.items

    def solve_host(self):
        result = []
        items_list = []
        more = True
        #tmp = self.vmm.items.copy()
        tmp = copy.deepcopy(self.vmm.items)
        done = False
        while not done:
            index = random.randrange(len(tmp))
            vm = tmp.pop(index)
            more = self.check_constraints(items_list + [vm])
            if more:
                #result += [vm.id]
                result += [vm]
                items_list += [vm]
            else:
                tmp.append(vm)
            done = not more or (len(tmp) == 0)
        return result
