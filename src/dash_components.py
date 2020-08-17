import dash_html_components as html
import dash_core_components as dcc

day_picker = html.Div([

        html.Br(),
        html.Div(id='output_data'),
        html.Br(),

        html.Label(['Weekday'],style={'font-weight': 'bold', "text-align": "center"}),

        dcc.Dropdown(id='weekday_dropdown',
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
            multi=False,                        #allow multiple dropdown values to be selected
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
    ],className='three columns')

data_picker = html.Div([

        html.Br(),
        html.Div(id='output_data'),
        html.Br(),

        html.Label(['Attribute'],style={'font-weight': 'bold', "text-align": "center"}),

        dcc.Dropdown(id='attribute_dropdown',
            options=[
                     {'label': 'Sleep', 'value': 'sleep'},
                     {'label': 'Exercise', 'value':'exercise'},
                     {'label': 'Heart Rate', 'value':'heart_rate','disabled':False},
                     {'label': 'Step Counts', 'value':'steps'},
                     {'label': 'Stress', 'value':'stress'}
            ],
            optionHeight=35, value='Sleep', disabled=False, multi=False, searchable=True, search_value='',                    #remembers the value searched in dropdown
            placeholder='Please select...', clearable=True, style={'width':"100%"}, 
            ),                                  
    ],className='three columns')