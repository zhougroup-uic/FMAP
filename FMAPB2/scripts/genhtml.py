#!/usr/bin/python

import string
from math import exp

template='''
<html>
<head>
<style>
.supsub {
    display: inline-block;
}

.supsub sup,
.supsub sub {
    position: relative;
    display: block;
    font-size: .6em;
    line-height: 1.0;
}

.supsub sub {
    top: .3em;
}
</style>
</head>
<body>
<h3> %s</h3>
<h4>
%s
</h4>
<BR>
<table border="1" align="center">
<tr>
<th>Ionic Strength</th>
<th>Temperature</th>
<th>Molecular Weight</th>
<th>Net Charge</th>
<th><i>v</i><sub>s</sub></th>
<th><i>diam</i></th>
<th><i>B</i><span class="supsub"><sup>0</sup><sub>2</sub></span> </th>
<th><i>B</i><sub>2</sub></th>
</tr>
<tr>
<th>(M)</th>
<th>(&#176C)</th>
<th>(Da)</th>
<th>(e)</th>
<th> &nbsp </th>
<th> &#8491 </th>
<th>(10<sup>-4</sup> ml.mol.g<sup>-2</sup>)</th>
<th>(10<sup>-4</sup> ml.mol.g<sup>-2</sup>)</th>
</tr>
<tr>
<th>%s</th>
<th>%s</th>
<th>%s</th>
<th>%s</th>
<th>%s</th>
<th>%s</th>
<th>%s &#177 %s</th>
<th>%s &#177 %s</th>
</tr>
</table>
<BR>
<img src="conv.png" alt="conv.png" width="48%%" />
<img src="gr.png" alt="gr.png" width="48%%" />
<BR>
<a href="Bltz.txt">Radial Distribution Data</a>;
<BR>
</html> 
'''

#<a href="resd.html">Residue Interaction Energy</a>.
#<a href="parms.txt">Parameters</a>

def ReadParas(fname):
	#out=''
	dct={}
	for line in open(fname):
		items=line.split()
		dct[string.strip(items[0])]=string.strip(items[2])
	#for key in dct.keys():
	#	out=out+"%s= %s\n"%(key,dct[key])
	#return out
	return dct

if __name__=="__main__":
	import sys
	import math
	jobname=open("job.name").read()
	parms=ReadParas('parms.txt')
	if parms.has_key('rcut') and  int(float(parms['rcut']))>36:
		rcuttext="Larger <i>rcut</i> at %d instead of 36 &#8491 are used for the low ion strength."%(int(float(parms['rcut'])))
	else:
		if parms.has_key('rcut'):
			rcuttext="<!--- Normal <i>rcut</i> at %d &#8491 are used.---!>"%(int(float(parms['rcut'])))
		else:
			rcuttext="<!--- Normal <i>rcut</i> at %d &#8491 are used.---!>"%(36)
	print template%(jobname,
			"%s"%(rcuttext),
			"%.3f"%(float(parms['ion'])),
			"%.2f"%(float(parms['Temperature'])-273.15),
			"%.0f"%(float(parms['mass'])),
			parms['charge'],
			parms.get('vscl',"0.16"),
                        parms['FMAPvr'],
			parms['FMAPexb22'],
			parms['FMAPexb22std'],
			parms['FMAPb22'],
			parms['FMAPb22std']
			)
