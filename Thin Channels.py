# ------------------------------------------------------------------ #
#      Introduction
#
#	This script is designed to create an array of vapor cells connected 
#	by various channels to resevoirs which will be probed optically. 
#	gdspy is useful for incrementally varying the dimensions and 
#	directions of the channels which will help tease apart the 
#	dependence of Rb transport in microsystems. The results of this 
#	work will identify the conductance of Rb vapors in microsystems 
#	particularly relevant for low-power, long-lifetime MEMS alkali 
#	sources and for MEMS-based atomic beams
#
# ------------------------------------------------------------------ #

# ------------------------------------------------------------------ #
#      Initialization
# ------------------------------------------------------------------ #
import gdspy
import numpy

spec1={'layer':1,'datatype':1}
spec2={'layer':2,'datatype':2}
units=1.0e-6

Op_Cav_Width=3000
Op_Cav_Len=3000

Pill_Cav_Width=3000
Pill_Cav_Len=3000

Separation=5000

# ------------------------------------------------------------------ #
#      Make Cells
# ------------------------------------------------------------------ #

cavity_pair=gdspy.Cell("POLYGONS")
path_cell=gdspy.Cell('PATHS')

def create_cavity(x,y,width,separation_of_first,width_of_first):
	length=(width_of_first*separation_of_first)/width
	cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x,-Op_Cav_Len/2+y),(Op_Cav_Width/2+x,Op_Cav_Len/2+y),**spec1))
	ynew=length+Pill_Cav_Len/2+Op_Cav_Len/2
	cavity_pair.add(gdspy.Rectangle((-Op_Cav_Width/2+x,-Op_Cav_Len/2+y+ynew),(Op_Cav_Width/2+x,Op_Cav_Len/2+y+ynew),**spec1))
	path1=gdspy.Path(width,(x,y+Op_Cav_Len/2))
	path1.segment(length,'+y',**spec1)
	cavity_pair.add(path1)
	#serpentine_connector(x,y,width,length,10)

def serpentine_connector(x,y,width,length,num_turns,spec):
	# min_bend_dist=width*4
	separation=length/(num_turns-1)
	path2=gdspy.Path(width,(x,y+Op_Cav_Len/2))
	path2.segment(separation,'+y',**spec)
	for n in range((num_turns-1)//2):
		print("in use")
		path2.segment(separation,'+x',**spec)
		path2.segment(separation/5,'+y',**spec)
		path2.segment(separation,'-x',**spec)
		path2.segment(separation/5,'+y',**spec)
	path2.segment(separation,'+y',**spec)
	print(path2.area())
	cavity_pair.add(path2)

displacement=10000

create_cavity(0+displacement,0,100,1000,100)
create_cavity(5000+displacement,0,50,1000,100)
create_cavity(10000+displacement,0,25,1000,100)
create_cavity(15000+displacement,0,10,1000,100)

#for x in range(20):
#	create_cavity(x*5000,0,300/(1+x**2),500,300)

serpentine_connector(0,0,50,5000,2,spec1)
serpentine_connector(1000,0,50,5000,4,spec1)
serpentine_connector(3000,0,50,5000,6,spec1)
serpentine_connector(5000,0,50,5000,8,spec1)
serpentine_connector(7000,0,50,5000,10,spec1)

# ------------------------------------------------------------------ #
#      Write and view file
# ------------------------------------------------------------------ #

gdspy.write_gds('Thin_Channel_Array.gds',unit=units,precision=1.0e-9)

gdspy.LayoutViewer()
