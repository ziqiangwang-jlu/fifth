#! /bin/bash

#Note: The lattice constant must be a value which results in zero internal pressure inside the box
#The lattice constant needs to be determined carefully

lattice_parameter.sh   # Run lattice_parameter.sh
rm -f *.lmp *.dat screw_relaxed.*

cp relaxed_lattice_parameter.txt ../

# The relaxed lattice constant for the interatomic potential developed by different researchers
a=$(cut -f 1 -d " " relaxed_lattice_parameter.txt)

b=$(echo "scale=5; $a*sqrt(3.)/2." | bc) #burgers vector

atomsk --create bcc $a Fe orient [11-2] [1-10] [111] \
-duplicate 70 65 1 \
-dislocation 0.251*box 0.251*box screw Z Y $b \
-dislocation 0.751*box 0.251*box screw Z Y -$b \
-dislocation 0.251*box 0.751*box screw Z Y -$b \
-dislocation 0.751*box 0.751*box screw Z Y $b \
Fe_screw_quad.lmp 

qsub lammps.pbs | xargs echo > job_id.txt
job_id=$(cut -f 1 -d "." job_id.txt) 
echo "Start to energy minimization!"
while [ ! -f minimize.e$job_id ]
do 
    sleep 5s
done
rm -f minimize.* log.* dump* Fe_screw_quad.lmp job_id.txt relaxed_lattice_parameter.txt 
