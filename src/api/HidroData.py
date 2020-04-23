import xml.etree.ElementTree as ET
import requests
import pandas as pd
import calendar


def get_stations(list_stations, tipoDados):
    '''
       A partir de uma lista com o número das estações em formato inteiro, essa função retorna a série de dados diárias em um dataframe
       tipoDados deve ser em formato string (e.g. '2')
    '''
    params = {'codEstacao': '', 'dataInicio': '', 'dataFim': '', 'tipoDados': '', 'nivelConsistencia': ''}
    typesData = {'3': ['Vazao{:02}'], '2': ['Chuva{:02}'], '1': ['Cota{:02}']}
    params['tipoDados'] = tipoDados
    all_stations = pd.DataFrame()
    for station in list_stations:
        print(station)
        params['codEstacao'] = str(station)
        response = requests.get('http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroSerieHistorica', params)
        tree = ET.ElementTree(ET.fromstring(response.content))
        root = tree.getroot()
        df=[]
        for month in root.iter('SerieHistorica'):
            codigo = month.find('EstacaoCodigo').text
            consist = int(month.find('NivelConsistencia').text)
            date = pd.to_datetime(month.find('DataHora').text,dayfirst=True)
            date = pd.Timestamp(date.year, date.month, 1, 0)
            last_day=calendar.monthrange(date.year,date.month)[1]
            month_dates = pd.date_range(date,periods=last_day, freq='D')
            data = []
            list_consist = []
            for i in range(last_day):
                value = typesData[params['tipoDados']][0].format(i+1)
                try:
                    data.append(float(month.find(value).text))
                    list_consist.append(consist)
                except TypeError:
                    data.append(month.find(value).text)
                    list_consist.append(consist)
                except AttributeError:
                    data.append(None)
                    list_consist.append(consist)
            index_multi = list(zip(month_dates,list_consist))
            index_multi = pd.MultiIndex.from_tuples(index_multi,names=["Date","Consistence"])
            df.append(pd.DataFrame({f'{int(codigo):08}': data}, index=index_multi))
        if (len(df))>0:
            df = pd.concat(df)
            df = df.sort_index()
            indice = df.reset_index(level=1,drop=True).index.duplicated(keep='last')
            df = df[~indice]
            df = df.reset_index(level=1, drop=True)
            series = df[f'{int(codigo):08}']
            date_index = pd.date_range(series.index[0], series.index[-1], freq='D')
            series=series.reindex(date_index)
            all_stations = pd.concat([all_stations,series],axis=1)
        else:
            print('Station with no data')

    return all_stations

a = get_stations(list_stations=[50230000], tipoDados='3')
print(a)
