import pandas as pd
import os
import re



def createDataFrame():
    df_temp = pd.read_csv(dir_name+'/'+file, parse_dates=[['Date', 'Time']])
    df_temp['Rack'] = rack_num
    return df_temp


def formatDataFrame(df):
    df = pd.concat([df, df_temp], axis=0)
    df.drop(['Row'], axis=1, inplace=True)
    df.reset_index(inplace=True, drop=True)
    return df


dir_name = "C:/Users/ai2318/Desktop/Unitronics"

alarm_df = pd.DataFrame(columns={'Rack', 'Row', 'Date_Time', 'Alarm'})
device_df = pd.DataFrame(
    columns={'Rack', 'Row', 'Date_Time' 'Device', 'State'})
sensor_df = pd.DataFrame(columns={'Rack', 'Row', 'Date_Time',
                         'Level', 'Temperature', 'pH', 'Conductivity', 'Flow', 'DO'})

for file in os.listdir(dir_name):
    rack_num = re.search(r'CF(.*?)\.', file)[1]
    if 'Alarms' in file:
        df_temp = createDataFrame()
        alarm_df = formatDataFrame(alarm_df)
        alarm_df = alarm_df[~alarm_df['Alarm'].str.contains('Alarm')]
        alarm_df = alarm_df[~alarm_df['Alarm'].str.contains('Test')]

    elif 'Sensor' in file:
        df_temp = createDataFrame()
        sensor_df = formatDataFrame(sensor_df)
        sensor_df.drop(['DO'], axis=1, inplace=True)

    elif 'Device' in file:
        df_temp = createDataFrame()
        device_df = formatDataFrame(device_df)

#reordering columngs
alarm_df = alarm_df[['Rack', 'Date_Time', 'Alarm']]
sensor_df = sensor_df[['Rack', 'Date_Time', 'pH',
                'Conductivity', 'Temperature', 'Flow', 'Level']]
device_df = device_df[['Rack', 'Date_Time','Device', 'State']]

alarm_df.drop_duplicates(subset=['Date_Time'],inplace=True)
sensor_df.drop_duplicates(subset=['Date_Time'], inplace=True)
device_df.drop_duplicates(subset=['Date_Time'], inplace=True)


alarm_df.to_csv('alarm_log.csv',index=False)
sensor_df.to_csv('sensor_log.csv', index=False)
device_df.to_csv('device_log.csv',index=False)

device_df.duplicated(subset=['Date_Time']).value_counts()