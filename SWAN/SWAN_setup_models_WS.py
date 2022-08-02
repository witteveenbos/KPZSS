# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 15:35:37 2022

@author: ENGT2
"""

# load modules

import os
import pandas as pd
from hmtoolbox.WB_basic import replace_keywords

# Settings

dirs = {'main':     r'z:\130991_Systeemanalyse_ZSS\3.Models\SWAN\2D\Westerschelde\tests\batch_01',
        'bathy':    r'z:\130991_Systeemanalyse_ZSS\3.Models\SWAN\2D\Westerschelde\tests\_bodem',
        'grid':     r'z:\130991_Systeemanalyse_ZSS\3.Models\SWAN\2D\Westerschelde\tests\_rooster',
        'input':    r'z:\130991_Systeemanalyse_ZSS\3.Models\SWAN\2D\Westerschelde\tests\batch_01\input'}

files = {'swan_templ':  'template.swn',
         'scen_xlsx':   'scenarios_SWAN_2D_WS_v01.xlsx',
         'hyd_output':  'hydra_output_WS_waves.csv',
         'grid':        'swan_grid_cart_4.grd',
         'HRbasis':     'HRbasis.pnt',
         'HRext01':     'HRbasisPlus50m.pnt',
         'HRext02':     'HRextra.pnt'}

xl_scen = pd.ExcelFile(os.path.join(dirs['input'],files['scen_xlsx']))
df_scen = xl_scen.parse()

df_hyd  = pd.read_csv(os.path.join(dirs['input'],files['hyd_output']), sep=';',dtype={'ZSS-scenario':str})

# loop over scenario's

for ss in range(len(df_scen)):
    
    # make scenario directory
    dir_scen = os.path.join(dirs['main'], str(df_scen.Naam[ss]))
    if not os.path.exists(dir_scen):
        os.makedirs(dir_scen)

    # scenario input
    grd     = files['grid']
    bot     = df_scen.Bodem[ss]+'.bot'
    scenid  = df_scen.Naam[ss]
    zss     = df_scen.ZSS[ss]
    
    # condition input
    is_scen =  df_hyd['ZSS-scenario']==df_scen.ZSS_scenario[ss]
    df_hyd_scen = df_hyd[is_scen]
    
    for cc, row in df_hyd_scen.iterrows():
        wl          = df_hyd_scen['WL'][cc]
        ws          = df_hyd_scen['WS'][cc]
        wd          = df_hyd_scen['WD'][cc]
        hs_zn       = df_hyd_scen['HS_ZN'][cc]
        tp_zn       = df_hyd_scen['TP_ZN'][cc]
        dirw_zn     = df_hyd_scen['DIR_ZN'][cc]
        dspr_zn     = df_hyd_scen['DSPR_ZN'][cc]
        hs_d        = df_hyd_scen['HS_D'][cc]
        tp_d        = df_hyd_scen['TP_D'][cc]
        dirw_d      = df_hyd_scen['DIR_D'][cc]
        dspr_d      = df_hyd_scen['DSPR_D'][cc]
        hs_s        = df_hyd_scen['HS_S'][cc]
        tp_s        = df_hyd_scen['TP_S'][cc]
        dirw_s      = df_hyd_scen['DIR_S'][cc]
        dspr_s      = df_hyd_scen['DSPR_S'][cc]
        hs_zs       = df_hyd_scen['HS_ZS'][cc]
        tp_zs       = df_hyd_scen['TP_ZS'][cc]
        dirw_zs     = df_hyd_scen['DIR_ZS'][cc]
        dspr_zs     = df_hyd_scen['DSPR_ZS'][cc]
        gamma       = df_hyd_scen['GAMMA'][cc]
        locid       = str(df_hyd_scen['OKADER VakId'][cc])
        conid       = "WS%02dWD%03dHS%02dTP%02dDIR%03d" % (ws, wd, hs_s, tp_s, dirw_s)
        runid       = locid + '_' + conid
        swan_out    = runid + '.swn'
        
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
                        'GRD': grd,
                        'BOT': bot,
                        'WS': ws,
                        'WD': wd,
                        'GAMMA': gamma,
                        'HS_ZN': hs_zn,
                        'TP_ZN': tp_zn,
                        'DIR_ZN': dirw_zn,
                        'DSPR_ZN': dspr_zn,
                        'HS_D': hs_d,
                        'TP_D': tp_d,
                        'DIR_D': dirw_d,
                        'DSPR_D': dspr_d,
                        'HS_S': hs_s,
                        'TP_S': tp_s,
                        'DIR_S': dirw_s,
                        'DSPR_S': dspr_s,
                        'HS_ZS': hs_zs,
                        'TP_ZS': tp_zs,
                        'DIR_ZS': dirw_zs,
                        'DSPR_ZS': dspr_zs,
                        'HRbasis': files['HRbasis'],
                        'HRext01': files['HRext01'],
                        'HRext02': files['HRext02']}

        # make *swn-files
        
        replace_keywords.replace_keywords(os.path.join(dirs['input'], files['swan_templ']), 
                                          os.path.join(dir_run, swan_out), 
                                          keyword_dict, '<', '>')