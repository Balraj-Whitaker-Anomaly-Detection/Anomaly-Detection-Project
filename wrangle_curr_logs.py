#!/usr/bin/env python
# coding: utf-8

# ## Acquire Data from the SQL DB

# In[15]:


def get_curriculum_logs():
    
    # imports
    import os
    import env
    import pandas as pd
    
    filename = "curr_logs.csv"

    if os.path.isfile(filename):
        return pd.read_csv(filename, index_col=False)
    else:
        # read the SQL query into a dataframe
        URL = f'mysql+pymysql://{env.user}:{env.password}@{env.host}/curriculum_logs'
        SQL = '''
        SELECT date, time, path, user_id, cohort_id, program_id, ip,
        name, slack, start_date, end_date, created_at, updated_at
        FROM logs
        JOIN cohorts on logs.cohort_id = cohorts.id
        '''
        curr_logs = pd.read_sql(SQL, URL)
        
        # Write that dataframe to cscfor later.
        curr_logs.to_csv('curriculum_logs.csv')

        return curr_logs 
    
    


# In[16]:


curr_logs = get_curriculum_logs()


# ## Acquire and Prep

# In[10]:


def get_n_prep_curr_logs():
    '''
    This function reads data from a csv and prepares is by: 
    reads from csv
    concats date + time 
    changes date_time to pd datetime
    changes date to pd datetime
    changes time to pd datetime
    sets index to date_time
    changes cohort start to datetime
    changes cohort end to datetime
    label students by the program they are in
    create column where true or false if staff
    create column with date - end date
    drop columns
    returns df
    '''
    
    # imports
    import pandas as pd
    import numpy as np

    # read from csv
    curr_logs = pd.read_csv('curriculum_logs.csv')
    
    # concat date + time 
    curr_logs['date_time']=curr_logs.date+' '+curr_logs.time
    
    # change date_time to pd datetime
    curr_logs.date_time = pd.to_datetime(curr_logs.date_time)
    
    # change date to pd datetime
    curr_logs.date = pd.to_datetime(curr_logs.date)
    
    # change time to pd datetime
    curr_logs.time = pd.to_datetime(curr_logs.time)
    
    # set index to date_time
    curr_logs = curr_logs.set_index(curr_logs.date_time)
    
    # change cohort start to datetime
    curr_logs.start_date = pd.to_datetime(curr_logs.start_date)
    
    # change cohort end to datetime
    curr_logs.end_date = pd.to_datetime(curr_logs.end_date)
    
    # label students by the program they are in
    program_id = [curr_logs.program_id == 1, curr_logs.program_id == 2, curr_logs.program_id == 3, curr_logs.program_id == 4]
    program = ['php','java','data_science','front_end']
    curr_logs['program'] = np.select(program_id, program)
    
    # create column where true or false if staff
    curr_logs['staff'] = curr_logs.name=='Staff'
    
    # create column with date - end date
    curr_logs['days_after_grad'] = curr_logs.date-curr_logs.end_date
    
    # drop columns
    cols_to_drop = ['Unnamed: 0', 'date', 'time']
    curr_logs = curr_logs.drop(columns=cols_to_drop)
    
    # drop null for path column
    curr_logs = curr_logs[curr_logs.path.notnull()]
    
    return curr_logs


# In[4]:


curr_logs = get_n_prep_curr_logs()


# In[ ]:


curr_logs.head()


# ## Scale

# In[7]:


def scale_vars(x): 

    '''
    This function scales variables you want to cluster.
    '''

    # Scaler import
    from sklearn.preprocessing import MinMaxScaler

    # create the scaler
    scaler = MinMaxScaler().fit(x)
    # use the scaler
    scaled_array = scaler.transform(x)
    scaled_array[0:10]


# In[ ]:




