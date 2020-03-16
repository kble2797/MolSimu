#----------------------#
#	KL Mask design
#----------------------#
import numpy as np
import gdspy
from scipy.constants import k,pi,N_A
from pill_cav_final import pill_cav_final
from OPCavFunnel import op_cav_funnel
from OPCavFunnelAngled import op_cav_funnel_angled

spec1={'layer':1,'datatype':1}
spec2={'layer':2,'datatype':2}
units=1.0e-6

oc_w=3000
oc_l=3000

pc_w=1500
pc_l=1500

# ------------------------------------------------------------------ #
#      Functions
# ------------------------------------------------------------------ #

cavity_pair = gdspy.Cell("POLYGONS")
path_cell=gdspy.Cell('PATHS')

def crt_cavity(x,y):
	cavity_pair.add(gdspy.Rectangle((-oc_w/2+x,-oc_l/2+y),(oc_w/2+x,oc_l/2+y),**spec1))
	

def crt_donut(xcenter,ycenter,length, width,rim_width,):
	p1=gdspy.Rectangle((xcenter-width/2,ycenter-length/2),(xcenter+width/2,ycenter+length/2))
	p2=gdspy.Rectangle((xcenter-width/2+rim_width,ycenter-length/2+rim_width),(xcenter+width/2-rim_width,ycenter+length/2-rim_width))
	p3=gdspy.boolean(p1,p2,'not',**spec1)
	cavity_pair.add(p3)


def crt_pcavity(x,y,rot=0):
	a=pill_cav_final(x,y,pc_l,pc_w,500,rot)
	cavity_pair.add(a)


def crt_path(w,l,x,y,dir):
	path=gdspy.Path(w,(x,y))
	path.segment(l,dir,**spec1)
	cavity_pair.add(path)


def linear_channel(x,y,w,l):
	crt_donut(x,y,oc_l,oc_w,500)
	crt_path(w,l,x,y+oc_l/2,'+y')
	crt_pcavity(x,y+l+oc_l/2+pc_l/2,-90)
	cavity_pair.add(op_cav_funnel(x,y+oc_l/2,50,w,0))
	cavity_pair.add(op_cav_funnel(x,y+l+oc_l/2,50,w,180))

def longpipe(x,y,w,dir,l):
	crt_donut(x,y,oc_l,oc_w,500)
	cavity_pair.add(op_cav_funnel_angled(x,y+oc_l/2,100,0,w))
	path=gdspy.Path(w,(x,y+oc_l/2))
	path.segment(l,dir,**spec1)
	cavity_pair.add(path)
	crt_pcavity(x-(l*np.cos(pi-dir))-pc_w/2,y+3*pc_w/8+oc_l/2+(l*np.sin(pi-dir)),-90)
	cavity_pair.add(op_cav_funnel_angled(x-(l*np.cos(pi-dir)),y+oc_l/2+(l*np.sin(pi-dir)),50,0,w))

def angle_path(x,y,w,l1,l2,k):
	crt_donut(x,y,oc_l,oc_w,500)
	path=gdspy.Path(w,(x,y+oc_l/2))
	path.segment(l2,"+y",**spec1)


# ------------------------------------------------------------------ #
#		Generating cells
# ------------------------------------------------------------------ #

# Channels ranging in cross sections (50 microns deep is our new fixed depth) with lengths from 1 mm to 5 mm
# but mostly in the 1-3 mm range in steps of 500 microns and with widths of 50 to 500 microns in steps of 50 (should give 60 experiments)

# w = 50um
for i in range(6):
	longpipe(-15125+6050*i,36500,50,10*pi/12,1000+500*i)		

# w = 100um
for i in range(3):
	longpipe(-27225+6050*i,29000,100,10*pi/12,1000+500*i)
for i in range(3):
	longpipe(-27225+6050*i,21500,100,10*pi/12,3000+500*i)

# w = 150um
for i in range(3):
	longpipe(-9075+6050*i,29000,150,10*pi/12,1000+500*i)
for i in range(3):
	longpipe(-9075+6050*i,21500,150,10*pi/12,3000+500*i)

# w = 200um
for i in range(3):
	longpipe(9075+6050*i,29000,200,10*pi/12,1000+500*i)
for i in range(3):
	longpipe(9075+6050*i,21500,200,10*pi/12,3000+500*i)	

# w = 250um
for i in range(4):
	longpipe(27225,29000-7500*i,250,10*pi/12,1000+500*i)
for i in range(2):
	longpipe(33275,21500-7500*i,250,10*pi/12,3500+500*i)

# w = 300um
for i in range(3):
	longpipe(-27225+6050*i,14000,300,10*pi/12,1000+500*i)
for i in range(3):
	longpipe(-27225+6050*i,6500,300,10*pi/12,3000+500*i)

# w = 350um
for i in range(3):
	longpipe(-9075+6050*i,14000,350,10*pi/12,1000+500*i)
for i in range(3):
	longpipe(-9075+6050*i,6500,350,10*pi/12,3000+500*i)

# w = 400um
for i in range(3):
	longpipe(9075+6050*i,14000,400,10*pi/12,1000+500*i)
for i in range(3):
	longpipe(9075+6050*i,6500,400,10*pi/12,3000+500*i)

# w = 450um
for i in range(4):
	longpipe(39325,14000-7500*i,450,10*pi/12,1000+500*i)
for i in range(2):
	longpipe(33275,6500-7500*i,450,10*pi/12,3500+500*i)

# w = 500um
for i in range(6):
	longpipe(-3025+6050*i,-1000,500,10*pi/12,1000+500*i)

# 16 experiments will be dedicated to angles in the channel (3 mm total length with the bend 1 mm from the pill cavity,
# widths of 50 microns to 200 microns in 50 micron steps, angles of 90 degrees, 45 degrees, 22.5 degrees, and 135 degrees)

angle_path(-9075,-8500,50,1000,2000,pi/2)
	

# ------------------------------------------------------------------ #
#      Write and view file
# ------------------------------------------------------------------ #

gdspy.write_gds('Cell_loc_v2.gds',unit=units,precision=1.0e-9)

gdspy.LayoutViewer()