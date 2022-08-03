# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 14:48:23 2022

@author: VERA7
reads Stackfiles and groups databases into database sets for DB method

It does the following steps:
    1 - loop over all files in stack_file table 
    2 - if they are in the right folder, we check the subfolder structure to get:
        - all relevant regions
        - all zss-options
        
        this is used to make a database set
        
    3 - all files in the folder are individually filled into database_table
"""
# import python modules
import numpy as np

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
database_table_id = ant_funcs.get_table_id(ant_connection, project_id, database_table)
database_set_table_id = ant_funcs.get_table_id(ant_connection, project_id, database_set_table)
region_table_id = ant_funcs.get_table_id(ant_connection, project_id, region_table)

# %% read relevant records
all_file_records = ant_connection.records_read(project_id, stack_files_table_id)
region_records = ant_connection.records_read(project_id, region_table_id)

# %% filter out the stackfiles we want
relevant_stack_file_records = [stackfile for stackfile in all_file_records \
                               if stackfile['relative_location'].startswith(database_stack_root_folder)]

# %% find all regions that are relevant
unique_regions = np.unique([stackfile['relative_location'].split('/')[1] for stackfile in relevant_stack_file_records])

# %% loop over regions, make a database set per subfolder and then add the database files
for region in unique_regions:
    # find the right id
    region_id = ant_funcs.find_id(records=region_records,
                                  cols_to_search=['Naam'], 
                                  items_to_find=[region])
    
    # get the records for this region
    region_stack_file_records = [stackfile for stackfile in all_file_records \
                                   if stackfile['relative_location'].split('/')[1] == region]
    
    # list subfolders
    number_folder = 3
    options = np.unique([stackfile['relative_location'].split('/')[number_folder] for stackfile in region_stack_file_records\
                         if 'ZSS' in stackfile['relative_location'].split('/')[number_folder] and \
                             'cm' in stackfile['relative_location'].split('/')[number_folder]])
    
    # loop over all options, make database set and list files
    for option in options:
        # capture zss
        zss = float(option.split('-')[1])
        
        # extract extra info 
        extra_info = option.split('cm-')[-1]
        if extra_info == option:
            extra_info = None
        
        # create database_set
        database_set_dict = {'Regio_id' : region_id,
                               'Zeespiegelstijging_CM' : zss,
                               'Extra_info' : extra_info}
        db_set_record = ant_connection.record_create(project_id, database_set_table_id, 
                                                         database_set_dict)
        
        # now capture the relevant files and make database items from them
        option_stack_file_records = [stackfile for stackfile in region_stack_file_records \
                                       if stackfile['relative_location'].split('/')[number_folder] == option]
            
        for stack_file in option_stack_file_records:
            # make entry
            db_record_dict = {'STACK_file_ID' : stack_file['id'],
                          'HR_database_set_ID' : db_set_record['id']}
            
            ant_connection.record_create(project_id, database_table_id, 
                                                             db_record_dict)
