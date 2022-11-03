# -*- coding: utf-8 -*-
"""
--- Synopsis --- 
This scripts does the following things:
    - reads output of SWAN1D simulations for Waddenzee
    - calculates differences between SWAN1D and SWAN2D outputat location 300m from dyke
    - changes boundary conditions of SWAN1D run based on difference at 300m location
    - generates input for new SWAN1D run
    - plots results of SWAN 1D run

--- Remarks --- 
See also: 
To-Do: 
Dependencies: 

--- Version --- 
Created on Thu Sep 29 09:17:28 2022
@author: ENGT2
Project: KP ZSS (130991)
Script name: read_SWAN_1D_model_WZ_iteratie_productie.py 

--- Revision --- 
Status: Unverified 

Witteveen+Bos Consulting Engineers 
Leeuwenbrug 8
P.O. box 233 
7411 TJ Deventer
The Netherlands 
		
"""

#%% Import modules

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from hmtoolbox.WB_SWAN import SWAN_read_tab
from hmtoolbox.WB_basic import list_files_folders
from hmtoolbox.WB_basic import save_plot
import shutil
# %pylab qt
import gc
import xlsxwriter

#%% Settings

# main
path_main = r'Z:\130991_Systeemanalyse_ZSS\3.Models\SWAN\1D\Waddenzee\02_productie\iter_03'
path_results_1D = r'Z:\130991_Systeemanalyse_ZSS\3.Models\SWAN\1D\Waddenzee\02_productie\iter_03\WZ_NM_01_000_RF'
path_profile_info = r'Z:\130991_Systeemanalyse_ZSS\3.Models\SWAN\1D\Waddenzee\02_productie\_bodem\profile_info_SWAN1D_WZ.xlsx'

tab_files = list_files_folders.list_files('.TAB',path_results_1D)

# input SWAN 1D
path_input = r'Z:\130991_Systeemanalyse_ZSS\3.Models\SWAN\1D\Waddenzee\02_productie\iter_01\input'
file_input = r'output_productie_SWAN2D_WZ.xlsx'

save_fig = True

new_iteration = False

save_result = False

# path with new iteration
path_new = r'Z:\130991_Systeemanalyse_ZSS\3.Models\SWAN\1D\Waddenzee\03_productie_vegetatie\iter_0x'

Xp_300 = 300
# Xp_basis = 99.8

#%% Load tab_file with simulation input

# Output at locations 'HRext01' (see .swan-file)
outloc = 'HRext01'

xl_input  = pd.ExcelFile(os.path.join(path_input, file_input),engine='openpyxl')
df_input = xl_input.parse(sheet_name = outloc)

# Output at locations 'HRbasis' (see .swan-file)
outloc = 'HRbasis'

xl_basis  = pd.ExcelFile(os.path.join(path_input, file_input),engine='openpyxl')
df_basis = xl_basis.parse(sheet_name = outloc)

# Excel with info on 1D profiles (orientation)
xl_profile  = pd.ExcelFile(path_profile_info,engine='openpyxl')
df_profile  = xl_profile.parse()
df_profile['Xp_teen'] = np.nan

#%% loop trough SWAN1D simulations, plot results, prepare input for new simulations (new iteration)

appended_output = []


for tab_file in tab_files:

    if 'WZ_NM_01_000_RF' in tab_file:
        
        # get relevant names from filename
        scene = tab_file.split('\\')[-3]
        simulation = tab_file.split('\\')[-2]
        loc = simulation.split('_')[0][2:]
        
        if scene == 'WZ_NM_01_000_RF':
            # output path 
            output_path = os.path.join(path_main,scene)

            data, headers = SWAN_read_tab.Freadtab(tab_file)
            data['Botlev'][data['Botlev']<-20] = -10
            
            #%% Determine location toe of dike (defined as first location where slope > 1/10, as seen from dyke)
            
            ii = 0
            slope = list()
            Xpteen = data['Xp'].iloc[-1]
            Ypteen = data['Yp'].iloc[-1]
            for x1, x2, y1, y2 in zip(data['Xp'][1:40], data['Xp'][:41], data['Botlev'][1:40], data['Botlev'][:41]):
                dx = x1 - x2
                dy = y1 - y2
                if dy == 0:
                    dydx = 0
                else:
                    dydx = dy/dx
                    if dydx <= 1/10 and ii == 0:
                        Xpteen = x1
                        Ypteen = y2
                        ii = ii +1             
                slope.append(dydx)
            if ii == 0:
                slope_max = np.nanmax(slope)
                slope_max_ind = np.nanargmax(slope)
                Xpteen = data['Xp'][slope_max_ind]

            # print(Xpteen)
        df_profile['Xp_teen'].loc[(df_profile['OkaderId']==float(loc)) & (df_profile['Scenario'] == scene)] = Xpteen
        # max_slope = max(slope)
        # imax = np.argmax(slope)

savename = os.path.join(r"D:\Users\BADD\Desktop\KP ZSS", 'profile_info_SWAN1D_WZ_v3.xlsx')
df_profile.to_excel(savename, index = False)
