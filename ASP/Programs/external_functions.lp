#script (python)

import clingo

from math import sqrt, floor, ceil
import random as rd
from OSMPythonTools.api import Api
from OSMPythonTools.nominatim import Nominatim
import math

N = clingo.Number
S = clingo.String

api = Api()
nomina = Nominatim()




def div(a, b):
    return N(a.number // b.number)

    	
def dist(x, y):
    xn = x.number
    yn = y.number
    d = sqrt(xn**2 + yn**2)
    #d_int = floor(d)
    d_int = ceil(d)    # ceil function: if 0 -> really Zero! ( but still unknown path possible )
    return N(d_int)


def nominatim(loc):
    osm_data = nomina.query(loc)
    print(osm_data.id())
    osm_id_s = str(osm_data.id())

    return S(osm_id_s)

def dist2(x, y):
    xn = x.number
    yn = y.number
    d = sqrt(xn**2 + yn**2)
    d_int = round(d)

    return N(d_int)
    
    


class Ellps():
    """ellipsoid"""
    def __init__(self, a, b):
        self.a =  a #equatorial radius in meters
        self.b =  b #polar radius in meters
        self.f = (self.a-self.b)/self.a     #inverse flat
        self.perimeter = (2*math.pi*self.a) #perimeter at equator

GRS80 = Ellps(6378137, 6356752.314245)

def webMercToLonLat(x, y):
    k = GRS80.perimeter/360
    lon = x / k
    lat = y / k
    lat = 180 / math.pi * (2 * math.atan( math.exp( lat * math.pi / 180.0)) - math.pi / 2.0)
    return lon, lat

def lonLatToWebMerc(lon, lat):
    k = GRS80.perimeter/360
    x = lon * k
    lat = math.log( math.tan((90 + lat) * math.pi / 360.0 )) / (math.pi / 180.0)
    y = lat * k
    return x, y    
    

#end.


%%%  Manhattan distance:
dist_manh( |X-X'|, |Y-Y'|, loc(X,Y), loc(X',Y') ) :- loc(X,Y), loc(X',Y'), loc(X,Y)<loc(X',Y').

%%%  Manhattan distance;  only when required ( via check_dist() ):
%dist_manh( |X-X'|, |Y-Y'|, loc(X,Y), loc(X',Y') ) :- check_dist(loc(X,Y),loc(X',Y')).

%%%  Euclidian distance:
%%%  dist2 or dist depending on floor() or ceil() or round() is required.
dist_eukl( @dist2(Xm,Ym), loc(X,Y), loc(X',Y') )   :- dist_manh( Xm,Ym, loc(X,Y), loc(X',Y')).    %% 












