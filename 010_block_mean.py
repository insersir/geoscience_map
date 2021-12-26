import pygmt
import pandas as pd
import numpy as np

# 1. Read Data Excel
data = pd.read_excel(r"D:\training_pygmt\data\catalog_earthquakes_Indonesia.xlsx")                # change this
# print(data)

# 2. Save figure
title = 'Block-mean'
file_path = r"D:\training_pygmt\saveplot"                                                        # change this

# 3. Define spacing in x and y direction (150 by 150 minute blocks)
spacing = "150m"

# Don't modify the lines below ###################################
# 4. Select only needed columns
data = data[["lon", "lat", "depth_km"]]

region = [np.min(data.lon)-5,
          np.max(data.lon)+5,
          np.min(data.lat)-5,
          np.max(data.lat)+5]

fig = pygmt.Figure()

# 5. Calculate mean depth in km from all events within 150x150 minute
# bins using blockmean
df = pygmt.blockmean(data=data, region=region, spacing=spacing)
# convert to grid
grd = pygmt.xyz2grd(data=df, region=region, spacing=spacing)

fig.grdimage(
    grid=grd,
    region=region,
    frame=["af", '+t"Mean earthquake depth inside each block"'],
    cmap="batlow", projection='M8i')

# plot slightly transparent landmasses on top
fig.coast(land="darkgray", transparency=40)
# plot original data points
fig.plot(x=data.lon, y=data.lat, style="c0.3c", color="white", pen="1p,black")
fig.colorbar(frame=["x+lkm"])

fig.shift_origin(xshift="w+5c")
fig.show()

file_save = file_path + "/" + title + '.png'
fig.savefig(file_save, crop=True, dpi=300, transparent=False)
