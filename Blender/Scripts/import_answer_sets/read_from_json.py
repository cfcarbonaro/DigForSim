import json
import re
import bpy

with open(r'/home/jens/spade_pur.json','r') as f: 
      j=json.load(f) 
      print (j)

coll = bpy.context.blend_data.collections.new(name="Answer Sets")
bpy.context.collection.children.link(coll)
      
for i, val in enumerate(j["Call"][0]["Witnesses"]):
    print(val["Value"])  
    
    soe = bpy.data.collections.new(name="SoE "+str(i)) 
    print(soe)
    
    bpy.data.collections['Answer Sets'].children.link(soe)
    
    #bpy.ops.mesh.primitive_cube_add(location=(i*2.3, 0, 0), scale=(1, 1, 1))
    #obj = bpy.context.active_object
    #bpy.ops.collection.objects_remove_all()
    #bpy.data.collections[soe.name].objects.link(obj)
    
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0,0,0), scale=(1, 1, 1))
    obj = bpy.context.active_object
    obj.name = "tom"+"_soe_"+str(i)
    obj.show_name = True
    
    bpy.ops.collection.objects_remove_all()
    bpy.data.collections[soe.name].objects.link(obj)


    bpy.ops.mesh.primitive_uv_sphere_add(location=(0,0,0), scale=(1, 1, 1))
    obj = bpy.context.active_object
    obj.name = "john"+"_soe_"+str(i)
    obj.show_name = True
    
    bpy.ops.collection.objects_remove_all()
    bpy.data.collections[soe.name].objects.link(obj)
    
    
### create every single agent manually... TODO: create automatically!
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0,0,0), scale=(1, 1, 1))
    obj = bpy.context.active_object
    obj.name = "sam_spade"+"_soe_"+str(i)
    obj.show_name = True
    
    bpy.ops.collection.objects_remove_all()
    bpy.data.collections[soe.name].objects.link(obj)
    
    for atom in val["Value"]:
             
        if atom.startswith('alibi('):
            print("ALIBI")
            #m = re.search(r"alibi\((\w+),loc\((-?\d+),(-?\d+)\),(\d+)", str(l[i]) )
        
        if atom.startswith('at('):
            #m = re.search(r"at\((\w+),loc\((-?\d+),(-?\d+)\),(\d+)", atom )
            m = re.search(r"at\((\w+),loc\((-?\d+),(-?\d+)\),(\d+)", atom )
            print(atom)
            if m:
                print( m[2], m[3], atom )
                a, x, y, t = m[1]+"_soe_"+str(i), eval(m[2]), eval(m[3]), eval(m[4])
                bpy.ops.mesh.primitive_circle_add(radius=1, location=(x,y,0))
                
                #bpy.ops.object.convert(target='GPENCIL')  ### makes it very slow!!
    
                obj = bpy.context.object
                obj.name = "{soe}: at( {a}, {t} )".format( a=a, t=t, soe=str(i) )
                obj.show_name = True
                
                bpy.ops.collection.objects_remove_all()
                bpy.data.collections[soe.name].objects.link(obj)
                
                agent = bpy.data.objects[a]
                agent.location = (x,y,0)
                
                fps = 24
                frame = t * fps
                agent.keyframe_insert(data_path="location", frame=frame)
    
    
