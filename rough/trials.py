

from turtle import width
from numpy import size
import pandas as pd #(version 0.24.2)
from datetime import datetime as dt
import dash         #(version 1.0.0)
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, callback
dash.register_page(__name__, path="/")
import plotly       #(version 4.4.1)
import plotly.express as px

df= pd.read_csv("sp_irad_accident.csv")
df['SUBMIT_DATE'] = pd.to_datetime(df['insert_date'])
df.set_index('SUBMIT_DATE', inplace=True)
#-------------------------------------------------------------------------------------
# Drop rows w/ no animals found or calls w/ varied age groups
#df = df[(df['# of Animals']>0) & (df['Age']!='Multiple')]

# Extract month from time call made to Ranger
df['Month'] = pd.to_datetime(df['insert_date'])
df['Month'] = df['Month'].dt.strftime('%m')
df['Month']
df['Crashes']=1

# df = df.filter(["crash_type", "Month","Crashes","year",'state','total_dead'], axis=1)
# df= df.groupby(['crash_type','Month','year','state','total_dead']).sum().reset_index()
#-------------------------------------------------------------------------------------
layout = html.Div(
    [
        
                    #title
                    html.Div([
                        html.Pre(children= "Bar Charts for RBG Accidents",
                        style={"text-align": "center", "font-size":"200%", "color":"black"})
                            ]),
                    
                    html.Div([
                        dbc.Row(
                            [
                                dbc.Col( dbc.Row([]),),
                                    
                                
                            
                                dbc.Col(
                                    dbc.Row(
                                        [
                                        #Radiobutton 2

                                        ],
                                    ),
                                ),
                        
                            
                                dbc.Col(
                                    dbc.Row(
                                        [
                                            #DatePicker

                                        ],
 
                                    ),
                                )
                            ],
                        )
                    ]),
        
                    html.Div([
                        dcc.Graph(id='the_graph')
                    ])

    ]
)      
 

#-------------------------------------------------------------------------------------
@callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='xaxis_raditem', component_property='value'),
    Input(component_id='yaxis_raditem', component_property='value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')]
)

def update_graph(x_axis, y_axis, start_date, end_date):

    dff = df.loc[start_date:end_date]
    barchart=px.bar(
            data_frame=dff,
            x=x_axis,
            y=y_axis,
            title=y_axis+': by '+x_axis
            )

    barchart.update_layout(xaxis={'categoryorder':'total ascending'},
                           title={'xanchor':'center', 'yanchor': 'top', 'y':0.9,'x':0.5,})
    barchart.update_traces(marker_color='black')
    barchart.update_xaxes(type='category')
    barchart.update_xaxes(categoryorder='category ascending')

    return (barchart)

# if __name__ == '__main__':
#     app.run_server(debug=True, port=2000)
