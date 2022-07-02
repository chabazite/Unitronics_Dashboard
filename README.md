# Unitronics Dashboard
This is a project to help streamline data wrangling for my facility. Previously 
there was a technician that was forced to combine hundreds of excel files and 
pivot them to gain insights every month.

## Preliminary Work
I first used Access Database with VBA and SQL to extract, transform, and load 
the data. Then monthly I would query into a summary table. This saves hours of 
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

Unitronics Dashboard
==============================

## Business Case
<a name="Business_Case"></a>



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

 1. Data Scraping	
      * 1.1 Scraping DnDWiki using requests

 2. Business Understanding
      * 2.1 Background on Challenge Rating

 3. Data Wrangling
      * 3.1 Basic Cleanup
      * 3.2 Turn Challenge Rating into usable integer
      * 3.3 Create consolidated monster type column

 4. Exploratory Data Analysis
      * 4.1 Insights into General Monster Stat blocks

 5. Modeling
      * 5.1 Scikit-Learn MultiOutputRegressor

      

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
