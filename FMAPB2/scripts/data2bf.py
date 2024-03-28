#!/usr/bin/env python

def data2bf(pdbfile, datafile):
	data={}
	for line in open(datafile).readlines():
		try:
			data[line[:10]]=float(line[10:])
		except:
			data[line[:10]]=-1
	values=data.values()
	values_max=max([abs(i) for i in values])
	for key in data.keys():
		data[key] =data[key]/values_max*10
	for line in open(pdbfile).readlines():
		if line[:4]=="ATOM":
			reslb=line[17:27]
			if data.has_key(reslb):
				print line[:54]+"%6.2f%6.2f"%(1.0,data[reslb])
			else:
				print line[:54]+"%6.2f%6.2f"%(0.0,0.0)

if __name__=="__main__":
	import sys
	try:
		data2bf(sys.argv[1],sys.argv[2])
	except IndexError:
		print sys.argv[0],"pdbfile","Bfile"
