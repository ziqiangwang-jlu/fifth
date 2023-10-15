#! /bin/bash


for i in $(seq 1 1 5)
do
    mkdir seed_$i
    seed=$(($i+10000))
    sed "30s/442211/$seed/1" in.mp > in.mp_mod
    position=antisite_0.005_relaxed.dat
    #awk 'NR==16 {$2=infile}' in.mp_mod > in.mp
    cp lammps.pbs in.mp_mod $position CeThUNpPuAmCmO.eam.alloy seed_$i
    cd seed_$i && awk -v infile=$position 'NR==16 {$2=infile} {print}' in.mp_mod > in.mp && qsub lammps.pbs 
    rm -f in.mp_mod
    cd ../
    rm -f in.mp_mod
done
    
