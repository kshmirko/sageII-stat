#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 09:28:16 2014

@author: kshmirko
"""
import netCDF4 as nc
import numpy as np

DB = '../sage-reader/data/SAGE-II-6.20.nc'
Lon0 = 131.9
Lat0 = 43.1
print('Station location: Lon = %5.2f\tLat = %5.2f\n'%(Lon0, Lat0))
Radius = float(input('Enter radius to search profiles:> '))
Radius2 = Radius**2

F=nc.Dataset(DB,'r')
VAR = F.variables

print(VAR['O3'].shape)
# select profiles inside Radius
Lon = VAR['Lon'][...]
Lat = VAR['Lat'][...]
Distance = ((Lon-Lon0)**2+(Lat-Lat0)**2)
ok = np.where(Distance<Radius2)[0]

# and corresponding timepoints
TP = VAR['TP']
Tp = nc.num2date(TP[ok],TP.units, TP.calendar)


import pandas as pds


O3_profiles = VAR['O3'][ok,:]
O3_profiles_Err = VAR['O3_Err'][ok,:]
Tropo_Height = VAR['Trop_Height'][ok]
Ext386 = VAR['Ext386'][ok,:]
Ext386_Err = VAR['Ext386_Err'][ok,:]
Ext452 = VAR['Ext452'][ok,:]
Ext452_Err = VAR['Ext452_Err'][ok,:]
Ext525 = VAR['Ext525'][ok,:]
Ext525_Err = VAR['Ext525_Err'][ok,:]
Ext1020 = VAR['Ext1020'][ok,:]
Ext1020_Err = VAR['Ext1020_Err'][ok,:]

Df_O3 = pds.DataFrame(O3_profiles, index=Tp)
Df_O3_Err = pds.DataFrame(O3_profiles_Err, index=Tp)
Df_TH = pds.DataFrame(Tropo_Height, index=Tp)
Df_Ext386 = pds.DataFrame(Ext386, index=Tp)
Df_Ext452 = pds.DataFrame(Ext452, index=Tp)
Df_Ext525 = pds.DataFrame(Ext525, index=Tp)
Df_Ext1020 = pds.DataFrame(Ext1020, index=Tp)
Df_Ext386_Err = pds.DataFrame(Ext386_Err, index=Tp)
Df_Ext452_Err = pds.DataFrame(Ext452_Err, index=Tp)
Df_Ext525_Err = pds.DataFrame(Ext525_Err, index=Tp)
Df_Ext1020_Err = pds.DataFrame(Ext1020_Err, index=Tp)


H5FileName = 'DS-%5.1f-%4.1f-%3.1f.h5'%(Lon0, Lat0, Radius)

Df_O3.to_hdf(H5FileName,'O3',append=True)
Df_O3_Err.to_hdf(H5FileName,'O3Err',append=True)
Df_TH.to_hdf(H5FileName,'TH',append=True)
Df_Ext386.to_hdf(H5FileName,'Ext386',append=True)
Df_Ext452.to_hdf(H5FileName,'Ext386',append=True)
Df_Ext525.to_hdf(H5FileName,'Ext386',append=True)
Df_Ext1020.to_hdf(H5FileName,'Ext386',append=True)
Df_Ext386_Err.to_hdf(H5FileName,'Ext386_Err',append=True)
Df_Ext452_Err.to_hdf(H5FileName,'Ext452_Err',append=True)
Df_Ext525_Err.to_hdf(H5FileName,'Ext525_Err',append=True)
Df_Ext1020_Err.to_hdf(H5FileName,'Ext1020_Err',append=True)


#O3_mean = np.mean(O3_profiles,0)
#O3_mean_Err = np.mean(O3_profiles_Err,0)

#import pylab as plt

#X = np.linspace(0.5, 70, 140)

#plt.figure()
#ax = plt.subplot(111)
#ax.plot(X, O3_mean)
#ax2=ax.twinx()
#ax2.plot(X, O3_mean_Err/100.0)
#plt.show()
