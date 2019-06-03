#KL Mask design

import numpy as np
import gdspy

spec1={'layer':1,'datatype':1}
spec2={'layer':2,'datatype':2}
units=1.0e-6

oc_w=3000
oc_l=3000

pc_w=3000
pc_l=3000


# ------------------------------------------------------------------ #
#      Functions
# ------------------------------------------------------------------ #

cavity_pair= gdspy.Cell("POLYGONS")
path_cell=gdspy.Cell('PATHS')


def cavity_pipe(x,y,width,separation_1,width_1):
	length=separation_1*width_1/width
	cavity_pair.add(gdspy.Rectangle((-pc_w/2+x,-pc_l/2+y),(pc_w/2+x,pc_l/2+y),**spec1))
	ynew=length+pc_l/2+oc_l/2
	cavity_pair.add(gdspy.Rectangle((-oc_w/2+x,-oc_l/2+y+ynew),(oc_w/2+x,oc_l/2+y+ynew),**spec1))
	path1=gdspy.Path(width,(x,y+oc_l/2))
	path1.segment(length,'+y',**spec1)
	cavity_pair.add(path1)

def cavity_serpentine(x,y,width,path_length,turns,spec1):
	cavity_pair.add(gdspy.Rectangle((-pc_w/2+x,-pc_l/2+y),(pc_w/2+x,pc_l/2+y),**spec1))
	segment_length=path_length/(2*turns+2)
	path2=gdspy.Path(width,(x,y+oc_l/2))
	path2.segment(segment_length,'+y',**spec1)
	for n in range(turns):
			path2.segment(segment_length,'+x',**spec1)
			path2.segment(width*2,'+y',**spec1)
			path2.segment(segment_length,'-x',**spec1)
			path2.segment(width*2,'+y',**spec1)
	path2.segment(segment_length-width,'+y',**spec1)		
	cavity_pair.add(path2)
	y_2=2*segment_length+(4*turns-1)*width
	cavity_pair.add(gdspy.Rectangle((-oc_w/2+x,-pc_l/2+y+pc_l+y_2),(oc_w/2+x,pc_l/2+oc_l+y+y_2),**spec1))

def parallel_channel(x,y,path_len,branches,spec1)
	cavity_pair.add(gdspy.Rectangle((-pc_w/2+x,-pc_l/2+y),(pc_w/2+x,pc_l/2+y),**spec1))
	segment_length=path_len/(branches+1)
	
# ------------------------------------------------------------------ #
#		Generating cells
# ------------------------------------------------------------------ #


cavity_pipe(0,0,100,1000,100)
cavity_pipe(5000,0,50,1000,100)
cavity_pipe(10000,0,25,1000,100)
cavity_pipe(15000,0,10,1000,100)

displacement=5000

cavity_serpentine(0,-12000,50,10000,2,spec1)
cavity_serpentine(displacement,-12000,50,10000,4,spec1)
cavity_serpentine(2*displacement,-12000,50,10000,6,spec1)
cavity_serpentine(3*displacement,-12000,50,10000,8,spec1)

# ------------------------------------------------------------------ #
#      Write and view file
# ------------------------------------------------------------------ #

# gdspy.write_gds('Mask_draft.gds',unit=units,precision=1.0e-9)

gdspy.LayoutViewer()
