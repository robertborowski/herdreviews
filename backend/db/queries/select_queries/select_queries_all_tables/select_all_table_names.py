# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_all_table_names_function(postgres_connection, postgres_cursor):
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT \
                              table_name \
                            FROM \
                              information_schema.tables \
                            WHERE \
                              table_schema='public' AND \
                              table_type='BASE TABLE'\
                            ORDER BY \
                              table_name;")
    # ------------------------ Query END ------------------------
    # ------------------------ Query Result START ------------------------
    # Get the results arr
    result_arr = postgres_cursor.fetchall()
    if result_arr == None or result_arr == []:
      return None
    return result_arr
    # ------------------------ Query Result END ------------------------
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      return None