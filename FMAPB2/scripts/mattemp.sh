#!/bin/bash

nrot=$1
mass=`grep mass parms.txt|awk '{print $3}'`
temp=`grep Temperature parms.txt|awk '{print $3-273.15}'`
blen=`grep blen parms.txt|awk '{print $3}'`

if [ -s fmap.ern.gz ];then
	raw=`zgrep sav fmap.ern.gz|awk '{print $3/'$nrot'}'`
else
	raw=`grep sav fmap.ern|awk '{print $3/'$nrot'}'`
fi
b22=`$FMAPB2/scripts/convV2b.sh $mass $raw 0.6 $blen`

echo "#" $temp $b22 $raw

for temp in `seq -5 5 35`
do
	tempk=`echo $temp |awk '{print $1+273.15}'`
	calc=`echo 1.0 1.0|${FMAPB2}/bin/matevscl mat.bin.gz 4001 0.02 -40 $tempk |awk '{print $4/'$nrot'}'`
	b22=`$FMAPB2/scripts/convV2b.sh $mass $calc 0.6 $blen`
	echo $temp $b22 $calc
done
