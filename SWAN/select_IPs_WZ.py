# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 13:26:10 2022

@author: ENGT2
"""

#%% load modules

import os
import pandas as pd
import numpy as np
import scipy
import matplotlib
import matplotlib.pyplot as plt
# %matplotlib qt
from hmtoolbox.WB_basic import save_plot

#%% settings

dirs = {'input':    r'z:\130991_Systeemanalyse_ZSS\5.Results\Hydra-NL_HBN',
        'output':   r'z:\130991_Systeemanalyse_ZSS\5.Results\Hydra-NL_HBN'}

files = {'hyd_output':  'Westerschelde_HBN_v3.csv'}

#%% read data

df_hyd  = pd.read_csv(os.path.join(dirs['input'],files['hyd_output']), sep=';')

#%% first plot IP's for all ZSS scenario's

save_fig = False

# filter on ZSS

# scenarios = df_hyd['ZSS-scenario'].unique()
scenarios = ["'KPZSS_2023_Referentie'", "'KPZSS_2100_Laag'", "'KPZSS_2100_Extreem'", "'KPZSS_2100_Zeer_extreem'", "'KPZSS_2200_Extreem'"]

plt.close('all')

fig = plt.figure()
colors = ['k','g','b','r','m']

nloc = len(df_hyd['OKADER VakId'].unique())
nscen = len(scenarios)
okid_mat = np.zeros((nloc,nscen))

ix = 0
for scenario in scenarios:
    is_scen =  df_hyd['ZSS-scenario']==scenario
    df_hyd_scen = df_hyd[is_scen]
    df_hyd_scen_sort = df_hyd_scen.sort_values('OKADER VakId')
    df_hyd_scen_sort = df_hyd_scen_sort.reset_index()
    df_hyd_scen_sort['index1'] = df_hyd_scen_sort.index
    okid_mat[:,ix] = df_hyd_scen_sort['OKADER VakId'].to_numpy()
    plt.subplot(3,1,1)
    s = plt.scatter(df_hyd_scen_sort['index1'],df_hyd_scen_sort['windsnelheid [m/s]'],20,colors[ix])
    s = plt.plot(df_hyd_scen_sort['index1'],df_hyd_scen_sort['windsnelheid [m/s]'],colors[ix],label=scenario)
    plt.grid()
    plt.xlabel('locatie')
    plt.ylabel('windsnelheid [m/s]')
    plt.legend()
    
    plt.subplot(3,1,2)
    s = plt.scatter(df_hyd_scen_sort['index1'],df_hyd_scen_sort['windrichting [graden N]'],20,colors[ix])
    s = plt.plot(df_hyd_scen_sort['index1'],df_hyd_scen_sort['windrichting [graden N]'],colors[ix],label=scenario)
    plt.grid()
    plt.xlabel('locatie')
    plt.ylabel('windrichting [graden N]')
    plt.legend()
    
    plt.subplot(3,1,3)
    s = plt.scatter(df_hyd_scen_sort['index1'],df_hyd_scen_sort['h, teen [m+NAP]'],20,colors[ix])
    s = plt.plot(df_hyd_scen_sort['index1'],df_hyd_scen_sort['h, teen [m+NAP]'],colors[ix],label=scenario)
    plt.grid()
    plt.xlabel('locatie')
    plt.ylabel('h, teen [m+NAP]')
    plt.legend()
    
    ix = ix + 1

# check if OKADER vakken are ordered in the same way for all plots
okid_mat_diff = np.diff(okid_mat,axis=1)
if okid_mat_diff.max() !=0:
    print('OKADER VakIds are not ordered in the same way')
else:
    print('OKADER VakIds are ordered in the same way')

if save_fig:
    name = f'output_hydra_vergelijking_ZSS.png'
    fname = os.path.join(dirs['output'],name)
    save_plot.save_plot(fig, fname, incl_wibo = False, dpi = 300, 
              change_size = True, figwidth = 14, figheight = 10)

#%% plot settings

scenario = "'KPZSS_2023_Referentie'"
is_scen =  df_hyd['ZSS-scenario']==scenario
df_hyd_scen = df_hyd[is_scen]
df_hyd_scen = df_hyd_scen.sort_values('OKADER VakId')
df_hyd_scen = df_hyd_scen_sort.reset_index()
df_hyd_scen['index1'] = df_hyd_scen_sort.index

hbn_min = round(min(df_hyd_scen['HBN [m+NAP]']) / 2) * 2
hbn_max = round(max(df_hyd_scen['HBN [m+NAP]']) / 2) * 2
hbn_step = 2
hbn_nstep = int((hbn_max - hbn_min)/hbn_step)
hbn_range = list(range(hbn_min, hbn_max + hbn_step, hbn_step))

ws_min = round(min(df_hyd_scen['windsnelheid [m/s]']) / 2) * 2
ws_max = round(max(df_hyd_scen['windsnelheid [m/s]']) / 2) * 2
ws_step = 3
ws_nstep = int((ws_max - ws_min)/ws_step)
ws_range = list(range(ws_min, ws_max + ws_step, ws_step))

hs_min = round(min(df_hyd_scen['Hm0, teen [m]']) / 2) * 2
hs_max = round(max(df_hyd_scen['Hm0, teen [m]']) / 2) * 2
hs_step = 1
hs_nstep = int((hs_max - hs_min)/hs_step)
hs_range = list(range(hs_min, hs_max + hs_step, hs_step))

h_min = round(min(df_hyd_scen['h, teen [m+NAP]']) / 2) * 2
h_max = round(max(df_hyd_scen['h, teen [m+NAP]']) / 2) * 2
h_step = 1
h_nstep = int((h_max - h_min)/h_step)
h_range = list(range(h_min, h_max + h_step, h_step))

dir_min = round(min(df_hyd_scen['windrichting [graden N]']) / 2) * 2
dir_max = round(max(df_hyd_scen['windrichting [graden N]']) / 2) * 2
dir_step = 30
dir_nstep = int((dir_max - dir_min)/dir_step)
dir_range = list(range(dir_min, dir_max + dir_step, dir_step))


#%% make spatial plots

fig = plt.figure()

cmap = plt.get_cmap('jet', hbn_nstep)

plt.subplot(3,2,1)
s = plt.scatter(df_hyd_scen['HYD_location_X'],df_hyd_scen['HYD_location_Y'],10,df_hyd_scen['HBN [m+NAP]'],cmap=cmap,vmin=hbn_min,vmax=hbn_max)
plt.xlabel('x (m)')
plt.ylabel('y (m)')
fig.colorbar(s, orientation='vertical', label='HBN [m+NAP]',boundaries = hbn_range,ticks = hbn_range)
plt.grid()
plt.axis('equal')

cmap = plt.get_cmap('jet', ws_nstep)

plt.subplot(3,2,4)
s = plt.scatter(df_hyd_scen['HYD_location_X'],df_hyd_scen['HYD_location_Y'],10,df_hyd_scen['windsnelheid [m/s]'],cmap=cmap,vmin=ws_min,vmax=ws_max)
plt.xlabel('x (m)')
plt.ylabel('y (m)')
# plt.clim(20,45)
fig.colorbar(s, orientation='vertical', label='windsnelheid [m/s]',boundaries = ws_range,ticks = ws_range)
plt.grid()
plt.axis('equal')

cmap = plt.get_cmap('jet', h_nstep)

plt.subplot(3,2,2)
s = plt.scatter(df_hyd_scen['HYD_location_X'],df_hyd_scen['HYD_location_Y'],10,df_hyd_scen['h, teen [m+NAP]'],cmap=cmap,vmin=h_min,vmax=h_max)
plt.xlabel('x (m)')
plt.ylabel('y (m)')
# plt.clim(5,9)
fig.colorbar(s, orientation='vertical', label='h, teen [m+NAP]',boundaries = h_range,ticks = h_range)
plt.grid()
plt.axis('equal')

cmap = plt.get_cmap('jet', dir_nstep)

plt.subplot(3,2,6)
s = plt.scatter(df_hyd_scen['HYD_location_X'],df_hyd_scen['HYD_location_Y'],10,df_hyd_scen['windrichting [graden N]'],cmap=cmap,vmin=dir_min,vmax=dir_max)
plt.xlabel('x (m)')
plt.ylabel('y (m)')
# plt.clim(230,360)
fig.colorbar(s, orientation='vertical', label='windrichting [graden N]',boundaries = dir_range,ticks = dir_range)
plt.grid()
plt.axis('equal')

cmap = plt.get_cmap('jet', hs_nstep)

plt.subplot(3,2,3)
s = plt.scatter(df_hyd_scen['HYD_location_X'],df_hyd_scen['HYD_location_Y'],10,df_hyd_scen['Hm0, teen [m]'],cmap=cmap,vmin=hs_min,vmax=hs_max)
plt.xlabel('x (m)')
plt.ylabel('y (m)')
# plt.clim(0,5)
fig.colorbar(s, orientation='vertical', label='Hm0 [m]',boundaries = hs_range,ticks = hs_range)
plt.grid()
plt.axis('equal')

fig.tight_layout()

plt.show()

plt.rcParams.update({'font.size': 8})

# namestr = scenario[1:-1]
# name = f'output_hydra_ruimtelijk_{namestr}.png'
# fname = os.path.join(dirs['output'],name)
# save_plot.save_plot(fig, fname, incl_wibo = False, dpi = 300, 
#           change_size = True, figwidth = 12, figheight = 8)


#%% make location spots

df_hyd_scen['index1'] = df_hyd_scen.index

limits = [0, 32, 38, 48, 88, 110, 143, len(df_hyd_scen['index1'])]

fig = plt.figure()

cmap = plt.get_cmap('jet', hbn_nstep)

plt.subplot(3,2,1)
s = plt.scatter(df_hyd_scen['index1'],df_hyd_scen['HBN [m+NAP]'],10,df_hyd_scen['HBN [m+NAP]'],cmap=cmap,vmin=hbn_min,vmax=hbn_max)
plt.xlabel('locatie')
fig.colorbar(s, orientation='vertical', label='HBN [m+NAP]',boundaries = hbn_range,ticks = hbn_range)
plt.grid()
ax =plt.gca()
ymin,ymax = ax.get_ylim()
plt.vlines(limits, ymin, ymax, colors='k', linestyles='dashed')

cmap = plt.get_cmap('jet', ws_nstep)

plt.subplot(3,2,4)
s = plt.scatter(df_hyd_scen['index1'],df_hyd_scen['windsnelheid [m/s]'],10,df_hyd_scen['windsnelheid [m/s]'],cmap=cmap,vmin=ws_min,vmax=ws_max)
plt.xlabel('locatie')
# plt.clim(20,45)
fig.colorbar(s, orientation='vertical', label='windsnelheid [m/s]',boundaries = ws_range,ticks = ws_range)
plt.grid()
ax =plt.gca()
ymin,ymax = ax.get_ylim()
plt.vlines(limits, ymin, ymax, colors='k', linestyles='dashed')

cmap = plt.get_cmap('jet', h_nstep)

plt.subplot(3,2,2)
s = plt.scatter(df_hyd_scen['index1'],df_hyd_scen['h, teen [m+NAP]'],10,df_hyd_scen['h, teen [m+NAP]'],cmap=cmap,vmin=h_min,vmax=h_max)
plt.xlabel('locatie')
# plt.clim(5,9)
fig.colorbar(s, orientation='vertical', label='h, teen [m+NAP]',boundaries = h_range,ticks = h_range)
plt.grid()
ax =plt.gca()
ymin,ymax = ax.get_ylim()
plt.vlines(limits, ymin, ymax, colors='k', linestyles='dashed')

cmap = plt.get_cmap('jet', dir_nstep)

plt.subplot(3,2,6)
s = plt.scatter(df_hyd_scen['index1'],df_hyd_scen['windrichting [graden N]'],10,df_hyd_scen['windrichting [graden N]'],cmap=cmap,vmin=dir_min,vmax=dir_max)
plt.xlabel('locatie')
# plt.clim(230,360)
fig.colorbar(s, orientation='vertical', label='windrichting [graden N]',boundaries = dir_range,ticks = dir_range)
plt.grid()
ax =plt.gca()
ymin,ymax = ax.get_ylim()
plt.vlines(limits, ymin, ymax, colors='k', linestyles='dashed')

cmap = plt.get_cmap('jet', hs_nstep)

plt.subplot(3,2,3)
s = plt.scatter(df_hyd_scen['index1'],df_hyd_scen['Hm0, teen [m]'],10,df_hyd_scen['Hm0, teen [m]'],cmap=cmap,vmin=hs_min,vmax=hs_max)
plt.xlabel('locatie')
# plt.clim(0,5)
fig.colorbar(s, orientation='vertical', label='Hm0 [m]',boundaries = hs_range,ticks = hs_range)
plt.grid()
ax =plt.gca()
ymin,ymax = ax.get_ylim()
plt.vlines(limits, ymin, ymax, colors='k', linestyles='dashed')

fig.tight_layout()

plt.show()

plt.rcParams.update({'font.size': 8})

# namestr = scenario[1:-1]
# name = f'output_hydra_locatie_{namestr}.png'
# fname = os.path.join(dirs['output'],name)
# save_plot.save_plot(fig, fname, incl_wibo = False, dpi = 300, 
#           change_size = True, figwidth = 12, figheight = 8)

#%%

# plt.close('all')

h   = df_hyd_scen['h, teen [m+NAP]']
ws  = df_hyd_scen['windsnelheid [m/s]']
wdir = df_hyd_scen['windrichting [graden N]']
okid = df_hyd_scen['OKADER VakId']

h_bins = np.array([4,5,6,7,8,9,10,11,12])
ws_bins = np.array([19,22,25,28,31,34,37,40,43,46,49])
wdir_val = np.array([240,270,300,360])

h_val = h_bins + 0.5
ws_val = ws_bins + 1.5

binning = pd.DataFrame()
okids = []

ix = 0
for k in range(len(wdir_val)):
    for i in range(len(h_bins)-1):
        for j in range(len(ws_bins)-1):
            ids = np.where((h>=h_bins[i]) & (h<h_bins[i+1]) & (ws>=ws_bins[j]) & (ws<ws_bins[j+1]) & (wdir==wdir_val[k]))
            ids_temp = np.array(ids)
            numel = ids_temp.size
            if numel == 0:
                okids = []
            else:
                okids = okid.iloc[[1,3,5]]
            # okids = [okid.iloc[id] for id in ids]
            data = {'wdir': wdir_val[k],
                    'h': h_val[i],
                    'ws': ws_val[j],
                    'ids': ids,
                    'numel': numel,
                    'okids': (np.array([]), )}
            df_temp = pd.DataFrame(data)
            df_temp.at[0,'okids'] = [100, 200, 301]
            binning = binning.append(df_temp, ignore_index=True)
            
totalfreq, xedges, yedges = np.histogram2d(h, ws, bins=(h_bins, ws_bins))

X,Y = np.meshgrid(h_bins,ws_bins)
X = np.transpose(X)
Y = np.transpose(Y)

binning.to_excel(os.path.join(dirs['output'],'binning.xlsx'))

#%%
# plt.close('all')

for direc in wdir_val:
    
    selec = binning[(binning['wdir'] == direc) & (binning['numel'] > 0)]
    
    plt.figure()
    s = plt.scatter(selec['h'],selec['ws'],10,'k',cmap='jet')
    plt.scatter(X,Y)
    for ix, row in selec.iterrows():
        plt.text(row['h'],row['ws'],'%d' % row['numel'])
    plt.xlabel('h, teen [m+NAP]')
    plt.ylabel('windsnelheid [m/s]')
    plt.xticks(ticks=h_bins)
    plt.yticks(ticks=ws_bins)
    plt.grid()
    plt.title('wdir = %d' % direc)
