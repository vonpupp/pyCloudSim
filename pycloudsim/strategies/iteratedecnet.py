import inspyred
import random
import time
import bisect
import collections
import math

#@functools.total_ordering
#class Lexicographic(object):
#    def __init__(self, values=None, maximize=True):
#        if values is None:
#            values = []
#        self.values = values
#        try:
#            iter(maximize)
#        except TypeError:
#            maximize = [maximize for v in values]
#        self.maximize = maximize
#
#    def __len__(self):
#        return len(self.values)
#
#    def __getitem__(self, key):
#        return self.values[key]
#
#    def __iter__(self):
#        return iter(self.values)
#
#    def __lt__(self, other):
#        for v, o, m in zip(self.values, other.values, self.maximize):
#            if m:
#                if v < o:
#                    return True
#                elif v > o:
#                    return False
#            else:
#                if v > o:
#                    return True
#                elif v < o:
#                    return False
#        return False
#
#    def __eq__(self, other):
#        return (self.values == other.values and self.maximize == other.maximize)
#
#    def __str__(self):
#        return str(self.values)
#
#    def __repr__(self):
#        return str(self.values)
def cdf(weights):
    total = sum(weights)
    result = []
    cumsum = 0
    for w in weights:
        cumsum += w
        result.append(cumsum / total)
    return result

def choice(population, weights):
    assert len(population) == len(weights)
    cdf_vals = cdf(weights)
    x = random.random()
    idx = bisect.bisect(cdf_vals, x)
    return population[idx]

def my_generator(random, args):
    items = args['items']
    #print items
    result = [random.choice([0]*99 + [1]) for _ in range(len(items))]
    return result

#    result = [[0] for _ in range(len(items))]
#    weights = [0.3, 0.4, 0.3]
#    population = 'ABC'
#    counts = collections.defaultdict(int)
#    counts[choice(population, weights)] += 1
#    print(counts)

@inspyred.ec.evaluators.evaluator
def my_evaluator(candidate, args):
    items = args['items']
    totals = {}
    resources = ['cpu', 'mem', 'disk', 'net']
    for metric in ['weight'] + resources:
        totals[metric] = 0
        for i, c in enumerate(candidate):
            if c == 1:
                totals[metric] += items[i][1][metric]
#        logging.debug('my_evaluator: totals[{}] = {}'.format(metric, totals[metric]))

    constraints = []
    for c in resources:
        constraints += [max(0, totals[c] - 99)]
#    logging.debug('my_evaluator: constraints = {}'.format(constraints))

    fitness = (totals['weight'] - sum(constraints))
#    logging.debug('my_evaluator: fitness1 = {}'.format(fitness))
#    if fitness > 0:
#        fitness *= math.pow(99 - totals['cpu'], 2)
    if fitness > 0:
#        resource_weights = ((totals['cpu'] * 1) + (totals['mem'] * 7) + \
#            (totals['disk'] * 1) + (totals['net'] * 1) / 100)
#        ratio = totals['weight'] / resource_weights
#        ratio = totals['weight'] * totals['net']  # Heuristic 7
#        ratio = totals['weight'] * (100 - totals['net'])  # Heuristic 8
        ratio = math.pow(100 - totals['net'], totals['weight'])  # Heuristic 9
        fitness = ratio
#        fitness = ratio * 10
#    logging.debug('my_evaluator: fitness2 = {}\n'.format(fitness))

    return fitness

class EvolutionaryComputationStrategyPlacementNet:
    def __init__(self):
        self.constraints = None
        self.items = None
        self.itemstuples = None
        self.vmm = None
        self.pmm = None
        #self.gen_costraints(['cpu', 'mem', 'disk', 'net'])

    def gen_vms(self):
        self.itemstuples = [(i, {
                      'name': 'item %d' % i,
                      'weight': 1,  # self.weight_function(vm.value['cpu']),
                      'cpu': vm.value['cpu'],
                      'mem': vm.value['mem'],
                      'disk': vm.value['disk'],
                      'net': vm.value['net'],
                      'n': 1
                 }) for i, vm in enumerate(self.items)]
        return self.itemstuples

    def weight_function1(self, value):
        result = 1
        if value > 90:
            result = 20
        elif value > 80:
            result = 15
        elif value > 70:
            result = 10
        elif value > 60:
            result = 1
        elif value > 50:
            result = 1
        elif value > 40:
            result = 1
        elif value > 30:
            result = 10
        elif value > 20:
            result = 15
        elif value > 10:
            result = 20
        else:
            result = 10

    #def check_constraints(self, item_list):
    #    total_cpu = sum(map(operator.itemgetter('cpu'), item_list))
    #    total_mem = sum(map(operator.itemgetter('mem'), item_list))
    #    total_disk = sum(map(operator.itemgetter('disk'), item_list))
    #    total_net = sum(map(operator.itemgetter('net'), item_list))
    #    return (total_cpu < 100) and (total_mem < 100) and \
    #        (total_disk < 100) and (total_net < 100)
    #
    def get_vm_objects(self, items_list):
        result = []
        for item in items_list:
            result += [self.vmm.items[item]]#get_item_values(item)]
        return result

    def set_vmm(self, vmm):
        self.vmm = vmm
        self.items = self.vmm.items

    def set_base_graph_name(self, base_graph_name):
        self.base_graph_name = base_graph_name

    def solve_host(self):
        prng = random.Random()
        prng.seed(time.time())

        itemstuples = self.gen_vms()

        psize = 50
        tsize = 25
        evals = 2500

        ea = inspyred.ec.EvolutionaryComputation(prng)
        ea.selector = inspyred.ec.selectors.tournament_selection
        ea.variator = [inspyred.ec.variators.n_point_crossover, inspyred.ec.variators.bit_flip_mutation]
        ea.replacer = inspyred.ec.replacers.generational_replacement
        #ea.observer = inspyred.ec.observers.stats_observer
        ea.terminator = inspyred.ec.terminators.evaluation_termination
        final_pop = ea.evolve(my_generator, my_evaluator,
                              bounder=inspyred.ec.DiscreteBounder([0, 1]),
                              maximize=True,
                              pop_size=psize,
                              tournament_size=tsize,
                              num_selected=psize,
                              num_crossover_points=1,
                              num_elites=1,
                              max_evaluations=evals,
                              items=itemstuples
                              )

        best = max(final_pop)
        result = [i for i, c in enumerate(best.candidate) if c == 1]
        return result
