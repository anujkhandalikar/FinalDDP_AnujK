import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash, dcc, html, Input, Output, callback
from dash.dependencies import Input, Output
import plotly.express as px
from datetime import datetime as dt
import dash_bootstrap_components as dbc
dash.register_page(__name__)

df = pd.read_csv("sp_irad_accident.csv")
df['SUBMIT_DATE'] = pd.to_datetime(df['insert_date'])
df.set_index('SUBMIT_DATE', inplace=True)
df['Month'] = pd.to_datetime(df['insert_date'])
df['Month'] = df['Month'].dt.strftime('%m')
df['Month']
df['Crashes']=1

# you need to include __name__ in your Dash constructor if
# you plan to use a custom CSS or JavaScript in your Dash apps
#app = dash.Dash(__name__)

#                               -
layout = html.Div([
    html.Div([
            html.Pre(children= "Pie Charts for RBG Accidents",
            style={"text-align": "center", "font-size":"200%", "color":"black"})
        ]),
    html.Div([
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Row([])),
                    
                    dbc.Col(
                        dbc.Row([
                            html.Label(['Choose the Chart you want'],style={'font-weight': 'bold'}),
                            dcc.Dropdown(
                                id='my_dropdown',
                                options=[
                                        {'label': 'Crash Types ', 'value': 'crash_type'},
                                        {'label': 'Year Wise Crashes ', 'value': 'year'},
                                        {'label': 'Severity Crashes ', 'value': 'severity'},
                                        {'label': 'Initial Observation Type ', 'value': 'initial_observation'},
                                        {'label': 'Collision Types', 'value': 'collision_type'}
                                        
                                ],
                                value='crash_type',
                                multi=False,
                                clearable=False,
                                style={"width": "100%"}
                            ),
                        ],
                        ),
                    ),
                    dbc.Col(
                        dbc.Row([
                            html.Br(),
                            html.Label(['Choose the Date'],style={'font-weight': 'bold'}),
                            html.Br(),
                            dcc.DatePickerRange(
                                #DatePicker
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
                    ),
                    dbc.Col(
                        dbc.Row([

                            ],
                        ),
                    )
                ]
            )
        ]),
    
    dbc.Row(
                [
                    dbc.Col(
                        dbc.Row([])
                        ),
                    dbc.Col(
                        dbc.Row([    
                            html.Div([
                            dcc.Graph(id='pie_graph')
                                ],
                            style={'width': '90vh', 'height': '90vh'}
                            )])
                        ),
                    dbc.Col(
                        dbc.Row([])
                        ),
                ]
    )
])

#                               -
@callback(
    Output(component_id='pie_graph', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')]
)

def update_graph(my_dropdown,start_date, end_date):
    dff = df.loc[start_date:end_date]

    piechart=px.pie(
            data_frame=dff,
            names=my_dropdown
            )

    piechart.update_traces(textposition='inside', textinfo='percent+label')
    return (piechart)


# if __name__ == '__main__':
#     app.run_server(debug=True, port = 3000)
