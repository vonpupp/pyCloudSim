#!/usr/bin/env python
# vim:ts=4:sts=4:sw=4:et:wrap:ai:fileencoding=utf-8:
#
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
Trace Generator Model
"""
__version__ = "0.1"
__author__  = "Albert De La Fuente"


import collections
#import matplotlib.pyplot as plt

factor = 1/4

class TraceGenerator():
  
      
    def __init__(self, fname):
        #fname='planetlab-selected/planetlab-20110420-filtered_pluto_cs_brown_edu_root'
        #fname='planetlab-workload-traces/merkur_planetlab_haw-hamburg_de_ yale_p4p'
        self.fname = fname
        with open(self.fname) as f:
            self.lines = f.readlines()
            self.cpu = map(int, self.lines)
      
    def gen_cpu_trace(self):
        return self.cpu

    def gen_mem_trace(self):
        self.mem = collections.deque(self.cpu)
        self.mem.rotate(len(self.cpu)/4)
        return self.mem

    def gen_disk_trace(self):
        self.disk = collections.deque(self.cpu)
        self.disk.rotate(2*len(self.cpu)/4)
        return self.disk

    def gen_net_trace(self):
        self.net = collections.deque(self.cpu)
        self.net.rotate(3*len(self.cpu)/4)
        return self.net
      
    def gen_trace(self):
        self.gen_cpu_trace()
        self.gen_mem_trace()
        self.gen_disk_trace()
        self.gen_net_trace()
        self.trace = zip(self.cpu, self.mem, self.disk, self.net)
        return self.trace

#tg = TraceGenerator()
#cpu = tg.gen_cpu_trace()
#mem = tg.gen_mem_trace()
#disk = tg.gen_disk_trace()
#net = tg.gen_net_trace()
#trace = zip(cpu, mem, disk, net)

#print trace
#plt.bar(range(0,len(cpu)), cpu)
#plt.show()