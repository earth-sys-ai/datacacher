# datacacher
Handles caching of data in NetCDF to json to be handled, processed, and served by the Flask server.

---
## Usage

The genCache.py script may be used to generate a json cache from a NetCDF file.
It takes a flag, an input file, an output file, a resolution, and a minimum deviation.
The script will only add the polygon if it's distance from zero exceeds the deviation value.
This is used to filter unwanted background polygons for size and efficiency.

Ex:
`> python3 genCache.py -e data.nc data100.json 100 0.5`

If you wish to preview the data before caching yoy may use the `-p` flag instead.

Ex:
`> python3 genCache.py -p data.nc data100.json 100 0.5`

The cacheData.sh script can be used to automatically generate cache files for multiple levels to use with the server in a given directory

Ex:
`> ./cacheData.sh data.nc cacheDir 0.5`

---
## Setup

To setup install the necessary requirements through pip.
```
netcdf4
numpy
matplotlib
```

Other packages such as python3-cairo or python3-gobjects may be required to be installed through a native package manager.


---
## API

The output of these scripts will generate json files with a list of polygons and values, aswell as information about them.   

It will have the following values in the following format:


```c
info
    - levels: int                       // number of levels
    - polygons: int                     // number of total polygons
    - vertices: int                     // number ot total vertices
    - min: float                        // minimum of all values
    - max: float                        // maximum of all values
    
levels: array                           // levels containing values and polygons
    - levels[X]                         // any level
        - value: float                  // value of current level
        - polyCount: int                // number of polygons in the current level
        - polygons: array               // polygon array
            - polygons[X]               // any polygon
                - vertCount: int        // number of vertices in the the current polygon
                - minV: [float, float]  // maximum x and y values for any vertex
                - maxV: [float, float]  // minimum x and y values for any vertex
                - vertices: array       // vertex array
                    - vertices[X]       // any vertex
                        - lat: float    // latitude as float
                        - lng: float    // longitude as float
```