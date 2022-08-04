# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 14:59:48 2022

@author: BEMC
"""

import matplotlib.pyplot as plt
import numpy as np
from hmtoolbox.WB_SWAN import SWAN_read_tab

path = 'z:\\130991_Systeemanalyse_ZSS\\3.Models\\SWAN\\1D\\tests\\'
data, headers = SWAN_read_tab.Freadtab(path+'uitvoer.txt')

data['Hsig'][data['Hsig']<=0] = np.nan

data['Tm_10'][data['Tm_10']<=0] = np.nan

#%% plotting
plt.figure(figsize=(6,7))
ax1 = plt.subplot(2,1,1)
ax1_copy = ax1.twinx()

ax1.plot(data['Xp'],data['Botlev'],'k',label = 'bathymetrie')
ax1.plot(data['Xp'], data['Watlev'], 'b--', label = 'waterstand')
ax1.set_ylabel('hoogte [m+NAP]')

ax1_copy.plot(data['Xp'], data['Hsig'],'g')#, label = '$H_s$ [m]')
ax1_copy.set_ylabel('$H_s$ [m]',color='g')
ax1_copy.tick_params(labelcolor='g')
plt.xlabel('afstand [m]')
#plt.legend()
plt.title(path+'uitvoer.txt')

ax2 = plt.subplot(2,1,2)
ax2_copy = ax2.twinx()
ax2.plot(data['Xp'],data['Botlev'],'k',label = 'bathymetrie')
ax2.plot(data['Xp'], data['Watlev'], 'b--', label = 'waterstand')
ax2.set_ylabel('hoogte [m+NAP]')

ax2_copy.plot(data['Xp'], data['Tm_10'],color='orange')
ax2_copy.set_ylabel('$H_s$ [m]',color='orange')
ax2_copy.tick_params(labelcolor='orange')
ax2_copy.set_ylabel('$T_{m-1,0}$ [s]')



