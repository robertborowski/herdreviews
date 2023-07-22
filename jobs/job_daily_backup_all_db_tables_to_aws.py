# ------------------------ imports start ------------------------
import os
import datetime
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.select_queries_all_tables.select_triviafy_all_table_names import select_triviafy_all_table_names_function
import boto3
from botocore.exceptions import ClientError
from io import StringIO
import psycopg2
import pandas as pd
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def job_daily_backup_all_db_tables_to_aws_function():
  # ------------------------ AWS Connect Bucket START ------------------------
  # Create AWS s3 client
  s3_resource = boto3.resource('s3')
  s3_bucket_name = os.environ.get('AWS_TRIVIAFY_BACKUP_BUCKET_NAME')
  # ------------------------ AWS Connect Bucket End ------------------------
  # ------------------------ DB Conection START ------------------------
  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ DB Conection End ------------------------
  # ------------------------ SQL Get DB Table Names START ------------------------
  # Get all table names in the current database
  db_table_names_arr = select_triviafy_all_table_names_function(postgres_connection, postgres_cursor)
  # ------------------------ SQL Get DB Table Names END ------------------------
  # ------------------------ Push Info Into AWS s3 START ------------------------
  for table_name_arr in db_table_names_arr:
    # Get table name
    table_name = table_name_arr[0]
    try:
      # ------------------------ Get Individual Table Data START ------------------------
      # Run sql statement on the table and get all row results
      postgres_cursor.execute("SELECT * FROM %s" % table_name)
      result_list = postgres_cursor.fetchall()
      # ------------------------ Get Individual Table Data END ------------------------
      # ------------------------ Get Individual Table Headers START ------------------------
      # Get table headers, store in array
      headers_tuple = postgres_cursor.description
      headers_arr = []
      for i in headers_tuple:
        headers_arr.append(i.name)
      # ------------------------ Get Individual Table Headers END ------------------------
      # Create into pandas dataframe
      df = pd.DataFrame(result_list, columns=headers_arr)
      # Get todays date as string
      todays_date_str = str(datetime.datetime.now().date())
      todays_date = todays_date_str.replace("-","")
      # ------------------------ Upload to AWS s3 as csv START ------------------------
      # Upload pandas df into aws s3
      csv_buffer = StringIO()
      df.to_csv(csv_buffer)
      s3_resource.Object(s3_bucket_name, todays_date + '_' + table_name + '.csv').put(Body=csv_buffer.getvalue())
      # ------------------------ Upload to AWS s3 as csv END ------------------------
    # Except clause
    except (Exception, psycopg2.Error) as error:
      localhost_print_function('error')
      return True
  # ------------------------ Push Info Into AWS s3 END ------------------------
  # ------------------------ DB Close Conection START ------------------------
  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ DB Close Conection END ------------------------
  return True
# ------------------------ individual function end ------------------------


# ------------------------ run function start ------------------------
if __name__ == "__main__":
  job_daily_backup_all_db_tables_to_aws_function()
# ------------------------ run function end ------------------------