#!/usr/bin/env python

import sys
from operator import add
from math import sqrt

def getxyz(line):
	return map(float,[line[30:38],line[38:46],line[46:54]])

def move(fname,xm,ym,zm):
	if fname=='-':
		fp=sys.stdin
	else:
		fp=open(fname)
	for line in fp:
		if line[:4]=='ATOM' or line[:6]=="HETATM":
			x,y,z=getxyz(line)
			print line[:30]+"%8.3f%8.3f%8.3f"%(x+xm,y+ym,z+zm)+line[54:],
		else:
			print line,

def getcenter(fname):
	cen=[0.0]*3
	count=0.0
	if fname=='-':
                fp=sys.stdin
        else:
                fp=open(fname)
        for line in fp:
		if line[:4]=='ATOM' or line[:6]=="HETATM":
			xyz=getxyz(line)
			cen=map(add,cen,xyz)
			count=count+1.0
	return cen[0]/count,cen[1]/count,cen[2]/count

#assuming file are centerized
def getmaxrad(fname):
	rad=0.0
	if fname=='-':
                fp=sys.stdin
        else:
                fp=open(fname)
        for line in fp:
                if line[:4]=='ATOM' or line[:6]=="HETATM":
                        xyz=getxyz(line)
			cur=xyz[0]*xyz[0]+xyz[1]*xyz[1]+xyz[2]*xyz[2]
			if cur > rad:
				rad=cur
	return sqrt(rad)

elemwt={"C":12.01,\
        "N":14.01,\
        "O":16.00,\
        "P":30.97,\
        "S":32.06,\
        "H":1.01,\
       }
def getmass(fname):
        mass=0.0
	if fname=='-':
                fp=sys.stdin
        else:
                fp=open(fname)
        for line in fp:
                if line[:4]=="ATOM" or line[:6]=="HETATM":
			if line[12]=='H':
				elem='H'
			else:
                        	elem=line[13]
                        try:
                                mass += elemwt[elem]
                        except KeyError:
                                pass
        return mass
	
def centerize(fname):
	tgt=getcenter(fname)
	move(fname,-tgt[0],-tgt[1],-tgt[2])

def main():
	import sys, getopt
    	try:
        	opts, args = getopt.getopt(sys.argv[1:], 'cfmr')
	except getopt.error as msg:
        	sys.stdout = sys.stderr
        	print(msg)
        	print("""usage: %s [-c|-f|-m|-r] [file|-]
        	-c: centerize
		-f: find center
		-m: mass
        	-r: maxrad"""%sys.argv[0])
        	sys.exit(2)
	fname=args[0]
	for o, a in opts:
		if o == '-c': centerize(fname)
		elif o == '-f': cen=getcenter(fname);print cen[0],cen[1],cen[2]
		elif o == '-m': print getmass(fname);
		elif o == '-r': print getmaxrad(fname)

if __name__=="__main__":
	main()
