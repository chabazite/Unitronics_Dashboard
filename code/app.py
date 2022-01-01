# Import requred libraries and read the dataset
import pandas as pd
import plotly.express as px
import dash
from dash import html
from dash import dcc

#read in the data (Eventually this will come from RDBMS)
#water_quality_data = pd.read_csv()
#equipment_state_data = pd.read_csv()

#This is where we will use plotly to create charts

#Create a dash application
app = dash.Dash(__name__)


app.title = "Unitronix Dashboard"

def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("Unitronix Dashboard"),
                    html.H6("Equipment State and Water Quality Reporting")
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.Button(
                        id="help-button",children="HELP", n_clicks=0
                    ),
                    html.A(
                        html.Img(id="logo",src=app.get_asset_url("***REMOVED***-logo.png")),
                        href="URL",
                    ),
                ],
            ),
        ],
    )

def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab2",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Equip-tab",
                        label="Equipment State Analysis",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Water-Quality-tab",
                        label="Water Quality Analysis",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )

def generate_help():
    return html.Div(
        id="markdown",
        className="help",
        children=(
            html.Div(
            id="markdown-container",
            className="markdown-container",
            children=[
                html.Div(
                    className="close-container",
                    children=html.Button(
                        "Close",
                        id="markdown_close",
                        n_clicks=0,
                        className="closeButton",
                    ),
                ),
                html.Div(
                    className="markdown-text",
                    children=dcc.Markdown(
                        children=(
                            """
                    ##### What is the Unitronix Dashboard for?

                    This is a dashboard for monitoring real-time equipment state
                    and water quality for all Racks in the facility.

                    ##### What does this app show?

                    The good stuff

                    ##### How do I use this app?

                    Easily
                """
                        )
                    ),
                ),
            ],
        )
    ),
)
#Get the layout of the application and adjust it.
#Create an outer division using html.Div and add title to the dashboard using 
# html.H1 component with css styling
#Add description about the graph using HTML P (paragraph) compenent and css 
# stlying
#Finally, add graph component and subsequent figures
app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                #Main app
                #html.Div(id-"app-content"),
            ],
        ),
        generate_help(),
    ],
)




#Run the application
if __name__ =='__main__':
    app.run_server()