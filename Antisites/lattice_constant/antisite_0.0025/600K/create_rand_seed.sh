#! /bin/bash

for i in $(seq 1 1 5)
do
    mkdir seed_$i
    seed=$((i+1000))
    sed "86s/442211/$seed/1" antisite_defect.in > antisites_defect.in
    cp lammps.pbs antisites_defect.in CeThUNpPuAmCmO.eam.alloy seed_$i
    cd seed_$i && qsub lammps.pbs && cd ../ && rm -f antisites_defect.in
done

