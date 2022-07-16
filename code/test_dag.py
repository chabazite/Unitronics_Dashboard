import pandas as pd
from src.dataframe import createDateFrame, formateDataFrame
from sqlalchemy import create_engine
import re
import os
from dataframe import formatDataFrame, createDataFrame

def extractData():

    dir_name = "C:/Users/Public/Desktop"

    #dataframe creation
    device_df = pd.DataFrame(columns={'rack_num', 'Date_Time' 'Device', 'State'})
    alarm_df = pd.DataFrame(columns={'rack_num', 'Date_Time' 'Device', 'State'})
    sensor_df = pd.DataFrame(columns={'rack_num', 'Date_Time' 'Device', 'State'})

    super_df_device = []
    super_df_sensor = []
    super_df_alarm = []

    for root, dirs, files in os.walk(dir_name):
        for filename in files:
            rack_number = re.search(r'CF(.*?)\.', filename)[1]
            try:
                if 'Device' in filename:
                    print(os.path.join(root, filename))
                    df_temp_device = createDataFrame()
                    super_df_device.append(df_temp_device)
                elif 'Sensor' in filename:
                    print(os.path.join(root, filename))
                    df_temp_sensor = createDataFrame()
                    super_df_sensor.append(df_temp_sensor)
                elif 'Alarm' in filename:
                    print(os.path.join(root, filename))
                    df_temp_alarm = createDataFrame()
                    super_df_alarm.append(df_temp_alarm)
            except (TypeError) as error:
                print(error)
                continue


    device_df = formatDataFrame(super_df_device)
    device_df = device_df[['rack_num', 'Date_Time', 'Device', 'State']]
    device_df.drop_duplicates(
        subset=['Date_Time'], inplace=True)

    sensor_df = formatDataFrame(super_df_sensor)
    sensor_df.drop(['DO'], axis=1, inplace=True)
    sensor_df = sensor_df[['rack_num', 'Date_Time', 'pH',
                           'Conductivity', 'Temperature', 'Flow', 'Level']]
    sensor_df.drop_duplicates(
        subset=['Date_Time'], inplace=True)
    
    alarm_df = formatDataFrame(super_df_alarm)
    alarm_df = alarm_df[['rack_num', 'Date_Time', 'Alarm']]
    alarm_df.drop_duplicates(
        subset=['Date_Time'], inplace=True)

    
    return device_df, sensor_df, alarm_df


def transformDeviceData(device_df):

    #rename for postgreSQL
    device_df.rename(columns={'rack_num': 'rack_num', 'Date_Time': 'date_time',
                              'Device': 'device', 'State': 'state_'}, inplace=True)
    # Remove NaN values and wingdings, flow has largest set of NA values
    device_df = device_df[~device_df['device'].isna()]
    # convert timestamp to string
    device_df['date_time'] = device_df.date_time.astype(str)

    #remove any non-timestamp dates (wingdings)
    device_df = device_df[device_df.date_time.str.contains(
        r'\d{2}:\d{2}:\d{2}', regex=True)]

    #check for remaining wonky dates
    device_df[~device_df.date_time.str.contains(
        r'\d{2}/\d{2}/\d{2}', regex=True) & ~device_df.date_time.str.contains(
        r'\d{4}-\d{2}-\d{2}', regex=True)]

    #turn feature into timestamp
    device_df['date_time'] = pd.to_datetime(
        device_df['date_time'])

    #convert to standard date time format
    device_df.date_time = device_df['date_time'].dt.strftime(
        '%Y-%m-%d %H:%M:%S')

    #Check all datetime format the same
    device_df[~device_df.date_time.str.contains(
        r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', regex=True)]

    device_df['state_'] = device_df['state_'].astype(int)

    return device_df

def transformSensorData(sensor_df):

    #rename for postgreSQL
    sensor_df.rename(columns={'rack_num': 'rack_num', 'Date_Time': 'date_time', 'pH': 'ph',
                                'Conductivity': 'conductivity', 'Temperature': 'temperature', 
                                'Flow': 'flow', 'Level': 'level_'}, inplace=True)

    sensor_df = sensor_df[~sensor_df['flow'].isna()]

    # convert timestamp to string
    sensor_df['date_time'] = sensor_df.date_time.astype(str)
    #remove any non-timestamp dates (wingdings)
    sensor_df = sensor_df[sensor_df.date_time.str.contains(
        r'\d{2}:\d{2}:\d{2}', regex=True)]

    #check for remaining wonky dates
    sensor_df[~sensor_df.date_time.str.contains(
        r'\d{2}/\d{2}/\d{2}', regex=True) & ~sensor_df.date_time.str.contains(
        r'\d{4}-\d{2}-\d{2}', regex=True)]

    #remove the date with letters in it
    sensor_df = sensor_df[~sensor_df.date_time.str.contains(
        r'\b[a-z]', regex=True)]

    sensor_df = sensor_df[sensor_df.date_time.str.contains('¯')]

    #turn feature into timestamp
    sensor_df['date_time'] = pd.to_datetime(
        sensor_df['date_time'])

    #convert to standard date time format
    sensor_df.date_time = sensor_df['date_time'].dt.strftime(
        '%Y-%m-%d %H:%M:%S')
    sensor_df['level_'] = sensor_df.level_.astype(float)


    return sensor_df


def transformAlarmData(alarm_df):


    alarm_df.rename(columns={'rack_num': 'rack_num',
                      'Date_Time': 'date_time', 'Alarm': 'alarm'}, inplace=True)

    # Remove NaN values and wingdings
    alarm_df = alarm_df[~alarm_df['alarm'].isna()]

    searchfor = ['System Manually Stopped', 'Low Water Level CO', 'Low Water Level', 'Low Temperature CO', 'Low Temperature', 'Low pH', 'Low Flow CO', 'Low Flow', 'Low Conductivity', 'Inspect Water Pump', 'Inspect Water Ex Solenoid', 'Inspect UV Lamps', 'Inspect UV',
                 'Inspect pH Dosing Pump', 'Inspect Heater', 'Inspect Cond Dosing Pump', 'Inspect Carbon', 'Inspect Air Pump', 'Inspect 50 Micron', 'High Water Level CO', 'High Water Level', 'High Temperature CO', 'High Temperature', 'High pH CO', 'High pH', 'High Flow', 'High Conductivity CO', 'High Conductivity']
    alarm_df = alarm_df[alarm_df['alarm'].str.contains('|'.join(searchfor))]

    return alarm_df

def transformData(device_df, sensor_df, alarm_df):

    device_df = transformDeviceData(device_df)
    sensor_df = transformSensorData(sensor_df)
    alarm_df = transformAlarmData(alarm_df)
    
    return device_df, sensor_df, alarm_df


def loadData(device_df, sensor_df, alarm_df):
    

    conn_string = 'postgresql://postgres:postgres@aquatics01.sgc.loc/Cavefish'
    db = create_engine(conn_string)
    conn = db.connect()

    df.to_sql('device_log', con=conn,
                        if_exists='append', index=False,chunksize=10000)