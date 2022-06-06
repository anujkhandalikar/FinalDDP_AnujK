import pandas as pd #(version 0.24.2)
from datetime import datetime as dt
import dash         #(version 1.0.0)
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, callback
dash.register_page(__name__)
import plotly       #(version 4.4.1)
import plotly.express as px
import json
df = pd.read_csv("sp_irad_accident.csv")
df['Crashes']=1
df['SUBMIT_DATE'] = pd.to_datetime(df['insert_date'])
df.set_index('SUBMIT_DATE', inplace=True)

df = df.filter(["state","Crashes","total_dead","total_injured"], axis=1)
df=df.groupby('state').sum().reset_index()

layout = html.Div(
    [
        
                    #title
                    html.Div([
                        html.Pre(children= "ChoroPleth Charts for RBG Accidents",
                        style={"text-align": "center", "font-size":"200%", "color":"black"})
                    ]),

                      
                    html.Div([
                            dbc.Row(
                            [
                                dbc.Col( dbc.Row([]),),
                                dbc.Col( dbc.Row([
                                    #Radiobutton 1
                                        html.Label(['Plot Data For:'],style={"text-align": "center",'font-weight': 'bold'}),
                                        dcc.Dropdown(
                                        id='xaxis_raditem',
                                        options=[
                                                {'label': 'Number of Crashes', 'value': 'Crashes'},
                                                {'label': 'Number of Dead People ', 'value': 'total_dead'},
                                                {'label': 'Number of Injured People', 'value': 'total_injured'}
                                            ],
                                        value='total_dead',
                                        style={"width": "100%"}
                                        )
                                    ])),
                                    dbc.Col( dbc.Row([]),)
                            ]
                            )
                    ]),
                        # #Radiobutton 1
                        # html.Label(['X-axis Categories:'],style={'font-weight': 'bold'}),
                        # dcc.RadioItems(
                        # id='xaxis_raditem',
                        # options=[
                        #         {'label': '# of Crashes ', 'value': 'Crashes'},
                        #         {'label': '# of Dead People ', 'value': 'total_dead'},
                        #         {'label': '# of Injured People', 'value': 'total_injured'}
                        #     ],
                        # value='total_dead',
                        # style={"width": "100%"}
                        # )

    dbc.Container(
                [
                    
                dbc.Row([    
                    html.Div([
                    dcc.Graph(id='chor_graph')
                    ])
                    ],
                    style={"align":"center"}),
                            
                ]
    )


    ]
)

india_states=json.load(open("states_india.geojson",'r'))
@callback(
    Output(component_id='chor_graph', component_property='figure'),
    [Input(component_id='xaxis_raditem', component_property='value')]
)


def update_graph(rad_button):

    chorchart = px.choropleth(
                df,
                geojson=india_states,
                featureidkey='properties.state_code',
                locations='state',
                color=rad_button,
                color_continuous_scale='Plasma'
        )

    chorchart.update_geos(fitbounds="locations", visible=False)


    return (chorchart)