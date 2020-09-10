import os
import flask
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from tabs import tab_introduction, tab_daily, tab_trend
from src import utils, dash_components

# Create instances of a flask web framework 
server = flask.Flask(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server)
app.config['suppress_callback_exceptions'] = True
app.scripts.config.serve_locally = True


app.layout = html.Div([
        # header/title display
        html.Div([
            html.H1('Health Data Analysis'),
            html.H4('Designed by: Kshitij Mamgain', style={'textAlign': 'center', 'color': "#ffffff"})], 
            style={'padding': '50px', 'backgroundColor': '#009dc4'}),
        # Define tabs
        dcc.Tabs(id="tabs-main", value='tab-intro', children=[
            dcc.Tab(label='Introduction', value='tab-intro'),
            dcc.Tab(label='Daily Analysis', value='tab-daily'),
            dcc.Tab(label='Trend Analysis', value='trends'),]),
        # define tabs call back id
        html.Div(id='tabs-contents') ])

# Tabs callback

@app.callback(Output('tabs-contents', 'children'),
              [Input('tabs-main', 'value')] )

def render_content(tab):

    if tab == 'tab-daily':
        return tab_daily.tab_daily_layout

    elif tab == 'trends':
        return tab_trend.trends_layout

    elif tab == 'tab-intro':
        return tab_introduction.tab_about_layout

@app.callback(
    Output('dashboard', 'figure'),
    [Input('my-date-picker-single', 'date')])
def health_dashboard(date):
    return utils.dailygraph(date)


# ------------------------
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
def build_boxgraph(attribute,view):
    return utils.boxplot(attribute,view)

@app.callback(
    Output(component_id='distplot-graph', component_property='figure'),
    [Input(component_id='attribute_dropdown', component_property='value')])
def build_distgraph(attribute):
    return utils.distplot(attribute)


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))
    # app.run_server(debug=True)