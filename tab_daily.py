import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime
markdown_text = '''
### Explanation

This dashboard extracts data from various data sources and presents the daily lifestyle of the individual.  
1. __Select__ a date ranging from 5th April 2019 to 5th May 2019.  
2. __Pie Chart__ presents the  _univariate_ analysis of the time spent on exercise.  
3. __Bar Plot__ presents _bivariate_ analysis of the calories burnt on each exercise.  
4. __Dual Plot__ presents the health status with shaded region indicating sleep pattern, and lines represent the heart rate and steps during a day. The x-axis is time-scale for each day. The _slider_ lets on zoom on each section.  

###### Technical Details
1. Information was extracted from four dataframes - sleep, exercise, heart rate and step count using _pandas and datetime_ modules.
2. Three subplots were created to plot 3 graphs together.
3. The range slider and date picker components were used from _plotly_ module.

'''

tab_daily_layout = html.Div([
            html.H2('Daily Routine Analsis'),
            html.P('This graph shows day wise composite information on various user level data. '),
            html.Div([

            html.Div([
                
            html.Div([
            dcc.DatePickerSingle(
            id='my-date-picker-single',
            min_date_allowed=datetime(2019, 4, 5),
            max_date_allowed=datetime(2019, 5, 5),
            initial_visible_month=datetime(2019, 4, 15),
            date=datetime(2019,4,15)
    ),
    dcc.Graph(id='dashboard')
])

        ],className='nine columns'),

           html.Div([
            dcc.Markdown(children=markdown_text)
        ], className='three columns') 
        
        ])
], className="row")