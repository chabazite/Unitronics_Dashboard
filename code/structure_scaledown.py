#import the required libraries
import dash
import pandas as pd
import plotly.express as px
from dash import html
from dash import dcc
from dash.dependencies import Input, Output


#Using the Dash framework created by plotly to make an interactive & real-time 
#dashboard for continuous Water Quality and Equipment state data

#initialize the app
app=dash.Dash(__name__)

#read in the data
df_water_quality=pd.read_csv('..\data\CFRACK12_Sensor Input_01_12_21_23_57.csv')
df_equip_state=pd.read_csv('..\data\CFRACK12_Device Log_01_12_21_23_57.csv')

"""Compute graph data for water quality reports

Function that takes water quality data as input and create 5 dataframes based on the grouping condition to be used for plottling charts and grphs.

Argument:
     
    df_water_quality: Filtered dataframe
    
Returns:
   Dataframes to create graph. 
"""

def compute_data_choice_1(df_WQ):
    # Conductivity
    conductivity_data=df_WQ.groupby(['Rack_Number','Time'])['Conductivity'].sum().reset_index()
    # pH
    ph_data=df_WQ.groupby(['Rack_Number','Time'])['pH'].sum().reset_index()
    # Flow
    flow_data=df_WQ.groupby(['Rack_Number','Time'])['Flow'].sum().reset_index()
    # Water Level
    water_level_data=df_WQ.groupby(['Rack_Number','Time'])['Level'].sum().reset_index()
    # Temperature
    temperature_data=df_WQ.groupby(['Rack_Number','Time'])['Temperature'].sum().reset_index()
   
    return ph_data, conductivity_data, flow_data, water_level_data, temperature_data
    

"""Compute graph data for creating equipment state analysis

This function takes in equipment state data, Rack location, and time as an input and performs computation for creating charts and plots.

Arguments:
    df_equip_state: Input equipment state data.
    
Returns:
    dataframes for graphs.
"""

def compute_data_choice_2(df_ES):
    # pH pump
    pH_pump_data=df_ES[(df_ES['Device_E']=='pH Pump')].groupby(['Rack_Number','Date_E','Device_E'])['State_E'].sum().reset_index()
    # Conductivity pump
    Conductivity_pump_data=df_ES[(df_ES['Device_E']=='Conductivity Pump')].groupby(['Rack_Number','Date_E','Device_E'])['State_E'].sum().reset_index()
    # Heat Exchange Compression (Turning Heat Pump on/off)
    Heat_Compressor_data=df_ES[(df_ES['Device_E']=='Heat Ex Comp')].groupby(['Rack_Number','Date_E','Device_E'])['State_E'].sum().reset_index()
    # Cooling (switching heat pump to cooling)
    Water_exchange_data=df_ES[(df_ES['Device_E']=='Effulent Coil')].groupby(['Rack_Number','Date_E','Device_E'])['State_E'].sum().reset_index()
    # Heating (switching heat pump to heating)
    Cooling_data=df_ES[(df_ES['Device_E']=='Cooling')].groupby(['Rack_Number','Date_E','Device_E'])['State_E'].sum().reset_index()
#This is the full layout of the app
    return pH_pump_data, Conductivity_pump_data, Heat_Compressor_data, Water_exchange_data, Cooling_data


app.layout = html.Div( style={'backgroundColor': '#111111','color':'white'}, children=[
                 #Header Div
                html.Div([
                    # Top Left App Title DIV
                    html.H1('Unitronics1 Dashboard',
                                    style={'textAlign': 'left',
                                           'font-size': 20
                                            }),
                    #Top Right Help Button DIV
                    html.Button('Help', id='help',n_clicks=0),
                ]),
                #Main Body DIV
                html.Div([
                    #Two Tabs from Water Quality to Equipment Analysis
                    dcc.Tabs(id="tabs",value='tab-1-Water-Quality', children=[
                        dcc.Tab(label='Water Quality', 
                                value='tab-1-Water-Quality'),
                        dcc.Tab(label='Equipment State',
                                value='tab-2-Equipment-State'),
                    ]),
                    html.Div([
                         html.Label('Rack Numbers'),
                            dcc.Checklist(
                                id='RackNumber',
                                options=[
                                    {'label': 'MUW', 'value':'MUW'},
                                    {'label': 'Rack 1', 'value':'Rack 1'},
                                    {'label': 'Rack 2', 'value':'Rack 2'},
                                    {'label': 'Rack 3', 'value':'Rack 3'},
                                    {'label': 'Rack 5', 'value':'Rack 5'},
                                    {'label': 'Rack 6', 'value':'Rack 6'},
                                    {'label': 'Rack 7', 'value':'Rack 7'},
                                    {'label': 'Rack 8', 'value':'Rack 8'},
                                    {'label': 'Rack 9', 'value':'Rack 9'},
                                    {'label': 'Rack 10', 'value':'Rack 10'},
                                    {'label': 'Rack 12', 'value':'Rack 12'}
                                ], value=['MUW']
                            ),
                            html.Br(),
                    ]),
                    #Graph Section
                    html.Div([
                        html.Div([], id='plot1'),
                        html.Div([], id='plot2')
                        ]),
                    html.Div([
                        html.Div([],id='plot3'),
                        html.Div([],id='plot4'),
                        html.Div([],id='plot5')
                    ],style={'display':'flex'}),
                ]),
            ])

@app.callback([Output(component_id='plot1', component_property='children'),
                Output(component_id='plot2', component_property='children'),
                Output(component_id='plot3', component_property='children'),
                Output(component_id='plot4', component_property='children'),
                Output(component_id='plot5', component_property='children')],
                [Input(component_id='tabs', component_property='value'),
                 Input(component_id='RackNumber', component_property='value'),
                 ])


def get_graph(chart, Rack):

    df_WQ = df_water_quality[df_water_quality['Rack_Number'].isin(Rack)]
    df_ES = df_equip_state[df_equip_state['Rack_Number'].isin(Rack)]
    print(df_WQ['Rack_Number'])
    print(Rack)
    if chart == 'tab-1-Water-Quality':
        
        # Compute data for creating graph
        ph_data, conductivity_data, flow_data, water_level_data, temperature_data = compute_data_choice_1(df_WQ)

        pH_fig = px.line(ph_data, x='Time', y='pH', color='Rack_Number', title='pH')

        conductivity_fig = px.line(conductivity_data, x='Time', y='Conductivity', color='Rack_Number', title='Conductivity')

        flow_fig =  px.line(flow_data, x='Time',y='Flow', color='Rack_Number',
        title='Water Flow Rate')

        water_level_fig =  px.line(water_level_data, x='Time', y='Level', 
        color='Rack_Number', title='Water Level')

        temperature_fig = px.line(temperature_data, x='Time', y='Temperature', 
        color='Rack_Number', title='Temperautre')

        return [
                dcc.Graph(figure=pH_fig),
                dcc.Graph(figure=conductivity_fig),
                dcc.Graph(figure=flow_fig),
                dcc.Graph(figure=water_level_fig),
                dcc.Graph(figure=temperature_fig)
             ]
    else:
        pH_pump_data, Conductivity_pump_data, Heat_Compressor_data, Water_exchange_data, Cooling_data=compute_data_choice_2(df_ES)
        
        #Create Graph
        pH_pump_fig=px.bar(pH_pump_data, x='Date_E', y='State_E', 
            color='Rack_Number', title= "pH Pump State")
       
        conductivity_pump_fig=px.bar(Conductivity_pump_data, x='Date_E', 
            y='State_E', color='Rack_Number', title= "Conductivity Pump State")

        Heat_Comp_fig=px.bar(Heat_Compressor_data, x='Date_E', y='State_E', 
            color='Rack_Number', title= "Heat Compressor State")

        Water_Exchange_fig=px.bar(Water_exchange_data, x='Date_E', y='State_E',
            color='Rack_Number', title= "Water Exchange State")

        Cooling_fig=px.bar(Cooling_data, x='Date_E', y='State_E', 
            color='Rack_Number', title= "Cooling State")
        return [dcc.Graph(figure=pH_pump_fig),
                dcc.Graph(figure=conductivity_pump_fig),
                dcc.Graph(figure=Heat_Comp_fig),
                dcc.Graph(figure=Water_Exchange_fig),
                dcc.Graph(figure=Cooling_fig)
             ]

if __name__ =='__main__':
    app.run_server(debug=False,port=8005)