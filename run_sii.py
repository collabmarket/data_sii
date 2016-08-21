#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
import pandas as pd
import sii
from datetime import date

update_all_years = sii.yesno(prompt = u'¿Actualizar datos históricos?', 
                            default = 'n')
update_last_year = sii.yesno(prompt = u'¿Actualizar año presente?', 
                            default = 'y')

# Opciones lectura de archivos csv compatibles con excel spanish
karg_csvr = dict(delimiter=';', decimal=',', index_col=0, parse_dates=True)
# Opciones escrituda de archivos csv compatibles con excel spanish
karg_csvw = dict(sep=';', decimal=',')

if update_all_years:
    dfs = []
    yr = date.today().year
    for year in range(1990,yr):
        df = sii.get_data(year)
        dfs.append(df)
    uf = pd.concat(dfs)
    uf.to_csv('uf.csv', **karg_csvw)
    print uf.info()

if update_last_year:
    uf = pd.read_csv('uf.csv', **karg_csvr)
    yr = date.today().year
    df = sii.get_data(yr)
    uf = pd.concat([uf,df])
    # Drop extra copy of duplicate index of Pandas Series
    uf = uf.groupby(uf.index).last()
    uf.to_csv('uf.csv', **karg_csvw)
    print uf.info()

