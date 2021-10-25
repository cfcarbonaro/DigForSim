#script (python)

import clingo
import math

N = clingo.Number

def div(a, b):
    return N(a.number // b.number)

    	
def dist(x, y):
    xn = x.number
    yn = y.number
    d = math.sqrt(xn**2 + yn**2)
    #d_int = math.floor(d)
    d_int = math.ceil(d)    # ceil function: if 0 -> really Zero! ( but still unknown path possible )
    return N(d_int)

#end.
