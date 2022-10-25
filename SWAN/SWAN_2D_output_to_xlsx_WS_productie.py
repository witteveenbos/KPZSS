# -*- coding: utf-8 -*-
"""
--- Synopsis --- 
This scripts reads output from SWAN2D runs and writes it to an Excel.

--- Remarks --- 
See also: 
To-Do: 
Dependencies: 

--- Version --- 
Created on Mon Sep 26 09:21:51 2022
@author: ENGT2
Project: KP ZSS (130991)
Script name: SWAN_2D_output_to_xlsx_WS_productie.py 

--- Revision --- 
Status: Unverified 

Witteveen+Bos Consulting Engineers 
Leeuwenbrug 8
P.O. box 233 
7411 TJ Deventer
The Netherlands 
		
"""

#%% load modules

import os
import geopandas as gp
import matplotlib.pyplot as plt
import numpy as np
from hmtoolbox.WB_SWAN import SWAN_read_tab
from hmtoolbox.WB_basic import list_files_folders
from hmtoolbox.WB_basic import save_plot
import pandas as pd

#%% Settings

# Location of SWAN2D output
path_main   = r'z:\130991_Systeemanalyse_ZSS\3.Models\SWAN\2D\Westerschelde\03_productiesommen\serie_01'
dirs        = list_files_folders.list_folders(path_main, dir_incl='WS', startswith = True, endswith = False)

# Shapefile with OKADER vak info (including id and fragility curve info)
path_OKid_shape = r'd:\Users\ENGT2\Documents\Projects\130991 - SA Waterveiligheid ZSS\GIS\illustratiepunten_methode\okader_fc_hydra_unique_handedit_WS_geom.shp'

# Excel file with coupling between illustratiepunten (simulations) and OKADER vakken
path_coupling = r'z:\130991_Systeemanalyse_ZSS\3.Models\SWAN\2D\Westerschelde\03_productiesommen\serie_01\input\IP_OKADER_coupling.xlsx'

# Shapefile with output locations along SWAN 1D profiles
path_1D_outlocs = r'd:\Users\ENGT2\Documents\Projects\130991 - SA Waterveiligheid ZSS\GIS\illustratiepunten_methode\HRD_locations_selectie_WS_300m_interval_OKid.shp'

# Switch to results to Excel
save_excel = True

#%% Read output for selected locations and export to Excel

# get list of unique okader ids from shapefile
df_ids = gp.read_file(path_OKid_shape)

# get coupling of okader ids to simulation
xl_coupling = pd.ExcelFile(path_coupling,engine='openpyxl')
df_coupling = xl_coupling.parse()
okids_a = df_coupling['A']
okids_na = df_coupling['NA']
okids_all = df_coupling['ALL']

del df_coupling['A']
del df_coupling['NA']
del df_coupling['ALL']
df_coupling = np.array(df_coupling)

OKids = df_ids['VakId']
X = df_ids['xcoord']
Y = df_ids['ycoord']


#%% first loop over all OKADR ids to get SWAN som number

som_ids = []
OKids_near = []

ix = 0

for OKid in OKids:
    
    # get som id for okader vak id        
    indices = np.where(df_coupling==int(OKid))
    if indices[0].size > 0:
        som_ids.append(indices[1][0])
        print('OKADER ID assinged, som ID found')
        OKids_near.append('')
    elif indices[0].size == 0:
        print('OKADER ID %s not assigned, find nearest point' % OKid)
        xq = df_ids[df_ids['VakId']==OKid]['xcoord'].iloc[0]
        yq = df_ids[df_ids['VakId']==OKid]['ycoord'].iloc[0]
        dx = X - xq
        dy = Y - yq
        dis = np.sqrt(dx**2 + dy**2)
        dis[dis==0] = 1e6
        min_ind = np.argmin(dis, axis=0)
        OKid_near = OKids[min_ind]
        # check if nearest point is assigned in SWAN runs
        check_ind = np.where(df_coupling==int(OKid_near))
        if check_ind[0].size > 0:
            som_ids.append(check_ind[1][0])
            print('nearest point is assigned')
            OKids_near.append(OKid_near)
        elif check_ind[0].size == 0:
            print('nearest point is not assigned, take next point')
            for tt in range(0,3):
                dis[min_ind] = 1e6
                min_ind = np.argmin(dis, axis=0)
                OKid_near = OKids[min_ind]
                print(OKid_near)
                check_ind = np.where(df_coupling==int(OKid_near))
                if check_ind[0].size > 0:
                    som_ids.append(check_ind[1][0])
                    print('nearest point is assigned')
                    OKids_near.append(OKid_near)
                    break
                else:
                    print('assignment failed after %d iterations' % tt)
                    failed = 1
                    OKid_failed = OKid
    ix = ix + 1

data = {'OKid': OKids,
        'som_id': som_ids,
        'OKids_near': OKids_near}
assignment = pd.DataFrame(data)

if save_excel:
    assignment.to_excel(os.path.join(path_main,'assignment_okader_ids_simulatie_SWAN2D_WS.xlsx')) 


#%% get output at HRbasis locations

outlocs_name = 'HRbasis'
    
pd.options.mode.chained_assignment = None

min_dis_max = 0

XX = df_ids['XCoordinat']
YY = df_ids['YCoordinat']

# loop over all scenario's and simulations

appended_data_01 = []
for diri in dirs:
    ix = 0
    dirname = os.path.basename(os.path.normpath(diri))
    for OKid in OKids:
        
        som_id = assignment[assignment['OKid']==OKid]['som_id']
        
        subdir = list_files_folders.list_folders(diri, dir_incl="ID%03d" % som_id)       
        subdir = subdir[0]
        
        files = list_files_folders.list_files('.TAB', subdir, startswith = False, endswith = True)
        subdirname = os.path.basename(os.path.normpath(subdir))
        scen_name = diri.split("\\")[-1]
        for file in files:
            f = os.path.basename(os.path.normpath(file))
            if f.startswith(outlocs_name):
                print(OKid)
                print(scen_name)
                print(f)
                data, headers = SWAN_read_tab.Freadtab(os.path.join(subdir,f))  
        xx = data['Xp']
        yy = data['Yp']        
        xq = XX[ix]
        yq = YY[ix]
        
        dx = xx - xq
        dy = yy - yq
        dis = np.sqrt(dx**2 + dy**2)

        min_dis = np.min(dis)
        print('min distance = %.2f' % min_dis)
        row_ind = np.argmin(dis, axis=0)
        print('min index = %d' % row_ind)
        min_dis_max = max(min_dis, min_dis_max)
               
        result  = data.iloc[[row_ind]]
        result['OkaderId'] = OKids[ix]
        result['Scenario'] = dirname
        result['min_dis'] = min_dis
        result['row_ind'] = row_ind
        appended_data_01.append(result)
        ix = ix + 1
        
        del data, result, dis, xx, yy, xq, yq  
                   
appended_data_01 = pd.concat(appended_data_01)
print('maximum distace with SWAN output loc = %.2f' % min_dis_max)


#%% get output along 1D profiles (input 1D SWAN simulations)

outlocs_name = 'HRext01'

df_outlocs = gp.read_file(path_1D_outlocs)

distance = 300

pd.options.mode.chained_assignment = None

min_dis_max = 0
no_match = 0

# loop over all scenario's and simulations

appended_data_02 = []
for diri in dirs:
    ix = 0
    dirname = os.path.basename(os.path.normpath(diri))
    for OKid in OKids:
                   
        som_id = assignment[assignment['OKid']==OKid]['som_id']
        
        subdir = list_files_folders.list_folders(diri, dir_incl="ID%03d" % som_id)       
        subdir = subdir[0]
        
        files = list_files_folders.list_files('.TAB', subdir, startswith = False, endswith = True)
        subdirname = os.path.basename(os.path.normpath(subdir))
        scen_name = diri.split("\\")[-1]
        for file in files:
            f = os.path.basename(os.path.normpath(file))
            if f.startswith(outlocs_name):
                print(OKid)
                print(scen_name)
                print(f)
                data, headers = SWAN_read_tab.Freadtab(os.path.join(subdir,f))  
        
        match = (df_outlocs['HubName'] == OKid) & (df_outlocs['cngmeters'] == distance)
        if match.any(axis=0) == True:
            xq = df_outlocs[(df_outlocs['HubName'] == OKid) & (df_outlocs['cngmeters'] == distance)]['xcoord'].iloc[0]  
            yq = df_outlocs[(df_outlocs['HubName'] == OKid) & (df_outlocs['cngmeters'] == distance)]['ycoord'].iloc[0] 
            
            xx = data['Xp']
            yy = data['Yp']        
            
            dx = xx - xq
            dy = yy - yq
            dis = np.sqrt(dx**2 + dy**2)

            min_dis = np.min(dis)
            print('min distance = %.2f' % min_dis)
            row_ind = np.argmin(dis, axis=0)
            print('min index = %d' % row_ind)
            min_dis_max = max(min_dis, min_dis_max)
                   
            result  = data.iloc[[row_ind]]
            
            result['OkaderId'] = OKid
            result['Scenario'] = dirname
            result['min_dis'] = min_dis
            result['row_ind'] = row_ind
            appended_data_02.append(result)
            
            del data, result, dis, xx, yy, xq, yq  
            
        else:  
            print('OKid %s has no matching 1D profile' % OKid)
            no_match = no_match + 1
                       
appended_data_02 = pd.concat(appended_data_02)
print('maximum distace with SWAN output loc = %.2f' % min_dis_max)


#%% now write result to Excel

if save_excel:
    writer = pd.ExcelWriter(os.path.join(path_main,'output_productie_SWAN2D_WS.xlsx'), engine = 'xlsxwriter')
    appended_data_01.to_excel(writer, sheet_name = 'HRbasis')
    appended_data_02.to_excel(writer, sheet_name = 'HRext01')
    writer.save()
    writer.close()