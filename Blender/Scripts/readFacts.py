import bge
import bpy
      
def split(s, prefix): 
        
    sls = s.lstrip(prefix)
    srs = sls.rstrip('). ')
    spl = srs.split(',') 
    
    ste = [ e.lstrip(' ') for e in spl ]

    for i in range(len(ste)):
        if not ste[i].startswith('"') and not ste[i].isdigit():
            ste[i] = '"'+ste[i]+'"'
        
    sev = [ eval(e) for e in ste ]     
    print(sev)  
    return sev   


path = "/home/j/UPBGEv0.2.5b-b2.79Linux64/reverse_II.lp"
with open(path,"r") as f:
    lines = f.read().splitlines()

time_dicts = [] 
time_list = [] 

go = ['name','mode','start','target','t_s','t_e']
stay = [ 'name', 'place', 't_s', 't_e' ]

for s in lines:
    
    if s.startswith('go('):
        sev = split(s, 'go(')
        d = dict(zip(go, sev))
        time_dicts.append(d)
        time_list.append(sev)
        
    if s.startswith('stay('):
        sev = split(s, 'stay(')
        d = dict(zip(stay, sev))
        time_dicts.append(d)
        time_list.append(sev)


cont = bge.logic.getCurrentController()
own = cont.owner
sce = bge.logic.getCurrentScene()

own['timeTable'] = time_list

own['t_idx'] = 0  # timeTable index

own['entryRead'] = False

own['t_s'] = -1
own['t_e'] = -1

own['entry'] = -1

own['path'] = False
own['pathLength'] = 0

own['waitOne'] = -1

own['case'] = 0
own['t'] = 0

own['t_s_old'] = 0        
