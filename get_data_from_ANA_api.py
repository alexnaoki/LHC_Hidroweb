import requests
import pandas as pd
import xml.etree.ElementTree as ET
import calendar

params = {'codEstacao': '50230000', 'dataInicio': '', 'dataFim': '', 'tipoDados': '3', 'nivelConsistencia': ''}
response = requests.get('http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroSerieHistorica', params)
print(response)

tree = ET.ElementTree(ET.fromstring(response.content))
print(tree)

root = tree.getroot()
print(root)

df = []
# Cada iteração é um mês
for i in root.iter('SerieHistorica'):
    # break
    codigo = i.find("EstacaoCodigo").text
    print(codigo)

    consistencia = i.find("NivelConsistencia").text
    print(consistencia)

    date = i.find("DataHora").text
    date = pd.to_datetime(i.find("DataHora").text, dayfirst=True)
    date = pd.Timestamp(date.year, date.month, 1, 0)
    last_day = calendar.monthrange(date.year, date.month)[1]
    month_dates = pd.date_range(date, periods=last_day, freq='D')
    print(date)
    print(last_day)

    data = []
    list_consistencia = []
    for day in range(last_day):
        print(day)
        if params['tipoDados'] == '3':
            value = 'Vazao{:02}'.format(day)
            print(value)
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
