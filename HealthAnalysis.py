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
                            html.H1(children='Trends Analysis on Different Indicators')],className='nine columns'),
                            dash_components.data_picker,])
                    
                    html.Div([
                        html.Div([
                            html.H1(children='Bar-plot Summary'),
                            dcc.Graph(id='bar-graph')],className='nine columns'),
                            dash_components.day_picker,]),
    
                    html.Div(children=[
                        html.Div([
                            html.H3(children='Box-plot Summary',style ={'textAlign':'center','color': colors['text']}),
                            dcc.Graph(id='boxplot-graph')],className='nine columns'),
                            dash_components.boxPlotOptions]),
                        
                    html.Div([
                        html.Div([                        
                            html.H3('Distplot summary '),
                            dcc.Graph(id='distplot-graph')], className='nine columns')])

                ], className='rows')
-------------------------
# Connecting the Dropdown values to the graph
@app.callback(
    Output(component_id='bar-graph', component_property='figure'),
    [Input(component_id='weekday_dropdown', component_property='value'),
     Input(component_id='attribute_dropdown', component_property='value')])
def build_bargraph(weekday,attribute):
    return utils.dropdown_barplot(weekday,attribute)

@app.callback(
    Output(component_id='boxplot-graph', component_property='figure'),
    [Input(component_id='attribute_dropdown', component_property='value'),
     Input(component_id='view_dropdown', component_property='value')])
def build_bargraph(weekday,attribute):
    return utils.dropdown_barplot(attribute,view)

@app.callback(
    Output(component_id='distplot-graph', component_property='figure'),
    [Input(component_id='attribute_dropdown', component_property='value')])
def build_bargraph(weekday,attribute):
    return utils.distplot(attribute)




if __name__ == '__main__':
    app.run_server(debug=True)