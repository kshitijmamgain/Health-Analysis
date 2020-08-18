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

#---------------------------------------------------------------
# Connecting the tab_daily_layout with the graph
#---------------------------------------------------------------
@app.callback(
    Output('dashboard', 'figure'),
    [Input('my-date-picker-single', 'date')])
def health_dashboard(date):
    return utils.dailygraph(date)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

trends_layout = html.Div(children=[
                    html.Div([
                        html.Div([
                            html.H1("Trends Analysis on different Indicators"),],className='nine columns'), 
                            dash_components.data_picker]),
                                        
                    html.Div([
                        html.H3(children='Bar Plot Summary'),
                        html.Div(children='''Dash: A web application framework for Python.'''),
                        html.Div([dcc.Graph(id='bar_graph')],className='nine columns'),
                        dash_components.day_picker]),
    
                    html.Div(children=[
                        html.H3(children='Box-plot Summary',style ={'textAlign':'center','color': colors['text']}),
                        html.Div(children=''''''),
                        html.Div([dcc.Graph(id='boxplot-graph')],className='nine columns'),
                        dash_components.boxPlotOptions]),

                    html.Div([
                        html.H3('Distplot summary '),
                        html.P(' '),
                        dcc.Graph(id='distplot-graph')], className='nine columns')

                ], className='rows')

#---------------------------------------------------------------
# Connecting the Dropdown values to the bar graph
@app.callback(
    Output(component_id='bar_graph', component_property='figure'),
    [Input(component_id='weekday_dropdown', component_property='value'),
     Input(component_id='attribute_dropdown', component_property='value')])
def build_bar_graph(weekday,attribute):

    return utils.dropdown_barplot(weekday, attribute)

#---------------------------------------------------------------
# Connecting the Dropdown values to the boxplot graph
@app.callback(
    Output(component_id='boxplot-graph', component_property='figure'),
    [Input(component_id='attribute_dropdown', component_property='value'),
     Input(component_id='view_dropdown', component_property='value')])
def build_boxplot_graph(attribute, view):
    print(attribute)
    return utils.boxplot(attribute,view)

#---------------------------------------------------------------
# Connecting the Dropdown values to the density plot graph
@app.callback(
    Output(component_id='distplot-graph', component_property='figure'),
    [Input(component_id='attribute_dropdown', component_property='value')])
def build_distplot_graph(attribute):
    print(attribute)
    return utils.distplot(attribute)

if __name__ == '__main__':
    app.run_server(debug=True)