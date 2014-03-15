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
Virtual Machine Model
"""
__version__ = "0.1"
__author__ = "Albert De La Fuente"


class VirtualMachine(dict):
    __count__ = 0

    def __init__(self, id, cpu_gen, mem_gen, disk_gen, net_gen):
        #id = uuid.uuid1()
        self.cpu_gen = cpu_gen
        self.mem_gen = mem_gen
        self.disk_gen = disk_gen
        self.net_gen = net_gen

        self.value = {}
        self.id = '%d' % id #VirtualMachine.__count__
        self.value['weight'] = 1
        self.value['cpu'] = cpu_gen.next()
        self.value['mem'] = mem_gen.next()
        self.value['disk'] = disk_gen.next()
        self.value['net'] = net_gen.next()
        self.value['n'] = 1
        self.value['placed'] = 0
        VirtualMachine.__count__ += 1

    def __str__(self):
        result = 'VM{}({}, {}, {}, {})'.format(
            self.id,
            self.value['cpu'],
            self.value['mem'],
            self.value['disk'],
            self.value['net'])
        return result

    def __getitem__(self, attribute):
        # http://stackoverflow.com/questions/5818192/getting-field-names-reflectively-with-python
        # val = getattr(ob, attr)
        if type(attribute) is str:
            ob = self.value
            result = ob[attribute]
            return result
        else:
            print('getitem: attribute is not a string, is:{}, value:{}'.format(type(attribute), attribute))
