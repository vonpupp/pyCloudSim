#!/usr/bin/python
# vim:ts=4:sts=4:sw=4:et:wrap:ai:fileencoding=utf-8:

import fnmatch
import os
import csv
import matplotlib.pyplot as plt
from matplotlib import pylab
#from matplotlib.font_manager import FontProperties
from matplotlib.patches import Polygon
from pylab import *
import numpy as np
import scipy as sp
import scipy.stats

dir = 'results'
pms_scenarios = [72] #range(10, 110, 10)


def fill_between(ax, x, y1, y2, **kwargs):
    # add x,y2 in reverse order for proper polygon filling
    verts = zip(x,y1) + [(x[i], y2[i]) for i in range(len(x)-1,-1,-1)]
    poly = Polygon(verts, **kwargs)
    ax.add_patch(poly)
    ax.autoscale_view()
    return poly

def do_error_bar(x, m, e, lw=2, w=2):
    wc = w/2
    o = plot([x-wc,x+wc], [m,m], color='b', lw=lw)
    o = plot([x,x], [m+e,m-e], color='b', lw=lw)
    o = plot([x-w,x+w], [m+e,m+e], color='r', lw=lw)
    o = plot([x-w,x+w], [m-e,m-e], color='g', lw=lw)
    
def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return m, h

def transposed(lists):
   if not lists: return []
   return map(lambda *row: list(row), *lists)

class GraphGenerator:
    def __init__(self, result_dir):
        self.data = None
        self.vms_scenarios = None
        self.result_dir = result_dir
        self.file_list = []
        
    def set_data(self, data):
        self.data = data
        self.vms_scenarios = self.data.itervalues().next().vms_scenarios

    #def get_experiments_file(self, scenario, patter='*'):
    #    self.file = None
    #    pattern = '{}-{}-*.csv'.format(patter, str(scenario))
    #    for file in os.listdir(dir):
    #        if fnmatch.fnmatch(file, pattern) and file not in self.file_list:
    #            self.file = file
    #    return self.file

    def legend(self, title):
        trans = {}
        trans['EnergyUnawareStrategyPlacement'] = 'Energy unaware'
        trans['OpenOptStrategyPlacement'] = 'Iterated-KSP'
        trans['EvolutionaryComputationStrategyPlacement'] = 'Iterated-EC'
        return trans[title]

    def vms_ticks(self, vms):
        result = ['{0:03d}'.format(i) for i in vms]
        return result


    def algorithms_comparison_figure(self, hosts_scenario, trace_file, case,
                 data_ref, data1, data2,
                 x_aspect, y_aspect,
                 x_title, y_title, title):
        x2 = map(int, self.remap_data(data_ref, x_aspect))
        y2a = self.remap_data(data_ref, y_aspect)
        y2b = self.remap_data(data1, y_aspect)
        y2c = self.remap_data(data2, y_aspect)
        
        #x2 = data_ref[x_aspect]
        #y2a = data_ref[y_aspect]
        #y2b = data1[y_aspect]
        #y2c = data2[y_aspect]
        
        fig, ax = plt.subplots()
        #self.remap_data(data_ref, 'strategy')
        ax.plot(x2, y2a, color='red', ls='-', marker='.', label=self.legend(data_ref[0]['strategy']))
        ax.plot(x2, y2b, color='blue', ls='-', marker='o', label=self.legend(data1[0]['strategy']))
        ax.plot(x2, y2c, color='green', ls='-', marker='s', label=self.legend(data2[0]['strategy']))
        #ax.fill(y2a, y2b, alpha=0.3)
        ax.set_xlabel(x_title, fontsize=18)
        ax.set_ylabel(y_title, fontsize=18)
        ax.set_title(title + ' (' + str(hosts_scenario) + ' hosts)')
        #ax.legend(loc=2); # upper left corner
        ax.xaxis.set_ticks(x2)
        pylab.xticks(x2, self.vms_ticks(x2), rotation='vertical', verticalalignment='top')
        
        ax = fig.gca()

        p = fill_between(ax, x2, y2a, y2b, facecolor='g')
        p.set_alpha(0.2)
        
        p = fill_between(ax, x2, y2b, y2c, facecolor='b')
        p.set_alpha(0.2)
        
        plt.grid(True)
        box = ax.get_position()
        #ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
        ax.set_position([box.x0, box.y0 + box.height * 0.2,
            box.width, box.height * 0.8])

        # Put a legend below current axis
        #ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=False, ncol=5)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
            fancybox=True, shadow=False, ncol=5)
        
        plt.savefig(self.result_dir + '/figure-' + trace_file + '-' +
            str(hosts_scenario).zfill(3) + '-' +
            title + '-' + case + '.png')
        plt.close()
        #return plt.savefig(self.result_dir + '/' + str(scenario) +
        #                   x_title + ' vs ' + y_title + '.png')
    
    def algorithms_comparison_figure_cases(self):
        self.algorithms_comparison_figure(
            self.hosts_scenario,
            self.trace_file,
            'best',
            self.data_eu.best_case,
            self.data_ksp.best_case,
            self.data_ec.best_case,
            self.x_key, self.y_key,
            self.x_title, self.y_title,
            self.title,
            )
        
        self.algorithms_comparison_figure(
            self.hosts_scenario,
            self.trace_file,
            'worst',
            self.data_eu.worst_case,
            self.data_ksp.worst_case,
            self.data_ec.worst_case,
            self.x_key, self.y_key,
            self.x_title, self.y_title,
            self.title,
            )
                
        self.algorithms_comparison_figure(
            self.hosts_scenario,
            self.trace_file,
            'average',
            self.data_eu.average_case,
            self.data_ksp.average_case,
            self.data_ec.average_case,
            self.x_key, self.y_key,
            self.x_title, self.y_title,
            self.title,
            )
        
    def algorithm_confidence_interval_figure(self, trace_file, algorithm,
                 data,
                 x_aspect, y_aspect,
                 x_title, y_title, title):
        
        reversed_data = transposed(data)

        fig, ax = plt.subplots()
        ax.set_xlabel(x_title, fontsize=18)
        ax.set_ylabel(y_title, fontsize=18)
        ax.set_title(title + ' (' + self.legend(algorithm) + ')')
        x = self.vms_scenarios
        ax.xaxis.set_ticks(x)
        pylab.xticks(x, self.vms_ticks(x), rotation='vertical', verticalalignment='top')
    
        ax = fig.gca()

        scenarios_series = []
        m_series = []
        upper_ci_series = []
        lower_ci_series = []
        vms_series = []
        
        plt.grid(True)
        for scenario in reversed_data:
            x_serie = []
            y_serie = []
            x = int(scenario[0][x_aspect])
            
            for repetition in scenario:
                y = float(repetition[y_aspect])
                scatter(x, y, s=1, color='k')
                #ax.plot(x, y, color='red', ls='-', marker='.')#, label=self.legend(data_ref[0]['strategy']))
                y_serie += [y]
                x_serie += [x]
            
            m, ci = mean_confidence_interval(y_serie)
            #scenarios_series += [scenario['#VM']]
            m_series += [m]
            upper_ci_series += [m+ci]
            lower_ci_series += [m-ci]
            vms_series += [x_serie[0]]
            #ax.plot(x_serie[0], m, color='red', ls='-', marker='.', label=self.legend(algorithm))
            
            do_error_bar(x, m, ci, 1, 4)
            #print(x_serie)
            #print(y_serie)
            #print(m)
            #print(ci)
            
        print vms_series
        print m_series
        ax.plot(vms_series, m_series, color='blue', ls='-', marker='.', label=self.legend(algorithm))
        ax.plot(vms_series, upper_ci_series, color='red', ls='-.', marker='.', label=self.legend(algorithm))
        ax.plot(vms_series, lower_ci_series, color='green', ls='-.', marker='.', label=self.legend(algorithm))
#        ax.plot(x2, y2b, color='blue', ls='-', marker='o', label=self.legend(data1[0]['strategy']))
        
        #plt.show()
        plt.savefig(self.result_dir + '/figure-' + trace_file + '-' +
            title + '-' + algorithm + '.png')
#        plt.savefig('test.png')
        plt.close()
        
    def algorithms_confidence_interval_figure_cases(self):
        self.algorithm_confidence_interval_figure(
            #self.hosts_scenario,
            self.trace_file,
            'EnergyUnawareStrategyPlacement',
            self.data_eu.data,
            self.x_key, self.y_key,
            self.x_title, self.y_title,
            self.title,
        )
        
        self.algorithm_confidence_interval_figure(
            #self.hosts_scenario,
            self.trace_file,
            'OpenOptStrategyPlacement',
            self.data_ksp.data,
            self.x_key, self.y_key,
            self.x_title, self.y_title,
            self.title,
        )
        
        self.algorithm_confidence_interval_figure(
            #self.hosts_scenario,
            self.trace_file,
            'EvolutionaryComputationStrategyPlacement',
            self.data_ec.data,
            self.x_key, self.y_key,
            self.x_title, self.y_title,
            self.title,
        )
        
    def remap_data(self, list_dict, key):
        l = {}
        for item in list_dict:
            try:
                l += [item[key]]
            except:
                l = [item[key]]
        return l
        
    def plot_all_algorithm_comparison(self, hosts_scenario, trace_file):
        #reference = self.get_experiments_file(scenario, 'EnergyUnawareStrategyPlacement')
        #method1 = self.get_experiments_file(scenario, 'OpenOptStrategyPlacement')
        #method2 = self.get_experiments_file(scenario, 'EvolutionaryComputationStrategyPlacement')
        #data_ref = self.load_csv_data(reference)
        #data1 = self.load_csv_data(method1)
        #data2 = self.load_csv_data(method2)
        #
        #x1 = data_ref['virtual_mahines_count']
        #y1a = data_ref['virtual_machines_placed']
        #y1b = data1['virtual_machines_unplaced']
        
        self.hosts_scenario = hosts_scenario
        self.trace_file = trace_file
        
        self.data_eu = self.data['EnergyUnawareStrategyPlacement']
        self.data_ksp = self.data['OpenOptStrategyPlacement']
        self.data_ec = self.data['EvolutionaryComputationStrategyPlacement']
        self.x_key = '#VM'
        self.x_title = 'Number of VMs'
        
        self.y_key = 'KW'
        self.y_title = 'Energy consumed (Watts)'
        self.title = 'Energy consumption comparison'
        self.algorithms_comparison_figure_cases()
        
        self.y_key = 'T'
        self.y_title = 'Time (seconds)'
        self.title = 'Time comparison'
        self.algorithms_comparison_figure_cases()
        
        self.y_key = '#PM-U'
        self.y_title = 'No. physical machines used'
        self.title = 'Used physical machines comparison'
        self.algorithms_comparison_figure_cases()
        
        self.y_key = '#PM-U'
        self.y_title = 'No. physical machines used'
        self.title = 'Used physical machines comparison'
        self.algorithms_comparison_figure_cases()
        
        self.y_key = '#PM-S'
        self.y_title = 'No. physical machines suspended'
        self.title = 'Suspended physical machines comparison'
        self.algorithms_comparison_figure_cases()
        
        self.y_key = '#PM-I'
        self.y_title = 'No. physical machines idle'
        self.title = 'Idle physical machines comparison'
        self.algorithms_comparison_figure_cases()
        
        self.y_key = '#VM-P'
        self.y_title = 'No. virtual machines placed'
        self.title = 'Placed VMs comparison'
        self.algorithms_comparison_figure_cases()
        
        self.y_key = 'VM-U'
        self.y_title = 'No. virtual machines not placed'
        self.title = 'Unplaced VMs comparison'
        self.algorithms_comparison_figure_cases()
        
    def plot_all_confidence_interval_comparison(self, trace_file):
        self.trace_file = trace_file
        self.data_eu = self.data['EnergyUnawareStrategyPlacement']
        self.data_ksp = self.data['OpenOptStrategyPlacement']
        self.data_ec = self.data['EvolutionaryComputationStrategyPlacement']
        
        self.x_key = '#VM'
        self.x_title = 'Number of VMs'
        
        self.y_key = 'KW'
        self.y_title = 'Energy consumed (Watts) 95% C.I.'
        self.title = 'Energy consumption - 95 percent C.I.' #'Energy consumption - 95% Confidence Interval for 30 simulations'
        self.algorithms_confidence_interval_figure_cases()
        
        self.y_key = 'T'
        self.y_title = 'Time (Seconds) 95% C.I.'
        self.title = 'Time - 95 percent C.I.' #'Energy consumption - 95% Confidence Interval for 30 simulations'
        self.algorithms_confidence_interval_figure_cases()
        
        self.y_key = '#PM-S'
        self.y_title = 'Suspended physical machines 95% C.I.'
        self.title = 'Suspended physical machines - 95 percent C.I.' #'Energy consumption - 95% Confidence Interval for 30 simulations'
        self.algorithms_confidence_interval_figure_cases()
        
        #result['physical_mahines_count'].append(int(row[0]))
        #result['virtual_mahines_count'].append(int(row[1]))
        #result['physical_machines_used'].append(int(row[2]))
        #result['physical_machines_suspended'].append(int(row[3]))
        #result['physical_machines_idle'].append(int(row[4]))
        #result['virtual_machines_placed'].append(int(row[5]))
        #result['virtual_machines_unplaced'].append(int(row[6]))
        #result['energy_consumed'].append(float(row[7]))
        #result['strategy'].append(row[8])
        #result['elapsed_time'].append(float(row[9]))
        
#        method2 = self.get_experiments_files('EnergyUnaware*')

if __name__ == '__main__':
    #gg = GraphGenerator(dir, pms_scenarios)
    #gg.create_comparison_graph()
    pass

