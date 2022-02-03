# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_triviafy_emails_sent_table_count_account_created_emails_per_team_channel_function(postgres_connection, postgres_cursor, team_id, channel_id, email_sent_search_category):
  localhost_print_function('=========================================== select_triviafy_emails_sent_table_count_account_created_emails_per_team_channel_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT COUNT(*) FROM triviafy_emails_sent_table AS e LEFT JOIN triviafy_user_login_information_table_slack AS l ON e.email_sent_to_user_uuid_fk=l.user_uuid WHERE l.user_slack_workspace_team_id=%s AND l.user_slack_channel_id=%s AND e.email_sent_category=%s", [team_id, channel_id, email_sent_search_category])
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    result_row = postgres_cursor.fetchone()
    
    if result_row == None or result_row == []:
      localhost_print_function('=========================================== select_triviafy_emails_sent_table_count_account_created_emails_per_team_channel_function END ===========================================')
      return None

    localhost_print_function('=========================================== select_triviafy_emails_sent_table_count_account_created_emails_per_team_channel_function END ===========================================')
    return result_row[0]
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_triviafy_emails_sent_table_count_account_created_emails_per_team_channel_function END ===========================================')
      return None