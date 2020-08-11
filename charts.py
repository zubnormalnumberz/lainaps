import pandas as pd
import numpy as np
from bokeh.layouts import column, row
from bokeh.plotting import show
from bokeh.models import Select, HoverTool, ColumnDataSource, Slider
from bokeh.palettes import Spectral5
from bokeh.plotting import curdoc, figure

df = pd.read_csv("BAS_2015_advanced.csv", decimal=",")

SIZES = list(range(6, 22, 3))
COLORS = Spectral5
N_SIZES = len(SIZES)
N_COLORS = len(COLORS)

columns = sorted(df.columns)
discrete = [x for x in columns if df[x].dtype == object]
continuous = [x for x in columns if x not in discrete]

def create_figure():

    current = df[(df['minutes'] >= minutes.value)].dropna()

    xs = current[x.value].values
    ys = current[y.value].values

    list_len = len(xs)
    names = current.players.values
    minutuak = current.minutes.values

    x_title = x.value.title()
    y_title = y.value.title()

    kw = dict()
    if x.value in discrete:
        kw['x_range'] = sorted(set(xs))
    if y.value in discrete:
        kw['y_range'] = sorted(set(ys))
    kw['title'] = "%s vs %s" % (x_title, y_title)

    p = figure(plot_height=600, plot_width=800, tools='pan,box_zoom, wheel_zoom, reset, save', **kw)
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title

    if x.value in discrete:
        p.xaxis.major_label_orientation = pd.np.pi / 4

    sz = 9
    if size.value != 'None':
        if len(set(current[size.value])) > N_SIZES:
            groups = pd.qcut(current[size.value].values, N_SIZES, duplicates='drop')
        else:
            groups = pd.Categorical(current[size.value])
        l_sz = [SIZES[xx] for xx in groups.codes]
    else:
        l_sz = [sz]*list_len

    c = "#31AADE"
    if color.value != 'None':
        if len(set(current[color.value])) > N_COLORS:
            groups = pd.qcut(current[color.value].values, N_COLORS, duplicates='drop')
        else:
            groups = pd.Categorical(current[color.value])
        l_c = [COLORS[xx] for xx in groups.codes]
    else:
        l_c = [c]*list_len

    source = ColumnDataSource(dict(mpg = xs, hp = ys, kolor = l_c, tam = l_sz, players = names, minutes = minutuak))

    p.circle(x = 'mpg', y = 'hp', size = 'tam', color = 'kolor', line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5, source=source)
    p.add_tools(HoverTool(tooltips = [ (x_title, "@mpg"), (y_title, "@hp"), ("Players", "@players"), ("Minutes", "@minutes") ]))

    return p

def update(attr, old, new):
    layout.children[1] = create_figure()

x = Select(title='X-Axis', value='offrat', options=columns)
x.on_change('value', update)

y = Select(title='Y-Axis', value='defrat', options=columns)
y.on_change('value', update)

size = Select(title='Size', value='None', options=['None'] + continuous)
size.on_change('value', update)

color = Select(title='Color', value='None', options=['None'] + continuous)
color.on_change('value', update)

minutes = Slider(start=0, end=200, value=0, step=1, title="Minutes")
minutes.on_change('value', update)

controls = column(x, y, color, size, minutes, width=200)
layout = row(controls, create_figure())

curdoc().add_root(layout)
curdoc().title = "Crossfilter"
