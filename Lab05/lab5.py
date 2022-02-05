import argparse
from bokeh.plotting import figure, row
from bokeh.models import Select, ColumnDataSource
from bokeh.layouts import layout
from bokeh.io import curdoc
import pandas as pd

parser = argparse.ArgumentParser(description="This script plots data using Bokeh library")
args = parser.parse_args()

df1 = pd.read_table('./data/3w1sym_255_0.txt', names=['y', 'x', 'z', 'I'], decimal=',')
df2 = pd.read_table('./data/3w1sym_200_0.txt', names=['y', 'x', 'z', 'I'], decimal='.')
df3 = pd.read_table('./data/3w1sym_185_0.txt', names=['y', 'x', 'z', 'I'], decimal='.')

d1 = {'x': df1['x']-31, 'y': df1['I']*10**6}
d2 = {'x': df2['x']-31, 'y': df2['I']*10**6}
d3 = {'x': df3['x']-31, 'y': df3['I']*10**6}

source = ColumnDataSource(data=d1)

fig = figure(x_range=[-35, 35], y_range=[0, 600])
fig.line('x', 'y', source=source, line_width=2)
fig.xaxis.axis_label = "x [mm]"
fig.yaxis.axis_label = "Intensity [arb. unit]"
fig.axis.axis_label_text_font_style = "bold"
fig.title = "Data for 3w1sym_255"

select = Select(value='3w1sym_255', title='Structure', options=['3w1sym_255', '3w1sym_200', '3w1sym_185'])


def update_dataset(attr, old, new):
    df = select.value
    fig.title.text = f"Data for {df}"
    if df == '3w1sym_255':
        source.data = d1
    if df == '3w1sym_200':
        source.data = d2
    if df == '3w1sym_185':
        source.data = d3


select.on_change('value', update_dataset)

lay = layout(row(fig, select))
curdoc().add_root(lay)
