#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 11:17:25 2014
статистика озоновых профилей относительно положения тропопаузы.

@author: kshmirko
"""

import pandas as pds
import numpy as np
import sys
import pylab as plt
import os

def seasons(x):
    """
    Фильтр данных по принадлежности к сезону.
    """
    month = x.month
    ret = None
    if month in [12,1,2]:
        ret = "Winter"
    elif month in [3,4,5]:
        ret = "Spring"
    elif month in [6,7,8]:
        ret = "Summer"
    else:
        ret = "Fall"

    return ret


# координаты региона
Lon0 = 131.9
Lat0 = 43.1

Radius = float(input('Enter radius:> '))

# имена баз данных для заданного региона
DB = 'DS-%5.1f-%4.1f-%3.1f.h5'%(Lon0, Lat0, Radius)
O3StatFileName_fig = 'O3-%5.1f-%4.1f-%3.1f-stat.eps'%(Lon0, Lat0, Radius)
O3StatFileName_hdf = 'O3-%5.1f-%4.1f-%3.1f-stat.h5'%(Lon0, Lat0, Radius)

store = pds.HDFStore(O3StatFileName_hdf,'w', complib='zlib', complevel=5)

if not os.path.exists(DB):
    print("Run prepare.py before.")
    sys.exit(-1)


O3 = pds.read_hdf(DB,'O3')
O3_Err = pds.read_hdf(DB,'O3Err')
TH = pds.read_hdf(DB,'TH')

# вычисляем сезонную стстистику относительно тропопаузы
# группируем профили озона по сезонам
O3seasons = O3.groupby(seasons)

# то же делаем для ошибки восстанвления
O3seasons_Err = O3_Err.groupby(seasons).mean().T / 100.00

# и для высоты тропопаузы
THseasons = TH.groupby(seasons)

# фирмируем отсчеты высот - относительно замли
X = np.linspace(0.5, 70, 140) # actual altitudes

# длина нового веткора отсчетов отностительно тропопаузы 
nXLen = 81
# и относительно тропопаузы
nX= np.linspace(-5,35, nXLen) # new altitudes

# Число столбцов в результирующей матрице
Ncols = 4*3

# результирующие данные
# 2D таблицы
# 1-4столбцы - средние профили ВРО для Зимы, Весны, Лета и Осени
# 5-8 столбцы - средние профили ошибки восстановления ВРО для Зимы, Весны, Лета
#               и Осени
# 9-12 столбцы - СКВО для профилей
# профили представлены относительно полощения тропопаузы
OutDS = np.zeros((nXLen, Ncols), dtype=np.float32)


ax = plt.subplot(111)
ax2 = ax.twinx()


SEASONS = ['Winter','Spring','Summer','Fall']
# перебираем сезоны и выполняем коррекцию профилей озона на высоту тропопаузы
for iseason in range(len(SEASONS)):
    # возьмем индексы профилей для текущего сезона
    idx = THseasons.groups[SEASONS[iseason]]
    # и выделим профили измерений
    O3tmp = O3.ix[idx]
    O3Err = O3_Err.ix[idx]
    THtmp = TH.ix[idx]
    
    # определим буфферные объекты для хранения временных значений концентрации 
    # озона, ошибки его измерений
    no3tmp = pds.DataFrame(index=nX)
    no3errtmp = pds.DataFrame(index=nX)
    # в этом цикле осуществляется привязка профиля ВРО к новой сетке
    for i in range(len(idx)):
        # tmpX - вектор отсчетов высоты относительно тропопаузы
        tmpX = X-THtmp.values[i]
        tmpY = O3tmp.values[i]
        
        # поскольку профиль концентрации содержит NaN значения, то перед интерполяцией
        # необходимо найти их положение
        notnan = ~np.isnan(tmpY)

        # интерполируем профиль озона на регулярную сетку относительно высоты тропопаузы

        no3tmp[idx[i]] = np.interp(nX, tmpX[notnan], tmpY[notnan],left=np.nan, right=np.nan)

        # повторяем аналогичные действия для ошибки восстановления профилей концентрации озона
        tmpY = O3Err.values[i]
        notnan = ~np.isnan(tmpY)
        
        no3errtmp[idx[i]] = np.interp(nX, tmpX[notnan], tmpY[notnan],left=np.nan, right=np.nan)

    OutDS[:,iseason] = no3tmp.T.mean()
    OutDS[:,iseason+4] = no3errtmp.T.mean()/100
    OutDS[:,iseason+8] = no3tmp.T.std()
    
    p=ax.plot(nX, OutDS[:,iseason]/1e12,linestyle='dashed',marker='o',label=SEASONS[iseason])
    ax.plot(nX, OutDS[:,iseason+8]/1e12,'.-')
    ax.set_xlabel('Altitude, km.')
    ax.set_ylabel('$[O_3] \cdot 10^{12}, cm^{-3}$')
    ax.grid(True)
    ax2.plot(nX, OutDS[:,iseason+4],'.-')
    ax2.set_ylabel('Error, \%')

ax.legend()
plt.savefig(O3StatFileName_fig)


StatSave = pds.DataFrame(OutDS, index=nX, columns=['Winter_m','Spring_m','Summer_m','Fall_m',
                                               'Winter_e','Spring_e','Summer_e','Fall_e',
                                               'Winter_s','Spring_s','Summer_s','Fall_s'])
store.put('Statistics', StatSave)
store.close()


