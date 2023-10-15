#! /bin/bash
#Please confirm the interatomic potential for your atomic simulations
#Please check the pair style for the interatomic potential such as eam/fs, eam/alloy
#!!!
#Note: manually modify the pair_style in the input file!
#!!!
#Created by Ziqiang Wang on Jilin univeristy

echo "Please confirm that the pair style in lammps input file has been modified yes or no?"
read answer
if [ $answer == 'yes' ] 
then
    echo "The interatomic potential file will be replaced automatically"
else
    exit 0
fi

interatomic_potential=/public/home/ziqiangw/myproj/potential/FeC.eam
inputfile=/public/home/ziqiangw/myproj/screw_carbon/box_relax/box_relax.in
pbs=/public/home/ziqiangw/myproj/lammps_submit/lammps.pbs
new_pbs=/public/home/ziqiangw/myproj/lammps_submit/lammps_new.pbs
inputfile_before=$(awk -F "=" 'NR==8 {print $2}' $pbs)
#echo "The inputfile before the modification: $inputfile_before"
#echo "The inputfile after the modification: $inputfile"

inter_potential_before=$(awk 'NR==25 {print $4}' $inputfile)

#echo $inter_potential_before

sed -i "s+${inter_potential_before}+${interatomic_potential}+1" $inputfile

awk -v var=$inputfile -F "=" 'NR==8 {$2=var} { if (NR==8) {print $1 "=" $2} else {print} }' $pbs > $new_pbs
#cat $new_pbs
#exit 0

qsub $new_pbs
while [ ! -f relaxed_lattpara.txt ]
do
    sleep 5s
done
mv relaxed_lattpara.txt relaxed_lattice_parameter.txt
rm minimize.*
rm log.*
    

