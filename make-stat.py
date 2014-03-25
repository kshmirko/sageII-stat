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


DB = 'O3data.h5'

O3 = pds.read_hdf(DB,'O3')
O3_Err = pds.read_hdf(DB,'O3Err')
TH = pds.read_hdf(DB,'TH')

O3seasons = O3.groupby(seasons).mean().T / 1.0e12
O3seasons_c = O3.groupby(seasons).count().T
O3seasons_Err = O3_Err.groupby(seasons).mean().T / 100.00
THseasons = TH.groupby(seasons).agg([np.mean, np.std]).T

import pylab as plt

fig_width_pt = 246.0  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inches
golden_mean = (np.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height =fig_width*golden_mean       # height in inches
fig_size = [fig_width,fig_height]

#params = {'backend': 'ps',
#          'axes.labelsize': 10,
#          'text.fontsize': 10,
#          'legend.fontsize': 10,
#          'xtick.labelsize': 8,
#          'ytick.labelsize': 8,
#          'text.usetex': True,
#          'figure.figsize': fig_size}
#plt.rcParams.update(params)

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

plt.savefig('o3.pdf')