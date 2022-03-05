import bpy
import os


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

class PropsASP(PropertyGroup):

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


# ------------------------------------------------------------------------
#    Operators ASP 
# ------------------------------------------------------------------------

class WM_OT_RunClingo(Operator):
    '''Runs ASP script in text editor with clingo'''
    bl_label = "Run clingo"
    bl_idname = "wm.run_clingo"

    def execute(self, context):
        #scene = context.scene
        #mytool = scene.my_tool2

        print("Run file in clingo...")
        #print(bpy.ops.text.run_script()


        #print("File path:", mytool.my_file)

        #path = "/home/j/UPBGEv0.2.5b-b2.79Linux64/Log_agents/"
        #textfile = mytool.my_file
        #text = bpy.data.texts.load(textfile)

        for area in bpy.context.screen.areas:
            if area.type == 'TEXT_EDITOR':
                print(area.spaces[0].text)
                
                cur_file = area.spaces[0].text.name
                area.spaces.active.text = bpy.data.texts[cur_file]

                save_path = "/home/j/DigForSim/ASP"
                file_name = "temp_clingo.lp"
                complete_path = os.path.join(save_path, file_name)
                        
        
                #if "out.log" in area.spaces[0].text.name:
                #    print("don't run clingo!")
                if area.spaces[0].text.name.endswith(".lp") and area.y > 300:
                    print("Accepted by clingo")

                    f = open(complete_path, "w")               
                    f.write(area.spaces[0].text.as_string())
                    f.close()

                    os.system('bash /home/j/DigForSim/ASP/run_clingo.sh')
               
                    #textfile = os.path.join(save_path, "out.log")
                    #text = bpy.data.texts.load(textfile)

                    #area.spaces[0].text = text # make loaded text file visible

        ## run loop again (shitty way )
        for area in bpy.context.screen.areas:
            if area.type == 'TEXT_EDITOR':
                #if "out.log" in area.spaces[0].text.name:
                if area.y < 50:
                    print("Here Result can be loaded!")
                    textfile = os.path.join(save_path, "out.log")
                    text = bpy.data.texts.load(textfile)              
                    area.spaces[0].text = text # make loaded text file visible

 
        print("Current file:", cur_file)
        #bpy.data.texts.load(textfile)
        #bpy.ops.text.open(filepath=textfile)

        return {'FINISHED'}



class WM_OT_LoadAnswerSets(Operator):
    bl_label = "Load found answer sets."
    bl_idname = "wm.load_answer_sets"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool2

        # print the values to the console
        print("Loaded answer sets to editor.")
        #print("bool state:", mytool.my_bool)
        #print("int value:", mytool.my_int)
        #print("float value:", mytool.my_float)
        print("File path:", mytool.my_file)
        #print("enum state:", mytool.my_enum)
        #path = "/home/j/UPBGEv0.2.5b-b2.79Linux64/Log_agents/"
        textfile = mytool.my_file
        text = bpy.data.texts.load(textfile)

        for area in bpy.context.screen.areas:
            if area.type == 'TEXT_EDITOR':
                area.spaces[0].text = text # make loaded text file visible

        #bpy.ops.text.open(filepath=textfile)

        return {'FINISHED'}




# ------------------------------------------------------------------------
#    Panels ASP 
# ------------------------------------------------------------------------

class EXAMPLE_panel2:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ASP"
    bl_options = {"DEFAULT_CLOSED"}

# Main Panel 1
class ASP_PT_panel_1(EXAMPLE_panel2, bpy.types.Panel):
    bl_idname = "ASP_PT_panel_1"
    bl_label = "Solo ASP"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Set parameters for ASP.")
        


# Subpanel 1-1
class ASP_PT_panel_1_1(EXAMPLE_panel2, bpy.types.Panel):
    bl_parent_id = "ASP_PT_panel_1"
    bl_label = "Load Answer Sets"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        propsasp = scene.props_asp

        layout.label(text="Read ASP file")
        layout.prop(propsasp, "use_clingo_v5")
        #layout.prop(mytool, "my_file")
        #layout.operator("wm.load_script")
        layout.operator("wm.run_clingo")



classes = [ ASP_PT_panel_1, ASP_PT_panel_1_1, PropsASP, WM_OT_RunClingo  ] 



def register():
    from bpy.utils import register_class
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.props_asp = PointerProperty(type=PropsASP)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.props_asp









