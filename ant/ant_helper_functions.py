# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 12:07:07 2022

@author: VERA7
"""
# import modules
import os
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