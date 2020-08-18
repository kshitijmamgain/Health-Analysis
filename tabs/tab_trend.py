import dash_html_components as html
import dash_core_components as dcc

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

trends_layout = html.Div(children=[
                    html.Div([
                        html.Div([
                            html.H1(children='Trends Analysis on Different Indicators')],className='nine columns'),
                            dash_components.data_picker,]),
                    
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

                ], className='row')