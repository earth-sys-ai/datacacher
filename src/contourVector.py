# vectorizes array of values into a array of polygons
# each element in the output array contains two elements:
# an array of polygons, and a value
# each polygon contains an array of coordinates, which are an array of floats.

from distutils.util import strtobool
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
import sys

# used for preview confirmation
def prompt(query):
    sys.stdout.write("%s [y/n]: " % query)
    val = input()
    try:
        ret = strtobool(val)
    except ValueError:
        sys.stdout.write("Please answer with y/n")
        return prompt(query)
    return ret

# returns an array of polygons and values
def genPoly(cs, levels, thres):
    print("Generating polygons...")
    outp = []
    for i, collection in enumerate(cs.collections):
        if (abs(levels[i]) > thres):
            poly = []
            for path in collection.get_paths():
                path.should_simplify = False
                verts = path.to_polygons(closed_only=True)
                for v in verts:
                    poly.append(v)
            if (len(poly) > 0):
                outp.append([levels[i], poly])
    return outp

# takes raster points and generates a vector contour
def vectorize(lat, lon, elems, data, res, prev, thres):
    print("Distributing levels...")
    MinVal = np.min(data) 
    MaxVal = np.max(data)
    levels = np.linspace(MinVal, MaxVal, num=str(int(res) + 1))
    print("Contouring data...")
    triangles = tri.Triangulation(lon, lat, triangles=elems)
    contour = plt.tricontourf(triangles, data, levels=levels, extend='max')
    
    # preview and confirm
    if (prev):
        plt.show()
        if not prompt("Would you like to write this data?"):
            exit()
            
    return genPoly(contour, levels, thres)