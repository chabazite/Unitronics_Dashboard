import os
import datetime as dt

#create variables for last month and that month's year
now = dt.datetime.now()
last_month = str(now.month-1) if now.month>1 else str(12)
last_month_year = str(now.year - 1) if now.month==1 else str(now.year)
folder_name = last_month_year + last_month

path = '/Users/Public/Documents/Individual Rack Data'


for folder in os.listdir(path):
    current_folder = os.path.join(path,folder)

    #Check if Rack folders have last month's directory
    folder_exists = os.path.exists(current_folder+'/'+folder_name)
         
   #Create folders for each rack to house last month data
    if not folder_exists:
        os.mkdir(os.path.join(current_folder,folder_name))
    
