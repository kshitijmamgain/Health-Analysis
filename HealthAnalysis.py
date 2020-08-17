import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from dash.dependencies import Input, Output
from datetime import datetime as dt
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from flask import Flask
from preprocess import (dt_object, offset, sleep_preprocess, heart_preprocess, step_preprocess, stress_preprocess, 
                            floors_preprocess, exercise_preprocess, stepcount_preprocess)
import glob
import os
from datetime import datetime
from datetime import timedelta
#from datetime import date
import tab_introduction, tab_daily
from src import utils, dash_components
#os.chdir('datasets')
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
step_daily_trend_df = step_preprocess(step_daily_trend_df)
stress_df = stress_preprocess(stress_df)
floors_climbed_df = floors_preprocess(floors_climbed_df)
Exercise_df = exercise_preprocess(Exercise_df)
step_count_df = stepcount_preprocess(step_count_df)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True
app.scripts.config.serve_locally = True
server = app.server

app.layout = html.Div([
        # header/title display
        html.Div([
            html.H1('Health Data Analysis'),
            html.H4('Designed by: Kshitij Mamgain',style ={'textAlign':'center','color': "#ffffff"})],  
            style = {'padding' : '50px' ,'backgroundColor' : '#009dc4'}),
        # Define tabs    
        dcc.Tabs(id="tabs-main", value='tab-intro', children=[
            dcc.Tab(label='Introduction', value='tab-intro'),
            dcc.Tab(label='Daily Analysis', value='tab-daily'),
            dcc.Tab(label='Trend Analysis', value='trends'),]),
        #define tabs call back id
        html.Div(id='tabs-contents') ])

#Tabs callback
@app.callback(Output('tabs-contents', 'children'),
              [Input('tabs-main', 'value')] )

def render_content(tab):

    if tab == 'tab-daily':
        return tab_daily.tab_daily_layout

    elif tab == 'trends':
        return trends_layout
    
    elif tab == 'tab-intro':
        return tab_introduction.tab_about_layout

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

trends_layout = html.Div([
    dcc.Tabs(id="tabs-trends", value='tab-sleep', children=[
        dcc.Tab(label='Sleep Trend', value='tab-sleep'),
        dcc.Tab(label='Exercise Trend', value='tab-exercise'),
        ]),
    html.Div(id='tabs-trends-content')    
])

@app.callback(Output('tabs-trends-content', 'children'),
              [Input('tabs-trends', 'value')] )

def render_trend_content(tab):

    if tab == 'tab-sleep':
        return trends_layout1

    elif tab == 'tab-exercise':
        return trends_layout2

trends_layout1 = html.Div(children=[
                    html.H3(children='Bar Plot Summary'),
                    html.Div(children='''Dash: A web application framework for Python.'''),
                    
                    html.Div([
                        html.Div([dcc.Graph(id='our_graph')],className='nine columns'),
                        dash_components.day_picker,]),
    
                    html.Div(children=[
                        html.H3(children='Box-plot Summary',style ={'textAlign':'center','color': colors['text']}),
                        html.Div(children=''''''),
                        dcc.Graph(id='example-graph-3', figure=utils.boxplot())],className='nine columns'),

                    html.Div([
                        html.H3('Distplot summary '),
                        html.P(' '),
                        dcc.Graph(id='graph-3-tabs', figure = utils.distplot())], className='nine columns')

                ], className='rows')

trends_layout2 = html.Div(children=[
                    html.H3(children='Bar Plot Summary'),
                    html.Div(children='''Dash: A web application framework for Python.'''),
                    html.Div([
                        html.Div(children=''''''),
                        dcc.Graph(id='example-graph-2',figure=utils.boxplot())],className='nine columns'),
                    html.Div([
                        html.H3('Distplot summary '),
                        html.P(' '),
                        dcc.Graph(id='graph-2-tabs',figure = utils.distplot())], className='nine columns')
                ], className='rows')
#---------------------------------------------------------------
# Connecting the Dropdown values to the graph
@app.callback(
    Output(component_id='our_graph', component_property='figure'),
    [Input(component_id='weekday_dropdown', component_property='value')])
def build_graph(column_chosen):
    return utils.dropdown_barplot(column_chosen)


@app.callback(
    Output('dashboard', 'figure'),
    [Input('my-date-picker-single', 'date')])
def health_dashboard(date):
    return utils.dailygraph(date)


if __name__ == '__main__':
    app.run_server(debug=True)