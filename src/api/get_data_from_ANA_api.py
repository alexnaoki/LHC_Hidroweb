import requests
import pandas as pd
import xml.etree.ElementTree as ET
import calendar



def get_stations(list_codigos, typeData, toSave_path):
    all_stations = pd.DataFrame()

    for station in list_codigos:
        params = {'codEstacao': station, 'dataInicio': '', 'dataFim': '', 'tipoDados': '{}'.format(typeData), 'nivelConsistencia': ''}
        response = requests.get('http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroSerieHistorica', params)
        print(response)

        tree = ET.ElementTree(ET.fromstring(response.content))
        # print(tree)

        root = tree.getroot()
        # print(root)

        # Cada iteração é um mês
        df = []

        for i in root.iter('SerieHistorica'):
            codigo = i.find("EstacaoCodigo").text
            # print(codigo)

            consistencia = i.find("NivelConsistencia").text
            # print(consistencia)

            date = i.find("DataHora").text
            date = pd.to_datetime(i.find("DataHora").text, dayfirst=True)
            date = pd.Timestamp(date.year, date.month, 1, 0)
            last_day = calendar.monthrange(date.year, date.month)[1]
            month_dates = pd.date_range(date, periods=last_day, freq='D')
            # print(date)
            # print(last_day)

            data = []
            list_consistencia = []
            for day in range(last_day):
                # print(day)
                if params['tipoDados'] == '3':
                    value = 'Vazao{:02}'.format(day)
                    # print(value)
                    try:
                        data.append(float(i.find(value).text))
                        list_consistencia.append(consistencia)
                    except TypeError:
                        data.append(i.find(value).text)
                        list_consistencia.append(consistencia)
                    except AttributeError:
                        data.append(None)
                        list_consistencia.append(consistencia)

                if params['tipoDados'] == '2':
                    value = 'Chuva{:02}'.format(day)
                    # print(value)
                    try:
                        data.append(float(i.find(value).text))
                        list_consistencia.append(consistencia)
                    except TypeError:
                        data.append(i.find(value).text)
                        list_consistencia.append(consistencia)
                    except AttributeError:
                        data.append(None)
                        list_consistencia.append(consistencia)

            index_multi = list(zip(month_dates, list_consistencia))
            index_multi = pd.MultiIndex.from_tuples(index_multi, names=["Date", "Consistence"])
            df.append(pd.DataFrame({f'{int(codigo):08}':data}, index=index_multi))

        if (len(df) > 0):
            print(len(df))
            df = pd.concat(df)
            df = df.sort_index()
            indice = df.reset_index(level=1, drop=True).index.duplicated(keep='last')
            df = df[~indice]
            df = df.reset_index(level=1, drop=True)
            series = df[f'{int(codigo):08}']
            data_index = pd.date_range(series.index[0], series.index[-1], freq='D')
            series = series.reindex(data_index)
            all_stations = pd.concat([all_stations, series], axis=1)
        else:
            print("Estação sem dados")

    all_stations.to_csv(r'{}'.format(toSave_path))

get_stations(list_codigos=[439012, 439011], typeData=2,toSave_path=r'C:\Users\Usuario\Desktop\lhc_hidroweb\test212e.csv')
