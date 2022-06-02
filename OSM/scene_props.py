import bpy

sce = bpy.data.scenes['Scene']

sc_x = sce['crs x']
sc_y = sce['crs y']

print(sc_x, sc_y)
