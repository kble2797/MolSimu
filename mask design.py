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

def crt_pcavity(x,y,rot):
	a=pill_cav_final(x,y,pc_l,pc_w,500,rot)
	cavity_pair.add(a)

def crt_path(w,l,x,y,dir):
	path=gdspy.Path(w,(x,y))
	path.segment(l,dir,**spec1)
	cavity_pair.add(path)

def aperture(x,y,w,l):
	crt_donut(x,y,oc_l,oc_w,500)
	crt_path(w,l,x,y+oc_l/2,'+y')
	crt_pcavity(x,y+l+oc_l/2+pc_l/2,-90)

def cavity_pipe(x,y,width,separation_1,width_1): #keeping same surface area
	length=separation_1*width_1/width
	crt_donut(x,y,oc_l,oc_w,500)
	ynew=length+pc_l/2+oc_l/2
	crt_pcavity(x,y+ynew,-90)
	path1=gdspy.Path(width,(x,y+oc_l/2))
	path1.segment(length,'+y',**spec1)
	cavity_pair.add(path1)

def n_parallels(x,y,width,length,n,separation): #same length, varying surface area (or width)
	crt_donut(x,y,oc_l,oc_w,500)
	ynew=length+pc_l/2+oc_l/2
	crt_pcavity(x,y+ynew,-90)
	path1=gdspy.Path(width,(x,y+oc_l/2),n,separation)
	if n % 2 == 0:
		for i in range(int(n/2)):
			cavity_pair.add(op_cav_funnel(x-separation/2-i*separation,y+oc_l/2,50,width,0))
			cavity_pair.add(op_cav_funnel(x+separation/2+i*separation,y+oc_l/2,50,width,0))
			cavity_pair.add(op_cav_funnel(x-separation/2-i*separation,y+oc_l/2+length,50,width,180))
			cavity_pair.add(op_cav_funnel(x+separation/2+i*separation,y+oc_l/2+length,50,width,180))
	else:
		for i in range(int((n+1)/2)):
			cavity_pair.add(op_cav_funnel(x-i*separation,y+oc_l/2,50,width,0))
			cavity_pair.add(op_cav_funnel(x+i*separation,y+oc_l/2,50,width,0))
			cavity_pair.add(op_cav_funnel(x-i*separation,y+oc_l/2+length,50,width,180))
			cavity_pair.add(op_cav_funnel(x+i*separation,y+oc_l/2+length,50,width,180))
	path1.segment(length,'+y',**spec1)
	cavity_pair.add(path1)

def cavity_pipe_sl(x,y,width,width_f,length,oc_l,oc_w): #same length, varying surface area (or width)
	crt_donut(x,y,oc_l,oc_w,500)
	ynew=length+pc_l/2+oc_l/2
	crt_pcavity(x,y+ynew,-90)
	path1=gdspy.Path(width,(x,y+oc_l/2))
	path1.segment(length/2,'+y',**spec1)
	path1.segment(length/2,'+y',final_width=width_f,**spec1)
	cavity_pair.add(path1)
	cavity_pair.add(op_cav_funnel(x,y+oc_l/2,50,width,0))
	cavity_pair.add(op_cav_funnel(x,y+length+oc_l/2,50,width_f,180))

def cavity_serpentine(x,y,width,path_length,turns):
	crt_donut(x,y,oc_l,oc_w,500)
	cavity_pair.add(op_cav_funnel(x,y+oc_l/2,50,width,0))
	segment_length=path_length/(2*turns+2)
	path2=gdspy.Path(width,(x,y+oc_l/2))
	path2.segment(segment_length,'+y',**spec1)	
	for n in range(turns):
		path2.turn(width,'r',**spec1)
		path2.segment(segment_length,'+x',**spec1)
		path2.turn(width,'ll',**spec1)
		path2.segment(segment_length,'-x',**spec1)
		path2.turn(width,'r',**spec1)
	path2.segment(segment_length,'+y',**spec1)		
	cavity_pair.add(path2)
	y_2=2*segment_length+(4*turns)*width
	crt_pcavity(x,y+oc_l/2+pc_l/2+y_2,-90)
	cavity_pair.add(op_cav_funnel(x,y+oc_l/2+y_2,50,width,180))

def parallel_channel(x,y,width,path_len,branches):
	crt_donut(x,y,oc_l,oc_w,500)
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

def linear_chambers(x,y,width,length,n):
	crt_donut(x,y,oc_l,oc_w,500)
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
		crt_donut(c[i],d[i],oc_l,oc_w,500)

def zigzag_channel(x,y,w,length,n):
	crt_donut(x,y,oc_l,oc_w,500)
	cavity_pair.add(op_cav_funnel_angled(x,y+oc_l/2,100,0,w))
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
	crt_pcavity(x,y+oc_l/2+pc_l/2+2*n*(l/np.sqrt(2)),-90)
	cavity_pair.add(op_cav_funnel_angled(x,y+oc_l/2+2*n*(l/np.sqrt(2)),100,0,w))

def weird_pipe(x,y,w_min,w_max,l,n):
	crt_donut(x,y,oc_l,oc_w,500)
	sin_path=gdspy.Path(w_min,(x,y+oc_l/2))
	sin_path.parametric(lambda u: (0,l*u),lambda u: (0,l), final_width=lambda u : w_min
	- (w_max-w_min)*np.sin(n*2*pi*u), number_of_evaluations=512,**spec1)
	cavity_pair.add(sin_path)
	crt_pcavity(x,y+oc_l/2+l+pc_l/2,-90)

def longpipe(x,y,w,dir,l):
	crt_donut(x,y,oc_l,oc_w,500)
	cavity_pair.add(op_cav_funnel_angled(x,y+oc_l/2,100,0,w))
	path=gdspy.Path(w,(x,y+oc_l/2))
	path.segment(l,dir,**spec1)
	cavity_pair.add(path)
	crt_pcavity(x-(l*np.cos(pi-dir))-pc_w/2,y+3*pc_w/8+oc_l/2+(l*np.sin(pi-dir)),-90)
	cavity_pair.add(op_cav_funnel_angled(x-(l*np.cos(pi-dir)),y+oc_l/2+(l*np.sin(pi-dir)),50,0,w))
	


# ------------------------------------------------------------------ #
#		Generating cells
# ------------------------------------------------------------------ #

cavity_pipe_sl(9075,6500,10,10,2000,oc_l,oc_w)
cavity_pipe_sl(15125,6500,15,15,2000,oc_l,oc_w)
cavity_pipe_sl(21175,6500,20,20,2000,oc_l,oc_w)
cavity_pipe_sl(27225,6500,25,25,2000,oc_l,oc_w)

cavity_pipe_sl(-39325,6500,10,10,2000,2000,2000)
cavity_pipe_sl(-27225,-1000,10,10,2000,2500,2500)
cavity_pipe_sl(-33275,-1000,10,10,2000,3500,3500)
cavity_pipe_sl(-39325,-1000,10,10,2000,4000,4000)


cavity_pipe_sl(9075,14000,10,50,2000,oc_l,oc_w)
cavity_pipe_sl(15125,14000,10,100,2000,oc_l,oc_w)
cavity_pipe_sl(21175,14000,10,150,2000,oc_l,oc_w)
cavity_pipe_sl(27225,14000,10,200,2000,oc_l,oc_w)


cavity_serpentine(15125,21500,20,2000,1)
cavity_serpentine(21175,21500,20,2000,2)
cavity_serpentine(27225,21500,20,2000,3)
cavity_serpentine(33275,21500,20,2000,4)


zigzag_channel(9075,29000,20,2000,3)
zigzag_channel(15125,29000,20,2000,4)
zigzag_channel(21175,29000,20,2000,5)
zigzag_channel(27225,29000,20,2000,6)


weird_pipe(3025,36500,200,220,2000,10)
weird_pipe(9075,36500,200,220,2000,20)
weird_pipe(15125,36500,200,300,2000,10)
weird_pipe(-3025,36500,200,390,2000,5)


n_parallels(-9075,14000,10,2000,2,200)
n_parallels(-3025,14000,10,2000,3,200)
n_parallels(3025,14000,10,2000,4,200)


#aperture
cavity_pipe_sl(39325,14000,100,100,500,oc_l,oc_w)
cavity_pipe_sl(39325,6500,250,250,500,oc_l,oc_w)
cavity_pipe_sl(33275,14000,500,500,500,oc_l,oc_w)
cavity_pipe_sl(33275,6500,1000,1000,500,oc_l,oc_w)


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


# Manually:

p_l=4000
x=-9075
y=36500
l=p_l/8

crt_donut(x,y,oc_l,oc_w,500)
path1=gdspy.Path(20,(x,y+oc_l/2))
path1.segment(l,'+y',**spec1)
path1.turn(20,'l',**spec1)
path1.segment(l,'-x',**spec1)
path1.turn(20,'r',**spec1)
path1.segment(l,'+y',**spec1)
path1.turn(20,'r',**spec1)
path1.segment(l,'+x',**spec1)
path1.turn(20,'l',**spec1)
path1.segment(l,'+y',**spec1)
path2=gdspy.Path(20,(x,y+oc_l/2))
path2.segment(l,'+y',**spec1)
path2.turn(20,'r',**spec1)
path2.segment(l,'+x',**spec1)
path2.turn(20,'l',**spec1)
path2.segment(l,'+y',**spec1)
path2.turn(20,'l',**spec1)
path2.segment(l,'-x',**spec1)
path2.turn(20,'r',**spec1)
path2.segment(l,'+y',**spec1)

crt_pcavity(x,y+pc_l/2+oc_l/2+3*l+80,180)
cavity_pair.add(op_cav_funnel(x,y+oc_l/2,50,20,0))
cavity_pair.add(op_cav_funnel(x,y+oc_l/2+3*l+80,50,20,180))

cavity_pair.add(path1)
cavity_pair.add(path2)

#---------------------------------------#
x2=-15125
y2=36500

crt_donut(x2,y2,oc_l,oc_w,500)
cavity_pair.add(op_cav_funnel(x2-50,y2+oc_l/2,50,10,0))
cavity_pair.add(op_cav_funnel(x2-50,y2+oc_l/2+3*l+40,50,10,180))
path1=gdspy.Path(5,(x2-50,y2+oc_l/2))
path1.segment(l,'+y',**spec1)
path1.turn(10,'l',**spec1)
path1.segment(l,'-x',**spec1)
path1.turn(10,'r',**spec1)
path1.segment(l,'+y',**spec1)
path1.turn(10,'r',**spec1)
path1.segment(l,'+x',**spec1)
path1.turn(10,'l',**spec1)
path1.segment(l,'+y',**spec1)
cavity_pair.add(op_cav_funnel(x2+50,y2+oc_l/2,50,10,0))
cavity_pair.add(op_cav_funnel(x2+50,y2+oc_l/2+3*l+40,50,10,180))
path2=gdspy.Path(5,(x2+50,y2+oc_l/2))
path2.segment(l,'+y',**spec1)
path2.turn(10,'r',**spec1)
path2.segment(l,'+x',**spec1)
path2.turn(10,'l',**spec1)
path2.segment(l,'+y',**spec1)
path2.turn(10,'l',**spec1)
path2.segment(l,'-x',**spec1)
path2.turn(10,'r',**spec1)
path2.segment(l,'+y',**spec1)

crt_pcavity(x2,y2+pc_l/2+oc_l/2+3*l+40,180)

cavity_pair.add(path1)
cavity_pair.add(path2)

#---------------------------------------#
crt_donut(3025,29000,oc_l,oc_w,500)
crt_donut(-3025,29000,oc_l,oc_w,500)
crt_donut(-9075,29000,oc_l,oc_w,500)
cavity_pair.add(op_cav_funnel(-9075,29000+oc_l/2,100,45,0))
crt_donut(-15125,29000,oc_l,oc_w,500)
cavity_pair.add(op_cav_funnel(-15125,29000+oc_l/2,100,45,0))
crt_donut(-21175,29000,oc_l,oc_w,500)
crt_donut(-27225,29000,oc_l,oc_w,500)

crt_pcavity(-24200,33500,270)
cavity_pair.add(op_cav_funnel(-24200+pc_l/2,33500,100,60,-90))
cavity_pair.add(op_cav_funnel(-24200,33500-pc_l/2,50,15,180))
crt_pcavity(0,33500,180)
cavity_pair.add(op_cav_funnel(0-pc_l/2,33500,100,60,+90))
cavity_pair.add(op_cav_funnel(0,33500-pc_l/2,50,15,180))

crt_path(15,3500,-24200,33500-pc_l/2,-pi/2)
crt_path(15,3500,0,33500-pc_l/2,-pi/2)
crt_path(15,3050,-27225+oc_w/2,29250,0)
cavity_pair.add(op_cav_funnel(-27225+oc_w/2,29250,50,10,-90))
cavity_pair.add(op_cav_funnel(-27225+oc_w/2+3050,29250,50,10,90))
crt_path(15,3050,-3025+oc_w/2,29250,0)
cavity_pair.add(op_cav_funnel(-3025+oc_w/2,29250,50,10,-90))
cavity_pair.add(op_cav_funnel(-3025+oc_w/2+3050,29250,50,10,90))
crt_path(60,22700,-24200+pc_w/2,33500,0)
crt_path(60,3000,-15125,33500,-pi/2)
crt_path(60,3000,-9075,33500,-pi/2)

#---------------------------------------#
crt_donut(-9075,6500,oc_l,oc_w,500)
cavity_pair.add(op_cav_funnel(-9075+oc_w/2,6500,50,50,-90))
crt_donut(-3025,-1000,oc_l,oc_w,500)
cavity_pair.add(op_cav_funnel(-3025,-1000+oc_l/2,50,50,0))
crt_donut(3025,6500,oc_l,oc_w,500)
cavity_pair.add(op_cav_funnel(3025-oc_w/2,6500,50,50,90))
crt_pcavity(-3025,10500,-90)
cavity_pair.add(op_cav_funnel(-3025,10500-pc_l/2,50,50,180))

cir=gdspy.Path(50,(-3025,9750))
cir.segment(2750,'-y',**spec1)

# def circle(u):
#     r = 500
#     theta = 2 * u * np.pi
#     x = r * np.cos(theta)
#     y = r * np.sin(theta)-500
#     return (x, y)
# cir.parametric(circle,**spec1)

cavity_pair.add(gdspy.Round((-3025,6500),550,
inner_radius=500,initial_angle=pi/2, final_angle=5*pi/2-5*pi/180,tolerance=0.01,**spec1))
crt_path(50,4050,-3525,6500,pi)
crt_path(50,4050,-2525,6500,0)
crt_path(50,5501,-3025,6000,-pi/2)


cavity_pair.add(cir)


# ------------------------------------------------------------------ #
#      Write and view file
# ------------------------------------------------------------------ #

gdspy.write_gds('Cell_loc.gds',unit=units,precision=1.0e-9)

gdspy.LayoutViewer()