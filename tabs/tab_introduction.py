import dash_html_components as html
import dash_core_components as dcc
import base64

img_path = './images/Intro.png'
img_base64 = base64.b64encode(open(img_path, 'rb').read()).decode('ascii')
intro_text="""
###### Background
Aim of the project is to analyze user data collected from Samsung health app and provide interactive plots that allow for data exploration and figures that summarize relevant trends. The _trend analysis_ is an important tool to assess consumer behavior and often paves way for new solution by drawing insights from the available data. The analysis would be done using the following raw files on **[sleep, steps, exercise, heart rate etc.](https://raw.githubusercontent.com/kshitijmamgain/Health-Analysis/master/datasets)**   

The schema of the project is presented below:  
###### Data Preprocessing  

__About Samsung Health Data__: The data has been taken from a samsung user. The provided datasets would come under 4 classes defined by Samsung ([here](https://developer.samsung.com/onlinedocs/health/com/samsung/android/sdk/healthdata/HealthConstants.html)).:\


- Activity: step_count, exercise, floors_climbed
- Rest: sleep, sleep_data
- Health Care: calories_burned, heart_rate, stress
- Summary: daily_summary, step_daily_trend

Time is a common feature in all the data following is the crucial information for data preprocessing\
    

###### Trend Analysis  
  i.   Weekly Trends  
  ii.  Histograms  
  iii. Box plots  
###### Daily Analysis  
  i.   Preparing a daily profile of the user using - step count, heart rate and sleep data

###### Methodology
The received data was very messy and required a lot of preparation to fraw insights. The problem was more complex since the project dealt with time transformation. A part of data required transforming timestamp to date while other required manipulation based on UTC timezone. A large task was also to deal with missing values and data imputations.  
The daily dashboard required advance operations on data joining, grouping and wrangling.  
The project outline was first done on Jupyter Notebook using **pandas, numpy, datetime, matplotlib and seaborn** packages. The second part involved translating selected graphs and info into interactive plots using **plotly and dash package**. The last part involved deploying the project as a web app.
"""
tab_about_layout = html.Div([
  html.Div([  
    html.Div([
                dcc.Markdown(children=intro_text, style={'marginLeft': '3em', 'marginTop': '5em'})
              ], className = "seven columns"),
              
    #Right panel.
    
    html.Div([
                html.Img(
                  src='data:image/png;base64,{}'.format(img_base64),
                  style={'width':'600px', 'height':'800px', 'margin':'auto'}),
                dcc.Markdown(
                    """
                    
                    """
                )
            ], style={'marginTop': '3em'}, className="five columns"),
     
        ], className="row")
])