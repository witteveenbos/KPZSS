# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 14:48:23 2022

@author: VERA7
reads Stackfiles and groups databases into database sets

It does the following steps:
    1 - loop over all files in stack_file table 
    2 - if they are in the right folder, all files in a folder are coupled to a region and zeespiegel
        stijging --> to a database set
    3 - all files in the folder are individually filled into database_table
"""
# import python modules
import os

# import ant functions
from ant import ant_helper_functions as ant_funcs
# make api connection
ant_connection = ant_funcs.get_api_connection()

# specify stack folder that contains the databases
database_stack_root_folder = 'Hydraulische databases met achtergrond informatie'

# %% specify where to read, to fill, etc
project_name = 'Systeemanalyse Waterveiligheid'
stack_files_table = 'STACK_file'
database_table = 'DBM_HR_database'
database_set_table = 'DBM_HR_database_set'
region_table = 'Locatie_Regio'

# %% get the project and table ids
project_id = ant_funcs.get_project_id(ant_connection, project_name=project_name)
stack_files_table_id = ant_funcs.get_table_id(ant_connection, project_id, stack_files_table)

all_file_records = ant_connection.records_read(project_id, stack_files_table_id)

# %%
for stackfile in all_file_records:
    if stackfile['relative_location'].startswith(database_stack_root_folder):
        region = os.path.split(stackfile['relative_location'])[1]
        break