#import the necessary libraries

import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

#loading the dataset
df_primary=pd.read_excel(r'C:\Users\ENVY\Desktop\third dash cen data\primary.xlsx') # read data of primary education status
df_secondary=pd.read_excel(r'C:\Users\ENVY\Desktop\third dash cen data\secondary.xlsx') # read data of secondary education status

#initialize the app and make size for each device
#instantiate an app
app=dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],
              meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],

)
server = app.server

#application layout
app.layout=dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Census main Indicators interactive report",className='text-center text-primary mb-4 font-weight-bold')
        ],width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.P('This interactive dasboard provides information on main indicators from 2022 RPHC, you have right to select different indicators to see how they change'),
            html.Label('Select indicator'),
            dcc.Dropdown(id='indicators',
                         value='education level',
                         options=['education level','employment','access to medical insurance']),
            html.Div(id='indicator-sent'),
            html.Label('select province'),
            dcc.Dropdown(id='sclt-province',
                         multi=False,
                         value='East',
                         options=[{'label':x,'value':x} for x in df_primary['Provinces'].unique()]),
            html.Label('select districts'),
            dcc.Dropdown(id='district-drpn',
                         multi=True,
                         options=[]),
            dcc.Graph(id='indicator-grap',figure={})
        ],width={'size':5,'offset':1}),

    ])

])

@app.callback(
        Output('indicator-sent','children'),
        Input('indicators','value')
)
def update_text(slctindicator):
    if slctindicator=='education level':
        return ('In Rwanda, {} percent of children between 7-12 were in primary school,\n'
                ' female were {} percent and male were {} percent.'.format(df_primary[df_primary['Districts']=='Rwanda'].squeeze()[2],df_primary[df_primary['Districts']=='Rwanda'].squeeze()[3],df_primary[df_primary['Districts']=='Rwanda'].squeeze()[4]))
    elif slctindicator=='employment':
        return ('In Rwanda, {} percent of children between 13-18 were in secondary school,\n'
                ' female were {} percent and male were {} percent.'.format(df_secondary[df_secondary['Districts']=='Rwanda'].squeeze()[2],df_secondary[df_secondary['Districts']=='Rwanda'].squeeze()[3],df_secondary[df_secondary['Districts']=='Rwanda'].squeeze()[4]))

# @app.callback(
#          Output('indicator-grap','figure'),
#          Input('indicators','value')
# )
# def graph_update(slctindicator):
#     if slctindicator=='education level':
#         fig=px.bar(df_primary[1:],
#                    x='Districts',
#                    y=['Both sexes','Female','Male'],
#                    barmode='group')
#         fig.update_layout(xaxis_title='Districts',yaxis_title='education status',title='status of {} in Rwanda'.format(slctindicator))
#         return fig
#     elif slctindicator=='employment':
#         fig=px.bar(df_secondary[1:],
#                    x='Districts',
#                    y=['Both sexes', 'Female', 'Male'],
#                    barmode='group')
#         fig.update_layout(xaxis_title='Districts', yaxis_title='employment status',title='status of {} in Rwanda'.format(slctindicator))
#         return fig

@app.callback(
        Output('district-drpn','options'),
        Input('sclt-province','value')
)
def update_district(province_slctd):
    dff_primary=df_primary[df_primary['Provinces']==province_slctd]
    return ([{'label':x,'value':x} for x in sorted(dff_primary['Districts'].unique())])
    dff_secondary=df_secondary[df_secondary['Provinces']==province_slctd]
    return ([{'label': x,'value': x} for x in sorted(dff_secondary['Districts'].unique())])

#populate initial values
@app.callback(
        Output('district-drpn','value'),
        Input('district-drpn','options')
)
def set_district_values(available_options):
    return [x['value'] for x in available_options]

@app.callback(
        Output('indicator-grap','figure'),
        [[Input('district-drpn','value'),
         Input('sclt-province','value'),
         Input('indicators','value')]]
)
def update_graph(district_slct,province_slct,select_indicators):
    if len(district_slct)==0:
        return dash.no_update
    if select_indicators=='education level':
        dff_primary=df_primary[(df_primary['Provinces']==province_slct) & (df_primary['Districts'].isin(district_slct))]
        fig=px.bar(dff_primary,
        x='Districts',
        y=['Both sexes','Female','Male'],
        barmode='group')
        fig.update_layout(xaxis_title='Districts', yaxis_title='education status',
                          title='status of {} in {}'.format(select_indicators,province_slct))
        return fig
    elif select_indicators=='employment':
        dff_secondary = df_secondary[(df_secondary['Provinces'] == province_slct) & (df_secondary['Districts'].isin(district_slct))]
        fig=px.bar(dff_secondary,
        x='Districts',
        y=['Both sexes', 'Female', 'Male'],
        barmode='group')
        fig.update_layout(xaxis_title='Districts', yaxis_title='education status',
                          title='status of {} in {}'.format(select_indicators,province_slct))
        return fig

app.run_server(debug=True, port=3000)