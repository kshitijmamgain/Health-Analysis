import dash_html_components as html
import dash_core_components as dcc
from src import utils, dash_components
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

barplot_text = '''
  
  
__Bar-plot Summary__  
  
The bar charts are great statistical tool to compare the distribution of variables. It usually plots quantitative data with ranges of the data grouped into bins or intervals.  
i. The drop down menu enables one to *select* a day of week to visualize the distribution of different attributes.  
ii. The y-axis represents the aggregated values based on feature on x-axis.
'''
boxplot_text = '''
  
  
__Box-plot Summary__  
  
The graphs on the right do resemble like pretty dresses on display!  
The box-plots present important 5 points summary of a quantitative feature. The five horizontal lines represent max, upper quartile, median, lower quartile and min values.  
i. The slant in the notched setting represents the 95% confidence that the median lise in the present spot.  
ii. The interactive graphs further provide buttons to select sub types, you can try selecting exercise types.
'''

distplot_text = '''
  
  
__Contour-plot Summary__  
  
A contour plot is great tool to see how a response variable relates to two predictor variables. It provides a two-dimensional view in which all points that have the same response are connected to produce contour lines of constant responses. Contour plots are useful for investigating desirable response values and operating conditions.
A contour plot contains the following elements:  
i. Predictors on the x- and y-axes.  
ii. Contour lines that connect points that have the same response value.  
'''
trends_layout = html.Div(children=[
                    html.Div([
                        html.Div([
                            html.H1(children='Trends Analysis on Different Indicators')],className='nine columns'),
                            dash_components.data_picker,]),
                    
                    html.Div([
                        html.Div([
                            #html.H1(children='Bar-plot Summary'),
                            dcc.Graph(id='bar-graph')],className='nine columns'),
                            dash_components.day_picker,
                            dcc.Markdown(children=barplot_text)]),
    
                    html.Div(children=[
                        html.Div([
                            #html.H3(children='Box-plot Summary',style ={'textAlign':'center','color': colors['text']}),
                            dcc.Graph(id='boxplot-graph')],className='nine columns'),
                            dash_components.boxPlotOptions,
                        html.Div([
                            dcc.Markdown(children=boxplot_text)], className='three columns')]),
                        
                    html.Div([
                        html.Div([                        
                            #html.H3('Distplot summary '),
                            dcc.Graph(id='distplot-graph')], className='nine columns'),
                        html.Div([
                            dcc.Markdown(children=distplot_text)], className='three columns')])
                ], className='row')