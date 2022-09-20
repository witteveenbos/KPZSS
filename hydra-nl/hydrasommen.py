 # -*- coding: utf-8 -*-
"""
Created on Thu May 14 08:32:24 2020

@author: BADD
"""


from pathlib import Path
import csv
import os
import pandas
import numpy as np


# Set paths
profile_dir = Path(r'C:\MyPrograms\Hydra-NL_KP_ZSS\profielen_productie')
os.chdir(profile_dir)
data_profielen = pandas.read_csv(r'D:\Users\BADD\Desktop\KP ZSS\GIS\new_1309\okader_fc_hydra_overzicht_v2.csv')

# strip taludhelling van bijvoorbeeld: 1op5 naar 5
data_profielen['FC_Tld'] = data_profielen['FC_Tld'].str[-1:]

count = 0

# loop over gehele csv om profielen te schrijven    
for i in range(0,len(data_profielen)):
    count += 1

    file = open(f"%s.prfl" %data_profielen['VakId'].loc[i],"w")
    txt=['VERSIE    4.0',
        'ID'  f'   %s' %data_profielen['VakId'].loc[i],
        '',
        f'RICHTING	%.2f'  %data_profielen['FC_DN'].loc[i],
        '',
        'DAM   0',
        'DAMHOOGTE     0',
        '',
        'VOORLAND     0',  
        '',    
        'DAMWAND  0',           

        f'KRUINHOOGTE  %.2f'   %data_profielen['FC_KH'].loc[i],


        'DIJK     2',

        f'-%.2s0.000  0.000 1.000' %data_profielen['FC_Tld'].loc[i],
        '0.000	10.000	1.000',
        '', 
        'MEMO', 
        '', 
        '']
    file.write('\n'.join(txt))    
    file.close()

    del file, txt    
        

# loop nogmaals om csv te schrijven waar hydra de info uit haalt
filecsv = r"D:\Users\BADD\Desktop\KP ZSS\profielen_productie.csv"
with open(filecsv, 'w') as f:
    f.write("Locatie;X-coordinaat;Y-coordinaat;Profiel;Directory\n")

    for i in range(0,len(data_profielen)):
        f.write(f"{data_profielen['Name'].loc[i]};{data_profielen['XCoordinat'].loc[i]};{data_profielen['YCoordinat'].loc[i]};{data_profielen['VakId'].loc[i]};")
        f.write("..\\profielen_productie\n")
