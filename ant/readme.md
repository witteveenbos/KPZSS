# How to use ANT

## Make connection

### First time connection
For first time use you need to create a file called "ant_key.env" in the folder "ant". **Don't commit this file. It contains your credentials**. This file should contain the following lines:

```
LIVE_HOST=https://api.antcde.io/
LIVE_USERNAME=<your username>
LIVE_PASSWORD=<your password>
LIVE_CLIENT_ID=<see below>
LIVE_CLIENT_SECRET=<see below>
```

You can create a token in ANT and fill in the cliend id and secret that belong to this token. 
The token can be made by clicking on your username a the bottom right and go to "profile settings".
The pane that opens contains the snippet below. Press new token to make one and copy the client id and client secret into the "ant_key.env"
![image](https://user-images.githubusercontent.com/68229914/181701896-8816896f-dd00-4c3e-a2dd-43320a9db912.png)

### Make API connection

If you have the "ant_key.env" in the "ant" folder and you installed the requirements (i.e. antconnect), you can make an api connection with ant with the following lines of code

```python
# import ant functions
from ant import ant_helper_functions as ant_funcs

# make api connection
ant_connection = ant_funcs.get_api_connection()

```

This connection will be used later on to read tables and upload to them, but also to work with sessions

## Upload to table

Upload to a table can be done with and without linking to a session. This example shows how to upload without a session:

```python
# specify where to put it
project_name = 'Systeemanalyse Waterveiligheid'
table_name = 'Calc_output'

# get the project and table id
project_id = ant_funcs.get_project_id(ant_connection, project_name=project_name)
table_id = ant_funcs.get_table_id(ant_connection, project_id, table_name)

# create a dict with a result. columns should have name of columns in output table
result_dict = {'Name' : 'vanuit python',
               'Number' : 10,
               'Correct' : True,
               'Use in next step' : True,
               'remarks' : None}
ant_connection.record_create(project_id, table_id, result_dict)

```

## Working with sessions

**Better description should be added**, for now, see [demo in this file]([../example/demo_upload.py](https://github.com/witteveenbos/KPZSS/blob/main/example/demo_upload.py))
