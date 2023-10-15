#! /bin/bash

#Note: The lattice constant must be a value which results in zero internal pressure inside the box
#The lattice constant needs to be determined carefully
alat=2.8553125 # The relaxed value for the interatomic potential developed by Becquart et al
atomsk --create bcc $alat Fe orient [11-2] [1-10] [111] \
-duplicate 50 65 1 \
-dislocation 0.251*box 0.501*box screw Z Y 2.47277316 \
-dislocation 0.751*box 0.501*box screw Z Y -2.47277316 \
Fe_screw_dipole.xsf
atomsk Fe_screw_dipole.xsf -cell add 1.23638658 zy Fe_screw_dipole_mod.cfg
atomsk Fe_screw_dipole_mod.cfg -alignx Fe_screw_dipole.lmp
rm -f Fe_screw_dipole_mod.* Fe_screw_dipole.xsf 
