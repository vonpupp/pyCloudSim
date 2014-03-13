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
Physical Machine Model
"""
__version__ = "0.1"
__author__  = "Albert De La Fuente"


class PhysicalMachine:
    __count__ = 0
    def __init__(self, id):
        self.id = '%d' % id # self.__count__
        self.vms = []
        self.startup_machine()
        PhysicalMachine.__count__ += 1
        
    def startup_machine(self):
        self.cpu = 15
        self.mem = 15
        self.disk = self.net = 0
        self.suspended = False

    def consumed_power(self):
        pass
    
    def place_vm(self, vm):
        self.vms.append(vm)
        vm.value['placed'] = 1
        self.cpu = self.mem = 0
        self.disk = self.net = 0
        for vm in self.vms:
            self.cpu += vm.value['cpu']
            self.mem += vm.value['mem']
            self.disk += vm.value['disk']
            self.net += vm.value['net']
    
    def vms_to_str(self):
        result = ''
        for vm in self.vms:
            result += str(vm) + ', '
        return result
    
    def __str__(self):
        if self.suspended:
            state = 'sus'
        else:
            state = 'run'
        result = 'PM[{}-{}/{}]({}, {}, {}, {}) | [{}/{}]'.format(
            self.id,
            state,
            self.estimate_consumed_power(),
            self.cpu,
            self.mem,
            self.disk,
            self.net,
            len(self.vms),
            self.vms_to_str())
        return result
    
    def suspend(self):
        self.suspended = True
        self.cpu = 0
        self.mem = 0
        self.disk = 0
        self.net = 0
        
    def wol(self):
        self.startup_machine()
    
    def estimate_consumed_power(self):
        if self.suspended:
            result = 5
        else:
            # P(cpu) = P_idle + (P_busy - P_idle) x cpu
            p_idle = 114.0
            p_busy = 250.0
            result = p_idle + (p_busy - p_idle) * self.cpu/100
            #if self.vms != []:
            #    p_idle = 114.0
            #    p_busy = 250.0
            #    result = p_idle + (p_busy - p_idle) * self.cpu/100
            #else:
            #    pass
        return result
