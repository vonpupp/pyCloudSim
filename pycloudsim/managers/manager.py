from pmmanager import PMManager
from vmmanager import VMManager
from pycloudsim.strategies.energyunaware import EnergyUnawareStrategyPlacement

class Manager:
    def __init__(self):
        self.placement = []
        self.total_pm = 0
        self.total_vm = 0
        self.vmm = None
        self.pmm = None
        self.strategy = None

    def set_vm_count(self, trace_file, total_vm):
        self.total_vm = total_vm
        self.vmm = VMManager(trace_file, total_vm)

    def set_pm_count(self, total_pm):
        self.total_pm = total_pm
        self.pmm = PMManager(total_pm)

    def set_strategy(self, strategy):
        self.strategy = strategy
        if self.base_graph_name:
            self.strategy.set_base_graph_name(self.base_graph_name)
        self.strategy.set_vmm(self.vmm)
        self.strategy.pmm = self.pmm

    def place_vms(self, vms, host):
        i = 0
        while i < len(vms):
            vm = vms[i]
            host.place_vm(vm)
            print('{}'.format(host))
            i += 1
        self.vmm.items_remove(vms)

    def placed_vms(self):
        result = 0
        for host in self.pmm.items:
            result += len(host.vms)
        return result

    def unplaced_vms(self):
        return self.total_vm - self.placed_vms()

    def solve_hosts(self):
        for host in self.pmm.items:
            if self.vmm.items != []:
                solution = self.strategy.solve_host()
                vms = self.strategy.get_vm_objects(solution)
                #import ipdb; ipdb.set_trace() # BREAKPOINT
                if vms is not None:
                    self.place_vms(vms, host)
            else:
                if not isinstance(self.strategy, EnergyUnawareStrategyPlacement):
                    host.suspend()
                print(host)

    def calculate_power_consumed(self):
        result = 0
        for host in self.pmm.items:
            result += host.estimate_consumed_power()
        return result

    def calculate_physical_hosts_used(self):
        result = 0
        for host in self.pmm.items:
            if host.vms != []:
                result += 1
        return result

    def calculate_physical_hosts_suspended(self):
        result = 0
        for host in self.pmm.items:
            if host.suspended:
                result += 1
        return result

    def calculate_physical_hosts_idle(self):
        result = 0
        for host in self.pmm.items:
            if host.vms == [] and not host.suspended:
                result += 1
        return result
