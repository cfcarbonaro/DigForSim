import pickle
from OSMPythonTools.nominatim import Nominatim
nominatim = Nominatim()

brb = nominatim.query('Brandenburger Straße 20, Potsdam', wkt=True)
print(brb.displayName())
print(brb.wkt())
pickle.dump(brb, open("Brandenburgerstr.p", "wb") )
