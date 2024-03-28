#!/bin/bash

ncpu=$1
source $FMAPB2/scripts/fmapb2.rc


#prevent accidently multiple runs
if [ -f parms.txt ] 
then
	exit
fi

if [ ! -s vscl.dat ];then
	#echo 0.16 >vscl.dat
	mass=`$FMAPB2/scripts/pdbtools.py -m subA.pqr`
	vs=`echo $mass|awk '{print 0.18*(80+0.27*$1/1000.0)/(80+$1/1000.0)}'`
	echo $vs >vscl.dat
fi

$FMAPB2/scripts/prepare.sh
$FMAPB2/scripts/runion.sh $ncpu
$FMAPB2/scripts/stats.sh
$FMAPB2/scripts/plot.sh
echo $(basename $(pwd)) >job.name
$FMAPB2/scripts/genhtml.py >index.html
