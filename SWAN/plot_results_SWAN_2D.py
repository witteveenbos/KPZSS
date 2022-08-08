# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 15:44:00 2022

@author: ENGT2
"""

import os
import matplotlib.pyplot as plt
import numpy as np
from hmtoolbox.WB_SWAN import SWAN_quickplot
from hmtoolbox.WB_basic import list_files_folders
from hmtoolbox.WB_basic import save_plot

main_path = r'z:\130991_Systeemanalyse_ZSS\3.Models\SWAN\2D\Westerschelde\tests\batch_02\WS_VT_06_300_A2'
output_path = r'z:\130991_Systeemanalyse_ZSS\3.Models\SWAN\2D\Westerschelde\tests\batch_02\WS_VT_06_300_A2\figures'

files = list_files_folders.list_files('.mat',main_path, startswith = False, endswith = False, recursive = True)
dirs = list_files_folders.list_folders(main_path, dir_incl='ID')

params  = ['Hsig','RTpeak','Depth']
labels  = ['Hsig (m)','Tp (s)', 'Bed level (m)']

for diri in dirs:
    files = list_files_folders.list_files('.mat',diri, startswith = False, endswith = False, recursive = True)
    file = files[0]
    subdir = os.path.basename(os.path.normpath(diri))
    title = subdir 
    fig = SWAN_quickplot.SWAN_quickplot_2D(file, parameters=params, parameters_clabel=labels, name=title,
                      coord_unit='m', cmap='jet', quivers = True, contours = False, vec_thinning=50, 
                      wat_lev=0, vmin=False, vmax=False, sf=False, figsize = (8,12), rows=3, columns=1)
    
    save_name = os.path.join(output_path, subdir + '_results.png')
    save_plot.save_plot(fig, save_name, incl_wibo = False, dpi = 300, 
                  change_size = True, figwidth = 8, figheight = 10)