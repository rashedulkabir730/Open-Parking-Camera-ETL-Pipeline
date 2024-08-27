

import calendar
from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.python import PythonOperator
import pandas as pd
import boto3
from airflow.operators.bash import BashOperator
from sodapy import Socrata

s3_client = boto3.client('s3')

now = datetime.now()
target_bucket = 'cam-transform'
url = 'nc67-uf89'


def extract_data(url ,limit_set=1000000, chunks = 50000):
    client = Socrata("data.cityofnewyork.us", None)
    offset = 0
    #offset for pagination
    data_chunks = []

    while offset < limit_set:
      results = client.get(url, limit=chunks, offset=offset)

      if not results:
        break

      data_chunks.append(pd.DataFrame.from_records(results))
      offset += chunks


    if data_chunks:
      df=pd.concat(data_chunks, ignore_index=True)
    else:
      df = pd.DataFrame()

    file_name = "cam_rev_data"
    df.to_csv(f"{file_name}.csv", index=False)

    output_file_path = f"/home/ubuntu/{file_name}.csv"
    output_list= [file_name, output_file_path]



    return output_list


def transform_data(task_instance):
  data = task_instance.xcom_pull(task_ids='tsk_extract_data')[0]
  object_key = task_instance.xcom_pull(task_ids='tsk_extract_data')[1]

  df = pd.read_csv(data)

  cols = ['plate','state'	,'license_type'	,	'issue_date',
          'violation_time', 'violation'	,
          'fine_amount', 'penalty_amount', 'interest_amount',
          'reduction_amount', 'payment_amount',	'amount_due',
          'precinct', 'county', 'issuing_agency'	, 'violation_status']
  df = df[cols]
  df = df.dropna()

  df['issue_date'] = pd.to_datetime(df['issue_date'])
  df['issuance_year'] = df['issue_date'].dt.year
  df['issuance_month'] = df['issue_date'].dt.month
  df['issuance_month'] = df['issuance_month'].apply(lambda x: calendar.month_abbr[x])

  df['fine_amount'] = pd.to_numeric(df['fine_amount'])
  df['penalty_amount'] = pd.to_numeric(df['penalty_amount'])
  df['interest_amount'] = pd.to_numeric(df['interest_amount'])
  df['reduction_amount'] = pd.to_numeric(df['reduction_amount'])

  df['violation_time'] = df['violation_time'].str.replace(r'(\d{1,2}:\d{2})([AP])', r'\1 \2M', regex=True)
  df['violation_time'] = df['violation_time'].str.replace(r'00:(\d{2}) AM', r'12:\1 AM')

  csv_data = df.to_csv(index=False)
  object_key = f"{object_key}.csv"
  s3_client.put_object(Bucket=target_bucket, Key=object_key, Body=csv_data)




default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': now,
    'email': ['myemail@domain.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=15)
}


with DAG('cam_rev_dag',
         default_args=default_args,
         catchup=False) as dag:

         extract_data = PythonOperator(
             task_id = 'tsk_extract_data',
             python_callable = extract_data,
             op_args=[url]
         )

         transform_data = PythonOperator(
             task_id = 'task_transform',
             python_callable = transform_data
         )

         load_to_s3 = BashOperator(
             task_id = 'tsk_load_to_s3',
             bash_command = 'aws s3 mv {{ ti.xcom_pull(task_ids="tsk_extract_data")[1] }} s3://store-raw-cam-rk'

         )


        extract_data >> transform_data >> load_to_s3
