import pickle

brb = pickle.load(open("Brandenburgerstr.p", "rb") )

print(brb.wkt())
