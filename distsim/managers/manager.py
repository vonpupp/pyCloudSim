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
Manager framework
"""
__version__ = "0.1"
__author__  = "Albert De La Fuente"


from pmmanager import PMManager
from vmmanager import VMManager
from distsim.strategies.energyunaware import EnergyUnawareStrategyPlacement

class Manager:
    def __init__(self):
        self.placement = []
        self.total_pm = 0
        self.total_vm = 0
        self.vmm = None
        self.pmm = None
        self.strategy = None

    def set_vm_count(self, trace_file, total_vm):
        self.total_vm = total_vm
        self.vmm = VMManager(trace_file, total_vm)

    def set_pm_count(self, total_pm):
        self.total_pm = total_pm
        self.pmm = PMManager(total_pm)
        
    def set_strategy(self, strategy):
        self.strategy = strategy
        self.strategy.set_vmm(self.vmm)
        self.strategy.pmm = self.pmm
      
    def place_vms(self, vms, host):
        i = 0
        while i < len(vms):
            vm = vms[i]
            host.place_vm(vm)
            print('{}'.format(host))
            i += 1
        self.vmm.items_remove(vms)

    def placed_vms(self):
        result = 0
        for host in self.pmm.items:
            result += len(host.vms)
        return result
      
    def unplaced_vms(self):
        return self.total_vm - self.placed_vms()
      
    def solve_hosts(self):
        for host in self.pmm.items:
            if self.vmm.items != []:
                solution = self.strategy.solve_host()
                vms = self.strategy.get_vm_objects(solution)
                if vms is not None:
                    self.place_vms(vms, host)
            else:
                if not isinstance(self.strategy, EnergyUnawareStrategyPlacement):
                    host.suspend()
                print(host)
        
    def calculate_power_consumed(self):
        result = 0
        for host in self.pmm.items:
            result += host.estimate_consumed_power()
        return result
    
    def calculate_physical_hosts_used(self):
        result = 0
        for host in self.pmm.items:
            if host.vms != []:
                result += 1
        return result
    
    def calculate_physical_hosts_suspended(self):
        result = 0
        for host in self.pmm.items:
            if host.suspended:
                result += 1
        return result
    
    def calculate_physical_hosts_idle(self):
        result = 0
        for host in self.pmm.items:
            if host.vms == [] and not host.suspended:
                result += 1
        return result
