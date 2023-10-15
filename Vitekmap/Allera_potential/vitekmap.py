#! /public/home/ziqiangw/anaconda3/envs/atomman_env/bin/python3

# a differential displacement vector is defined as x(ij) - X(ij)
# x is the vector difference between atoms i and j in the defect configuration, and X(ij) is the vector difference
# between atoms i and j in the perfect configuration
# The configuration must be periodic in all three directions, so the quadrupole arrangement of dislocations is created
# The periodicity in all directions can also be created by tilting the xz or yz component of the box

import math
import numpy as np
import matplotlib.pyplot as plt
import atomman as am
import atomman.unitconvert as uc

potential = 'Allera_potential'
base_system = am.load('atom_dump', 'perfect_relaxed.dump')
disl_system = am.load('atom_dump', 'screw_relaxed.dump')

# The relaxed lattice constant for the interatomic potential developed by different researchers
with open ('relaxed_lattice_parameter.txt', 'r') as file:
    line = file.readline()
    alat = float(line.split()[0])
#alat=$(cut -f 1 -d " " relaxed_lattice_parameter.txt)

burger_value = math.sqrt(3)*alat/2.0
burgers = np.array([0.0, 0.0, burger_value])

# Note: the reference choice corresponds to the system for which the neighbor list was computed and plotting atomic
# positions!
neighbors = base_system.neighborlist(cutoff = alat)
dd = am.defect.DifferentialDisplacement(base_system, disl_system, neighbors=neighbors, reference=0)

ddmax = np.linalg.norm(burgers)/2.0 # b/2 is typically used for fullly compact dislocations i.e. 1/2<111> screw for bcc
params = {}
params['plotxaxis'] = 'x'
params['plotyaxis'] = 'y'
params['xlim'] = (115, 130)
params['ylim'] = (57.5, 72.5)
params['zlim'] = (-0.05, alat*3**0.5/2.0+0.05) # should be one periodic width
#params['figsize'] = 100
params['arrowwidth'] = 1/150 # Made bigger to make arrows easier to see
params['arrowscale'] = 1.5  # Typically chosen to make arrows of length ddmax touch the corresponding atom circles

dd.plot('z', ddmax, **params)
plt.title('DD map for '+potential)
plt.xlabel('X axis(Angstrom)')
plt.ylabel('Y axis(Angstrom)')
plt.savefig(potential+'.tiff', dpi=300.0, bbox_inches='tight')
plt.show()
