import pandas as pd
import os
import re
import psycopg2
from sqlalchemy import create_engine
import configuration.helper as helper
config = helper.read_config()
host = config['Database']['host']
dbase = config['Database']['dbase']
userName = config['Database']['userName']
password = config['Database']['password']

#engine
conn_string = username,'://',username,':'password,'@',host,'/',dbase
engine = create_engine(conn_string)
db = create_engine(conn_string)
conn = db.connect()


#columns for postgres
columns_alarm = ('rack_num', 'date_time', 'alarm')
columns_sensor = ('rack_num', 'date_time', 'ph',
                  'conductivity', 'temperature', 'flow', 'level_')
columns_device = ('rack_num', 'date_time', 'device', 'state_')



def createDataFrame():
    df_temp = pd.read_csv(dir_name_month+'/'+file,
                          parse_dates=[['Date', 'Time']], encoding="ISO-8859-1", on_bad_lines='skip')
    df_temp['rack_num'] = rack_num
    df_temp.drop(['Row'], axis=1, inplace=True)
    return df_temp


def formatDataFrame(df):
    df = pd.concat([df, df_temp], axis=0)
    df.reset_index(inplace=True, drop=True)
    return df


dir_name = "L:/Cavefish/Facility/Life Support Systems/PLC Data Logs/Individual Rack Data"

#dataframe creation
alarm_df = pd.DataFrame(columns={'rack_num', 'Date_Time', 'Alarm'})
device_df = pd.DataFrame(columns={'rack_num', 'Date_Time' 'Device', 'State'})
sensor_df = pd.DataFrame(columns={'rack_num', 'Date_Time',
                         'Level', 'Temperature', 'pH', 'Conductivity', 'Flow', 'DO'})

for folder in os.listdir(dir_name):
    dir_name_rack = dir_name + '/' + folder
    for year_folder in os.listdir(dir_name_rack):
        dir_name_year = dir_name + '/' + folder + '/' + year_folder
        for month_folder in os.listdir(dir_name_year):
            dir_name_month = dir_name + '/' + folder + '/'+year_folder+'/'+month_folder
            for file in os.listdir(dir_name_month):
                rack_num = re.search(r'CF(.*?)\.', file)[1]
                try:
                    if 'Alarms' in file:
                        df_temp = createDataFrame()
                        alarm_df = formatDataFrame(alarm_df)
                        alarm_df = alarm_df[~alarm_df['Alarm'].str.contains(
                            'Alarm', na=False)]
                        alarm_df = alarm_df[~alarm_df['Alarm'].str.contains(
                            'Test', na=False)]
                        alarm_df = alarm_df[['rack_num', 'Date_Time', 'Alarm']]
                        alarm_df.drop_duplicates(
                            subset=['Date_Time'], inplace=True)
                        alarm_df.to_sql('alarm_log', con=conn,
                                        if_exists='append', index=False)
                    elif 'Sensor' in file:
                        df_temp = createDataFrame()
                        sensor_df = formatDataFrame(sensor_df)
                        sensor_df.drop(['DO'], axis=1, inplace=True)
                        sensor_df = sensor_df[['rack_num', 'Date_Time', 'pH',
                    'Conductivity', 'Temperature', 'Flow', 'Level']]
                        sensor_df.drop_duplicates(
                            subset=['Date_Time'], inplace=True)
                        sensor_df.to_sql('sensor_log', con=conn,
                                          if_exists='append',index=False)
                    elif 'Device' in file:
                        df_temp = createDataFrame()
                        device_df = formatDataFrame(device_df)
                        device_df = device_df[[
                            'rack_num', 'Date_Time', 'Device', 'State']]
                        device_df.drop_duplicates(
                            subset=['Date_Time'], inplace=True)
                        device_df.to_sql('device_log', con=conn, if_exists='append', index=False)
                    conn = psycopg2.connect(conn_string)
                    conn.autocommit =True
                except TypeError:
                    continue



