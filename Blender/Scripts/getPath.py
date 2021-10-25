# This file reads the paths on the navigaton mesh.
# It reads the "go" statements and its start and end times, starting point and target.
# The navmesh calculates the path and returns the vertices in the scene. 
# The pathlength will be summed up and the velocity calculated.
# These velocities can be used to compare with other statements, reasonability, etc. - e.g. tram/car must have been used etc.

import bge

cont = bge.logic.getCurrentController()
own = cont.owner
steer = cont.actuators['Steering']
sce = bge.logic.getCurrentScene()

intTime = sce.objects['UniversalTime']['intTime']        
diff    = sce.objects['UniversalTime']['diff'] 



def getPath():
    
    if own['case'] == 1:
        own['t'] = bge.logic.getClockTime()
                
        for v in steer.path:
            print(v)
            
        l_total = 0
        for i in range(len(steer.path)-1):
            l = (steer.path[i+1] -  steer.path[i]).length
            l_total = l_total + l 
            
        #print("Path length", l_total) 
                  
        own['case'] = 2
        return l_total

    if own['case'] == 0:
         
        own['t'] = bge.logic.getClockTime()        
        own['case'] = 1


  
for entry in range(len(own['timeTable'])):
           
    if own['t_idx'] == entry and own['entryRead'] == False:
        
        own['entryRead'] = True  
        own['t_s_old']   = own['t_s'] 
        own['t_s']       = own['timeTable'][entry][-2] 
        own['t_e']       = own['timeTable'][entry][-1]         
        own['entry']     = entry 
                         
           
        
    if intTime == own['t_s'] and own['entryRead'] == True:  # new entry read and start time of this entry reached
              
        own['entryRead'] = False                               
        own['t_idx']     = own['t_idx'] + 1    
                                       
        e = own['timeTable'][own['entry']]   
                     
        if len(e) == 6:                       # length of 'go'-statements is 6
                                           
            steer.target = sce.objects[e[3]]  # position of target in go-entry  is 3 
            print('target:', e[3]) 
            
            own['t_s_old'] = own['t_s'] 
            own['case'] = 0   

  
             
if intTime == own['t_s_old']:
    
    if own['case'] == 1:
       
        length  =  getPath()
        t_delta =  ( own['t_s'] - own['t_s_old'] )
        
        if t_delta != 0:
            veloc   =  length / t_delta
        else:
            print("t_delta and veloc set to zero")  
            t_delta  =  0
            veloc    =  0  
        
        print("Length   Time    Duration    Velocity")
        print(length, bge.logic.getClockTime(), t_delta, veloc)
                 
           
    if diff != 0:
        
        getPath()    # run once to get empty path and change 'case' variable 
