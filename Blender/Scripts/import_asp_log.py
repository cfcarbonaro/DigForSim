# this script imports result-files from clingo-output, i.e. one or multiple answer sets.
import bpy
import re
import pickle


# path = "/home/j/Schreibtisch/i.log"
path = "/home/j/UPBGEv0.2.5b-b2.79Linux64/Log_agents/i.log"

with open(path,"r") as f:
    lines = f.read().splitlines()
    print("lines::",lines)

print(20*"=")
counter = 0  

# anser sets ( possible sequences of events )
answers = {}

for l in lines:
    
    if l.startswith('Answer:'):
        counter += 1 
        answers.update( { str(counter) : dict() } )  # create empty dict for every answer set 
        print(l)
    else:
        l = l.split() 
        l.insert(0, counter)                         # label all lines (lists) that belong to the same answer set.

        for i in range(len(l)):
                       
            if str(l[i]).startswith('at('):
                
                # careful!!: -?\d+ is necessary for negative/positive integers....
                m = re.search(r"at\((\w+),loc\((-?\d+),(-?\d+)\),(\d+)", str(l[i]) )  # name, location X,Y, time  
                    
                if (str(m[1]) not in answers[str(counter)]) or (m[1] not in answers[str(counter)]):  # create person's key
                    answers[str(counter)][str(m[1])] = []
                    answers[str(counter)][str(m[1])].append( ( eval(m[4]), (eval(m[2]),eval(m[3])) ) )  # append tupel ( time, ( X,Y ) ) to time-location-list
                else:
                    answers[str(counter)][str(m[1])].append( ( eval(m[4]), (eval(m[2]),eval(m[3])) ) )
                
                    sortLocs = sorted( answers[str(counter)][str(m[1])] , key=lambda x: x[0] )   
                    answers[str(counter)][str(m[1])] = sortLocs                      
                          
                print( m[1],'located at (',m[2],',',m[3],') at', m[4])
                
            elif str(l[i]).startswith('murder('):
             
                m = re.search(r'loc\((\d+),(\d+)\),(\d+)', str(l[i]) )             # murder location, time 
                if 'murder' not in answers[str(counter)]:  # create "crime" key
                    answers[str(counter)]['crime'] = []
                    answers[str(counter)]['crime'].append( ( eval(m[3]), (eval(m[1]),eval(m[2])), "murder" ) ) 
                else:
                    answers[str(counter)]['crime'].append( ( eval(m[3]), (eval(m[1]),eval(m[2])), "murder" ) ) 
                                                                           
                print('Murder/crime located at (',m[1],',', m[2],') at', m[3] )
                               
            elif str(l[i]).startswith('stayAt('):

                m = re.search(r'stayAt\((\w+),loc\((\d+),(\d+)\),(\d+),(\d+)', str(l[i]) )
                print(m[1],'stays from', m[4], 'to', m[5], 'at (',m[2],',', m[3],').')
                
                if str(m[1]) not in answers[str(counter)]:
                    
                    answers[str(counter)][str(m[1])] = []
                    answers[str(counter)][str(m[1])].append( ( eval(m[4]), (eval(m[2]),eval(m[3])) ) )
                else:
                    answers[str(counter)][str(m[1])].append( ( eval(m[4]), (eval(m[2]),eval(m[3])) ) )
                                              
                
            elif str(l[i]).startswith('suspect('):
                
                m = re.search(r'suspect\((\w+)\)', str(l[i]) )
                
                if 'suspects' not in answers[str(counter)]:  # create "suspects" key
                    answers[str(counter)]['suspects'] = []
                    answers[str(counter)]['suspects'].append(m[1])
                else:
                    answers[str(counter)]['suspects'].append(m[1])
                                                                
                print('Suspect:', m[1])
                
            elif str(l[i]).startswith('person('):
                
                m = re.search(r'person\((\w+)\)', str(l[i]) )
                
                if 'persons' not in answers[str(counter)]:
                    answers[str(counter)]['persons'] = []
                    answers[str(counter)]['persons'].append(m[1])
                else:
                    answers[str(counter)]['persons'].append(m[1])
                            
                
        #answers_asp.append(l)   # list of answer sets ( not YET in Python format )

  
pickle.dump( answers, open( "/home/j/Schreibtisch/answers.p", "wb" ) )    


                     
                                                           
                    
                
        
        

