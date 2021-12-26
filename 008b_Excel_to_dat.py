import pandas as pd

# 1. Read Data
data = pd.read_excel(r"D:\training_pygmt\data\List_FM_Juni_2021-mod.xlsx")
data = data[10:20].reset_index(drop=True)

# 2. Save to .dat
path_save = r"D:\training_pygmt\data" + "/" + "data_bmkg_offset.dat"                                 # change this

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
print('Longitude_ori:', data.longitude.values.tolist())
print('Latitude_ori:', data.latitude.values.tolist())

# Input plot_longitude and plot_latitude to avoid overlapping
plot_longitude = [121.68, 104, 100.03, 95.9, 123, 125.54, 102.33, 129.54, 126.09, 129.46]
plot_latitude = [0.46, -5.5, -0.05, 3.93, -2, 1.36, -4.33, -2, -0.39, -5]

# 4. Save to dat
data.insert(7, "plot_longitude", plot_longitude)
data.insert(8, "plot_latitude", plot_latitude)

save = data.to_csv(path_save, sep=' ', index=False, header=False)
