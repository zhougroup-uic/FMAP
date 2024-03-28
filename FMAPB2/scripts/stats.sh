#!/bin/bash

mass=`grep mass parms.txt|awk '{print $3}'`
blen=`grep blen parms.txt|awk '{print $3}'`
if [ -f fmap.ern.gz ];then
nrot=`zcat fmap.ern.gz|grep -c "^vol"`
else
nrot=`cat fmap.ern|grep -c "^vol"`
fi
step=`echo $nrot  ${nrot:0:2}.${nrot:2:10}|awk '{printf("%d",$1/$2)}'`
for ern in v+e vol
do
	if [ -f fmap.ern ];then
		grep -n $ern fmap.ern|shuf --random-source=subA.vdw |sed 's/:/ /' >fmap.ern.$ern
	elif [ -f fmap.ern.gz ];then
		zgrep -n $ern fmap.ern.gz|shuf --random-source=subA.vdw |sed 's/:/ /' >fmap.ern.$ern
	fi
        cat /dev/null >fmap.ern.$ern.msf
	let nrot1=nrot+step
        for i in `seq $step $step $nrot1`
        do
        	head -$i fmap.ern.$ern|sort -gk1 >tmp
        	$FMAPB2/scripts/flyvbjerg_petersen_std_err_msf.py tmp 3 |tail -1|awk '{printf("%16d%16.5f %16.5f %16.5f\n",$1,$2,$3,$4)}' >>fmap.ern.${ern}.msf
		#break
        done
	$FMAPB2/scripts/convV2b.sh $mass fmap.ern.${ern}.msf 0.6 $blen >fmap.ern.${ern}.msf.b22
done
\rm tmp 

vco=`tail -1 fmap.ern.vol.msf|awk '{print ('$blen'^3-$2)*0.6^3}'`
vs=`tail -1 fmap.ern.v+e.msf|awk '{print ('$blen'^3-$2)*0.6^3}'`

vr=`echo $vco|awk '{print ($1/(32.0/3*3.1415926))^(1.0/3.0)*2.0}'`
printf "%-12s :%16.3f %s\n" "FMAPvr" $vr "angstrom" >>parms.txt

exb22=`tail -1 fmap.ern.vol.msf.b22|awk '{print $2}'`
b22=`tail -1 fmap.ern.v+e.msf.b22|awk '{print $2}'`
exb22std=`tail -1 fmap.ern.vol.msf.b22|awk '{print $4}'`
b22std=`tail -1 fmap.ern.v+e.msf.b22|awk '{print $4}'`
#echo $rsvc $vco $vs >subA.RSV.txt
printf "%-12s :%16.3f %s\n" "FMAPvco" $vco 'angstrom^3' >>parms.txt
printf "%-12s :%16.3f %s\n" "FMAPvs" $vs 'angstrom^3' >>parms.txt
printf "%-12s :%16.3f %s\n" "FMAPexb22" $exb22 'x 1e-4 mL mol / g^2' >>parms.txt
printf "%-12s :%16.3f %s\n" "FMAPb22" $b22 'x 1e-4 mL mol / g^2' >>parms.txt
printf "%-12s :%16.4f %s\n" "FMAPexb22std" $exb22std 'x 1e-4 mL mol / g^2' >>parms.txt
printf "%-12s :%16.4f %s\n" "FMAPb22std" $b22std 'x 1e-4 mL mol / g^2' >>parms.txt
