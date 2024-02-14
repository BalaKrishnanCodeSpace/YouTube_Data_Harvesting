# YouTube Data Harvesting and Warehousing: A Comprehensive Data Analysis Solution

## Introduction 

**The YouTube Data Harvesting and Warehousing project is a sophisticated system designed to facilitate seamless access and in-depth analysis of YouTube channel data. Leveraging cutting-edge technologies such as SQL, MongoDB, and Streamlit, this project empowers users to retrieve, store, and query YouTube channel and video data with utmost efficiency and precision.**


## Project Overview
**The YouTube Data Harvesting and Warehousing project comprises the following key components:**

### 1. Streamlit Application: An intuitive user interface developed using the Streamlit library, enabling users to interact with the application seamlessly and perform intricate data retrieval and analysis tasks effortlessly.

### 2. YouTube API Integration: Seamless integration with the YouTube API to procure comprehensive channel and video data based on specified channel IDs, ensuring a robust data retrieval mechanism.

### 3. MongoDB Data Lake: A robust and scalable MongoDB database serves as the foundation for storing and managing the retrieved data, offering unparalleled flexibility in handling unstructured and semi-structured data formats.

### 4. SQL Data Warehouse: Efficient migration of data from the MongoDB data lake to a SQL database (MySQL), enabling swift and effective querying and analysis through SQL queries.

### 5. Data Visualization: Utilization of Streamlit's advanced data visualization features to present the retrieved data in an insightful and visually appealing manner, empowering users to derive actionable insights through interactive charts and graphs.




![Intro GUI](https://github.com/Gopinathalpha7/YouTube_Data_Harvesting_and_Warehousing./blob/88b80dca65246a606d9495deddad95202c685430/youtube%20data%20harvesting%20gui.png)


## Developer Guide 

### 1. Tools Install

* Virtual code.
* Jupyter notebook.
* Python 3.11.0 or higher.
* MySQL.
* MongoDB.
* Youtube API key.

### 2. Requirement Libraries to Install

* pip install google-api-python-client, pymongo, mysql-connector-python, sqlalchemy, pymysql, pymysql, pandas, numpy, 
  plotly-express, streamlit.
  
 ( pip install google-api-python-client pymongo mysql-connector-python sqlalchemy pymysql pandas numpy plotly-express streamlit )
 
### 3. Import Libraries

**Youtube API libraries**
* import googleapiclient.discovery
* from googleapiclient.discovery import build

**File handling libraries**
* import json
* import re

**MongoDB**
* import pymongo

**SQL libraries**
* import mysql.connector
* import sqlalchemy
* from sqlalchemy import create_engine
* import pymysql

**pandas, numpy**
* import pandas as pd
* import numpy as np

**Dashboard libraries**
* import streamlit as st
* import plotly.express as px

### 4. E T L Process

#### a) Extract data

* Extract the particular youtube channel data by using the youtube channel id, with the help of the youtube API developer console.

#### b) Process and Transform the data

* After the extraction process, takes the required details from the extraction data and transform it into JSON format.

#### c) Load  data 

* After the transformation process, the JSON format data is stored in the MongoDB database, also It has the option to migrate the data to MySQL database from the MongoDB database.

### 5. E D A Process and Framework

#### a) Access MySQL DB 

* Create a connection to the MySQL server and access the specified MySQL DataBase by using pymysql library and access tables.

#### b) Filter the data

* Filter and process the collected data from the tables depending on the given requirements by using SQL queries and transform the processed data into a DataFrame format.

#### c) Visualization 

* Finally, create a Dashboard by using Streamlit and give dropdown options on the Dashboard to the user and select a question from that menu to analyse the data and show the output in Dataframe Table and Bar chart.


## User Guide

#### Step 1. Data collection zone

* Search **channel_id**, copy and **paste on the input box** and click the **Get data and stored** button in the **Data collection zone**.

#### Step 2. Data Migrate zone

* Select the **channel name** and click the **Migrate to MySQL** button to migrate the specific channel data to the MySQL database from MongoDB in the **Data Migrate zone**.

#### Step 3. Channel Data Analysis zone

* **Select a Question** from the dropdown option you can get the **results in Dataframe format or bar chat format**.


## Video link

* Click the below Image

[![Intro GUI](https://github.com/Gopinathalpha7/YouTube_Data_Harvesting_and_Warehousing./blob/88b80dca65246a606d9495deddad95202c685430/youtube%20data%20harvesting%20gui.png)](https://www.linkedin.com/feed/update/urn:li:activity:7065793132247871488/)
