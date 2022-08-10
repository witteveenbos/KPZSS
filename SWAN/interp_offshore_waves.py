# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 08:43:31 2022

@author: ENGT2
"""

import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
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
    df_golfrand_richting_selected = df_offshore[df_offshore['Windrichting'] == windrichting].reset_index()

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
    plt.scatter(df_offshore['Golfperiode Tp'],df_offshore['Golfhoogte'],
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

    return float(Hs), float(Tp), fig