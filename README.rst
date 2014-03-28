**********
pyCloudSim
**********

A VM placement simulator with energy-efficiency focus.

pyCloudSim has the following available strategies:

* Iterated-KSP. A KSP (Knapsack) based strategy
* Iterated-KSP-Mem. Similar to Iterated-KSP it considers using the virtual memory by doubling the RAM
* Iterated-EC. An EC (Evolutionary Computation) based strategy
* Iterated-EC-Net. Similart to the Iterated-EC it considers minimizing the network usage simultaneously
* Iterated-EU. An enery-unaware strategy

Execution:

  $ python pycloudsim.py -t ``TRACEFILE`` -o ``OUTDIR`` -pm ``#PHYSICAL MACHINES`` -vma ``#STARTING VIRTUAL MACHINES`` -vmo ``#ENDING VIRTUAL MACHINES`` -vme ``#INCREMENT VIRTUAL MACHINES`` ``STRATEGIES``

Where

* ``TRACEFILE`` is the trace file to be used. Traces can be found here: https://github.com/vonpupp/planetlab-workload-traces
* ``OUTDIR`` is the output folder where simulation results will be stored
* ``#PHYSICAL MACHINES`` is the number of physical machines
* ``#STARTING VIRTUAL MACHINES`` is the starting number of virtual machines
* ``#ENDING VIRTUAL MACHINES`` is the ending number of virtual machines
* ``#INCREMENT VIRTUAL MACHINES`` is the increment of the virtual machines
* ``STRATEGIES`` are: ``-seu`` (energy-unaware strategy) ``-sksp`` (Knapsack based strategy) ``-sec`` (Evolutionary Computation based strategy)

The setup scripts can be found in the setup folder.
