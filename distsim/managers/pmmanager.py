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
Physical Machines Manager
"""
__version__ = "0.1"
__author__  = "Albert De La Fuente"


from distsim.model.phisicalmachine import PhysicalMachine

class PMManager:
    def __init__(self, total_pm):
        self.items = [PhysicalMachine(i)
                          for i in range(total_pm)]

    def __str__(self):
        result = 'PMPool['
        for item in self.items:
            result += str(item) + ', '
        result += ']'
        return result