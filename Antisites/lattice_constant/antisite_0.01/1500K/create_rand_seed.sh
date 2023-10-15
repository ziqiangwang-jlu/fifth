#! /bin/bash

for i in $(seq 1 1 5)
do
    mkdir seed_$i
    seed=$((i+1000))
    sed "62s/45362/$seed/1" antisite_defect.in > antisites_defect.in
    cp lammps.pbs antisites_defect.in perfect_relaxed.dat CeThUNpPuAmCmO.eam.alloy seed_$i
    cd seed_$i && mv antisites_defect.in antisite_defect.in && qsub lammps.pbs && cd ../ && rm -f antisites_defect.in
done

