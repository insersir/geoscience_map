# Seismicity map
# C. Combination of color bar and circle size

import pygmt
import pandas as pd
import numpy as np

# 1. Read Data
data = pd.read_excel(r"D:\training_pygmt\data\catalog_earthquakes_Indonesia.xlsx")   # change this

# 2. save figure
title = 'events_map_depth_magnitude'
file_path = r"D:\training_pygmt\saveplot"                                           # change this

# 3. define topography data source
topo_data = '@earth_relief_30s'                                                     # change this


# Don't modify the lines below ###################################
lon = data.lon
lat = data.lat
mag = data.mag
depth_km = data.depth_km

region = [np.min(lon)-5,
          np.max(lon)+5,
          np.min(lat)-5,
          np.max(lat)+5]


# 4. Plot events (color bar represents the depth and circle size represents the magnitude)
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

# color bar colormap
pygmt.makecpt(cmap="jet", series=[
              depth_km.min(), depth_km.max()])

fig.plot(
    x=lon,
    y=lat,
    size=0.01 * (2 ** mag),
    color=depth_km,
    cmap=True,
    style="cc",
    pen="black",  transparency=50)
fig.colorbar(frame='af+l"Depth (km)"')

fig.show()

file_save = file_path + "/" + title + '.png'
fig.savefig(file_save, crop=True, dpi=300, transparent=False)
