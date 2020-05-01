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

import bqplot as bq
from functools import reduce

class ANA_interactive_map:


    def __init__(self):

        self.m01 = ipyleaflet.Map(zoom=4, center=(-16, -50), scroll_wheel_zoom=True,layout=ipywidgets.Layout(width='60%', height='500px'))

        self.controls_on_Map()

        self.out01 = ipywidgets.Output()

        self.tabs = ipywidgets.Tab([self.tab00(), self.tab01(), self.tab02(),self.tab03(),  self.tab04()], layout=ipywidgets.Layout(width='40%'))
        self.tabs.set_title(0, 'Inventory ')
        self.tabs.set_title(1, 'Tables')
        self.tabs.set_title(2, 'Stats')
        self.tabs.set_title(3, 'Download')
        self.tabs.set_title(4, 'Graphs')



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
            self.html_00_01 = ipywidgets.HTML(value="<h2>Inventory</h2><hr><p>In order to utilize the program, you need to insert a <b>Inventory File</b> or get it from the <b>ANA's API</b>.</p><p>After completed the upload of the Inventory, you can select which <b>Layers</b> to visualize by checking the <b>top-right widget</b> on the map.</p>")
            self.radioButton_typeInvetario = ipywidgets.RadioButtons(options=['Select Path', 'Get from API'], value=None)
            self.radioButton_typeInvetario.observe(self._radioButton_inventario, names='value')


            self.text_pathInvetario = ipywidgets.Text(placeholder='Insert path of the Inventario')
            self.button_pathInventario = ipywidgets.Button(description='Apply')
            self.button_pathInventario.on_click(self._button_pathinventario)


            self.button_showInventario = ipywidgets.Button(description='Show')
            self.button_showInventario.on_click(self._button_showInventario)

            self.floatProgress_loadingInventario = ipywidgets.FloatProgress(min=0, max=1, value=0, layout=ipywidgets.Layout(width='90%'))
            self.floatProgress_loadingInventario.bar_style = 'info'



            self.intSlider_01 = ipywidgets.IntSlider(description='Radius', min=1, max=50, value=15)
            self.intSlider_01.observe(self._intSlider_radius, 'value')
            widget_control01 = ipyleaflet.WidgetControl(widget=self.intSlider_01, position='bottomright')
            self.m01.add_control(widget_control01)


            self.selectionSlider_date01 = ipywidgets.SelectionSlider(options=pd.date_range(start='2000-01-01',end='2020-01-01', freq='M').to_numpy())
            self.selectionSlider_date01.observe(self._selection_observe_01, names='value')
            widget_control02 = ipyleaflet.WidgetControl(widget=self.selectionSlider_date01, position='bottomright')
            self.m01.add_control(widget_control02)


            self.html_00_02 = ipywidgets.HTML(value="<hr><p>Save the <b>API's</b> Inventory file:</p>")
            self.text_pathSaveInventario = ipywidgets.Text(placeholder='Insert path to Save Inventario')
            self.button_pathSaveInventario = ipywidgets.Button(description='Save')
            self.button_pathSaveInventario.on_click(self._button_saveInventario)

            self.text_pathInvetario.disabled = True
            self.button_pathInventario.disabled = True
            self.text_pathSaveInventario.disabled = True
            self.button_pathSaveInventario.disabled = True

            self.intSlider_01.disabled = True
            self.selectionSlider_date01.disabled = True

        return ipywidgets.VBox([self.html_00_01,
                                self.radioButton_typeInvetario,
                                ipywidgets.HBox([self.text_pathInvetario,self.button_pathInventario]),
                                self.button_showInventario,
                                self.floatProgress_loadingInventario,
                                self.html_00_02,
                                ipywidgets.HBox([self.text_pathSaveInventario, self.button_pathSaveInventario])])

    def tab03(self):
        self.html_03_01 = ipywidgets.HTML(value="<h2>Download</h2><hr><p>In order to <b>Download</b>, you need the <b>Inventory</b>.<p> Then, you can choose between using the <b>Watershed's Shapefile</b> or <b>Draw a Contour</b>.</p><p> Finally, you'll can choose to download <b>Rain</b> or <b>Flow</b> data.</p> <p>(*)You also, if selected <b>byDate</b> can filter the data.</p>")
        self.dropdown_typeDownload = ipywidgets.Dropdown(options=['Watershed', 'All', 'byDate'], value=None, description='Select type:', layout=ipywidgets.Layout(width='90%'))
        self.dropdown_typeDownload.observe(self._dropdown_observe_01, names='value')
        self.dropdown_typeDownload.observe(self._shapefile_buttom, names='value')

        self.text_pathShapefle = ipywidgets.Text(placeholder='Insert Shapefile PATH HERE')
        self.button_ViewShapefile = ipywidgets.Button(description='View', layout=ipywidgets.Layout(width='30%'))
        self.button_ViewShapefile.on_click(self._shapefile_buttom)

        self.text_pathShapefle.disabled = True
        self.button_ViewShapefile.disabled = True

        self.checkbox_downloadIndividual = ipywidgets.Checkbox(description='Individual Files', value=True)
        self.checkbox_downloadGrouped = ipywidgets.Checkbox(description='Grouped Files')

        self.text_pathDownload = ipywidgets.Text(placeholder='Write your PATH to Download HERE.')

        self.button_download = ipywidgets.Button(description='Download', layout=ipywidgets.Layout(width='30%'))
        self.button_download.on_click(self._download_button01)

        self.floatProgress_loadingDownload = ipywidgets.FloatProgress(min=0, max=1, value=0, layout=ipywidgets.Layout(width='90%'))
        self.radioButton_typeDownload = ipywidgets.RadioButtons(options=['Rain', 'Flow'], layout=ipywidgets.Layout())


        return ipywidgets.VBox([ipywidgets.VBox([self.html_03_01,
                                                 self.dropdown_typeDownload,
                                                 ipywidgets.HBox([self.text_pathShapefle,self.button_ViewShapefile])]),
                                self.radioButton_typeDownload,
                                ipywidgets.HBox([self.checkbox_downloadIndividual, self.checkbox_downloadGrouped]),
                                ipywidgets.HBox([self.text_pathDownload, self.button_download]),
                                self.floatProgress_loadingDownload])

    def tab01(self):
        self.out02 = ipywidgets.Output()

        with self.out02:
            self.html_01_01 = ipywidgets.HTML(value="<h2>Inventory</h2><hr><p>This tab is for the visualization of the <b>Inventory's</b> data table.</p>")

            self.dropdown_typeView = ipywidgets.Dropdown(options=['Watershed', 'All', 'byDate'], value=None, description='Select type:', layout=ipywidgets.Layout(width='90%'))
            self.dropdown_typeView.observe(self._dropdown_oberve_01_02, 'value')
            self.dropdown_typeView.observe(self._selectionMultiple_column, 'value')
            self.dropdown_typeView.observe(self._dropdown_observe_02, 'value')

            self.text_pathShapefile_02 = ipywidgets.Text(placeholder='Insert Shapefile')
            self.button_ViewShapefile_02 = ipywidgets.Button(description='View')
            self.button_ViewShapefile_02.on_click(self._shapefile_buttom_02)
            self.button_ViewShapefile_02.on_click(self._shapefile_buttom_03)

            self.selectionMultiple_df_01 = ipywidgets.SelectMultiple(description='Columns:')
            self.selectionMultiple_df_01.observe(self._selectionMultiple_column, 'value')

            self.selectionSlider_date02 = ipywidgets.SelectionSlider(options=pd.date_range(start='2000-01-01',end='2020-01-01', freq='M').to_numpy(),layout=ipywidgets.Layout(width='90%'))
            self.selectionSlider_date02.observe(self._selection_observe_02, 'value')

            self.html_01_02 = ipywidgets.HTML(value="<hr><p>Save the <b>Table</b> below:</p>")
            self.text_pathSaveInventarioDF = ipywidgets.Text(placeholder='Insert Path to Save')
            self.button_pathSaveInventarioDF = ipywidgets.Button(description='Save')
            self.button_pathSaveInventarioDF.on_click(self._button_saveInventarioDF)

            self.text_pathShapefile_02.disabled = True
            self.button_ViewShapefile_02.disabled = True
            self.text_pathSaveInventarioDF.disabled = True
            self.button_pathSaveInventarioDF.disabled = True

        return ipywidgets.VBox([self.html_01_01,
                                self.dropdown_typeView,
                                ipywidgets.HBox([self.text_pathShapefile_02, self.button_ViewShapefile_02]),
                                self.selectionMultiple_df_01,
                                self.selectionSlider_date02,
                                self.html_01_02,
                                ipywidgets.HBox([self.text_pathSaveInventarioDF, self.button_pathSaveInventarioDF]),
                                self.out02])

    def tab02(self):
        self.out03 = ipywidgets.Output()
        self.out03_02 = ipywidgets.Output()
        self.html_02_01 = ipywidgets.HTML(value="<h2>Inventory</h2><hr><p>This tab is for the visualization of the <b>Inventory's</b> basic stats.</p>")
        self.html_02_02 = ipywidgets.HTML()


        self.accordion01 = ipywidgets.Accordion([self.out03_02])
        self.accordion01.set_title(0, 'More stats')
        self.accordion01.selected_index = None

        return ipywidgets.VBox([self.html_02_01,
                                self.dropdown_typeView,
                                ipywidgets.HBox([self.text_pathShapefile_02, self.button_ViewShapefile_02]),
                                self.selectionSlider_date02,
                                self.html_02_02,
                                self.out03,
                                self.accordion01])

    def tab04(self):
        self.html_teste = ipywidgets.HTML(value="<h2>Download</h2><hr><p>In this tab, <b>after completed the Download</b> you can visualize the Date Periods of your data. But first, you'll need to select <b>2 or more columns</b>.</p><p><b>Red</b> means no data in the month.</p><p><b>Blue</b> means at least one day with data in the month.</p>")
        self.out04 = ipywidgets.Output()
        with self.out04:
            # self.x_scale_01 = bq.DateScale()
            # self.y_scale_01 = bq.LinearScale()
            self.x_scale_hm_01 = bq.OrdinalScale()
            self.y_scale_hm_01 = bq.OrdinalScale()
            self.c_scale_hm_01 = bq.ColorScale(scheme='RdYlBu')

            self.x_axis_01 = bq.Axis(scale=self.x_scale_hm_01,tick_rotate=270,tick_style={'font-size': 12}, num_ticks=5)
            self.y_axis_01 = bq.Axis(scale=self.y_scale_hm_01, orientation='vertical',tick_style={'font-size': 10})
            self.c_axis_01 = bq.ColorAxis(scale=self.c_scale_hm_01)

            self.fig_01 = bq.Figure(axes=[self.x_axis_01, self.y_axis_01],fig_margin={'top':40,'bottom':40,'left':40,'right':40})

            # self.dropdown_xAxis_01 = ipywidgets.Dropdown(description='X-Axis')
            # self.dropdown_yAxis_01 = ipywidgets.Dropdown(description='Y-Axis')
            # self.dropdown_xAxis_01.observe(self._dropdown_observe_axis, 'value')
            # self.dropdown_yAxis_01.observe(self._dropdown_observe_axis, 'value')

            self.selectionMultiple_column = ipywidgets.SelectMultiple(description='Columns')
            self.selectionMultiple_column.observe(self._selectionMultiple_observe_column, 'value')


            self.button_datePeriod = ipywidgets.Button(description='Plot')
            self.button_datePeriod.on_click(self._button_datePeriod)

        return ipywidgets.VBox([self.html_teste,
                                self.selectionMultiple_column,
                                self.button_datePeriod,
                                self.fig_01,
                                self.out04])




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
        self.dfs_download = []

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
                df = pd.DataFrame({'Date': list_month_dates, 'Consistence_{}_{}'.format(typeData,station): list_consistenciaF, 'Data{}_{}'.format(typeData,station): list_data})

                if self.checkbox_downloadIndividual.value == True:
                    filename = '{}_{}.csv'.format(typeData, station)
                    df.to_csv(path_folder / filename)
                else:
                    pass

                count += 1
                self.floatProgress_loadingDownload.value = float(count+1)/numberOfcodes
                self.dfs_download.append(df)
            else:
                count += 1
                self.floatProgress_loadingDownload.value = float(count+1)/numberOfcodes

        try:
            self.dfs_merge_teste0 = reduce(lambda left,right: pd.merge(left, right, on=['Date'], how='outer'), self.dfs_download)

            if self.checkbox_downloadGrouped.value == True:
                self.dfs_merge_teste0.to_csv(path_folder/'GroupedData_{}.csv'.format(typeData))
            else:
                pass
            self.selectionMultiple_column.options = list(filter(lambda i: 'Data' in i, self.dfs_merge_teste0.columns.to_list()))
        except:
            pass

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
            self.floatProgress_loadingInventario.bar_style = 'info'

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

            self.intSlider_01.disabled = False
            self.selectionSlider_date01.disabled = False

    def _intSlider_radius(self, *args):
        self.heatmap_all.radius = self.intSlider_01.value
        self.heatmap_byLast.radius = self.intSlider_01.value

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
                    self.html_02_02.value = "<table> <tr><td><span style='font-weight:bold'>Count:</spam></td> <td>{}</td></tr><tr><td><span style='font-weight:bold'>Operating:</span></td> <td>{}</td></tr> <tr> <td><span style='font-weight:bold'>Last Update:</span></td><td>{}</td>  </tr>  <tr>    <td><span style='font-weight:bold'>Mean Drainage Area:</span></td>    <td>{:.2f}</td>  </tr>  <tr>    <td><span style='font-weight:bold'>Mean Altitude:</span></td>    <td>{:.2f}</td>  </tr></table>".format(self.df_stat['Codigo'].count(),self.df_stat.loc[self.df_stat['Operando']==1, 'Codigo'].count(),self.df_stat['UltimaAtualizacao'].max(),self.df_stat['AreaDrenagem'].mean(),self.df_stat['Altitude'].mean())
                    # print('Count:')
                    # display(self.df_stat['Codigo'].count())
                    # print('Operating:')
                    # display(self.df_stat.loc[self.df_stat['Operando']==1, 'Codigo'].count())
                    # print('Last update:')
                    # display(self.df_stat['UltimaAtualizacao'].max())
                    # print('Drainage Area (mean):')
                    # display(self.df_stat['AreaDrenagem'].mean())
                    # print('Altitude (mean):')
                    # display(self.df_stat['Altitude'].mean())
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

    def _dropdown_oberve_01_02(self, *args):
        with self.out03:
            if self.dropdown_typeView.value == 'Watershed':
                self.text_pathShapefile_02.disabled = False
                self.button_ViewShapefile_02.disabled = False
            else:
                self.text_pathShapefile_02.disabled = True
                self.button_ViewShapefile_02.disabled = True
            self.text_pathSaveInventarioDF.disabled = False
            self.button_pathSaveInventarioDF.disabled = False


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
            self.html_02_02.value = "<table> <tr><td><span style='font-weight:bold'>Count:</spam></td> <td>{}</td></tr><tr><td><span style='font-weight:bold'>Operating:</span></td> <td>{}</td></tr> <tr> <td><span style='font-weight:bold'>Last Update:</span></td><td>{}</td>  </tr>  <tr>    <td><span style='font-weight:bold'>Mean Drainage Area:</span></td>    <td>{:.2f}</td>  </tr>  <tr>    <td><span style='font-weight:bold'>Mean Altitude:</span></td>    <td>{:.2f}</td>  </tr></table>".format(self.df_stat['Codigo'].count(),self.df_stat.loc[self.df_stat['Operando']==1, 'Codigo'].count(),self.df_stat['UltimaAtualizacao'].max(),self.df_stat['AreaDrenagem'].mean(),self.df_stat['Altitude'].mean())



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

                self.html_02_02.value = "<table> <tr><td><span style='font-weight:bold'>Count:</spam></td> <td>{}</td></tr><tr><td><span style='font-weight:bold'>Operating:</span></td> <td>{}</td></tr> <tr> <td><span style='font-weight:bold'>Last Update:</span></td><td>{}</td>  </tr>  <tr>    <td><span style='font-weight:bold'>Mean Drainage Area:</span></td>    <td>{:.2f}</td>  </tr>  <tr>    <td><span style='font-weight:bold'>Mean Altitude:</span></td>    <td>{:.2f}</td>  </tr></table>".format(self.df_stat['Codigo'].count(),self.df_stat.loc[self.df_stat['Operando']==1, 'Codigo'].count(),self.df_stat['UltimaAtualizacao'].max(),self.df_stat['AreaDrenagem'].mean(),self.df_stat['Altitude'].mean())
                # print('Count:')
                # display(self.df_stat['Codigo'].count())
                # print('Operating:')
                # display(self.df_stat.loc[self.df_stat['Operando']==1, 'Codigo'].count())
                # print('Last update:')
                # display(self.df_stat['UltimaAtualizacao'].max())
                # print('Drainage Area (mean):')
                # display(self.df_stat['AreaDrenagem'].mean())
                # print('Altitude (mean):')
                # display(self.df_stat['Altitude'].mean())
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

            if self.dropdown_typeView.value == 'Watershed':
                for i in self.shape_02['geometry']:
                    self.df_stat = self.gdf.loc[self.gdf['geometry'].within(i)]
            self.html_02_02.value = "<table> <tr><td><span style='font-weight:bold'>Count:</spam></td> <td>{}</td></tr><tr><td><span style='font-weight:bold'>Operating:</span></td> <td>{}</td></tr> <tr> <td><span style='font-weight:bold'>Last Update:</span></td><td>{}</td>  </tr>  <tr>    <td><span style='font-weight:bold'>Mean Drainage Area:</span></td>    <td>{:.2f}</td>  </tr>  <tr>    <td><span style='font-weight:bold'>Mean Altitude:</span></td>    <td>{:.2f}</td>  </tr></table>".format(self.df_stat['Codigo'].count(),self.df_stat.loc[self.df_stat['Operando']==1, 'Codigo'].count(),self.df_stat['UltimaAtualizacao'].max(),self.df_stat['AreaDrenagem'].mean(),self.df_stat['Altitude'].mean())


        self.out03_02.clear_output()
        with self.out03_02:
            pd.set_option('display.max_rows', None)
            display(self.df_stat.groupby(by='OperadoraSigla')['Codigo'].count())


    def _selectionMultiple_observe_column(self, *args):
        with self.out04:
            self.dfs_merge_teste = self.dfs_merge_teste0.copy()

            self.y_scale_hm_01 = bq.OrdinalScale()
            self.y_axis_01 = bq.Axis(scale=self.y_scale_hm_01, orientation='vertical',tick_style={'font-size': 10})


    def _button_datePeriod(self, *args):
        with self.out04:
            idx = pd.date_range(start=self.dfs_merge_teste['Date'].min(), end=self.dfs_merge_teste['Date'].max())
            # print(len(idx),np.shape(self.dfs_merge_teste))
            self.dfs_merge_teste.set_index('Date', inplace=True)
            # print(self.dfs_merge_teste[self.dfs_merge_teste.index.duplicated()])
            self.dfs_merge_teste = self.dfs_merge_teste[~self.dfs_merge_teste.index.duplicated()]
            # print(self.dfs_merge_teste.head())
            self.dfs_merge_teste = self.dfs_merge_teste.reindex(idx)

            self.dfs_resample = self.dfs_merge_teste.resample('M').count()
            self.dfs_resample = self.dfs_resample.rename_axis('Date').reset_index()

            x = [i.strftime('%Y-%m') for i in self.dfs_resample['Date']]
            y = self.dfs_resample[list(self.selectionMultiple_column.value)].columns.to_list()
            color = (self.dfs_resample[list(self.selectionMultiple_column.value)].to_numpy()!=0).transpose().astype(int)

            self.heat_01 = bq.HeatMap(x=x,y=y,color=color,scales={'x':self.x_scale_hm_01,'y':self.y_scale_hm_01,'color':self.c_scale_hm_01})
            self.fig_01.marks = [self.heat_01]
            self.y_axis_01.tick_values = []
