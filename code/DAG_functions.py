import pandas as pd
from sqlalchemy import create_engine
import re
import os
from dataframe import concatDataFrame, createDataFrame
from sqlalchemy.exc import IntegrityError

def extractData(dir_name):
    """
    function that parses through folder structure and uses the createDataFrame 
    function to read the individual csv files, then concatonates them into a 
    single dataframe for each table type.

    Returns:
        DataFrame: Three dataframes, one for each table in the database
    """

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
                    df_temp_device = createDataFrame(root, filename, rack_number)
                    super_df_device.append(df_temp_device)
                elif 'Sensor' in filename:
                    df_temp_sensor = createDataFrame(
                        root, filename, rack_number)
                    super_df_sensor.append(df_temp_sensor)
                elif 'Alarms' in filename:
                    df_temp_alarm = createDataFrame(root, filename, rack_number)
                    super_df_alarm.append(df_temp_alarm)
            except (TypeError) as error:
                print(error)
                continue

    device_df = concatDataFrame(super_df_device)
    device_df = device_df[['rack_num', 'Date_Time', 'Device', 'State']]
    device_df.drop_duplicates(
        subset=['Date_Time'], inplace=True)

    sensor_df = concatDataFrame(super_df_sensor)
    sensor_df.drop(['DO'], axis=1, inplace=True)
    sensor_df = sensor_df[['rack_num', 'Date_Time', 'pH',
                           'Conductivity', 'Temperature', 'Flow', 'Level']]
    sensor_df.drop_duplicates(
        subset=['Date_Time'], inplace=True)
    
    alarm_df = concatDataFrame(super_df_alarm)
    alarm_df = alarm_df[['rack_num', 'Date_Time', 'Alarm']]
    alarm_df.drop_duplicates(
        subset=['Date_Time'], inplace=True)

    
    return device_df, sensor_df, alarm_df


def transformDeviceData(device_df):
    """
    function that formats and wrangles the device log dataframe extracted in the
    extractData function. Removes corrupted data, reformates date column, and 
    prepares the dataframe to merge with the postgres database

    Args:
        device_df (DataFrame): the dataframe for devices created in the extract function

    Returns:
        DataFrame: formated dataframe
    """
    #rename for postgreSQL
    device_df.rename(columns={'rack_num': 'rack_num', 'Date_Time': 'date_time',
                              'Device': 'device', 'State': 'state_'}, inplace=True)

    # Remove NaN values
    device_df = device_df[~device_df['device'].isna()]

    # convert timestamp to string
    device_df['date_time'] = device_df.date_time.astype(str)

    #remove any non-timestamp dates (wingdings)
    device_df = device_df[device_df.date_time.str.contains(
        r'\d{2}:\d{2}:\d{2}', regex=True)]

    #turn feature into timestamp
    device_df['date_time'] = pd.to_datetime(
        device_df['date_time'])

    #convert to standard date time format
    device_df.date_time = device_df['date_time'].dt.strftime(
        '%Y-%m-%d %H:%M:%S')

    device_df['state_'] = device_df['state_'].astype(int)

    return device_df

def transformSensorData(sensor_df):
    """
    function that formats and wrangles the sensor log dataframe extracted in the
    extractData function. Removes corrupted data, reformates date and 
    prepares the dataframe to merge with the postgres database

    Args:
        sensor_df (DataFrame): the dataframe for sensor created in the extract function

    Returns:
        DataFrame: wrangled dataframe ready to load into database
    """
    #rename for postgreSQL
    sensor_df.rename(columns={'rack_num': 'rack_num', 'Date_Time': 'date_time', 'pH': 'ph',
                                'Conductivity': 'conductivity', 'Temperature': 'temperature', 
                                'Flow': 'flow', 'Level': 'level_'}, inplace=True)
    
    # Remove NaN values
    sensor_df = sensor_df[~sensor_df['flow'].isna()]

    # convert timestamp to string
    sensor_df['date_time'] = sensor_df.date_time.astype(str)

    #remove any non-timestamp dates (wingdings)
    sensor_df = sensor_df[sensor_df.date_time.str.contains(
        r'\d{2}:\d{2}:\d{2}', regex=True)]

    #remove dates with letters in it
    sensor_df = sensor_df[~sensor_df.date_time.str.contains(
        r'\b[a-z]', regex=True)]

    #remove dates with '¯' in it
    sensor_df = sensor_df[~sensor_df.date_time.str.contains('¯')]

    #turn feature into timestamp
    sensor_df['date_time'] = pd.to_datetime(
        sensor_df['date_time'])

    #convert to standard date time format
    sensor_df.date_time = sensor_df['date_time'].dt.strftime(
        '%Y-%m-%d %H:%M:%S')

    sensor_df['level_'] = sensor_df.level_.astype(float)

    return sensor_df


def transformAlarmData(alarm_df):
    """
    function that formats and wrangles the alarm log dataframe extracted in the
    extractData function. Removes corrupted data and 
    prepares the dataframe to merge with the postgres database

    Args:
        alarm_df (DataFrame): the dataframe for alarms created in the extract function

    Returns:
        DataFrame: wrangled dataframe ready to load into database
    """
    alarm_df.rename(columns={'rack_num': 'rack_num',
                      'Date_Time': 'date_time', 'Alarm': 'alarm'}, inplace=True)

    # Remove NaN values
    alarm_df = alarm_df[~alarm_df['alarm'].isna()]

    searchfor = ['System Manually Stopped', 'Low Water Level CO', 'Low Water Level', 'Low Temperature CO', 'Low Temperature', 'Low pH', 'Low Flow CO', 'Low Flow', 'Low Conductivity', 'Inspect Water Pump', 'Inspect Water Ex Solenoid', 'Inspect UV Lamps', 'Inspect UV',
                 'Inspect pH Dosing Pump', 'Inspect Heater', 'Inspect Cond Dosing Pump', 'Inspect Carbon', 'Inspect Air Pump', 'Inspect 50 Micron', 'High Water Level CO', 'High Water Level', 'High Temperature CO', 'High Temperature', 'High pH CO', 'High pH', 'High Flow', 'High Conductivity CO', 'High Conductivity']

    alarm_df = alarm_df[alarm_df['alarm'].str.contains('|'.join(searchfor))]

    return alarm_df

def transformData(device_df, sensor_df, alarm_df):
    """
    function that consolodates individual transform Data functions for each dataframe.

    Args:
        device_df (DataFrame): extracted datframe created in extractData()
        sensor_df (DataFrame):  extracted datframe created in extractData()
        alarm_df (DataFrame):  extracted datframe created in extractData()

    Returns:
        DataFrames: Three dataframes now ready to load into postgres database
    """
    device_df = transformDeviceData(device_df)
    sensor_df = transformSensorData(sensor_df)
    alarm_df = transformAlarmData(alarm_df)
    
    return device_df, sensor_df, alarm_df

def checkIntegrity(df,log_name,conn):
    """
    runs through each line of the dataframe and checks if there is a primary key 
    duplicate in the database. This prevents dup errors.

    Args:
        df (dataframe): the dataframe to be checked against the database
        log_name (string): the name of the table in the database
        conn (engine): SQLAlchemy engine
    """
    for i in range(len(df)):
        try:
          df.iloc[i:i+1].to_sql(log_name, con=conn,
                                if_exists='append', index=False, chunksize=10000)
        except IntegrityError:
            pass

def loadData(device_df, sensor_df, alarm_df):
    """
    ingests dataframes that were transformed into the postgres database

    Args:
        device_df (DataFrame): wrangled dataframe ready for ingestion
        sensor_df (DataFrame):  wrangled dataframe ready for ingestion
        alarm_df (DataFrame):  wrangled dataframe ready for ingestion
    """

    conn_string = 'postgresql://postgres:postgres@aquatics01.sgc.loc/Cavefish'
    db = create_engine(conn_string)
    conn = db.connect()

    checkIntegrity(device_df, 'device_log', conn)
    checkIntegrity(sensor_df, 'sensor_log', conn)
    checkIntegrity(alarm_df, 'alarm_log', conn)

def deleteFiles(dir_name):
    """
    deletes files ingested into database

    Args:
        dir_name (string): directory path where files will be deleted
    """
    for root, dirs, files in os.walk(dir_name):
        for filename in files:
            os.remove(root+'/'+filename)