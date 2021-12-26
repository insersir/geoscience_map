# Seismicity map
# B. The size of the circle represents the magnitude

import pygmt
import pandas as pd
import numpy as np

# 1. Read data
data = pd.read_excel(r"D:\training_pygmt\data\catalog_earthquakes_Indonesia.xlsx")      # change this

# 2. save figure
title = 'events_map_magnitude'
file_path = r"D:\training_pygmt\saveplot"                                               # change this

# 3. define topography data source
topo_data = '@earth_relief_30s'                                                         # change this


# Don't modify the lines below ###################################
lon = data.lon
lat = data.lat
mag = data.mag
depth_km = data.depth_km

region = [np.min(lon)-5,
          np.max(lon)+5,
          np.min(lat)-5,
          np.max(lat)+5]


# 4. Plot events (Circle's size represents the magnitude)
fig = pygmt.Figure()

# make color pallets
pygmt.makecpt(
    cmap='geo',
    series='-8000/6000/1000',
    continuous=True)

# plot high res topography
fig.grdimage(
    grid=topo_data,
    region=region,
    projection='M8i',
    shading=True,
    frame=True)

# plot coast lines
fig.coast(shorelines=True,
          frame=True)

# colorbar in x-axis
fig.colorbar(
    frame=['+l"Topography"', "y+lm"])

fig.plot(
    x=lon,
    y=lat,
    size=0.05 * (2 ** mag),
    color='red',
    style="cc",
    pen="black")
fig.show()

file_save = file_path + "/" + title + '.png'
fig.savefig(file_save, crop=True, dpi=300, transparent=False)
