# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 11:17:25 2014

@author: kshmirko
"""

import pandas as pds
import numpy as np

def seasons(x):
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

Lon0 = 131.9
Lat0 = 43.1
Radius = 4.0
DB = 'DS-%5.1f-%4.1f-%3.1f.h5'%(Lon0, Lat0, Radius)
O3StatFileName = 'O3-%5.1f-%4.1f-%3.1f.pdf'%(Lon0, Lat0, Radius)

O3 = pds.read_hdf(DB,'O3')
O3_Err = pds.read_hdf(DB,'O3Err')
TH = pds.read_hdf(DB,'TH')


#вычисляем статистику по сезонам относительно земли
O3seasons = O3.groupby(seasons).mean().T / 1.0e12
O3seasons_c = O3.groupby(seasons).count().T
O3seasons_Err = O3_Err.groupby(seasons).mean().T / 100.00
THseasons = TH.groupby(seasons).agg([np.mean, np.std]).T

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