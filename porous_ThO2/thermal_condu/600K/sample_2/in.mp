#---------------------------------------
#
# This script is used to calculate the thermal conuctivity of UO2 containning vacancy clusters
# using Muller-Plathe method
# By Ziqiang Wang on 04/21/2022 on Jilin university
# 
#---------------------------------------

variable  i  index  0.01 #for 1% vacancies
label        loop
variable     Nevery    equal   200
variable     T         equal   600  #at the temperature of 600K
#variable directory string antisite_${T}K_$i


clear
units          metal
boundary       p p p

atom_style     full

#lattice sc 4.329

#region box block 0 1 0 1 0 1

#create_box 2 box

#create_atoms 1 single 0 0 0
#create_atoms 1 single 0.5 0.5 0
#create_atoms 1 single 0.5 0 0.5
#create_atoms 1 single 0 0.5 0.5
#create_atoms 2 single 0.25 0.25 0.25
#create_atoms 2 single 0.75 0.75 0.25
#create_atoms 2 single 0.75 0.25 0.75
#create_atoms 2 single 0.25 0.75 0.75

#mass 1 28.086
#mass 2 12.011
#read_data     ${directory}/UO2-single_cell.lmpstruct
read_data     porous.dat

set           type     1    charge     -1.1104
set           type     2    charge      2.2208
#set           type     3    charge     -1.1104
#set           type     4    charge      2.2208

#replicate     4  4  $L

kspace_style    pppm   1.0e-05
pair_style      hybrid/overlay  coul/long  11.0  eam/alloy
pair_coeff      * * coul/long
pair_coeff      * * eam/alloy CeThUNpPuAmCmO.eam.alloy O Th
newton          on
neighbor        0.3 bin
neigh_modify    delay 0 check yes every 1 

velocity      all create $T 443322 mom yes rot yes dist gaussian
#The first equilation

fix             nvt  all  nvt  temp  $T $T  0.1

thermo          100000
thermo_style    one

reset_timestep  0
run             500000

velocity        all   scale   $T
unfix           nvt
reset_timestep  0

# the second run
fix             1 all nve

group           Silicon type 1
fix             2 Silicon thermal/conductivity ${Nevery} z 20

compute         ke all ke/atom
variable        temp atom c_ke/1.5

compute         layers all chunk/atom bin/1d z lower 0.05 units reduced
fix             3      all ave/chunk  2 50000 100000 layers v_temp file profile_${T}K_$i.mp

variable        Tdiff    equal     f_3[11][3]-f_3[1][3]
variable        deltaT   equal     v_Tdiff*1.5/0.0001292

timestep        0.001

thermo_style    custom step f_2 temp v_Tdiff v_deltaT
thermo          100000

#dump            1 all atom 500 dump.meam

run             2000000
#undump          1

#reset_timestep  0
fix             2 Silicon thermal/conductivity ${Nevery} z 20

fix             ave all ave/time 100000 2 200000 v_Tdiff ave running

thermo_style    custom step temp epair etotal f_2 v_Tdiff f_ave
thermo          200000

dump            2 all xyz 1000000 calcdump.*.xyz
run             400000
undump          2
next            i
jump            in.mp loop

