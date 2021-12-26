import pygmt

title = 'Global_map'
file_path = r"D:\training_pygmt\saveplot"                               # change this

fig = pygmt.Figure()
fig.coast(
    region='g',
    projection='R120/8i',
    shorelines=True,
    water='lightblue',
    land='grey',
    frame='ag',
    borders="1/0.5p,black")
fig.show()

file_save = file_path + "/" + title + '.png'
fig.savefig(file_save)
