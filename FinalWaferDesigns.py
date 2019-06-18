# This code contains all of to designs I've created on a single wafer

import gdspy
import numpy as np

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

# ------------------------------------------------------------------ #
#      Make Cells
# ------------------------------------------------------------------ #

cavity_pair= gdspy.Cell("POLYGONS")
path_cell=gdspy.Cell('PATHS')

def channel_bend(x,y,width,angle):
	length=2000
	#path length between cavities
	cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x,-Op_Cav_Len/2+y),(Op_Cav_Width/2+x,Op_Cav_Len/2+y),**spec1))
	#creates pill cavity
	if angle>=np.pi/4:
		xnew=(length/2)*np.cos(angle)
		ynew=length/2+Pill_Cav_Len+(length/2)*np.sin(angle)
		cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+xnew,-Op_Cav_Len/2+y+ynew),(Op_Cav_Width/4+x+xnew,y+ynew),**spec1))
	else:
		xnew=(length/2)*np.cos(angle)+Op_Cav_Width/4
		ynew=length/2+Pill_Cav_Len/2+(length/2)*np.sin(angle)+500
		cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+xnew,-Op_Cav_Len/4+y+ynew),(Op_Cav_Width/4+x+xnew,Op_Cav_Len/4+y+ynew),**spec1))
	#defines position and creates second cavity
	path1=gdspy.Path(width,(x,y+Op_Cav_Len/2))
	path1.segment(length/2,'+y',**spec1)
	#creates the path from the pill cavity to the bend
	path2=gdspy.Path(width,(x,y+Op_Cav_Len/2+length/2))
	path2.segment(length/2,angle,**spec1)
	#creates the path from the second cavity to the bend

	cavity_pair.add(path1)
	cavity_pair.add(path2)


def avoid_bounceback(x,y,width,angle):
	length=2000
	#length of the path between cavities
	cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x,-Op_Cav_Len/2+y),(Op_Cav_Width/2+x,Op_Cav_Len/2+y),**spec1))
	#creates pill cavity
	if angle>=np.pi/4:
		xnew=length*np.cos(angle)
		ynew=Pill_Cav_Len+length*np.sin(angle)
		cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+xnew,-Op_Cav_Len/2+y+ynew),(Op_Cav_Width/4+x+xnew,Op_Cav_Len/4+y+ynew-Op_Cav_Len/4),**spec1))
	else:
		xnew=length*np.cos(angle)+Op_Cav_Width/4
		ynew=Pill_Cav_Len+length*np.sin(angle)-Op_Cav_Len/2+500
		cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+xnew,-Op_Cav_Len/4+y+ynew),(Op_Cav_Width/4+x+xnew,Op_Cav_Len/4+y+ynew),**spec1))
	#defines position and creates second cavity
	path1=gdspy.Path(width,(x,y+Op_Cav_Len/2))
	path1.segment(length,angle,**spec1)
	#creates the path from the second cavity to the pill cavity

	cavity_pair.add(path1)


def avoid_bounceback_corner(x,y,width,angle):
	length=2000
	#length of path between cavities
	cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x,-Op_Cav_Len/2+y),(Op_Cav_Width/2+x,Op_Cav_Len/2+y),**spec1))
	#creates pill cavity
	if angle>=np.pi/4:
		xnew=length*np.cos(angle)+Op_Cav_Width/2
		ynew=Pill_Cav_Len+length*np.sin(angle)
		cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+xnew,-Op_Cav_Len/2+y+ynew),(Op_Cav_Width/4+x+xnew,y+ynew),**spec1))
	else:
		xnew=length*np.cos(angle)+Op_Cav_Width/4+Op_Cav_Width/2
		ynew=Pill_Cav_Len+length*np.sin(angle)-Op_Cav_Len/2+500
		cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+xnew,-Op_Cav_Len/4+y+ynew),(Op_Cav_Width/4+x+xnew,Op_Cav_Len/4+y+ynew),**spec1))
	#defines position and creates second cavity
	path1=gdspy.Path(width,(x+Op_Cav_Width/2,y+Op_Cav_Len/2))
	path1.segment(length,angle,**spec1)
	#creates the path from the second cavity to the pill cavity

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
	
	cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x,-Op_Cav_Len/2+y),(Op_Cav_Width/2+x,Op_Cav_Len/2+y),**spec1))
	#creates optical cavity for the right top
	path1=gdspy.Path(width,(x+Op_Cav_Width/4,y-length_pre_bend1-Op_Cav_Len/2))
	path1.segment(length_pre_bend1,'+y',**spec1)
	cavity_pair.add(path1)
	#creates a path along the y axis for the right top
	cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x-length_post_bend1-Pill_Cav_Width/4+Op_Cav_Width/4,-Op_Cav_Len/4+y-length_pre_bend1-Op_Cav_Len/2),(Op_Cav_Width/4+x-length_post_bend1-Pill_Cav_Width/4+Op_Cav_Width/4,Op_Cav_Len/4+y-length_pre_bend1-Op_Cav_Len/2),**spec1))
	path2=gdspy.Path(width,(x-length_post_bend1+Op_Cav_Width/4,y-length_pre_bend1-Op_Cav_Len/2))
	path2.segment(length_post_bend1,'+x',**spec1)
	cavity_pair.add(path2)
	#creates the pill cavity and the x axis path for the right top

	cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x-gridspacingx,-Op_Cav_Len/2+y),(Op_Cav_Width/2+x-gridspacingx,Op_Cav_Len/2+y),**spec1))
	#creates optical cavity for the left top
	path3=gdspy.Path(width,(x-gridspacingx+Op_Cav_Width/4,y-length_pre_bend2-Op_Cav_Len/2))
	path3.segment(length_pre_bend2,'+y',**spec1)
	cavity_pair.add(path3)
	#creates a path along the y axis for the left top
	cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x-length_post_bend2-gridspacingx-Pill_Cav_Width/4+Op_Cav_Width/4,-Op_Cav_Len/4+y-length_pre_bend2-Op_Cav_Len/2),(Op_Cav_Width/4+x-length_post_bend2-gridspacingx-Pill_Cav_Width/4+Op_Cav_Width/4,Op_Cav_Len/4+y-length_pre_bend2-Op_Cav_Len/2),**spec1))
	path4=gdspy.Path(width,(x-length_post_bend2-gridspacingx+Op_Cav_Width/4,y-length_pre_bend2-Op_Cav_Len/2))
	path4.segment(length_post_bend2,'+x',**spec1)
	cavity_pair.add(path4)
	#creates the pill cavity and the x axis path for the left top

	cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x,-Op_Cav_Len/2+y-gridspacingy),(Op_Cav_Width/2+x,Op_Cav_Len/2+y-gridspacingy),**spec1))
	#creates optical cavity for the bottom
	path5=gdspy.Path(width,(x,y-length_pre_bend3-gridspacingy-Op_Cav_Len/2))
	path5.segment(length_pre_bend3,'+y',**spec1)
	cavity_pair.add(path5)
	#creates a path along the y axis for the bottom
	cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x-length_post_bend3-Pill_Cav_Width/4,-Op_Cav_Len/4+y-length_pre_bend3-gridspacingy-Op_Cav_Len/2),(Op_Cav_Width/4+x-length_post_bend3-Pill_Cav_Width/4,Op_Cav_Len/4+y-length_pre_bend3-gridspacingy-Op_Cav_Len/2),**spec1))
	path6=gdspy.Path(width,(x-length_post_bend3,y-length_pre_bend3-gridspacingy-Op_Cav_Len/2))
	path6.segment(length_post_bend3,'+x',**spec1)
	cavity_pair.add(path6)
	#creates the pill cavity and the x axis path for the bottom
	

def channel_bend_circ(x,y,width,angle,radius):
	length=2000
	#length of the channel between cavities
	cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x,-Op_Cav_Len/2+y),(Op_Cav_Width/2+x,Op_Cav_Len/2+y),**spec1))
	#creates pill cavity
	if angle>=np.pi/4:
		xnew=(length/2)*np.cos(angle)
		ynew=length/2+Pill_Cav_Len+(length/2)*np.sin(angle)
		cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+xnew,-Op_Cav_Len/2+y+ynew),(Op_Cav_Width/4+x+xnew,Op_Cav_Len/4+y+ynew-Op_Cav_Len/4),**spec1))
	else:
		xnew=(length/2)*np.cos(angle)+Op_Cav_Width/4
		ynew=length/2+Pill_Cav_Len/2+(length/2)*np.sin(angle)+500
		cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+xnew,-Op_Cav_Len/4+y+ynew),(Op_Cav_Width/4+x+xnew,Op_Cav_Len/4+y+ynew),**spec1))
	#defines position and creates second cavity
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


def double_cavity(x,y,width):
	length=gridspacingy/2-Op_Cav_Width
	x+=4*gridspacingx
	y-=gridspacingy
	cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+gridspacingx/2,-Op_Cav_Len/4+y-250+Pill_Cav_Width/4),(Op_Cav_Width/4+x+gridspacingx/2,Op_Cav_Len/4+y-250+Pill_Cav_Width/4),**spec1))
	#creates pill cavity
	ynew=length+Op_Cav_Len
	cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x,-Op_Cav_Len/2+y+ynew),(Op_Cav_Width/2+x,Op_Cav_Len/2+y+ynew),**spec1))
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

	cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x+gridspacingx,-Op_Cav_Len/2+y+ynew),(Op_Cav_Width/2+x+gridspacingx,Op_Cav_Len/2+y+ynew),**spec1))
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
	cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+gridspacingx/2,-Op_Cav_Len/4+y-250+Pill_Cav_Len/4),(Op_Cav_Width/4+x+gridspacingx/2,Op_Cav_Len/4+y-250+Pill_Cav_Len/4),**spec1))
	#creates pill cavity
	ynew=length+Op_Cav_Len
	cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x,-Op_Cav_Len/2+y+ynew),(Op_Cav_Width/2+x,Op_Cav_Len/2+y+ynew),**spec1))
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

	cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x+gridspacingx,-Op_Cav_Len/2+y+ynew),(Op_Cav_Width/2+x+gridspacingx,Op_Cav_Len/2+y+ynew),**spec1))
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

	cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+gridspacingx/2,-Op_Cav_Len/4+y-250-Pill_Cav_Len/4-2*500),(Op_Cav_Width/4+x+gridspacingx/2,Op_Cav_Len/4+y-250-Pill_Cav_Len/4-2*500),**spec1))
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

	cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x,-Op_Cav_Len/2+y+ynew-gridspacingy),(Op_Cav_Width/2+x,Op_Cav_Len/2+y+ynew-gridspacingy),**spec1))
	#defines position and creates a bottom cavity

	cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x+gridspacingx,-Op_Cav_Len/2+y+ynew-gridspacingy),(Op_Cav_Width/2+x+gridspacingx,Op_Cav_Len/2+y+ynew-gridspacingy),**spec1))
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
	cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/4+x+gridspacingx/2+gridspacingx/4,y-250),(Op_Cav_Width/4+x+gridspacingx/2+gridspacingx/4,Op_Cav_Len/2+y-250),**spec1))
	#creates pill cavity
	ynew=length+Op_Cav_Len
	cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x,-Op_Cav_Len/2+y+ynew),(Op_Cav_Width/2+x,Op_Cav_Len/2+y+ynew),**spec1))
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

	cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x+gridspacingx,-Op_Cav_Len/2+y+ynew),(Op_Cav_Width/2+x+gridspacingx,Op_Cav_Len/2+y+ynew),**spec1))
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
		cavity_pair.add(poly)

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
		cavity_pair.add(poly)

	SA_old=2*Op_Cav_Len+2*Op_Cav_Width
	SA_new=2*Op_Cav_Len+2*Op_Cav_Width+4*2*N*h+2*2*h*add_half
	# print('The surface area ratio is: ' + str(SA_new/SA_old))
	# print('The height to width ratio is( must be <5 ): ' + str(h/w))
	# #gives information about the chosen cavity

	cavity_pair.add(gdspy.Rectangle((-Pill_Cav_Width/2+x+Pill_Cav_Width/2,-Pill_Cav_Len/2+y-length-Op_Cav_Len),(Pill_Cav_Width/2+x+Pill_Cav_Width/2,Pill_Cav_Len/2+y-length-Op_Cav_Len),**spec1))
	#creates pill cavity
	path1=gdspy.Path(width,(x+Pill_Cav_Width/2+500,y+Pill_Cav_Len/2-length-Op_Cav_Len))
	path1.segment(length,'+y',**spec1)
	cavity_pair.add(path1)
	#creates path between the cavities and puts it on the first layer


channel_bend(gridpositionx,gridpositiony-2*gridspacingy,10,0)
channel_bend(gridpositionx+gridspacingx,gridpositiony-2*gridspacingy,10,np.pi/16)
channel_bend(gridpositionx+2*gridspacingx,gridpositiony-2*gridspacingy,10,np.pi/8)
channel_bend(gridpositionx+3*gridspacingx,gridpositiony-2*gridspacingy,10,3*np.pi/16)
channel_bend(gridpositionx+4*gridspacingx,gridpositiony-2*gridspacingy,10,np.pi/4)
channel_bend(gridpositionx+5*gridspacingx,gridpositiony-2*gridspacingy,10,5*np.pi/16)
channel_bend(gridpositionx+6*gridspacingx,gridpositiony-2*gridspacingy,10,3*np.pi/8)
channel_bend(gridpositionx+7*gridspacingx,gridpositiony-2*gridspacingy,10,7*np.pi/16)
channel_bend(gridpositionx+8*gridspacingx,gridpositiony-2*gridspacingy,10,np.pi/2)


avoid_bounceback(gridpositionx-2*gridspacingx,gridpositiony+gridspacingy,10,np.pi/2)
avoid_bounceback(gridpositionx-gridspacingx,gridpositiony+gridspacingy,10,np.pi/4)
avoid_bounceback_corner(gridpositionx-gridspacingx,gridpositiony-gridspacingy,10,np.pi/4)

const_len(gridpositionx-gridspacingx,gridpositiony,10)

channel_bend_circ(gridpositionx+2*gridspacingx,gridpositiony-3*gridspacingy,10,0,250)
channel_bend_circ(gridpositionx+3*gridspacingx,gridpositiony-3*gridspacingy,10,np.pi/8,250)
channel_bend_circ(gridpositionx+4*gridspacingx,gridpositiony-3*gridspacingy,10,np.pi/4,250)
channel_bend_circ(gridpositionx+5*gridspacingx,gridpositiony-3*gridspacingy,10,3*np.pi/8,250)
channel_bend_circ(gridpositionx+7*gridspacingx,gridpositiony-3*gridspacingy,10,np.pi/2,250)

double_cavity(gridpositionx+2*gridspacingx,gridpositiony-gridspacingy/2,10)
double_circ_cavity(gridpositionx+4*gridspacingx,gridpositiony-gridspacingy/2,10,200)
double_circ_cavity_bottom(gridpositionx+4*gridspacingx,gridpositiony-gridspacingy/2,10,200)
double_circ_cavity_uneven(gridpositionx+2*gridspacingx,gridpositiony-gridspacingy-gridspacingy/2,10,200)

SA_cavity(gridpositionx-Op_Cav_Width/2,gridpositiony,10,300,100,0,0)
SA_cavity(gridpositionx+gridspacingx-Op_Cav_Width/2,gridpositiony,10,300,100,2,1)
SA_cavity(gridpositionx+2*gridspacingx-Op_Cav_Width/2,gridpositiony,10,300,100,5,0)
SA_cavity(gridpositionx+3*gridspacingx-Op_Cav_Width/2,gridpositiony,10,300,100,7,1)
SA_cavity(gridpositionx+4*gridspacingx-Op_Cav_Width/2,gridpositiony,10,300,100,10,0)
SA_cavity(gridpositionx+5*gridspacingx-Op_Cav_Width/2,gridpositiony,10,300,100,12,1)
SA_cavity(gridpositionx+6*gridspacingx-Op_Cav_Width/2,gridpositiony,10,300,100,15,0)

# ------------------------------------------------------------------ #
#      Write and view file
# ------------------------------------------------------------------ #

gdspy.write_gds('Final_Wafer_Designs.gds',unit=units,precision=1.0e-9)

gdspy.LayoutViewer()