#!/bin/bash

set -x
ncpu=$1

#tail -25 /proc/cpuinfo >test20.sh.cpuinfo
#free >>test20.sh.cpuinfo

export OMP_NUM_THREADS=$ncpu
ln -sf $FMAPB2/dat/lattice.txt .
ln -sf $FMAPB2/dat/evscl.lst .
ln -sf $FMAPB2/dat/rotation_samples/oim15.eul .
ion=`grep ion parms.txt |awk '{print $3}'`
temp=`grep Temperature parms.txt  |awk '{print $3}'`
qscl=`grep qscl parms.txt |awk '{print $3}'`
blen=`grep blen parms.txt |awk '{print $3}'`
vscl=`grep vscl parms.txt |awk '{print $3}'`
rcut=`grep rcut parms.txt |awk '{print $3}'`
time $FMAPB2/bin/fmapgrevst.cen subA.vdw subA.vdw $blen 0.6 $ion 1.08 $qscl $temp oim15.eul 1.0 $vscl -6 $rcut $rcut 1>fmap.log 2>fmap.ern
