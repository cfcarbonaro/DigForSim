# adapted for this blend-file on dec 10, 2021

# read single log data in and set directly keyframes according to loc and time


import bpy
import re
import pickle

#path = "/home/j/UPBGEv0.2.5b-b2.79Linux64/Log_agents/Anna Xing_log.lp"
path = "/home/j/DigForSim/Simulate/rw7/rWalker_3.log"

with open(path,"r") as f:
    lines = f.read().splitlines()
    print("lines::",lines)

print(40*"=")


def set_keyframes( agent, x, y, t ):
    
    ag = bpy.data.objects[agent]
    
    x = int(x)
    y = int(y)
    z = int(0)
    t = int(t)
    
    frame_number = 10*(t-1)
    bpy.context.scene.frame_set(frame_number)    
    ag.location = ( x, y, z )
    ag.keyframe_insert(data_path='location', index=-1)
    


for l in lines:
    r = l.replace(" ","")
        
    if l.startswith('at('):
        # careful!!: -?\d+ is necessary for negative/positive integers....
        m = re.search(r"at\((\w+),loc\((-?\d+),(-?\d+)\),(\d+)", r )  # name, location X,Y, time 
        print( m[1],'located at place (',m[2],',',m[3],') at time', m[4])
        
        set_keyframes( m[1], m[2], m[3], m[4] )
