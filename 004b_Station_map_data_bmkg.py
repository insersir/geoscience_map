import pygmt
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Read Data
data = pd.read_excel(r"D:\training_pygmt\data\List Stasiun Gabungan_Tahun_Instalasi_160521_rev6.xlsx")   # change this

# 2. save figure
title = 'Station_map_data_bmkg'
file_path = r"D:\training_pygmt\saveplot"                                                              # change this


# 3. Grouping by "SISTEM"
plt.figure(figsize=(15, 5))
group = data.groupby(['SISTEM']).size()
splot = sns.barplot(x=group.index, y=group.values)
for p in splot.patches:
    splot.annotate(format(p.get_height(), '.0f'),
                   (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha='center', va='center',
                   size=11,
                   xytext=(0, 3.5),
                   textcoords='offset points')
plt.grid()
plt.ylabel('Total')
plt.show()


# 4. Grouping by "Asesmen Kualitas"
group = data.groupby(['ASESMEN KUALITAS']).size()
splot = sns.barplot(x=group.index, y=group.values)
for p in splot.patches:
    splot.annotate(format(p.get_height(), '.0f'),
                   (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha='center', va='center',
                   size=12,
                   xytext=(0, 3.5),
                   textcoords='offset points')
plt.grid()
plt.ylabel('Total')
plt.show()


# 5. Plot the stations by "SISTEM"
data.SISTEM = data.SISTEM.astype(dtype="category")

region = pygmt.info(
    data=data[["LNG", "LAT"]],
    per_column=True, spacing=(8, 8))

sistem_list = []
grouped = data.groupby('SISTEM')
for name_of_the_group, group in grouped:
    sistem_list.append(name_of_the_group)
# print(sistem_list)

fig = pygmt.Figure()
fig.coast(
    region=region,
    projection='M10i',
    shorelines=True,
    water='lightblue',
    land='grey',
    frame='a')

new_sistem_list = ','.join(sistem_list)
cmod = str("+c" + new_sistem_list)

pygmt.makecpt(cmap="cyclic", series=(0, 8, 1),
              color_model=cmod)

fig.plot(x=data.LNG, y=data.LAT,
         color=data.SISTEM.cat.codes.astype(int), cmap=True,
         style="i0.1i",
         transparency=0)
fig.colorbar()

with fig.inset(position="jBL+w4.5c+o0.2c/0.2c", margin=0, box="+p1,black"):
    fig.coast(
        region="g",
        projection="G110/-20/4.5c",
        land="gray", water="white",
        dcw='ID+gred')
fig.show()


# 6. Plot the stations without categorization
lon = data.LNG
lat = data.LAT
sta = data.KODE

# regions = [np.min(lon)-5, np.max(lon)+5, np.min(lat)-5, np.max(lat)+5]
regions = [90, 100, -5, 5]

fig = pygmt.Figure()
fig.coast(
    region=regions,
    projection='M10i',
    shorelines=True,
    water='lightblue',
    land='grey',
    frame='a'
)

fig.plot(
    x=lon,
    y=lat,
    style='i0.1i',
    color='red',
    pen='black',
    label='station',
)
fig.legend()

with fig.inset(position="jBL+w4.5c+o0.2c/0.2c", margin=0, box="+p1,black"):
    fig.coast(
        region="g",
        projection="G110/-20/4.5c",
        land="gray", water="white",
        dcw='ID+gred')

file_save = file_path + "/" + title + '.png'
fig.savefig(file_save)
fig.show()
