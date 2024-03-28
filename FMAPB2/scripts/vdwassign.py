#!/usr/bin/env python

import math

class vdw:
        data=None

        @classmethod
        def assign(cls,key):
                return cls.data[key] 	

        @classmethod
        def fromFF(cls,fname):
                cls.data={}
                for line in open(fname):
                        tp,s_sig,s_eps=line.split()
			sig,eps=map(float,[s_sig,s_eps])
			sig6=math.pow(sig,6)
			sqA=math.sqrt(4.0*eps*sig6*sig6)
			sqB=math.sqrt(4.0*eps*sig6)
                        cls.data[tp]=[sig,eps,sqA,sqB]
			
        @classmethod
        def fromTop(cls,fname):
                cls.data=[]
                tp,ljA,ljB=readparm(fname)
                n=len(tp)
                for i in range(0,tp):
                        mytp=int(tp[i])
                        mypos=mytp-1


def vdwassign(pdb,vdwfn):
	vdw.fromFF(vdwfn)
	for line in open(pdb):
		if line[:4]!="ATOM":
			continue
		if line[12]=="H":
			key="H"
		else:
			key=line[13]#line[70:].strip()
		if key in vdw.data.keys():
			sig,eps,sqA,sqB=vdw.assign(key)
		else:
			key=line[12:16].strip()
			sig,eps,sqA,sqB=vdw.assign(key)
		print line[:62]+"%8.4f%8s%16.11f%16.11f%16.8e%16.8e"%(sig/2.0,key,sig,eps,sqA,sqB)


if __name__=="__main__":
	import sys
	vdwfn=sys.argv[1]
	pdb=sys.argv[2]
	vdwassign(pdb,vdwfn)
