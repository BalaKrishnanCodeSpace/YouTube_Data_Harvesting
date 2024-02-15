# YouTube Data Scraping Web Application

## Introduction

>Welcome to the YouTube Data Scraping Web Application repository!The YouTube Data Harvesting and Warehousing project is a comprehensive system designed to facilitate the seamless retrieval, storage, and analysis of YouTube channel data. Leveraging state-of-the-art technologies such as SQL, MongoDB, and Streamlit, this project empowers users to access and analyze YouTube channel and video data efficiently and effectively.

## Table of Contents

- [Overview](#overview)
- [Developer Guide](#developer-guide)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

# Overview

>This project aims to provide a comprehensive solution for scraping data from YouTube channels, storing it in a database, and querying it using SQL. It leverages the YouTube Data API, MongoDB, MySQL, and Streamlit to achieve its functionality. The YouTube Data Harvesting and Warehousing project consists of several key components:

## 1. Streamlit Application

>An intuitive user interface built using the Streamlit library allows users to interact with the application effortlessly. Users can perform complex data retrieval and analysis tasks with ease.

## 2. YouTube API Integration

>Integration with the YouTube API enables the retrieval of extensive channel and video data based on specified channel IDs. This ensures a robust and reliable data retrieval mechanism.

## 3. MongoDB Data Lake

>A robust MongoDB database serves as the backbone for storing and managing retrieved data. MongoDB offers exceptional flexibility in handling unstructured and semi-structured data formats.

## 4. SQL Data Warehouse

>Efficient migration of data from the MongoDB data lake to a SQL database (MySQL) facilitates swift and effective querying and analysis through SQL queries.

## 5. Data Visualization

>Streamlit's advanced data visualization features are utilized to present retrieved data in an insightful and visually appealing manner. Interactive charts and graphs empower users to derive actionable insights from the data.
<br>
<br>

# Developer Guide  

## 1. Tools Installation
   * Virtual code environment
   * Visual Studio Code (or other IDE's)
   * Python 3.11.0 or higher
   * MySQL
   * MongoDB
   * YouTube API key

## 2. Required Libraries Installation in Visual Studio Code
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

## 3. Import Libraries
```python
# YouTube API libraries
from googleapiclient.discovery import build

# File handling libraries
import re

# MongoDB
import pymongo

# SQL libraries
import mysql.connector

# Pandas, numpy
import pandas as pd

# Dashboard libraries
import streamlit as st
```

## 4. ETL Process

a) **Extract Data**
   - Extract specific YouTube channel data using the YouTube channel ID with the YouTube API.

b) **Process and Transform Data**
   - Transform extracted data into JSON format after extraction for further processing.

c) **Load Data**
   - Store JSON formatted data into the MongoDB database. Optionally, migrate data from MongoDB to MySQL database


## 5. EDA Process and Framework

a) **Access MySQL DB**
   - Establish connection to the MySQL server and access specified MySQL Database using pymysql library.

b) **Filter Data**
   - Filter and process collected data from tables based on specified requirements using SQL queries. Transform processed data into DataFrame format.

c) **Visualization**
   - Utilize Streamlit to create a Dashboard with dropdown options for user selection. Analyze selected data and display results in DataFrame Table and Bar chart formats.


## User Guide

**Step 1. Data Collection Zone**

- Enter the channel ID in the input box and click the "Get data and stored" button to retrieve and store channel data.

**Step 2. Data Migrate Zone**
- Select the channel name and click the "Migrate to MySQL" button to migrate channel data from MongoDB to MySQL.

**Step 3. Channel Data Analysis Zone**
- Choose a question from the dropdown menu to analyze data and view results in DataFrame format or Bar chart format.







## Features

- **Data Scraping**: Retrieve data from one or more YouTube channels using the YouTube Data API.
- **Data Storage**: Store the scraped data in a MongoDB database for temporary storage.
- **Data Migration**: Transfer the data from MongoDB to a MySQL database for long-term storage.
- **SQL Queries**: Perform various SQL queries on the MySQL database to extract insights from the data.
- **Streamlit Web Interface**: Access the application through a user-friendly Streamlit web interface.

## Installation

To run the application locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/youtube-data-scraping.git
