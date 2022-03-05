   
import bpy
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


#print(bpy.data.scenes['Scene'].my_tool2.startPosAgent[0])

# ------------------------------------------------------------------------
#    Scene Properties 
# ------------------------------------------------------------------------

class PropsDateTime(PropertyGroup):

    date: IntVectorProperty(
        name="Date",
        description="Date vector",
        default = (0,0,0)
        )
    year: IntProperty(
        name="Year",
        description="YYYY",
        default = time.localtime().tm_year
        )
        
    month: IntProperty(
        name="Month",
        description="MM",
        default = time.localtime().tm_mon
        )
        
    day: IntProperty(
        name="Day",
        description="DD",
        default = time.localtime().tm_mday
        )   
    hour: IntProperty(
        name="Hour",
        description="hh",
        default = time.localtime().tm_hour
        )
        
    minute: IntProperty(
        name="Minute",
        description="mm",
        default = time.localtime().tm_min
        )
        
    second: IntProperty(
        name="Second",
        description="ss",
        default = time.localtime().tm_sec
        ) 
        
        
        
# ------------------------------------------------------------------------
#    Panels 
# ------------------------------------------------------------------------
class DATETIME_panel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Dig-For-Sim"
    bl_options = {"DEFAULT_CLOSED"}

# Main Panel 1
class DATETIME_PT_panel_1(DATETIME_panel, bpy.types.Panel):
    bl_idname = "DATETIME_PT_panel_1"
    bl_label = "Date and Time"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props_Datetime = scene.props_Datetime        
        layout.label(text="Start date of Agent:")
        layout.prop(props_Datetime, "year")
        layout.prop(props_Datetime, "month")
        layout.prop(props_Datetime, "day")
        layout.separator()
        layout.label(text="Start time of Agent:")
        layout.prop(props_Datetime, "hour")
        layout.prop(props_Datetime, "minute")
        layout.prop(props_Datetime, "second")        
        

# ------------------------------------------------------------------------
#    Registering
# ------------------------------------------------------------------------    
classes = [ PropsDateTime, DATETIME_PT_panel_1 ] 

def register():
    from bpy.utils import register_class
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.props_Datetime = PointerProperty(type=PropsDateTime)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.props_Datetime
  
    
if __name__ == "__main__":
    register()    
    
    
