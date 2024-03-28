#!/bin/bash

tail -25 /proc/cpuinfo >test20.sh.cpuinfo
free >>test20.sh.cpuinfo

export OMP_NUM_THREADS=1
ion=`grep ion parms.txt |awk '{print $3}'`
temp=`grep Temperature parms.txt  |awk '{print $3}'`
vscl=`grep vscl parms.txt |awk '{print $3}'`
rcut=`grep rcut parms.txt |awk '{print $3}'`

head -4 fmap.log.out.dd.filt.pre >fmap.log.out.dd.filts.pre
awk '(NR>4){print $0}'  fmap.log.out.dd.filt.pre |sort -gk8 >>fmap.log.out.dd.filts.pre
head -1004 fmap.log.out.dd.filts.pre >fmap.log.out.dd.filts1g.pre
nconf=`wc -l fmap.log.out.dd.filts1g.pre|awk '{print $1-4}'`
printf "%-12s :%16d\n" "nconf" $nconf >>parms.txt
awk '(NR==5){printf("%-12s :%16.3f\n","ernlow",$8,"kcal/mol")};END{printf("%-12s :%16.3f\n","ernhigh",$8,"kcal/mol")}' fmap.log.out.dd.filts1g.pre >>parms.txt
$FMAPB2/bin/fmapdd.atm fmap.log.out.dd.filts1g.pre $ion $temp 1.0 $vscl $rcut $rcut >fmap.log.out.dd.filts1g.scl
grep ^ATOM fmap.log.out.dd.filts1g.scl >fmap.log.out.dd.filts1g.scl.atom
grep -v ^ATOM fmap.log.out.dd.filts1g.scl >fmap.log.out.dd.filts1g.scl.out
nline=`wc -l fmap.log.out.dd.filts1g.scl.atom|awk '{print $1/2}'`
head -$nline fmap.log.out.dd.filts1g.scl.atom >fmap.log.out.dd.filts1g.scl.atomh
tail -$nline fmap.log.out.dd.filts1g.scl.atom >fmap.log.out.dd.filts1g.scl.atomt
python $FMAPB2/scripts/resern.py fmap.log.out.dd.filts1g.scl.atomh -fav >fmap.log.out.dd.filts1g.scl.atomh.res
python $FMAPB2/scripts/resern.py fmap.log.out.dd.filts1g.scl.atomt -fav >fmap.log.out.dd.filts1g.scl.atomt.res
python $FMAPB2/scripts/resern.py fmap.log.out.dd.filts1g.scl.atomh >fmap.log.out.dd.filts1g.scl.atomh.resa
python $FMAPB2/scripts/resern.py fmap.log.out.dd.filts1g.scl.atomt >fmap.log.out.dd.filts1g.scl.atomt.resa
cut -c18-27,115- fmap.log.out.dd.filts1g.scl.atomh.res >resd1ghbf.txt
cut -c18-27,115- fmap.log.out.dd.filts1g.scl.atomt.res >resd1gtbf.txt
paste resd1ghbf.txt resd1gtbf.txt |awk '(NF==8){print substr($0,0,10),($4+$8)/2.0/'$nconf'};(NF==6){print substr($0,0,10),($3+$6)/2.0/'$nconf'}' >resdA.txt

$FMAPB2/scripts/data2bf.py subA.vdw resdA.txt >subAbf.pdb
cp fmap.log.out.dd.filts1g.scl.out top1k.txt
$FMAPB2/scripts/fmappdb.py top1k.txt -cpdb >top1k.pdb

