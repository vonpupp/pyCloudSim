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
        elif self.fname == 'hybrid2':
           self.gen_hybrid2()
        elif self.fname == 'hybrid3':
           self.gen_hybrid3()
        elif self.fname == 'hybrid4':
           self.gen_hybrid4()
        elif self.fname == 'hybrid5':
           self.gen_hybrid5()
        elif self.fname == 'hybrid6':
           self.gen_hybrid6()
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

    # CPU: T1
    # MEM: T3
    # DISK: T2
    # NET: T4
    # Conclusion: Notable optimization with ksp-mem
    def gen_hybrid1(self):  # T1 T3 T2 T4
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

    # CPU: T3
    # MEM: T1
    # DISK: T2
    # NET: T1 (shifted)
    # Conclusion:
    def gen_hybrid2(self):
        self.fname = '../planetlab-workload-traces/20110420/plgmu4_ite_gmu_edu_rnp_dcc_ufjf'
        self.trace_loader()
        self.cpu = map(int, self.lines)
        self.fname = '../planetlab-workload-traces/20110409/146-179_surfsnel_dsl_internl_net_root'
        self.trace_loader()
        self.mem = map(int, self.lines)
        self.fname = '../planetlab-workload-traces/20110409/host4-plb_loria_fr_uw_oneswarm'
        self.trace_loader()
        self.disk = map(int, self.lines)
        self.fname = '../planetlab-workload-traces/20110409/146-179_surfsnel_dsl_internl_net_root'
        self.trace_loader()
        self.net = map(int, self.lines)
        self.net.rotate(3*len(self.cpu)/4)

    # CPU: New with mean 15, std 7.31 and var 53.51
    # MEM: T1
    # DISK: T2
    # NET: T1 (shifted)
    # Conclusion:
    def gen_hybrid3(self):
        self.fname = '../planetlab-workload-traces/20110322/planetlab1_williams_edu_uw_oneswarm'
        self.trace_loader()
        self.cpu = map(int, self.lines)
        self.fname = '../planetlab-workload-traces/20110409/146-179_surfsnel_dsl_internl_net_root'
        self.trace_loader()
        self.mem = map(int, self.lines)
        self.fname = '../planetlab-workload-traces/20110409/host4-plb_loria_fr_uw_oneswarm'
        self.trace_loader()
        self.disk = map(int, self.lines)
        self.fname = '../planetlab-workload-traces/20110409/146-179_surfsnel_dsl_internl_net_root'
        self.trace_loader()
        self.net = map(int, self.lines)
        self.net.rotate(3*len(self.cpu)/4)

    # CPU: New with mean 15, std 7.31 and var 53.51
    # MEM: T3
    # DISK: Same as CPU (shifted)
    # NET: T1 (shifted)
    # Conclusion:
    def gen_hybrid4(self):
        self.fname = '../planetlab-workload-traces/20110322/planetlab1_williams_edu_uw_oneswarm'
        self.trace_loader()
        self.cpu = map(int, self.lines)
        self.fname = '../planetlab-workload-traces/20110420/plgmu4_ite_gmu_edu_rnp_dcc_ufjf'
        self.trace_loader()
        self.mem = map(int, self.lines)
        self.fname = '../planetlab-workload-traces/20110322/planetlab1_williams_edu_uw_oneswarm'
        self.trace_loader()
        self.disk = map(int, self.lines)
        self.disk.rotate(3*len(self.cpu)/4)
        self.fname = '../planetlab-workload-traces/20110409/146-179_surfsnel_dsl_internl_net_root'
        self.trace_loader()
        self.net = map(int, self.lines)
        self.net.rotate(3*len(self.cpu)/4)

    # CPU: New with mean 25 std 6 and var 37
    # MEM: T3
    # DISK: Same as CPU (shifted)
    # NET: mean 15
    # Conclusion:
    def gen_hybrid5(self):
        self.fname = '../planetlab-workload-traces/20110322/planetlab2_millennium_berkeley_edu_root'
        self.trace_loader()
        self.cpu = map(int, self.lines)
        self.fname = '../planetlab-workload-traces/20110420/plgmu4_ite_gmu_edu_rnp_dcc_ufjf'
        self.trace_loader()
        self.mem = map(int, self.lines)
        self.fname = '../planetlab-workload-traces/20110322/planetlab1_williams_edu_uw_oneswarm'
        self.trace_loader()
        self.disk = map(int, self.lines)
        self.disk.rotate(3*len(self.cpu)/4)
        self.fname = '../planetlab-workload-traces/20110409/146-179_surfsnel_dsl_internl_net_root'
        self.trace_loader()
        self.net = map(int, self.lines)
        self.net.rotate(3*len(self.cpu)/4)

    # CPU: New with mean 25 std 6 and var 37
    # MEM: T3
    # DISK: Same as CPU (shifted)
    # NET: mean 15
    # Conclusion:
    def gen_hybrid6(self):
        self.fname = '../planetlab-workload-traces/20110322/planetlab1_williams_edu_uw_oneswarm'
        self.trace_loader()
        self.cpu = map(int, self.lines)
        self.fname = '../planetlab-workload-traces/20110322/planetlab2_millennium_berkeley_edu_root'
        self.trace_loader()
        self.mem = map(int, self.lines)
        self.fname = '../planetlab-workload-traces/20110322/planetlab1_williams_edu_uw_oneswarm'
        self.trace_loader()
        self.disk = map(int, self.lines)
        self.disk.rotate(3*len(self.cpu)/4)
        self.fname = '../planetlab-workload-traces/20110409/146-179_surfsnel_dsl_internl_net_root'
        self.trace_loader()
        self.net = map(int, self.lines)
        self.net.rotate(3*len(self.cpu)/4)
