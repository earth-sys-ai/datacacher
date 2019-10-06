from netCDF4 import Dataset
import numpy as np
import sys
import os
from contourVector import vectorize
import json

# variables to array of polygons
def getData(cdf, res, prev):
    lat = cdf["y"][:]
    lon = cdf["x"][:]
    elems = cdf['element'][:,:]-1
    data = cdf['zeta_max'][:]
    return vectorize(lat, lon, elems, data, res, prev, float(sys.argv[5]));

# convert ndarray structure to json string
def arrToJson(data, min, max):
        print("Encoding json...")

        # collective info and level vars
        levels = []
        polyLen = 0
        vertLen = 0

        # levels
        for i in data:
                polygons = []

                # polygons
                for n in i[1]:
                        vertices = []
                        minV = [n[0][1], n[0][0]]
                        maxV = [n[0][1], n[0][0]]                        
                        
                        # vertices
                        for v in n:
                                vertices.append({
                                        "lat": v[1],
                                        "lng": v[0]
                                })

                                # max and min
                                if v[0] < minV[1]:
                                        minV[1] = v[0]
                                if v[1] < minV[0]:
                                       minV[0] = v[1]
                                if v[0] > maxV[1]:
                                        maxV[1] = v[0]
                                if v[1] > maxV[0]:
                                        maxV[0] = v[1]

                        curVertLen = len(n)
                        polygons.append({
                                "vertCount": curVertLen,
                                "minV": minV, 
                                "maxV": maxV, 
                                "vertices": vertices
                        })
                        vertLen += curVertLen

                curPolyLen = len(i[1])
                levels.append({
                        "value": i[0],
                        "polyCount": curPolyLen,
                        "polygons": polygons
                })
                polyLen += curPolyLen

        # parse as json
        return json.dumps({

                # info
                "info": {
                        "levels": len(data),
                        "polygons": polyLen,
                        "vertices": vertLen,
                        "min": min,
                        "max": max
                },

                # everything above
                "levels": levels,
        })

# record size of different levels to csv
def testSize(max, cdf):
        with open('out.csv', 'a') as f:
                for i in range(2, max):
                        l = len(arrToJson(getData(cdf, i), np.min(cdf['zeta_max'][:]), np.max(cdf['zeta_max'][:])))
                        f.write(str(i) + ", " + str(l) + "\n")
                        print("Done: " + str((i / max) * 100) + "%")

# get data, contour, and write to file
def writeData(cdf, res, prev, file):
        data = getData(cdf, res, prev)
        min = np.min(cdf['zeta_max'][:])
        max = np.max(cdf['zeta_max'][:])
        json = arrToJson(data, min, max)
        print("Writing json to file...")
        try:
                os.remove(file)
        except:
                pass
        with open(file, 'a') as f:
                f.write(json)

# encode
if (sys.argv[1] == "-e"):
        print("Reading data from file...")
        ncv = Dataset(sys.argv[2])
        writeData(ncv.variables, sys.argv[4], False, sys.argv[3])
        print("Finished.")

# encode with preview
elif (sys.argv[1] == "-p"):
        print("Reading data from file...")
        ncv = Dataset(sys.argv[2])
        writeData(ncv.variables, sys.argv[4], True, sys.argv[3])
        print("Finished.")

# size test
elif (sys.argv[1] == "-t"):
        ncv = Dataset(sys.argv[2])
        testSize(sys.argv[3], ncv.variables)
        print("Finished.")