import ipyleaflet
import ipywidgets
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, Point
import datetime
import requests
import xml.etree.ElementTree as ET
import calendar

class ANA_interactive_map:

    def __init__(self, path_inventario):
        self.df = pd.read_csv(path_inventario, engine='python', sep='\t', delimiter=';', parse_dates=['UltimaAtualizacao'])
        self.df[['Latitude', 'Longitude']] = self.df[['Latitude', 'Longitude']].apply(lambda x: x.str.replace(',','.'))
        self.df['Latitude'] = self.df['Latitude'].astype('float')
        self.df['Longitude'] = self.df['Longitude'].astype('float')

    def date_location(_):
        self.heatmap_byLast.locations = [tuple(s) for s in self.df.loc[df['UltimaAtualizacao'] > self.date_slider.value, ['Latitude','Longitude']].to_numpy()]

    def handle_draw(self,  action,geo_json):
        self.feature_collection['features'].append(geo_json)

    def controls_on_Map(self):
        control_layer = ipyleaflet.LayersControl(position='topright')
        self.m01.add_control(control_layer)

        control_fullscreen = ipyleaflet.FullScreenControl()
        self.m01.add_control(control_fullscreen)

        control_draw = ipyleaflet.DrawControl()
        self.feature_collection = {'type': 'FeatureCollection', 'features': []}
        control_draw.on_draw(self.handle_draw)
        self.m01.add_control(control_draw)

        control_scale = ipyleaflet.ScaleControl(position='bottomleft')
        self.m01.add_control(control_scale)

        slider_heatmap_radius = ipywidgets.IntSlider(description='Radius', min=1, max=50, value=15)
        ipywidgets.jslink((slider_heatmap_radius, 'value'),(self.heatmap_all,'radius'))
        widget_control01 = ipyleaflet.WidgetControl(widget=slider_heatmap_radius, position='bottomright')
        self.m01.add_control(widget_control01)

        self.date_slider = ipywidgets.SelectionSlider(options=pd.date_range(start='2000-01-01',end='2020-01-01', freq='M').to_numpy())
        self.date_slider.observe(self.date_location, names='value')
        ipywidgets.jslink((slider_heatmap_radius, 'value'), (self.heatmap_byLast,'radius'))
        widget_control02 = ipyleaflet.WidgetControl(widget=self.date_slider, position='topright')
        self.m01.add_control(widget_control02)

    def layer(self):
        self.heatmap_all = ipyleaflet.Heatmap(locations=[tuple(r) for r in self.df[['Latitude', 'Longitude']].to_numpy()],radius=30, name='All point Heatmap')
        self.m01.add_layer(self.heatmap_all)

        self.heatmap_byLast = ipyleaflet.Heatmap(locations=[tuple(r) for r in self.df[['Latitude', 'Longitude']].to_numpy()],radius=30, name='By Date')
        self.m01.add_layer(self.heatmap_byLast)



    def map(self):
        self.m01 = ipyleaflet.Map(zoom=2)
        self.layer()
        self.controls_on_Map()
        display(self.m01)
