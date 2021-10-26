# assigned to an game-object called e.g. "UniversalTime".
# it reads the internal clock of the game engine, and uses a floor function to make it integer. 
# too ignore all changes between two integers, there is a variable called diff (=difference).

# All the other agents will have access to these values.

import bge
import math as m

cont = bge.logic.getCurrentController()
sce  = bge.logic.getCurrentScene()
own = cont.owner
    
    
#----------------  Time   ----------------------------------------
       
time_scale = 1  # x-times velocity of simulation   
bge.logic.setTimeScale(time_scale)
t = bge.logic.getClockTime()
            
own["intTime_old"] = own["intTime"]    
own["intTime"] = m.floor(t)    
diff = own["intTime_old"] - own["intTime"] 
own["diff"] = diff    
               
