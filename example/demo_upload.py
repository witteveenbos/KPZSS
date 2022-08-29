# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 12:04:36 2022

@author: VERA7
The following steps are required to upload data to a session
1. Specify:
   1. Which session you are working on (name);
   2. Which task (block) you are working on (name);
   3. which table you want to put your results in at top of the script;
2. Get the job in the session;
3. Set it on processing (just because we can);
4. Upload the data
5. Close the job. 
"""
# import python modules
import datetime

# import own modules
from ant import ant_helper_functions as ant_funcs

# %% set some variables
project_name = 'Systeemanalyse Waterveiligheid'

# step 1: specify 
session_name = 'test_new'
task_name = 'calc'
output_table = 'Calc_output'

# %% step 2: get the job in the session
# make api connection
ant_connection = ant_funcs.get_api_connection()

# get ids required to do the analysis
project_id = ant_funcs.get_project_id(ant_connection, project_name=project_name)
signed_in_user_uuid = ant_connection._make_api_request('user', 'GET')['id']

# get first open task
runs = ant_connection.tasks_read(project_id=project_id, status='open',
                                 user=signed_in_user_uuid)

found_job = False
for task_dict in runs:
    # get job
    job = ant_connection.task_getJob(project_id, task_dict['id']) 
    
    # check if this is the one we want
    if not isinstance(job, bool) and job['session_object']['name'] == session_name \
        and job['task']['name'] == f'{task_name} Task':    
            print("=== \nFound job\n===")
            found_job = True
            break
if not found_job:
    raise UserWarning('Did not find the right job. Did you assign the job to yourself?')

# %% step 3: set task to pending
datestring = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
ant_connection.task_respond(task_id=task_dict['id'], 
                         status='processing',
                         response=f"processing at {datestring}", 
                         appendix=None,
                         assigned_user=signed_in_user_uuid, #can be removed once implemented in ANT
                         due_date=task_dict['due_date']) #can be removed once implemented in ANT

# %% step 4: do a simple upload to output table
table_id = ant_funcs.get_table_id(ant_connection, project_id, output_table)

# create a dict with a result. columns should have name of columns in output table
result_dict = {'Name' : 'vanuit python',
               'Number' : 10,
               'Correct' : True,
               'Use in next step' : True,
               'remarks' : None}

ant_connection.record_create(project_id, table_id, result_dict, session=job['session'])

# %% step 5: finish the job
ant_connection.job_finish(project_id, job['id'])
