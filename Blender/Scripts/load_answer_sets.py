# use this script to load 'pickled' answer sets ( a dict, created in 'import_asp_log.py' )
# I create here for every answer set its own 'collection' ( i.e. kind of layer )
# Then create corresponding agents ('persons') and artifacts --> move to corresp. collection
# Set visibility of agents etc.  
# Import Universal Time
# Set visibility according to universal Time.


import pickle
import bpy


answers = pickle.load( open( "/home/j/Schreibtisch/answers.p", "rb" ) )

scene = bpy.data.scenes['Scene']

# print all available answer sets ( i.e. possible sequence of events = soe )
print("Available Answer sets ( i.e. possible sequences of events ) :", answers.keys())


# create empty for Universal time
bpy.ops.object.empty_add(type='SINGLE_ARROW', align='WORLD', location=(0, 0, 5), scale=(1, 1, 1) )
bpy.context.object.name = 'UNIVERSAL TIME'
bpy.context.object.show_name = True

# and make its logic bricks:
bpy.ops.logic.sensor_add(type='ALWAYS', name="Universal Time")

bpy.ops.logic.controller_add(type='PYTHON', name="Universal Time")

# connect sensor to controller
obj = bpy.context.object
sensor = obj.game.sensors['Universal Time']
sensor.use_pulse_true_level=True
sensor.link( obj.game.controllers['Universal Time'] ) 

# create new game properties (intTime and old intTime)
bpy.ops.object.game_property_new(type='INT', name="intTime")
prop = obj.game.properties['intTime']
prop.value = 0

bpy.ops.object.game_property_new(type='INT', name="intTime_old")
prop = obj.game.properties['intTime_old']
prop.value = 0

# assign Universal Time script
ut = bpy.data.texts['universalTime_2.py']
obj.game.controllers['Universal Time'].text = ut


for num, soe in enumerate(answers.keys()):
    print("Answer set", num + 1)            # count plus one for "human readability" - Starts with 1 instead of 0
    print(answers[soe])
    
    # Create new collection
    collection = bpy.data.collections.new(name="SOE "+str(num + 1))

    # Add collection to scene
    scene.collection.children.link(collection)

    # Create collection instance in scene
    object = bpy.data.objects.new(name="dummy", object_data=None)
    object.instance_collection = collection
    scene.collection.objects.link(object)
        
    # create logic bricks
    bpy.ops.logic.sensor_add(type='ALWAYS', name="Always_"+str(soe))
    bpy.ops.logic.controller_add(type='PYTHON', name="Python_"+str(soe))
    obj = bpy.context.object
        
    # link logic bricks
    sensors = obj.game.sensors
    controllers = obj.game.controllers

    sensor = sensors['Always_'+str(soe)]
    cont = controllers['Python_'+str(soe)]
    sensor.link(cont)
    
    # assign script to logic brick
    script = bpy.data.texts['start_object.py']   # only 'say hello!'-script.
    cont.text = script
   

# choose the answer set ( i.e. possible sequence of events ):
#ans = str(2)  # I chose the second answer set...

# show place of crime in scene
def crimeScene(soe):
    
    print( "Crime at", answers[ soe ]['crime'][0][1])

    x =  answers[soe]['crime'][0][1][0] 
    y =  answers[soe]['crime'][0][1][1] 

    bpy.ops.mesh.primitive_circle_add(radius=1, enter_editmode=False, align='WORLD', location=(x, y, 0), scale=(1, 1, 1))
    bpy.ops.object.convert(target='GPENCIL')



# set agents / persons
def setAgents( agents, soe ):
    
    for agent in answers[ soe ][ agents ]:
        
        if agent in answers[ soe ]:
            
            # get first known position of agent
            x =  answers[ soe ][ agent ][0][1][0]
            y =  answers[ soe ][ agent ][0][1][1] 
            
            # create sphere for agent        
            bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(x, y, 0), scale=(0.4, 0.4, 1))
            bpy.context.object.name = agent
            bpy.context.object.show_name = True



# use this also for appending locations to a list and use that list for createCurve(<list>, <name>)
def paintLocs( agents, soe ):  # paints locations where agents have been with Grease Pencil ; soe = answer set
    
    for agent in answers[ soe ][ agents ]:
        
        if agent in answers[ soe ]:
            
            coords = [] # coords-list for every single agent
            print( "paint locs of agent", agent )
            for loc in answers[ soe ][ agent ]:
                
                print( "Location", loc )
                x = loc[1][0]
                y = loc[1][1]
                z = 0.4 
                t = loc[0] 
                
                # append to list for createCurve function
                coords.append((x,y,0.4))    
                
                if t % 5 == 0:
                    createCircle(x,y,z,t, agent)      
                
                coll = 'SOE '+ soe
                if coll in bpy.data.collections:
                                                         
                    bpy.ops.object.move_to_collection(collection_index=1)
                    bpy.ops.object.collection_link(collection=coll)
            
            print("Coordinates:", coords)
            createCurve(coords, "Path of "+agent, coll)


def createCircle(x,y,z,t, agent):
    
    bpy.ops.mesh.primitive_circle_add(radius=1, enter_editmode=False, align='WORLD', location=(x, y, z), scale=(1, 1, 1))
    bpy.ops.object.convert(target='GPENCIL')
    
    obj = bpy.context.object
    obj.name = "at( {a}, {t} )".format( a=agent, t=t )
    obj.show_name = True
    


def createCurve(coords, name, coll):
    
    # create the Curve Datablock
    curveData = bpy.data.curves.new(name, type='CURVE')
    curveData.dimensions = '3D'
    curveData.resolution_u = 1

    # map coords to spline
    polyline = curveData.splines.new('POLY')
    polyline.points.add(len(coords)-1)
    for i, coord in enumerate(coords):
        x,y,z = coord
        polyline.points[i].co = (x, y, z, 1)

    # create Object
    curveOB = bpy.data.objects.new(name, curveData)

    scn = bpy.context.scene

    bpy.data.collections[coll].objects.link(curveOB)  # assign path to desired collection (e.g. SOE)

    ob = bpy.data.collections[coll].objects[name]

    # set active object ( Blender >= 2.8 )
    bpy.context.view_layer.objects.active = ob

    # select object ( Blender >= 2.8 ) 
    ob.select_set(True)


crimeScene(soe)
setAgents( 'persons', '1' )                     
paintLocs( 'persons', '1' )   

        
                                                             
