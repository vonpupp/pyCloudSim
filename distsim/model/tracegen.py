#!/usr/bin/env python
# vim:ts=4:sts=4:sw=4:et:wrap:ai:fileencoding=utf-8:

import collections
#import matplotlib.pyplot as plt

factor = 1/4

class TraceGenerator():


    def __init__(self, fname):
        #fname='planetlab-selected/planetlab-20110420-filtered_pluto_cs_brown_edu_root'
        #fname='planetlab-workload-traces/merkur_planetlab_haw-hamburg_de_ yale_p4p'
        self.fname = fname

    def gen_cpu_trace(self):
#        with open(self.fname) as f:
#            self.lines = f.readlines()
        self.trace_loader()
        self.cpu = map(int, self.lines)
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
        if self.fname == 'hybrid1':
           self.gen_hybrid1()
        else:
            self.gen_cpu_trace()
            self.gen_mem_trace()
            self.gen_disk_trace()
            self.gen_net_trace()
        self.trace = zip(self.cpu, self.mem, self.disk, self.net)
        return self.trace

    def trace_loader(self):
        with open(self.fname) as f:
            self.lines = f.readlines()

    def gen_hybrid1(self):
        self.fname = '../planetlab-workload-traces/20110409/146-179_surfsnel_dsl_internl_net_root'
        self.trace_loader()
        self.cpu = map(int, self.lines)
        self.fname = '../planetlab-workload-traces/20110420/plgmu4_ite_gmu_edu_rnp_dcc_ufjf'
        self.trace_loader()
        self.mem = map(int, self.lines)
        self.fname = '../planetlab-workload-traces/20110409/host4-plb_loria_fr_uw_oneswarm'
        self.trace_loader()
        self.disk = map(int, self.lines)
        self.fname = '../planetlab-workload-traces/20110309/planetlab1_fct_ualg_pt_root'
        self.trace_loader()
        self.net = map(int, self.lines)
#        self.trace = zip(self.cpu, self.mem, self.disk, self.net)
#        return self.trace

#tg = TraceGenerator()
#cpu = tg.gen_cpu_trace()
#mem = tg.gen_mem_trace()
#disk = tg.gen_disk_trace()
#net = tg.gen_net_trace()
#trace = zip(cpu, mem, disk, net)

#print trace
#plt.bar(range(0,len(cpu)), cpu)
#plt.show()
