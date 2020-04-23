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
import os

class ANA_interactive_map:


    def __init__(self, path_inventario):
        print('teste')
        self.df = pd.read_csv(path_inventario, engine='python', sep='\t', delimiter=';', parse_dates=['UltimaAtualizacao'])
        self.df[['Latitude', 'Longitude']] = self.df[['Latitude', 'Longitude']].apply(lambda x: x.str.replace(',','.'))
        self.df['Latitude'] = self.df['Latitude'].astype('float')
        self.df['Longitude'] = self.df['Longitude'].astype('float')

        self.gdf = gpd.GeoDataFrame(self.df, geometry=gpd.points_from_xy(self.df.Longitude, self.df.Latitude), crs='epsg:4674')

        self.m01 = ipyleaflet.Map(zoom=2, center=(-16, -47))
        self.layer()
        self.controls_on_Map()
        self.button_download.on_click(self._download_button01)
        self.button_ViewShapefile.on_click(self._shapefile_buttom)

        self.out01 = ipywidgets.Output()


        display(ipywidgets.VBox([self.m01,
                                 self.out01]))


    def _selection_observe_01(self, *args):
        self.heatmap_byLast.locations = [tuple(s) for s in self.df.loc[self.df['UltimaAtualizacao'] > self.selectionSlider_date01.value, ['Latitude','Longitude']].to_numpy()]


    def download_ANA_stations(self, list_codes, typeData, folder_toDownload):
        numberOfcodes = len(list_codes)
        count = 0
        path_folder = pathlib.Path(folder_toDownload)
        self.floatProgress_loadingDownload.bar_style = 'info'

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
                            list_consistencia.append(int(consistencia))
                        except TypeError:
                            data.append(i.find(value).text)
                            list_consistencia.append(int(consistencia))
                        except AttributeError:
                            data.append(None)
                            list_consistencia.append(int(consistencia))
                    if params['tipoDados'] == '2':
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
                df.to_csv(path_folder / filename)
                count += 1
                self.floatProgress_loadingDownload.value = float(count+1)/numberOfcodes
            else:
                count += 1
                self.floatProgress_loadingDownload.value = float(count+1)/numberOfcodes

        self.floatProgress_loadingDownload.bar_style = 'success'
                # pass

    def _download_button01(self, *args):
        try:
            # last_draw = self.feature_collection['features'][-1]['geometry']
            last_draw = self.draw_control.last_draw['geometry']
            last_polygon = Polygon([(i[0], i[1]) for i in last_draw['coordinates'][0]])
        except:
            pass

        if self.radioButton_typeDownload.value == 'Rain':
            option = 2
        if self.radioButton_typeDownload.value == 'Flow':
            option = 3

        if self.dropdown_typeDownload.value == 'All':
            code_list = self.gdf.loc[self.gdf['geometry'].within(last_polygon), 'Codigo'].to_list()

            self.download_ANA_stations(list_codes=code_list, typeData=option, folder_toDownload=self.text_pathDownload.value)

        elif self.dropdown_typeDownload.value == 'byDate':
            code_list = self.gdf.loc[(self.gdf['geometry'].within(last_polygon)) & (self.gdf['UltimaAtualizacao']>self.selectionSlider_date01.value), 'Codigo'].to_list()
            self.download_ANA_stations(list_codes=code_list, typeData=option, folder_toDownload=self.text_pathDownload.value)

        elif self.dropdown_typeDownload.value == 'Watershed':
            for i in self.shape['geometry']:
                code_list = self.gdf.loc[self.gdf['geometry'].within(i), 'Codigo'].to_list()
                self.download_ANA_stations(list_codes=code_list, typeData=option, folder_toDownload=self.text_pathDownload.value)

    def _dropdown_observe_01(self, *args):
        if self.dropdown_typeDownload.value == 'Watershed':
            self.control_shapefileText = ipywidgets.Text(placeholder='Insert Shapefile PATH HERE')

            hbox_shape = ipywidgets.HBox([self.control_shapefileText, self.button_ViewShapefile])
            widget_control04 = ipyleaflet.WidgetControl(widget=hbox_shape, position='bottomright')
            self.m01.add_control(widget_control04)

        else:
            try:
                self.control_shapefileText.close()
                self.button_ViewShapefile.close()
                self.m01.remove_control(widget_control04)
                self.m01.remove_layer(self.geo_data)
            except:
                pass

    def _shapefile_buttom(self, *args):
        if self.dropdown_typeDownload.value == 'Watershed':
            try:
                self.shape = gpd.read_file(self.control_shapefileText.value)
                self.geo_data = ipyleaflet.GeoData(geo_dataframe=self.shape, name='Bacias',style={'color': 'red', 'fillColor': '#c51b8a', 'opacity':0.05, 'weight':1.9, 'dashArray':'2', 'fillOpacity':0.6},
                               hover_style={'fillColor': 'red', 'fillOpacity': 0.2})
                self.m01.add_layer(self.geo_data)
            except:
                pass
        else:
            try:
                # self.m01.remove_layer(geo_data)
                pass
            except:
                pass

    def controls_on_Map(self):
        layer_control = ipyleaflet.LayersControl(position='topright')
        self.m01.add_control(layer_control)

        fullscreen_control = ipyleaflet.FullScreenControl()
        self.m01.add_control(fullscreen_control)

        self.draw_control = ipyleaflet.DrawControl()
        self.m01.add_control(self.draw_control)

        scale_control = ipyleaflet.ScaleControl(position='bottomleft')
        self.m01.add_control(scale_control)

        intSlider_01 = ipywidgets.IntSlider(description='Radius', min=1, max=50, value=15)
        ipywidgets.jslink((intSlider_01, 'value'),(self.heatmap_all,'radius'))
        widget_control01 = ipyleaflet.WidgetControl(widget=intSlider_01, position='bottomright')
        self.m01.add_control(widget_control01)

        self.selectionSlider_date01 = ipywidgets.SelectionSlider(options=pd.date_range(start='2000-01-01',end='2020-01-01', freq='M').to_numpy())
        self.selectionSlider_date01.observe(self._selection_observe_01, names='value')
        ipywidgets.jslink((intSlider_01, 'value'), (self.heatmap_byLast,'radius'))
        widget_control02 = ipyleaflet.WidgetControl(widget=self.selectionSlider_date01, position='topright')
        self.m01.add_control(widget_control02)

        self.dropdown_typeDownload = ipywidgets.Dropdown(options=['Watershed', 'All', 'byDate'], value=None, description='Select type:')
        self.dropdown_typeDownload.observe(self._dropdown_observe_01, names='value')
        self.dropdown_typeDownload.observe(self._shapefile_buttom, names='value')

        # box_layout = ipywidgets.Layout(display='flex', flex_flow='column', align_items='stretch', width='100%')

        self.text_pathDownload = ipywidgets.Text(placeholder='Write your PATH to Download HERE.')
        # vbox01 = ipywidgets.VBox([self.dropdown_typeDownload, self.text_pathDownload])
        self.button_download = ipywidgets.Button(description='Download')
        self.floatProgress_loadingDownload = ipywidgets.FloatProgress(min=0, max=1, value=0)

        self.radioButton_typeDownload = ipywidgets.RadioButtons(options=['Rain', 'Flow'], layout=ipywidgets.Layout(width='50%'))
        # hbox01 = ipywidgets.HBox([self.radioButton_typeDownload, self.button_download], layout=box_layout)
        #
        # vbox02 = ipywidgets.VBox([vbox01, hbox01, self.floatProgress_loadingDownload], layout=box_layout)


        # widget_control03 = ipyleaflet.WidgetControl(widget=vbox02, position='bottomright')
        widget_control03 = ipyleaflet.WidgetControl(widget=ipywidgets.VBox([ipywidgets.VBox([self.dropdown_typeDownload,
                                                                                             self.text_pathDownload]),
                                                                            ipywidgets.HBox([self.radioButton_typeDownload, self.button_download]),
                                                                            self.floatProgress_loadingDownload]), position='bottomright')
        self.m01.add_control(widget_control03)
        # control_progressDownload = ipywidgets.FloatProgress()
        self.button_ViewShapefile = ipywidgets.Button(description='View')


        # self.control_teste01 = ipywidgets.Gr

    def layer(self):
        self.heatmap_all = ipyleaflet.Heatmap(locations=[tuple(r) for r in self.df[['Latitude', 'Longitude']].to_numpy()],radius=30, name='All point Heatmap')
        self.m01.add_layer(self.heatmap_all)

        self.heatmap_byLast = ipyleaflet.Heatmap(locations=[tuple(r) for r in self.df[['Latitude', 'Longitude']].to_numpy()],radius=30, name='By Date')
        self.m01.add_layer(self.heatmap_byLast)

        # try:
        #     # path_shapefile = r'G:\Meu Drive\USP-SHS\Outros\Shapefile\Jaguaribe\Jaguaribe.shp'
        #     self.shape = gpd.read_file(self.control_shapefileText.value)
        #     geo_data = ipyleaflet.GeoData(geo_dataframe=self.shape, name='Bacias',style={'color': 'black', 'fillColor': '#3366cc', 'opacity':0.05, 'weight':1.9, 'dashArray':'2', 'fillOpacity':0.6},
        #                    hover_style={'fillColor': 'red' , 'fillOpacity': 0.2})
        #     self.m01.add_layer(geo_data)
        # except:
        #     pass

        # Layer too slow to used
        # marks = tuple([ipyleaflet.Marker(location=(lat, lon)) for lat, lon in self.df[['Latitude', 'Longitude']].to_numpy()])
        # marker_cluster = ipyleaflet.MarkerCluster(markers=marks)
        # self.m01.add_layer(marker_cluster)
