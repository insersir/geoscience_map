import pygmt

region = [95, 105, -10, 6]      # long_min, long_max, lat_min, lat_max

title = 'exercise1'
file_path = r"D:\training_pygmt\saveplot"                   # change this

fig = pygmt.Figure()
fig.coast(
    region=region,
    projection='M8i',
    shorelines=True,
    water='grey',
    land='white',
    frame='ag')
fig.show()

file_save = file_path + "/" + title + '.pdf'
fig.savefig(file_save)
