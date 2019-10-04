import json
import sys
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import matplotlib as mpl
import numpy as np

# reads file to polycollection
def readJson(filename):
    with open(filename) as f:
        return json.load(f)

# convert json to poly collection
def genPoly(json):
    polygons = []
    values = []
    for level in json["levels"]:
        value = level["value"]
        for poly in level["polygons"]:
                polygon = []
                for v in poly['vertices']:
                        polygon.append([v['lat'], v['lng']])
                polygons.append(polygon)
                values.append(value)
                
    return PolyCollection(polygons, array=np.array(values), closed=True)

# plot
ax = plt.subplot()
polys = genPoly(readJson(sys.argv[1]))
ax.add_collection(polys)
ax.autoscale_view()
plt.show()