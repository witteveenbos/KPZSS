# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 14:25:16 2022

@author: ENGT2
"""

#%% import

import os
#import matplotlib
#matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
from hmtoolbox.WB_basic import list_files_folders
from hmtoolbox.WB_basic import save_plot
import datetime
from hmtoolbox.WB_basic import deg2uv
import scipy.io
from mpl_toolkits.axes_grid1 import make_axes_locatable
import gc

#%% settings

path_main_01 = r'z:\130991_Systeemanalyse_ZSS\3.Models\SWAN\2D\Waddenzee\04_sensitivity\01_bodem\G1_01'
path_main_02 = r'z:\130991_Systeemanalyse_ZSS\3.Models\SWAN\2D\Waddenzee\04_sensitivity\01_bodem\G2_01'

save_switch = False

figsize = (8,12)

vec_thinning = 40

#%% get directions with output data

dirs_01 = list_files_folders.list_folders(path_main_01, dir_incl='WZ_VM_01_050_F', startswith = True, endswith = False)
dirs_02 = list_files_folders.list_folders(path_main_02, dir_incl='WZ_VM_01_050_F', startswith = True, endswith = False)

if len(dirs_01) == len(dirs_01):
    print('== list of dirs for G1 is the same length as for G2')
else:
    print('== list of dirs for G1 is not the same length as for G2!')

#%% loop over directions and plot output
    
for diri in dirs_01:
    subdirs = list_files_folders.list_folders(diri, dir_incl='ID')
    for subdiri in subdirs:
        print('Start at {} doing stuff'.format(datetime.datetime.now()))
        files = list_files_folders.list_files('.mat',subdiri, startswith = False, endswith = False, recursive = True)
        file_01 = files[0]
        file_02 = file_01.replace('G1','G2')        
        subdir = os.path.basename(os.path.normpath(subdiri))
        title = subdir 
            
        #%% Read G1 output
        mat_01 = dict(scipy.io.loadmat(file_01))
        
        # Cut off dummy rows and columns 
        Xp_01 = mat_01['Xp'][:,:]
        Yp_01 = mat_01['Yp'][:,:]
        Botlev_01 = -1 * mat_01['Depth'][:,:]
                        
        Hsig_01 = mat_01['Hsig'][:,:]
        Tp_01 = mat_01['RTpeak'][:,:]
        direction_01 = mat_01['Dir'][:,:]
        
        # Convert the direction to u,v coordinates with scaling Hsig
        u_01,v_01 = deg2uv.deg2uv(direction_01,intensity=Hsig_01)
        
        #%% Read G2 output
        mat_02 = dict(scipy.io.loadmat(file_02))
        
        # Cut off dummy rows and columns 
        Xp_02 = mat_02['Xp'][:,:]
        Yp_02 = mat_02['Yp'][:,:]
        Botlev_02 = -1 * mat_02['Depth'][:,:]
                        
        Hsig_02 = mat_02['Hsig'][:,:]
        Tp_02 = mat_02['RTpeak'][:,:]
        direction_02 = mat_02['Dir'][:,:]
        
        # Convert the direction to u,v coordinates with scaling Hsig
        u_02,v_02 = deg2uv.deg2uv(direction_02,intensity=Hsig_02)
        
        #%% Plot results
        fig = plt.figure(figsize=figsize)
        
        # Hsig
        plt.subplot(3,1,1)
        plt.gca().set_aspect('equal')
        pcol = plt.pcolor(Xp_01,Yp_01,Hsig_01,cmap='jet')
        vmin, vmax = plt.gci().get_clim()
        pcol = plt.pcolor(Xp_02,Yp_02,Hsig_02,cmap='jet')
        # plt.quiver(Xp_01[::vec_thinning, ::vec_thinning],Yp_01[::vec_thinning, ::vec_thinning],
        #            u_01[::vec_thinning, ::vec_thinning],v_01[::vec_thinning, ::vec_thinning],color='black')
        # plt.quiver(Xp_02[::vec_thinning, ::vec_thinning],Yp_02[::vec_thinning, ::vec_thinning],
        #            u_02[::vec_thinning, ::vec_thinning],v_02[::vec_thinning, ::vec_thinning],color='black')
        
        plt.xlabel('x-coordinate [m]')
        plt.ylabel('y-coordinate [m]')
        
        plt.xlim(np.nanmin(Xp_01)-3e3,np.nanmax(Xp_01)+3e3)
        plt.ylim(np.nanmin(Yp_01)-3e3,np.nanmax(Yp_01)+3e3)
        plt.grid(visible=True, which='major', axis='both')
        plt.clim(vmin=vmin)
        plt.clim(vmax=vmax)
        
        ax = plt.gca()
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.275)
        plt.colorbar(pcol,cax = cax)
        plt.ylabel('Hsig (m)')
        
        # Tp
        plt.subplot(3,1,2)
        plt.gca().set_aspect('equal')
        pcol = plt.pcolor(Xp_01,Yp_01,Tp_01,cmap='jet')
        vmin, vmax = plt.gci().get_clim()
        pcol = plt.pcolor(Xp_02,Yp_02,Tp_02,cmap='jet')
        # plt.quiver(Xp_01[::vec_thinning, ::vec_thinning],Yp_01[::vec_thinning, ::vec_thinning],
        #            u_01[::vec_thinning, ::vec_thinning],v_01[::vec_thinning, ::vec_thinning],color='black')
        # plt.quiver(Xp_02[::vec_thinning, ::vec_thinning],Yp_02[::vec_thinning, ::vec_thinning],
        #            u_02[::vec_thinning, ::vec_thinning],v_02[::vec_thinning, ::vec_thinning],color='black')
        
        plt.xlabel('x-coordinate [m]')
        plt.ylabel('y-coordinate [m]')
        
        plt.xlim(np.nanmin(Xp_01)-3e3,np.nanmax(Xp_01)+3e3)
        plt.ylim(np.nanmin(Yp_01)-3e3,np.nanmax(Yp_01)+3e3)
        plt.grid(visible=True, which='major', axis='both')
        plt.clim(vmin=vmin)
        plt.clim(vmax=vmax)
        
        ax = plt.gca()
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.275)
        plt.colorbar(pcol,cax = cax)
        plt.ylabel('Tp (s)')
        
        # Depth
        plt.subplot(3,1,3)
        plt.gca().set_aspect('equal')
        pcol = plt.pcolor(Xp_01,Yp_01,Botlev_01,cmap='jet')
        plt.clim(vmin=-30, vmax=5)
        pcol = plt.pcolor(Xp_02,Yp_02,Botlev_02,cmap='jet')
        plt.clim(vmin=-30, vmax=5)
        
        plt.xlabel('x-coordinate [m]')
        plt.ylabel('y-coordinate [m]')
        
        plt.xlim(np.nanmin(Xp_01)-3e3,np.nanmax(Xp_01)+3e3)
        plt.ylim(np.nanmin(Yp_01)-3e3,np.nanmax(Yp_01)+3e3)
        plt.grid(visible=True, which='major', axis='both')
        
        ax = plt.gca()
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.275)
        plt.colorbar(pcol,cax = cax)
        plt.ylabel('Water depth (m)')
        
        #%% Save figure
        if save_switch:
            save_name = os.path.join(diri, 'figures', os.path.basename(os.path.normpath(subdiri) + '_results_combined.png'))
            save_plot.save_plot(fig, save_name, incl_wibo = False, dpi = 300, 
                      change_size = True, figwidth = 8, figheight = 10)
        #plt.close('all')
        #del fig
        print('End at {} doing stuff'.format(datetime.datetime.now()))
        gc.collect()