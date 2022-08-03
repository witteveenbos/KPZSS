# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 12:07:07 2022

@author: VERA7
"""
# import modules
import os
import numpy as np
import antconnect
from dotenv import load_dotenv

# %%All config vars and secrets should be put into environmental vars
# if they are present, set skipping it

dirname_of_this_file = os.path.dirname(__file__)

def get_api_connection(ant_platform='LIVE', env_file=None):
    """
    returns connected api class
    
    Args:
        None
    Kwargs:
        ant_platform - platform for which credentials are required
            default = 'BETA'
            can be ALPHA, BETA and LIVE
        env_file - location of env file None is default, then 'ant_key.evn'
            in this directory is used
    Returns:
        ant - connected antconnect api class
    """

    # load environment variables
    if env_file is None:
        env_file = os.path.join(dirname_of_this_file, 'ant_key.env')
    load_dotenv(env_file)

    # Extract them, and use as globals
    clientID = os.environ[f'{ant_platform}_CLIENT_ID']
    host = os.environ[f'{ant_platform}_HOST']
    clientSecret = os.environ[f'{ant_platform}_CLIENT_SECRET']
    username = os.environ[f'{ant_platform}_USERNAME']
    password = os.environ[f'{ant_platform}_PASSWORD']
    
    # connect to ant
    ant = antconnect.API(host)
    ant.login(clientID, clientSecret, username, password)
    
    ant.ant_platform = ant_platform
    ant.env_file = os.path.abspath(env_file)
    
    return ant

def get_project_id(ant, project_name):
    """gets project id by name"""
    #read all projects
    projects = ant.projects_read()
    
    #loop and find right name
    for project in projects:
        if project['name'] == project_name:
            #if right name found, store id and break
            project_id = project['id']
            return project_id
    raise UserWarning('project "{project_name}" not found')

def get_table_id(ant, project_id, tableName):
    """gets table id by name"""
    tables = ant.tables_read(project_id)
    for table in tables:
        if table['name'] == tableName:
            tableID = table['id']
            return tableID
    raise UserWarning('table "{tableName}" not found')

def find_id(records, cols_to_search, items_to_find):
    """
    returns the id of the first entry that matches items_to_find in cols_to_find
    
    For example:
        cols_to_search = ['Naam', 'Methode']
        items_to_find  = ['Waddenzee', 'IPM']
        
        records = [{'id': 'df2985bd-7aa4-4bf6-b745-a50054e7e5ce',
                     'Naam': 'Waddenzee',
                     'Methode': 'IPM'},
                    {'id': 'b228477c-c82b-459f-af89-407ff71f9a72',
                     'Naam': 'Westerschelde',
                     'Methode': 'IPM'},
                    {'id': 'fc04022d-896b-41a5-b305-e70c8a1cd547',
                     'Naam': 'Waddenzee',
                     'Methode': 'Database'},
                    {'id': '10958d59-f3dd-45f8-98c8-cce9c4a3dd2a',
                     'Naam': 'Hollandse IJssel',
                     'Methode': 'Database'},
                    {'id': '5d4bb442-1934-4258-b6cd-8eb226a8c627',
                     'Naam': 'Oosterschelde',
                     'Methode': 'Database'}]
        
        This will return:
            'df2985bd-7aa4-4bf6-b745-a50054e7e5ce'
        
    """
    # loop over all records
    for record in records:
        # check if all cols match
        if np.all([record[col]==item_to_find for col, item_to_find in zip(cols_to_search, items_to_find)]):
            found_id = record['id']
            return found_id
    
    raise UserWarning('Did not find the right record')
    