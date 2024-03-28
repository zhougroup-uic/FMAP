#!/bin/bash

mass=$1
conv=`echo $mass|awk '{conv=6.022140857e+23/1e+27/$1^2*1000*10000; print conv}'`
#echo $conv
if [ "$2" != "" ];then
	if [ "$2" == "-" ] || [ -f $2 ];then
		#for msf file at col2,3,4
		if [ $# -eq 4 ];then
			dx=$3
			blen=$4
			awk '{a=0.5*(('${blen}'^3-$2)*'${conv}'*'${dx}'^3);
			      b=0.5*($3*'${conv}'*'${dx}'^3);
                              c=0.5*($4*'${conv}'*'${dx}'^3);print $1,a,b,c}' $2
		#for fmap.ern col3 or msf file at col2, need specify the column
		elif [ $# -eq 5 ];then
			col=$3
			dx=$4
			blen=$5
			awk '{print 0.5*(('${blen}'^3-$'${col}')*'${conv}'*'${dx}'^3)}' $2
		fi
	else
		#vol in angstrom
		if [ $# -eq 2 ];then
			echo $2 $conv |awk '{print  $1*$2}'
		#covolume in angstrom using 1, in grid volume using 0.6 for $3
		elif [ $# -eq 3 ];then
			echo $2 $conv $3|awk '{print  0.5*$1*$2*$3^3}'
		#free grid volume from fmap calcaltion using 0.6 blen
		elif [ $# -eq 4 ];then
			echo $2 $conv $3 $4|awk '{print  0.5*($4^3-$1)*$2*$3^3}'
		fi
	fi
fi
