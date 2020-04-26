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


    def __init__(self):

        self.m01 = ipyleaflet.Map(zoom=3, center=(-16, -47), layout=ipywidgets.Layout(width='70%'))

        self.controls_on_Map()

        self.out01 = ipywidgets.Output()

        self.tabs = ipywidgets.Tab([self.tab00(), self.tab01(), self.tab02(), self.tab03()], layout=ipywidgets.Layout(width='30%'))
        self.tabs.set_title(0, 'Inventario')
        self.tabs.set_title(1, 'Download')
        self.tabs.set_title(2, 'View Tables')
        self.tabs.set_title(3, 'Stats')


        display(ipywidgets.VBox([ipywidgets.HBox([self.m01, self.tabs]),
                                 self.out01]))

    def controls_on_Map(self):
        # pass
        layer_control = ipyleaflet.LayersControl(position='topright')
        self.m01.add_control(layer_control)

        fullscreen_control = ipyleaflet.FullScreenControl()
        self.m01.add_control(fullscreen_control)

        self.draw_control = ipyleaflet.DrawControl()
        self.m01.add_control(self.draw_control)

        self.draw_control.observe(self._draw_testeObserve, 'last_draw')

        self.draw_control.observe(self._output_stats, 'last_draw')

        self.draw_control.observe(self._output_stats02, 'last_draw')

        scale_control = ipyleaflet.ScaleControl(position='bottomleft')
        self.m01.add_control(scale_control)



        # Layer too slow to used
        # marks = tuple([ipyleaflet.Marker(location=(lat, lon)) for lat, lon in self.df[['Latitude', 'Longitude']].to_numpy()])
        # marker_cluster = ipyleaflet.MarkerCluster(markers=marks)
        # self.m01.add_layer(marker_cluster)

    def tab00(self):
        with self.out01:
            # print('asdfasfsd')
            self.radioButton_typeInvetario = ipywidgets.RadioButtons(options=['Select Path', 'Get from API'], value=None)
            self.radioButton_typeInvetario.observe(self._radioButton_inventario, names='value')


            self.text_pathInvetario = ipywidgets.Text(placeholder='Insert path of the Inventario')
            self.button_pathInventario = ipywidgets.Button(description='Apply')
            self.button_pathInventario.on_click(self._button_pathinventario)


            self.button_showInventario = ipywidgets.Button(description='Show')
            self.button_showInventario.on_click(self._button_showInventario)

            self.floatProgress_loadingInventario = ipywidgets.FloatProgress(min=0, max=1, value=0, layout=ipywidgets.Layout(width='90%'))
            self.floatProgress_loadingInventario.bar_style = 'info'


            self.checkbox_intSliderRadius = ipywidgets.Checkbox(value=False, description='Radius Slider')
            self.checkbox_intSliderRadius.observe(self._checkbox_radius, 'value')

            self.checkbox_selectionDate = ipywidgets.Checkbox(value=False, description='Date Slider')
            self.checkbox_selectionDate.observe(self._checkbox_date, 'value')

            self.text_pathSaveInventario = ipywidgets.Text(placeholder='Insert path to Save Inventario')
            self.button_pathSaveInventario = ipywidgets.Button(description='Save')
            self.button_pathSaveInventario.on_click(self._button_saveInventario)

            self.text_pathInvetario.disabled = True
            self.button_pathInventario.disabled = True
            self.text_pathSaveInventario.disabled = True
            self.button_pathSaveInventario.disabled = True

        return ipywidgets.VBox([self.radioButton_typeInvetario,
                                ipywidgets.HBox([self.text_pathInvetario,self.button_pathInventario]),
                                self.button_showInventario,
                                self.floatProgress_loadingInventario,
                                self.checkbox_intSliderRadius,
                                self.checkbox_selectionDate,
                                ipywidgets.HBox([self.text_pathSaveInventario, self.button_pathSaveInventario])])

    def tab01(self):
        self.dropdown_typeDownload = ipywidgets.Dropdown(options=['Watershed', 'All', 'byDate'], value=None, description='Select type:', layout=ipywidgets.Layout(width='90%'))
        self.dropdown_typeDownload.observe(self._dropdown_observe_01, names='value')
        self.dropdown_typeDownload.observe(self._shapefile_buttom, names='value')

        self.text_pathShapefle = ipywidgets.Text(placeholder='Insert Shapefile PATH HERE')
        self.button_ViewShapefile = ipywidgets.Button(description='View', layout=ipywidgets.Layout(width='30%'))
        self.button_ViewShapefile.on_click(self._shapefile_buttom)

        self.text_pathShapefle.disabled = True
        self.button_ViewShapefile.disabled = True

        self.text_pathDownload = ipywidgets.Text(placeholder='Write your PATH to Download HERE.')

        self.button_download = ipywidgets.Button(description='Download', layout=ipywidgets.Layout(width='30%'))
        self.button_download.on_click(self._download_button01)

        self.floatProgress_loadingDownload = ipywidgets.FloatProgress(min=0, max=1, value=0, layout=ipywidgets.Layout(width='90%'))
        self.radioButton_typeDownload = ipywidgets.RadioButtons(options=['Rain', 'Flow'], layout=ipywidgets.Layout(width='30%'))


        return ipywidgets.VBox([ipywidgets.VBox([self.dropdown_typeDownload,
                                                 self.radioButton_typeDownload,
                                                 ipywidgets.HBox([self.text_pathShapefle,self.button_ViewShapefile])]),
                                ipywidgets.HBox([self.text_pathDownload, self.button_download]),
                                self.floatProgress_loadingDownload])

    def tab02(self):
        self.out02 = ipywidgets.Output()

        with self.out02:
            self.dropdown_typeView = ipywidgets.Dropdown(options=['Watershed', 'All', 'byDate'], value=None, description='Select type:', layout=ipywidgets.Layout(width='90%'))
            self.dropdown_typeView.observe(self._selectionMultiple_column, 'value')
            self.dropdown_typeView.observe(self._dropdown_observe_02, 'value')

            self.text_pathShapefile_02 = ipywidgets.Text(placeholder='Insert Shapefile')
            self.button_ViewShapefile_02 = ipywidgets.Button(description='View')
            self.button_ViewShapefile_02.on_click(self._shapefile_buttom_02)
            self.button_ViewShapefile_02.on_click(self._shapefile_buttom_03)

            self.selectionMultiple_df_01 = ipywidgets.SelectMultiple(description='Columns:')
            self.selectionMultiple_df_01.observe(self._selectionMultiple_column, 'value')

            self.selectionSlider_date02 = ipywidgets.SelectionSlider(options=pd.date_range(start='2000-01-01',end='2020-01-01', freq='M').to_numpy())
            self.selectionSlider_date02.observe(self._selection_observe_02, 'value')

            self.text_pathSaveInventarioDF = ipywidgets.Text(placeholder='Insert Path to Save')
            self.button_pathSaveInventarioDF = ipywidgets.Button(description='Save')
            self.button_pathSaveInventarioDF.on_click(self._button_saveInventarioDF)

        return ipywidgets.VBox([self.dropdown_typeView,
                                ipywidgets.HBox([self.text_pathShapefile_02, self.button_ViewShapefile_02]),
                                self.selectionMultiple_df_01,
                                self.selectionSlider_date02,
                                ipywidgets.HBox([self.text_pathSaveInventarioDF, self.button_pathSaveInventarioDF]),
                                self.out02])

    def tab03(self):
        self.out03 = ipywidgets.Output()
        self.out03_02 = ipywidgets.Output()
            # self.dropdown_typeView = ipywidgets.Dropdown(options=['Watershed', 'All', 'byDate'], value=None, description='Select type:', layout=ipywidgets.Layout(width='90%'))


        # with self.out03:
            # display(self.subset01['Codigo'].count())

        self.accordion01 = ipywidgets.Accordion([self.out03_02])
        self.accordion01.set_title(0, 'More stats')

        return ipywidgets.VBox([self.dropdown_typeView,
                                ipywidgets.HBox([self.text_pathShapefile_02, self.button_ViewShapefile_02]),
                                self.selectionSlider_date02,
                                self.out03,
                                self.accordion01])

    def _api_inventario(self):
        api_inventario = 'http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroInventario'
        params = {'codEstDE':'','codEstATE':'','tpEst':'','nmEst':'','nmRio':'','codSubBacia':'',
                  'codBacia':'','nmMunicipio':'','nmEstado':'','sgResp':'','sgOper':'','telemetrica':''}

        response = requests.get(api_inventario, params)
        tree = ET.ElementTree(ET.fromstring(response.content))
        root = tree.getroot()
        invent_data = {'BaciaCodigo':[],'SubBaciaCodigo':[],'RioCodigo':[],'RioNome':[],'EstadoCodigo':[],
                        'nmEstado':[],'MunicipioCodigo':[],'nmMunicipio':[],'ResponsavelCodigo':[],
                        'ResponsavelSigla':[],'ResponsavelUnidade':[],'ResponsavelJurisdicao':[],
                        'OperadoraCodigo':[],'OperadoraSigla':[],'OperadoraUnidade':[],'OperadoraSubUnidade':[],
                        'TipoEstacao':[],'Codigo':[],'Nome':[],'CodigoAdicional':[],'Latitude':[],'Longitude':[],
                        'Altitude':[],'AreaDrenagem':[],'TipoEstacaoEscala':[],'TipoEstacaoRegistradorNivel':[],
                        'TipoEstacaoDescLiquida':[],'TipoEstacaoSedimentos':[],'TipoEstacaoQualAgua':[],
                        'TipoEstacaoPluviometro':[],'TipoEstacaoRegistradorChuva':[],'TipoEstacaoTanqueEvapo':[],
                        'TipoEstacaoClimatologica':[],'TipoEstacaoPiezometria':[],'TipoEstacaoTelemetrica':[],'PeriodoEscalaInicio':[],'PeriodoEscalaFim':[] ,
                        'PeriodoRegistradorNivelInicio' :[],'PeriodoRegistradorNivelFim' :[],'PeriodoDescLiquidaInicio' :[],'PeriodoDescLiquidaFim':[] ,'PeriodoSedimentosInicio' :[],
                        'PeriodoSedimentosFim':[] ,'PeriodoQualAguaInicio':[] ,'PeriodoQualAguaFim' :[],'PeriodoPluviometroInicio':[] ,'PeriodoPluviometroFim':[] ,
                        'PeriodoRegistradorChuvaInicio' :[],'PeriodoRegistradorChuvaFim' :[],'PeriodoTanqueEvapoInicio':[] ,'PeriodoTanqueEvapoFim':[] ,'PeriodoClimatologicaInicio' :[],'PeriodoClimatologicaFim':[] ,
                        'PeriodoPiezometriaInicio':[] ,'PeriodoPiezometriaFim' :[],'PeriodoTelemetricaInicio' :[],'PeriodoTelemetricaFim' :[],
                        'TipoRedeBasica' :[],'TipoRedeEnergetica' :[],'TipoRedeNavegacao' :[],'TipoRedeCursoDagua' :[],
                        'TipoRedeEstrategica':[] ,'TipoRedeCaptacao':[] ,'TipoRedeSedimentos':[] ,'TipoRedeQualAgua':[] ,
                        'TipoRedeClasseVazao':[] ,'UltimaAtualizacao':[] ,'Operando':[] ,'Descricao':[] ,'NumImagens':[] ,'DataIns':[] ,'DataAlt':[]}
        total = len(list(root.iter('Table')))
        for i in root.iter('Table'):
            for j in invent_data.keys():
                d = i.find('{}'.format(j)).text
                if j == 'Codigo':
                    invent_data['{}'.format(j)].append('{:08}'.format(int(d)))
                else:
                    invent_data['{}'.format(j)].append(d)
            self.floatProgress_loadingInventario.value += 1/(total)

        self.df = pd.DataFrame(invent_data)

        self.text_pathSaveInventario.disabled = False
        self.button_pathSaveInventario.disabled = False

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



    def _radioButton_inventario(self, *args):
        with self.out01:
            self.floatProgress_loadingInventario.value = 0
            # print(self.radioButton_typeInvetario.value)
            if self.radioButton_typeInvetario.value == 'Select Path':
                self.text_pathInvetario.disabled = False
                self.button_pathInventario.disabled = False

            else:
                self.text_pathInvetario.disabled = True
                self.button_pathInventario.disabled = True
                # self._api_inventario()
                # self.floatProgress_loadingInventario.bar_style = 'success'

    def _button_pathinventario(self, *args):
        self.path_inventario = self.text_pathInvetario.value

    def _button_showInventario(self, *args):
        with self.out01:
            if self.radioButton_typeInvetario.value == 'Select Path':
                self.floatProgress_loadingInventario.value = 0
                try:
                    self.df = pd.read_csv(self.path_inventario, engine='python', sep='\t', delimiter=';', parse_dates=['UltimaAtualizacao'],low_memory=False)
                    self.df[['Latitude', 'Longitude']] = self.df[['Latitude', 'Longitude']].apply(lambda x: x.str.replace(',','.'))
                except:
                    self.df = pd.read_csv(self.path_inventario, parse_dates=['UltimaAtualizacao'],low_memory=False)

                self.df['Latitude'] = self.df['Latitude'].astype('float')
                self.df['Longitude'] = self.df['Longitude'].astype('float')
                self.gdf = gpd.GeoDataFrame(self.df, geometry=gpd.points_from_xy(self.df.Longitude, self.df.Latitude), crs='epsg:4674')

                self.selectionMultiple_df_01.options = self.gdf.columns.to_list()

                self.heatmap_all = ipyleaflet.Heatmap(locations=[tuple(r) for r in self.df[['Latitude', 'Longitude']].to_numpy()],radius=30, name='All point Heatmap')
                self.m01.add_layer(self.heatmap_all)

                self.heatmap_byLast = ipyleaflet.Heatmap(locations=[tuple(r) for r in self.df[['Latitude', 'Longitude']].to_numpy()],radius=30, name='By Date')
                self.m01.add_layer(self.heatmap_byLast)

                self.floatProgress_loadingInventario.value = 1
                self.floatProgress_loadingInventario.bar_style = 'success'


            elif self.radioButton_typeInvetario.value == 'Get from API':
                self.floatProgress_loadingInventario.value = 0
                self._api_inventario()
                self.df[['Latitude', 'Longitude']] = self.df[['Latitude', 'Longitude']].apply(lambda x: x.str.replace(',','.'))
                self.df['Latitude'] = self.df['Latitude'].astype('float')
                self.df['Longitude'] = self.df['Longitude'].astype('float')

                self.gdf = gpd.GeoDataFrame(self.df, geometry=gpd.points_from_xy(self.df.Longitude, self.df.Latitude), crs='epsg:4674')
                self.selectionMultiple_df_01.options = self.gdf.columns.to_list()

                self.heatmap_all = ipyleaflet.Heatmap(locations=[tuple(r) for r in self.df[['Latitude', 'Longitude']].to_numpy()],radius=30, name='All point Heatmap')
                self.m01.add_layer(self.heatmap_all)

                self.heatmap_byLast = ipyleaflet.Heatmap(locations=[tuple(r) for r in self.df[['Latitude', 'Longitude']].to_numpy()],radius=30, name='By Date')
                self.m01.add_layer(self.heatmap_byLast)


                self.floatProgress_loadingInventario.bar_style = 'success'

    def _checkbox_radius(self, *args):
        with self.out01:
            try:
                if self.checkbox_intSliderRadius.value == True:
                    self.intSlider_01 = ipywidgets.IntSlider(description='Radius', min=1, max=50, value=15)
                    self.intSlider_01.observe(self._intSlider_radius, 'value')
                    widget_control01 = ipyleaflet.WidgetControl(widget=self.intSlider_01, position='bottomright')
                    self.m01.add_control(widget_control01)

                else:
                    try:
                        self.intSlider_01.close()
                        self.m01.remove_control(widget_control01)
                    except:
                        pass
            except:
                pass

    def _intSlider_radius(self, *args):
        # ipywidgets.jslink((intSlider_01, 'value'),(self.heatmap_all,'radius'))
        # ipywidgets.jslink((intSlider_01, 'value'), (self.heatmap_byLast,'radius'))
        self.heatmap_all.radius = self.intSlider_01.value
        self.heatmap_byLast.radius = self.intSlider_01.value

    def _checkbox_date(self, *args):
        with self.out01:
            try:
                if self.checkbox_selectionDate.value == True:
                    self.selectionSlider_date01 = ipywidgets.SelectionSlider(options=pd.date_range(start='2000-01-01',end='2020-01-01', freq='M').to_numpy())
                    self.selectionSlider_date01.observe(self._selection_observe_01, names='value')
                    widget_control02 = ipyleaflet.WidgetControl(widget=self.selectionSlider_date01, position='bottomright')
                    self.m01.add_control(widget_control02)

                else:
                    try:
                        self.selectionSlider_date01.close()
                        self.m01.remove_control(widget_control02)
                    except:
                        pass
            except:
                pass

    def _selection_observe_01(self, *args):
        self.heatmap_byLast.locations = [tuple(s) for s in self.df.loc[self.df['UltimaAtualizacao'] > self.selectionSlider_date01.value, ['Latitude','Longitude']].to_numpy()]

    def _button_saveInventario(self, *args):
        with self.out01:
            try:
                path = pathlib.Path(self.text_pathSaveInventario.value)
                inventario_path = path/'Inventario.csv'
                self.df.to_csv('{}'.format(inventario_path))
            except:
                pass




    def _dropdown_observe_01(self, *args):
        if self.dropdown_typeDownload.value == 'Watershed':
            self.text_pathShapefle.disabled = False
            self.button_ViewShapefile.disabled = False
        else:
            self.text_pathShapefle.disabled = True
            self.button_ViewShapefile.disabled = True
            try:
                self.m01.remove_layer(self.geo_data)

            except:
                pass

    def _shapefile_buttom(self, *args):
        if self.dropdown_typeDownload.value == 'Watershed':
            try:
                self.shape = gpd.read_file(self.text_pathShapefle.value)
                self.geo_data = ipyleaflet.GeoData(geo_dataframe=self.shape, name='Bacias',style={'color': 'red', 'fillColor': '#c51b8a', 'opacity':0.05, 'weight':1.9, 'dashArray':'2', 'fillOpacity':0.6},
                               hover_style={'fillColor': 'red', 'fillOpacity': 0.2})
                self.m01.add_layer(self.geo_data)
            except:
                pass
        else:
            try:
                self.m01.remove_layer(self.geo_data)
            except:
                pass

    def _download_button01(self, *args):
        try:
            # with self.out01:
            # last_draw = self.feature_collection['features'][-1]['geometry']
            last_draw = self.draw_control.last_draw['geometry']
            # print(last_draw)
            last_polygon = Polygon([(i[0], i[1]) for i in last_draw['coordinates'][0]])
            # print(last_polygon)
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



    def _shapefile_buttom_02(self, *args):
        if self.dropdown_typeView.value == 'Watershed':
            try:
                # with self.ou02:
                #     print('fasas')
                self.shape_02 = gpd.read_file(self.text_pathShapefile_02.value)
                self.geo_data_02 = ipyleaflet.GeoData(geo_dataframe=self.shape_02, name='Bacia02',style={'color': 'red', 'fillColor': '#c51b8a', 'opacity':0.05, 'weight':1.9, 'dashArray':'2', 'fillOpacity':0.6},
                               hover_style={'fillColor': 'red', 'fillOpacity': 0.2})
                self.m01.add_layer(self.geo_data_02)
            except:
                pass
        else:
            try:
                self.m01.remove_layer(self.geo_data_02)
            except:
                pass

    def _selectionMultiple_column(self, *args):
        self.out02.clear_output()
        with self.out02:
            pd.set_option('display.max_rows', 10)
            try:
                last_draw = self.draw_control.last_draw['geometry']
                last_polygon = Polygon([(i[0], i[1]) for i in last_draw['coordinates'][0]])

                code_list = self.gdf.loc[self.gdf['geometry'].within(last_polygon), 'Codigo'].to_list()
            except:
                pass

            try:
                if self.dropdown_typeView.value == 'All':
                    self.subset01 = self.gdf.loc[self.gdf['geometry'].within(last_polygon),list(self.selectionMultiple_df_01.value)]

                elif self.dropdown_typeView.value == 'byDate':
                    self.subset01 = self.gdf.loc[(self.gdf['geometry'].within(last_polygon)) & (self.gdf['UltimaAtualizacao']>self.selectionSlider_date02.value),list(self.selectionMultiple_df_01.value)]

                elif self.dropdown_typeView.value == 'Watershed':
                    for i in self.shape_02['geometry']:
                        self.subset01 = self.gdf.loc[self.gdf['geometry'].within(i), list(self.selectionMultiple_df_01.value)]

                        # self.df_stat = self.gdf.loc[self.gdf['geometry'].within(i)]
                        #
                        # self.out03.clear_output()
                        # with self.out03:
                        #     print('Count:')
                        #     display(self.df_stat['Codigo'].count())
                        #     print('Operating:')
                        #     display(self.df_stat.loc[self.df_stat['Operando']==1, 'Codigo'].count())
                        #     print('Last update:')
                        #     display(self.df_stat['UltimaAtualizacao'].max())
                        #     print('Drainage Area (mean):')
                        #     display(self.df_stat['AreaDrenagem'].mean())
                        #     print('Altitude (mean):')
                        #     display(self.df_stat['Altitude'].mean())

                display(self.subset01)

            except:
                pass

    def _selection_observe_02(self, *args):
        try:
            if self.dropdown_typeView.value == 'byDate':
                last_draw = self.draw_control.last_draw['geometry']
                last_polygon = Polygon([(i[0], i[1]) for i in last_draw['coordinates'][0]])
                self.out02.clear_output()
                with self.out02:
                    self.subset01 = self.gdf.loc[(self.gdf['geometry'].within(last_polygon)) & (self.gdf['UltimaAtualizacao']>self.selectionSlider_date02.value),list(self.selectionMultiple_df_01.value)]

                    display(self.subset01)



                self.out03_02.clear_output()
                with self.out03_02:
                    pd.set_option('display.max_rows', None)
                    # last_draw = self.draw_control.last_draw['geometry']
                    # last_polygon = Polygon([(i[0], i[1]) for i in last_draw['coordinates'][0]])
                    self.df_stat = self.gdf.loc[(self.gdf['geometry'].within(last_polygon)) & (self.gdf['UltimaAtualizacao']>self.selectionSlider_date02.value)]
                    display(self.df_stat.groupby(by='OperadoraSigla')['Codigo'].count())

                self.out03.clear_output()
                with self.out03:
                    print('Count:')
                    display(self.df_stat['Codigo'].count())
                    print('Operating:')
                    display(self.df_stat.loc[self.df_stat['Operando']==1, 'Codigo'].count())
                    print('Last update:')
                    display(self.df_stat['UltimaAtualizacao'].max())
                    print('Drainage Area (mean):')
                    display(self.df_stat['AreaDrenagem'].mean())
                    print('Altitude (mean):')
                    display(self.df_stat['Altitude'].mean())
            else:
                pass
        except:
            pass

    def _button_saveInventarioDF(self, *args):
        with self.out02:
            try:
                path = pathlib.Path(self.text_pathSaveInventarioDF.value)
                inventarioDF_path = path/'Invent_df.csv'
                self.subset01.to_csv('{}'.format(inventarioDF_path))
            except:
                pass

    def _draw_testeObserve(self, *args):
        self.out02.clear_output()
        with self.out02:
            # print(list(self.selectionMultiple_df_01.value))
            pd.set_option('display.max_rows', 10)

            last_draw = self.draw_control.last_draw['geometry']
            last_polygon = Polygon([(i[0], i[1]) for i in last_draw['coordinates'][0]])

            code_list = self.gdf.loc[self.gdf['geometry'].within(last_polygon), 'Codigo'].to_list()

            self.subset01 = self.gdf.loc[self.gdf['geometry'].within(last_polygon),list(self.selectionMultiple_df_01.value)]
            display(self.subset01)




    def _output_stats(self, *args):
        self.out03.clear_output()
        with self.out03:
            try:
                last_draw = self.draw_control.last_draw['geometry']
                last_polygon = Polygon([(i[0], i[1]) for i in last_draw['coordinates'][0]])
            except:
                pass

            if self.dropdown_typeView.value == 'All':
                self.df_stat = self.gdf.loc[self.gdf['geometry'].within(last_polygon)]

            elif self.dropdown_typeView.value == 'byDate':
                self.df_stat = self.gdf.loc[(self.gdf['geometry'].within(last_polygon)) & (self.gdf['UltimaAtualizacao']>self.selectionSlider_date02.value)]

            elif self.dropdown_typeView.value == 'Watershed':
                pass

            print('Count:')
            display(self.df_stat['Codigo'].count())
            print('Operating:')
            display(self.df_stat.loc[self.df_stat['Operando']==1, 'Codigo'].count())
            print('Last update:')
            display(self.df_stat['UltimaAtualizacao'].max())
            print('Drainage Area (mean):')
            display(self.df_stat['AreaDrenagem'].mean())
            print('Altitude (mean):')
            display(self.df_stat['Altitude'].mean())



    def _output_stats02(self, *args):
        self.out03_02.clear_output()
        with self.out03_02:
            pd.set_option('display.max_rows', None)
            last_draw = self.draw_control.last_draw['geometry']
            last_polygon = Polygon([(i[0], i[1]) for i in last_draw['coordinates'][0]])
            self.df_stat = self.gdf.loc[self.gdf['geometry'].within(last_polygon)]
            display(self.df_stat.groupby(by='OperadoraSigla')['Codigo'].count())


    def _dropdown_observe_02(self, *args):
        self.out03.clear_output()
        with self.out03:
            try:
                last_draw = self.draw_control.last_draw['geometry']
                last_polygon = Polygon([(i[0], i[1]) for i in last_draw['coordinates'][0]])
            except:
                pass

            try:

                if self.dropdown_typeView.value == 'All':
                    self.df_stat = self.gdf.loc[self.gdf['geometry'].within(last_polygon)]

                elif self.dropdown_typeView.value == 'byDate':
                    self.df_stat = self.gdf.loc[(self.gdf['geometry'].within(last_polygon)) & (self.gdf['UltimaAtualizacao']>self.selectionSlider_date02.value)]

                elif self.dropdown_typeView.value == 'Watershed':
                    for i in self.shape_02['geometry']:
                        self.df_stat = self.gdf.loc[self.gdf['geometry'].within(i)]

                print('Count:')
                display(self.df_stat['Codigo'].count())
                print('Operating:')
                display(self.df_stat.loc[self.df_stat['Operando']==1, 'Codigo'].count())
                print('Last update:')
                display(self.df_stat['UltimaAtualizacao'].max())
                print('Drainage Area (mean):')
                display(self.df_stat['AreaDrenagem'].mean())
                print('Altitude (mean):')
                display(self.df_stat['Altitude'].mean())
            except:
                pass

        self.out03_02.clear_output()
        with self.out03_02:
            pd.set_option('display.max_rows', None)
            display(self.df_stat.groupby(by='OperadoraSigla')['Codigo'].count())

    def _shapefile_buttom_03(self, *args):
        self.out03.clear_output()
        with self.out03:
            try:
                last_draw = self.draw_control.last_draw['geometry']
                last_polygon = Polygon([(i[0], i[1]) for i in last_draw['coordinates'][0]])
            except:
                pass

            # if self.dropdown_typeView.value == 'All':
            #     self.df_stat = self.gdf.loc[self.gdf['geometry'].within(last_polygon)]
            #
            # elif self.dropdown_typeView.value == 'byDate':
            #     self.df_stat = self.gdf.loc[(self.gdf['geometry'].within(last_polygon)) & (self.gdf['UltimaAtualizacao']>self.selectionSlider_date02.value)]

            if self.dropdown_typeView.value == 'Watershed':
                for i in self.shape_02['geometry']:
                    self.df_stat = self.gdf.loc[self.gdf['geometry'].within(i)]

            print('Count:')
            display(self.df_stat['Codigo'].count())
            print('Operating:')
            display(self.df_stat.loc[self.df_stat['Operando']==1, 'Codigo'].count())
            print('Last update:')
            display(self.df_stat['UltimaAtualizacao'].max())
            print('Drainage Area (mean):')
            display(self.df_stat['AreaDrenagem'].mean())
            print('Altitude (mean):')
            display(self.df_stat['Altitude'].mean())

        self.out03_02.clear_output()
        with self.out03_02:
            pd.set_option('display.max_rows', None)
            display(self.df_stat.groupby(by='OperadoraSigla')['Codigo'].count())

    # def _selection_observe_03(self, *args):
    #     try:
    #         if self.dropdown_typeView.value == 'byDate':
    #             self.out03.clear_output()
    #
    #             last_draw = self.draw_control.last_draw['geometry']
    #             last_polygon = Polygon([(i[0], i[1]) for i in last_draw['coordinates'][0]])
    #             self.df_stat = self.gdf.loc[(self.gdf['geometry'].within(last_polygon)) & (self.gdf['UltimaAtualizacao']>self.selectionSlider_date02.value)]
    #             print('Count:')
    #             display(self.df_stat['Codigo'].count())
    #             print('Operating:')
    #             display(self.df_stat.loc[self.df_stat['Operando']==1, 'Codigo'].count())
    #             print('Last update:')
    #             display(self.df_stat['UltimaAtualizacao'].max())
    #             print('Drainage Area (mean):')
    #             display(self.df_stat['AreaDrenagem'].mean())
    #             print('Altitude (mean):')
    #             display(self.df_stat['Altitude'].mean())
    #     except:
    #         pass
