# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 12:14:36 2022

@author: BEMC
"""

import matplotlib.pyplot as plt
import numpy as np
from hmtoolbox.WB_topo import interpolate, geometry_funcs
import geopandas as gpd
import pandas as pd
import mat73

path = 'z:\\130991_Systeemanalyse_ZSS\\2.Data\\bathy\\ontvangen\\WZ\\Niet meegroeien\\0m = base_minimum_bathymetry\\'
file = path+'Volledig_meegroeien_minimumbathy_0m.mat'

path_dummy = 'z:\\130991_Systeemanalyse_ZSS\\2.Data\\dummy\\'
file_chain_xy = path_dummy+'1D_voorland_chain_xy_10m.csv'
file_shape = path_dummy+'1D_voorland_transect.shp'

#%% input data
buffer = 200
spacing = 1

#%% load shape and make buffer
df_shp = gpd.read_file(file_shape)
df_shp_buffered = df_shp.buffer(buffer)

#%% load data using mat73
data = mat73.loadmat(file)

x = data['grd']['x']
y = data['grd']['y']
z = data['grd']['dp']

#%% find indices inside buffer and make df_xyz
ind_inside = geometry_funcs.get_points_in_polygon(df_shp_buffered[0],x,y)

df_xyz = pd.DataFrame({'x':x[ind_inside].ravel(),'y':y[ind_inside].ravel(),'z':z[ind_inside].ravel()})
df_xyz = df_xyz.dropna()

#%% make chain on shape
chain = geometry_funcs.points_on_line(df_shp.geometry[0],spacing,incl_end_point=False)
chain_coords = []
[chain_coords.append((c.coords.xy[0][0],c.coords.xy[1][0])) for c in chain]

# make dataframe of chain
df_xy = pd.DataFrame({'x':list(zip(*chain_coords))[0],'y':list(zip(*chain_coords))[1]})
df_xy['z'] = np.zeros_like(df_xy['x'])

#%% drape on xy
interpolate.interpolate_xyz_on_xy(df_xyz,df_xy)

#%% finish df_xy dataframe
# limit to last valid index of z
last_valid_ind = df_xy['z'].last_valid_index()
df_xy = df_xy.iloc[:last_valid_ind]

# calculate distance and fill out nans
df_xy['distance'] = np.sqrt((df_xy['x']-df_xy['x'][0])**2+(df_xy['y']-df_xy['y'][0])**2)
df_xy['z_filled'] = df_xy['z'].interpolate()

#%% show plot
fig,ax = plt.subplots(1,2,figsize=(12,6))
df_shp_buffered.plot(ax = ax[0])
ax[0].scatter(x[ind_inside],y[ind_inside],5,z[ind_inside])
df_shp.plot(ax = ax[0], color = 'red',linewidth=3)
ax[0].scatter(list(zip(*chain_coords))[0],list(zip(*chain_coords))[1],5,'k',zorder=10)

ax[0].set_xlabel('x-coord [m]')
ax[0].set_ylabel('y-coord [m]')
ax[0].set_title(f'bathy buffered with {buffer} m')

ax[1].plot(df_xy['distance'],df_xy['z'],label='raw 1D profile')
ax[1].plot(df_xy['distance'],df_xy['z_filled'],label='interpolated NaNs',zorder=0)
ax[1].set_title(f'interpolated 1D bathy, spacing = {spacing} m')
ax[1].set_xlabel('distance [m]')
ax[1].set_ylabel('height [m NAP]')
ax[1].legend()

#%% export to text file
save_file = path_dummy+'bottom.txt'
df_xy.to_csv(save_file,columns = 'z_filled',sep=' ', index=False, header=False, float_format='%.3f')





