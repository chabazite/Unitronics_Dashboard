#import the required libraries
import dash
import pandas as pd
import plotly.express as px
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


#Using the Dash framework created by plotly to make an interactive & real-time 
#dashboard for continuous Water Quality and Equipment state data

#initialize the app
app=dash.Dash(external_stylesheets=[dbc.themes.SOLAR])

#create sidebar stlying

#Created Main content stlying

#read in the data
df_water_quality=pd.read_csv('..\data\Sensor_Input.csv')
df_equip_state=pd.read_csv('..\data\Device_Log.csv')

"""Compute graph data for water quality reports

Function that takes water quality data as input and create 5 dataframes 
based on the grouping condition to be used for plottling charts and grphs.

Argument:
     
    df_water_quality: Filtered dataframe
    
Returns:
   Dataframes to create graph. 

This has been separated based on the 3 possible datasets (daily, monthly, or yearly)
called by the filter. Each function returns a different dataset.
"""

def compute_data_daily_WQ(df_WQ):
    # Conductivity grouping Racknumber and Time, while finding the mean for that time period
    conductivity_data=df_WQ.groupby(['Rack_Number','Time'])['Conductivity'].mean().reset_index()
    # pH
    ph_data=df_WQ.groupby(['Rack_Number','Time'])['pH'].mean().reset_index()
    # Flow
    flow_data=df_WQ.groupby(['Rack_Number','Time'])['Flow'].mean().reset_index()
    # Water Level
    water_level_data=df_WQ.groupby(['Rack_Number','Time'])['Level'].mean().reset_index()
    # Temperature
    temperature_data=df_WQ.groupby(['Rack_Number','Time'])['Temperature'].mean().reset_index()
   
    return ph_data, conductivity_data, flow_data, water_level_data, temperature_data

def compute_data_monthly_WQ(df_WQ):
    conductivity_data=df_WQ.groupby(['Rack_Number','Month'])['Conductivity'].mean().reset_index()
    ph_data=df_WQ.groupby(['Rack_Number','Month'])['pH'].mean().reset_index()
    flow_data=df_WQ.groupby(['Rack_Number','Month'])['Flow'].mean().reset_index()
    water_level_data=df_WQ.groupby(['Rack_Number','Month'])['Level'].mean().reset_index()
    temperature_data=df_WQ.groupby(['Rack_Number','Month'])['Temperature'].mean().reset_index()
   
    return ph_data, conductivity_data, flow_data, water_level_data, temperature_data

def compute_data_yearly_WQ(df_WQ):
    conductivity_data=df_WQ.groupby(['Rack_Number','Year'])['Conductivity'].mean().reset_index()
    ph_data=df_WQ.groupby(['Rack_Number','Year'])['pH'].mean().reset_index()  
    flow_data=df_WQ.groupby(['Rack_Number','Year'])['Flow'].mean().reset_index()
    water_level_data=df_WQ.groupby(['Rack_Number','Year'])['Level'].mean().reset_index()
    temperature_data=df_WQ.groupby(['Rack_Number','Year'])['Temperature'].mean().reset_index()
   
    return ph_data, conductivity_data, flow_data, water_level_data, temperature_data


"""Compute graph data for creating equipment state analysis

This function takes in equipment state data, Rack location, and time as an input
 and performs computation for creating charts and plots. Just like the WQ datasets,
 this is split into 3 (daily, monthly, and yearly) based on user input

Arguments:
    df_equip_state: Input equipment state data.
    
Returns:
    dataframes for graphs.
"""

def compute_data_daily_ES(df_ES):
    # pH pump
    pH_pump_data=df_ES[(df_ES['Device_E'] == 'pH Pump')].groupby([
        'Rack_Number','Date_E','Device_E'])['State_E'].sum().reset_index()
    # Conductivity pump
    Conductivity_pump_data=df_ES[(df_ES['Device_E'] == 'Conductivity Pump')].groupby([
        'Rack_Number','Date_E','Device_E'])['State_E'].sum().reset_index()
    # Heat Exchange Compression (Turning Heat Pump on/off)
    Heat_Compressor_data=df_ES[(df_ES['Device_E'] == 'Heat Ex Comp')].groupby([
        'Rack_Number','Date_E','Device_E'])['State_E'].sum().reset_index()
    # Water Exchange 
    Water_exchange_data=df_ES[(df_ES['Device_E'] == 'Effulent Coil')].groupby([
        'Rack_Number','Date_E','Device_E'])['State_E'].sum().reset_index()
    # Cooling (switching heat pump to cooling)
    Cooling_data=df_ES[(df_ES['Device_E'] == 'Cooling')].groupby([
        'Rack_Number','Date_E','Device_E'])['State_E'].sum().reset_index()

    return pH_pump_data, Conductivity_pump_data, Heat_Compressor_data, Water_exchange_data, Cooling_data



def compute_data_monthly_ES(df_ES):
    pH_pump_data=df_ES[(df_ES['Device_E'] == 'pH Pump')].groupby([
        'Rack_Number','Month_E','Device_E'])['State_E'].sum().reset_index()

    Conductivity_pump_data=df_ES[(df_ES['Device_E'] == 'Conductivity Pump')].groupby([
        'Rack_Number','Month_E','Device_E'])['State_E'].sum().reset_index()

    Heat_Compressor_data=df_ES[(df_ES['Device_E'] == 'Heat Ex Comp')].groupby([
        'Rack_Number','Month_E','Device_E'])['State_E'].sum().reset_index()

    Water_exchange_data=df_ES[(df_ES['Device_E'] == 'Effulent Coil')].groupby([
        'Rack_Number','Month_E','Device_E'])['State_E'].sum().reset_index()

    Cooling_data=df_ES[(df_ES['Device_E'] == 'Cooling')].groupby([
        'Rack_Number','Month_E','Device_E'])['State_E'].sum().reset_index()

    return pH_pump_data, Conductivity_pump_data, Heat_Compressor_data, Water_exchange_data, Cooling_data


def compute_data_yearly_ES(df_ES):

    pH_pump_data=df_ES[(df_ES['Device_E'] == 'pH Pump')].groupby([
        'Rack_Number','Year_E','Device_E'])['State_E'].sum().reset_index()

    Conductivity_pump_data=df_ES[(df_ES['Device_E'] == 'Conductivity Pump')].groupby([
        'Rack_Number','Year_E','Device_E'])['State_E'].sum().reset_index()

    Heat_Compressor_data=df_ES[(df_ES['Device_E'] == 'Heat Ex Comp')].groupby([
        'Rack_Number','Year_E','Device_E'])['State_E'].sum().reset_index()

    Water_exchange_data=df_ES[(df_ES['Device_E'] == 'Effulent Coil')].groupby([
        'Rack_Number','Year_E','Device_E'])['State_E'].sum().reset_index()

    Cooling_data=df_ES[(df_ES['Device_E'] == 'Cooling')].groupby([
        'Rack_Number','Year_E','Device_E'])['State_E'].sum().reset_index()

    return pH_pump_data, Conductivity_pump_data, Heat_Compressor_data, Water_exchange_data, Cooling_data



#Sidebar element which contains the filters. Used bootstrap for components (dbc)
sidebar = html.Div([
                html.H2("Filters", style={'textAlign': 'center',
                                           'font-size': 30}),
                html.Hr(),
                html.Div([
                    html.Label('Rack Numbers'),
                    dbc.Checklist(
                        id='RackNumber',
                        options=[
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
                html.Label('TimeFrame'),
                dbc.RadioItems(
                    id='TimeFrame',
                    options=[
                        {'label': 'Daily', 'value':'Daily'},
                        {'label': 'Monthly', 'value':'Monthly'},
                        {'label': 'Yearly', 'value':'Yearly'},
                            ],
                    value='Daily'),
                html.Br(),
                ]),   
            ])

#Main page of the app (graphs) which uses bootstrap for oranization and components
content = html.Div([
                dbc.Row([
                    dcc.Dropdown(id='chart-dropdown',
                        options=[
                            {'label': 'pH', 'value': 'pH'},
                            {'label': 'Conductivity', 'value': 'Conductivity'},
                            {'label': 'Water Level', 'value': 'Water Level'},
                            {'label': 'Flow Rate', 'value': 'Water Flow'},
                            {'label': 'Temperature', 'value': 'Temperature'},
                        ], value='pH')
                ]),
                dbc.Row([
                    html.Div([], id='plot1'),
                ]),
            ])


app.layout = html.Div([
                #Header row that includes title and help button column              
                dbc.Row([
                    dbc.Col(html.H1('Unitronics Dashboard',
                                    style={'textAlign': 'left',
                                           'font-size': 50}),
                            width={'size':10}),
                    dbc.Col(dbc.Button('Help', color='info',className='me-1'),
                    width={'size':2})
                ]),
                #Tab Row that allows us to change from WQ to Equipment
                dbc.Row([
                    dbc.Col(
                    dbc.Tabs(id="tabs",active_tab='tab-1-Water-Quality', children=[
                        dbc.Tab(label='Water Quality', 
                                tab_id='tab-1-Water-Quality'),
                        dbc.Tab(label='Equipment State',
                                tab_id='tab-2-Equipment-State'),
                    ]),
                    width={'size':12})
                ]),
                dbc.Row([
                    #Div surrounding both the graphs and sidebar filters
                   dbc.Col(sidebar,width={'size':3}),
                   dbc.Col(content,width={'size':9}),
                        #Sidebar filters                
                ]),
])

@app.callback(Output(component_id='plot1', component_property='children'),
                [Input(component_id='tabs', component_property='active_tab'),
                 Input(component_id="chart-dropdown", component_property='value'),
                 Input(component_id='RackNumber', component_property='value'),
                 Input(component_id='TimeFrame', component_property='value')
                 ])


def get_graph(chart, dropdown, Rack, Time):

    df_WQ = df_water_quality[df_water_quality['Rack_Number'].isin(Rack)]
    df_ES = df_equip_state[df_equip_state['Rack_Number'].isin(Rack)]


    if chart == 'tab-1-Water-Quality':
        if Time == 'Daily':
          
            ph_data, conductivity_data, flow_data, water_level_data, temperature_data = compute_data_daily_WQ(df_WQ)
           
            if dropdown == 'pH':  
              fig = px.line(ph_data, x='Time', y='pH', color='Rack_Number', title='pH',
                                labels={
                                    "Time": "Sampling Time",
                                })
              fig.add_shape(#add a horizontal "target" line"
                type ="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
                x0=0,x1=1,xref="paper", y0=7.65,y1=7.65,yref="y"
              )
            elif dropdown == 'Conductivity':
              fig = px.line(conductivity_data, x='Time', y='Conductivity', color='Rack_Number', title='Conductivity',
                                labels={
                                    "Time": "Sampling Time",
                                    "Conductivity": "Conductivity uS/cm"
                                })

              fig.add_shape(#add a horizontal "target" line"
                type ="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
                x0=0,x1=1,xref="paper", y0=800,y1=800,yref="y"
              )
            elif dropdown == "Water Flow":
              fig =  px.line(flow_data, x='Time',y='Flow', color='Rack_Number',
              title='Water Flow Rate')
            elif dropdown == "Water Level":
              fig =  px.line(water_level_data, x='Time', y='Level', 
              color='Rack_Number', title='Water Level')
            else:
              fig = px.line(temperature_data, x='Time', y='Temperature', 
              color='Rack_Number', title='Temperautre')

        elif Time == 'Monthly':
          
            ph_data, conductivity_data, flow_data, water_level_data, temperature_data = compute_data_monthly_WQ(df_WQ)
            if dropdown == 'pH':
              fig = px.line(ph_data, x='Month', y='pH', color='Rack_Number', title='pH')
            elif dropdown == "Conductivity":
              fig = px.line(conductivity_data, x='Month', y='Conductivity', color='Rack_Number', title='Conductivity')
            elif dropdown == "Water Flow":
              fig =  px.line(flow_data, x='Month',y='Flow', color='Rack_Number',
              title='Water Flow Rate')
            elif dropdown == "Water Level":
              fig =  px.line(water_level_data, x='Month', y='Level', 
              color='Rack_Number', title='Water Level')
            else:
              fig = px.line(temperature_data, x='Month', y='Temperature', 
              color='Rack_Number', title='Temperautre')

        else:
           
            ph_data, conductivity_data, flow_data, water_level_data, temperature_data = compute_data_yearly_WQ(df_WQ)
            if dropdown == 'pH':
              fig = px.line(ph_data, x='Year', y='pH', color='Rack_Number', title='pH')
            elif dropdown == 'Conductivity':
              fig = px.line(conductivity_data, x='Year', y='Conductivity', color='Rack_Number', title='Conductivity')
            elif dropdown == 'Water Flow':
              fig =  px.line(flow_data, x='Year',y='Flow', color='Rack_Number',
              title='Water Flow Rate')
            elif dropdown == 'Water Level':
              fig =  px.line(water_level_data, x='Year', y='Level', 
              color='Rack_Number', title='Water Level')
            else:
              fig = px.line(temperature_data, x='Year', y='Temperature', 
              color='Rack_Number', title='Temperautre')

    else:
        if Time =='Daily':
            pH_pump_data, Conductivity_pump_data, Heat_Compressor_data, Water_exchange_data, Cooling_data=compute_data_daily_ES(df_ES)

            if dropdown == "pH":
                fig=px.bar(pH_pump_data, x='Date_E', y='State_E', 
                    color='Rack_Number', title= "pH Pump State", barmode='group',
                                labels={
                                    "Date_E": "Sampling Date",
                                    "State_E": "Equipment Uses"
                                })
            elif dropdown == "Conductivity":
                fig=px.bar(Conductivity_pump_data, x='Date_E', 
                    y='State_E', color='Rack_Number', title= "Conductivity Pump State",
                     barmode='group',
                                labels={
                                    "Date_E": "Sampling Date",
                                    "State_E": "Equipment Uses"
                                }) 
            elif dropdown == "Water Level":
                fig=px.bar(Heat_Compressor_data, x='Date_E', y='State_E', 
                    color='Rack_Number', title= "Heat Compressor State", barmode='group',
                                labels={
                                    "Date_E": "Sampling Date",
                                    "State_E": "Equipment Uses"
                                })
                fig.layout.xaxis.tickvals = pd.date_range('2015-01', '2050-12', freq = 'MS')
            
            elif dropdown == "Water Flow":
                fig=px.bar(Water_exchange_data, x='Date_E', y='State_E',
                    color='Rack_Number', title= "Water Exchange State", barmode='group',
                                labels={
                                    "Date_E": "Sampling Date",
                                    "State_E": "Equipment Uses"
                                })
            else:
                fig=px.bar(Cooling_data, x='Date_E', y='State_E', 
                    color='Rack_Number', title= "Cooling State", barmode='group',
                                labels={
                                    "Date_E": "Sampling Date",
                                    "State_E": "Equipment Uses"
                                })

        elif Time == 'Monthly':
            pH_pump_data, Conductivity_pump_data, Heat_Compressor_data, Water_exchange_data, Cooling_data=compute_data_monthly_ES(df_ES)

            if dropdown == 'pH':       
                fig=px.bar(pH_pump_data, x='Month_E', y='State_E', 
                    color='Rack_Number', title= "pH Pump State", barmode='group',
                                labels={
                                    "Month_E": "Sampling Month",
                                    "State_E": "Equipment Uses"
                                })
                fig.layout.xaxis.tickvals = pd.date_range('2015-01', '2050-12', freq = 'MS')
                fig.layout.xaxis.tickformat = '%b-%y'
            elif dropdown == "Conductivity":
                fig=px.bar(Conductivity_pump_data, x='Month_E', 
                    y='State_E', color='Rack_Number', title= "Conductivity Pump State",
                     barmode='group',
                                labels={
                                    "Month_E": "Sampling Month",
                                    "State_E": "Equipment Uses"
                                })
                fig.layout.xaxis.tickvals = pd.date_range('2015-01', '2050-12', freq = 'MS')
                fig.layout.xaxis.tickformat = '%b-%y'     

            elif dropdown == "Water Flow":
                fig=px.bar(Heat_Compressor_data, x='Month_E', y='State_E', 
                    color='Rack_Number', title= "Heat Compressor State", barmode='group',
                                labels={
                                    "Month_E": "Sampling Month",
                                    "State_E": "Equipment Uses"
                                })
                fig.layout.xaxis.tickvals = pd.date_range('2015-01', '2050-12', freq = 'MS')
                fig.layout.xaxis.tickformat = '%b-%y'

            elif dropdown == "Water Level":
                fig=px.bar(Water_exchange_data, x='Month_E', y='State_E',
                    color='Rack_Number', title= "Water Exchange State", barmode='group',
                                labels={
                                    "Month_E": "Sampling Month",
                                    "State_E": "Equipment Uses"
                                })
                fig.layout.xaxis.tickvals = pd.date_range('2015-01', '2050-12', freq = 'MS')
                fig.layout.xaxis.tickformat = '%b-%y'

            else:
                fig=px.bar(Cooling_data, x='Month_E', y='State_E', 
                    color='Rack_Number', title= "Cooling State", barmode='group',
                                labels={
                                    "Month_E": "Sampling Month",
                                    "State_E": "Equipment Uses"
                                })
                fig.layout.xaxis.tickvals = pd.date_range('2015-01', '2050-12', freq = 'MS')
                fig.layout.xaxis.tickformat = '%b-%y'

        else:
            pH_pump_data, Conductivity_pump_data, Heat_Compressor_data, Water_exchange_data, Cooling_data=compute_data_yearly_ES(df_ES)
        
            if dropdown == 'pH':
                fig=px.bar(pH_pump_data, x='Year_E', y='State_E', 
                    color='Rack_Number', title= "pH Pump State", barmode='group',
                                labels={
                                    "Year_E": "Sampling Year",
                                    "State_E": "Equipment Uses"
                                })
                fig.layout.xaxis.tickvals = pd.date_range('2015-01', '2050-12', freq = 'MS')
                fig.layout.xaxis.tickformat = '%y'
            
            elif dropdown == 'Conductivity':    
                fig=px.bar(Conductivity_pump_data, x='Year_E', 
                    y='State_E', color='Rack_Number', title= "Conductivity Pump State",
                     barmode='group',
                                labels={
                                    "Year_E": "Sampling Year",
                                    "State_E": "Equipment Uses"
                                })
                fig.layout.xaxis.tickvals = pd.date_range('2015-01', '2050-12', freq = 'MS')
                fig.layout.xaxis.tickformat = '%y'     
            elif dropdown == 'Water Flow':    
                fig=px.bar(Heat_Compressor_data, x='Year_E', y='State_E', 
                    color='Rack_Number', title= "Heat Compressor State", barmode='group',
                                labels={
                                    "Year_E": "Sampling Year",
                                    "State_E": "Equipment Uses"
                                })
                fig.layout.xaxis.tickvals = pd.date_range('2015-01', '2050-12', freq = 'MS')
                fig.layout.xaxis.tickformat = '%y'
                
            elif dropdown == 'Water Level':    
                fig=px.bar(Water_exchange_data, x='Year_E', y='State_E',
                    color='Rack_Number', title= "Water Exchange State", barmode='group',
                                labels={
                                    "Year_E": "Sampling Year",
                                    "State_E": "Equipment Uses"
                                })
                fig.layout.xaxis.tickvals = pd.date_range('2015-01', '2050-12', freq = 'MS')
                fig.layout.xaxis.tickformat = '%y'

            else:
                fig=px.bar(Cooling_data, x='Year_E', y='State_E', 
                    color='Rack_Number', title= "Cooling State", barmode='group',
                                labels={
                                    "Year_E": "Sampling Year",
                                    "State_E": "Equipment Uses"
                                })
                fig.layout.xaxis.tickvals = pd.date_range('2015-01', '2050-12', freq = 'MS')
                fig.layout.xaxis.tickformat = '%y'

    return [dcc.Graph(figure=fig)
             ]

if __name__ =='__main__':
    app.run_server(debug=False,port=8005)