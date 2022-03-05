import json
import math
import bpy
import numpy as np
import os
import time
import datetime

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       IntVectorProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )




# ------------------------------------------------------------------------
#    Create new Agent : Properties
# ------------------------------------------------------------------------

class PropsCoordsDurations(PropertyGroup):

    fps: IntProperty(
        name="FPS",
        description="Frames per second",
        default = 1
        )

    route_json: StringProperty(
        name = "JSON file",
        description="Choose a route JSON file:",
        default="",
        maxlen=1024,
        subtype='FILE_PATH'
        )

# stole the ellps class and proj-functions from domlyz github


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



def flatten(t):
    return [item for sublist in t for item in sublist]



def routeFromJson(json_file, output=False):

    # overwrite existing csv file and set Lon, Lat header
    ##with open('./general_info.csv', "w") as f:   
    ##    f.write('Lon,Lat,Dur\n')
        
    print("Read ORSM json file.")        
    ##with open('./{}'.format(json_file)) as f:
    with open(json_file) as f:
        j = json.load(f)

        
    #  take just the first route  ( maybe someday also alternatives )
    ##route = j["routes"][0]
    route = j["routes"][1]

    legs = route["legs"]
    
    for leg in legs:
    
        durations = leg['annotation']['duration']
        
        if output == True:
            print(20*"--")
            print("Leg ")
            print("distance: ", leg["distance"])
            print("duration: ", leg["duration"])
        
        coords = []
        for step in leg['steps']:
            #print(step['geometry']['coordinates'][0:-1])
            coords.append(step['geometry']['coordinates'][0:-1])  # last coord is doubled (=first in the next step)

        sc = bpy.data.scenes['Scene']
        crsx = sc['crs x']   #crsx = 995057.1280538852
        crsy = sc['crs y']   #crsy = 5529688.030683989 
               
        coords_flat = flatten(coords)  
        
        merc = [ lonLatToWebMerc(p[0], p[1]) for p in coords_flat ]   # convert coords to web-mercator

        merc_ori = [ (p[0]-crsx, p[1]-crsy) for p in merc ]   # transform to scene-origin
        
        return merc_ori, durations



def makeRoute(coords2d):
    
    coords3d = [ (x,y,0) for (x,y) in coords2d ]
    e = []
    for i in range(len(coords3d)-1):  # -1 to avoid edge to center
        e.append(( i, i+1 ))
        
    # make mesh
    vertices = coords3d
    edges = e
    faces = []
    
    route = bpy.data.meshes.new('Route')
    route.from_pydata(vertices, edges, faces)
    route.update()
    
    # make object from mesh
    route_ob = bpy.data.objects.new('Route', route)
    
    # make collection
    #if coll in bpy.data.collections:    
    timed_routes = bpy.data.collections.new('Timed_Routes')
    bpy.context.scene.collection.children.link(timed_routes)
    
    # add object to scene collection
    timed_routes.objects.link(route_ob)
    
    return route_ob



class WM_OT_RouteFromJson(Operator):
    """Read route from JSON and create."""
    bl_label = "Create."
    bl_idname = "wm.route_from_json"
    
    def execute(self, context):
        layout = self.layout
        scene = context.scene
        p = scene.props_coords_durations 
        
        json_file_abs = bpy.path.abspath(p.route_json)  # need absolute path rather than blender relative path 
        #json_file = json_file_abs  ## "/home/j/UPBGE-0.30-linux-x86_64/o_gen_3.json"  # "asp_route.json"  
        json_file = "/home/j/UPBGE-0.30-linux-x86_64/o_gen_3.json"                  
        merc_ori, durs = routeFromJson(json_file)
        print("json-fie debug:", json_file) 
        print("json-fie, p. debug:", p.route_json)             
        print("Read route from JSON.")
        
        route_ob = makeRoute(merc_ori)    # input: 2d coords (web-mercator, centered); output: blender-mesh-object (the route, added z-coords, all zero yet)
        
        print("Create route as mesh and add z-coords (all zero).")
        
        bpy.context.view_layer.objects.active = route_ob  # set route as active object
        
        
               
        return {'FINISHED'}



def shrinkWrap(obj):
    
    modifier = obj.modifiers.new(name="Shrinkwrap", type='SHRINKWRAP')
    modifier.wrap_method = "PROJECT"
    modifier.wrap_mode = 'ABOVE_SURFACE'

    modifier.use_project_z = True
    modifier.target = bpy.data.objects["EXPORT_OSM_MAPNIK_WM"]
    modifier.offset = 1.00
    
    #modifier.apply


class WM_OT_ElevateRoute(Operator):
    """Add z-values to route. (Relative to Map-elevation.)"""
    bl_label = "Elevate route."
    bl_idname = "wm.elevate_route"
    
    def execute(self, context):
    
        layout = self.layout
        scene = context.scene
        p = scene.props_coords_durations 
                     
        print("Add z-values to route. (Relative to Map-elevation.)")
        obj = bpy.context.object
        print("Current object: ", obj.name)        
        shrinkWrap(obj)
        print("Apply manually, please.")
               
        return {'FINISHED'}


def setKeyframesOnRoute(agent, coords3d, durs):  # agent has e.g. "car" with him ( in future)
    
    #coords3d = [ (x,y,0) for (x,y) in coords2d ]
    durs = [0] + durs            # put a zero at beginning of durations
    durs_cum = np.cumsum(durs)   # yields cumulated time at every route-point ( according to ORSM time )
    
    fps = 1   # instead of 24 etc. 
           
    for i, loc in enumerate(coords3d):
        
        agent.location = loc 
        frame = durs_cum[i] * fps   # can also be float!
        agent.keyframe_insert(data_path="location", frame=frame)
   

class WM_OT_SetKeyframes(Operator):
    """Set keyframes to agent (e.g. car) on route."""
    bl_label = "Set keyframes."
    bl_idname = "wm.set_keyframes"
    
    def execute(self, context):
    
        layout = self.layout
        scene = context.scene
        p = scene.props_coords_durations 
                     
        print("Set keyframes to agent (e.g. car) on route.")
        obj = bpy.context.object
        print("Current object: ", obj.name)        
        setKeyframesOnRoute(agent, coords3d, durs)
        print("Apply manually, please.")
               
        return {'FINISHED'}

#--------------------------------------------------------------------------------------------------------
#    PANELS
#--------------------------------------------------------------------------------------------------------
#    MAIN : Get coordinates from ORMS route and corresponding durations
#-------------------------------------------------------------------------------------------------------- 

class ROUTE_panel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Routes / OSM"    
    bl_options = {"DEFAULT_CLOSED"}

# Main Panel 1
class ROUTE_PT_panel_1(ROUTE_panel, bpy.types.Panel):
    bl_idname = "ROUTE_PT_panel_1"
    bl_label = "Routing"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        p = scene.props_coords_durations 
        rp = scene.route_props
        
        layout.prop(p, "fps")
        layout.label(text=str(p.fps))        
        layout.separator()
        
        layout.prop(rp, "start_obj")
        layout.prop(rp, "end_obj")
        layout.label(text="Route from {}".format(rp.start_obj) )
        layout.label(text="to {}".format(rp.end_obj) )
        
        layout.label(text="Only car-mode possible: https://github.com/Project-OSRM/osrm-backend/issues/4868")
        layout.prop(rp, "move_mode")
               
        layout.operator("object.get_route")
        layout.prop(p, "route_json")   # select route JSON file ( if not already given implicitly )
        layout.operator("wm.route_from_json")
        layout.operator("wm.elevate_route")
        
        

#--# coords, durs = getCoordsFromJson("o_gen_2.json")   #todo: give better name to file 

#--# car = bpy.data.scenes['Scene'].objects['Car']


# after shrinkwrapping fetch the created z-coordinates:
#--# coords3d = [ v.co for v in obj.data.vertices ]

#--# setKeyframesOnRoute(car, coords3d, durs)

  

#--------------------------------------------------------------------------------------------------------
#    REGISTERING
#--------------------------------------------------------------------------------------------------------
#    
#--------------------------------------------------------------------------------------------------------  
  
classes = [ PropsCoordsDurations,
            ROUTE_PT_panel_1,
            WM_OT_RouteFromJson, WM_OT_ElevateRoute ] 

def register():
    from bpy.utils import register_class
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.props_coords_durations = PointerProperty(type=PropsCoordsDurations)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.props_coords_durations
  
    
if __name__ == "__main__":
    register()    












