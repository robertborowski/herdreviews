# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_count_all_table_team_channel_combo_general_function(postgres_connection, postgres_cursor, team_id, channel_id, table_name, table_team_id_column_name, table_channel_id_column_name):
  localhost_print_function('=========================================== select_count_all_table_team_channel_combo_general_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT COUNT(*) FROM {} WHERE {}=%s AND {}=%s;".format(table_name, table_team_id_column_name, table_channel_id_column_name), [team_id, channel_id])
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    result_row = postgres_cursor.fetchone()
    
    if result_row == None or result_row == []:
      localhost_print_function('=========================================== select_count_all_table_team_channel_combo_general_function END ===========================================')
      return None
    
    localhost_print_function('=========================================== select_count_all_table_team_channel_combo_general_function END ===========================================')
    return result_row
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_count_all_table_team_channel_combo_general_function END ===========================================')
      return None