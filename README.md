
Unitronics Dashboard
==============================

## Business Case
<a name="Business_Case"></a>

When first starting at Stowers, there was one task in particular that I noticed 
a severe time sink. Every month they would spend an entire day combining hundreds
of csv files for the entire month for all 12 racks. Then create pivot tables
to gain insights into the month. They would also invidividuall move each of these
files from a local computer into their respective folders on the department drive.

While this was helful in looking back at our previous month of equipment states, 
there were some glaring issues I thought I could fix immediately. 

1) The file names are structured the same, we can automate the moving process.
2) We can automate the concat process through sql queries
3) We can automate the pivot process and then have all historic data in a nice 
graph to look back at every month to help with trends.

Ultimately, this should cause the time to go from 8 hours a month to less than 
10 minutes!

### Preliminary Work
I first used Access Database with VBA and SQL to extract, transform, and load 
the data. Then monthly I would query into a summary table. This save hours of 
time for the technician monthly. However, it still was only able to help us
look at issues after they had occured.

Additionally, we weren't even using the water quality or alarm data!I knew the 
water quality and equipment state data could be used in real time to help prevent emergencies
from cropping up in the facility.

We currently recieve csv files every day from the PLCs, which
contain data by the minute. If this project proves successful, I will change the 
download capabilities to decrease time between data writing so we can see real-
time data as it is occuring.

### Current Work

   1) Setup a postgreSQL database with three tables to house past and future data
   2) Using python, transfer historic data from csv into database
   3) Create a dashboard that provides easy-to-understand visuals
   4) Create and maintain an ETL pipeline using Airflow to provide near real-time 
   data for the dashboard.

## Table of Contents
<details open>
  <summary>Show/Hide</summary>
  <br>
 
1. [ File Descriptions ](#File_Description)
2. [ Technologies Used ](#Technologies_Used)    
3. [ Structure ](#Structure)
4. [ Evaluation ](#Evaluation)
5. [ Future Improvements ](#Future_Improvements)

</details>


## Project Organization

<details>
<a name="File_Description"></a>
<summary>Show/Hide</summary>
 <br>


    ├── LICENSE
    ├── .gitignore
    ├── README.md          <- The top-level README for developers using this project.
    ├──
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── deployment         <- Folder that contains all deployment needs
    │   ├── structure_app.py         <- first iteration dashboard
    │
    ├── env                <- Virtual Environment for the project
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    └── src                <- Source code for use in this project.
        ├── __init__.py    <- Makes src a Python module
        │
        ├── data           <- Scripts to download or generate data
        |   ├── selenium_scrape.py
        │   └── make_dataset.py
        │
        ├── features       <- Scripts to turn raw data into features for modeling
        │   └── build_features.py
        │
        ├── models         <- Scripts to train models and then use trained models to make              
        │   |                 predictions
        │   └── test_model.py    
        │
        └── visualization  <- Scripts to create exploratory and results oriented visualizations

--------
  </details>   

## Technologies Used:
<details>
<a name="Technologies_Used"></a>
<summary>Show/Hide</summary>
<br>

    ├──Airflow
    ├──Linux
    ├──PostgreSQL
    ├──PowerBi  
    ├──Python
        ├──Numpy
        ├──Pandas
        ├──OS
        ├──RegEx
        ├──DASH
 
 ------------
 </details>

## Structure of Notebooks:
<details>
<a name="Structure"></a>
<summary>Show/Hide</summary>
<br>

 1.0 Historic Data Wrangling Attempt	
      * 1.0.1 Scraping DnDWiki using requests

 1.1 Historic Alarm Data Wrangling
      * 1.1.1 Background on Challenge Rating

 1.2 Historic Sensor Data Wrangling
      * 1.2.1 Basic Cleanup

 1.3 Historic Device Data Wrangling
      * 1.3.1 Insights into General Monster Stat blocks


 </details>

## Evaluation:
<a name="Evaluation"></a>
<details>
<summary>Show/Hide</summary>
<br>


</details>
  
## Future Improvements
 <a name="Future_Improvements"></a>
 <details>
<summary>Show/Hide</summary>
<br>


</details>

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
<p>README outline tailored from [awesomeahi95][]<p>
