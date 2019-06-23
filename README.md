# datacacher
Handles caching of data in NetCDF to json to be handled, processed, and served by the Flask server.

---
## Usage

The genCache.py script may be used to generate a json cache from a NetCDF file.
It takes a flag, an input file, an output file, and a resolution.

Ex:
`> python3 genCache.py -e data.nc data100.json 100`

If you wish to preview the data before caching you can use the `-p` flag instead.

Ex:
`> python3 genCache.py -p data.nc data100.json 100`

If you wish to preview the data after being cache you can use the viewCache.py script.

Ex:
`> python3 viewCache.py data100.json`

The cacheData.sh script can be used to automatically generate cache files for multiple levels to use with the server in a given directory

Ex:
`> ./cacheData.sh data.nc cacheDir`

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
            - polygons[X]               // any level
                - vertCount: int        // number of vertices in the the current polygon
                - vertices: array       // vertex array
                    - vertices[X]       // any vertex
                        - lat: float    // latitude as float
                        - lng: float    // longitude as float
```