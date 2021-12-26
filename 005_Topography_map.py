import pygmt
import pandas as pd
import numpy as np

# 1. Read data
data = pd.read_excel(r"D:\training_pygmt\data\List Stasiun Gabungan_Tahun_Instalasi_160521_rev6.xlsx")  # change this
print(data.head())

# 2. Save figure
title = 'Station_map_data_BMKG_with_topo'
file_path = r"D:\training_pygmt\saveplot"                                                               # change this

# 3. Define topographic data source
topo_data = '@earth_relief_30s'             # 30 arc second global relief (SRTM15+V2.1 @ 1.0 km)
# topo_data = '@earth_relief_15s'           # 15 arc second global relief (SRTM15+V2.1)
# topo_data = pygmt.datasets.load_earth_relief(resolution="30s", region=region)


# Don't modify the lines below ###################################
lon = data.LNG
lat = data.LAT
sta = data.KODE

region = [np.min(lon)-5,
          np.max(lon)+5,
          np.min(lat)-5,
          np.max(lat)+5]

# 4. Plot topography & stations
fig = pygmt.Figure()

# make color pallets
pygmt.makecpt(
    cmap='geo',
    series='-3000/4000/200',
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

# Plot colorbar
# colorbar in x-axis
fig.colorbar(
    frame=['+l"Topography"', "y+lm"])

# colorbar in y-axis
# fig.colorbar(
#     position="JMR+o0.5c/0c+w7c/0.5c",
#     frame=["+ltopography", "y+lm"])


# plot stations
fig.plot(
    x=lon,
    y=lat,
    style='i0.1i',
    color='red',
    pen='black',
    label='station')
fig.legend()
fig.show()

file_save = file_path + "/" + title + '.png'
fig.savefig(file_save, crop=True, dpi=300, transparent=False)
