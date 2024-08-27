create warehouse cam_rev_warehouse;

drop database if exists cam_rev_db;
create database cam_rev_db

create schema cam_rev_schema;
SELECT CURRENT_ACCOUNT();
SELECT COUNT(*) FROM cam_rev_db.cam_rev_schema.cam_rev_table;

CREATE OR REPLACE TABLE cam_rev_db.cam_rev_schema.cam_rev_table (
plate STRING,
state STRING,
license_type STRING,
issue_date DATE , 
violation_time STRING , 
violation STRING,
fine_amount FLOAT, 
penalty_amount FLOAT, 
interest_amount FLOAT,
reduction_amount FLOAT, 
payment_amount FLOAT,	
amount_due FLOAT, 
precinct STRING , 
county STRING, 
issuing_agency STRING, 
violation_status STRING,
issuance_year STRING ,
issuance_month STRING)
;


SELECT * FROM cam_rev_db.cam_rev_schema.cam_rev_table;

CREATE SCHEMA file_format_schema;
CREATE OR REPLACE file format cam_rev_db.file_format_schema.format_csv
    type = 'CSV'
    field_delimiter = ','
    RECORD_DELIMITER = '\n'
    skip_header = 1


CREATE SCHEMA external_stage_schema;

CREATE OR REPLACE STAGE cam_rev_db.external_stage_schema.cam_rev_ext_stage
url = 's3://cam-transform/cam_rev_data.csv'
credentials = (aws_key_id = 'xxxx'
aws_secret_key = 'xxxx' )
FILE_FORMAT = cam_rev_db.file_format_schema.format_csv;


CREATE OR REPLACE SCHEMA cam_rev_db.snowpipe_schema;

CREATE OR REPLACE PIPE cam_rev_db.snowpipe_schema.cam_snowpipe
auto_ingest = TRUE
as
COPY into cam_rev_db.cam_rev_schema.cam_rev_table
FROM @cam_rev_db.external_stage_schema.cam_rev_ext_stage;

DESC PIPE cam_rev_db.snowpipe_schema.cam_snowpipe;