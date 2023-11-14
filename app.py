from pathlib import Path

import pandas as pd
import geoviews as gv

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Div, Select, RangeTool, HoverTool
from bokeh.plotting import figure, curdoc

from geoviews import dim

gv.extension('bokeh')
renderer = gv.renderer('bokeh')
renderer = renderer.instance(mode='server')

cities = pd.read_csv('data/cities.csv', encoding="ISO-8859-1")
population = gv.Dataset(cities, kdims=['Station Name', 'State', 'Year'])
points = population.to(gv.Points, ['Longitude', 'Latitude'], ['Total Days', 'Station Name', 'State'])

tiles = gv.tile_sources.OSM

layout = tiles * points.opts(
    color='Total Days', cmap='viridis', size=dim('Total Days')*0.5,
    tools=['hover'], global_extent=False, width=800, height=600)

desc = Div(text=(Path(__file__).parent / "description.html").read_text("utf8"), sizing_mode="stretch_width",
           margin=(2, 2, 2, 15))

curdoc().add_root(column(desc))

doc = renderer.server_doc(layout)
doc.title = 'GeoViews App'
