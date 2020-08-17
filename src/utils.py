import os
import glob
import pandas as pd
import numpy as np
from datetime import datetime

import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from preprocess import (sleep_preprocess, heart_preprocess, exercise_preprocess, stepcount_preprocess)

file = glob.glob(r'datasets\*')
file_list = []
for f in file:
    if f.endswith('.csv'):
        globals()['%s_df' % f.split('.')[0].split('\\')[1]] = pd.read_csv(f, index_col = 0)
        file_list.append('%s_df' % f.split('.')[0].split('\\')[1])

#drop null columns

for df in file_list:
    print(df)
    l = len(globals()[df])
    globals()[df].dropna(axis = 1, how = 'all', inplace = True) 

# preprocess the datasets
sleep_df = sleep_preprocess(sleep_df)
heart_rate_df = heart_preprocess(heart_rate_df)
Exercise_df = exercise_preprocess(Exercise_df)
step_count_df = stepcount_preprocess(step_count_df)

def dailyroutine(dt):
    # creat index for time to join heart rate and step counts
    df = pd.DataFrame()
    df['time'] = pd.date_range("00:00", "23:59", freq="min").time
    df.set_index('time',inplace=True)
    
    # extract daily data from heart_rate_df
    df_h = heart_rate_df[heart_rate_df.date == dt].sort_values(by = 'hour')
    df_h.hour = df_h.hour.apply(lambda x: x.replace(microsecond=0))
    df_h.hour = df_h.hour.apply(lambda x: x.replace(second=0))
    
    # extract daily calories from step_count_df
    df_steps = step_count_df[step_count_df.date == dt].sort_values(by = 'day_time')
    df_steps.day_time = df_steps.day_time.apply(lambda x: x.replace(microsecond=0))
    df_steps.day_time = df_steps.day_time.apply(lambda x: x.replace(second=0))
    
    # join available points on index
    df = pd.concat([df,df_steps.groupby('day_time').mean()['calorie']],axis=1)
    df = pd.concat([df, df_h.groupby('hour').mean()['heart_rate']], axis=1)
    
    return df

def sleeppattern(dt2):

    t0 = []
    t1 = []
    
    # morning sleep schedule
    s_df = sleep_df[sleep_df.end_date==dt2]
    wk_tm = min(s_df[s_df.end_date==dt2].end_hour)
    if s_df[s_df.end_hour==wk_tm].end_date.values[0] > s_df[s_df.end_hour==wk_tm].start_date.values[0]:
        slp_tm = '00:00:00'
    else:  
        slp_tm = str(s_df[s_df.end_hour==wk_tm].start_hour.values[0])
    wk_tm = str(wk_tm)
    t0.append(slp_tm)
    t1.append(wk_tm)
    try:
        s_df = sleep_df[sleep_df.start_date==dt2]
        slp_tm = max(s_df[s_df.start_date==dt2].start_hour)
        if s_df[s_df.start_hour==slp_tm].start_date.values[0] < s_df[s_df.start_hour==slp_tm].end_date.values[0]:
            wk_tm = '23:59:00'
        else:  
            wk_tm = str(s_df[s_df.start_hour==slp_tm].end_hour.values[0])
        slp_tm = str(slp_tm)
        t0.append(slp_tm)
        t1.append(wk_tm)
    except: 
        t0.append(None)
        t1.append(None)
    return t0,t1

def dailygraph(date):
    dt2 = datetime.strptime(date.split("T")[0],'%Y-%m-%d').date()    
    print(dt2)
    print(type(dt2))
    e_df = Exercise_df[Exercise_df.start_date==dt2].groupby('exercise_type').sum()[['duration','calorie']]
    labels = e_df.duration.index
    values1 = e_df.duration.values
    values2 = e_df.calorie.values
    fig = make_subplots(rows=2, cols=2,
                        specs=[ [{"type": "pie","rowspan":1}, {"type": "bar"}],
                                [{"secondary_y": True, "colspan":2},None]],
                        subplot_titles=('Total time spent on exercises: '+'<b>'+str(int(sum(e_df.duration)))+' mins </b>',
                                        "Calorie spent during the day",
                                       'Heart rate and calorie plot for : ' + str(dt2))
                       )
    
    # Use `hole` to create a donut-like pie chart
    fig.add_trace(go.Pie(labels=labels, values=values1, hole=.3), row=1, col=1)
    fig.add_trace(go.Bar(x=labels, y=list(values2), marker_color='rgb(158,202,225)',showlegend=False), row=1,col=2)
    fig.update_yaxes(title_text="Calories burnt with the activities", row=1, col=2)
    
    df = dailyroutine(dt2)
    # Create figure with secondary y-axis
    
    # Add traces
    fig.add_trace(
        go.Scatter(x=df.index, y=df.heart_rate, name="Heart Rate",connectgaps=True),
        secondary_y=False, row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=df.index, y=df.calorie, name="Calories Burnt",connectgaps=True),
        secondary_y=True, row=2, col=1
    )
    
    # Add figure title
    """fig.update_layout(
        title_text='Heart rate and Step Count plot for : ' + str(dt)
    )"""
    
    # Set x-axis title
    fig.update_xaxes(title_text="Time on "+str(dt2), row=2, col=1)
    
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Heart Rate</b> (bpm)", secondary_y=False, row=2, col=1)
    fig.update_yaxes(title_text="<b>Calories Spent</b> (Step Count) ", secondary_y=True, row=2, col=1)
    
    fig.update_xaxes(rangeslider_visible=True, row=2, col=1)
    
    # Add shape regions
      #shape regions
    t0,t1 = sleeppattern(dt2)
    
    fig.add_shape(
            type="rect",
            # x-reference is assigned to the x-values
            #xref="paper",
            # y-reference is assigned to the plot paper [0,1]
            #yref="paper",
            x0=t0[0],
            y0=0,
            x1=t1[0],
            y1=100,
            fillcolor="LightSalmon",
            opacity=0.5,
            layer="below",
            line_width=0,
            row=2,col=1),
    fig.add_shape(
            type="rect",
            # x-reference is assigned to the x-values
            #xref="paper",
            # y-reference is assigned to the plot paper [0,1]
            #yref="paper",
            x0=t0[1],
            y0=0,
            x1=t1[1],
            y1=100,
            fillcolor="LightSalmon",
            opacity=0.5,
            layer="below",
            line_width=0,
            row=2,col=1)
    
    
    
    
    fig.update_layout(height=1050, width=1000,
            title_text='<b> Daily Health Dashboard</b>'
        )
    return fig

def dropdown_barplot(column_chosen):
    if column_chosen=='Total':
        fig = px.bar(x=list(sleep_df.groupby(["waking_hour"]).mean().unstack().sleep_duration.index),
                     y=list(sleep_df.groupby(["waking_hour"]).mean().unstack().sleep_duration.values), 
                     labels={'x':'Hour of day', 'y':'Average sleeping hours'})
    else:
        fig = px.bar(x=list(sleep_df.groupby(["waking_hour","weekday"]).mean().unstack().sleep_duration[column_chosen].index),
                     y=list(sleep_df.groupby(["waking_hour","weekday"]).mean().unstack().sleep_duration[column_chosen].values), 
                     labels={'x':'Hour of day', 'y':'Average sleeping hours'})
        
    
    #fig.update_traces(textinfo='percent+label')
    fig.update_layout(title={'text':'Day-wise Sleeping Pattern',
                      'font':{'size':28},'x':0.5,'xanchor':'center'})
    return fig

def distplot():
    sleep_duration = [c for c in sleep_df['sleep_duration']]
    day_nap = list(sleep_df[(sleep_df.waking_hour >= 10) &(sleep_df.waking_hour <= 19)]['sleep_duration'])
    disturbed = list(sleep_df[sleep_df.Disrupted == True]['sleep_duration']) 
    fig = ff.create_distplot([sleep_duration, day_nap, disturbed], ['sleep duration', 'day nap', 'disrupted sleep'], bin_size=[.5, 1, 1], show_rug = False)
    fig.update_layout(title_text='Customized Distplot')
    return fig

def boxplot():
    # Figure Boxplot
    fig = px.box(sleep_df, x="weekday", y="efficiency", color="Disrupted",notched=True)
    #fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
    fig.update_layout(title='Sleep efficiency during different days of the week',
        yaxis=dict(autorange=True, showgrid=True, zeroline=True, dtick=5, gridcolor='rgb(255, 255, 255)',
            gridwidth=1, zerolinecolor='rgb(255, 255, 255)', zerolinewidth=2),
        margin=dict(l=40, r=30, b=80,t=100,), paper_bgcolor='rgb(243, 243, 243)', plot_bgcolor='rgb(243, 243, 243)',
        showlegend=True)
    return fig