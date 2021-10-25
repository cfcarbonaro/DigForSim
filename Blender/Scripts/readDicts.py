import bpy

conf = "persons.config"
path = "./config_DFS/" + conf   # set actual path

with open(path,"r") as f:
    lines = f.read().splitlines()
    print(lines)
 
dicts = []    
for l in lines: 
    dicts.append(eval(l))   
    
for entry in range(len(lines)):    # entry of persons database == each is one dictionary
    # for each entry an agent (as sphere) will be created:
    # its location ( in this script ) is directly next to the one before:
    bpy.ops.mesh.primitive_uv_sphere_add(size=1, location=(0+2*entry, 0, 1))
    ob = bpy.context.object
    ob.name = ( dicts[entry]['surname'] + " " + dicts[entry]['name'] )
    ob.show_name = True

    for attr in dicts[entry]:
        print(attr)
        ob[attr] = dicts[entry][attr]  # Blender properties are created ( UI-entries )

    if 'mobilePhone' in ob:
        print('has a mobile phone')
        # phone created as "cube", location is relative to active object!
        bpy.ops.mesh.primitive_cube_add(radius=0.3, location=(0, 0, 2.5) )
        
        ob_c = bpy.context.object  # will become child (c) object
        
        ob_c.name = ( "MobilePhone " + str(dicts[entry]['mobilePhone']) )
        ob_c.show_name = True
        ob_c.parent = bpy.data.objects[ob.name]
       
    if 'bankcard' in ob:
        print('has a bankcard')
        # card created as "cube", z-location grows for visibility (above the parent)
        bpy.ops.mesh.primitive_cube_add(radius=0.2, location=(0, 0, 3.1) )
        ob_c = bpy.context.object
        ob_c.name = ( "Bankcard " + str(dicts[entry]['bankcard']) )
        ob_c.show_name = True
        ob_c.parent = bpy.data.objects[ob.name]
