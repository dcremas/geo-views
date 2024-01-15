from pathlib import Path

import pandas as pd
import geoviews as gv

from bokeh.io import show
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, DataTable, DateFormatter, TableColumn, Div, Button, CustomJS
from bokeh.plotting import figure, curdoc

from geoviews import dim

gv.extension('bokeh')
renderer = gv.renderer('bokeh')
renderer = renderer.instance(mode='server')

desc = Div(text=(Path(__file__).parent / "description.html").read_text("utf8"), sizing_mode="stretch_width",
           margin=(5, 25, 5, 25))

cities = pd.read_csv('data/cities.csv', encoding="ISO-8859-1")
population = gv.Dataset(cities, kdims=['Station Name', 'State', 'Year'])
points = population.to(gv.Points, ['Longitude', 'Latitude'], ['Total Days', 'Station Name', 'State'])

tiles = gv.tile_sources.OSM

title = "US Cities: Significant Decreases In Hourly Barometric Pressure Bubble Map"

layout = tiles * points.opts(title=title, color='Total Days',
                             cmap='viridis', size=dim('Total Days')*0.5,
                             tools=['hover'], global_extent=False,
                             width=800, height=600)

source = ColumnDataSource(cities)

columns = [
        TableColumn(field="Station Name", title="Station Name"),
        TableColumn(field="State", title="State"),
        TableColumn(field="Latitude", title="Latitude"),
        TableColumn(field="Longitude", title="Longitude"),
        TableColumn(field="Year", title="Year"),
        TableColumn(field="Total Days", title="Total Days"),
    ]

data_table = DataTable(source=source, columns=columns, width=800, height=600,
                       margin=(5, 25, 25, 25))

hyperlink_div = Div(
    text="""<a href="https://dataviz.dustincremascoli.com">Go back to Data Visualizations Main Page</a>""",
    width=400, height=25,
    margin=(10, 10, 10, 25)
    )

button = Button(label="Click to Download data to a .csv file",
                button_type="success",
                margin=(5, 25, 25, 25))

button.js_on_event(
    "button_click",
    CustomJS(
        args=dict(source=source),
        code=(Path(__file__).parent / "download.js").read_text("utf8"),
    ),
)

curdoc().add_root(column(desc, hyperlink_div))

doc = renderer.server_doc(layout)
doc.title = 'GeoViews App'

curdoc().add_root(column(button, data_table))
