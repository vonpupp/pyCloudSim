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
Virtual Machines Manager
"""
__version__ = "0.1"
__author__  = "Albert De La Fuente"

from distsim.model.tracegen import TraceGenerator
from itertools import islice
from distsim.model.virtualmachine import VirtualMachine

class VMManager:
    def __init__(self, trace_file, total_vm):
        tg = TraceGenerator(trace_file)
        trace = tg.gen_trace()
        self.items = []
        for t in islice(enumerate(trace), total_vm):
            self.items += [VirtualMachine(t[0], t[1][0], t[1][1], t[1][2], t[1][3])]

    def get_item_index(self, id):
        result = -1
        i = 0
        found = False
        while i < len(self.items) and not found:
            item = self.items[i]
            j = item.id
            found = j == id.id
            if found:
                result = i
            i += 1
        return result

    def get_item_values(self, id):
        result = self.get_item_index(id)
        if result is not -1:
            result = self.items[result]
        else:
            result = None
        return result

    def items_remove(self, remove_list):
        for to_delete in remove_list:
            i = self.get_item_index(to_delete)
            if i is not -1:
                del self.items[i]

    def __str__(self):
        result = 'VMPool['
        for item in self.items:
            result += str(item) + ', '
        result += ']'
        return result
