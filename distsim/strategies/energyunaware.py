import copy
import random
import operator


class EnergyUnawareStrategyPlacement:
    def __init__(self):
        self.constraints = None
        self.items = None
        self.vmm = None
        self.pmm = None
        self.gen_costraints(['cpu', 'mem', 'disk', 'net'])

    def gen_costraints(self, constraint_list):
        self.constraints = lambda values: (
            add_constraints(values, constraint_list)
        )

    def check_constraints(self, item_list):
        total_cpu = sum(map(operator.itemgetter('cpu'), item_list))
        total_mem = sum(map(operator.itemgetter('mem'), item_list))
        total_disk = sum(map(operator.itemgetter('disk'), item_list))
        total_net = sum(map(operator.itemgetter('net'), item_list))
        return (total_cpu < 100) and (total_mem < 100) and \
            (total_disk < 100) and (total_net < 100)

    def get_vm_objects(self, items_list):
        return items_list

    def set_vmm(self, vmm):
        self.vmm = vmm
        self.items = self.vmm.items

    def set_base_graph_name(self, base_graph_name):
        self.base_graph_name = base_graph_name

    def solve_host(self):
        result = []
        items_list = []
        more = True
        #tmp = self.vmm.items.copy()
        tmp = copy.deepcopy(self.vmm.items)
        done = False
        while not done:
            index = random.randrange(len(tmp))
            vm = tmp.pop(index)
            more = self.check_constraints(items_list + [vm])
            if more:
                #result += [vm.id]
                result += [vm]
                items_list += [vm]
            else:
                tmp.append(vm)
            done = not more or (len(tmp) == 0)
        return result
