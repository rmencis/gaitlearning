import CycleLength as cl

frameList = cl.loadFile("/Users/rmencis/RUG/Machine_Learning/project/perturbed-walking-data-01/T031/mocap-031")
cycles = cl.getCycles(frameList,0.1,0.1)