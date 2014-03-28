from openopt import KSP

def gen_costraint(self, values, constraint):
    return values.value[constraint] < 99

def add_constraints(self, values, constraint_list):
    return [self.add_constraint(values, constraint) for constraint in constraint_list]

def add_constraint(values, constraint):
    # http://stackoverflow.com/questions/5818192/getting-field-names-reflectively-with-python
    # val = getattr(ob, attr)
    return values[constraint] < 99

def add_double_constraint(values, constraint):
    # http://stackoverflow.com/questions/5818192/getting-field-names-reflectively-with-python
    # val = getattr(ob, attr)
    return values[constraint] < 200

def add_constraints(values, constraint_list):
    return [add_constraint(values, constraint) for constraint in constraint_list]

class OpenOptStrategyPlacementNetGraph:
    def __init__(self):
        self.constraints = None
        self.items = None
        self.vmm = None
        self.pmm = None
        #self.items_count = items_count
        #self.hosts_count = hosts_count
        self.gen_costraints()

    def gen_costraints(self):
        self.constraints = lambda values: (
            values['cpu'] < 99,
            values['mem'] < 99,
            values['disk'] < 99,
            values['net'] < 99,
        )
#        self.constraints = lambda values: (
#            add_constraints(values, constraint_list),
#            add_double_constraint(values, 'mem')
#        )
#        import ipdb; ipdb.set_trace() # BREAKPOINT

    def get_vm_objects(self, items_list):
        result = []
        for item in items_list.xf:
            result += [self.vmm.items[item]]#get_item_values(item)]
        return result

    def set_vmm(self, vmm):
        self.vmm = vmm
        self.items = self.vmm.items
        #TODO: Remap items
        self.remap_items_weight()

    def set_base_graph_name(self, base_graph_name):
        self.base_graph_name = base_graph_name

    def remap_items_weight(self):
        if self.base_graph_name:
            # load graph
            # remap weights
            pass

    def solve_host(self):
        p = KSP('weight', self.items, constraints = self.constraints)
        result = p.solve('glpk', iprint = -1)
        return result
