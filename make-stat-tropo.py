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
Radius = 4.0

# имена баз данных для заданного региона
DB = 'DS-%5.1f-%4.1f-%3.1f.h5'%(Lon0, Lat0, Radius)
O3StatFileName = 'O3-%5.1f-%4.1f-%3.1f.pdf'%(Lon0, Lat0, Radius)


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
nX= np.linspace(-5,35,81) # new altitudes

# Число столбцов в результирующей матрице
Ncols = 4*2+1

# результирующие данные
# 2D таблицы
# 1 столбец   - высота
# 2-5 столбцы - средние профили ВРО для Зимы, Весны, Лета и Осени
# 6-9 столбцы - средние профили ошибки восстановления ВРО для Зимы, Весны, Лета
#               и Осени 
# профили представлены относительно полощения тропопаузы
OutDS = np.zeros((nXLen, Ncols), dtype=np.float32)



#o3mean = pds.DataFrame(index=nX, columns=['Winter','Spring','Summer','Fall'])
#o3mean_err = pds.DataFrame(index=nX, columns=['Winter','Spring','Summer','Fall'])

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
    no3tmp = pds.DataFrame(index=nX,columns=O3tmp.index)
    no3errtmp = pds.DataFrame(index=nX,columns=O3tmp.index)

    # в этом цикле осуществляется привязка профиля ВРО к новой сетке
    for i in range(len(THtmp)):
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

    OutDS[:,iseason+1] = no3tmp.T.mean()
    OutDS[:,iseason+5] = no3tmp.T.std()
    plt.plot(nX, OutDS[:,iseason+1]/1e12, nX, OutDS[:,iseason+5]/1e12)

plt.legend(SEASONS)
plt.show()
sys.exit()

import pylab as plt

X = np.linspace(0.5, 70, 140)
plt.figure(1)
plt.clf()
ax = plt.subplot(2,2,1)
ax.plot(X, O3seasons['Winter'])
ax.set_xlim((0,40))
ax.set_ylim((0,6))
ax.set_ylabel('$[O3]x10^{12}, cm^{-3}$' )
ax.set_title('Winter')
Ht0 = THseasons['Winter'][0]['mean']
Ht0e= THseasons['Winter'][0]['std']
ax.plot([Ht0,Ht0],[0,6],
        'k.--',lw=2)
ax.plot([Ht0,Ht0],[0,6],
        'k.--',lw=2)
ax.annotate('$H_{tropo}=%3.1f\pm%3.1f km$'%(Ht0, Ht0e), xy=(Ht0, 4,),  
            xycoords='data', xytext=(30, 4.0),
            arrowprops=dict(arrowstyle="->", lw=2),
            size=16
            )
ax.grid()
ax2 = ax.twinx()
ax2.plot(X,O3seasons_Err['Winter'],'r.--')
ax.spines['right'].set_color('red')
ax2.yaxis.label.set_color('red')
ax2.tick_params(axis='y', colors='red')
ax2.set_ylim((0,100))

# 2-nd plot
ax = plt.subplot(2,2,2)
ax.plot(X, O3seasons['Spring'],'g')
ax.set_xlim((0,40))
ax.set_ylim((0,6))
ax.set_title('Spring')
Ht0 = THseasons['Spring'][0]['mean']
Ht0e= THseasons['Spring'][0]['std']
ax.plot([Ht0,Ht0],[0,6],
        'k.--',lw=2)
ax.plot([Ht0,Ht0],[0,6],
        'k.--',lw=2)
ax.annotate('$H_{tropo}=%3.1f\pm%3.1f km$'%(Ht0, Ht0e), xy=(Ht0, 4,),  
            xycoords='data', xytext=(30, 4.0),
            arrowprops=dict(arrowstyle="->", lw=2),
            size=16
            )
ax.grid()
ax2 = ax.twinx()
ax2.plot(X,O3seasons_Err['Spring'],'r.--')
ax.spines['right'].set_color('red')
ax2.set_ylabel('Error,$\%$')
ax2.tick_params(axis='y', colors='red')
ax2.yaxis.label.set_color('red')
ax2.set_ylim((0,100))

#3-rd plot
ax = plt.subplot(2,2,3)
ax.plot(X, O3seasons['Summer'],'y')
ax.set_xlim((0,40))
ax.set_ylim((0,6))
ax.grid()
ax.set_xlabel('Altitude, km')
ax.set_ylabel('$[O3]x10^{12}, cm^{-3}$' )
ax.set_title('Summer')
Ht0 = THseasons['Summer'][0]['mean']
Ht0e= THseasons['Summer'][0]['std']
ax.plot([Ht0,Ht0],[0,6],
        'k.--',lw=2)
ax.plot([Ht0,Ht0],[0,6],
        'k.--',lw=2)
ax.annotate('$H_{tropo}=%3.1f\pm%3.1f km$'%(Ht0, Ht0e), xy=(Ht0, 4,),  
            xycoords='data', xytext=(30, 4.0),
            arrowprops=dict(arrowstyle="->", lw=2),
            size=16
            )
ax2 = ax.twinx()
ax2.plot(X,O3seasons_Err['Summer'],'r.--')
ax.spines['right'].set_color('red')
ax2.tick_params(axis='y', colors='red')
ax2.yaxis.label.set_color('red')
ax2.set_ylim((0,100))

#4-th plot
ax = plt.subplot(2,2,4)
ax.plot(X, O3seasons['Fall'],'k')
ax.set_xlim((0,40))
ax.set_ylim((0,6))
Ht0 = THseasons['Fall'][0]['mean']
Ht0e= THseasons['Fall'][0]['std']
ax.plot([Ht0,Ht0],[0,6],
        'k.--',lw=2)
ax.plot([Ht0,Ht0],[0,6],
        'k.--',lw=2)
ax.annotate('$H_{tropo}=%3.1f\pm%3.1f km$'%(Ht0, Ht0e), xy=(Ht0, 4,),  
            xycoords='data', xytext=(30, 4.0),
            arrowprops=dict(arrowstyle="->", lw=2),
            size=16
            )
ax.grid()
ax.set_xlabel('Altitude, km')
ax.set_title('Fall')
ax2 = ax.twinx()
ax2.plot(X,O3seasons_Err['Fall'],'r.--')
ax.spines['right'].set_color('red')
ax2.yaxis.label.set_color('red')
ax2.set_ylabel('Error,$\%$')
ax2.tick_params(axis='y', colors='red')
ax2.set_ylim((0,100))

plt.savefig(O3StatFileName)