import pandas as pd
import os
import re
import psycopg2
from sqlalchemy import create_engine

#engine
conn_string = '***REMOVED***://***REMOVED***:***REMOVED***@***REMOVED***/***REMOVED***'
engine = create_engine(conn_string)
db = create_engine(conn_string)
conn = db.connect()

def createDataFrame():
    df_temp = pd.read_csv(
        dir_name+'/'+file,parse_dates=[['Date','Time']])
    df_temp['rack_num'] = rack_num
    return df_temp


def formatDataFrame(df):
    df.drop(['Row'], axis=1, inplace=True)
    df.columns = ['date_time', 'alarm','rack_num',]
    return df


dir_name = "C:/Users/ai2318/Desktop/Unitronics"
alarm_df = pd.DataFrame(columns={'date_time', 'alarm','rack_num'})

for file in os.listdir(dir_name):
    rack_num = re.search(r'CF(.*?)\.', file)[1]
    if 'Alarms' in file:
        df_temp = formatDataFrame(createDataFrame())
        alarm_df = pd.concat([alarm_df, df_temp], axis=0)
alarm_df = alarm_df[~alarm_df['alarm'].str.contains(
             'Alarm', na=False)]
alarm_df = alarm_df[~alarm_df['alarm'].str.contains(
             'Test', na=False)]
alarm_df.drop_duplicates(
            subset=['date_time'], inplace=True)
alarm_df.to_sql('alarm_log', con=conn,
                        if_exists='append',index=False)
# 
# conn = psycopg2.connect(conn_string)
# conn.autocommit = True
print(alarm_df)