#! /bin/bash

for i in $(seq 1 1 5)
do
    mkdir seed_$i
    seed=$((i+1000))
    sed "87s/45362/$seed/1" frenkel_defect.in > frenkels_defect.in
    cp lammps.pbs frenkels_defect.in perfect_relaxed.dat CeThUNpPuAmCmO.eam.alloy seed_$i
    cd seed_$i && mv frenkels_defect.in frenkel_defect.in && qsub lammps.pbs && cd ../ && rm -f frenkels_defect.in
done

