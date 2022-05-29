import psycopg2


conn = psycopg2.connect("host=***REMOVED*** dbname=***REMOVED*** user=***REMOVED*** password = ***REMOVED***")
cur = conn.cursor()

columns_alarm = ('rack_num','date_time','alarm')
columns_sensor = ('rack_num','date_time','ph', 'conductivity','temperature','flow','level_')
columns_device = ('rack_num', 'date_time', 'device', 'state_')

with open('alarm_log.csv','r') as f:
    next(f)
    cur.copy_from(f, 'alarm_log', sep=',', columns=columns_alarm)

with open('sensor_log.csv', 'r') as f:
    next(f)
    cur.copy_from(f, 'sensor_log', sep=',', columns=columns_sensor)

with open('device_log.csv', 'r') as f:
    next(f)
    cur.copy_from(f, 'device_log', sep=',', columns=columns_device)
conn.commit()