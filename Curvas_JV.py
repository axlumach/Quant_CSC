# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 18:07:18 2020

@author: massa
"""

import numpy as np
import pandas as pd
import requests
import urllib.request
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import datetime
from bizdays import Calendar, load_holidays
holidays = load_holidays('Brazil.txt')
cal = Calendar(holidays, ['Sunday', 'Saturday'], name = 'Brazil')

def strip_date(date):
    """
    Recebe uma variável string e retorna uma tupla com os valores de dia, mês e
    ano.
    """
    d = datetime.strptime(date, "%Y-%m-%d")
    year = d.year
    month = d.month
    day = d.day
    if month <10:
        month = '0'+str(month)
    if day<10:
        day = '0'+str(day)
       
    return day, month, year

def strip_date_arr(date_array):
    """
    Recebe um vetor com datas no formato string e retorna vetores com os valo
    res de dia, mês e ano
    """
    day, month, year = [], [], []
    
    for i in range(len(date_array)):
        year.append(date_array[i].year)
        month.append(date_array[i].month)
        day.append(date_array[i].day)
        if month[i]<10:
            month[i] = '0'+str(month[i])
        if day[i]<10:
            day[i] = '0'+str(day[i])
            
    return day,month, year

def get_f_du(dates):
    """
    Recebe um vetor com datas no formato string e, caso estas não sejam dias
    úteis do calendário BR, retorna vetor com as datas dos dias úteis seguintes
    """
    dus = []
    for i in range(len(dates)):
        aux = cal.isbizday(dates[i])
        if aux == False:
            dates[i] = cal.following(dates[i])
        dus.append(dates[i])
    return dus
       
def lista_du(d_inicial,d_final):
    """
    Recebe duas datas e retorna um vetor com os dias úteis entre estas (inputs
    inclusive)
    """
    arr_du = []
    du = cal.bizdays(d_inicial, d_final)    
    for i in range(0,du+1):
        if i ==0:
            arr_du.append(datetime.strptime(d_inicial, "%Y-%m-%d"))
        else:
            arr_du.append(cal.offset(arr_du[i-1],1))
    arr_du = [d.strftime('%Y-%m-%d') for d in arr_du]
    return arr_du
  
def CCL(date):
    """
    Recebe uma data em formato string e retorna dataframe com a curva do cupom
    cambial para a data especificada
    """
    dias, taxas = [],[]
    (dia,mes,ano) = strip_date(date)
    url = 'http://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/TxRef1.asp?Data='+str(dia)+'/'+str(mes)+'/'+str(ano)+'&Data1='+str(str(ano)+str(mes)+str(dia))+'&slcTaxa=DOC'
    site = requests.get(url)
    bs = BeautifulSoup(site.content, 'html.parser')
    txt = bs.find_all('td')
    tabelas = ["['tabelaConteudo1']","['tabelaConteudo2']"]
    for i in range(len(txt)):
        try:
            if str(txt[i]['class']) in tabelas:
                tratado = txt[i].text.replace('\r\n', '').replace(',','.').replace(' ', '')
                if i==0 or i%2 ==0:
                    dias.append(int(tratado))
                else:
                    taxas.append(float(tratado)/100)
        except:
            pass
        
    return pd.DataFrame(data = taxas, index = dias, columns = {'CCL 360 Dias'})

def PRE_DI(date):
    """
    Recebe uma data em formato string e retorna dataframe com as curvas pré
    252dias e 360dias para a data especificada
    """
    dias, tx252, tx360 = [], [], []
    (dia,mes,ano) = strip_date(date)
    url = 'http://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/TxRef1.asp?Data='+str(dia)+'/'+str(mes)+'/'+str(ano)+'&Data1='+str(str(ano)+str(mes)+str(dia))+'slcTaxa=PRE'
    site = requests.get(url)
    bs = BeautifulSoup(site.content, 'html.parser')
    txt = bs.find_all('td')
    tabelas = ["['tabelaConteudo1']","['tabelaConteudo2']"]
    for i in range(0,len(txt), 3):
        try:
            if str(txt[i]['class']) in tabelas:
                tratado = txt[i].text.replace('\r\n', '').replace(',','.').replace(' ', '')
                if i<=len(txt)-2:
                    dias.append(int(txt[i].text.replace('\r\n', '').replace(',','.').replace(' ', '')))
                    tx252.append(float(txt[i+1].text.replace('\r\n', '').replace(',','.').replace(' ', ''))/100)
                    tx360.append(float(txt[i+2].text.replace('\r\n', '').replace(',','.').replace(' ', ''))/100)
        except:
            pass
        
    return pd.DataFrame({'taxas252':tx252,'taxas360':tx360}, index = dias)

def IPCA(date):
    """
    Recebe uma data em formato string e retorna dataframe com a curva de infla
    ção para a data especificada
    """
    dias, taxas = [],[]
    (dia,mes,ano) = strip_date(date)
    url = 'http://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/TxRef1.asp?Data='+str(dia)+'/'+str(mes)+'/'+str(ano)+'&Data1='+str(str(ano)+str(mes)+str(dia))+'&slcTaxa=DIC'
    site = requests.get(url)
    bs = BeautifulSoup(site.content, 'html.parser')
    txt = bs.find_all('td')
    tabelas = ["['tabelaConteudo1']","['tabelaConteudo2']"]
    for i in range(len(txt)):
        try:
            if str(txt[i]['class']) in tabelas:
                tratado = txt[i].text.replace('\r\n', '').replace(',','.').replace(' ', '')
                if i==0 or i%2 ==0:
                    dias.append(int(tratado))
                else:
                    taxas.append(float(tratado)/100)
        except:
            pass
        
    return pd.DataFrame(data = taxas, index = dias, columns = {'IPCA 252 Dias'})
  
def Importa_DI(d_inicial, d_final, fixings, flag = 'dates'):
    """
    Inputs:
    Datas inicial e final;
    Fixing: vetor de vértices com datas ou números inteiros
    Flag: sinaliza o formato dos valores contidos em 'fixings'
    Funcionamento:
    Recebe as datas de referência para a curva pre 252dias cc e retorna datafra
    me com valores especificados pelo vetor 'fixings'
    """
    dates = lista_du(d_inicial, d_final)    
    array = np.zeros((len( dates),len(fixings)))
    if flag.lower() == 'dates':
        dus = get_f_du(fixings)
        for i in tqdm(range(len(dates))):
            aux_dus = [cal.bizdays(dates[i],d) for d in dus]
            aux_yd = PRE_DI(dates[i])
            aux_int = interpola_vetor(aux_dus,aux_yd,'taxas252',252,'exp')
            array = np.insert(array,[i],aux_int,axis = 0)
        df = pd.DataFrame(data = array,columns = fixings).drop_duplicates()[:-1]
        df['Data'] = dates
        df.set_index('Data',inplace = True)
    elif flag.lower() == 'num':
        for i in tqdm(range(len(dates))):
            aux_yd = PRE_DI(dates[i])
            aux_int = interpola_vetor(fixings,aux_yd,'taxas252',252,'exp')
            array = np.insert(array,[i],aux_int,axis = 0)
        df = pd.DataFrame(data = array,columns = fixings).drop_duplicates()[:-1]
        df['Data'] = dates
        df.set_index('Data',inplace = True)
        df.index = pd.to_datetime(df.index, format="%Y-%m-%d")
    return df

def Importa_CCL(d_inicial, d_final, fixings, flag = 'dates'):
    """
    Inputs:
    Datas inicial e final;
    Fixing: vetor de vértices com datas ou números inteiros
    Flag: sinaliza o formato dos valores contidos em 'fixings'
    Funcionamento:
    Recebe as datas de referência para as curvas do cc e retorna dataframe com
    valores especificados pelo vetor 'fixings'
    """
    dates = lista_du(d_inicial, d_final)    
    array = np.zeros((len( dates),len(fixings)))
    if flag.lower() == 'dates':
        dus = get_f_du(fixings)
        for i in tqdm(range(len(dates))):
            aux_dus = [cal.bizdays(dates[i],d) for d in dus]
            aux_yd = CCL(dates[i])
            aux_int = interpola_vetor(aux_dus,aux_yd,'CCL 360 Dias',360, 'lin')
            array = np.insert(array,[i],aux_int,axis = 0)
        df = pd.DataFrame(data = array,columns = fixings).drop_duplicates()[:-1]
        df['Data'] = dates
        df.set_index('Data',inplace = True)
    elif flag.lower() == 'num':
        for i in tqdm(range(len(dates))):
            aux_yd = CCL(dates[i])
            aux_int = interpola_vetor(fixings,aux_yd,'CCL 360 Dias',360, 'lin')
            array = np.insert(array,[i],aux_int,axis = 0)
        df = pd.DataFrame(data = array,columns = fixings).drop_duplicates()[:-1]
        df['Data'] = dates
        df.set_index('Data',inplace = True)
        df.index = pd.to_datetime(df.index, format="%Y-%m-%d")
    return df

def Importa_FWD_DI(d_inicial, d_final, fixings):
    """
    Inputs:
    Datas inicial e final;
    Fixing: vetor de vértices com datas no formato string
    Funcionamento:
    Recebe as datas de referência para as curvas do cc e retorna dataframe com
    valores especificados pelo vetor 'fixings'
    """    
    fwd = []
    dates = lista_du(d_inicial, d_final)
    array = np.zeros((len(dates),len(fixings)-1))
    dus = get_f_du(fixings)
    for i in tqdm(range(len(dates))):
        aux_dus = [cal.bizdays(dates[i],d) for d in dus]
        aux_yd = PRE_DI(dates[i])
        spot = interpola_vetor(aux_dus,aux_yd,'taxas252',252,'exp')
        for j in range(len(dus)-1):
            if j == 0:
                fwd.append(spot[j])
            else:
                fwd.append(((1+spot[j+1])**(aux_dus[j+1]/252))/((1+spot[j])**(aux_dus[j]/252))-1)
        array = np.insert(array,[i],fwd, axis = 0)
        fwd.clear()
    df = pd.DataFrame(data = array,columns = fixings[:-1]).drop_duplicates()[:-1]
    df['Data'] = dates
    df.set_index('Data',inplace = True)
    df.index = pd.to_datetime(df.index, format="%Y-%m-%d")
    return df

def Importa_FWD_CCL(d_inicial, d_final, fixings):
    fwd = []
    dates = lista_du(d_inicial, d_final)
    array = np.zeros((len(dates),len(fixings)-1))
    dus = get_f_du(fixings)
    for i in tqdm(range(len(dates))):
        aux_dus = [cal.bizdays(dates[i],d) for d in dus]
        aux_yd = CCL(dates[i])
        spot = interpola_vetor(aux_dus,aux_yd,'CCL 360 Dias',360,'lin')
        for j in range(len(dus)-1):
            if j == 0:
                fwd.append(spot[j])
            else:
                fwd.append(((1+spot[j+1])**(aux_dus[j+1]/360))/((1+spot[j])**(aux_dus[j]/360))-1)
        array = np.insert(array,[i],fwd, axis = 0)
        fwd.clear()
    df = pd.DataFrame(data = array,columns = fixings[:-1]).drop_duplicates()[:-1]
    df['Data'] = dates
    df.set_index('Data',inplace = True)
    df.index = pd.to_datetime(df.index, format="%Y-%m-%d")
    return df  

def interpolador(xi, df, column, dc, mod):
    """
    Inputs:
    xi: valores a serem interpolados
    df: dataframe que contém valores de referência para a interpolação
    column: columa a ser utilizada na interpolação
    dc: daycount utilizado. Pode ser 252 ou 360
    mod: tipo de interpolação a ser realizada, Pode ser linear ou exponencial    
    """
    x_axis = list(df.index)
    y_axis = list(df[column])    
    x1 = min(x_axis, key = lambda a:abs(a-xi))
    
    if xi-x1>0:
        x2 = x_axis[x_axis.index(x1)+1]
    elif xi-x1 ==0:
        x2 = x1
    elif xi-x1<0:
        x2 = x1
        x1 = x_axis[x_axis.index(x1)-1]
        
    y1 = y_axis[x_axis.index(x1)]
    y2 = y_axis[x_axis.index(x2)]
    
    if mod.lower() == 'lin':
        if x1-x2!=0:
            return(y1 + (xi-x1)*(y2-y1)/(x2-x1))        
        else:
            return(y1)
    elif mod.lower() == 'exp':
        if x1-x2!=0:
            f1 = (1+y1)**(x1/dc)
            f2 = (1+y2)**(x2/dc)
            f3 = (f2/f1)**((xi-x1)/(x2-x1))
            f4 = (f1*f3)**(dc/xi) -1
            return(f4)
        else:
            return(y1)

def interpola_vetor(x_arr, df, column, dc, mod):
    y_arr = []
    for x in range(len(x_arr)):
        y_arr.append(interpolador(x_arr[x], df, column, dc, mod))
    
    return(y_arr)            