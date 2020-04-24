import xml.etree.ElementTree as ET
import requests
import pandas as pd

api_inventario = 'http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroInventario'

params = {'codEstDE':'',
          'codEstATE':'',
          'tpEst':'',
          'nmEst':'',
          'nmRio':'',
          'codSubBacia':'',
          'codBacia':'',
          'nmMunicipio':'',
          'nmEstado':'',
          'sgResp':'',
          'sgOper':'',
          'telemetrica':''}

response = requests.get(api_inventario, params)

print(response)

tree = ET.ElementTree(ET.fromstring(response.content))

root = tree.getroot()

data = {'BaciaCodigo':[],'SubBaciaCodigo':[],'RioCodigo':[],'RioNome':[],'EstadoCodigo':[],
        'nmEstado':[],'MunicipioCodigo':[],'nmMunicipio':[],'ResponsavelCodigo':[],
        'ResponsavelSigla':[],'ResponsavelUnidade':[],'ResponsavelJurisdicao':[],
        'OperadoraCodigo':[],'OperadoraSigla':[],'OperadoraUnidade':[],'OperadoraSubUnidade':[],
        'TipoEstacao':[],'Codigo':[],'Nome':[],'CodigoAdicional':[],'Latitude':[],'Longitude':[],
        'Altitude':[],'AreaDrenagem':[],'TipoEstacaoEscala':[],'TipoEstacaoRegistradorNivel':[],
        'TipoEstacaoDescLiquida':[],'TipoEstacaoSedimentos':[],
        'TipoEstacaoQualAgua':[],
        'TipoEstacaoPluviometro':[],
        'TipoEstacaoRegistradorChuva':[],
        'TipoEstacaoTanqueEvapo':[],
        'TipoEstacaoClimatologica':[],
        'TipoEstacaoPiezometria':[],
        'TipoEstacaoTelemetrica':[],
        'PeriodoEscalaInicio':[],
        'PeriodoEscalaFim':[] ,
        'PeriodoRegistradorNivelInicio' :[],
        'PeriodoRegistradorNivelFim' :[],
        'PeriodoDescLiquidaInicio' :[],
        'PeriodoDescLiquidaFim':[] ,
        'PeriodoSedimentosInicio' :[],
        'PeriodoSedimentosFim':[] ,
        'PeriodoQualAguaInicio':[] ,
        'PeriodoQualAguaFim' :[],
        'PeriodoPluviometroInicio':[] ,
        'PeriodoPluviometroFim':[] ,
        'PeriodoRegistradorChuvaInicio' :[],
        'PeriodoRegistradorChuvaFim' :[],
        'PeriodoTanqueEvapoInicio':[] ,
        'PeriodoTanqueEvapoFim':[] ,
        'PeriodoClimatologicaInicio' :[],
        'PeriodoClimatologicaFim':[] ,
        'PeriodoPiezometriaInicio':[] ,
        'PeriodoPiezometriaFim' :[],
        'PeriodoTelemetricaInicio' :[],
        'PeriodoTelemetricaFim' :[],
        'TipoRedeBasica' :[],
        'TipoRedeEnergetica' :[],
        'TipoRedeNavegacao' :[],
        'TipoRedeCursoDagua' :[],
        'TipoRedeEstrategica':[] ,
        'TipoRedeCaptacao':[] ,
        'TipoRedeSedimentos':[] ,
        'TipoRedeQualAgua':[] ,
        'TipoRedeClasseVazao':[] ,
        'UltimaAtualizacao':[] ,
        'Operando':[] ,
        'Descricao':[] ,
        'NumImagens':[] ,
        'DataIns':[] ,
        'DataAlt':[]}

# print(root.tag)
for i in root.iter('Table'):
    print(i.find('ResponsavelSigla').text)
    print(i.find('Codigo').text)
    code = i.find('Codigo').text
    print('{:08}'.format(int(code)))
    # print(i.find('Latitude').text)
    # print(i.find('Longitude').text)
    # print(i.find('AreaDrenagem').text)
