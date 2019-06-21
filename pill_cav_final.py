import gdspy
import numpy as np

units=1.0e-6
pill_size=0.6e3

def pill_cav(xcenter,ycenter,length,width,separation,rotation):
	coords=[(pill_size,0),(width,0),(width,length),(0,length),(width-separation,1e3),(width-separation,separation),(0.5*1e3,separation),(pill_size,0.5e3)]
	coords=np.asarray(coords)
	for a,element in enumerate(coords):
		coords[a][0]+=xcenter-width/2
		coords[a][1]+=ycenter-length/2
	p1=gdspy.Polygon(coords)
	p2=gdspy.Round((xcenter-0.5*1e3,ycenter-0.4*1e3),pill_size,number_of_points=100)
	p3=gdspy.boolean(p1,p2,'or',layer=1,datatype=1)
	p3.rotate(rotation*np.pi/180,(xcenter,ycenter))
	return p3

# cell1=gdspy.Cell('First')
# cell1.add(pill_cav(0,0,1.5e3,2e3,500,0))

# gdspy.write_gds('pill_cav2.gds',unit=units,precision=1.0e-6)

# gdspy.LayoutViewer()