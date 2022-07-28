# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 12:04:36 2022

@author: VERA7
"""
# import python modules
import datetime

# import own modules
from ant import ant_helper_functions as ant_funcs

# %% set some variables
project_name = 'Systeemanalyse Waterveiligheid'
session_name = 'voorbeeld sessie databasemethode'
output_table = 'Calc_output'

# %% 
# make api connection
ant_connection = ant_funcs.get_api_connection()

# get ids required to do the analysis
project_id = ant_funcs.get_project_id(ant_connection, project_name=project_name)
signed_in_user_uuid = ant_connection._make_api_request('user', 'GET')['id']

# get first open task
runs = ant_connection.tasks_read(project_id=project_id, status='open',
                                 user=signed_in_user_uuid)

for task_dict in runs:
    # get job
    job = ant_connection.task_getJob(project_id, task_dict['id']) 
    
    # check if this is the one we want
    if not isinstance(job, bool) and job['session_object']['name'] == session_name:
        print(task_dict)        
        print(f"=== \n printing job {job} \n ===")
        
        break

# %% set task to pending
datestring = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
ant_connection.task_respond(task_id=task_dict['id'], 
                         status='processing',
                         response=f"processing at {datestring}", 
                         appendix=None,
                         assigned_user=signed_in_user_uuid, #can be removed once implemented in ANT
                         due_date=task_dict['due_date']) #can be removed once implemented in ANT

# %% do a simple upload to output table
table_id = ant_funcs.get_table_id(ant_connection, project_id, output_table)

# create a dict with a result. columns should have name of columns in output table
result_dict = {'Name' : 'vanuit python',
               'Number' : 10,
               'Correct' : True,
               'Use in next step' : True,
               'remarks' : None}

ant_connection.record_create(project_id, table_id, result_dict, session=job['session'])

# %% finish the job
ant_connection.job_finish(project_id, job['id'])
