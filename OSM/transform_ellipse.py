import math

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
