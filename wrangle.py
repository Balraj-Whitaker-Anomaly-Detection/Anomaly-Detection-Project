#!/usr/bin/env python
# coding: utf-8

# ## Acquire Data from the SQL DB

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
    



curr_logs = get_curriculum_logs()
df = curr_logs

# ## Acquire and Prep



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


curr_logs = get_n_prep_curr_logs()


curr_logs.head()


# ## Scale


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


# -------------------------------------------------------------------------------------------

# FUNCTION to get a dataframe with all nulls by column
# ----------------------------------------
def nulls_by_col(curr_logs):
    num_missing = curr_logs.isnull().sum()
    rows = curr_logs.shape[0]
    prcnt_miss = num_missing / rows * 100
    cols_missing = pd.DataFrame({'num_rows_missing': num_missing, 'percent_rows_missing': prcnt_miss})
    return cols_missing


# FUNCTION to get a dataframe with all nulls by column
# ----------------------------------------
def nulls_by_row(curr_logs):
    num_missing = curr_logs.isnull().sum(axis=1)
    prcnt_miss = num_missing / curr_logs.shape[1] * 100
    rows_missing = pd.DataFrame({'num_cols_missing': num_missing, 'percent_cols_missing': prcnt_miss})\
    .reset_index()\
    .groupby(['num_cols_missing', 'percent_cols_missing']).count()\
    .rename(index=str, columns={'customer_id': 'num_rows'}).reset_index()
    return rows_missing



def summarize(curr_logs):
    '''
    summarize will take in a single argument (a pandas dataframe) 
    and output to console various statistics on said dataframe, including:
    # .head()
    # .info()
    # .describe()
    # value_counts()
    # observation of nulls in the dataframe
    '''
    print('=====================================================\n\n')
    print('Dataframe head: ')
    print(curr_logs.head(3).to_markdown())
    print('=====================================================\n\n')
    print('Dataframe info: ')
    print(curr_logs.info())
    print('=====================================================\n\n')
    print('Dataframe Description: ')
    print(curr_logs.describe().to_markdown())
    num_cols = [col for col in curr_logs.columns if curr_logs[col].dtype != 'O']
    cat_cols = [col for col in curr_logs.columns if col not in num_cols]
    print('=====================================================')
    print('DataFrame value counts: ')
    for col in curr_logs.columns:
        if col in cat_cols:
            print(curr_logs[col].value_counts())
        else:
            print(curr_logs[col].value_counts(bins=10, sort=False))
    print('=====================================================')
    print('nulls in dataframe by column: ')
    print(nulls_by_col(curr_logs))
    print('=====================================================')
    print('nulls in dataframe by row: ')
    print(nulls_by_row(curr_logs))
    print('=====================================================')


# FUNCTION to remove columns 
# ----------------------------------------
def remove_columns(curr_logs, cols_to_remove):
    curr_logs = curr_logs.drop(columns=cols_to_remove)
    return curr_logs


# FUNCTION to handle missing values
# ----------------------------------------
def handle_missing_values(curr_logs, prop_required_columns=0.5, prop_required_row=0.75):
    threshold = int(round(prop_required_columns * len(curr_logs.index), 0))
    curr_logs = curr_logs.dropna(axis=1, thresh=threshold)
    threshold = int(round(prop_required_row * len(curr_logs.columns), 0))
    curr_logs = curr_logs.dropna(axis=0, thresh=threshold)
    return curr_logs




# FUNCTION plots a normalized value count as a percent using catplot
# ----------------------------------------
def category_percentages_by_another_category_col(curr_logs, category_a, category_b):
    """
    Produces a .catplot with a normalized value count
    """
    (curr_logs.groupby(category_b)[category_a].value_counts(normalize=True)
    .rename('percent')
    .reset_index()
    .pipe((sns.catplot, 'data'), x=category_a, y='percent', col=category_b, kind='bar', ))

    