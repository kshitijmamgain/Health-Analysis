import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from dash.dependencies import Input, Output
from datetime import datetime as dt
import plotly.graph_objs as go
from flask import Flask
from preprocess import (dt_object, offset, sleep_preprocess, heart_preprocess, step_preprocess, stress_preprocess, 
                            floors_preprocess, exercise_preprocess)
import glob
import os
from datetime import datetime
from datetime import timedelta
from datetime import date
#os.chdir('datasets')
file = glob.glob('datasets\*')
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

sleep_duration = [c for c in sleep_df['sleep_duration']]
day_nap = list(sleep_df[(sleep_df.waking_hour >= 10) &(sleep_df.waking_hour <= 19)]['sleep_duration'])
disturbed = list(sleep_df[sleep_df.Disrupted == True]['sleep_duration']) 

# Step 1. Launch the application

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True
app.scripts.config.serve_locally = True
server = app.server


markdown_text = '''
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
'''
# Step 2. Import the dataset
# Figure Distplot
fig = ff.create_distplot([sleep_duration, day_nap, disturbed], ['sleep duration', 'day nap', 'disrupted sleep'], bin_size=[.5, 1, 1], show_rug = False)
fig.update_layout(title_text='Customized Distplot')


# Figure Boxplot
fig3 = px.box(sleep_df, x="weekday", y="efficiency", color="Disrupted",notched=True)
#fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
fig3.update_layout(
    title='Sleep efficiency during different days of the week',
    yaxis=dict(
        autorange=True,
        showgrid=True,
        zeroline=True,
        dtick=5,
        gridcolor='rgb(255, 255, 255)',
        gridwidth=1,
        zerolinecolor='rgb(255, 255, 255)',
        zerolinewidth=2,
    ),
    margin=dict(
        l=40,
        r=30,
        b=80,
        t=100,
    ),
    paper_bgcolor='rgb(243, 243, 243)',
    plot_bgcolor='rgb(243, 243, 243)',
    showlegend=True
)
# Add dropdown
fig3.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(
                    args=["notched", "True"],
                    label="Notched",
                    method="update"
                ),
                dict(
                    args=["notched", False],
                    label="Standard",
                    method="update"
                )
            ]),
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.1,
            yanchor="top"
        ),
    ]
)
# Add annotation
fig3.update_layout(
    annotations=[
        dict(text="Boxplot :", showarrow=False,
        x=0, y=1.05, yref="paper", align="left")
    ]
)
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
# dropdown options

#opts = [{'label' : i, 'value' : i} for i in features]
#features = merged_sleep_exercise.columns[[2,3,4,6,8]]
#labels=['Calorie (cal)','Exercise Duration (min)','Time Offset','Sleep Efficiency (%)','Sleep Duration (min)']

#Date chooser
#merged_sleep_exercise['start_date'] = pd.to_datetime(merged_sleep_exercise['start_date'], format='%Y-%m-%d')

# Step 3. Create a plotly figure


# Step 4. Create a Dash layout
app.layout = html.Div([
    html.Div([
        html.H1('Health Data Analysis'),
        html.P('By: Kshitij Mamgain')],style = {'padding' : '50px' ,'backgroundColor' : '#3aaab2'}),

    
    dcc.Tabs(id="tabs-example", value='tab-2-example', children=[
        dcc.Tab(label='Exercise Types', value='tab-2-example'),
        dcc.Tab(label='Walking Calories', value='tab-3-example'),
        dcc.Tab(label='Dash', value='tab-1-example'),
        dcc.Tab(label='DropDown', value='tab-4')
        ]),
    html.Div(id='tabs-content-example')
    
    
])



@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')]
              
              )


def render_content(tab):

    if tab == 'tab-2-example':
        return tab_2_layout

    elif tab == 'tab-3-example':
        return tab_3_layout

    elif tab == 'tab-1-example':
        return tab_1_layout
    
    elif tab == 'tab-4':
        return tab_4_layout

tab_4_layout = html.Div([

    html.Div([
        dcc.Graph(id='our_graph')
    ],className='nine columns'),

    html.Div([

        html.Br(),
        html.Div(id='output_data'),
        html.Br(),

        html.Label(['Choose column:'],style={'font-weight': 'bold', "text-align": "center"}),

        dcc.Dropdown(id='my_dropdown',
            options=[
                     {'label': 'Total', 'value': 'Total'},
                     {'label': 'Monday', 'value':'Monday'},
                     {'label': 'Tuesday', 'value':'Tuesday','disabled':False},
                     {'label': 'Wednesday', 'value':'Wednesday'},
                     {'label': 'Thursday', 'value':'Thursday'},
                     {'label': 'Friday', 'value':'Friday'},
                     {'label': 'Saturday', 'value':'Saturday'},
                     {'label': 'Sunday', 'value':'Sunday'}
            ],
            optionHeight=35,                    #height/space between dropdown options
            value='Total',                    #dropdown value selected automatically when page loads
            disabled=False,                     #disable dropdown value selection
            multi=True,                        #allow multiple dropdown values to be selected
            searchable=True,                    #allow user-searching of dropdown values
            search_value='',                    #remembers the value searched in dropdown
            placeholder='Please select...',     #gray, default text shown when no option is selected
            clearable=True,                     #allow user to removes the selected value
            style={'width':"100%"},             #use dictionary to define CSS styles of your dropdown
            # className='select_box',           #activate separate CSS document in assets folder
            # persistence=True,                 #remembers dropdown value. Used with persistence_type
            # persistence_type='memory'         #remembers dropdown value selected until...
            ),                                  #'memory': browser tab is refreshed
                                                #'session': browser tab is closed
                                                #'local': browser cookies are deleted
    ],className='three columns'),

])

#---------------------------------------------------------------
# Connecting the Dropdown values to the graph
@app.callback(
    Output(component_id='our_graph', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value')]
)

def build_graph(column_chosen):
    
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

tab_1_layout = html.Div(children=[
    html.H1(children='Hello Dash1'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    ),
    
    html.Div([
            dcc.Markdown(children=markdown_text)
        ]),
    
    html.Div(children=[
        html.H1(
            children='Hello Dash',
            style ={
            'textAlign':'center',
            'color': colors['text']
            }
           ),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(
            id='example-graph-2',
            figure={
                'data': [
                    {'x': [1, 3, 5], 'y': [4, 5, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 3, 5], 'y': [1, 3, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization 2',
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text']
                        }
                }
            }
        )
    ]),

    html.Div(children=[
        html.H1(
            children='Hello Dash',
            style ={
            'textAlign':'center',
            'color': colors['text']
            }
           ),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(
            id='example-graph-3',
            figure=fig3
        )
    ])

])


tab_2_layout = html.Div([
            html.H2('Calorie vs. Exercise Duration for each Exercise Type'),
            html.P('This graph shows Calories used during each exercise type and its correlation with Exercise Duration. Also, distribution of Calories and Exercise Duration for each exercise type are shown. '),
                dcc.Graph(id='graph-2-tabs',
                figure = px.histogram(sleep_df, x="waking_hour", y="sleep_duration", color="weekday", hover_data=sleep_df.columns)         
            )
        ], style={"height" : "100vh", "width" : "75%"})

tab_3_layout = html.Div([
            html.H3('Calorie vs. Walking Duration and Average Spead'),
            html.P('This graph shows correlation between Walking Duration and burnt Calories. Also, we can see the Average Walking Speed for each data point. Moreover, distribution of Calories and Walking Duration are shown. '),
                dcc.Graph(id='graph-3-tabs',
                figure = fig

            )
        ])



if __name__ == '__main__':
    app.run_server(debug=True)