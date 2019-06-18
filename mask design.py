#----------------------#
#	KL Mask design
#----------------------#
import numpy as np
import gdspy
from scipy.constants import k,pi,N_A


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

cavity_pair= gdspy.Cell("POLYGONS")
path_cell=gdspy.Cell('PATHS')

def crt_cavity(x,y):
	cavity_pair.add(gdspy.Rectangle((-oc_w/2+x,-oc_l/2+y),(oc_w/2+x,oc_l/2+y),**spec1))

def crt_pcavity(x,y):
	cavity_pair.add(gdspy.Rectangle((-pc_w/2+x,-pc_l/2+y),(pc_w/2+x,pc_l/2+y),**spec1))

def crt_donut(x,y):
	a=gdspy.Rectangle((-oc_w/2+x,-oc_l/2+y),(oc_w/2+x,oc_l/2+y),**spec1)


def crt_path(w,l,x,y,dir):
	path=gdspy.Path(w,(x,y))
	path.segment(l,dir,**spec1)
	cavity_pair.add(path)

def aperture(x,y,w,l):
	crt_cavity(x,y)
	crt_path(w,l,x,y+oc_l/2,'+y')
	crt_pcavity(x,y+l+oc_l/2+pc_l/2)

def cavity_pipe(x,y,width,separation_1,width_1): #keeping same surface area
	length=separation_1*width_1/width
	crt_cavity(x,y)
	ynew=length+pc_l/2+oc_l/2
	cavity_pair.add(gdspy.Rectangle((-pc_w/2+x,-pc_l/2+y+ynew),(pc_w/2+x,pc_l/2+y+ynew),**spec1))
	path1=gdspy.Path(width,(x,y+oc_l/2))
	path1.segment(length,'+y',**spec1)
	cavity_pair.add(path1)

def n_parallels(x,y,width,length,n,separation): #same length, varying surface area (or width)
	crt_cavity(x,y)
	ynew=length+pc_l/2+oc_l/2
	crt_pcavity(x,y+ynew)
	path1=gdspy.Path(width,(x,y+oc_l/2),n,separation)
	path1.segment(length,'+y',**spec1)
	cavity_pair.add(path1)

def cavity_pipe_sl(x,y,width,width_f,length): #same length, varying surface area (or width)
	crt_cavity(x,y)
	ynew=length+pc_l/2+oc_l/2
	cavity_pair.add(gdspy.Rectangle((-pc_w/2+x,-pc_l/2+y+ynew),(pc_w/2+x,pc_l/2+y+ynew),**spec1))
	path1=gdspy.Path(width,(x,y+oc_l/2))
	path1.segment(length/2,'+y',**spec1)
	path1.segment(length/2,'+y',final_width=width_f,**spec1)
	cavity_pair.add(path1)

def cavity_serpentine(x,y,width,path_length,turns):
	crt_cavity(x,y)
	segment_length=path_length/(2*turns+2)
	path2=gdspy.Path(width,(x,y+oc_l/2))
	path2.segment(segment_length,'+y',**spec1)	
	for n in range(turns):
		path2.turn(width,'r',**spec1)
		path2.segment(segment_length,'+x',**spec1)
		path2.turn(width,'ll',**spec1)
		path2.segment(segment_length,'-x',**spec1)
		path2.turn(width,'r',**spec1)
	path2.segment(segment_length-width,'+y',**spec1)		
	cavity_pair.add(path2)
	y_2=2*segment_length+(4*turns-1)*width
	cavity_pair.add(gdspy.Rectangle((-pc_w/2+x,-oc_l/2+y+oc_l+y_2),(pc_w/2+x,oc_l/2+pc_l+y+y_2),**spec1))

def parallel_channel(x,y,width,path_len,branches):
	crt_cavity(x,y)
	segment_length=path_len/(2*branches)
	path3=gdspy.Path(width,(x,y+oc_l/2))
	path3.segment(segment_length,'+y',**spec1)
	path41=gdspy.Path(width,(x,y+oc_l/2+segment_length))
	path42=gdspy.Path(width,(x,y+oc_l/2+segment_length))
	if branches % 2 != 0:		
		path3.segment(segment_length,'+y',**spec1)
		for n in range(int((branches-1)/2)-1):
			path41.segment(oc_w/(branches-1),'-x',**spec1)
			path41.segment(segment_length,'+y',**spec1)
			path41.segment(segment_length,'-y',**spec1)
			path42.segment(oc_w/(branches-1),'+x',**spec1)
			path42.segment(segment_length,'+y',**spec1)
			path42.segment(segment_length,'-y',**spec1)
		path41.segment((oc_w/(branches-1))/2,'-x',**spec1)
		path41.segment(segment_length,'+y',**spec1)
		path42.segment((oc_w/(branches-1))/2,'+x',**spec1)
		path42.segment(segment_length,'+y',**spec1)			
	else:
		for n in range(int((branches)/2)-1):
			path41.segment(oc_w/(branches),'-x',**spec1)
			path41.segment(segment_length,'+y',**spec1)
			path41.segment(segment_length,'-y',**spec1)
			path42.segment(oc_w/(branches),'+x',**spec1)
			path42.segment(segment_length,'+y',**spec1)
			path42.segment(segment_length,'-y',**spec1)
		path41.segment((oc_w/(branches-1))/2,'-x',**spec1)
		path41.segment(segment_length,'+y',**spec1)
		path42.segment((oc_w/(branches-1))/2,'+x',**spec1)
		path42.segment(segment_length,'+y',**spec1)
	cavity_pair.add(path3)
	cavity_pair.add(path41)
	cavity_pair.add(path42)
	cavity_pair.add(gdspy.Rectangle((-pc_w/2+x,y+oc_l/2+2*segment_length),(pc_w/2+x,pc_l+y+oc_l/2+2*segment_length),**spec1))

def linear_chambers(x,y,width,length,n): # here the pc = oc
	crt_cavity(x,y)	
	for i in range(n):
		x_i=i*(length+oc_w)
		cavity_pair.add(gdspy.Rectangle((oc_w/2+x+length+x_i,-oc_l/2+y),(oc_w/2+x+oc_w+length+x_i,oc_l/2+y),**spec1))
	path=gdspy.Path(width,(x+oc_w/2,y))
	path.segment(length*n+(n-1)*oc_w,'+x',**spec1)
	cavity_pair.add(path)

def n_chambers(x,y,w,l,n): # n<=4
	cavity_pair.add(gdspy.Rectangle((-pc_w/2+x,-pc_l/2+y),(pc_w/2+x,pc_l/2+y),**spec1))
	a=(x,x+pc_w/2,x,x-pc_w/2)
	b=(y+pc_l/2,y,y-pc_l/2,y)
	c=(x,x+pc_w/2+l+oc_w/2,x,x-oc_w/2-l-pc_w/2)
	d=(y+pc_l/2+l+oc_l/2,y,y-pc_l/2-l-oc_l/2,y)
	for i in range(n):
		crt_path(w,l,a[i],b[i],pi/2-i*pi/2)
		crt_cavity(c[i],d[i])

def zigzag_channel(x,y,w,length,n):
	crt_cavity(x,y)
	a=np.zeros((2*n+1,2))
	l=length/(2*n)			
	for i in range(2*n+1):	
		if i % 2 == 0:
			a[i][0]=x
			a[i][1]=y+oc_l/2+i*(l/np.sqrt(2))
		else:
			a[i][0]=x-l/np.sqrt(2)
			a[i][1]=y+oc_l/2+i*(l/np.sqrt(2))
	path=gdspy.FlexPath(a,w,corners='smooth',**spec1)
	cavity_pair.add(path)
	cavity_pair.add(gdspy.Rectangle((x-pc_w/2,y+oc_l/2+2*n*(l/np.sqrt(2))),
	(x+pc_w/2,y+oc_l/2+pc_l+2*n*(l/np.sqrt(2))),**spec1))

def weird_pipe(x,y,w_min,w_max,l,n):
	crt_cavity(x,y)
	sin_path=gdspy.Path(w_min,(x,y+oc_l/2))
	sin_path.parametric(lambda u: (0,l*u),lambda u: (0,l), final_width=lambda u : w_min
	- (w_max-w_min)*np.sin(n*2*pi*u), number_of_evaluations=512,**spec1)
	cavity_pair.add(sin_path)
	crt_pcavity(x,y+oc_l/2+l+pc_l/2)

def longpipe(x,y,w,dir,l):
	crt_cavity(x,y)
	path=gdspy.Path(w,(x,y+oc_l/2))
	path.segment(l,dir,**spec1)
	cavity_pair.add(path)
	crt_pcavity(x-(l*np.cos(pi-dir))-pc_w/2,y+3*pc_w/8+oc_l/2+(l*np.sin(pi-dir)))

# ------------------------------------------------------------------ #
#		Generating cells
# ------------------------------------------------------------------ #

cavity_pipe_sl(9075,6500,10,10,2000)
cavity_pipe_sl(15125,6500,15,15,2000)
cavity_pipe_sl(21175,6500,20,20,2000)
cavity_pipe_sl(27225,6500,25,25,2000)


cavity_pipe_sl(9075,14000,10,50,2000)
cavity_pipe_sl(15125,14000,10,100,2000)
cavity_pipe_sl(21175,14000,10,150,2000)
cavity_pipe_sl(27225,14000,10,200,2000)


cavity_serpentine(15125,21500,10,2000,1)
cavity_serpentine(21175,21500,10,2000,2)
cavity_serpentine(27225,21500,10,2000,3)
cavity_serpentine(33275,21500,10,2000,4)


zigzag_channel(9075,29000,10,2000,3)
zigzag_channel(15125,29000,10,2000,4)
zigzag_channel(21175,29000,10,2000,5)
zigzag_channel(27225,29000,10,2000,6)


weird_pipe(3025,36500,200,220,2000,10)
weird_pipe(9075,36500,200,220,2000,20)
weird_pipe(15125,36500,200,300,2000,10)
weird_pipe(-3025,36500,200,390,2000,5)


n_parallels(-9075,14000,10,2000,2,200)
n_parallels(-3025,14000,10,2000,3,200)
n_parallels(3025,14000,10,2000,4,200)


#aperture
cavity_pipe_sl(39325,14000,100,100,500)
cavity_pipe_sl(39325,6500,250,250,500)
cavity_pipe_sl(33275,14000,500,500,500)
cavity_pipe_sl(33275,6500,1000,1000,500)


longpipe(9075,21500,10,11*pi/12,2000)
longpipe(3025,21500,10,11*pi/12,4000)
longpipe(-3025,21500,10,11*pi/12,6000)
longpipe(-9075,21500,10,11*pi/12,8000)
longpipe(-15125,21500,10,11*pi/12,10000)
longpipe(-21175,21500,10,11*pi/12,12000)
longpipe(-15125,14000,10,11*pi/12,14000)
longpipe(-21175,14000,10,11*pi/12,16000)
longpipe(-15125,6500,10,11*pi/12,18000)
longpipe(-21175,6500,10,11*pi/12,20000)


linear_chambers(-9075,6500,2,3050,2)

# Manually:

p_l=4000
x=-9075
y=36500
l=p_l/8

crt_cavity(x,y)
path1=gdspy.Path(10,(x,y+oc_l/2))
path1.segment(l,'+y',**spec1)
path1.segment(l,'-x',**spec1)
path1.segment(l,'+y',**spec1)
path1.segment(l,'+x',**spec1)
path1.segment(l,'+y',**spec1)
path2=gdspy.Path(10,(x,y+oc_l/2+l))
path2.segment(l,'+x',**spec1)
path2.segment(l,'+y',**spec1)
path2.segment(l,'-x',**spec1)

crt_pcavity(x,y+pc_l/2+oc_l/2+3*l)

cavity_pair.add(path1)
cavity_pair.add(path2)

#---------------------------------------#
x2=-15125
y2=36500

crt_cavity(x2,y2)
path1=gdspy.Path(5,(x2-50,y2+oc_l/2))
path1.segment(l,'+y',**spec1)
path1.segment(l,'-x',**spec1)
path1.segment(l,'+y',**spec1)
path1.segment(l,'+x',**spec1)
path1.segment(l,'+y',**spec1)
path2=gdspy.Path(5,(x2+50,y2+oc_l/2))
path2.segment(l,'+y',**spec1)
path2.segment(l,'+x',**spec1)
path2.segment(l,'+y',**spec1)
path2.segment(l,'-x',**spec1)
path2.segment(l,'+y',**spec1)

crt_pcavity(x2,y2+pc_l/2+oc_l/2+3*l)

cavity_pair.add(path1)
cavity_pair.add(path2)

#---------------------------------------#
crt_donut(3025,29000)
crt_donut(-3025,29000)
crt_donut(-9075,29000)
crt_donut(-15125,29000)
crt_donut(-21175,29000)
crt_donut(-27225,29000)

# crt_pcavity(-24200,33500)
# crt_pcavity(0,33500)

# crt_path(2,3500,-24200,33500-pc_l/2,-pi/2)
# crt_path(2,3500,0,33500-pc_l/2,-pi/2)
# crt_path(2,3050,-27225+oc_w/2,29250,0)
# crt_path(2,3050,-3025+oc_w/2,29250,0)
# crt_path(2,22700,-24200+pc_w/2,33500,0)
# crt_path(2,3000,-15125,33500,-pi/2)
# crt_path(2,3000,-9075,33500,-pi/2)


# ------------------------------------------------------------------ #
#      Write and view file
# ------------------------------------------------------------------ #

gdspy.write_gds('Cell_loc.gds',unit=units,precision=1.0e-9)

gdspy.LayoutViewer()