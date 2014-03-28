#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 09:28:16 2014

@author: kshmirko
"""
import netCDF4 as nc
import numpy as np
import tables as tbl
from structs import LocalDS
from datetime import datetime

DB = '../sage-reader/data/SAGE-II-6.20.nc'


Lon0 = float(input('Longitude?:> '))#131.9
Lat0 = float(input('Latitude?:> '))#43.1

print('Station location: Lon = %5.2f\tLat = %5.2f\n'%(Lon0, Lat0))
Radius = float(input('Enter radius to search profiles:> '))
Radius2 = Radius**2

F=nc.Dataset(DB,'r')
VAR = F.variables

print(VAR['O3'].shape)
# select profiles inside Radius
Lon = VAR['Lon'][...]
Lat = VAR['Lat'][...]
TP = np.array(VAR['TP'][...])
Distance = ((Lon-Lon0)**2+(Lat-Lat0)**2)
ok = np.where((Distance<Radius2)&(TP!=-999.0))[0]

# and corresponding timepoints


#Tp = nc.num2date(TP[ok],TP.units, TP.calendar)


# выходной файл
H5FileName = 'DK-%5.1f-%4.1f-%3.1f.h5'%(Lon0, Lat0, Radius)

F = tbl.openFile(H5FileName, mode='w')
root = F.root

LocalDS = F.create_table(root, 'LocalDS', LocalDS, 'LocalDS')
LocalDS.attrs.time_units = 'days since 1984-02-08 00:00:00'
LocalDS.attrs._FillValue = -999.0
LocalDS.attrs.timestamp0 = datetime(1984,2,8,0,0,0).timestamp()

row = LocalDS.row

for i in np.arange(len(ok)):
    idx = ok[i]
    
    row['time'] = TP[idx]
    row['O3'] = np.array(VAR['O3'][idx].data)
    row['O3Err'] = np.array(VAR['O3_Err'][idx].data)
    row['TH'] = np.array(VAR['Trop_Height'][idx])
    row['Ext386'] = np.array(VAR['Ext386'][idx].data)
    row['Ext452'] = np.array(VAR['Ext452'][idx].data)
    row['Ext525'] = np.array(VAR['Ext525'][idx].data)
    row['Ext1020'] = np.array(VAR['Ext1020'][idx].data)
    row['Ext386_Err'] = np.array(VAR['Ext386_Err'][idx].data)
    row['Ext452_Err'] = np.array(VAR['Ext452_Err'][idx].data)
    row['Ext525_Err'] = np.array(VAR['Ext525_Err'][idx].data)
    row['Ext1020_Err'] = np.array(VAR['Ext1020_Err'][idx].data)

    row.append()


F.close()

