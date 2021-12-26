import pygmt
import numpy as np

# 1. Read Data
file = r"D:\training_pygmt\data\data_bmkg_offset.dat"                                        # change this

# 2. save figure
title = 'focal_mechanism_data_bmkg_offset'
file_path = r"D:\training_pygmt\saveplot"                                                   # change this


# Don't modify the lines below ###################################
data = np.loadtxt(file)
depth = data[:, 2]

# plot focal mechanism
fig = pygmt.Figure()
fig.coast(
    region="ID",
    projection="M14i",
    land="grey",
    water="lightblue",
    shorelines=True)

pygmt.makecpt(cmap='jet',
              series=[np.min(depth)-5, np.max(depth)+5, 5], continuous=True)

fig.meca(
    spec=file,
    convention='aki',
    scale="1.0c",
    offset="+s0.2",
    frame=True,
    C=True)

fig.colorbar(
    position="JMB-o0.5c/0c+w12c/0.6c",
    frame=["+lDepth", "y+lkm"])
fig.show()

file_save = file_path + "/" + title + '.png'
fig.savefig(file_save, crop=True, dpi=300, transparent=False)
