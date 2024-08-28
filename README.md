# Open-Parking-Camera-ETL-Pipeline
## End-to-End Data Engineering Project 

# Architecture: 

![Blank diagram](https://github.com/user-attachments/assets/5e3f2e54-b905-4781-8078-bf4ce8ee7ae4)


# Process:
- created a EC2 instance VM and installed all of the needed dependencies, which included Python Pandas, Sodapy, Apache Airflow and more
- then extracted data using the NYC Open Data API into an S3 bucket.
- transformed the data, which included changing data types, adding columns, dropping columns and making minor edits.
- this transformed data then loaded a new s3 bucket.
- this process was orchestrated by Apache Airflow
- I then created a Snowflake database, schema, and table for storing the  data. Then, you defined a CSV file format, set up an external stage to access a CSV file from S3
- created a Snowpipe to be able to access the data in Power Bi
- Imported Data from snowflake to Power BI and created a dashboard with relevent metrics

# Technologies Used:

Programming Language
- Python
AWS:
- EC2 Instance
- S3 Buckets
Snowflake:
- Snowpipe
Power Bi
Orchestrator:
-Apache Airflow

# Dataset Used:
- https://data.cityofnewyork.us/City-Government/Open-Parking-and-Camera-Violations/nc67-uf89/about_data

