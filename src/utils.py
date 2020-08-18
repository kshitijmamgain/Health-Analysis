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
    
    # Set x-axis title
    fig.update_xaxes(title_text="Time on "+str(dt2), row=2, col=1)
    
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Heart Rate</b> (bpm)", secondary_y=False, row=2, col=1)
    fig.update_yaxes(title_text="<b>Calories Spent</b> (Step Count) ", secondary_y=True, row=2, col=1)
    
    fig.update_xaxes(rangeslider_visible=True, row=2, col=1)
    
    # Add shape regions
      #shape regions
    t0,t1 = sleeppattern(dt2)
    
    fig.add_shape(type="rect", x0=t0[0], y0=0, x1=t1[0], y1=100, fillcolor="LightSalmon", opacity=0.5,
                  layer="below", line_width=0, row=2,col=1),
    fig.add_shape(type="rect", x0=t0[1], y0=0, x1=t1[1], y1=100, fillcolor="LightSalmon", opacity=0.5, 
                  layer="below", line_width=0, row=2,col=1)

    fig.update_layout(height=1050, width=1000, title_text='<b> Daily Health Dashboard</b>')
    return fig

def dropdown_barplot(weekday,attribute):
    if attribute == 'sleep':
        df = sleep_df
        xaxis = "waking_hour"
        vals = "sleep_duration"
        slabels={'x':'Hour of day', 'y':'Average sleeping hours'}
        stitle ='Day-wise Sleeping Pattern'
    
    elif attribute == 'exercise':
        df = Exercise_df
        xaxis = "exercise_type"
        vals = "calorie"
        slabels={'x':'Type of execise', 'y':'Average calories spent'}
        stitle ='Day-wise Step Count Pattern'
    
    elif attribute == 'steps':
        df = step_count_df
        xaxis = "day_hour"
        vals = "count"
        slabels={'x':'Hour of day', 'y':'Average steps taken'}
        stitle ='Day-wise Exercise Pattern'

    else:# attribute == 'heart_rate':
        df = heart_rate_df
        xaxis = "day_hour"
        vals = "heart_rate"
        slabels={'x':'Hour of day', 'y':'Average heart beat rate'}
        stitle ='Day-wise Heart Rate Pattern'

    if weekday=='Total':
        fig = px.bar(x=list(df.groupby([xaxis]).mean().unstack()[vals].index),
                     y=list(df.groupby([xaxis]).mean().unstack()[vals].values), 
                     labels=slabels)
    else:
        fig = px.bar(x=list(df.groupby([xaxis,"weekday"]).mean().unstack()[vals][weekday].index),
                     y=list(df.groupby([xaxis,"weekday"]).mean().unstack()[vals][weekday].values), 
                     labels=slabels)     
    #fig.update_traces(textinfo='percent+label')
    fig.update_layout(title={'text':stitle,
                      'font':{'size':28},'x':0.5,'xanchor':'center'})
    return fig

def distplot(attribute):
    
    if attribute == 'sleep':
        df = sleep_df
        xaxis = "sleep_duration"
        cols = "Disrupted"
        vals = "efficiency"
        slabels={'sleep_duration':'Sleep Duration (hrs)', 'efficiency':'Sleep Efficiency (%)'}
        stitle ='Density Contour for Sleep Efficiency'
    
    elif attribute == 'exercise':
        df = Exercise_df[(Exercise_df.exercise_type=='Custom')|(Exercise_df.exercise_type=='Swimming')|
                            (Exercise_df.exercise_type=='Cycling')|(Exercise_df.exercise_type=='Running')]
        xaxis = "duration"
        vals = "calorie"
        cols = "exercise_type"
        slabels={'duration':'Time Spent on Exercise (mins)', 'calorie':'Calories Spent (cal)', 'exercise_type': 'Exercise Type'}
        stitle ='Density Contour for Exercise'
    
    elif attribute == 'steps':
        df = step_count_df
        xaxis = "distance"
        vals = "calorie"
        cols = None
        slabels={'distance':'Distance Covered (m)', 'calorie':'Calories Spent (cal)'}
        stitle ='Density Conour for Step Count'
    
    else:# attribute == 'heart_rate':
        df = heart_rate_df
        xaxis = "day_hour"
        vals = "heart_rate"
        cols = None
        slabels={'day_hour':'Day Time (hrs)', 'heart_rate':'Heart Rate (bpm)'}
        stitle ='Density Contour for Heart Rate'
    
    fig = px.density_contour(df, x=xaxis, y=vals, color=cols,labels=slabels)
    fig.update_layout(title={'text':stitle, 'font':{'size':28},'x':0.5,'xanchor':'center'},
                      yaxis=dict(autorange=True, showgrid=True, zeroline=True, nticks=10, gridcolor='rgb(255, 255, 255)',
                      gridwidth=1, zerolinecolor='rgb(255, 255, 255)', zerolinewidth=2),xaxis=dict(nticks=10),
                      margin=dict(l=40, r=30, b=80,t=100,), paper_bgcolor='rgb(243, 243, 243)', plot_bgcolor='rgb(243, 243, 243)',
                      showlegend=True)
    return fig

def boxplot(attribute, view='T'):
    typ = True if view=='T' else False
    if attribute == 'sleep':
        df = sleep_df
        xaxis = "weekday"
        cols = "Disrupted"
        vals = "sleep_duration"
        slabels={"weekday":'Distribution over days of week', 'sleep_duration':'Sleep Duration (hrs)'}
        stitle ='Sleep efficiency during different days of the week'
    
    elif attribute == 'exercise':
        df = Exercise_df[(Exercise_df.exercise_type=='Custom')|(Exercise_df.exercise_type=='Swimming')|
                            (Exercise_df.exercise_type=='Cycling')|(Exercise_df.exercise_type=='Running')]
        xaxis = "weekday"
        vals = "calorie"
        cols = "exercise_type"
        slabels={"weekday":'Distribution over days of week', 'calorie':'Calories Spent (cal)','exercise_type': 'Exercise Type'}
        stitle ='Calories burnt during different days of the week'
    
    elif attribute == 'steps':
        df = step_count_df
        xaxis = "weekday"
        vals = "distance"
        cols = None
        slabels={"weekday":'Distribution over days of week', 'distance':'Distance Covered Walking (m)'}
        stitle ='Step count during different days of the week'
    
    else:# attribute == 'heart_rate':
        df = heart_rate_df
        xaxis = "weekday"
        vals = "heart_rate"
        cols = None
        slabels={"weekday":'Distribution over days of week', 'heart_rate':'Heart Rate (bpm)'}
        stitle ='Heart beat during different days of the week'    
    # Figure Boxplot
    weekday_order = {"weekday": ["Monday", "Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]}
    fig = px.box(df, x=xaxis, y=vals, color=cols,notched=typ, category_orders=weekday_order,
                 points='suspectedoutliers',labels=slabels)

    fig.update_layout(title={'text':stitle, 'font':{'size':28},'x':0.5,'xanchor':'center'},
                      yaxis=dict(autorange=True, showgrid=True, zeroline=True, nticks=5, gridcolor='rgb(255, 255, 255)',
                      gridwidth=1, zerolinecolor='rgb(255, 255, 255)', zerolinewidth=2),
                      margin=dict(l=40, r=30, b=80,t=100,), paper_bgcolor='rgb(243, 243, 243)', plot_bgcolor='rgb(243, 243, 243)',
                      showlegend=True)
    return fig