import gdspy
import numpy as np

units=1.0e-6
pill_size=600
spec1={'layer':1,'datatype':1}

def pill_cav_final(xcenter,ycenter,length,width,separation,rotation):
	coords=[(pill_size,0),(width,0),(width,length),(0,length),(width-500,1e3),(width-500,500),(0.5*1e3,500),(pill_size,0.5e3)]
	coords=np.asarray(coords)
	for a,element in enumerate(coords):
		coords[a][0]+=xcenter-width/2
		coords[a][1]+=ycenter-length/2
	p1=gdspy.Polygon(coords)
	p2=gdspy.Round((xcenter-0.5*1e3,ycenter-0.4*1e3),pill_size,number_of_points=100)
	p3=gdspy.boolean(p1,p2,'or',**spec1)
	p4=gdspy.Rectangle((-width/2+xcenter,ycenter+200),(width/4+xcenter,length/2+ycenter),**spec1)
	p5=gdspy.boolean(p3,p4,'not',**spec1)
	p5.rotate(rotation*np.pi/180,(xcenter,ycenter))
	return p5

cell1=gdspy.Cell('First')
cell1.add(pill_cav_final(0,0,1500,2000,750,0))

gdspy.write_gds('pill_cav_final2.gds',unit=units,precision=1.0e-9)

gdspy.LayoutViewer()