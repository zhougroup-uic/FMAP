#!/bin/bash

ion=$(cat ion.dat)
temp=$(awk '{print  273.15+$1}' temp.dat)
vscl=$(cat vscl.dat)
$FMAPB2/bin/getparm $temp $ion >parms.txt
printf "%-12s :%16.3f\n" "vscl" $vscl >>parms.txt
chrg=`awk '{sum+=substr($0,55,8)};END{print sum}' subA.pqr`
mass=`$FMAPB2/scripts/pdbtools.py -m subA.pqr`
printf "%-12s :%16.0f\n" "charge" $chrg >>parms.txt
printf "%-12s :%16.3f %s\n" "mass" $mass "Da" >>parms.txt
rcut=`grep kappa parms.txt|awk '{printf("%0.f",1.0/$3*3.0)}'`
if [ $rcut -lt 36 ];then
	rcut=36
fi
printf "%-12s :%16.3f %s\n" "rcut" $rcut 'angstrom' >>parms.txt
$FMAPB2/scripts/pdbtools.py -c subA.pqr >cenA.pqr
$FMAPB2/scripts/vdwassign.py $FMAPB2/dat/vdw cenA.pqr >subA.vdw

cut -c63-70 subA.vdw >rad.txt
maxr=`$FMAPB2/scripts/pdbtools.py -r subA.vdw`
atomr=`sort -nk1 rad.txt  |tail -1`
blen=`echo $maxr $atomr $rcut|awk '{print 2*(int((2*($1+$2)+$3)/0.6)+1)}'`
printf "%-12s :%16.3f %s\n" "MaxR" $maxr 'angstrom' >>parms.txt
printf "%-12s :%16.0f\n" "blen" $blen >>parms.txt
