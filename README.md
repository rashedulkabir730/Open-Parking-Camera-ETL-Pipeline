# Open-Parking-Camera-ETL-Pipeline
## End-to-End Data Engineering Project 

# Architecture: 

![Blank diagram](https://github.com/user-attachments/assets/5e3f2e54-b905-4781-8078-bf4ce8ee7ae4)


This project demonstrates the development of a robust data engineering pipeline that automates the extraction, transformation, and loading (ETL) of NYC Open Data for parking and camera violations. The pipeline is built using cloud services and orchestration tools, ensuring the data is efficiently processed and made available for visualization and analysis in Power BI.

## Project Overview

The goal of this project was to create an end-to-end pipeline that automates the movement of data from the NYC Open Data API into a Snowflake data warehouse for further analysis and dashboard reporting. The process is orchestrated using Apache Airflow to ensure continuous, automated data flow.

## Pipeline Process

Provisioned AWS EC2 Instance:
Set up a virtual machine to install and configure all necessary dependencies such as Python (Pandas, Sodapy), and Apache Airflow for workflow orchestration.

Data Extraction:
Used the NYC Open Data API to extract parking and camera violation data and store it in an AWS S3 bucket for further processing.

Data Transformation:
Cleaned the data, changed column data types, added and dropped relevant columns, and applied minor adjustments to ensure consistency and accuracy.

Data Loading:
Loaded the transformed data into a separate S3 bucket for staging.

Orchestration with Apache Airflow:
Managed and scheduled the entire ETL process using Apache Airflow to automate the extraction, transformation, and loading of the data.

Snowflake Data Storage:
Created a Snowflake database, schema, and table to store the processed data. Set up a CSV file format and an external stage to ingest the data from S3 into Snowflake.

Snowpipe Automation:
Configured Snowpipe to automate continuous data loading into Snowflake, ensuring near-real-time availability for analysis.

Data Visualization in Power BI:
Imported the processed data into Power BI and created an interactive dashboard displaying key insights and metrics from the violations data.

Technologies Used:
Programming Language: Python (Pandas, Sodapy)
Cloud Infrastructure: AWS EC2, AWS S3
Data Warehouse: Snowflake (Snowpipe)
Orchestration: Apache Airflow
Data Visualization: Power BI


# Dataset Used:
- https://data.cityofnewyork.us/City-Government/Open-Parking-and-Camera-Violations/nc67-uf89/about_data

