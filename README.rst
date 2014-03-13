*******
DistSim
*******

A VM placement simulator with energy-efficiency focus.

DistSim has the following available strategies:

* A KSP (Knapsack) based strategy
* A EC (Evolutionary Computation) based strategy
* An enery-unaware strategy

Execution:

  $ python distsim.py -t ``TRACEFILE`` -o ``OUTDIR`` -pm ``#PHYSICAL MACHINES`` -vma ``#STARTING VIRTUAL MACHINES`` -vmo ``#ENDING VIRTUAL MACHINES`` -vme ``#INCREMENT VIRTUAL MACHINES`` ``STRATEGIES``

Where

* ``TRACEFILE`` is the trace file to be used. Traces can be found here: https://github.com/vonpupp/planetlab-workload-traces
* ``OUTDIR`` is the output folder where simulation results will be stored
* ``#PHYSICAL MACHINES`` is the number of physical machines
* ``#STARTING VIRTUAL MACHINES`` is the starting number of virtual machines
* ``#ENDING VIRTUAL MACHINES`` is the ending number of virtual machines
* ``#INCREMENT VIRTUAL MACHINES`` is the increment of the virtual machines
* ``STRATEGIES`` are: ``-seu`` (energy-unaware strategy) ``-sksp`` (Knapsack based strategy) ``-sec`` (Evolutionary Computation based strategy)

The setup scripts can be found in the setup folder.
