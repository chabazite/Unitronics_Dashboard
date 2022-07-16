from DAG_functions import extractData, transformData, loadData

device_df, sensor_df, alarm_df = extractData()

device_df, sensor_df, alarm_df = transformData(device_df, sensor_df, alarm_df)

loadData(device_df, sensor_df, alarm_df)
