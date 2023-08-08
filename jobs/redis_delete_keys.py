# ------------------------ imports start ------------------------
from backend.db.connection.redis_connect_to_database import redis_connect_to_database_function
# ------------------------ imports end ------------------------


# ------------------------ individual function start ------------------------
def run_function():
  # ------------------------ connect to redis start ------------------------
  redis_connection = redis_connect_to_database_function()
  redis_keys = redis_connection.keys()
  # ------------------------ connect to redis end ------------------------
  # ------------------------ loop through start ------------------------
  for key in redis_keys:
    redis_value = redis_connection.get(key).decode('utf-8')
    if 'bcooke' not in key.decode('utf-8'):
      redis_connection.delete(key.decode('utf-8'))
  # ------------------------ loop through end ------------------------
  return True
# ------------------------ individual function end ------------------------

# =======================================================================================================================================
# ------------------------ run start ------------------------
if __name__ == "__main__":
  run_function()
# ------------------------ run end ------------------------