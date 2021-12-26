import pygmt
import numpy as np
from obspy.geodetics import locations2degrees

# 1. Read data
data = r"D:\training_pygmt\data\Cross-section\earthquakes.dat"                                   # change this

# 2. Save figure
title = 'Cross-section'
file_path = r"D:\training_pygmt\saveplot"                                                        # change this

# 3. Save the cross-section to .dat
save_cross_sect = r"D:\training_pygmt\data\Cross-section" + "/" + "slice.dat"                    # change this


#
# Don't modify the lines below ###################################
fig = pygmt.Figure()
fig.coast(
    region=[95, 110, -10, 5],                                                                    # change this
    projection="M6i",
    frame=["xa2g2", "ya2g2"],
    land="lightbrown",
    shorelines="0.25p")
fig.show()


# 3. Plot events and the slicing line
# plot events
pygmt.makecpt(cmap="red,green,blue,black", series=[0, 160, 5], continuous=True)                 # depth's colorbar
fig.plot(data=data, pen="faint", style="c0.35", cmap=True)
fig.colorbar(frame='+l"Depth (km)"')

# plot the slicing line
cross_sect = [100, 106, -3, -6]    # [x1, x2, y1, y2]                                           # change this

fig.plot(x=[cross_sect[0], cross_sect[1]], y=[cross_sect[2], cross_sect[3]],
         projection="M", pen=2)   # membuat garis penampang

fig.text(x=99.5, y=-3, text="A", font="15,Helvetica")       # make text "A"                     # change this
fig.text(x=106.5, y=-6.2, text="B", font="15,Helvetica")    # make text "B"                     # change this
fig.show()


# 4. Plot cross-section
pygmt.project(
    data=data,
    unit=True,              # True, convert the distance from degree to km
    center=[cross_sect[0], cross_sect[2]],
    endpoint=[cross_sect[1], cross_sect[3]],
    convention="pz",
    width=[-50, 50],     # width: lebar proyeksi yang sehingga akan mempengaruhi jumlah data [kiri, kanan]
    outfile=save_cross_sect)

data_cross = np.loadtxt(save_cross_sect)
y = data_cross[:, 1]        # take all data from column depth

dist_max = (locations2degrees(cross_sect[2], cross_sect[0], cross_sect[3], cross_sect[1]))*111.1
depth_max = np.max(y)

fig.basemap(
    projection="X15c/-6c",    # basemap with length = 15 cm and wide= 6cm
    region=[0, dist_max+50, 0, depth_max+50],
    frame=['xafg200+l"Distance (km)"', 'yafg50+l"Depth (km)"', "WSen"],
    yshift=-9)

fig.plot(data=save_cross_sect, projection="X", style="c0.25", pen=0.5, color='red')
fig.text(x=15, y=10, text="A", font="13,Helvetica")
fig.text(x=dist_max+35, y=10, text="B", font="13,Helvetica")
fig.show()

file_save = file_path + "/" + title + '.png'
fig.savefig(file_save, crop=True, dpi=300, transparent=False)
