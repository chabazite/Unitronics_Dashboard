# Unitronics Dashboard
This is a project to help streamline data wrangling for my facility. Previously 
there was a technician that was forced to combine hundreds of excel files and 
pivot them to gain insights every month.

## Preliminary Work
I first used Access Database with VBA and SQL to extract, transform, and load 
the data. Then monthly I would query into a summary table. This save hours of 
time for the technician monthly. However, it still was only able to help us
look at issues after they had occured, I knew the water quality and 
equipment state data could be used in real time to help prevent emergencies
from cropping up in the facility.

## Current Program
Using Dash framwork, python, and setting up an ETL pipeline with Azure, I am 
attempting to create a up-to-date dashboard that can help up monitor our systems 
in real time. We currently recieve csv files every day from the PLCs, which
contain data by the minute. If this project proves successful, I will change the 
download capabilities to decrease time between data writing so we can see real-
time data as it is occuring.

I would like us to be able to compare to past year, monthly data, and drill down
to daily data. 