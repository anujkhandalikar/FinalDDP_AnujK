import dash
# Code from: https://github.com/plotly/dash-labs/tree/main/docs/demos/multi_page_example1
dash.register_page(__name__)

from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import plotly.express as px
import pandas as pd

df1 = pd.read_csv("sp_irad_accident.csv")

df1['Month'] = pd.to_datetime(df1['insert_date'])
df1['Month'] = df1['Month'].dt.strftime('%m')
df1['Crashes']=1

df = df1.filter(["crash_type", "Month","Crashes"], axis=1)
df_m=df.copy()
df_m= df_m.groupby(['crash_type','Month']).sum().reset_index().pivot('Month','crash_type').fillna(0)
df_m.columns = df_m.columns.droplevel(0)
df_m = df_m.reset_index().rename_axis(None, axis=1)

layout = html.Div(
    [
        html.Div([
            html.Pre(children= "HeatMap  for RBG Accidents",
            style={"text-align": "center", "font-size":"200%", "color":"black"})
        ]),
        html.P("Crashes included:"),
        dcc.Checklist(
            id="crashes",
            options=[{"label": x, "value": x} for x in df_m.columns],
            value=df_m.columns.tolist(),
        ),
        dcc.Graph(id="heatmaps-graph"),
    ]
)


@callback(Output("heatmaps-graph", "figure"), Input("crashes", "value"))
def filter_heatmap(cols):
    fig = px.imshow(df_m[cols])
    return fig
    