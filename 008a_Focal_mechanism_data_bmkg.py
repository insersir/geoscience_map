import pygmt
import pandas as pd

# 1. Read Data
data = pd.read_excel(r"D:\training_pygmt\data\List_FM_Juni_2021-mod.xlsx")                  # change this
data = data[10:20].reset_index(drop=True)
# print(data)

# 2. save figure
title = 'focal_mechanism_data_bmkg'
file_path = r"D:\training_pygmt\saveplot"                                                   # change this


# Don't modify the lines below ###################################
data.loc[data["Dir_Lat"] == 'S', "Lat"] = data['Lat']*-1
data.loc[data["Dir_Long"] == 'W', "Long"] = data['Long']*-1
# print(data)


# 3. Meca method used is 'aki'
data = data[['Long', 'Lat', 'Depth_km', 'strike1', 'dip1', 'slip1', 'Mag']]
# print(data)

# In CSV or Excel format, we need to rename the header.
data = data.rename(columns={'Long': 'longitude',
                            'Lat': 'latitude',
                            'Depth_km': 'depth',
                            'strike1': 'strike',
                            'dip1': 'dip',
                            'slip1': 'rake',
                            'Mag': 'magnitude'})
# print(data)


# 4. Plot focal mechanism
fig = pygmt.Figure()

# region = [np.min(data.longitude)-5,
#           np.max(data.longitude)+5,
#           np.min(data.latitude)-5,
#           np.max(data.latitude)+5]

fig.coast(
    region="ID",
    projection="M14i",
    land="grey",
    water="lightblue",
    shorelines=True)

fig.meca(
    spec=data,
    convention='aki',
    scale="1.0c",
    offset=False,
    frame=True)
fig.show()


# 5. Plot focal mechanism with color depth
fig = pygmt.Figure()
fig.coast(
    region="ID",
    projection="M14i",
    land="grey",
    water="lightblue",
    shorelines=True)

pygmt.makecpt(cmap='jet',
              series=[min(data.depth)-5, max(data.depth)+5, 5], continuous=True)

fig.meca(
    spec=data,
    convention='aki',
    scale="1.0c",
    offset=False,
    frame=True,
    C=True)

fig.colorbar(
    position="JMB-o0.5c/0c+w12c/0.6c",
    frame=["+lDepth", "y+lkm"])

# fig.colorbar(
#     position="JMR+o0.5c/0c+w7c/0.6c",
#     frame=["+lDepth", "y+lkm"])
fig.show()

file_save = file_path + "/" + title + '.png'
fig.savefig(file_save, crop=True, dpi=300, transparent=False)
