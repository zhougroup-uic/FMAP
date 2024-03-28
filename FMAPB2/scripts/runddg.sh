#!/bin/bash

ncpu=$1

export OMP_NUM_THREADS=$ncpu
date
if [ -f fmap.ern ];then
	grep sav fmap.ern >fmap.ern.sav
elif [ -f fmap.ern.gz ];then
	zgrep sav fmap.ern >fmap.ern.sav
fi
if [ -f fmap.log ];then
	grep -v -e "^  0.000000  0.000000  0.000000" -e "RG" fmap.log >fmap.log.out
elif [ -f fmap.log.gz ];then
	zgrep -v -e "^  0.000000  0.000000  0.000000" -e "RG" fmap.log >fmap.log.out
fi
head -4 fmap.log.out >fmap.log.h200k
awk '(NR>4){print $0}' fmap.log.out |sort -gk7 |head -3000 >>fmap.log.h200k
date


ion=`grep ion parms.txt |awk '{print $3}'`
temp=`grep Temperature parms.txt  |awk '{print $3}'`
vscl=`grep vscl parms.txt |awk '{print $3}'`
rcut=`grep rcut parms.txt |awk '{print $3}'`
kbt=`grep kbt parms.txt |awk '{print $3}'`

$FMAPB2/bin/fmapdd fmap.log.h200k $ion $temp 1.0 $vscl $rcut $rcut  >fmap.log.out.dd

date

awk '(NF==11)&&($9<0.5){print $0}' fmap.log.out.dd >fmap.log.out.dd.filt
$FMAPB2/scripts/colbltztemp.sh fmap.log.out.dd.filt 7 $kbt >fmap.log.out.dd.filt.bz7
$FMAPB2/scripts/colbltztemp.sh fmap.log.out.dd.filt 8 $kbt >fmap.log.out.dd.filt.bz8
$FMAPB2/scripts/colbltztemp.sh fmap.log.h200k 7  $kbt >fmap.log.h200k.bz7
$FMAPB2/scripts/colbltztemp.sh fmap.log.out 7 $kbt >fmap.log.out.bz7
date
head -4 fmap.log.out >fmap.log.out.dd.filt.pre
cat fmap.log.out.dd.filt >>fmap.log.out.dd.filt.pre
date
