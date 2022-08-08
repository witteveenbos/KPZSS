# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 15:35:37 2022

@author: ENGT2
"""

# load modules

import os
import pandas as pd
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
from hmtoolbox.WB_basic import replace_keywords
from hmtoolbox.WB_basic import save_plot

def interp_offshore_waves(df_offshore, windrichting, windsnelheid, savename):
    '''
    function to obtain offshore waves
    using both interpolation and extrapolation

    Parameters
    ----------
    df_offshore : TYPE
        DESCRIPTION.
    windrichting : TYPE
        DESCRIPTION.
    windsnelheid : TYPE
        DESCRIPTION.
    savename : TYPE
        DESCRIPTION.

    Returns
    -------
    Hs : interpolated or extrapolated wave height
    Tp : interpolated or extrapolated wave period

    '''
    # select directions
    df_golfrand_richting_selected = df_golfrand[df_golfrand['Windrichting'] == windrichting].reset_index()

    # perform interpolation and allow for extrapolation
    Hs = interpolate.interp1d(df_golfrand_richting_selected['Windsnelheid'].values, 
               df_golfrand_richting_selected['Golfhoogte'].values,fill_value='extrapolate')(windsnelheid)
    
    Tp = interpolate.interp1d(df_golfrand_richting_selected['Windsnelheid'].values, 
               df_golfrand_richting_selected['Golfperiode Tp'].values,fill_value='extrapolate')(windsnelheid)
    
    # print some data
    if windsnelheid > np.max(df_golfrand_richting_selected['Windsnelheid'].values):
        print(f'we extrapolated the windsnelheid of {windsnelheid:.2f} with richting of {windrichting:.2f}, resulting Hs {Hs:.2f} m and Tp {Tp:.2f} s')
    else:
        print(f'we interpolated the windsnelheid of {windsnelheid:.2f} with richting of {windrichting:.2f}, resulting Hs {Hs:.2f} m and Tp {Tp:.2f} s')
    
    # plot
    fig = plt.figure()
    plt.scatter(df_golfrand['Golfperiode Tp'],df_golfrand['Golfhoogte'],
                label='Alle windrichtingen')
    plt.scatter(df_golfrand_richting_selected['Golfperiode Tp'], df_golfrand_richting_selected['Golfhoogte'].values,
                label="Windrichting = %d graden" % windrichting)
    plt.scatter(Tp,Hs, c='red',label='Inter/extrapolatie')
    plt.text(Tp,Hs,"Hs = %.2f m, Tp = %.2f s" % (Hs, Tp))
    plt.legend()
    plt.title("Windrichting = %d graden, Windsnelheid = %.1f m/s\n" % (windrichting, windsnelheid))
    plt.xlabel('Golfperiode Tp (s)')
    plt.ylabel('Golfhoogte Hm0 (m)')
    plt.show()
    save_plot.save_plot(fig, savename)

    return float(Hs), float(Tp)

# Settings

dirs = {'main':     r'z:\130991_Systeemanalyse_ZSS\3.Models\SWAN\2D\Westerschelde\tests\batch_03',
        'bathy':    r'z:\130991_Systeemanalyse_ZSS\3.Models\SWAN\2D\Westerschelde\tests\_bodem',
        'grid':     r'z:\130991_Systeemanalyse_ZSS\3.Models\SWAN\2D\Westerschelde\tests\_rooster',
        'input':    r'z:\130991_Systeemanalyse_ZSS\3.Models\SWAN\2D\Westerschelde\tests\batch_02\input',
        'golfrand': r'z:\130991_Systeemanalyse_ZSS\2.Data\dummy\randvoorwaarden'}

files = {'swan_templ':  'template.swn',
         'qsub_templ':  'dummy.qsub',
         'scen_xlsx':   'scenarios_SWAN_2D_WS_v01.xlsx',
         'hyd_output':  'hydra_output_WS_waves.csv',
         'grid':        'swan_grid_cart_4.grd',
         'HRbasis':     'HRbasis.pnt',
         'HRext01':     'HR_voorland_rand.pnt',
         'HRext02':     'HR_voorland_rand_300m.pnt',
         'diepwaterrandvoorwaarden': 'HKV2010_diepwaterrandvoorwaarden.xlsx'}

node = 'despina'
ppn = 4

# Read scenario input

xl_scen = pd.ExcelFile(os.path.join(dirs['input'],files['scen_xlsx']),engine='openpyxl')
df_scen = xl_scen.parse()

# Read Hydra-NL output

df_hyd  = pd.read_csv(os.path.join(dirs['input'],files['hyd_output']), sep=';',dtype={'ZSS-scenario':str})

# Read diepwaterrandvoorwaarden

xl_golfrand = pd.ExcelFile(os.path.join(dirs['golfrand'],files['diepwaterrandvoorwaarden']),engine='openpyxl')
df_golfrand = xl_golfrand.parse(sheet_name = 'SCW',skiprows=1).drop([0,1])

# loop over scenario's

for ss in range(1):#range(len(df_scen)):
    
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
    
    # Loop over scenario's
    
    for cc, row in df_hyd_scen.iterrows():
        wl          = df_hyd_scen['WL'][cc]
        ws          = df_hyd_scen['WS'][cc]
        wd          = df_hyd_scen['WD'][cc]
        
        # determine offshore wave boundary
        locid       = str(df_hyd_scen['OKADER VakId'][cc])
        savename    = os.path.join(dir_scen, locid + '_wave_conditions.png')
        Hs_offshore, Tp_offshore = interp_offshore_waves(df_golfrand, wd, ws, savename)
        
        hs_zn       = 0.01 # zero boundary
        tp_zn       = Tp_offshore # dummy
        dirw_zn     = wd # dummy
        dspr_zn     = 30 # dummy
        
        hs_d        = Hs_offshore # obtained using linear interpolation on offshore diepwaterrandvoorwaarden
        tp_d        = Tp_offshore # obtained using linear interpolation on offshore diepwaterrandvoorwaarden
        dirw_d      = wd # assumption same as wind direction
        dspr_d      = 30 # default
        
        hs_s        = Hs_offshore # obtained using linear interpolation on offshore diepwaterrandvoorwaarden
        tp_s        = Tp_offshore # obtained using linear interpolation on offshore diepwaterrandvoorwaarden
        dirw_s      = wd # assumption same as wind direction
        dspr_s      = 30 # default
        
        hs_zs       = 0.01 # zero boundary
        tp_zs       = Tp_offshore # dummy
        dirw_zs     = wd # dummy
        dspr_zs     = 30 # dummy
        
        gamma       = 3.3 # default for all boundary conditions
        
        conid       = "WS%02dWD%03dHS%02dTP%02dDIR%03d" % (ws, wd, hs_s, tp_s, dirw_s)
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
        
        # make qsub files
        
        keyword_dict2 = {'NODE': node,
                         'PPN': ppn,
                         'RUNID': runid}
        
        replace_keywords.replace_keywords(os.path.join(dirs['input'], files['qsub_templ']), 
                                          os.path.join(dir_run, qsub_out), 
                                          keyword_dict2, '<', '>')