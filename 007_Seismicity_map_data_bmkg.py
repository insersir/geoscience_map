import pygmt
import pandas as pd
import numpy as np

# 1. Read Data Excel
data = pd.read_excel(r"D:\training_pygmt\data\List_FM_Juni_2021-mod.xlsx")           # change this
# print(data)

# 2. Save figure
title = 'events_map_data_bmkg'
file_path = r"D:\training_pygmt\saveplot"                                           # change this


# Don't modify the lines below ###################################
# 3. Conditioning Data
# If the latitude is S so it will multiply to -1.
data.loc[data["Dir_Lat"] == 'S', "Lat"] = data['Lat']*-1

# If the longitude is W so it will multiply to -1.
data.loc[data["Dir_Long"] == 'W', "Long"] = data['Long']*-1
# print(data)


# 4. Plot events
lon = data.Long
lat = data.Lat
mag = data.Mag
depth_km = data.Depth_km

fig = pygmt.Figure()
fig.coast(
    region='g',
    projection='R120/8i',
    shorelines=True,
    water='white',
    land='grey',
    frame='ag',
    borders="1/0.5p,black")

# colorbar colormap
pygmt.makecpt(cmap="jet", series=[
              depth_km.min(), depth_km.max()])

fig.plot(
    x=lon,
    y=lat,
    color=depth_km,
    cmap=True,
    style="c0.25c",
    pen="black")

fig.colorbar(frame='af+l"Depth (km)"')
fig.show()

file_save = file_path + "/" + title + '.png'
fig.savefig(file_save, crop=True, dpi=300, transparent=False)

# note: We can change the global region into Indonesia's region
