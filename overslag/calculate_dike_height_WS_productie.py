# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 15:14:52 2022

@author: ESB
"""

import os
import geopandas as gpd
import pandas as pd
import numpy as np

from overtopping import overtopping

# settings
path_input      = r'z:\130991_Systeemanalyse_ZSS\5.Results\SWAN\WS\concept02\output_productie_combined_WS_v04.xlsx'
path_locations  = r'd:\Users\ENGT2\Documents\Projects\130991 - SA Waterveiligheid ZSS\GIS\illustratiepunten_methode\shape + 1d-flag\okader_fc_hydra_unique_handedit_WS_havens_berm_1d-flag.shp'
path_out        = r'z:\130991_Systeemanalyse_ZSS\5.Results\SWAN\WS\concept02'

save_excel = False

# Load data
combinations = pd.read_excel(path_input)
locations = gpd.read_file(path_locations)

# Create new dataframe
dikeheight = pd.DataFrame({'OkaderId':[],
                           'FC_VakID':[],
                           'Scenario':[],
                           'DikeHeight':[]})

for index, combination in combinations.iterrows():
    print(f'Calculating combination {index}')
    # Combine with locations (could be multiple)
    vakid = locations[locations['VakId']==str(combination.OkaderId)]
    for location_index in range(len(vakid)):
        location = vakid.iloc[location_index]
        # Variables for overtopping discharge
        Hm0 = combination.Hsig
        Tm = combination.Tm_10
        slope = 1/float(location.FC_Tld[-1])
        yb = float(location.y_b)
        betaw = abs(int(location.FC_DN)-combination.Dir)
        yf = 1
        yv = 1
        
        # Estimate overtopping discharge every cm
        Rc = np.arange(25,-0.02,-0.01)
        q = np.zeros(Rc.shape)
        for i, RC in enumerate(Rc):
            q[i] = overtopping(np.array(Hm0),np.array(Tm),np.array(slope),np.array(RC), 
                        betaw = betaw, yf = yf, yb = yb, yv = yv, 
                        ed = 2007, ctype = 'det')
            # Stop if overtopping discharge reaches limit
            if q[i] > location.FC_q/1000:
                break
        
        #Calculate dikeheight
        DikeHeight = combination.Watlev + Rc[i-1]
        dikeheight = dikeheight.append({'OkaderId':combination.OkaderId,
                                        'FC_VakID': location.FC_VakID,
                                        'Scenario': combination.Scenario,
                                        'DikeHeight': DikeHeight}, ignore_index=True)

# Write results
if save_excel: 
    dikeheight.to_excel(os.path.join(path_out,'DikeHeight.xlsx'), index=False)