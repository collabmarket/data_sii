#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date
import pandas as pd
import numpy as np
import scipy as sp

def get_data(year):
    url = 'http://www.sii.cl/pagina/valores/uf/uf%s.htm' % (year)
    df = pd.read_html(url, thousands='.')[0]
    df.rename(columns={u'Día': 'day'}, inplace=True)
    df['year'] = year
    # Transforma una columna para cada mes a una columna con el mes y otra con el valor
    df = pd.melt(df, id_vars=['day', 'year'], 
        value_vars=[u'Ene', u'Feb', u'Mar', u'Abr', u'May', u'Jun', u'Jul', 
                    u'Ago', u'Sep', u'Oct', u'Nov', u'Dic'])
    # Reemplaza str con nombre meses por int del mes
    df.replace({u'Ene':1, u'Feb':2, u'Mar':3, u'Abr':4, u'May':5, u'Jun':6, u'Jul':7, 
            u'Ago':8, u'Sep':9, u'Oct':10, u'Nov':11, u'Dic':12}, inplace=True)
    # Renombra columna variable creada por pd.melt
    df.rename(columns={'variable': 'month'}, inplace=True)
    # Crea serie con fechas a partir de columnas year, month y day
    fechas = pd.to_datetime(df.year.apply(str) + '-' + df.month.apply(str) + '-' + df.day.apply(str), errors='coerce')
    # Guarda serie fechas en columna date
    df['date'] = fechas
    df.dropna(inplace=True)
    # Establece columna date como index
    df.sort_values('date', inplace=True)
    df.set_index('date', inplace=True)
    # Crea indice con valores unicode
    str_index = df.value.apply(type) == unicode
    # Filtra los valores unicode y los transforma a float
    df.loc[str_index, 'value'] = df.value[str_index].str.replace('.', '')
    df.loc[str_index, 'value'] = df.value[str_index].str.replace(',', '.')
    df.loc[str_index, 'value'] = df.value[str_index].astype(float)
    df.value = df.value.astype(float)
    # Elimina las columnas year, month y day
    df.drop(['year', 'day', 'month'], axis=1, inplace=True)
    return df

def yesno(prompt = 'Continue?', default = 'y'):
    if default == 'y':
        alt = 'n'
    if default == 'n':
        alt = 'y' 
    q = "%s  [%s]/%s: "%(prompt,default,alt)
    ans = raw_input(q).lower().rstrip()
    if ans == '':
        ans = default
    return ans == 'y'


