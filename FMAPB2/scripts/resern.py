#!/usr/bin/python
import sys

def ReadAtomLine(line):
	'''
	Read a ATOM RECORD in pdb and split it to
	card=   substr($0,1,6)
        anum=   substr($0,7,5)
        aname=  substr($0,13,4)
        altloc= substr($0,17,1)
        resname=substr($0,18,3)
        chainid=substr($0,22,1)
        resnum= substr($0,23,4)
        inscode=substr($0,27,1)
        x=      substr($0,31,8)
        y=      substr($0,39,8)
        z=      substr($0,47,8)
        occ=    substr($0,55,6)
        tempfac=substr($0,61,6)
        footnot=substr($0,67,4)		#not use
        charge= substr($0,71,6)         # *** PDBq format ONLY ***
	* from renumber-residue of AutoDock
	'''
	assert(len(line)>54)
	card = line[0:6]
	anum = line[6:11]
	aname = line[12:16]
	altloc = line[16:17]
	resname = line[17:20]
	#1X(blank)
	chainid = line[21:22]
	resnum = line[22:26]
	inscode = line[26:27]
	#3X
	x = line[30:38]
	y = line[38:46]
	z = line[46:54]
	occ=float(line[54:60])
	tempfac=float(line[60:66])
	vol=float(line[66:82])
	ele=float(line[82:98])
	vdw=float(line[98:114])
	tot=float(line[114:130])
	return card,anum,aname,altloc,resname,chainid,resnum,inscode,x,y,z,occ,tempfac,vol,ele,vdw,tot

def selefav(lines,onlyfav=False):
	favs=[" CA "," C3 "," C3H"]
	n=len(lines)
	if n==0:
		return	
	if onlyfav:
		sel=[]
		for i in range(0,n):
			if lines[i][12:16] in favs:
				sel.append(i)
		if len(sel)==0:
			sel=[0]
		elif len(sel)>1:
			sel=[sel[0]]
	else:
		sel=range(0,n)
	out=[lines[i] for i in sel]
	return out
		
def RenumResidue(fname,onlyfav=False):
	count=0
	oldresnum=''
	oldresname=''
	#test=0.0
	for line in open(fname):
		if line[:6]=="ATOM  ":
			card,anum,aname,altloc,resname,chainid,resnum,inscode,x,y,z,occ,tempfac,vol,ele,vdw,tot=ReadAtomLine(line)
			#test+=tot
			#print >>sys.stderr,test
			count += 1
			if ((resnum == oldresnum) and (resname == oldresname)):
				#print "%6s%5s %4s%1s%3s %1s%4s%1s   %8s%8s%8s%6s%6s"\
				#	%(card, count, aname, altloc, resname, chainid, resnum, inscode, x, y, z,occ, tempfac)
				cur_occ+=occ
				cur_tempfac+=tempfac
				cur_vol+=vol
				cur_ele+=ele
				cur_vdw+=vdw
				cur_tot+=tot
				out.append(line[:54])
			else:
				if oldresnum!='':
					outfav=selefav(out,onlyfav)
					for newline in outfav:
						print "%s%6.2f%6.2f%16.8f%16.8f%16.8f%16.8f"%(newline,cur_occ,cur_tempfac,cur_vol,cur_ele,cur_vdw,cur_tot)
				oldresnum=resnum
				oldresname=resname
				cur_occ=occ
				cur_tempfac=tempfac
				cur_vol=vol
				cur_ele=ele
				cur_vdw=vdw
				cur_tot=tot
				out=[]
				out.append(line[:54])
	outfav=selefav(out,onlyfav)
	for newline in outfav:
		print "%s%6.2f%6.2f%16.8f%16.8f%16.8f%16.8f"%(newline,cur_occ,cur_tempfac,cur_vol,cur_ele,cur_vdw,cur_tot)


if __name__=="__main__":
	import sys
	if len(sys.argv)==2:
		RenumResidue(sys.argv[1])
	elif len(sys.argv)==3:
		if sys.argv[2]=="-fav":
			RenumResidue(sys.argv[1],True)
		else:
			RenumResidue(sys.argv[1],False)
