# This code contains all of to designs I've created on a single wafer

import gdspy
import numpy as np
#from doughnuts import doughnut
#from pill_cav_final import *
#from OPCavFunnel import *

spec1={'layer':1,'datatype':1}
spec2={'layer':2,'datatype':2}
units=1.0e-6

Op_Cav_Width=3000
Op_Cav_Len=3000

Pill_Cav_Width=3000
Pill_Cav_Len=3000

gridspacingx=6050
gridspacingy=7500
gridpositionx=-27225
gridpositiony=-16000

pill_size=800

# ------------------------------------------------------------------ #
#      Make Cells
# ------------------------------------------------------------------ #

cavity_pair= gdspy.Cell("POLYGONS")
path_cell=gdspy.Cell('PATHS')

def pill_cav_final(xcenter,ycenter,length,width,separation,rotation):
	coords=[(pill_size,0),(width,0),(width,length),(0,length),(width-500,1e3),(width-500,500),(0.5*1e3,500),(pill_size,0.5e3)]
	coords=np.asarray(coords)
	for a,element in enumerate(coords):
		coords[a][0]+=xcenter-width/2
		coords[a][1]+=ycenter-length/2
	p1=gdspy.Polygon(coords)
	p2=gdspy.Round((xcenter-0.5*1e3,ycenter-0.6*1e3),pill_size,number_of_points=100)
	p3=gdspy.boolean(p1,p2,'or',**spec1)
	p4=gdspy.Rectangle((-width/2+xcenter-500,ycenter+200+200),(width/4+xcenter-500,length/2+ycenter),**spec1)
	p5=gdspy.boolean(p3,p4,'not',**spec1)
	p5.rotate(rotation*np.pi/180,(xcenter,ycenter))
	cavity_pair.add(p5)

def channel_bend(x,y,width,angle):
	length=1800
	#path length between cavities
	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x,-Op_Cav_Len/2+y),(Op_Cav_Width/2+x,Op_Cav_Len/2+y),**spec1))
	#creates optical cavity
	if angle>=5*np.pi/16:
		xnew=(length/2)*np.cos(angle)+700
		ynew=length/2+Pill_Cav_Len+(length/2)*np.sin(angle)-10-1500
		pill_cav_final(x+xnew,y+ynew,1500,2000,750,90)
		#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+xnew,-Op_Cav_Len/2+y+ynew),(Op_Cav_Width/4+x+xnew,y+ynew),**spec1))
	else:
		xnew=(length/2)*np.cos(angle)+Op_Cav_Width/4-5+250
		ynew=length/2+Pill_Cav_Len/2+(length/2)*np.sin(angle)+500+50
		pill_cav_final(x+xnew,y+ynew,1500,2000,750,180)
		#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+xnew,-Op_Cav_Len/4+y+ynew),(Op_Cav_Width/4+x+xnew,Op_Cav_Len/4+y+ynew),**spec1))
	#defines position and creates pill cavity
	path1=gdspy.Path(width,(x,y+Op_Cav_Len/2))
	path1.segment(length/2,'+y',**spec1)
	#creates the path from the pill cavity to the bend
	path2=gdspy.Path(width,(x,y+Op_Cav_Len/2+length/2-5))
	path2.segment(length/2,angle,**spec1)
	#creates the path from the second cavity to the bend

	cavity_pair.add(path1)
	cavity_pair.add(path2)


def channel_bend_circ(x,y,width,angle,radius):
	length=1800
	#length of the channel between cavities
	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x,-Op_Cav_Len/2+y),(Op_Cav_Width/2+x,Op_Cav_Len/2+y),**spec1))
	#creates optical cavity
	if angle>=np.pi/4:
		xnew=(length/2)*np.cos(angle)+50+600
		ynew=length/2+Pill_Cav_Len+(length/2)*np.sin(angle)-5-750
		pill_cav_final(x+xnew,y+ynew,1500,2000,750,180)
		#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+xnew,-Op_Cav_Len/2+y+ynew),(Op_Cav_Width/4+x+xnew,Op_Cav_Len/4+y+ynew-Op_Cav_Len/4),**spec1))
	else:
		xnew=(length/2)*np.cos(angle)+Op_Cav_Width/4-5+250
		ynew=length/2+Pill_Cav_Len/2+(length/2)*np.sin(angle)+500+50
		pill_cav_final(x+xnew,y+ynew,1500,2000,750,180)
		#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+xnew,-Op_Cav_Len/4+y+ynew),(Op_Cav_Width/4+x+xnew,Op_Cav_Len/4+y+ynew),**spec1))
	#defines position and creates pill cavity
	path1=gdspy.Path(width,(x,y+Op_Cav_Len/2))
	path1.segment(length/2,'+y',**spec1)
	#creates the path from the pill cavity to the bend
	path2=gdspy.Path(width,(x,y+Op_Cav_Len/2+length/2))
	path2.segment(length/2,angle,**spec1)
	#creates the path from the second cavity to the bend
	cavity_pair.add(gdspy.Round((x,y+length/2+Pill_Cav_Len/2),radius,**spec1))
	#creates the circle

	cavity_pair.add(path1)
	cavity_pair.add(path2)


def avoid_bounceback(x,y,width,angle):
	length=2000
	#length of the path between cavities
	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x,-Op_Cav_Len/2+y),(Op_Cav_Width/2+x,Op_Cav_Len/2+y),**spec1))
	#creates optical cavity
	if angle==np.pi/2:
		xnew=length*np.cos(angle)
		ynew=Pill_Cav_Len+length*np.sin(angle)
		#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+xnew,-Op_Cav_Len+y+ynew-2*length-Op_Cav_Len),(Op_Cav_Width/4+x+xnew,y+ynew-Op_Cav_Len/2-2*length-Op_Cav_Len),**spec1))
		path1=gdspy.Path(width,(x,y+Op_Cav_Len/2-length-Op_Cav_Len))
		path1.segment(length,angle,**spec1)
		#creates the path from the optical cavity to the pill cavity
	
	elif angle>=np.pi/4:
		xnew=length*np.cos(angle)
		ynew=Pill_Cav_Len+length*np.sin(angle)-10
		#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+xnew,-Op_Cav_Len/2+y+ynew),(Op_Cav_Width/4+x+xnew,Op_Cav_Len/4+y+ynew-Op_Cav_Len/4),**spec1))
		path1=gdspy.Path(width,(x,y+Op_Cav_Len/2-5))
		path1.segment(length,angle,**spec1)
		#creates the path from the optical cavity to the pill cavity
	
	else:
		xnew=length*np.cos(angle)+Op_Cav_Width/4-5
		ynew=Pill_Cav_Len+length*np.sin(angle)-Op_Cav_Len/2+500-5
		#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+xnew,-Op_Cav_Len/4+y+ynew),(Op_Cav_Width/4+x+xnew,Op_Cav_Len/4+y+ynew),**spec1))
		#defines position and creates pill cavity
		path1=gdspy.Path(width,(x,y+Op_Cav_Len/2-5))
		path1.segment(length,angle,**spec1)
		#creates the path from the optical cavity to the pill cavity
	
	cavity_pair.add(path1)


def avoid_bounceback_corner(x,y,width,angle):
	length=2000
	#length of path between cavities
	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x,-Op_Cav_Len/2+y),(Op_Cav_Width/2+x,Op_Cav_Len/2+y),**spec1))
	#creates optical cavity
	if angle>=np.pi/4:
		xnew=length*np.cos(angle)+Op_Cav_Width/2-5
		ynew=Pill_Cav_Len+length*np.sin(angle)-10
		#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+xnew,-Op_Cav_Len/2+y+ynew),(Op_Cav_Width/4+x+xnew,y+ynew),**spec1))
	else:
		xnew=length*np.cos(angle)+Op_Cav_Width/4+Op_Cav_Width/2-10
		ynew=Pill_Cav_Len+length*np.sin(angle)-Op_Cav_Len/2+500-5
		#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+xnew,-Op_Cav_Len/4+y+ynew),(Op_Cav_Width/4+x+xnew,Op_Cav_Len/4+y+ynew),**spec1))
	#defines position and creates pill cavity
	path1=gdspy.Path(width,(x+Op_Cav_Width/2-5,y+Op_Cav_Len/2-5))
	path1.segment(length,angle,**spec1)
	#creates the path from the optical cavity to the pill cavity

	cavity_pair.add(path1)


def avoid_bounceback_both_corners(x,y,width,angle):
	length=2000
	#length of path between cavities
	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x,-Op_Cav_Len/2+y),(Op_Cav_Width/2+x,Op_Cav_Len/2+y),**spec1))
	#creates optical cavity
	if angle>=np.pi/4:
		xnew=length*np.cos(angle)+Op_Cav_Width/2-10
		ynew=Pill_Cav_Len+length*np.sin(angle)-10
		#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+xnew+Pill_Cav_Width/4,-Op_Cav_Len/2+y+ynew),(Op_Cav_Width/4+x+xnew+Pill_Cav_Width/4,y+ynew),**spec1))
	else:
		xnew=length*np.cos(angle)+Op_Cav_Width/4+Op_Cav_Width/2-10
		ynew=Pill_Cav_Len+length*np.sin(angle)-Op_Cav_Len/2+500-10
		#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+xnew+Pill_Cav_Width/4,-Op_Cav_Len/4+y+ynew),(Op_Cav_Width/4+x+xnew+Pill_Cav_Width/4,Op_Cav_Len/4+y+ynew),**spec1))
	#defines position and creates pill cavity
	path1=gdspy.Path(width,(x+Op_Cav_Width/2-5,y+Op_Cav_Len/2-5))
	path1.segment(length,angle,**spec1)
	#creates the path from the optical cavity to the pill cavity

	cavity_pair.add(path1)


def const_len(x,y,width):
	length=4000
	#length of the channels
	length_pre_bend1=length/4
	length_post_bend1=length-length_pre_bend1
	length_pre_bend2=length/2
	length_post_bend2=length-length_pre_bend2
	length_pre_bend3=3*length/4
	length_post_bend3=length-length_pre_bend3
	#length_pre_bend is the length of the path from the pill cavity to the bend
	

	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x,-Op_Cav_Len/2+y),(Op_Cav_Width/2+x,Op_Cav_Len/2+y),**spec1))
	#creates optical cavity for the right top
	path1=gdspy.Path(width,(x+Op_Cav_Width/4,y-length_pre_bend1-Op_Cav_Len/2))
	path1.segment(length_pre_bend1,'+y',**spec1)
	cavity_pair.add(path1)
	#creates a path along the y axis for the middle
	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x-length_post_bend1-Pill_Cav_Width/4+Op_Cav_Width/4,-Op_Cav_Len/4+y-length_pre_bend1-Op_Cav_Len/2),(Op_Cav_Width/4+x-length_post_bend1-Pill_Cav_Width/4+Op_Cav_Width/4,Op_Cav_Len/4+y-length_pre_bend1-Op_Cav_Len/2),**spec1))
	path2=gdspy.Path(width,(x-length_post_bend1+Op_Cav_Width/4+5,y-length_pre_bend1-Op_Cav_Len/2+5))
	path2.segment(length_post_bend1,'+x',**spec1)
	cavity_pair.add(path2)
	#creates the pill cavity and the x axis path for the middle


	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x-gridspacingx,-Op_Cav_Len/2+y),(Op_Cav_Width/2+x-gridspacingx,Op_Cav_Len/2+y),**spec1))
	#creates optical cavity for the left
	path3=gdspy.Path(width,(x-gridspacingx+Op_Cav_Width/4,y-length_pre_bend2-Op_Cav_Len/2+Op_Cav_Len+length_pre_bend2))
	path3.segment(length_pre_bend2,'+y',**spec1)
	cavity_pair.add(path3)
	#creates a path along the y axis for the left
	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x-length_post_bend2-gridspacingx-Pill_Cav_Width/4+Op_Cav_Width/4,-Op_Cav_Len/4+y-length_pre_bend2-Op_Cav_Len/2),(Op_Cav_Width/4+x-length_post_bend2-gridspacingx-Pill_Cav_Width/4+Op_Cav_Width/4,Op_Cav_Len/4+y-length_pre_bend2-Op_Cav_Len/2),**spec1))
	path4=gdspy.Path(width,(x-length_post_bend2-gridspacingx+Op_Cav_Width/4+5,y-length_pre_bend2-Op_Cav_Len/2+Op_Cav_Len+2*length_pre_bend2-5))
	path4.segment(length_post_bend2,'+x',**spec1)
	cavity_pair.add(path4)
	#creates the pill cavity and the x axis path for the left top


	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x+gridspacingx,-Op_Cav_Len/2+y),(Op_Cav_Width/2+x+gridspacingx,Op_Cav_Len/2+y),**spec1))
	#creates optical cavity for the right
	path5=gdspy.Path(width,(x+gridspacingx-200,y-length_pre_bend3-Op_Cav_Len/2))
	path5.segment(length_pre_bend3,'+y',**spec1)
	cavity_pair.add(path5)
	#creates a path along the y axis for the right
	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x-length_post_bend3-Pill_Cav_Width/4+gridspacingx,-Op_Cav_Len/4+y-length_pre_bend3-Op_Cav_Len/2),(Op_Cav_Width/4+x-length_post_bend3-Pill_Cav_Width/4+gridspacingx,Op_Cav_Len/4+y-length_pre_bend3-Op_Cav_Len/2),**spec1))
	path6=gdspy.Path(width,(x-length_post_bend3+gridspacingx-200+5,y-length_pre_bend3-Op_Cav_Len/2+5))
	path6.segment(length_post_bend3,'+x',**spec1)
	cavity_pair.add(path6)
	#creates the pill cavity and the x axis path for the bottom
	


def double_cavity(x,y,width):
	length=gridspacingy/2-Op_Cav_Width
	x+=4*gridspacingx
	y-=gridspacingy
	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+gridspacingx/2,-Op_Cav_Len/4+y-250+Pill_Cav_Width/4),(Op_Cav_Width/4+x+gridspacingx/2,Op_Cav_Len/4+y-250+Pill_Cav_Width/4),**spec1))
	#creates pill cavity
	ynew=length+Op_Cav_Len
	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x,-Op_Cav_Len/2+y+ynew),(Op_Cav_Width/2+x,Op_Cav_Len/2+y+ynew),**spec1))
	#defines position and creates second cavity
	path1=gdspy.Path(width,(x+gridspacingx/2,y+Op_Cav_Len/2-250))
	path1.segment(500,'+y',**spec1)
	#creates the path from the pill cavity to the path connecting all the cavities
	path2=gdspy.Path(width,(x,y+Op_Cav_Len/2+length/2-125))
	path2.segment(500,'+y',**spec1)
	#creates the path from the second cavity to the path connecting them all

	path3=gdspy.Path(width,(x-width/2,y+Op_Cav_Len/2+width/2+length/2-125))
	path3.segment(gridspacingx,'+x',**spec1)
	cavity_pair.add(path3)
	#path connecting all the channels

	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x+gridspacingx,-Op_Cav_Len/2+y+ynew),(Op_Cav_Width/2+x+gridspacingx,Op_Cav_Len/2+y+ynew),**spec1))
	#creates a third cavity
	path4=gdspy.Path(width,(x+gridspacingx,y+Op_Cav_Len/2+length/2-125))
	path4.segment(500,'+y',**spec1)
	cavity_pair.add(path4)
	#creates the path to connect the third cavity to the path connecting them all

	cavity_pair.add(path1)
	cavity_pair.add(path2)


def double_circ_cavity(x,y,width,radius):
	length=gridspacingy/2-Op_Cav_Width
	x+=4*gridspacingx
	y-=gridspacingy
	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+gridspacingx/2,-Op_Cav_Len/4+y-250+Pill_Cav_Len/4),(Op_Cav_Width/4+x+gridspacingx/2,Op_Cav_Len/4+y-250+Pill_Cav_Len/4),**spec1))
	#creates pill cavity
	ynew=length+Op_Cav_Len
	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x,-Op_Cav_Len/2+y+ynew),(Op_Cav_Width/2+x,Op_Cav_Len/2+y+ynew),**spec1))
	#defines position and creates second cavity
	path1=gdspy.Path(width,(x+gridspacingx/2,y+Op_Cav_Len/2-250))
	path1.segment(500,'+y',**spec1)
	#creates the path from the pill cavity to the path connecting the two top cavities
	path2=gdspy.Path(width,(x,y+Op_Cav_Len/2+length/2-125))
	path2.segment(500,'+y',**spec1)
	#creates the path from the second cavity to the path connecting them all

	path3=gdspy.Path(width,(x-width/2,y+Op_Cav_Len/2+width/2+length/2-125))
	path3.segment(gridspacingx,'+x',**spec1)
	cavity_pair.add(path3)
	#path connecting all the channels

	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x+gridspacingx,-Op_Cav_Len/2+y+ynew),(Op_Cav_Width/2+x+gridspacingx,Op_Cav_Len/2+y+ynew),**spec1))
	#creates another cavity
	path4=gdspy.Path(width,(x+gridspacingx,y+Op_Cav_Len/2+length/2-125))
	path4.segment(500,'+y',**spec1)
	cavity_pair.add(path4)
	#creates the path to connect the third cavity to the path connecting them all

	cavity_pair.add(gdspy.Round((x+gridspacingx/2,y+length/2+Pill_Cav_Len/2-125),radius,**spec1))
	#creates the top circle

	cavity_pair.add(path1)
	cavity_pair.add(path2)


def double_circ_cavity_bottom(x,y,width,radius):
	length=gridspacingy/2-Op_Cav_Width
	ynew=length+Op_Cav_Len

	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+gridspacingx/2,-Op_Cav_Len/4+y-250-Pill_Cav_Len/4-2*500),(Op_Cav_Width/4+x+gridspacingx/2,Op_Cav_Len/4+y-250-Pill_Cav_Len/4-2*500),**spec1))
	#creates pill cavity
	path1=gdspy.Path(width,(x+gridspacingx/2,y+ynew-gridspacingy-Op_Cav_Len/2-500))
	path1.segment(6*500,'+y',**spec1)
	#creates the path below from the pill cavity to the path connecting the two bottom cavities

	cavity_pair.add(gdspy.Round((x+gridspacingx/2,y+length/2+Pill_Cav_Len/2-gridspacingy-125),radius,**spec1))
	#creates the bottom circle

	path2=gdspy.Path(width,(x-width/2,y+Op_Cav_Len/2+width/2+length/2-gridspacingy-125))
	path2.segment(gridspacingx,'+x',**spec1)
	cavity_pair.add(path2)
	#bottom path connecting the two bottom channels

	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x,-Op_Cav_Len/2+y+ynew-gridspacingy),(Op_Cav_Width/2+x,Op_Cav_Len/2+y+ynew-gridspacingy),**spec1))
	#defines position and creates a bottom cavity

	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x+gridspacingx,-Op_Cav_Len/2+y+ynew-gridspacingy),(Op_Cav_Width/2+x+gridspacingx,Op_Cav_Len/2+y+ynew-gridspacingy),**spec1))
	#creates another bottom cavity

	path3=gdspy.Path(width,(x,y+Op_Cav_Len/2+length/2-gridspacingy-125))
	path3.segment(500,'+y',**spec1)
	#creates the path from the first bottom cavity to the path connecting them all
	path4=gdspy.Path(width,(x+gridspacingx,y+Op_Cav_Len/2+length/2-gridspacingy-125))
	path4.segment(500,'+y',**spec1)
	#creates the path from the second bottom cavity to the path connecting them all

	cavity_pair.add(path1)
	cavity_pair.add(path2)
	cavity_pair.add(path3)
	cavity_pair.add(path4)

def double_circ_cavity_uneven(x,y,width,radius):
	length=gridspacingy/2-Op_Cav_Width
	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+gridspacingx/2+gridspacingx/4,y-250),(Op_Cav_Width/4+x+gridspacingx/2+gridspacingx/4,Op_Cav_Len/2+y-250),**spec1))
	#creates pill cavity
	ynew=length+Op_Cav_Len
	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x,-Op_Cav_Len/2+y+ynew),(Op_Cav_Width/2+x,Op_Cav_Len/2+y+ynew),**spec1))
	#defines position and creates second cavity
	path1=gdspy.Path(width,(x+gridspacingx/2+gridspacingx/4,y+Op_Cav_Len/2-250))
	path1.segment(500,'+y',**spec1)
	#creates the path from the pill cavity to the path connecting all the cavities
	path2=gdspy.Path(width,(x,y+Op_Cav_Len/2+length/2-125))
	path2.segment(500,'+y',**spec1)
	#creates the path from the second cavity to the path connecting them all

	path3=gdspy.Path(width,(x-width/2,y+Op_Cav_Len/2+width/2+length/2-125))
	path3.segment(gridspacingx,'+x',**spec1)
	cavity_pair.add(path3)
	#path connecting all the channels

	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x+gridspacingx,-Op_Cav_Len/2+y+ynew),(Op_Cav_Width/2+x+gridspacingx,Op_Cav_Len/2+y+ynew),**spec1))
	#creates a third cavity
	path4=gdspy.Path(width,(x+gridspacingx,y+Op_Cav_Len/2+length/2-125))
	path4.segment(500,'+y',**spec1)
	cavity_pair.add(path4)
	#creates the path to connect the third cavity to the path connecting them all

	cavity_pair.add(gdspy.Round((x+gridspacingx/2+gridspacingx/2,y+length/2+Pill_Cav_Len/2-125),radius,**spec1))
	#creates the right circle
	cavity_pair.add(gdspy.Round((x,y+length/2+Pill_Cav_Len/2-125),radius,**spec1))
	#creates the left circle

	cavity_pair.add(path1)
	cavity_pair.add(path2)


def make_bars(start_x,start_y,h,w,N):
	coords=[]
	start_y=start_y+Op_Cav_Len/4+550
	for a in range(N):
		coords.append((start_x,start_y-a*2*w))
		coords.append((start_x+h,start_y-a*2*w))
		coords.append((start_x+h,start_y-a*2*w-w))
		coords.append((start_x-h,start_y-a*2*w-w))
		coords.append((start_x-h,start_y-a*2*w-2*w))
		coords.append((start_x,start_y-a*2*w-2*w))
	return coords
#makes the bars on the left

def make_top_bars(start_x,start_y,h,w,N):
	coords=[]
	start_x=start_x+Op_Cav_Len/2
	start_y=start_y+Op_Cav_Width/2
	for a in range(N):
		coords.append((start_x-a*2*w,start_y))
		coords.append((start_x-a*2*w,start_y+h))
		coords.append((start_x-a*2*w-w,start_y+h))
		coords.append((start_x-a*2*w-w,start_y-h))
		coords.append((start_x-a*2*w-2*w,start_y-h))
		coords.append((start_x-a*2*w-2*w,start_y))
	return coords
#makes the bars on top


def SA_cavity(x,y,width,h,w,N,add_half):
	length=1000
	#length between cavities
	if N<=12:
		points=make_bars(x,y,h,w,N)
		#makes left bars
		points+=[(x+0,y-Op_Cav_Len/2),(x+Op_Cav_Width,y-Op_Cav_Len/2)]
		#makes bottom two points
		points2=make_bars(x+Op_Cav_Width,y,h,w,N)
		points2.reverse()
		points+=points2
		#makes right bars
		points+=[(x+Op_Cav_Width,y+Op_Cav_Len/2),(x+0,y+Op_Cav_Len/2)]
		#makes top two points
		if add_half==1:
			points+=make_bars(x,y-N*(2*w),h,w,1)
		#adds bars on left side only
		poly=gdspy.Polygon(points,**spec1)
		#makes outer polygon
		inner=gdspy.Rectangle((-Pill_Cav_Width/2+x+500+Op_Cav_Width/2+h,-Pill_Cav_Len/2+y+500+h),(Pill_Cav_Width/2+x-500+Op_Cav_Width/2-h,Pill_Cav_Len/2+y-500-h),**spec1)
		#subtract this
		together=gdspy.boolean(poly,inner,'not',**spec1)
		#puts them together to create whole optical cavity
		cavity_pair.add(together)


	elif N>12:
		points=make_bars(x,y,h,w,12)
		#makes left bars
		points+=[(x+0,y-Op_Cav_Len/2)]
		#makes bottom left point
		points1=make_top_bars(x,y-Op_Cav_Len,h,w,N-12)
		points1.reverse()
		points+=points1
		#makes bottom bars
		points+=[(x+Op_Cav_Width,y-Op_Cav_Len/2)]
		#makes right bottom point
		points2=make_bars(x+Op_Cav_Width,y,h,w,12)
		points2.reverse()
		points+=points2
		#makes right bars
		points+=[(x+Op_Cav_Width,y+Op_Cav_Len/2)]
		#makes top right point
		points+=make_top_bars(x,y,h,w,N-12)
		#makes top bars
		points+=[(x+0,y+Op_Cav_Len/2)]
		#makes top left point
		if add_half==1:
			points+=make_bars(x,y-N*(2*w),h,w,1)
		#adds bars on left side only
		poly=gdspy.Polygon(points,**spec1)
		#makes outer polygon
		inner=gdspy.Rectangle((-Pill_Cav_Width/2+x+500+Op_Cav_Width/2+h,-Pill_Cav_Len/2+y+500+h),(Pill_Cav_Width/2+x-500+Op_Cav_Width/2-h,Pill_Cav_Len/2+y-500-h),**spec1)
		#subtract this
		together=gdspy.boolean(poly,inner,'not',**spec1)
		#puts them together to create whole optical cavity
		cavity_pair.add(together)

	SA_old=2*Op_Cav_Len+2*Op_Cav_Width+2*(Op_Cav_Width*Op_Cav_Len)
	SA_new=2*Op_Cav_Len+2*Op_Cav_Width+4*2*N*h+2*2*h*add_half+2*(Op_Cav_Width*Op_Cav_Len)
	# print('The surface area ratio is: ' + str(SA_new/SA_old))
	# print('The height to width ratio is( must be <5 ): ' + str(h/w))
	# #gives information about the chosen cavity

	#cavity_pair.add(gdspy.Rectangle((-Pill_Cav_Width/4+x+Pill_Cav_Width/2+100,-Pill_Cav_Len/4+y-length-Op_Cav_Len+Pill_Cav_Width/4),(Pill_Cav_Width/4+x+Pill_Cav_Width/2+100,Pill_Cav_Len/4+y-length-Op_Cav_Len+Pill_Cav_Width/4),**spec1))
	#creates pill cavity
	path1=gdspy.Path(width,(x+Pill_Cav_Width/2+500,y+Pill_Cav_Len/2-length-Op_Cav_Len))
	path1.segment(length,'+y',**spec1)
	cavity_pair.add(path1)
	#creates path between the cavities and puts it on the first layer

def diagonal_cavities(x,y,width,circle):
	length=5000
	#length of the path between cavities
	angle1=np.pi/4
	angle2=np.pi-angle1
	radius=250
	xforcenter=-(gridspacingx/2-length*np.cos(angle1)+length/2*np.cos(angle1)+Pill_Cav_Width/4)+15
	yforcenter=Pill_Cav_Len/4+Pill_Cav_Len/8
	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x-length*np.cos(angle1)+xforcenter,-Op_Cav_Len/4+y+Op_Cav_Len/4-length*np.sin(angle1)-Op_Cav_Len+10+yforcenter),(Op_Cav_Width/4+x+xforcenter-length*np.cos(angle1),Op_Cav_Len/4+y+Op_Cav_Len/4-length*np.sin(angle1)-Op_Cav_Len+10+yforcenter),**spec1))
	#creates pill cavity

	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x,-Op_Cav_Len/2+y),(Op_Cav_Width/2+x,Op_Cav_Len/2+y),**spec1))
	#create right optical cavity
	#cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x-gridspacingx,-Op_Cav_Len/2+y),(Op_Cav_Width/2+x-gridspacingx,Op_Cav_Len/2+y),**spec1))
	#create left optical cavity
	path1=gdspy.Path(width,(x-length*np.cos(angle1)-Op_Cav_Width/2+200+53,y+Op_Cav_Len/2-length*np.sin(angle1)-Op_Cav_Len+5))
	path1.segment(length,angle1,**spec1)
	#creates the right path from the optical cavity to the pill cavity
	cavity_pair.add(path1)

	path2=gdspy.Path(width,(x-Op_Cav_Len-length/2*np.cos(angle2)-gridspacingx/2+Op_Cav_Width/2-200-53,y+Op_Cav_Len/2-length/2*np.sin(angle1)-Op_Cav_Len+5))
	path2.segment(length/2,angle2,**spec1)
	#creates the left path from the optical cavity to the pill cavity
	cavity_pair.add(path2)

	if circle==1:
			cavity_pair.add(gdspy.Round((x-Op_Cav_Len-length/2*np.cos(angle2)-gridspacingx/2+Op_Cav_Width/2-200-53,y+Op_Cav_Len/2-length/2*np.sin(angle1)-Op_Cav_Len+5),radius,**spec1))
	#creates the circle

def original_exp(xcenter,ycenter,xchange,angle):
	height=2000
	pathwidth=10
	path1=gdspy.Path(pathwidth,(xcenter+xchange,ycenter+Op_Cav_Len/2))
	path1.segment(height,'+y',**spec1)
	cavity_pair.add(path1)

def original_exp_rot(xcenter,ycenter,ychange,angle):
	height=2000
	pathwidth=10
	path1=gdspy.Path(pathwidth,(xcenter+Op_Cav_Len/2,ycenter+ychange))
	path1.segment(height,'+x',**spec1)
	cavity_pair.add(path1)

def doughnut(xcenter,ycenter,length, width,rim_width):
	p1=gdspy.Rectangle((xcenter-width/2,ycenter-length/2),(xcenter+width/2,ycenter+length/2),**spec1)
	p2=gdspy.Rectangle((xcenter-width/2+rim_width,ycenter-length/2+rim_width),(xcenter+width/2-rim_width,ycenter+length/2-rim_width),**spec1)
	p3=gdspy.boolean(p1,p2,'not',**spec1)
	cavity_pair.add(p3)

# def pill_cav_final(xcenter,ycenter,length,width,separation,rotation):
# 	a=pill_cav_final(xcenter,ycenter,length,width,separation,rotation)
# 	cavity_pair.add(a)


def op_cav_funnel(xcenter,ycenter,height,pathwidth,rotation):
	width=200
	p1=gdspy.Rectangle((-width/4+xcenter+pathwidth/2+width/4,-height/2+ycenter+height/2),(width/4+xcenter+pathwidth/2+width/4,height/2+ycenter+height/2),**spec1)
	p2=gdspy.Round((xcenter+width/4+pathwidth/2+width/4,ycenter+height/2+height/2),width/2,number_of_points=100,**spec1)
	p3=gdspy.boolean(p1,p2,'not',**spec1)
	#makes the right side swoop
	p4=gdspy.Rectangle((-width/4+xcenter-pathwidth/2-width/4,-height/2+ycenter+height/2),(width/4+xcenter-pathwidth/2-width/4,height/2+ycenter+height/2),**spec1)
	p5=gdspy.Round((xcenter+width/4-pathwidth/2-width/2-width/4,ycenter+height/2+height/2),width/2,number_of_points=100,**spec1)
	p6=gdspy.boolean(p4,p5,'not',**spec1)
	#makes the left side swoop
	p7=gdspy.boolean(p3,p6,'or',**spec1)
	#puts the swoops together
	path1=gdspy.Path(pathwidth,(xcenter,ycenter))
	path1.segment(height,'+y',**spec1)
	p8=gdspy.boolean(p7,path1,'or',**spec1)
	p8.rotate(rotation*np.pi/180,(xcenter,ycenter))
	cavity_pair.add(p8)


def op_cav_funnel_angled(xcenter,ycenter,height,rotation):
	width=200
	p1=gdspy.Round((xcenter,ycenter),width/2,number_of_points=100,**spec1)
	#creates a circle
	p2=gdspy.Rectangle((-width/2+xcenter,-height/2+ycenter-height/2),(width/2+xcenter,height/2+ycenter-height/2),**spec1)
	p3=gdspy.boolean(p1,p2,'not',**spec1)
	#creates a rectangle and uses it to subtract off the bottom half of the circle
	p3.rotate(rotation*np.pi/180,(xcenter,ycenter))
	#allows rotation
	cavity_pair.add(p3)


def op_cav_funnel_angled_corner(xcenter,ycenter,height,rotation):
	width=200
	p1=gdspy.Round((xcenter,ycenter),width/2,number_of_points=100,**spec1)
	#creates a circle
	p1.rotate(rotation*np.pi/180,(xcenter,ycenter))
	#allows rotation
	cavity_pair.add(p1)



channel_bend(gridpositionx,gridpositiony-2*gridspacingy,10,0)
channel_bend(gridpositionx+gridspacingx,gridpositiony-2*gridspacingy,10,np.pi/16)
channel_bend(gridpositionx+2*gridspacingx,gridpositiony-2*gridspacingy,10,np.pi/8)
channel_bend(gridpositionx+3*gridspacingx,gridpositiony-2*gridspacingy,10,3*np.pi/16)
channel_bend(gridpositionx+4*gridspacingx,gridpositiony-2*gridspacingy,10,np.pi/4)
channel_bend(gridpositionx+5*gridspacingx,gridpositiony-2*gridspacingy,10,5*np.pi/16)
channel_bend(gridpositionx+6*gridspacingx,gridpositiony-2*gridspacingy,10,3*np.pi/8)
channel_bend(gridpositionx+7*gridspacingx,gridpositiony-2*gridspacingy,10,7*np.pi/16)
channel_bend(gridpositionx+8*gridspacingx,gridpositiony-2*gridspacingy,10,np.pi/2)

channel_bend_circ(gridpositionx+2*gridspacingx,gridpositiony-3*gridspacingy,10,0,250)
channel_bend_circ(gridpositionx+3*gridspacingx,gridpositiony-3*gridspacingy,10,np.pi/8,250)
channel_bend_circ(gridpositionx+4*gridspacingx,gridpositiony-3*gridspacingy,10,np.pi/4,250)
channel_bend_circ(gridpositionx+5*gridspacingx,gridpositiony-3*gridspacingy,10,3*np.pi/8,250)
channel_bend_circ(gridpositionx+6*gridspacingx,gridpositiony-3*gridspacingy,10,np.pi/2,250)

avoid_bounceback(gridpositionx-gridspacingx,gridpositiony-gridspacingy,10,np.pi/2)
avoid_bounceback(gridpositionx,gridpositiony-gridspacingy,10,np.pi/4)
avoid_bounceback_corner(gridpositionx+gridspacingx,gridpositiony-gridspacingy,10,np.pi/4)
avoid_bounceback_both_corners(gridpositionx+2*gridspacingx,gridpositiony-gridspacingy,10,np.pi/4)

const_len(gridpositionx-gridspacingx,gridpositiony,10)

double_cavity(gridpositionx+3*gridspacingx,gridpositiony-gridspacingy/2,10)
double_circ_cavity(gridpositionx+5*gridspacingx,gridpositiony-gridspacingy/2,10,200)
double_circ_cavity_bottom(gridpositionx+5*gridspacingx,gridpositiony-gridspacingy/2,10,200)
double_circ_cavity_uneven(gridpositionx+3*gridspacingx,gridpositiony-gridspacingy-gridspacingy/2,10,200)

SA_cavity(gridpositionx+gridspacingx-Op_Cav_Width/2,gridpositiony,10,300,100,0,0)
SA_cavity(gridpositionx+2*gridspacingx-Op_Cav_Width/2,gridpositiony,10,300,100,2,1)
SA_cavity(gridpositionx+3*gridspacingx-Op_Cav_Width/2,gridpositiony,10,300,100,5,0)
SA_cavity(gridpositionx+4*gridspacingx-Op_Cav_Width/2,gridpositiony,10,300,100,7,1)
SA_cavity(gridpositionx+5*gridspacingx-Op_Cav_Width/2,gridpositiony,10,300,100,10,0)
SA_cavity(gridpositionx+6*gridspacingx-Op_Cav_Width/2,gridpositiony,10,300,100,12,1)
SA_cavity(gridpositionx+7*gridspacingx-Op_Cav_Width/2,gridpositiony,10,300,100,15,0)

diagonal_cavities(gridpositionx+9*gridspacingx,gridpositiony,10,0)
diagonal_cavities(gridpositionx+11*gridspacingx,gridpositiony,10,1)

original_exp(gridpositionx+9*gridspacingx,gridpositiony-2*gridspacingy,-1200,90)
original_exp_rot(gridpositionx+7*gridspacingx,gridpositiony-3*gridspacingy,0,90)
original_exp(gridpositionx-2*gridspacingx,gridpositiony+gridspacingy,1200,90)
original_exp(gridpositionx-gridspacingx,gridpositiony+5*gridspacingy,-1400,90)
original_exp(gridpositionx+11*gridspacingx,gridpositiony+2*gridspacingy,-1200,90)




doughnut(gridpositionx,gridpositiony,3000,3000,500)
doughnut(gridpositionx-gridspacingx,gridpositiony,3000,3000,500)
doughnut(gridpositionx-2*gridspacingx,gridpositiony,3000,3000,500)
# doughnut(gridpositionx+gridspacingx,gridpositiony,3000,3000,500)
# doughnut(gridpositionx+2*gridspacingx,gridpositiony,3000,3000,500)
# doughnut(gridpositionx+3*gridspacingx,gridpositiony,3000,3000,500)
# doughnut(gridpositionx+4*gridspacingx,gridpositiony,3000,3000,500)
# doughnut(gridpositionx+5*gridspacingx,gridpositiony,3000,3000,500)
# doughnut(gridpositionx+6*gridspacingx,gridpositiony,3000,3000,500)
# doughnut(gridpositionx+7*gridspacingx,gridpositiony,3000,3000,500)
doughnut(gridpositionx+8*gridspacingx,gridpositiony,3000,3000,500)
doughnut(gridpositionx+9*gridspacingx,gridpositiony,3000,3000,500)
doughnut(gridpositionx+10*gridspacingx,gridpositiony,3000,3000,500)
doughnut(gridpositionx+11*gridspacingx,gridpositiony,3000,3000,500)
#top row
doughnut(gridpositionx,gridpositiony-gridspacingy,3000,3000,500)
doughnut(gridpositionx-gridspacingx,gridpositiony-gridspacingy,3000,3000,500)
doughnut(gridpositionx+gridspacingx,gridpositiony-gridspacingy,3000,3000,500)
doughnut(gridpositionx+2*gridspacingx,gridpositiony-gridspacingy,3000,3000,500)
doughnut(gridpositionx+3*gridspacingx,gridpositiony-gridspacingy,3000,3000,500)
doughnut(gridpositionx+4*gridspacingx,gridpositiony-gridspacingy,3000,3000,500)
doughnut(gridpositionx+5*gridspacingx,gridpositiony-gridspacingy,3000,3000,500)
doughnut(gridpositionx+6*gridspacingx,gridpositiony-gridspacingy,3000,3000,500)
doughnut(gridpositionx+7*gridspacingx,gridpositiony-gridspacingy,3000,3000,500)
doughnut(gridpositionx+8*gridspacingx,gridpositiony-gridspacingy,3000,3000,500)
doughnut(gridpositionx+9*gridspacingx,gridpositiony-gridspacingy,3000,3000,500)
doughnut(gridpositionx+10*gridspacingx,gridpositiony-gridspacingy,3000,3000,500)
#second row
doughnut(gridpositionx,gridpositiony-2*gridspacingy,3000,3000,500)
doughnut(gridpositionx+gridspacingx,gridpositiony-2*gridspacingy,3000,3000,500)
doughnut(gridpositionx+2*gridspacingx,gridpositiony-2*gridspacingy,3000,3000,500)
doughnut(gridpositionx+3*gridspacingx,gridpositiony-2*gridspacingy,3000,3000,500)
doughnut(gridpositionx+4*gridspacingx,gridpositiony-2*gridspacingy,3000,3000,500)
doughnut(gridpositionx+5*gridspacingx,gridpositiony-2*gridspacingy,3000,3000,500)
doughnut(gridpositionx+6*gridspacingx,gridpositiony-2*gridspacingy,3000,3000,500)
doughnut(gridpositionx+7*gridspacingx,gridpositiony-2*gridspacingy,3000,3000,500)
#third row
doughnut(gridpositionx+8*gridspacingx,gridpositiony-2*gridspacingy,3000,3000,500)
doughnut(gridpositionx+2*gridspacingx,gridpositiony-3*gridspacingy,3000,3000,500)
doughnut(gridpositionx+3*gridspacingx,gridpositiony-3*gridspacingy,3000,3000,500)
doughnut(gridpositionx+4*gridspacingx,gridpositiony-3*gridspacingy,3000,3000,500)
doughnut(gridpositionx+5*gridspacingx,gridpositiony-3*gridspacingy,3000,3000,500)
doughnut(gridpositionx+6*gridspacingx,gridpositiony-3*gridspacingy,3000,3000,500)
#fourth row
doughnut(gridpositionx+9*gridspacingx,gridpositiony-2*gridspacingy,3000,3000,500)
doughnut(gridpositionx+7*gridspacingx,gridpositiony-3*gridspacingy,3000,3000,500)
doughnut(gridpositionx-2*gridspacingx,gridpositiony+gridspacingy,3000,3000,500)
doughnut(gridpositionx-gridspacingx,gridpositiony+5*gridspacingy,3000,3000,500)
doughnut(gridpositionx+11*gridspacingx,gridpositiony+2*gridspacingy,3000,3000,500)
#original exp doughnuts

pill_cav_final(gridpositionx-2*gridspacingx-2000+5,gridpositiony-Op_Cav_Len/2-1400+Op_Cav_Len+4000,1500,2000,750,-90)
pill_cav_final(gridpositionx-gridspacingx-3000-250+5,gridpositiony-Op_Cav_Len/2-1400,1500,2000,750,0)
pill_cav_final(gridpositionx-Op_Cav_Width/4-1000-200+5,gridpositiony-Op_Cav_Len/2-2400,1500,2000,750,-90)
#const length pill cavities left to right
pill_cav_final(gridpositionx+gridspacingx+600,gridpositiony-Op_Cav_Len/2-1250-Pill_Cav_Len/4,1500,2000,750,90)
pill_cav_final(gridpositionx+2*gridspacingx+800,gridpositiony-Op_Cav_Len/2-1250-Pill_Cav_Len/4,1500,2000,750,90)
pill_cav_final(gridpositionx+3*gridspacingx+800,gridpositiony-Op_Cav_Len/2-1250-Pill_Cav_Len/4,1500,2000,750,90)
pill_cav_final(gridpositionx+4*gridspacingx+800,gridpositiony-Op_Cav_Len/2-1250-Pill_Cav_Len/4,1500,2000,750,90)
pill_cav_final(gridpositionx+5*gridspacingx,gridpositiony-Op_Cav_Len/2-1000-Pill_Cav_Len/4,1500,2000,750,0)
pill_cav_final(gridpositionx+6*gridspacingx+800,gridpositiony-Op_Cav_Len/2-1250-Pill_Cav_Len/4,1500,2000,750,90)
pill_cav_final(gridpositionx+7*gridspacingx+800,gridpositiony-Op_Cav_Len/2-1250-Pill_Cav_Len/4,1500,2000,750,90)
#SA pill cavities left to right
pill_cav_final(gridpositionx-gridspacingx-600,gridpositiony-gridspacingy-2000-Op_Cav_Len/2-Pill_Cav_Len/4,1500,2000,750,0)
pill_cav_final(gridpositionx+2000*np.cos(np.pi/4)+600,gridpositiony-gridspacingy+Op_Cav_Len/2+Pill_Cav_Len/4+2000*np.sin(np.pi/4)-10,1500,2000,750,180)
pill_cav_final(gridpositionx+gridspacingx+Op_Cav_Width/2+2000*np.cos(np.pi/4)-5+600,gridpositiony-gridspacingy+Op_Cav_Len/2+Pill_Cav_Len/4+2000*np.sin(np.pi/4)-10,1500,2000,750,180)
pill_cav_final(gridpositionx+2*gridspacingx+Op_Cav_Width/2+Pill_Cav_Width/4+2000*np.cos(np.pi/4)-10+250,gridpositiony-gridspacingy+Op_Cav_Len/2+Pill_Cav_Len/4+2000*np.sin(np.pi/4)-10,1500,2000,750,180)
#avoid bounceback pill cavities left to right
pill_cav_final(gridpositionx+3*gridspacingx+gridspacingx/2+gridspacingx/4+100,gridpositiony-gridspacingy-1250-Pill_Cav_Len/4-Op_Cav_Len/2,1500,2000,750,90)
pill_cav_final(gridpositionx+5*gridspacingx+gridspacingx/2-100,gridpositiony-gridspacingy+Op_Cav_Len/2+2*500-Pill_Cav_Len/4+250,1500,2000,750,-90)
pill_cav_final(gridpositionx+7*gridspacingx+gridspacingx/2+400,gridpositiony-gridspacingy-1250-Pill_Cav_Len/4-Op_Cav_Len/2,1500,2000,750,90)
pill_cav_final(gridpositionx+9*gridspacingx+gridspacingx/2+400,gridpositiony-gridspacingy-1250-Pill_Cav_Len/4-Op_Cav_Len/2,1500,2000,750,90)
#Multiple Cavities Designs pill cavities
pill_cav_final(gridpositionx+9*gridspacingx-(gridspacingx/2-5000*np.cos(np.pi/4)+5000/2*np.cos(np.pi/4)+Pill_Cav_Width/4)+15-5000*np.cos(np.pi/4),gridpositiony+Pill_Cav_Len/2+Pill_Cav_Len/8-5000*np.sin(np.pi/4)-Op_Cav_Len+10+250,1500,2000,750,-90)
pill_cav_final(gridpositionx+11*gridspacingx-(gridspacingx/2-5000*np.cos(np.pi/4)+5000/2*np.cos(np.pi/4)+Pill_Cav_Width/4)+15-5000*np.cos(np.pi/4),gridpositiony+Pill_Cav_Len/2+Pill_Cav_Len/8-5000*np.sin(np.pi/4)-Op_Cav_Len+10+250,1500,2000,750,-90)
#diagonal cavity pill cavities
pill_cav_final(gridpositionx+9*gridspacingx-1800,gridpositiony-2*gridspacingy+Op_Cav_Len/2+3000,1500,2000,750,-90)
pill_cav_final(gridpositionx+8*gridspacingx-Op_Cav_Width/2-50,gridpositiony-3*gridspacingy,1500,2000,750,180)
pill_cav_final(gridpositionx-2*gridspacingx+1800,gridpositiony+gridspacingy+Op_Cav_Len/2+2000,1500,2000,750,90)
pill_cav_final(gridpositionx-gridspacingx-2100,gridpositiony+5*gridspacingy+Op_Cav_Len/2+3000,1500,2000,750,-90)
pill_cav_final(gridpositionx+11*gridspacingx-1800,gridpositiony+2*gridspacingy+Op_Cav_Len/2+3000,1500,2000,750,-90)
#original cavity pill cavities

op_cav_funnel(gridpositionx-200,gridpositiony-Op_Cav_Len/2,100,10,180)
op_cav_funnel(gridpositionx-gridspacingx+Op_Cav_Width/4,gridpositiony-Op_Cav_Len/2,100,10,180)
op_cav_funnel(gridpositionx-2*gridspacingx+Op_Cav_Width/4,gridpositiony-Op_Cav_Len/2+Op_Cav_Len,100,10,0)
#const len funnels
op_cav_funnel(gridpositionx+gridspacingx+500,gridpositiony-Op_Cav_Len/2,100,10,180)
op_cav_funnel(gridpositionx+2*gridspacingx+500,gridpositiony-Op_Cav_Len/2,100,10,180)
op_cav_funnel(gridpositionx+3*gridspacingx+500,gridpositiony-Op_Cav_Len/2,100,10,180)
op_cav_funnel(gridpositionx+4*gridspacingx+500,gridpositiony-Op_Cav_Len/2,100,10,180)
op_cav_funnel(gridpositionx+5*gridspacingx+500,gridpositiony-Op_Cav_Len/2,100,10,180)
op_cav_funnel(gridpositionx+6*gridspacingx+500,gridpositiony-Op_Cav_Len/2,100,10,180)
op_cav_funnel(gridpositionx+7*gridspacingx+500,gridpositiony-Op_Cav_Len/2,100,10,180)
#SA funnels
op_cav_funnel_angled(gridpositionx+8*gridspacingx+Op_Cav_Width/2-200,gridpositiony-Op_Cav_Len/2,100,180)
op_cav_funnel_angled(gridpositionx+9*gridspacingx-Op_Cav_Width/2+200,gridpositiony-Op_Cav_Len/2,100,180)
op_cav_funnel_angled(gridpositionx+10*gridspacingx+Op_Cav_Width/2-200,gridpositiony-Op_Cav_Len/2,100,180)
op_cav_funnel_angled(gridpositionx+11*gridspacingx-Op_Cav_Width/2+200,gridpositiony-Op_Cav_Len/2,100,180)
#multiple channels funnels
op_cav_funnel_angled(gridpositionx-gridspacingx,gridpositiony-gridspacingy-Op_Cav_Len/2,100,180)
op_cav_funnel_angled(gridpositionx,gridpositiony-gridspacingy+Op_Cav_Len/2,100,0)
op_cav_funnel_angled_corner(gridpositionx+gridspacingx+Op_Cav_Width/2-50,gridpositiony-gridspacingy+Op_Cav_Len/2-50,100,-45)
op_cav_funnel_angled_corner(gridpositionx+2*gridspacingx+Op_Cav_Width/2-50,gridpositiony-gridspacingy+Op_Cav_Len/2-50,100,-45)
#avoid bounceback funnels
op_cav_funnel(gridpositionx+3*gridspacingx,gridpositiony-gridspacingy-Op_Cav_Len/2,100,10,180)
op_cav_funnel(gridpositionx+4*gridspacingx,gridpositiony-gridspacingy-Op_Cav_Len/2,100,10,180)
op_cav_funnel(gridpositionx+5*gridspacingx,gridpositiony-gridspacingy-Op_Cav_Len/2,100,10,180)
op_cav_funnel(gridpositionx+6*gridspacingx,gridpositiony-gridspacingy-Op_Cav_Len/2,100,10,180)
op_cav_funnel(gridpositionx+7*gridspacingx,gridpositiony-gridspacingy-Op_Cav_Len/2,100,10,180)
op_cav_funnel(gridpositionx+8*gridspacingx,gridpositiony-gridspacingy-Op_Cav_Len/2,100,10,180)
op_cav_funnel(gridpositionx+9*gridspacingx,gridpositiony-gridspacingy-Op_Cav_Len/2,100,10,180)
op_cav_funnel(gridpositionx+10*gridspacingx,gridpositiony-gridspacingy-Op_Cav_Len/2,100,10,180)
#multiple channels funnels
op_cav_funnel(gridpositionx,gridpositiony-2*gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx+gridspacingx,gridpositiony-2*gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx+2*gridspacingx,gridpositiony-2*gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx+3*gridspacingx,gridpositiony-2*gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx+4*gridspacingx,gridpositiony-2*gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx+5*gridspacingx,gridpositiony-2*gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx+6*gridspacingx,gridpositiony-2*gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx+7*gridspacingx,gridpositiony-2*gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx+8*gridspacingx,gridpositiony-2*gridspacingy+Op_Cav_Len/2,100,10,0)
#channel bends funnels
op_cav_funnel(gridpositionx+2*gridspacingx,gridpositiony-3*gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx+3*gridspacingx,gridpositiony-3*gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx+4*gridspacingx,gridpositiony-3*gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx+5*gridspacingx,gridpositiony-3*gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx+6*gridspacingx,gridpositiony-3*gridspacingy+Op_Cav_Len/2,100,10,0)
#channel bends circ funnels
op_cav_funnel(gridpositionx+9*gridspacingx-1200,gridpositiony-2*gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx+7*gridspacingx+Op_Cav_Len/2,gridpositiony-3*gridspacingy,100,10,-90)
op_cav_funnel(gridpositionx-2*gridspacingx+1200,gridpositiony+gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx-gridspacingx-1400,gridpositiony+5*gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx+11*gridspacingx-1200,gridpositiony+2*gridspacingy+Op_Cav_Len/2,100,10,0)
#original exp funnel
op_cav_funnel(gridpositionx-gridspacingx,gridpositiony+gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx,gridpositiony+gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx+3*gridspacingx,gridpositiony+gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx+4*gridspacingx,gridpositiony+gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx+5*gridspacingx,gridpositiony+gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx+6*gridspacingx,gridpositiony+gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx+7*gridspacingx,gridpositiony+gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx+8*gridspacingx,gridpositiony+gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx+9*gridspacingx,gridpositiony+gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx+10*gridspacingx,gridpositiony+gridspacingy+Op_Cav_Len/2,100,10,0)
op_cav_funnel(gridpositionx+11*gridspacingx,gridpositiony+gridspacingy+Op_Cav_Len/2,100,10,0)
#Doug's funnels




# ------------------------------------------------------------------ #
#      Write and view file
# ------------------------------------------------------------------ #

gdspy.write_gds('Final_Wafer_Designs.gds',unit=units,precision=1.0e-9)

gdspy.LayoutViewer()