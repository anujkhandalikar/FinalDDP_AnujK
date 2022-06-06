# Bar charts are useful for displaying data that is classified into nominal or ordinal categories.
# A bar chart uses bars to show comparisons between categories of data. A bar chart will always have two axis.
# One axis will generally have numerical values, and the other will describe the types of categories being compared.

from turtle import width
from numpy import size
import pandas as pd #(version 0.24.2)
from datetime import datetime as dt
import dash         #(version 1.0.0)
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, callback
dash.register_page(__name__)
import plotly       #(version 4.4.1)
import plotly.express as px

df= pd.read_csv("sp_irad_accident.csv")

#-------------------------------------------------------------------------------------
# Drop rows w/ no animals found or calls w/ varied age groups
#df = df[(df['# of Animals']>0) & (df['Age']!='Multiple')]

# Extract month from time call made to Ranger
df['Month'] = pd.to_datetime(df['insert_date'])
df['Month'] = df['Month'].dt.strftime('%m')
df['Crashes']=1

df = df.filter(["Month","year","Crashes","total_dead","total_injured","insert_date"], axis=1)
df['SUBMIT_DATE'] = pd.to_datetime(df['insert_date']).dt.date

#-------------------------------------------------------------------------------------
layout = html.Div(
    [
        
                    #title
                    html.Div([
                        html.Pre(children= "Line Charts for RBG Accidents",
                        style={"text-align": "center", "font-size":"200%", "color":"black"})
                            ]),
                    
                    html.Div([
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Row(
                                        [
                                            #Radiobutton 1
                                            html.Label(['--X-axis Categories:'],style={'font-weight': 'bold'}),
                                            dcc.Dropdown(
                                            id='xaxis_raditem',
                                            options=[
                                                    {'label': 'Month--', 'value': 'Month'},
                                                    {'label': 'Year--', 'value': 'year'},
                                            ],
                                            value='Month',
                                            style={"width": "100%"}
                                            )
                                        ]
                                    ),
                                ),
                                    
                                
                            
                                dbc.Col(
                                    dbc.Row(
                                        [
                                            #Radiobutton 2
                                            html.Br(),
                                            html.Label(['Y-axis Values:'], style={'font-weight': 'bold'}),
                                            dcc.Dropdown(
                                                id='yaxis_raditem',
                                                options=[
                                                        {'label': 'Number of people dead', 'value': 'total_dead'},
                                                        {'label': 'Number of people injured', 'value': 'total_injured'},
                                                        {'label': 'Number of crashes', 'value': 'Crashes'}
                                                        
                                                ],
                                                value='total_dead',
                                                style={"width": "100%"}
                                            )
                                        ],
                                    ),
                                ),
                        
                            
                                dbc.Col(
                                    dbc.Row(
                                        [
                                            #DatePicker
                                            html.Br(),
                                            html.Label(['Choose TimeFrame'],style={'font-weight': 'bold'}),
                                            html.Br(),
                                            dcc.DatePickerRange(
                                                id='my-date-picker-range',  # ID to be used for callback
                                                calendar_orientation='horizontal',  # vertical or horizontal
                                                day_size=39,  # size of calendar image. Default is 39
                                                end_date_placeholder_text="Return",  # text that appears when no end date chosen
                                                with_portal=False,  # if True calendar will open in a full screen overlay portal
                                                first_day_of_week=0,  # Display of calendar when open (0 = Sunday)
                                                reopen_calendar_on_clear=True,
                                                is_RTL=False,  # True or False for direction of calendar
                                                clearable=True,  # whether or not the user can clear the dropdown
                                                number_of_months_shown=1,  # number of months shown when calendar is open
                                                min_date_allowed=dt(2021, 1, 2),  # minimum date allowed on the DatePickerRange component
                                                max_date_allowed=dt(2022, 4, 3),  # maximum date allowed on the DatePickerRange component
                                                initial_visible_month=dt(2021, 2, 22),  # the month initially presented when the user opens the calendar
                                                start_date=dt(2021, 1, 2).date(),
                                                end_date=dt(2022, 4, 3).date(),
                                                display_format='MMM Do, YY',  # how selected dates are displayed in the DatePickerRange component.
                                                month_format='MMMM, YYYY',  # how calendar headers are displayed when the calendar is opened.
                                                minimum_nights=2,  # minimum number of days between start and end date

                                                persistence=True,
                                                persisted_props=['start_date'],
                                                persistence_type='session',  # session, local, or memory. Default is 'local'

                                                updatemode='singledate'  # singledate or bothdates. Determines when callback is triggered
                                            )
                            
                                        ],
 
                                    ),
                                )
                            ],
                        )
                    ]),
        
                    html.Div([
                        dcc.Graph(id='line_graph')
                    ])

    ]
)      
 

#-------------------------------------------------------------------------------------
@callback(
    Output(component_id='line_graph', component_property='figure'),
    [Input(component_id='xaxis_raditem', component_property='value'),
    Input(component_id='yaxis_raditem', component_property='value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')]
)

def update_graph(x_axis, y_axis, start_date, end_date):
    start_date_dt = dt.strptime(start_date,"%Y-%m-%d").date()
    end_date_dt = dt.strptime(end_date,"%Y-%m-%d").date()

    date_range = (df['SUBMIT_DATE'] >= start_date_dt) & (df['SUBMIT_DATE'] <= end_date_dt)
    dff = df.loc[date_range]
    dff = dff.groupby(x_axis).sum()
    dff[x_axis] = dff.index
    linechart=px.line(
            data_frame=dff,
            x=x_axis,
            y=y_axis,
            title=y_axis+': by '+x_axis
            )

    linechart.update_layout(xaxis={'categoryorder':'total ascending'},
                           title={'xanchor':'center', 'yanchor': 'top', 'y':0.9,'x':0.5,})
    linechart.update_traces(marker_color='black')
    linechart.update_xaxes(categoryorder='category ascending')
   

    return (linechart)

# if __name__ == '__main__':
#     app.run_server(debug=True, port=2000)
