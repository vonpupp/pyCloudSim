from pycloudsim.globals.pmmanager import PMManager
from vmmanager import VMManager
#from distsim.strategies.energyunaware import EnergyUnawareStrategyPlacement
from pycloudsim.config import *
import pycloudsim.common as common
from pycloudsim.classes.repeatedtimer import RepeatedTimer
import time


class ManagerTemplateClass:
    def __init__(self):
        pass

    def start(init_state, execute, config, time_interval, iterations=-1):
        """ Start the processing loop.

        :param init_state: A function accepting a config and
                        returning a state dictionary.
        :type init_state: function

        :param execute: A function performing the processing at each iteration.
        :type execute: function

        :param config: A config dictionary.
        :type config: dict(str: *)

        :param time_interval: The time interval to wait between iterations.
        :type time_interval: int

        :param iterations: The number of iterations to perform, -1 for infinite.
        :type iterations: int

        :return: The final state.
        :rtype: dict(str: *)
        """
        state = init_state(config)
        interval = int(config['tiks'])
        rt = RepeatedTimer(interval, execute, state)

#        if iterations == -1:
#            while True:
#                state = execute(config, state)
##                time.sleep(time_interval)
#        else:
#            for _ in xrange(iterations):
#                state = execute(config, state)
##                time.sleep(time_interval)
#
        return state

class Manager:
    def __init__(self):
        add_physical_hosts_factory = None
        add_physical_hosts_args = None
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

#    def solve_hosts(self):
#        for host in self.pmm.items:
#            if self.vmm.items != []:
#                solution = self.strategy.solve_host()
#                vms = self.strategy.get_vm_objects(solution)
#                if vms is not None:
#                    self.place_vms(vms, host)
#            else:
#                if not isinstance(self.strategy, EnergyUnawareStrategyPlacement):
#                    host.suspend()
#                print(host)

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

    def add_physical_host(self, host):
        print('add_physical_host: {}'.format(host))

    def add_physical_hosts(self, host=None):
        if self.add_physical_hosts_factory:
            result = self.add_physical_hosts_factory(
                self.add_physical_hosts_args)
            for host in result:
                self.add_physical_host(host)
        else:
            self.add_physical_host(host)

    def execute(config, state):
        print("execute method")

    def start(self):
        """ Start the local manager loop.

        :return: The final state.
        :rtype: dict(str: *)
        """
        self.config = read_and_validate_config()
        config = self.config
        common.init_logging(
            config['log_directory'],
            __file__ + '.log',
            int(config['log_level']))

        interval = int(config['clock_tick_interval']) / 1000.0
        if log.isEnabledFor(logging.INFO):
            log.info('Starting the global manager, ' +
                     'iterations every %s seconds', interval)

        # it auto-starts, no need of rt.start()
        #rt = RepeatedTimer(interval, hello, "World")
        import pdb; pdb.set_trace() # BREAKPOINT

        rt = RepeatedTimer(interval, self.execute, config)
        rt.start()
#        rt = RepeatedTimer(interval, callback, "")
        try:
            # your long-running job goes here...
            # sleep(5)

            #state = init_state(config)

            while True:
                time.sleep(1)
#            return common.start(
#                init_state,
#                execute,
#                config,
#                int(interval))
        finally:
            # better in a try/finally block to make sure the program ends!
            rt.stop()

def execute(config):
    print("regular execute")

#def execute(config, state):
#    """ Execute an iteration of the local manager.
#
#1. Read the data on resource usage by the VMs running on the host from
#   the <local_data_directory>/vm directory.
#
#2. Call the function specified in the algorithm_underload_detection
#   configuration option and pass the data on the resource usage by the
#   VMs, as well as the frequency of the CPU as arguments.
#
#3. If the host is underloaded, send a request to the REST API of the
#   global manager and pass a list of the UUIDs of all the VMs
#   currently running on the host in the vm_uuids parameter, as well as
#   the reason for migration as being 0.
#
#4. If the host is not underloaded, call the function specified in the
#   algorithm_overload_detection configuration option and pass the data
#   on the resource usage by the VMs, as well as the frequency of the
#   host's CPU as arguments.
#
#5. If the host is overloaded, call the function specified in the
#   algorithm_vm_selection configuration option and pass the data on
#   the resource usage by the VMs, as well as the frequency of the
#   host's CPU as arguments
#
#6. If the host is overloaded, send a request to the REST API of the
#   global manager and pass a list of the UUIDs of the VMs selected by
#   the VM selection algorithm in the vm_uuids parameter, as well as
#   the reason for migration as being 1.
#
#    :param config: A config dictionary.
#     :type config: dict(str: *)
#
#    :param state: A state dictionary.
#     :type state: dict(str: *)
#
#    :return: The updated state dictionary.
#     :rtype: dict(str: *)
#    """
#    log.info('Started an iteration')
#    vm_path = common.build_local_vm_path(config['local_data_directory'])
#    vm_cpu_mhz = get_local_vm_data(vm_path)
#    vm_ram = get_ram(state['vir_connection'], vm_cpu_mhz.keys())
#    vm_cpu_mhz = cleanup_vm_data(vm_cpu_mhz, vm_ram.keys())
#
#    if not vm_cpu_mhz:
#        if log.isEnabledFor(logging.INFO):
#            log.info('The host is idle')
#        log.info('Skipped an iteration')
#        return state
#
#    host_path = common.build_local_host_path(config['local_data_directory'])
#    host_cpu_mhz = get_local_host_data(host_path)
#
#    host_cpu_utilization = vm_mhz_to_percentage(
#        vm_cpu_mhz.values(),
#        host_cpu_mhz,
#        state['physical_cpu_mhz_total'])
#    if log.isEnabledFor(logging.DEBUG):
#        log.debug('The total physical CPU Mhz: %s', str(state['physical_cpu_mhz_total']))
#        log.debug('VM CPU MHz: %s', str(vm_cpu_mhz))
#        log.debug('Host CPU MHz: %s', str(host_cpu_mhz))
#        log.debug('CPU utilization: %s', str(host_cpu_utilization))
#
#    if not host_cpu_utilization:
#        log.info('Not enough data yet - skipping to the next iteration')
#        log.info('Skipped an iteration')
#        return state
#
#    time_step = int(config['data_collector_interval'])
#    migration_time = common.calculate_migration_time(
#        vm_ram, float(config['network_migration_bandwidth']))
#
#    if 'underload_detection' not in state:
#        underload_detection_params = common.parse_parameters(
#            config['algorithm_underload_detection_parameters'])
#        underload_detection = common.call_function_by_name(
#            config['algorithm_underload_detection_factory'],
#            [time_step,
#             migration_time,
#             underload_detection_params])
#        state['underload_detection'] = underload_detection
#        state['underload_detection_state'] = {}
#
#        overload_detection_params = common.parse_parameters(
#            config['algorithm_overload_detection_parameters'])
#        overload_detection = common.call_function_by_name(
#            config['algorithm_overload_detection_factory'],
#            [time_step,
#             migration_time,
#             overload_detection_params])
#        state['overload_detection'] = overload_detection
#        state['overload_detection_state'] = {}
#
#        vm_selection_params = common.parse_parameters(
#            config['algorithm_vm_selection_parameters'])
#        vm_selection = common.call_function_by_name(
#            config['algorithm_vm_selection_factory'],
#            [time_step,
#             migration_time,
#             vm_selection_params])
#        state['vm_selection'] = vm_selection
#        state['vm_selection_state'] = {}
#    else:
#        underload_detection = state['underload_detection']
#        overload_detection = state['overload_detection']
#        vm_selection = state['vm_selection']
#
#    if log.isEnabledFor(logging.INFO):
#        log.info('Started underload detection')
#    underload, state['underload_detection_state'] = underload_detection(
#        host_cpu_utilization, state['underload_detection_state'])
#    if log.isEnabledFor(logging.INFO):
#        log.info('Completed underload detection')
#
#    if log.isEnabledFor(logging.INFO):
#        log.info('Started overload detection')
#    overload, state['overload_detection_state'] = overload_detection(
#        host_cpu_utilization, state['overload_detection_state'])
#    if log.isEnabledFor(logging.INFO):
#        log.info('Completed overload detection')
#
#    if underload:
#        if log.isEnabledFor(logging.INFO):
#            log.info('Underload detected')
#        try:
#            r = requests.put('http://' + config['global_manager_host'] +
#                             ':' + config['global_manager_port'],
#                             {'username': state['hashed_username'],
#                              'password': state['hashed_password'],
#                              'time': time.time(),
#                              'host': state['hostname'],
#                              'reason': 0})
#            if log.isEnabledFor(logging.INFO):
#                log.info('Received response: [%s] %s',
#                         r.status_code, r.content)
#        except requests.exceptions.ConnectionError:
#            log.exception('Exception at underload request:')
#
#    else:
#        if overload:
#            if log.isEnabledFor(logging.INFO):
#                log.info('Overload detected')
#
#            log.info('Started VM selection')
#            vm_uuids, state['vm_selection_state'] = vm_selection(
#                vm_cpu_mhz, vm_ram, state['vm_selection_state'])
#            log.info('Completed VM selection')
#
#            if log.isEnabledFor(logging.INFO):
#                log.info('Selected VMs to migrate: %s', str(vm_uuids))
#            try:
#                r = requests.put('http://' + config['global_manager_host'] +
#                                 ':' + config['global_manager_port'],
#                                 {'username': state['hashed_username'],
#                                  'password': state['hashed_password'],
#                                  'time': time.time(),
#                                  'host': state['hostname'],
#                                  'reason': 1,
#                                  'vm_uuids': ','.join(vm_uuids)})
#                if log.isEnabledFor(logging.INFO):
#                    log.info('Received response: [%s] %s',
#                             r.status_code, r.content)
#            except requests.exceptions.ConnectionError:
#                log.exception('Exception at overload request:')
#        else:
#            if log.isEnabledFor(logging.INFO):
#                log.info('No underload or overload detected')
#
#    if log.isEnabledFor(logging.INFO):
#        log.info('Completed an iteration')
#
#    return state
