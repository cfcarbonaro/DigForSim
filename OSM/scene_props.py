import bpy
import pickle
from pyproj import Proj, transform



sce = bpy.data.scenes['Scene']

sc_x = sce['crs x']
sc_y = sce['crs y']

print(sc_x, sc_y)





#brb = pickle.load(open("Brandenburgerstr.p", "rb") )

#print(brb.wkt())
#POINT(13.0541953 52.4002587)
lon = 13.0541953
lat = 52.4002587
#obj.location.x + crsx

###  from lon/lat to Meters
inProj = Proj('epsg:4326')
outProj = Proj('epsg:3857')

###  from Meters to lon/lat
#inProj = Proj('epsg:3857')
#outProj = Proj('epsg:4326')

lb = transform(inProj,outProj,lon, lat)  # leftbutton
#rt = transform(inProj,outProj,xmax, ymax)  # righttop

print(lb)
# (5833170.115919803, 1465924.6346602493)
