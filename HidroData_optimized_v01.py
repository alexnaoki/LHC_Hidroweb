import requests
import pandas as pd
import xml.etree.ElementTree as ET
import calendar
import numpy as np
import datetime
import pathlib
import ipywidgets

def get_stations(list_codigos, typeData, folder_toDownload):

    path_folder = pathlib.Path(folder_toDownload)
    if __name__ != '__main__':
        control_progress = ipywidgets.IntProgress(min=0, value=0,max=len())

    for station in list_codigos:
        params = {'codEstacao': station, 'dataInicio': '', 'dataFim': '', 'tipoDados': '{}'.format(typeData), 'nivelConsistencia': ''}
        response = requests.get('http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroSerieHistorica', params)
        print(response)

        try:
            control_progress.value += 1
        except:
            pass
        tree = ET.ElementTree(ET.fromstring(response.content))
        # print(tree)

        root = tree.getroot()
        # print(root)

        # Cada iteração é um mês
        # df1 = pd.DataFrame()
        # to_df = np.array(['Date', 'Consistence','Data'])
        list_data = []
        list_consistenciaF = []
        list_month_dates = []
        for i in root.iter('SerieHistorica'):
            codigo = i.find("EstacaoCodigo").text

            consistencia = i.find("NivelConsistencia").text

            date = i.find("DataHora").text

            date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

            date = pd.Timestamp(date.year, date.month, 1, 0)
            last_day = calendar.monthrange(date.year, date.month)[1]
            month_dates = []
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
            df.to_csv(path_folder/filename)

        else:
            print("Estação sem dados")

get_stations(list_codigos=[50230000], typeData=3,  folder_toDownload=r'C:\Users\Usuario\Desktop\lhc_hidroweb')
