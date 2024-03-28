#!/usr/bin/env python

from math import cos,sin
from operator import sub,mul

def fmap2zdock(fname):
	'''
	Convert fmap.log to format of zdock.out
	'''
	cnt=0
	for line in open(fname):
		cnt=cnt+1
		if (cnt==1):
			bl=int(line.split()[0])
		if (cnt>4):
			i,j,k=map(int,line[30:54].split())
			print "%30s%8d%8d%8d%s"%(line[:30],bl-i,bl-j,bl-k,line[54:]),
		else:
			print line,

def euler2rotmat(euler):
	psi, theta, phi = euler
	r11 = cos(psi)*cos(phi)  -  sin(psi)*cos(theta)*sin(phi)
        r21 = sin(psi)*cos(phi)  +  cos(psi)*cos(theta)*sin(phi)
        r31 = sin(theta)*sin(phi)

        r12 = -cos(psi)*sin(phi)  -  sin(psi)*cos(theta)*cos(phi)
        r22 = -sin(psi)*sin(phi)  +  cos(psi)*cos(theta)*cos(phi)
        r32 = sin(theta)*cos(phi)

        r13 = sin(psi)*sin(theta)
        r23 = -cos(psi)*sin(theta)
        r33 = cos(theta)
	return r11,r12,r13,r21,r22,r23,r31,r32,r33

def rotatom(xyz,rotmat):
	oldX,oldY,oldZ=xyz
	r11,r12,r13,r21,r22,r23,r31,r32,r33=rotmat

	newX = r11 * oldX + r12 * oldY + r13 * oldZ
	newY = r21 * oldX + r22 * oldY + r23 * oldZ
	newZ = r31 * oldX + r32 * oldY + r33 * oldZ
	return newX,newY,newZ

def Nf2z(Nf,N):
	#print "Nf:",Nf
	#print "N:",N
	Nz=map(sub,[N]*3,Nf)
	return Nz

def Nz2R(Nz,N):
	for i in range(0,3):
		if Nz[i]>=N/2:
        		Nz[i]=Nz[i]-N
	return Nz[0],Nz[1],Nz[2]

def Nf2R(Nf,N):
	Nz=Nf2z(Nf,N)
	return Nz2R(Nz,N)

class FMAP:
	def __init__(self,fname):
		self.fname=fname
		cnt=0
		for line in open(fname):
			cnt=cnt+1
			if (cnt==1):
				items=line.split()
				self.N=int(items[0])
				self.spacing=float(items[1])
			elif (cnt==2):
				self.rand=map(float,line.split())
				self.randmat=euler2rotmat(self.rand)
			elif (cnt==3):
				items=line.split()
				self.recf=items[0]
				self.rec=map(float,items[1:4])
			elif (cnt==4):
				items=line.split()
				self.ligf=items[0]
				self.rec=map(float,items[1:4])
			else:
				break

	def creatlig(self,tgt):
		cnt=0
		for line in open(self.fname):
			items=line.split()
			if len(items)>=6:
				cnt=cnt+1
			if cnt==tgt:
				ang=map(float,items[0:3])
				rmat=euler2rotmat(ang)
				tran=Nf2R(map(int,items[3:6]),self.N)
				txyz=map(mul,tran,[self.spacing]*3)
				for line in open(self.ligf):
					if line[:4]=="ATOM":
						xyz=map(float,[line[30:38],line[38:46],line[46:54]])
						nxyz=rotatom(xyz,rmat)
						ntxyz=map(sub,nxyz,txyz)
						print line[0:30]+"%8.3f%8.3f%8.3f"%(ntxyz[0],ntxyz[1],ntxyz[2])
	def creatcens(self,format="pdb"):
		i=0
		for line in open(self.fname):
                        items=line.split()
                        if len(items)>=6:
				tran=Nf2R(map(int,items[3:6]),self.N)
				txyz=map(mul,tran,[self.spacing]*3)
				ntxyz=map(sub,[0.0]*3,txyz)
				#print line[:-1],"%8.3f%8.3f%8.3f"%(ntxyz[0],ntxyz[1],ntxyz[2])
				if format=="xyz":
					print "%8.3f%8.3f%8.3f"%(ntxyz[0],ntxyz[1],ntxyz[2])
				elif format=="angxyz":
					print "%10s%10s%10s%8.3f%8.3f%8.3f %s"%(items[0],items[1],items[2],ntxyz[0],ntxyz[1],ntxyz[2],' '.join(items[6:]))
				else:
					i4=i%10000
                			i5=i%100000
                			info="ATOM  %5d  N   ALA  %4d    "%(i5,i4)
					print "%30s%8.3f%8.3f%8.3f"%(info,ntxyz[0],ntxyz[1],ntxyz[2])
					i=i+1
	
	def realspace(self,xyz=False):
		for line in open(self.fname):
                        items=line.split()
                        if len(items)>=6:
                                tran=Nf2R(map(int,items[3:6]),self.N)
				txyz=map(mul,tran,[self.spacing]*3)	
				if xyz:
					print "%10s%10s%10s%10.3f%10.3f%10.3f"%(items[0],items[1],items[2],txyz[0],txyz[1],txyz[2]),
				else:
					print "%10s%10s%10s%8.0f%8.0f%8.0f"%(items[0],items[1],items[2],tran[0],tran[1],tran[2]),
				if len(items)>=7:
					print "%9s"%(items[6])
				else:
					print

def usage(prog):
        print '''
usage:
    %s fmap.log [-cxyz|-cpdb|n]
  convert fmap.log to zdock.out
    %s fmap.log
  show center of all ligand in xyz or pdb format
    %s fmap.log -cxyz|-cpdb
  show configuratuion of nth ligand
    %s fmap.log n
'''%(prog,prog,prog,prog)
        sys.exit()


if __name__=="__main__":
	import sys
	if len(sys.argv)<2:
		usage(sys.argv[0])
	if len(sys.argv)==2:
		fmaplog=sys.argv[1]
		fmap2zdock(fmaplog)
	elif len(sys.argv)==3:
		fmaplog=sys.argv[1]
		fmap=FMAP(fmaplog)
		if sys.argv[2]=="-cxyz":
			fmap.creatcens("xyz")
		elif sys.argv[2]=="-cangxyz":
			fmap.creatcens("angxyz")
		elif sys.argv[2]=="-cpdb":
			fmap.creatcens("pdb")
		elif sys.argv[2]=="-r":
			fmap.realspace()
		elif sys.argv[2]=="-rxyz":
			fmap.realspace(True)
		else:
			tgt=int(sys.argv[2])
			fmap.creatlig(tgt)
