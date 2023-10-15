#! /bin/bash

alat=2.8553125
atomsk --create bcc $alat Fe orient [11-2] [1-10] [111] \
-duplicate 70 65 1 \
Fe_perfect.lmp 

qsub lammps.pbs
while [ ! -f perfect_relaxed.dat ] 
do 
    sleep 5s
done

if [ ! -e minimize.* ] 
then 
    sleep 5s
else
    rm -f minimize.* log* dump* 
fi
