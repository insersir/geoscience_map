import numpy as np
import pandas as pd
from pykrige.ok import OrdinaryKriging
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Path, PathPatch

df = pd.read_excel(r"D:\test\crustal_thickness.xlsx")

lons = np.array(df['Longitude'])
lats = np.array(df['Latitude'])
data = np.array(df['H'])


grid_space = 0.01
grid_lon = np.arange(np.amin(lons), np.amax(lons), grid_space) # grid_space is the desired delta/step of the output array
grid_lat = np.arange(np.amin(lats)-0.1, np.amax(lats), grid_space)

OK = OrdinaryKriging(lons, lats, data, variogram_model='gaussian', verbose=False, enable_plotting=False, nlags=20)
z1, ss1 = OK.execute('grid', grid_lon, grid_lat)

xintrp, yintrp = np.meshgrid(grid_lon, grid_lat)
fig, ax = plt.subplots(figsize=(10, 10))
m = Basemap(llcrnrlon=np.min(lons)-0.5, llcrnrlat=np.min(lats)-0.5,
            urcrnrlon=np.max(lons)+0.5, urcrnrlat=np.max(lats)+0.5,
            projection='merc', resolution='h', area_thresh=1000., ax=ax)
# m.etopo()
m.drawcoastlines()          # draw coastlines on the map
x, y = m(xintrp, yintrp)     # convert the coordinates into the map scales
ln, lt = m(lons, lats)
cs = ax.contourf(x, y, z1, np.linspace(25, 40, 100), extend='both', cmap='magma')  # plot the data on the map.
cbar = m.colorbar(cs, location='right', pad="5%", label='Depth (km)')   # plot the colorbar on the map

# draw parallels.
parallels = np.arange(-9, -6., 1)
m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=14, linewidth=1)  # Draw the latitude labels on the map

# draw meridians
meridians = np.arange(80., 120., 1)
m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=14, linewidth=1)
# plt.show()

# getting the limits of the map:
x0, x1 = ax.get_xlim()
y0, y1 = ax.get_ylim()
map_edges = np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]])
# getting all polygons used to draw the coastlines of the map
polys = [p.boundary for p in m.landpolygons]

# combining with map edges
polys = [map_edges]+polys[:]

# creating a PathPatch
codes = [[Path.MOVETO]+[Path.LINETO for p in p[1:]] for p in polys]
polys_lin = [v for p in polys for v in p]
codes_lin = [xx for cs in codes for xx in cs]
path = Path(polys_lin, codes_lin)
patch = PathPatch(path, facecolor='white', lw=0)

# masking the data outside the inland of Taiwan
ax.add_patch(patch)
plt.show()
