#!/bin/bash

if [ -f fmap.log ];then
	grep RG fmap.log >fmap.log.RG
elif [ -f fmap.log.gz ];then
	zgrep RG fmap.log.gz >fmap.log.RG
fi

nl=`wc -l  fmap.log.RG|awk '{print $1/6}'`
split -l $nl -d -a 2 fmap.log.RG fmap.log.RG.

xm=`wc -l  fmap.log.RG|awk '{print ($1/6-1)*0.6}'`
awk '(NR>1){printf("%8.3f%16.5f\n",($2+0.5)*0.6,$3/4392.0)}' fmap.log.RG.00 >Bltz.txt
fmapvr=`grep FMAPvr parms.txt|awk '{print $3}'`
$FMAPB2/scripts/epsplot '
set encoding iso_8859_1;
set xr [0:'$xm'];
set yr [0:];
set size 0.55;
set ylabel "exp(-{/Symbol-Oblique b}{/Italic W})";
set xlabel "{/Italic R} (\305)";
set arrow from '$fmapvr', graph 0 to '$fmapvr',graph 1 nohead lt 0 lw 2;
' '
"Bltz.txt" u 1:2 smooth csplines w l lt 1 lc rgb "red" not
' >gr.eps
$FMAPB2/scripts/eps2png gr.eps

$FMAPB2/scripts/epsplot '
set xlabel "Number of rotations";
set xr [0:4500];
set xtics 1000;
set size 0.55;
set ylabel "{/Italic B}_{2} (10^{-4} ml.mol.g^{-2})";
set key center right;
set key spacing 3;
' '
"fmap.ern.vol.msf.b22" u 1:2:4 w e pt 0 lt 0 lw 2 t "{/Italic B}@^0_{2}",
"fmap.ern.vol.msf.b22" u 1:2 w l lt 0 lw 2 not,
"fmap.ern.v+e.msf.b22" u 1:2:4 w e pt 0 lt 1 lc rgb "red" t "{/Italic B}_{2}",
"fmap.ern.v+e.msf.b22" u 1:2 w l lt 1 lc rgb "red" not
'>conv.eps
$FMAPB2/scripts/eps2png conv.eps

temp=`grep Temperature parms.txt|awk '{print $3}'`
tail -1 fmap.ern.v+e.msf.b22 |sed 's/4392/'$temp'/' >calc.temp.txt
$FMAPB2/scripts/mattemp.sh 4392.0 >mattemp.txt
awk '(NR>1){print  $1,$2}' mattemp.txt >tdep.txt
$FMAPB2/scripts/epsplot '
set size 0.55;
set ylabel "{/Italic B}_{2} (10^{-4} ml.mol.g^{-2})";
set xlabel "Temperature ({/Symbol \260}C)";
set xr [0:35];
' '
"calc.temp.txt" u ($1-273.15):2:4 w e lt -1 pt 0 not,
"mattemp.txt" u 1:2 w l lt 1 not
'>mattemp.eps
$FMAPB2/scripts/eps2png mattemp.eps

