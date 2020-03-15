import ipyleaflet
import ipywidgets
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, Point
import datetime
import requests
import xml.etree.ElementTree as ET
import calendar
import numpy as np
import pathlib


class ANA_interactive_map:

    def __init__(self, path_inventario):
        self.df = pd.read_csv(path_inventario, engine='python', sep='\t', delimiter=';', parse_dates=['UltimaAtualizacao'])
        self.df[['Latitude', 'Longitude']] = self.df[['Latitude', 'Longitude']].apply(lambda x: x.str.replace(',','.'))
        self.df['Latitude'] = self.df['Latitude'].astype('float')
        self.df['Longitude'] = self.df['Longitude'].astype('float')

        self.gdf = gpd.GeoDataFrame(self.df, geometry=gpd.points_from_xy(self.df.Longitude, self.df.Latitude), crs='epsg:4674')

    def date_location(_):
        self.heatmap_byLast.locations = [tuple(s) for s in self.df.loc[df['UltimaAtualizacao'] > self.date_slider.value, ['Latitude','Longitude']].to_numpy()]

    def handle_draw(self, action,geo_json):
        self.feature_collection['features'].append(geo_json)

    def download_ANA_stations(self, list_codes, typeData, folder_toDownload):

        path_folder = pathlib.Path(folder_toDownload)
        for station in list_codes:
            params = {'codEstacao': station, 'dataInicio': '', 'dataFim': '', 'tipoDados': '{}'.format(typeData), 'nivelConsistencia': ''}
            response = requests.get('http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroSerieHistorica', params)

            tree = ET.ElementTree(ET.fromstring(response.content))

            root = tree.getroot()

            list_data = []
            list_consistenciaF = []
            list_month_dates = []
            for i in root.iter('SerieHistorica'):
                codigo = i.find("EstacaoCodigo").text
                consistencia = i.find("NivelConsistencia").text
                date = i.find("DataHora").text
                date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                last_day = calendar.monthrange(date.year, date.month)[1]
                month_dates = [date + datetime.timedelta(days=i) for i in range(last_day)]
                data = []
                list_consistencia = []
                for day in range(last_day):
                    if params['tipoDados'] == '3':
                        value = 'Vazao{:02}'.format(day+1)
                        try:
                            data.append(float(i.find(value).text))
                            list_consitencia.append(int(consistencia))
                        except TypeError:
                            data.append(i.find(value).text)
                            list_consistencia.append(int(consistencia))
                        except AttributeError:
                            data.append(None)
                            list_consistencia.append(int(consistencia))
                    if params['tipoDados'] == '2'
                        value = 'Chuva{:02}'.format(day+1)
                        try:
                            data.append(float(i.find(value).text))
                            list_consistencia.append(consistencia)
                        except TypeError:
                            data.append(i.find(value).text)
                            list_consistencia.append(consistencia)
                        except AttributeError:
                            data.append(None)
                            list_consistencia.append(consistencia)
                list_data = list_data + data
                list_consistenciaF = list_consistenciaF + list_consistencia
                list_month_dates = list_month_dates + month_dates

            if len(list_data) > 0:
                df = pd.DataFrame({'Date': list_month_dates, 'Consistence': list_consistenciaF, 'Data': list_data})
                filename = '{}_{}.csv'.format(typeData, station)
                df.to_csv(path_folder/filename)
            else:
                pass

    def download_buttom(_):
        try:
            last_draw = self.feature_collection['features'][-1]['geometry']
            last_polygon = Polygon([(i[0], i[1]) for i in last_draw['coordinates'][0]])
        except:
            pass

        if self.control_choiceDownload.value == 'Rain':
            option = 2
        if self.control_choiceDownload.value == 'Flow':
            option = 3

        if self.control_selectDownload.value == 'All':
            code_list = self.gdf.loc[gdf['geometry'].within(last_polygon), 'Codigo'].to_list()
            self.download_ANA_stations(list_codes=code_list, typeData=option, folder_toDownload=self.control_pathDownload.value)

        elif self.control_selectDownload.value == 'byDate':
            code_list = self.gdf.loc[(self.gdf['geometry'].within(last_polygon)) & (self.gdf['UltimaAtualizacao']>self.date_slider.value), 'Codigo'].to_list()
            self.download_ANA_stations(list_codes=code_list, typeData=option, folder_toDownload=self.control_pathDownload.value)

        elif self.control_selectDownload.value == 'Watershed':
            for i in shape['geometry']:
                code_list = self.gdf.loc[self.gdf['geometry'].within(i), 'Codigo'].to_list()
                self.download_ANA_stations(list_codes, typeData=a, folder_toDownload=self.control_pathDownload.value)


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

        control_selectDownload = ipywidgets.Dropdown(options=['Watershed', 'All', 'byDate'])
        self.control_pathDownload = ipywidgets.Text(placeholder='Write your PATH to Download HERE.')
        control_buttonDownload = ipywidgets.Button(description='Download')
        control_choiceDownload = ipywidgets.RadioButtons(options=['Rain', 'Flow'])
        # control_progressDownload = ipywidgets.IntProgress()
        control_buttonDownload.on_click(self.download_buttom)


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
