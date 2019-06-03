import numpy as np
import matplotlib.pyplot as plt
import math

#This program is built to simulate the trajectories of atomic/molecular
# beams through irregular channels while having the chance to be 
#adsorbed by the side wall and reemitted in a new direction with a new
#velocity

h=100
w=100
Num=100
T=273
timesteps=5000

coords=np.zeros((timesteps,2))


BC=np.ones((h,w))
BC1=np.ones((h,w))
n=np.ones((h,w,2))


def create_path(x_start,x_finish,y_start,y_finish,val):
	lx=(x_finish-x_start)
	ly=(y_finish-y_start)
	ls=math.sqrt(lx**2+ly**2)
	slope=ly/(0.000001+lx)
	if lx>ly:
		for i in range(lx):
			BC[int(y_start+(i*slope)//1)][i+int(x_start)]=val
			BC1[int(y_start+(i*slope)//1)][i+int(x_start)]=val
	else:
		for j in range(ly):
			BC[int(y_start+j)][int(x_start+(j/slope)//1)]=val
			BC1[int(y_start+j)][int(x_start+(j/slope)//1)]=val


for j in range(10):
	create_path(5,20,j,j,0)
for j in range(10):
	create_path(5+j,5+j,10,90,0)
for j in range(10):
	create_path(5,80,90-j,90-j,0)
for j in range(10):
	create_path(75+j,75+j,10,90,0)
for j in range(10):
	create_path(10,75+j,10,10+j,0)

def MBDist(T):
	return np.random.random()

class Particle:
	def __init__(self,T):
		self.temp=T
		self.v=np.random.rand()
		self.theta=math.pi/2.8
		self.x=7
		self.y=7
		self.vx=0.11*math.cos(self.theta)
		self.vy=0.11*math.sin(self.theta)

Rb=Particle(10)

#To propagate a particle into the channel, it is necessary to rescale the 
# motion the characteristic cell size i.e. 1. Thus, the larger value of the
#x or y momentum is rescaled to a box and the other is corresponding #sine(theta) or cosine(theta). This allows the particle to move in increments #of the BC

def Reflect(d):
	if d=="y":
		Rb.vy*=-1
		print("reflected y!")
	if d=="x":
		Rb.vx*=-1
		print("reflected x!")
	
def calc_norm_vectors():
	for i in range(h):
		for j in range(w):
			if BC[i][j]==0:
				if BC[i+1][j]==1:
					n[i+1][j]=[0,1]
				if BC[i-1][j]==1:
					n[i-1][j]=[0,1]
				if BC[i][j+1]==1:
					n[i][j+1]=[1,0]
				if BC[i][j-1]==1:
					n[i][j-1]=[1,0]
	#for i in range(h-1):
	#	for j in range(w-1):
	#		if BC[i][j]==1:
	#			if (n[i][j][0])**2+(n[i][j][1])**2>0:
	#				navgx=0
	#				navgy=0
	#				norm=0
	#				navgx+=n[i][j-1][0]
	#				navgy+=n[i][j-1][1]
	#				navgx+=n[i][j+1][0]
	#				navgy+=n[i][j+1][1]					
	#				navgx+=n[i+1][j][0]
	#				navgy+=n[i+1][j][1]
	#				navgx+=n[i-1][j][0]
	#				navgy+=n[i-1][j][1]
	#				normn=navgx**2+navgy**2
	#				n[i][j]=[navgx/normn,navgy/norm]

calc_norm_vectors()

def propagator():
	count=0
	#while Rb.x<w or Rb.y<h:
	while count<timesteps:
		Rb.x+=Rb.vx
		Rb.y+=Rb.vy
		#check collision
		if BC[int(Rb.y)][int(Rb.x)]==1:
			#go back
			oldx=Rb.x-Rb.vx
			oldy=Rb.y-Rb.vy
			#calc new velocities
			newvx=Rb.vx*(1-2*n[int(Rb.y)][int(Rb.x)][0])
			newvy=Rb.vy*(1-2*n[int(Rb.y)][int(Rb.x)][1])
			if BC[int(oldy+1*newvy)][int(oldx+1*newvx)]==0:
				Rb.x=oldx+newvx
				Rb.y=oldy+newvy
				Rb.vx=newvx
				Rb.vy=newvy
				#print(Rb.vx,Rb.vy)
				#print(Rb.x, Rb.y)
				#print(count)
			else:
				Rb.x=oldx-2.3*Rb.vx
				Rb.y=oldy-2.3*Rb.vy
				print(Rb.vx,Rb.vy)
				print(Rb.x,Rb.y)
				print("a little trouble here")
		BC1[int(Rb.y)][int(Rb.x)]=2
		#coords[count]=[Rb.x,Rb.y]
		#print(coords[count])
		count+=1	
		
		
		
		
		
def plotter(map):
	fig1, ax1= plt.subplots()
	plt.imshow(map,origin="lower", 				cmap='gist_heat',interpolation='nearest')
	plt.colorbar()
	plt.show()

propagator()

plotter(BC1)
