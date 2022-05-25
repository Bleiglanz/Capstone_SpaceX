
# I did not work in the online IDE

import pandas as pd
import dash
from dash import html
from dash import dcc
from dash import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# The list of available launch sites as the data for the dropdown menu
sites = spacex_df['Launch Site'].unique().tolist()
options = [{'label': 'All Sites', 'value': 'ALL'}]
for s in sites:
    options.append({'label': s, 'value': s})


# Create a dash application
app = dash.Dash(__name__)

top = html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40})

dropdown = dcc.Dropdown(id='site_dropdown', options=options,
                        placeholder='Select Launch Site', searchable=True, value='ALL'),

marks = {i: "{} kg".format(i) for i in range(0, 11000, 1000)}

slider = dcc.RangeSlider(id='payload-slider', min=0, max=10000,
                         step=1000, marks=marks, value=[min_payload, max_payload],)

# Create an app layout
app.layout = html.Div(children=[html.Div(top), html.Br(),
                                html.Div(dropdown), html.Br(),
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Div(html.P("Payload range (Kg):")),
                                html.Div(slider),
                                html.Div(dcc.Graph(id='scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site_dropdown', component_property='value')]
)
def update_dropdown(drop_sel):
    df = spacex_df[spacex_df['class'] == 1]
    title = 'Total Launches By all sites'
    names = 'Launch Site'
    if drop_sel != 'ALL':
        df = spacex_df.loc[spacex_df['Launch Site'] == drop_sel]
        title = 'Total Launches for {} success is class=1, failure is class=0'.format(drop_sel)
        names = 'class'
    return px.pie(df, names=names, hole=.3, title=title)


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
     Output(component_id='scatter-chart', component_property='figure'),
     [Input(component_id='site_dropdown', component_property='value'),
      Input(component_id="payload-slider", component_property="value")]
)
def update_slider(drop_sel, slid_sel):
    low, high = slid_sel
    col = 'Payload Mass (kg)'
    if drop_sel == 'ALL':
        df = spacex_df[(spacex_df[col] > low) & (spacex_df[col] < high)]
    else:
        dfs = spacex_df[spacex_df['Launch Site'] == drop_sel]
        df = dfs[(dfs[col] > low) & (dfs[col] < high)]
    return px.scatter(df, x=col, y="class", color="Booster Version", size=col, hover_data=[col])
# Run the app


if __name__ == '__main__':
    app.run_server()
# %%
