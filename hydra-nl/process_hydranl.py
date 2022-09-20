from cmath import nan
from operator import contains, index
import string
from reader import lees_invoerbestand, lees_uitvoerhtml, lees_illustratiepunten, lees_ofl
from pathlib import Path
import os
import pandas as pd
import numpy as np


hydra_werkmap = r"C:\MyPrograms\Hydra-NL_KP_ZSS\werkmap"
okader_norm_csv = pd.read_csv(r"D:\Users\BADD\Desktop\KP ZSS\kust\koppelingen\Pf_Vak_Eis_20220718.csv", delimiter=';')
df_hydra_definition = pd.read_csv(r"D:\Users\BADD\Desktop\KP ZSS\GIS\new_1309\okader_fc_hydra_overzicht_v2.csv")

# toevoegen orientatie dijknormaal

hydra_results = {
    'OKADER VakId':[], 
    'Uitvoerbestand':[], 
    'Terugkeertijd':[], 
    'q [m3/s/m]':[], 
    'ZSS-scenario':[], 
    'HYD_location_name':[], 
    'HYD_location_X':[], 
    'HYD_location_Y':[], 
    'Profiel':[],
    'HBN [m+NAP]':[], 
    'Zeewaterstand [m+NAP]':[], 
    'windsnelheid [m/s]':[], 
    'h, teen [m+NAP]': [], 
    'Hm0, teen [m]':[], 
    'Tm-1.0, ts':[], 
    'golfrichting [graden]':[], 
    'windrichting [graden N]':[], 
    'bijdrage ov. freq [%]':[]}


for folder in os.listdir(hydra_werkmap):

    # geïnteresseerd in de data van generieke database-namen
    # string_to_match = ["Westerschelde", "Waddenzee"]
    string_to_match = ["Westerschelde"]

    for substring in string_to_match:
        if substring in folder:

            #zoek naar folders met string_to_match
            for root, dirs, files in os.walk(os.path.join(hydra_werkmap, folder)):
                if "sensitivity" in root:
                    for file in files:
                        # print(folder)
                        # op basis van invoer.hyd de eerste kolommen vullen van output
                        if file.endswith('invoer.hyd'):
                            location_invoer = os.path.join(root, file)
                            invoer, terugkeertijden = lees_invoerbestand(location_invoer)
                            

                            # path van profiel staat in invoer, strip tot naam profiel
                            profielpath = invoer['algemeen']['PROFIEL']
                            valueprofiel = profielpath.split("\\")[-1]
                            valueprofiel = valueprofiel[:-1]
                            value = valueprofiel.split(".")[0]

                            hydra_results['OKADER VakId'].append(value)
                            hydra_results['q [m3/s/m]'].append(invoer['criterium']['QCR'])
                            hydra_results['Uitvoerbestand'].append(invoer['algemeen']['UITVOERBESTAND'])
                            hydra_results['ZSS-scenario'].append(invoer['algemeen']['SCENARIONAAM'])
                            hydra_results['HYD_location_name'].append(invoer['algemeen']['LOCATIE'])
                            hydra_results['HYD_location_X'].append(invoer['algemeen']['XCOORDINAAT'])
                            hydra_results['HYD_location_Y'].append(invoer['algemeen']['YCOORDINAAT'])
                            hydra_results['Profiel'].append(valueprofiel)
                            
                            # haal ondergrens norm op uit de excel
                            for i in range(len(okader_norm_csv['VAK'])):
                                if okader_norm_csv['VAK'].loc[i] == int(value):
                                    req_terugkeertijd = okader_norm_csv['T_eis_hbn'].loc[i]


                        # op basis van uitvoer de andere kolommen vullen van dataframe
                        elif file.endswith('uitvoer.html'):
                            location_uitvoer = os.path.join(root, file)
                            tekst = lees_uitvoerhtml(location_uitvoer)
                            cips, ip = lees_illustratiepunten(tekst)
                            ofl = lees_ofl(tekst)
                            # print(ip)


                            # # check if this results in 2 illustratiepunten
                            a = (ip['bijdrage ov. freq (%)'].loc[[req_terugkeertijd][0]])
                            if a.size > 1:
                                rel_ip = ip.loc[[req_terugkeertijd][0]]
                                rel_ip = rel_ip.iloc[np.argmax(rel_ip['h,teen m+NAP'])]

                            else:
                                rel_ip = ip.loc[[req_terugkeertijd][0]]
                        
                            # if (range(ip['bijdrage ov. freq (%)'].loc[[req_terugkeertijd][0]])) > 1:
                            #     print('yes')
                            #     # in that case, we just need the one with the heighest water level
                            #     rel_ip = ip.loc[vak['Norm_frequentie']]
                            #     rel_ip = rel_ip.iloc[np.argmax(rel_ip['h,teen m+NAP'])]
                            # # if not, we can just get the first one
                            # else:
                            # # get the relevant ip
                            #     rel_ip = ip.loc[vak['Norm_frequentie']]


                            hydra_results['Terugkeertijd'].append(req_terugkeertijd)

                            # in dezelfde map data ophalen van berekeningen afhankelijk van norm geldend bij Okader VakID
                            hydra_results['HBN [m+NAP]'].append(ofl['hoogte'].loc[[req_terugkeertijd][0]])
                            hydra_results['Zeewaterstand [m+NAP]'].append(rel_ip['zeews. m+NAP'])
                            hydra_results['windsnelheid [m/s]'].append(rel_ip['windsn. m/s'])
                            hydra_results['h, teen [m+NAP]'].append(rel_ip['h,teen m+NAP'])
                            hydra_results['Hm0, teen [m]'].append(rel_ip['Hm0,teen m'])
                            hydra_results['Tm-1.0, ts'].append(rel_ip['Tm-1,0,t s'])
                            hydra_results['golfrichting [graden]'].append(rel_ip['golfr graden'])
                            hydra_results['windrichting [graden N]'].append(rel_ip['r'])
                            hydra_results['bijdrage ov. freq [%]'].append(rel_ip['bijdrage ov. freq (%)'])


                            # hydra_results['windsnelheid [m/s]'].append(rel_ip['windsn. m/s'].loc[[req_terugkeertijd][0]])
                            # hydra_results['h, teen [m+NAP]'].append(rel_ip['h,teen m+NAP'].loc[[req_terugkeertijd][0]])
                            # hydra_results['Hm0, teen [m]'].append(rel_ip['Hm0,teen m'].loc[[req_terugkeertijd][0]])
                            # hydra_results['Tm-1.0, ts'].append(rel_ip['Tm-1,0,t s'].loc[[req_terugkeertijd][0]])
                            # hydra_results['golfrichting [graden]'].append(rel_ip['golfr graden'].loc[[req_terugkeertijd][0]])
                            # hydra_results['windrichting [graden N]'].append(rel_ip['r'].loc[[req_terugkeertijd][0]])
                            # hydra_results['bijdrage ov. freq [%]'].append(rel_ip['bijdrage ov. freq (%)'].loc[[req_terugkeertijd][0]])


          
df = pd.DataFrame(hydra_results)

savename = os.path.join(r"D:\Users\BADD\Desktop\KP ZSS\kust\output\HBN", f"{string_to_match}" + '_HBN_v3_sensitivity.csv')
df.to_csv(savename, sep = ';', index = False)


