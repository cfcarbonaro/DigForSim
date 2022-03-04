## bundle here some operators I can use for many different tasks?
## e.g. compute overlap of radio cells
## draw area ( bounding box )



import bpy
import os
from pyproj import Proj, transform
from shapely import geometry as g    # shapely for overlap (=intersection) computation.
#from .new_radio_cell import makeRoute
from .draw_area import getBBox


from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
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
#    Scene Properties 
# ------------------------------------------------------------------------

#sc = bpy.data.scenes['Scene']
#p_rcell = sc.props_new_radio_cell
#print("Lat:", sc['latitude'])
#print("Name of radiocell:", bpy.data.scenes['Scene']['props_new_radio_cell']['name'])




class PropsOperators(PropertyGroup):

 
    
    use_clingo_v5: BoolProperty(
        name="Use clingo >= v.5.0",
        description="Check to use specified clingo version.",
        default = True
        )

    answer_sets: StringProperty(
        name = "File",
        description="Choose a file:",
        default="",
        maxlen=1024,
        #subtype='FILE_PATH'
        )
        
    obj_1: StringProperty(
        name="Obj 1",
        description="First object to intersect",
        default = ""
        ) 
        
    obj_2: StringProperty(
        name="Obj 2",
        description="Second object to intersect",
        default = ""
        )
        
    rCellsToIntersect : EnumProperty(
                    name='Radio cells',
                    description='Select radio cells to intersect.',
                    items={
                    ('PNG', 'png', 'Save as png'),
                    ('JPEG', 'jpg', 'Save as jpg'),
                    ('OPEN_EXR_MULTILAYER', 'exr', 'Save as multilayer exr')},
                    default='PNG')
                    
                  
def getRCells(self, context): #

    items = []
    for item in bpy.data.scenes["Scene"].collection.children["Radio cells"].all_objects:
    
        items.append((item.name, item.name, ""))
    
    return items                    
                    
def makePolygonMesh(coords2d, name):  # name = a string,
    
    coords3d = [ (x,y,0) for (x,y) in coords2d ]
    e = []
    for i in range(len(coords3d)-1):  # -1 to avoid edge to center
        e.append(( i, i+1 ))
        
    # make mesh
    vertices = coords3d
    edges = e
    faces = []
    
    circle = bpy.data.meshes.new(name)   # not only circle, but intersect/overlap here
    circle.from_pydata(vertices, edges, faces)
    circle.update()
    
    # make object from mesh
    circle_ob = bpy.data.objects.new(name, circle)
    
    scene = bpy.context.scene        
    p_nrc = scene.props_new_radio_cell   
     
    #ob = bpy.context.object  # ob should be radio cell object
    #circle_ob.parent = bpy.data.objects[ob.name]  

       
    # make collection
    coll = 'Overlapping areas'
    if coll in bpy.data.collections:
        print("Coll in collections:", coll)  
              
    else:
        sa = bpy.data.collections.new('Overlapping areas')
        bpy.context.scene.collection.children.link(sa)
    
    bpy.data.collections[coll].objects.link(circle_ob) 
    print("Active obj before getBBox", circle_ob) 
    getBBox()
                  
    return circle_ob 
                       




def setPencil():

    bpy.ops.object.gpencil_add(type='EMPTY')
    
    pen = bpy.context.object
    pen.name = "Pen"
    print("Name: ", pen.name)


    bpy.ops.object.mode_set(mode='PAINT_GPENCIL')

    bpy.ops.wm.tool_set_by_id(name="builtin.box")

    bpy.context.scene.tool_settings.gpencil_stroke_placement_view3d = 'SURFACE'
    bpy.context.object.data.zdepth_offset = 0.0001

    bpy.context.object.data.stroke_thickness_space = 'SCREENSPACE'
    

    
def setOrigin():
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
 

    
def getBBox():

    sc = bpy.data.scenes['Scene']
    crsx = sc['crs x'] 
    crsy = sc['crs y'] 

    obj = bpy.context.object
    boundPts = bpy.context.object.bound_box

    xmin = min([pt[0] for pt in boundPts]) + obj.location.x + crsx
    xmax = max([pt[0] for pt in boundPts]) + obj.location.x + crsx
    ymin = min([pt[1] for pt in boundPts]) + obj.location.y + crsy
    ymax = max([pt[1] for pt in boundPts]) + obj.location.y + crsy

    inProj = Proj('epsg:3857')
    outProj = Proj('epsg:4326')

    lb = transform(inProj,outProj,xmin, ymin)  # leftbutton
    rt = transform(inProj,outProj,xmax, ymax)  # righttop

    S, W, N, E = lb[0], lb[1], rt[0], rt[1]

    bbox = "{},{},{},{}".format(S,W,N,E)

    print(bbox)
    
    return S, W, N, E



# ------------------------------------------------------------------------
#    Operators ASP 
# ------------------------------------------------------------------------

class WM_OT_AreaOfInterest(Operator):
    '''Draw square to indicate area of interest.'''
    bl_label = "Draw AOI."
    bl_idname = "wm.draw_aoi"

    def execute(self, context):
    
        scene = context.scene
        p_ops = scene.props_ops
            
        setPencil()  

        return {'FINISHED'}



class WM_OT_Confirm_Aoi(Operator):
    '''Confirm area of interest.'''
    bl_label = "Confirm."
    bl_idname = "wm.confirm_aoi"

    def execute(self, context):
    
        scene = context.scene
        p_ops = scene.props_ops
        
        setOrigin() 

        return {'FINISHED'}



class WM_OT_Get_BBox(Operator):
    '''Get the bounding box of pencil-object.'''
    bl_label = "Get Bounding Box."
    bl_idname = "wm.get_bbox"

    def execute(self, context):
    
        scene = context.scene
        #draw = scene.props_draw
        
        S, W, N, E = getBBox() 
        
        ll_lat = S
        ll_lon = W
        ur_lat = N
        ur_lon = E
        
        url="http://overpass-api.de/api/interpreter?data=(nwr({},{},{},{});<;node(w););out meta;".format(ll_lat,ll_lon,ur_lat,ur_lon)
        qry = 'wget -O bbox_temp.osm "{}"'.format(url)
        os.system(qry)
        print(qry)
        
        #url="http://overpass-api.de/api/interpreter?data=(node({},{},{},{});<;rel(br););out meta;".format(ll_lat,ll_lon,ur_lat,ur_lon)
                
        return {'FINISHED'}
        



class WM_OT_Import_Objects(Operator):
    '''Import (buildings) from bounding box of pencil-object.'''
    bl_label = "Import objects inside bbox."
    bl_idname = "wm.import_objects"

    def execute(self, context):
    
        scene = context.scene
        #draw = scene.props_draw
        
        #S, W, N, E = getBBox() 
        
        return {'FINISHED'}




# ------------------------------------------------------------------------
#    more operators : compute overlap

       


class MyEnumItems(bpy.types.PropertyGroup):
    @classmethod
    def register(cls):
        bpy.types.Scene.my_enum_items = bpy.props.PointerProperty(type=MyEnumItems)

    @classmethod
    def unregister(cls):
        del bpy.types.Scene.my_enum_items

    overlap1 : bpy.props.EnumProperty(
        name="overlap1",
        description="overlap1",
        # items argument required to initialize, just filled with empty values
        items = getRCells,
    )
    
    overlap2 : bpy.props.EnumProperty(
        name="overlap2",
        description="overlap2",
        # items argument required to initialize, just filled with empty values
        items = getRCells,
    )
    
    
      
class WM_OT_Compute_Overlap(Operator):
    '''Compute overlap (=intersection) of e.g. radio cells.'''
    bl_label = "Compute overlap."
    bl_idname = "wm.compute_overlap"

    def execute(self, context):
    
        scene = context.scene
        p_ops = scene.props_ops
        p_rcell = scene.props_new_radio_cell
        
        print("Obj 1:", p_ops.overlap1)
        print("Obj 2:", p_ops.overlap2)
        obj_1 = p_ops.overlap1
        obj_2 = p_ops.overlap2
        r1 = scene.objects[obj_1]['Radius']
        r2 = scene.objects[obj_2]['Radius']
        print(r1)
        print(r2)
        pos1 = scene.objects[obj_1].location
        pos2 = scene.objects[obj_2].location
        
        a = g.Point(pos1).buffer(r1)
        b = g.Point(pos2).buffer(r2)
        
        i = b.intersects(a)
        print("Intersects?", i)
        x = b.intersection(a)
        print(x)
        coords = list(x.exterior.coords)
        
        rb = makePolygonMesh(coords, "Intersect")


       
        
        return {'FINISHED'}


 
      
# ------------------------------------------------------------------------
#    Panels ASP 
# ------------------------------------------------------------------------


class DRAW_AOI_panel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Routes / OSM"
    bl_options = {"DEFAULT_CLOSED"}


# Main Panel 1
class DRAW_AOI_PT_panel_1(DRAW_AOI_panel, bpy.types.Panel):
    bl_idname = "DRAW_AOI_PT_panel_1"
    bl_label = "Area of Interest"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Use grease Pencil to sketch area of interest.")
        layout.operator("wm.draw_aoi")
        layout.operator("wm.confirm_aoi")
        layout.operator("wm.get_bbox")
        layout.operator("wm.compute_overlap")


# Subpanel 1-1
class DRAW_AOI_PT_panel_1_1(DRAW_AOI_panel, bpy.types.Panel):
    bl_parent_id = "DRAW_AOI_PT_panel_1"
    bl_label = "Some subpanel."

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        p_asp = scene.props_asp
        p_ops = scene.props_ops
        p_enum = scene.my_enum_items

        layout.label(text="Read ASP file")
        layout.prop(p_asp, "use_clingo_v5")
        #layout.prop(p_ops, "rCellsToIntersect")
        #layout.prop(context.scene.my_enum_items, "asdf")
        #layout.prop(context.scene.my_enum_items, "asdf2")
        layout.prop(p_enum, "overlap1")
        layout.prop(p_enum, "overlap2")

        



classes = [ WM_OT_AreaOfInterest, DRAW_AOI_PT_panel_1, DRAW_AOI_PT_panel_1_1, PropsOperators,
            WM_OT_Confirm_Aoi, WM_OT_Get_BBox,
            WM_OT_Compute_Overlap,
            MyEnumItems ]

           




def register():
    from bpy.utils import register_class
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.props_ops = PointerProperty(type=PropsOperators)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.props_draw








