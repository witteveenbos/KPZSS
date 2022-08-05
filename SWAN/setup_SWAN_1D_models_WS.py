# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 17:12:02 2022

@author: BEMC
"""

# load modules

import os
import pandas as pd
from hmtoolbox.WB_basic import replace_keywords

# Settings

dirs = {'main':     r'z:\130991_Systeemanalyse_ZSS\3.Models\SWAN\1D\Westerschelde\tests\test_03',
        'bathy':    r'z:\130991_Systeemanalyse_ZSS\3.Models\SWAN\1D\Westerschelde\tests\_bodem',
        'input':    r'z:\130991_Systeemanalyse_ZSS\3.Models\SWAN\1D\Westerschelde\tests\test_03\input'}

files = {'swan_templ':  '1D_swanfile_template.swn',
         'qsub_templ':  'dummy.qsub',
         'scen_xlsx':   'scenarios_SWAN_1D_WS_v03.xlsx',
         'hyd_output':  'SWAN2D_output_WS.csv'}

node = 'triton'
ppn = 1

# Read scenario input

xl_scen = pd.ExcelFile(os.path.join(dirs['input'],files['scen_xlsx']),engine='openpyxl')
df_scen = xl_scen.parse()

# Read Hydra-NL output

df_hyd  = pd.read_csv(os.path.join(dirs['input'],files['hyd_output']), sep=';',dtype={'ZSS-scenario':str})

# loop over scenario's

for ss in range(len(df_scen)):
    
    # make scenario directory
    dir_scen = os.path.join(dirs['main'], str(df_scen.Naam[ss]))
    if not os.path.exists(dir_scen):
        os.makedirs(dir_scen)

    # scenario input
    bot     = df_scen.Bodem[ss]+'_bottom.txt'
    scenid  = df_scen.Naam[ss]
    zss     = df_scen.ZSS[ss]
    
    # condition input
    is_scen =  df_hyd['ZSS-scenario']==df_scen.ZSS_scenario[ss]
    print(df_scen.ZSS_scenario[ss])
    print(is_scen)
    df_hyd_scen = df_hyd[is_scen]
    
    # Loop over scenario's
    
    for cc, row in df_hyd_scen.iterrows():
        wl          = df_hyd_scen['WL'][cc]
        ws          = df_hyd_scen['WS'][cc]
        wd          = df_hyd_scen['WD'][cc]
        hs       = df_hyd_scen['HS'][cc]
        tp       = df_hyd_scen['TP'][cc]
        dirw     = 180
        dspr     = 30
        gamma       = 3.3
        locid       = str(df_hyd_scen['OKADER VakId'][cc])
        conid       = "WS%02dWD%03dHS%02dTP%02dDIR%03d" % (ws, wd, hs, tp, dirw)
        runid       = 'ID' + locid + '_' + conid
        swan_out    = runid + '.swn'
        qsub_out    = runid + '.qsub'
        
        #
        # CONSIDER skipping lines 54-73 and putting this directly into keyword_dict
        #
        # FILTERING NEEDS TO BE DONE ON WAVE CONDITIONS, REMOBE DUBPLICATE CONDITIONS
        #
        
        # make scenario directory
        dir_run = os.path.join(dir_scen, runid)
        if not os.path.exists(dir_run):
            os.makedirs(dir_run)
            
        keyword_dict = {'LOCID': locid,
                        'RUNID': runid,
                        'LEVEL': wl,
                        'BOT': bot,
                        'WS': ws,
                        'WD': wd,
                        'GAMMA': gamma,
                        'HS': hs,
                        'TP': tp,
                        'DIR': dirw,
                        'DSPR': dspr}

        # make *swn-files
        
        replace_keywords.replace_keywords(os.path.join(dirs['input'], files['swan_templ']), 
                                          os.path.join(dir_run, swan_out), 
                                          keyword_dict, '<', '>')
        
        # make qsub files
        
        keyword_dict2 = {'NODE': node,
                         'PPN': ppn,
                         'RUNID': runid}
        
        replace_keywords.replace_keywords(os.path.join(dirs['input'], files['qsub_templ']), 
                                          os.path.join(dir_run, qsub_out), 
                                          keyword_dict2, '<', '>')