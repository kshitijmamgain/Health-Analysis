import numpy as np
import pandas as pd
from datetime import datetime
from datetime import timedelta
from datetime import date
import os

def dt_object(timestamp):

    from datetime import datetime
    dt_object = datetime.utcfromtimestamp(timestamp)
    return (dt_object)

def offset(dataframe,columnname_offset,columnname_torewrite):
   
    column_offset=[]
    hr= lambda a : int(a[3:6])
    mins= lambda a : int(a[3]+a[6:8])
    for i in dataframe.index:
        hour=(hr(dataframe[columnname_offset][i]))
        minute=(mins(dataframe[columnname_offset][i]))
        human_readable_time=pd.to_datetime(dataframe[columnname_torewrite][i], unit='ms')
        new_time=human_readable_time+timedelta(hours=hour, minutes=minute )
        column_offset.append(new_time)
    return column_offset

def remove_outlier(df_in, col_name):
    q1 = df_in[col_name].quantile(0.25)
    q3 = df_in[col_name].quantile(0.75)
    iqr = q3-q1 #Interquartile range
    fence_low  = q1-1.5*iqr
    fence_high = q3+1.5*iqr
    df_out = df_in.loc[(df_in[col_name] > fence_low) & (df_in[col_name] < fence_high)]
    return df_out

def sleep_preprocess(sleep_df):
    '''ETL -> Preprocesses sleep file'''
    # looking at the long column name can be confusing let's make the column names clean
    new_cols = []
    new_cols.append([col.split('.')[-1] for col in sleep_df.columns])
    new_cols[0]

    sleep_df.columns = new_cols[0]


    # Also the column with time stamp should be converted to date time format we can use the same function defined above
    time_stamp_cols = ['create_time', 'end_time', 'start_time', 'update_time']

    for colname in time_stamp_cols:
        sleep_df[colname] = sleep_df.apply(lambda x: dt_object(x[colname]/1000), axis =1)

    # Apply the offset and create new columns. 
    sleep_df['offset_starttime']=offset(sleep_df, 'time_offset', 'start_time')
    sleep_df['offset_endtime']=offset(sleep_df, 'time_offset', 'end_time')

    # let us clean data more to make it easier to comprehend
    sleep_df.dropna(axis = 1, inplace = True)

    # create new columns for weekday and sleep duration
    sleep_df['weekday'] = [day.weekday() for day in sleep_df['start_time']]
    sleep_df['sleep_duration'] = (sleep_df['end_time']-sleep_df['start_time'])/np.timedelta64(1,'h')

    # add seperate columns for date and hour
    sleep_df['start_date'] = [d.date() for d in sleep_df['offset_starttime']]
    sleep_df['start_hour'] = [d.time() for d in sleep_df['offset_starttime']]
    sleep_df['end_date'] = [d.date() for d in sleep_df['offset_endtime']]
    sleep_df['end_hour'] = [d.time() for d in sleep_df['offset_endtime']]

    # Sort values by start time
    sleep_df.sort_values(by = ['start_time'], inplace = True)
    sleep_df.reset_index(inplace = True)
    
    # Add a column with gap between 2 sleeps
    sleep_df['sleep_gap'] = (sleep_df['start_time'].shift(-1) - sleep_df['end_time'])/np.timedelta64(1,'h')

    # now check for disrupted sleep
    sleep_df['Disrupted']=(sleep_df.sleep_gap < 2) & (sleep_df.sleep_duration < 4)

    sleep_df['waking_hour'] = sleep_df.apply(lambda a: a['offset_endtime'].time().hour, axis =1)

    # map the wekday names
    sleep_df['weekday']= sleep_df['weekday'].map({0:"Monday", 1: "Tuesday", 2:"Wednesday",
                                                  3:"Thursday",4:"Friday",5:"Saturday", 6:"Sunday"})
    sleep_df.drop(['index', 'datauuid', 'pkg_name', 'create_time', 'time_offset', 'end_time', 'start_time', 
                   'update_time', 'offset_starttime','offset_endtime'], axis = 1 , inplace = True)
    
    return sleep_df

def heart_preprocess(heart_rate_df):
    #Heart rate#
    heart_rdf = heart_rate_df[['heart_rate', 'end_time', 'time_offset', 'deviceuuid']].copy()
    # Convert string type to datetime
    heart_rdf['end_time'] = pd.to_datetime(heart_rdf['end_time'])
    # seperate column for date
    heart_rdf['date'] = [d.date() for d in heart_rdf['end_time']]
    # seperate column for time
    heart_rdf['hour'] = [d.time() for d in heart_rdf['end_time']]
    # sort values
    heart_rdf.sort_values(by = ['end_time'], inplace = True)
    heart_rdf.reset_index(inplace = True)
    heart_rdf.drop(heart_rdf.index[[0,1]], inplace = True)
    heart_rdf.drop('index', axis =1 ,inplace = True)
    
    #time offset
    heart_rdf['offset_hour'] = (heart_rdf.time_offset.str.split("C").str[1].astype(int))/100
    
    oh = list(heart_rdf['offset_hour'])
    
    for i,val in enumerate(oh):
        if val == 5.3:
            oh[i] = 5.5
        else:
            pass
    
    td = []
    
    for hr in oh:
        td.append(timedelta(hours = hr))
    heart_rdf['delta_time'] = td
    heart_rdf['adjusted_time'] = heart_rdf['end_time']+heart_rdf['delta_time']
    
    return heart_rdf

def step_preprocess(df):
    df['date'] = df.apply(lambda x: datetime.fromtimestamp(x['day_time']/1000), axis =1)
    df.drop(['binning_data', 'datauuid','source_pkg_name','source_type', 
                                    'pkg_name', 'create_time' ], axis=1, inplace = True)
    return df

def stress_preprocess(stress_df):
    stress_df['start_time'] = pd.to_datetime(stress_df['start_time'])
    # seperate column for date
    stress_df['date'] = [d.date() for d in stress_df['start_time']]
    # seperate column for time
    stress_df['hour'] = [d.time() for d in stress_df['start_time']]
    stress_df.drop(['create_time', 'time_offset','tag_id', 'algorithm', 
                                'end_time', 'custom', 'pkg_name'], axis=1, inplace = True)
    return stress_df

def floors_preprocess(floors_climbed_df):
    # Convert string type to datetime
    floors_climbed_df['start_time'] = pd.to_datetime(floors_climbed_df['start_time'])
    
    # Convert string type to datetime
    floors_climbed_df['end_time'] = pd.to_datetime(floors_climbed_df['end_time'])
    # seperate column for date
    floors_climbed_df['date'] = [d.date() for d in floors_climbed_df['start_time']]
    # seperate column for time
    floors_climbed_df['hour'] = [d.time() for d in floors_climbed_df['start_time']]
    
    floors_climbed_df.drop(['pkg_name', 'update_time', 'create_time', 'time_offset', 'datauuid'], axis=1, inplace = True)
    return floors_climbed_df

def exercise_preprocess(Exercise_df):
    Exercise_df['start_time'] = pd.to_datetime(Exercise_df['start_time'])
    Exercise_df['start_time'] = pd.to_datetime(Exercise_df['start_time'])
    Exercise_df['end_time'] = pd.to_datetime(Exercise_df['end_time'])
    Exercise_df['offset_starttime']=offset(Exercise_df, 'time_offset', 'start_time')
    Exercise_df['offset_endtime']=offset( Exercise_df, 'time_offset', 'end_time')
    Exercise_df.exercise_type.value_counts()
    
    Exercise_df['exercise_type'] = Exercise_df['exercise_type'].map({1001:'Walking', 0: 'Custom', 14001:'Swiming',
                                                                      11007:'Cycling',1002:'Running',9002:'Yoga',
                                                                      13001:'Hiking',15006:'Elliptical Trainer'})
    Exercise_df['weekday'] = Exercise_df.apply(lambda x: x['offset_endtime'].weekday(), axis =1)
    Exercise_df.duration = Exercise_df.duration/60000
    Exercise_df['weekday'] = Exercise_df['weekday'].map({0:"Monday", 1: "Tuesday", 2:"Wednesday",
                                                                      3:"Thursday",4:"Friday",5:"Saturday",
                                                                      6:"Sunday"})
    Exercise_df['start_date'] = [d.date() for d in Exercise_df['offset_starttime']]
    
    return Exercise_df
def stepcount_preprocess(step_count_df):
    step_count_df['start_time'] = pd.to_datetime(step_count_df['start_time'])
    step_count_df['end_time'] = pd.to_datetime(step_count_df['end_time'])

    step_count_df['offset_hour'] = (step_count_df.time_offset.str.split("C").str[1].astype(int))/100
    oh = list(step_count_df['offset_hour'])

    for i,val in enumerate(oh):
        if val == 5.3:
            oh[i] = 5.5
        else:
            pass

    td = []

    for hr in oh:
        td.append(timedelta(hours = hr))

    step_count_df['timedelta'] = td
    step_count_df['offset_etime'] = step_count_df['end_time']+step_count_df['timedelta']
    step_count_df['day_time'] = [d.time() for d in step_count_df.offset_etime]
    step_count_df['day_hour'] = [d.strftime('%H') for d in step_count_df.day_time]
    step_count_df['date'] =  [d.date() for d in step_count_df['offset_etime']]
    return step_count_df