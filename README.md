# <div align="center"> YouTube Data Scraping Web Application </font> </div>
</br>

### Introduction

>Welcome to the YouTube Data Scraping Web Application repository!!!
>The YouTube Data Harvesting and Warehousing project is a comprehensive system designed to facilitate the seamless retrieval, storage, and analysis of YouTube channel data. Leveraging state-of-the-art technologies such as SQL, MongoDB, and Streamlit, this project empowers users to access and analyze YouTube channel and video data efficiently and effectively.
</br>

### Table of Contents

- [Overview](#overview)
- [Developer Guide](#developer-guide)
- [User Guide](#user-guide)
- [Conclusion](#conclusion)

</br>

# Overview

> This project aims to provide a comprehensive solution for scraping data from YouTube channels, storing it in a database, and querying it using SQL. It leverages the YouTube Data API, MongoDB, MySQL, and Streamlit to achieve its functionality. The YouTube Data Harvesting and Warehousing project consists of several key components:

### 1. Streamlit Application
   - An intuitive user interface built using the Streamlit library allows users to interact with the application effortlessly. Users can perform complex data retrieval and analysis tasks with ease.

### 2. YouTube API Integration
   - Integration with the YouTube API enables the retrieval of extensive channel and video data based on specified channel IDs. This ensures a robust and reliable data retrieval mechanism.

### 3. MongoDB Data Lake
   - A robust MongoDB database serves as the backbone for storing and managing retrieved data. MongoDB offers exceptional flexibility in handling unstructured and semi-structured data formats.

### 4. SQL Data Warehouse
   - Efficient migration of data from the MongoDB data lake to a SQL database (MySQL) facilitates swift and effective querying and analysis through SQL queries.

### 5. Data Visualization
   - Streamlit's advanced data visualization features are utilized to present retrieved data in an insightful and visually appealing manner. Interactive charts and graphs empower users to derive actionable insights from the data.
</br>


# Developer Guide  

### 1. Tools Installation
   * Virtual code environment
   * Visual Studio Code (or other IDE's)
   * Python 3.11.0 or higher
   * MySQL
   * MongoDB
   * YouTube API key
</br>

### 2. Required Libraries Installation in Visual Studio Code
```python
pip install google-api-python-client
```
```python
pip install pymongo
```
```python
pip install mysql-connector-python
```
```python
pip install pandas
```
```python
pip install streamlit
```
```python
pip install streamlit_option_menu
```
```python
pip install plotly
```
</br>


### 3. Import Libraries
```python
# YouTube API libraries
from googleapiclient.discovery import build

# MongoDB
import pymongo

# SQL libraries
import mysql.connector

# Pandas
import pandas as pd

# Dashboard libraries
import streamlit as st
```
</br>


### 4. ETL Process

a) **Extract Data**
   - Extract specific YouTube channel data using the YouTube channel ID with the YouTube API.

b) **Process and Transform Data**
   - Transform extracted data into JSON format after extraction for further processing.

c) **Load Data**
   - Establish connection to MongoDB using from pymongo import MongoClient python library
   - Store JSON formatted data into the MongoDB database.
   - Establish connection to the MySQL server and access specified MySQL Database using mysql.connector python library .
   - Create a database and tables as mentioned in <i><b>.sql</b></i> file in MySQL.
   - Migrate data from MongoDB to MySQL database
</br>


### 5. EDA Process and Framework

a) **Access MySQL DB**
   - Establish connection to the MySQL server and access specified MySQL Database using mysql.connector python library .

b) **Filter Data**
   - Filter and process collected data from tables based on specified requirements using SQL queries. Transform processed data into DataFrame format.

c) **Visualization**
   - Utilize Streamlit to create a Dashboard with dropdown options for user selection. Analyze selected data and display results in DataFrame Table and Bar chart formats.
</br>

## User Guide
<p>To effectively utilize the YouTube Data Harvesting and Warehousing system, follow these steps:
</br>

1. **Data Collection Zone**
</br>

![Data Scraping Page](https://github.com/BalaKrishnanCodeSpace/YouTube_Data_Harvesting/raw/main/Data%20Scraping%20Page.JPG)
   - Input the API key created to fetch the Youtube channel data into the designated field.
   - Input the channel ID into the designated field.
   - Click the "Scrape Data" button to retrieve and store channel data.
   - Results will be shown if successfully scraped the Youtube channel data.
</br>

2. **Data Migration Zone**
</br>

![Data Migration](https://github.com/BalaKrishnanCodeSpace/YouTube_Data_Harvesting/raw/main/Data%20Migration.JPG)
   - Click the "Upload to MongoDB" button to store the channel data into MongoDB
   - Click the "Upload to MySQL" button to transfer channel data from MongoDB to MySQL.
</br>

3. **Channel Data Analysis Zone**
</br>

![SQL Queries](https://github.com/BalaKrishnanCodeSpace/YouTube_Data_Harvesting/raw/main/SQL%20Queries.JPG)
   - Utilize the dropdown menu to select a specific analysis question.
   - View and analyze data results in either DataFrame or Bar chart formats.
</br>

## Conclusion

>The YouTube Data Harvesting and Warehousing project provides a powerful solution for analyzing YouTube channel data efficiently. With its integration of advanced technologies and user-friendly interfaces, this project enables users to derive valuable insights from YouTube data for various purposes including business analytics, content creation strategies, and market research.
