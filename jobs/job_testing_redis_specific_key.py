# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.connection.redis_connect_to_database import redis_connect_to_database_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.polling import select_manual_function
# ------------------------ imports end ------------------------


# ------------------------ individual function start ------------------------
def run_function():
  # ------------------------ open connection start ------------------------
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ open connection end ------------------------
  # ------------------------ select start ------------------------
  db_all_users_arr_of_dict = select_manual_function(postgres_connection, postgres_cursor, 'select_all_user_ids')
  # ------------------------ select end ------------------------
  # ------------------------ close connection start ------------------------
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ close connection end ------------------------
  # ------------------------ connect to postgres start ------------------------
  # Connect to redis database pool (no need to close) 
  redis_connection = redis_connect_to_database_function()
  redis_keys = redis_connection.keys()
  # ------------------------ connect to postgres end ------------------------
  # ------------------------ all redis keys, store in counted dict, delete if doesnt exist start ------------------------
  counter = 0
  id_counter_dict = {}
  for key in redis_keys:
    counter += 1
    redis_value = redis_connection.get(key).decode('utf-8')
    print(f'key: {key} | value: {redis_value}')
    if redis_value not in id_counter_dict:
      id_counter_dict[redis_value] = 1
    else:
      id_counter_dict[redis_value] += 1
    # ------------------------ find user start ------------------------
    exists_in_db = False
    db_current_email = ''
    for i_dict in db_all_users_arr_of_dict:
      if i_dict['id'] == redis_value:
        exists_in_db = True
        db_current_email = i_dict['email']
    # ------------------------ find user end ------------------------
    if exists_in_db == True:
      pass
    else:
      redis_connection.delete(key)
      print(f'deleted: {redis_value}')
  localhost_print_function(counter)
  # ------------------------ all redis keys, store in counted dict, delete if doesnt exist end ------------------------
  # ------------------------ loop through counted dict to see who is logged in multiple browsers start ------------------------
  print(' ------------------- ')
  counter = 0
  for k,v in id_counter_dict.items():
    counter += 1
    if v > 1:
      # ------------------------ find user start ------------------------
      exists_in_db = False
      db_current_email = ''
      for i_dict in db_all_users_arr_of_dict:
        if i_dict['id'] == k:
          exists_in_db = True
          db_current_email = i_dict['email']
      # ------------------------ find user end ------------------------
      print(f'db_current_email: {db_current_email} <----------------------------')
      print(f'k: {k} | v: {v} <----------------------------')
      print(' ')
    else:
      pass
  localhost_print_function(counter)
  # ------------------------ loop through counted dict to see who is logged in multiple browsers end ------------------------
  return True
# ------------------------ individual function end ------------------------

# =======================================================================================================================================
# ------------------------ run start ------------------------
if __name__ == "__main__":
  run_function()
# ------------------------ run end ------------------------