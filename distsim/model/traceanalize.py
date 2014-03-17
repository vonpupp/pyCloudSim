#!/usr/bin/env python
# vim:ts=4:sts=4:sw=4:et:wrap:ai:fileencoding=utf-8:

import collections
import numpy as np
import csv


class TraceAnalize():
    def __init__(self):
        #fname='planetlab-selected/planetlab-20110420-filtered_pluto_cs_brown_edu_root'
        #fname='planetlab-workload-traces/merkur_planetlab_haw-hamburg_de_ yale_p4p'
        pass

    def analyze(self, fname):
        self.fname = fname
        with open(self.fname) as f:
            self.lines = f.readlines()
            self.trace = map(int, self.lines)

        self.sum = sum(self.trace)

        self.amin = np.amin(self.trace)
        self.amax = np.amax(self.trace)
        self.nanmin = np.nanmin(self.trace)
        self.nanmax = np.nanmax(self.trace)
        self.ptp = np.ptp(self.trace)
        self.percentile10 = np.percentile(self.trace, 10)

        self.average = np.average(self.trace)
        self.mean = np.mean(self.trace)
        self.median = np.median(self.trace)
        self.std = np.std(self.trace)
        self.var = np.var(self.trace)
        self.media = float(self.sum) / float(len(self.trace))
        #print('sum = {}, media = {}, average = {}'.format(self.sum, self.media, self.average))

    def csv_write_header(self, fout):
        self.out_file = open(fout, 'wb')
        #out_file = open(fout, 'a+')
        self.writer = csv.writer(self.out_file, delimiter='\t')
        header = ['file', 'sum', 'amin', 'amax', 'nanmin', 'nanmax', 'ptp',
            'percentile10',
#            'mode',
            'mean', 'median', 'std', 'var']
        self.writer.writerow(header)

    def csv_append_row(self):
        self.writer.writerow([self.fname,
            self.sum,
            self.amin,
            self.amax,
            self.nanmin,
            self.nanmax,
            self.ptp,
            self.percentile10,
#            self.mode,
            self.mean,
            self.median,
            self.std,
            self.var])

    def csv_close(self):
        self.out_file.close()
