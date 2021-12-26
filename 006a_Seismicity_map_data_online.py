# Seismicity map
# A. Color bar to represent the depth of events

import pygmt
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
import pandas as pd
import numpy as np


# 1. Download Data
client = Client("IRIS")
starttime = UTCDateTime("2011-01-01T00:00:00")                                              # change this
endtime = UTCDateTime("2011-06-01T00:00:00")                                                # change this
min_lon = 90                                                                                # change this
max_lon = 140                                                                               # change this
min_lat = -9                                                                                # change this
max_lat = 10                                                                                # change this

# 2. Save figure
title = 'events_map_depth'
file_path = r"D:\training_pygmt\saveplot"                                                   # change this


# 3. save catalog to excel
save_catalog = r"D:\training_pygmt\data" + "/" + "catalog_earthquakes_Indonesia.xlsx"       # change this

# 4. define topography data source
topo_data = '@earth_relief_30s'                                                             # change this


#
# Don't modify the lines below ###################################
catalog = client.get_events(starttime=starttime, endtime=endtime, minmagnitude=5,
                            minlongitude=min_lon, maxlongitude=max_lon,
                            minlatitude=min_lat, maxlatitude=max_lat)

lon, lat, depth, mag = [], [], [], []
for i in range(len(catalog)):
    event = catalog[i]
    origins = event.origins[0]
    lon.append(origins.longitude)
    lat.append(origins.latitude)
    depth.append(origins.depth/1000)
    mag.append(event.magnitudes[0].mag)

data = pd.DataFrame({"lon": lon, "lat": lat, "depth_km": depth, "mag": mag})
lon = data.lon
lat = data.lat
mag = data.mag
depth_km = data.depth_km

data.to_excel(save_catalog, index=False)
region = [np.min(lon)-5,
          np.max(lon)+5,
          np.min(lat)-5,
          np.max(lat)+5]


# 5. Plot events (color bar to represent the depth)
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
    color=depth_km,
    cmap=True,
    style="c0.3c",
    pen="black")

fig.colorbar(frame='af+l"Depth (km)"')
fig.show()

file_save = file_path + "/" + title + '.png'
fig.savefig(file_save, crop=True, dpi=300, transparent=False)
