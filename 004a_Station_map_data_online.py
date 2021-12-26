import pygmt
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
import pandas as pd
import numpy as np

# 1. Retrieve station data from the server
client = Client("GFZ")
network = "Z6"
station = "AG2"
starttime = UTCDateTime("2004-01-01")
endtime = UTCDateTime("2007-01-02")

# 2. save figure
title = 'Station_map'
file_path = r"D:\training_pygmt\saveplot"               # change this


# Don't modify the lines below ###################################
inventory = client.get_stations(network=network, station=station,
                                starttime=starttime,
                                endtime=endtime)
# print(inventory)
# print(inventory[0][0])

# 3. DataFrame
lon_sta, lat_sta, code_sta = [], [], []
for i in range(len(inventory[0])):
    lon = inventory[0][i].longitude
    lat = inventory[0][i].latitude
    sta = inventory[0][i].code
    lon_sta.append(lon)
    lat_sta.append(lat)
    code_sta.append(sta)
data = pd.DataFrame({"lon": lon_sta, "lat": lat_sta, "code": code_sta})


# 4. Plot map
regions = [np.min(data.lon) - 1,
           np.max(data.lon) + 1,
           np.min(data.lat) - 0.1,
           np.max(data.lat) + 0.1]

fig = pygmt.Figure()
fig.coast(
    region=regions,
    projection='M6i',
    shorelines=True,
    water='lightblue',
    land='grey',
    frame='ag'
)

fig.plot(
    x=data.lon,
    y=data.lat,
    style='i0.05i',
    color='red',
    pen='black',
    label='station',
)
fig.legend()

with fig.inset(position="jTL+w2.5c+o0.1c/0.1c", margin=0, box="+p1,black"):
    fig.coast(
        region="g",
        projection="G110/-20/2.5c",
        land="gray", water="white",
    )

    rectangle = [[regions[0], regions[2], regions[1], regions[3]]]  # long_min, lat_min, long_maks, lat maks
    fig.plot(data=rectangle, style="r+s", pen="1p,blue")

for i in range(len(data.code)):
    fig.text(text=data.code[i], x=data.lon[i]+0.1, y=data.lat[i]+0.1, font="6p,black")

file_save = file_path + "/" + title + '.png'
fig.savefig(file_save)
fig.show()
